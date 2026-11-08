# St. Aurelia Klinikum: CTI and Incident Response Simulation

**Data Security & Privacy, MSc Cybersecurity. Team: Tejas and Arjun. Presentation and submission: Fri 20 Nov 2026.**

A fictional 400-bed Berlin hospital is hit by a Qilin-style double-extortion ransomware attack. The project has five parts:

1. Profile the threat with cyber threat intelligence (ATT&CK, the Diamond Model, IOCs, STIX).
2. Emulate parts of the attack in an isolated lab with Wazuh, Sysmon and a mini EHR holding **synthetic** patient data.
3. Detect the attack and rebuild its timeline from the logs.
4. Respond using NIST SP 800-61r3 and a tabletop exercise.
5. Handle the GDPR and NIS2 reporting duties.

## Start here

| If you want to… | Open |
| --- | --- |
| Put the project on GitHub (repo, Arjun, issues) | [SETUP_GITHUB.md](SETUP_GITHUB.md) |
| Understand how every piece of code works | [CODE_EXPLAINED.md](CODE_EXPLAINED.md) |
| See the tasks as user stories | [USER_STORIES.md](USER_STORIES.md) |
| Know what to do, and why, for every task | [TASKS.md](TASKS.md) |
| Know what to push to git | [GIT_GUIDE.md](GIT_GUIDE.md) |
| Build the lab | [lab/README.md](lab/README.md) |
| Run the attack emulation | [emulation/emulation-plan.md](emulation/emulation-plan.md) |
| Write the report | [report/outline.md](report/outline.md) |

## Repository layout

```
docs/          hospital profile, network diagram                        (Arjun)
data/          synthetic patients, asset list, risk register           (Arjun; data generator: both)
cti/           threat landscape, Qilin profile, Diamond Model,
               ATT&CK mapping + Navigator layer, IOCs, STIX bundle      (Tejas)
lab/           Wazuh rules + agent configs, mini EHR server + setup     (Arjun)
emulation/     emulation plan, run log                                  (Tejas)
ir/            playbook, RACI, decision log, tabletop injects + roles   (Arjun; tabletop: Tejas)
compliance/    NIS2 + GDPR timeline, BSI / authority / patient notices  (Tejas)
evidence/      screenshots, sanitised logs, incident timeline           (both)
report/        report outline and chapters                              (both)
slides/        deck outline and deck                                    (Arjun)
scripts/       generate_patients.py, iocs_to_stix.py, setup_github.py
project/       user-stories.json (source for the GitHub issues)
```

## Quick commands

```bash
python3 scripts/generate_patients.py      # regenerate the synthetic patients (seed 42, 500 patients)
python3 scripts/iocs_to_stix.py           # cti/iocs.csv -> cti/stix-bundle.json
python3 scripts/setup_github.py --arjun <user>   # private repo + invite + 23 issues (SETUP_GITHUB.md)
sudo bash lab/ehr-server/setup_ehr.sh     # on the Ubuntu lab VM: install the mini EHR
sudo bash lab/ehr-server/restore_ehr.sh   # restore the EHR records after a test
```

All scripts use only the Python 3 standard library, so there is nothing to `pip install`.

## Ground rules

- **Synthetic data only.** No real patient data, or real personal data of any kind, ever enters this repo.
- **Attack tests run only in the isolated lab network.** See the rules of engagement in `emulation/emulation-plan.md`.
- **No secrets in git.** See `GIT_GUIDE.md`.
- The `.md` drafts in `cti/`, `docs/`, `ir/` and `compliance/` are starting points. Check every source and write the report in your own words.
