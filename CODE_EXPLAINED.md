# Code explained: every file, how it works

Read this side by side with the code. For each file it explains what the file does, why it is built that way, how it works step by step, and what to say if the professor asks. Both of you should know **every** file, not only your own.

---

## 0. The big picture

```
 ehr-srv01 (Ubuntu)                                   ws-admin01 (Windows)
 ──────────────────                                   ────────────────────
 generate_patients.py → patients.csv                  user action / Atomic Red Team test
          │                                                    │
 ehr_app.py serves records, writes JSON audit line    Sysmon records process + LSASS events
          │                                                    │
 Wazuh agent: reads JSON log + FIM on records         Wazuh agent: reads Sysmon + PowerShell logs
          └──────────────── port 1514, encrypted ───────────────┘
                                     │
                    Wazuh manager: decoders → local_rules.xml
                                     │
                     ALERT (e.g. 100103, level 12) → analyst → IR playbook + NIS2/GDPR clocks
```

Say it in one sentence: *an event is recorded, the agent ships it, the manager decodes it and matches our rules, and the alert starts the response.*

---

## 1. `scripts/generate_patients.py`: the synthetic patient data

**Purpose.** It creates 500 invented patients, about 1,300 hospital stays and about 2,000 lab results as three CSV files. Using real patient data would violate GDPR (Art. 9 special-category data; Art. 5(1)(c) data minimisation).

| Code | What it does | Why |
| --- | --- | --- |
| `FIRST`, `LAST`, `STREETS`, … | Lists the values are drawn from | Realistic-looking but invented |
| `DIAGNOSES` | Real ICD-10 codes (e.g. `I10` hypertension) | The data looks clinical |
| `LAB_TESTS` | Test code, name, unit, normal low, normal high | Lets us compute H/L flags |
| `rnd = random.Random(seed)` | A private random generator with a fixed seed (42) | **Reproducible**: same seed, identical files |
| `pid = f"SYN-P{i:06d}"` | IDs like `SYN-P000001` (6 digits, zero-padded) | `SYN-` marks every record as synthetic |
| `dob = today - timedelta(days=…)` | A birth date up to 95 years back | Ages 0 to 95 |
| `"+49 30 5550…"` | Phone numbers in the 555 range | A fictional range, so they are never real numbers |
| The encounter loop `for _ in range(rnd.randint(1, 4))` | 1–4 stays per patient | Models the 1→n relationship |
| The lab loop `range(rnd.randint(0, 3))` | 0–3 results per stay | The second 1→n level |
| `patient_id` / `encounter_id` in the child rows | Point to the parent row | Act as **foreign keys**, like a database |
| `val = rnd.uniform(lo * 0.7, hi * 1.4)` | Values from 70% to 140% of the normal range | Some results are abnormal on purpose |
| `"flag": "H" if val > hi else ("L" if val < lo else "")` | High/low flag | Computed from the range, not random |
| `csv.DictWriter(…, fieldnames=list(rows[0].keys()))` | Writes a header plus the rows | The column order follows the dictionary keys |
| `argparse` with `-n`, `-s`, `-o` | Command-line options | `setup_ehr.sh` uses `-o /srv/ehr/records` |

**Likely questions.**
- *Why not Faker?* It would be one more dependency on every VM. The stdlib plus a seed is enough.
- *How realistic is the data?* It is realistic in **structure** (fields, relationships, volume) but not in **statistics** (the diagnoses are uniformly random).

---

## 2. `lab/ehr-server/ehr_app.py`: the mini hospital record system

**Purpose.** A small web server plays the hospital's EHR. It serves the synthetic patients and writes **one JSON line per request** to an audit log. Wazuh reads that log, which is how attacks on patient data become alerts.

### Imports

`base64` decodes the login header, `csv` reads and writes data, `io.StringIO` builds the export in memory, `json` writes the log lines, `datetime` adds UTC timestamps, `http.server` is the built-in web server, and `urllib.parse` splits the URL and query string. There are no external libraries.

### `USERS`

```python
USERS = {"dr.weber": ("Clinic-Lab-2026!", "clinician"), ..., "it.admin": ("Admin-Lab-2026!", "admin")}
```

Each user has a password and a **role**, which gives role-based access control (RBAC): only `admin` may export. *Weakness:* the passwords are in plain text in the code. That is acceptable only in the lab. See the Defence Prep doc, section 10.1, for the hashed-password fix.

### `class EHR(BaseHTTPRequestHandler)`

The built-in server creates one handler object per request and calls `do_GET()` for GET requests. `patients` and `log_path` are **class attributes**, so all requests share them: the data is loaded once at start.

- `log_message()` is overridden to stay silent; we write our own log instead.
- `_audit(user, action, status, records, detail)` builds a dictionary (`timestamp` in UTC ISO format, `app`, `src_ip` from `self.client_address[0]`, `user`, `action`, `path`, `status`, `records`, `detail`). It writes it as one JSON line, a format called *JSON Lines*. This is what Wazuh's `json` log reader expects.
- `_send(code, body, ctype)` sends the status, `Content-Type` and `Content-Length` headers and the body. It encodes strings to bytes first.
- `_auth()` handles HTTP **Basic** auth:
  1. It reads the `Authorization: Basic xxx` header.
  2. `base64.b64decode` turns `xxx` into `user:password`. Base64 is encoding, **not** encryption.
  3. `split(":", 1)` splits only at the first colon, so a password may contain colons.
  4. If the pair matches `USERS`, it returns `(user, role)`. Otherwise it logs `login_failed` and returns `(None, None)`.
  5. A malformed header is caught by `except` and treated as not logged in.

### `do_GET()`: routing

1. `urlparse(self.path)` splits `/search?q=sch` into the path `/search` and the query `q=sch`.
2. `/health` needs no login, so monitoring can check that the service is up.
3. All other paths call `_auth()`. Without valid credentials the server replies **401** with a `WWW-Authenticate` header, which makes a browser show a login box.
4. The endpoints:

| Path | Code | Logged action | Detection rule |
| --- | --- | --- | --- |
| `/patients/<id>` | `self.patients.get(pid)`, then 200 or 404 | `view_record` | 100105 when 30+ in 60 s (scraping) |
| `/search?q=` | `parse_qs` reads `q`; last names starting with `q`; `[:20]` caps the hits | `search` | via 100100 |
| `/export` as clinician | role check, then 403 | `export_denied` | 100104 |
| `/export` as admin | `csv.DictWriter` into `io.StringIO`, returned as `text/csv` | `bulk_export` + record count | **100103 (level 12)** |
| anything else | 404 | none | none |

### `main()`

1. `argparse` reads `--data`, `--log` and `--port`.
2. The patients are loaded into a **dictionary keyed by `patient_id`**: `{r["patient_id"]: r for r in csv.DictReader(f)}`. Lookup is O(1).
3. The log folder is created with `mkdir(parents=True, exist_ok=True)`.
4. `ThreadingHTTPServer(("0.0.0.0", port), EHR)` listens on all network interfaces and handles each request in its own thread.

**The key idea to explain.** The app logs **business events** (who exported how many patient records), not just HTTP hits. A web-server access log would only show `GET /export 200`. This is application-level audit logging, required for GDPR accountability (Art. 5(2)) and for detecting data theft.

---

## 3. `lab/ehr-server/setup_ehr.sh` and `restore_ehr.sh`

| Line | What it does | Why |
| --- | --- | --- |
| `set -euo pipefail` | `-e`: stop at the first error; `-u`: error on unset variables; `pipefail`: a pipe fails if any part fails | A half-installed server is worse than a clear error |
| `REPO="$(cd "$(dirname "$0")/../.." && pwd)"` | Finds the repo root from the script's own location | The script works from any folder |
| `generate_patients.py -n 500 -o /srv/ehr/records` | Writes the data where the app reads it | |
| `useradd --system --no-create-home --shell /usr/sbin/nologin ehr` | A service account that cannot log in | **Least privilege**: a hacked app gets a powerless user, not root |
| `cp … /srv/ehr/backup/` | A clean copy of the data | Lets us restore after tests |
| `chown -R ehr:ehr …` | The service account owns only its own files | Least privilege |
| systemd unit, `User=ehr`, `Restart=on-failure` | Runs the app as a service that restarts on crashes | |
| `systemctl enable --now` | Starts the service now and on every boot | |
| `curl …/health` | Smoke test | Proves the install worked |

`restore_ehr.sh` stops the service, deletes the current records, copies the backup back, fixes ownership and restarts. It is the **Recover** function in miniature. The VM snapshot is the full-size version.

---

## 4. `lab/wazuh/agent-linux.conf` and `agent-windows.conf`

- **`<localfile><log_format>json</log_format>`** makes the Linux agent read the EHR log line by line. The manager's JSON decoder turns each key into a field (`action`, `user`, …) that rules can match.
- **`<syscheck><directories realtime="yes" check_all="yes">/srv/ehr/records`** is **file integrity monitoring (FIM)**. Wazuh records a hash and the attributes of every file and reports within seconds (Linux inotify) when one is added, changed or deleted. Scheduled scans run every 12 h by default, which is far too late for ransomware.
- **Windows `eventchannel` blocks** read `Microsoft-Windows-Sysmon/Operational` and `Microsoft-Windows-PowerShell/Operational`.
  - Sysmon event 1 is **process creation with the full command line**.
  - Sysmon event 10 is **process access**, for example a process opening LSASS.
  - The default Windows logs contain neither, which is why we install Sysmon.

---

## 5. `lab/wazuh/local_rules.xml`: the detections

### How a Wazuh rule works

```xml
<rule id="100103" level="12">                 <!-- unique ID (custom: 100000+) and severity 0-15 -->
  <if_sid>100100</if_sid>                      <!-- only checked if parent rule 100100 matched -->
  <field name="action">bulk_export</field>     <!-- decoded JSON field must match (regex) -->
  <description>... $(records) records by $(user) ...</description>   <!-- $(x) inserts field values -->
  <mitre><id>T1213</id></mitre>               <!-- ATT&CK tag for the MITRE dashboard -->
  <group>ehr,data_exfiltration,</group>       <!-- groups for filtering -->
</rule>
```

**Correlation rules** count events:

```xml
<rule id="100102" level="10" frequency="8" timeframe="60">
  <if_matched_sid>100101</if_matched_sid>   <!-- count matches of rule 100101 ... -->
  <same_field>src_ip</same_field>           <!-- ... only from the same source IP -->
```

Read it as: *8 failed logins from the same IP within 60 seconds.* (Wazuh's `frequency` has an off-by-one quirk in some versions; check the real count with your tests.)

### Rule by rule

| Rule | Level | Fires when | Technique | Reasoning |
| --- | --- | --- | --- | --- |
| 100100 | 3 | Any EHR log line (`app` = `aurelia-ehr`) | none | Parent of all EHR rules |
| 100101 | 5 | `login_failed` | T1110 | One typo is normal |
| 100102 | 10 | 8 failures in 60 s from one IP | T1110 | Scripts fail fast; humans don't. Also catches **password spraying** across many users |
| 100103 | 12 | `bulk_export` | T1213 | The data-theft step of double extortion |
| 100104 | 8 | Non-admin tried to export | none | A policy violation, or a stolen clinician account probing |
| 100105 | 10 | 30+ requests in 60 s by one user | T1213 | Catches slow record-by-record scraping that avoids the export rule |
| 100200 | 7 | FIM: a record file modified (parent 550) | none | The record store rarely changes |
| 100201 | 7 | FIM: a new file in the record store (parent 554) | none | Same |
| 100202 | 13 | 3+ modifications in 120 s | T1486 | Ransomware touches many files fast; our highest alert |
| 100203 | 12 | New file named like readme/recover/decrypt/restore .txt/.html | T1486 | Ransom-note naming patterns |
| 100300 | 12 | Sysmon 10: LSASS opened with a memory-read access mask | T1003.001 | LSASS holds credentials; few legitimate readers |
| 100301 | 12 | Command line deletes shadow copies or backups | T1490 | Ransomware does this right before encrypting |
| 100302 | 8 | `schtasks /create` | T1053.005 | Persistence; admins do it too, so a medium level |
| 100303 | 10 | PowerShell `-enc` / `downloadstring` / `iex(` | T1059.001 | Hidden or downloaded code |
| 100304 | 12 | Access to the Chrome/Edge `Login Data` file | T1555.003 | The exact Qilin technique Sophos documented |
| 100305 | 12 | Windows event 1102: security log cleared | T1070.001 | Attackers covering their tracks |

**Regex details:**
- `type="pcre2"` means Perl-compatible regex.
- `(?i)` makes it case-insensitive.
- `^` and `$` anchor the start and end.
- `\\lsass\.exe$` means "the path ends in \lsass.exe".

**LSASS access masks.** `grantedAccess` is a bitmask of the rights requested. `0x1010`, `0x1410` and the others include `PROCESS_VM_READ` (read the other process's memory). Credential dumpers need exactly that right on LSASS.

**Parent IDs.**
- 550 and 554 are the built-in FIM rules.
- 61603 and 61612 are Sysmon event 1 and event 10.
- 60000 is the Windows base rule.

Check them with `/var/ossec/bin/wazuh-logtest`, because IDs can differ between Wazuh versions.

---

## 6. `scripts/iocs_to_stix.py`: sharing threat intelligence

**Purpose.** It turns `cti/iocs.csv` into a **STIX 2.1** bundle: the standard JSON format for sharing CTI with CERTs, ISACs or MISP.

| Code | Meaning |
| --- | --- |
| `PATTERNS` | Maps an IOC type to a STIX pattern, e.g. `[ipv4-addr:value = '10.10.50.21']` |
| `sid(kind)` | Builds a STIX ID: `type--uuid4` |
| `identity` | Who produced the intelligence (our CSIRT, sector healthcare) |
| `intrusion-set` | The actor, Qilin, with alias Agenda and motivation `personal-gain` |
| An `indicator` per CSV row | Pattern plus `valid_from` and `indicator_types: malicious-activity` |
| `relationship` "indicates" | Links each indicator to Qilin; this link makes a list into intelligence |
| `TLP_CLEAR` | The official STIX marking-definition ID for TLP:CLEAR (free to share) |
| `.replace("'", "\\'")` | Escapes quotes so the pattern stays valid |

**Pyramid of Pain.** File names and IPs are easy for an attacker to change, while TTPs are hard to change. So our *detections* focus on behaviour, and the IOCs are a supplement.

`cti/navigator-layer.json` is a layer for the MITRE ATT&CK Navigator. Each technique carries a `score` (1 = tabletop only, 2 = emulated in the lab) and a `comment` with the scenario step and our rule. Load it, take a screenshot, and recolour by result after the emulation.

---

## 7. `scripts/setup_github.py`: the GitHub setup

| Function | What it does |
| --- | --- |
| `run(cmd)` | Runs a command, or only prints it with `--dry-run`. It stops with the error message if a command fails |
| `preflight()` | Checks that `git` and `gh` are installed, that you are logged in, and that your git identity is set. It returns your GitHub username from `gh api user` |
| `init_and_push()` | Runs `git init` and the first commit if needed, then `gh repo create --private --source . --push` (or only pushes if the repo already exists) |
| `invite()` | Calls the GitHub REST API `PUT /repos/{owner}/{repo}/collaborators/{user}` with `permission=push` (write access) |
| `labels_and_milestones()` | `gh label create --force` (creates or updates); milestones through the API, skipping existing ones |
| `issues()` | Reads `project/user-stories.json` and creates one issue per story (story, owner, due date, acceptance-criteria checkboxes, labels, milestone), skipping titles that already exist |

Every step is **idempotent**, so running the script twice does not create duplicates.

---

## 8. Data and CTI files at a glance

| File | Format | Content |
| --- | --- | --- |
| `data/synthetic/*.csv` | CSV | 500 patients, about 1,300 encounters, about 2,000 lab results (seed 42) |
| `data/assets.csv` | CSV | 11 assets: zone, data class, criticality 1–5, lab stand-in |
| `data/risk-register.csv` | CSV | 8 risks, likelihood × impact (1–5 each); 15+ High, 20+ Critical |
| `cti/attack-mapping.csv` | CSV | 15 techniques: stage, tactic, Qilin evidence, emulated or not, rule ID, result |
| `cti/iocs.csv` | CSV | IOCs with type, value, source, TLP |
| `emulation/run-log.csv` | CSV | One row per test: time, technique, host, result, alert time |
| `evidence/timeline-template.csv` | CSV | The incident timeline, rebuilt from the logs |
| `ir/raci.csv` | CSV | Who is Responsible, Accountable, Consulted or Informed per activity |
| `ir/decision-log.csv` | CSV | Tabletop decisions with time and rationale |
| `project/user-stories.json` | JSON | The 23 user stories behind the GitHub issues |
