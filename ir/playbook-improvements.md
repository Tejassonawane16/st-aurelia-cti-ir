# Playbook improvements: plan vs. simulation (owner: Arjun)

Assignment step 8: *"Compare the planned response with the simulation results and improve the playbook based on the gaps found."*

Fill this in **after** the tabletop (Mon 16 Nov), in your own words. Use:

- `ir/decision-log.csv` (what you decided, and when)
- `evidence/results/detection_matrix.csv` (what was detected or missed)
- `ir/playbook.md` (what the plan said)

## 1. Planned vs. actual

| Playbook step | What the plan said | What happened in the simulation (time, decision) | Gap? |
| --- | --- | --- | --- |
| 1.1 Triage within 30 min | | | |
| 1.5 Start the regulatory clocks | | | |
| 2.1 Isolate hosts | | | |
| 2.4 Take the EHR offline (clinical lead) | | | |
| 2.7 Ransom decision | | | |
| 3 Recovery order | | | |
| Communication (press, staff, patients) | | | |

## 2. Gaps from the detection results

Questions to answer for each gap:

- What did the analyst *not* see?
- What would that have changed in the response?
- What is your fix?

| Gap | Impact on the response | Improvement | Owner | Priority |
| --- | --- | --- | --- | --- |
| Domain discovery (T1087.002) not detected | | | | |
| Exfiltration upload (T1048) not detected | | | | |
| False positive on the backup task (rule 100302) | | | | |
| Initial VPN login not visible (no VPN logs) | | | | |
| Alerts outside office hours (first alert at 17:40 Fri) | | | | |

## 3. Changes made to `ir/playbook.md`

List each change with its commit ID:

-
-
