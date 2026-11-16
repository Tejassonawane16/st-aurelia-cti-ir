#!/usr/bin/env python3
"""Write SAFE SAMPLE LOGS of the St. Aurelia incident scenario (no attack is executed).

The assignment allows "safe sample logs, alerts, or simulated evidence". This script writes
synthetic log events in the same formats our sources produce:
  - EHR audit log lines (exactly like lab/ehr-server/ehr_app.py writes them)
  - Sysmon / Windows Security events (simplified JSON)
  - File-integrity-monitoring (FIM) events
It also writes the scenario's ground truth (what the attacker did, and when), so that
scripts/detect.py can measure what was detected, what was missed and what was a false alarm.

Benign background activity (clinicians at work, a legitimate backup task) is mixed in on
purpose, so the detection test also shows false positives.

Usage:  python3 scripts/make_sample_logs.py           -> evidence/sample-logs/
"""
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "evidence" / "sample-logs"
T0 = datetime(2026, 11, 13, 16, 40, 0, tzinfo=timezone.utc)   # Fri 17:40 Berlin time
WS, EHR = "ws-admin01", "ehr-srv01"
ATTACKER_WS_IP = "10.10.50.21"     # the compromised admin workstation
EXFIL_IP = "203.0.113.50"          # RFC 5737 documentation address, never a real host


def ts(minutes, seconds=0):
    return (T0 + timedelta(minutes=minutes, seconds=seconds)).isoformat(timespec="seconds")


def ehr(t, user, action, status, records=0, path="/", detail="", ip=ATTACKER_WS_IP):
    return {"timestamp": t, "app": "aurelia-ehr", "src_ip": ip, "user": user, "action": action,
            "path": path, "status": status, "records": records, "detail": detail}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ehr_lines, events, truth = [], [], []

    # ---------- benign background activity ----------
    for i, m in enumerate([2, 9, 17, 26, 41, 55]):
        pid = f"SYN-P{100 + i:06d}"
        ehr_lines.append(ehr(ts(m), "dr.weber", "view_record", 200, 1, f"/patients/{pid}", pid, ip="10.10.30.15"))
    ehr_lines.append(ehr(ts(13), "nurse.koch", "search", 200, 4, "/search?q=mue", "mue", ip="10.10.30.16"))
    ehr_lines.append(ehr(ts(14), "nurse.koch", "login_failed", 401, ip="10.10.30.16"))   # one typo: normal
    events.append({"timestamp": ts(-10), "source": "sysmon", "host": WS, "event_id": 1,
                   "image": r"C:\Windows\System32\schtasks.exe", "user": "HOSPITAL\\svc_backup",
                   "command_line": r'schtasks /create /tn "NightlyBackup" /tr "C:\Backup\run.cmd" /sc daily /st 03:00'})
    events.append({"timestamp": ts(1), "source": "sysmon", "host": WS, "event_id": 1,
                   "image": r"C:\Program Files\Google\Chrome\Application\chrome.exe", "user": "HOSPITAL\\it.admin",
                   "command_line": r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'})

    # ---------- the attack (ground truth) ----------
    def step(n, minute, technique, name, expected_rule, observable=True):
        truth.append({"step": n, "time": ts(minute), "technique": technique, "action": name,
                      "expected_rule": expected_rule, "observable_in_logs": "yes" if observable else "no"})

    step(1, 0, "T1133/T1078", "VPN login with phished credentials (no MFA)", "", observable=False)

    step(2, 12, "T1110", "Password guessing against the EHR from the workstation", "100102")
    for s in range(10):
        ehr_lines.append(ehr(ts(12, s * 3), "dr.weber", "login_failed", 401, path="/patients/SYN-P000001"))

    step(3, 21, "T1059.001", "Encoded PowerShell command", "100303")
    events.append({"timestamp": ts(21), "source": "sysmon", "host": WS, "event_id": 1,
                   "image": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe", "user": "HOSPITAL\\it.admin",
                   "command_line": "powershell.exe -NoProfile -EncodedCommand SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQA"})

    step(4, 23, "T1087.002", "Domain admin group enumerated", "")
    events.append({"timestamp": ts(23), "source": "sysmon", "host": WS, "event_id": 1,
                   "image": r"C:\Windows\System32\net.exe", "user": "HOSPITAL\\it.admin",
                   "command_line": 'net group "Domain Admins" /domain'})

    step(5, 25, "T1555.003", "Chrome saved-password database copied", "100304")
    events.append({"timestamp": ts(25), "source": "sysmon", "host": WS, "event_id": 1,
                   "image": r"C:\Windows\System32\cmd.exe", "user": "HOSPITAL\\it.admin",
                   "command_line": r'cmd /c copy "C:\Users\it.admin\AppData\Local\Google\Chrome\User Data\Default\Login Data" C:\Users\Public\ld.db'})

    step(6, 29, "T1003.001", "LSASS memory read by an unknown process", "100300")
    events.append({"timestamp": ts(29), "source": "sysmon", "host": WS, "event_id": 10,
                   "source_image": r"C:\Users\Public\svc.exe", "target_image": r"C:\Windows\System32\lsass.exe",
                   "granted_access": "0x1010", "user": "HOSPITAL\\it.admin"})

    step(7, 35, "T1053.005", "Scheduled task created for persistence", "100302")
    events.append({"timestamp": ts(35), "source": "sysmon", "host": WS, "event_id": 1,
                   "image": r"C:\Windows\System32\schtasks.exe", "user": "HOSPITAL\\it.admin",
                   "command_line": r'schtasks /create /tn "Updater" /tr "C:\Users\Public\svc.exe" /sc onlogon'})

    step(8, 50, "T1213", "All patient records exported from the EHR", "100103")
    ehr_lines.append(ehr(ts(50), "it.admin", "bulk_export", 200, 500, "/export"))

    step(9, 54, "T1048", "Export uploaded to an external server", "")
    events.append({"timestamp": ts(54), "source": "sysmon", "host": WS, "event_id": 3,
                   "image": r"C:\Users\Public\svc.exe", "user": "HOSPITAL\\it.admin",
                   "destination_ip": EXFIL_IP, "destination_port": 443})

    step(10, 8 * 60 + 18, "T1070.001", "Security event log cleared", "100305")
    events.append({"timestamp": ts(8 * 60 + 18), "source": "security", "host": WS, "event_id": 1102,
                   "user": "HOSPITAL\\it.admin"})

    step(11, 8 * 60 + 22, "T1490", "Shadow copies deleted", "100301")
    events.append({"timestamp": ts(8 * 60 + 22), "source": "sysmon", "host": WS, "event_id": 1,
                   "image": r"C:\Windows\System32\vssadmin.exe", "user": "HOSPITAL\\it.admin",
                   "command_line": "vssadmin delete shadows /all /quiet"})

    step(12, 8 * 60 + 30, "T1486", "Patient record files changed + ransom note (simulated)", "100202")
    for i, f in enumerate(["patients.csv", "encounters.csv", "lab_results.csv"]):
        events.append({"timestamp": ts(8 * 60 + 30, i * 5), "source": "fim", "host": EHR,
                       "event": "modified", "path": f"/srv/ehr/records/{f}"})
    events.append({"timestamp": ts(8 * 60 + 30, 20), "source": "fim", "host": EHR,
                   "event": "added", "path": "/srv/ehr/records/README_RECOVER.txt"})

    ehr_lines.sort(key=lambda e: e["timestamp"])
    events.sort(key=lambda e: e["timestamp"])
    (OUT / "ehr_audit.jsonl").write_text("\n".join(json.dumps(e) for e in ehr_lines) + "\n", encoding="utf-8")
    (OUT / "host_events.jsonl").write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
    with open(OUT / "ground_truth.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(truth[0].keys()))
        w.writeheader()
        w.writerows(truth)
    print(f"Wrote {len(ehr_lines)} EHR lines, {len(events)} host events and {len(truth)} ground-truth steps to {OUT}")


if __name__ == "__main__":
    main()
