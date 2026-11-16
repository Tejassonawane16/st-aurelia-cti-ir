# Tejas: Student 1, threat intelligence and detection

**Your role per the assignment:** assets, threat scenario, threat and indicator summary, likely impact, and detection. You also merge the final report.

## New files in this pack

| File | What it is |
| --- | --- |
| `scripts/make_sample_logs.py` | Writes **safe sample logs** of the scenario (EHR, Sysmon-style, FIM) plus the ground truth. No attack is run |
| `scripts/detect.py` | Replays logs through our 16 rules (same IDs as `local_rules.xml`); writes `alerts.csv` and `detection_matrix.csv` |
| `scripts/ehr_tests.py` | Five test cases against our own EHR app running on your laptop |
| `cti/threat-model.md` | The 4-question framework, FIPS 199, STRIDE, policy vs. mechanism, applied to our EHR |

## Order of work

1. Unzip into the repo, then `git switch -c tejas/t07-detection`.
2. Run the commands in section 2 of the Final Week Plan doc and screenshot the outputs.
3. Commit, push, open a PR and merge it. **Then tell Arjun to `git pull`**, so he can reproduce the run.
4. Review and adapt `cti/threat-model.md`, then commit.
5. Mon: condense report Ch. 2, 4 and 5 into the 3–5-page format; run the tabletop at 19:00.
6. Tue: your slides; TryHackMe; Presentation 1.
7. Wed: merge the report; the integration call (explain Arjun's part).
8. Thu: rehearse, export the PDF, submit by 20:30.

## Be able to explain (the professor may ask)

- **How `detect.py` works:**
  - `Window` is a sliding time window per key (IP or user). It fires when *n* events fall inside *t* seconds, then resets, just like Wazuh's `frequency`/`timeframe`.
  - Every rule is an `if` on decoded fields: the same logic as the XML rules.
- **Why sample logs and not real attacks:** the assignment allows safe sample logs. They are reproducible and contain known ground truth, so we can *measure* detection: 9 of 11 detected, 2 missed, 1 false positive.
- **Limitation:** sample logs are written by us, so they test the *rule logic*, not real-world noise. The live EHR test and the optional Wazuh lab add realism.
