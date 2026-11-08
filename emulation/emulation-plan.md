# Adversary emulation plan (owner: Tejas, run on Thu 12 Nov)

**Goal:** check whether St. Aurelia's detections catch a Qilin-style intrusion, and produce timestamped evidence for the incident timeline.

**Tooling:** [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) with its PowerShell runner Invoke-AtomicRedTeam. This is Red Canary's open-source library of small, documented tests, one per ATT&CK technique. Follow the project's own install and usage documentation, then list the available tests for a technique before choosing one. Read each test's description and its cleanup step before you run it.

## Rules of engagement

These apply to every run:

1. Run tests **only** on `ws-admin01` and `ehr-srv01`, and only while their adapters are on the Internal Network `aurelia-lab`, which has no internet.
2. Before starting, revert both VMs to the `clean-baseline` snapshot.
3. Arjun watches the Wazuh dashboard live during the run.
4. Log every test in `emulation/run-log.csv` **at the moment you run it**: UTC time, technique, test name, host, result. This log is what Arjun's timeline is built from.
5. Run each test's cleanup afterwards. Revert to the snapshot at the end of the day.
6. Never run these tests on a university, work or personal machine outside the lab.

## Scenario stages and what we test

The stages follow the Qilin intrusion Sophos documented in 2024 (see `cti/actor-profile-qilin.md`). Stages marked *tabletop only* are not emulated in the lab. They enter the scenario as injects (`ir/tabletop/injects.md`).

| # | Stage | ATT&CK technique | In the lab? | Telemetry source | Our rule |
| --- | --- | --- | --- | --- | --- |
| 1 | Credentials phished; VPN login without MFA | T1566.002, T1078, T1133 | Tabletop only | VPN logs (not in lab) | n/a |
| 2 | Password guessing against the EHR | T1110 | Yes: defender test in `lab/README.md` | EHR JSON log | 100101, 100102 |
| 3 | PowerShell execution and discovery | T1059.001, T1087.002 | Yes: Atomic test | Sysmon event 1, PowerShell log | 100303 |
| 4 | Persistence with a scheduled task | T1053.005 | Yes: Atomic test | Sysmon event 1 | 100302 |
| 5 | Browser credential store accessed | T1555.003 | Yes: Atomic test | Sysmon event 1 | 100304 |
| 6 | LSASS memory access | T1003.001 | Yes: Atomic test (Defender may block it, which is also a finding) | Sysmon event 10 | 100300 |
| 7 | Group Policy abused to push scripts | T1484.001 | Tabletop only (no domain controller in the lab) | n/a | n/a |
| 8 | Bulk theft of patient data | T1213, T1048 | Yes: admin export test in `lab/README.md` | EHR JSON log | 100103, 100105 |
| 9 | Event logs cleared | T1070.001 | Yes: Atomic test | Windows Security 1102 | 100305 |
| 10 | Shadow copies deleted | T1490 | Yes: Atomic test | Sysmon event 1 | 100301 |
| 11 | Patient records encrypted | T1486 | Simulated by the FIM change test, **not** real encryption | Wazuh FIM | 100200, 100202 |

## After the run

- For each row, record **Detected / Partly detected / Missed** and the alert time in `emulation/run-log.csv`. A missed detection is a valid finding for chapter 8.
- Hand the run log to Arjun the same evening. He matches each line to its alert to build `evidence/timeline.csv`.
- Update the `lab_result` column in `cti/attack-mapping.csv`.
