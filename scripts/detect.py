#!/usr/bin/env python3
"""Replay safe sample logs through the St. Aurelia detection rules (no Wazuh needed).

The rules are the same as lab/wazuh/local_rules.xml (same IDs, levels and ATT&CK tags),
written in Python so they run on any laptop. Wazuh remains the production design; this
replay is how we test the detection logic on safe sample logs.

Usage:
  python3 scripts/detect.py                          # scenario sample logs + ground truth
  python3 scripts/detect.py --ehr evidence/sample-logs/ehr_live.jsonl --no-truth
                                                     # a real log from the running EHR app
Outputs (in evidence/results/): alerts.csv, detection_matrix.csv (with ground truth)
"""
import argparse
import csv
import json
import re
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "evidence" / "sample-logs"
RESULTS = ROOT / "evidence" / "results"

LSASS_MASKS = {"0x1010", "0x1410", "0x1438", "0x143a", "0x1fffff"}
SHADOW_DELETE = re.compile(r"(vssadmin.*delete.*shadows|wmic.*shadowcopy.*delete|wbadmin.*delete.*catalog|"
                           r"bcdedit.*recoveryenabled.*no)", re.I)
PS_SUSPICIOUS = re.compile(r"(-enc\b|-encodedcommand|downloadstring|iex\s*\()", re.I)
BROWSER_STORE = re.compile(r"\\(Google\\Chrome|Microsoft\\Edge)\\User Data\\.*Login Data", re.I)
RANSOM_NOTE = re.compile(r"^/srv/ehr/records/.*(readme|recover|decrypt|restore).*\.(txt|html)$", re.I)


def t(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


class Window:
    """Correlation helper: fires when `count` matches with the same key fall inside `seconds`."""

    def __init__(self, count, seconds):
        self.count, self.seconds, self.q = count, seconds, defaultdict(deque)

    def hit(self, key, when):
        q = self.q[key]
        q.append(when)
        while q and (when - q[0]).total_seconds() > self.seconds:
            q.popleft()
        if len(q) >= self.count:
            q.clear()          # like Wazuh: fire once, then start counting again
            return True
        return False


def load(path):
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            e = json.loads(line)
            if e.get("app") == "aurelia-ehr":
                e.setdefault("source", "ehr")
                e.setdefault("host", "ehr-srv01")
            out.append(e)
    return out


def detect(events):
    alerts = []
    w_fail, w_scrape, w_fim = Window(8, 60), Window(30, 60), Window(3, 120)

    def alert(e, rule, level, technique, desc):
        alerts.append({"time": e["timestamp"], "rule": rule, "level": level, "technique": technique,
                       "host": e.get("host", ""), "description": desc})

    for e in sorted(events, key=lambda x: x["timestamp"]):
        when, src = t(e["timestamp"]), e.get("source")
        if src == "ehr":                                                     # parent rule 100100
            a, user, ip = e.get("action"), e.get("user"), e.get("src_ip")
            if a == "login_failed":
                alert(e, 100101, 5, "T1110", f"EHR failed login for {user} from {ip}")
                if w_fail.hit(ip, when):
                    alert(e, 100102, 10, "T1110", f"8+ failed EHR logins in 60 s from {ip}")
            if a == "account_locked":
                alert(e, 100106, 10, "T1110", f"EHR account {user} locked from {ip}")
            if a == "bulk_export":
                alert(e, 100103, 12, "T1213", f"FULL patient export ({e.get('records')} records) by {user} from {ip}")
            if a == "export_denied":
                alert(e, 100104, 8, "", f"Export attempt by non-admin {user} from {ip}")
            if w_scrape.hit(user, when):
                alert(e, 100105, 10, "T1213", f"30+ EHR requests in 60 s by {user}")
        elif src == "fim" and e.get("path", "").startswith("/srv/ehr/records"):
            if e.get("event") == "modified":
                alert(e, 100200, 7, "", f"EHR record file modified {e['path']}")
                if w_fim.hit("records", when):
                    alert(e, 100202, 13, "T1486", "Several record files changed within 2 min - possible ransomware")
            if e.get("event") == "added":
                alert(e, 100201, 7, "", f"New file in EHR record store {e['path']}")
                if RANSOM_NOTE.search(e["path"]):
                    alert(e, 100203, 12, "T1486", f"Ransom-note style file {e['path']}")
        elif src == "sysmon" and e.get("event_id") == 10:
            if e.get("target_image", "").lower().endswith("\\lsass.exe") and e.get("granted_access", "").lower() in LSASS_MASKS:
                alert(e, 100300, 12, "T1003.001", f"{e.get('source_image')} opened LSASS memory")
        elif src == "sysmon" and e.get("event_id") == 1:
            img, cmd = e.get("image", "").lower(), e.get("command_line", "")
            if SHADOW_DELETE.search(cmd):
                alert(e, 100301, 12, "T1490", f"Backup/shadow-copy deletion: {cmd}")
            if img.endswith("\\schtasks.exe") and "/create" in cmd.lower():
                alert(e, 100302, 8, "T1053.005", f"Scheduled task created by {e.get('user')}: {cmd}")
            if img.endswith("\\powershell.exe") and PS_SUSPICIOUS.search(cmd):
                alert(e, 100303, 10, "T1059.001", "Suspicious PowerShell (encoded or download cradle)")
            if BROWSER_STORE.search(cmd):
                alert(e, 100304, 12, "T1555.003", "Process touching browser saved-password store")
        elif src == "security" and e.get("event_id") == 1102:
            alert(e, 100305, 12, "T1070.001", "Security event log cleared")
    return alerts


def matrix(alerts, truth_rows):
    rows = []
    for s in truth_rows:
        exp = s["expected_rule"]
        start = t(s["time"])
        hits = [a for a in alerts if exp and str(a["rule"]) == exp and t(a["time"]) >= start]
        if s["observable_in_logs"] == "no":
            result, first, ttd = "Not observable (no log source)", "", ""
        elif hits:
            first = hits[0]["time"]
            result, ttd = "Detected", int((t(first) - start).total_seconds())
        else:
            result, first, ttd = "Missed (no rule)", "", ""
        rows.append({**s, "result": result, "first_alert": first, "time_to_detect_s": ttd})
    return rows


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ehr", default=str(SAMPLES / "ehr_audit.jsonl"), help="EHR audit log (JSON lines)")
    ap.add_argument("--events", default=str(SAMPLES / "host_events.jsonl"), help="host/FIM events (JSON lines)")
    ap.add_argument("--truth", default=str(SAMPLES / "ground_truth.csv"))
    ap.add_argument("--no-truth", action="store_true", help="only list alerts (e.g. for a live EHR log)")
    ap.add_argument("--out", default=str(RESULTS))
    a = ap.parse_args()

    events = load(a.ehr)
    if not a.no_truth and Path(a.events).exists():
        events += load(a.events)
    alerts = detect(events)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "alerts.csv", alerts)

    print(f"\n{len(events)} events in, {len(alerts)} alerts out\n")
    print(f"{'TIME (UTC)':<26}{'RULE':<8}{'LVL':<5}{'ATT&CK':<11}DESCRIPTION")
    for x in alerts:
        if x["level"] >= 8:      # show what an analyst must look at; all alerts are in alerts.csv
            print(f"{x['time']:<26}{x['rule']:<8}{x['level']:<5}{x['technique']:<11}{x['description'][:70]}")

    if a.no_truth:
        print(f"\nAlerts written to {out / 'alerts.csv'}")
        return
    with open(a.truth, encoding="utf-8") as f:
        rows = matrix(alerts, list(csv.DictReader(f)))
    write_csv(out / "detection_matrix.csv", rows)
    observable = [r for r in rows if r["observable_in_logs"] == "yes"]
    detected = [r for r in observable if r["result"] == "Detected"]
    print(f"\nDETECTION MATRIX: {len(detected)} of {len(observable)} observable attack steps detected")
    for r in rows:
        ttd = f" ({r['time_to_detect_s']} s)" if r["time_to_detect_s"] != "" else ""
        print(f"  step {r['step']:>2}  {r['technique']:<12} {r['result']}{ttd}  - {r['action']}")
    fp = [x for x in alerts if x["rule"] == 100302 and "svc_backup" in x["description"]]
    if fp:
        print(f"\nFALSE POSITIVES: {len(fp)} - rule 100302 fired on the legitimate NightlyBackup task "
              f"(tune: exclude the backup service account)")
    print(f"\nWritten: {out / 'alerts.csv'} and {out / 'detection_matrix.csv'}")


if __name__ == "__main__":
    main()
