# User stories

Each task on the board is written as a user story with acceptance criteria. `scripts/setup_github.py` turns these into GitHub issues, one per story, with labels and milestones.

| ID | Owner | Due | Story |
| --- | --- | --- | --- |
| T01 | Both | 2026-11-08 | As a team member, I want to know the exact course requirements, so that we size the report, slides and demo correctly. |
| T02 | Both | 2026-11-08 | As a team member, I want one private repo we both can push to, so that our work and individual contributions are in one place. |
| T03 | Arjun | 2026-11-08 | As a hospital CISO, I want a clear profile of St. Aurelia Klinikum, so that every later analysis has a concrete organisation to protect. |
| T04 | Tejas | 2026-11-08 | As a hospital board member, I want to understand why hospitals are attacked, so that I support the security budget. |
| T05 | Arjun | 2026-11-09 | As a risk manager, I want a network diagram, asset list and risk register, so that I can see the crown jewels and the biggest risks. |
| T06 | Tejas | 2026-11-09 | As a CTI analyst, I want a Qilin actor profile and Diamond Model, so that defenders know who attacks us and how. |
| T07 | Tejas | 2026-11-10 | As a SOC analyst, I want the attack chain mapped to MITRE ATT&CK with IOCs, so that I know which techniques to detect. |
| T08 | Arjun | 2026-11-11 | As a SOC analyst, I want a working lab with Wazuh, a Windows PC with Sysmon and the EHR server, so that we can test detections on real telemetry. |
| T09 | Arjun | 2026-11-11 | As a SOC analyst, I want custom detection rules that fire on attacks against patient data, so that we catch data theft and ransomware early. |
| T10 | Tejas | 2026-11-10 | As a hospital CSIRT, I want our IOCs as a STIX 2.1 bundle, so that we can share intelligence with CERTs and other hospitals. |
| T11 | Tejas | 2026-11-12 | As a SOC analyst, I want the Qilin-style techniques emulated in the isolated lab, so that we measure which attacks we detect. |
| T12 | Tejas | 2026-11-13 | As a incident response team, I want realistic tabletop injects and role cards, so that we practise decisions under pressure. |
| T13 | Arjun | 2026-11-13 | As a forensic analyst, I want an incident timeline rebuilt from logs, so that we know exactly what happened and when. |
| T14 | Arjun | 2026-11-13 | As a incident lead, I want a ransomware playbook based on NIST SP 800-61r3, so that the team knows who does what during an attack. |
| T15 | Both | 2026-11-14 | As a hospital management, I want to rehearse the incident in a tabletop exercise, so that we find gaps before a real attack. |
| T16 | Tejas | 2026-11-13 | As a Data Protection Officer, I want a NIS2 and GDPR notification timeline with drafts, so that we meet the 24 h, 72 h and one-month deadlines. |
| T17 | Both | 2026-11-15 | As a examiner, I want each chapter written by its owner, so that individual contributions are clear. |
| T18 | Both | 2026-11-16 | As a hospital CISO, I want lessons learned with prioritised recommendations, so that we know what to fix first. |
| T19 | Tejas | 2026-11-16 | As a examiner, I want one consistent, edited report, so that it reads as one piece of work. |
| T20 | Arjun | 2026-11-16 | As a audience, I want a clear 15-minute slide deck, so that we understand the project quickly. |
| T21 | Arjun | 2026-11-17 | As a presenter, I want a backup demo video, so that the presentation works even if the live demo fails. |
| T22 | Both | 2026-11-19 | As a presenter, I want two mock Q&A rounds and a timed rehearsal, so that we can answer any question on the code and project. |
| T23 | Both | 2026-11-20 | As a team member, I want to submit everything on time, so that we get graded. |

## Acceptance criteria

### T01 (Both, due 2026-11-08)
As a **team member**, I want **to know the exact course requirements**, so that **we size the report, slides and demo correctly**.

- [ ] Word limit, slide count, presentation time and demo expectation noted
- [ ] Citation style and submission format noted
- [ ] Requirements section added to report/outline.md

### T02 (Both, due 2026-11-08)
As a **team member**, I want **one private repo we both can push to**, so that **our work and individual contributions are in one place**.

- [ ] Private GitHub repo created and code pushed
- [ ] Arjun accepted the collaborator invite
- [ ] Both cloned the repo and pushed a test commit

### T03 (Arjun, due 2026-11-08)
As a **hospital CISO**, I want **a clear profile of St. Aurelia Klinikum**, so that **every later analysis has a concrete organisation to protect**.

- [ ] Size, departments, systems and vendors described
- [ ] Patient data flow written
- [ ] Regulatory status (NIS2 important entity, GDPR Art. 9) stated
- [ ] Numbers consistent with report and slides

### T04 (Tejas, due 2026-11-08)
As a **hospital board member**, I want **to understand why hospitals are attacked**, so that **I support the security budget**.

- [ ] Three case studies cited from sources you opened (Duesseldorf, Change Healthcare, Synnovis)
- [ ] ENISA health threat report added
- [ ] Qilin confirmed as modelled actor; technique list sent to Arjun

### T05 (Arjun, due 2026-11-09)
As a **risk manager**, I want **a network diagram, asset list and risk register**, so that **I can see the crown jewels and the biggest risks**.

- [ ] Network diagram exported as PNG
- [ ] data/assets.csv and data/risk-register.csv reviewed
- [ ] 5x5 risk heat map figure created

### T06 (Tejas, due 2026-11-09)
As a **CTI analyst**, I want **a Qilin actor profile and Diamond Model**, so that **defenders know who attacks us and how**.

- [ ] Actor profile with at least 4 sources
- [ ] All four Diamond features and meta-features filled
- [ ] Lab values added after the emulation

### T07 (Tejas, due 2026-11-10)
As a **SOC analyst**, I want **the attack chain mapped to MITRE ATT&CK with IOCs**, so that **I know which techniques to detect**.

- [ ] cti/attack-mapping.csv checked
- [ ] Navigator layer loaded and screenshot saved
- [ ] cti/iocs.csv up to date

### T08 (Arjun, due 2026-11-11)
As a **SOC analyst**, I want **a working lab with Wazuh, a Windows PC with Sysmon and the EHR server**, so that **we can test detections on real telemetry**.

- [ ] All three VMs on the isolated network
- [ ] Both agents Active in the dashboard
- [ ] EHR /health returns ok
- [ ] clean-baseline snapshots taken
- [ ] Screenshot evidence/screenshots/agents-active.png

### T09 (Arjun, due 2026-11-11)
As a **SOC analyst**, I want **custom detection rules that fire on attacks against patient data**, so that **we catch data theft and ransomware early**.

- [ ] local_rules.xml installed
- [ ] Defender tests in lab/README.md step 6 pass
- [ ] Screenshot of every rule that fired
- [ ] Dashboard filtered on rule.groups: aurelia

### T10 (Tejas, due 2026-11-10)
As a **hospital CSIRT**, I want **our IOCs as a STIX 2.1 bundle**, so that **we can share intelligence with CERTs and other hospitals**.

- [ ] scripts/iocs_to_stix.py run
- [ ] cti/stix-bundle.json validated or imported into MISP

### T11 (Tejas, due 2026-11-12)
As a **SOC analyst**, I want **the Qilin-style techniques emulated in the isolated lab**, so that **we measure which attacks we detect**.

- [ ] Rules of engagement followed (isolated network, snapshot before and after)
- [ ] Every lab technique has a line in emulation/run-log.csv
- [ ] Result Detected / Partly / Missed recorded
- [ ] Run log handed to Arjun the same day

### T12 (Tejas, due 2026-11-13)
As a **incident response team**, I want **realistic tabletop injects and role cards**, so that **we practise decisions under pressure**.

- [ ] 10 injects final and aligned with the playbook
- [ ] Role cards shared

### T13 (Arjun, due 2026-11-13)
As a **forensic analyst**, I want **an incident timeline rebuilt from logs**, so that **we know exactly what happened and when**.

- [ ] evidence/timeline.csv has a row per emulated step
- [ ] Time to detect calculated per technique
- [ ] Each row links to an evidence file

### T14 (Arjun, due 2026-11-13)
As a **incident lead**, I want **a ransomware playbook based on NIST SP 800-61r3**, so that **the team knows who does what during an attack**.

- [ ] Phases, steps and owners final
- [ ] RACI table final
- [ ] Communication tree included
- [ ] Draft sent to Tejas

### T15 (Both, due 2026-11-14)
As a **hospital management**, I want **to rehearse the incident in a tabletop exercise**, so that **we find gaps before a real attack**.

- [ ] Exercise run (about 90 min)
- [ ] Every inject has a decision in ir/decision-log.csv
- [ ] Debrief answers written

### T16 (Tejas, due 2026-11-13)
As a **Data Protection Officer**, I want **a NIS2 and GDPR notification timeline with drafts**, so that **we meet the 24 h, 72 h and one-month deadlines**.

- [ ] BSIG section numbers checked in the official text
- [ ] Deadlines calculated from the tabletop T0
- [ ] BSI, authority and patient notices filled

### T17 (Both, due 2026-11-15)
As a **examiner**, I want **each chapter written by its owner**, so that **individual contributions are clear**.

- [ ] Tejas: Ch. 1, 2, 4, 7
- [ ] Arjun: Ch. 3, 5, 6
- [ ] Written in our own words with citations

### T18 (Both, due 2026-11-16)
As a **hospital CISO**, I want **lessons learned with prioritised recommendations**, so that **we know what to fix first**.

- [ ] Findings table: finding, evidence, recommendation, NIS2 Art. 21 measure, priority
- [ ] Risk register updated

### T19 (Tejas, due 2026-11-16)
As a **examiner**, I want **one consistent, edited report**, so that **it reads as one piece of work**.

- [ ] Chapters merged, numbers consistent
- [ ] References complete
- [ ] Executive summary written last
- [ ] PDF exported

### T20 (Arjun, due 2026-11-16)
As a **audience**, I want **a clear 15-minute slide deck**, so that **we understand the project quickly**.

- [ ] Follows slides/outline.md
- [ ] Figures match the report
- [ ] Speaker split agreed

### T21 (Arjun, due 2026-11-17)
As a **presenter**, I want **a backup demo video**, so that **the presentation works even if the live demo fails**.

- [ ] 2-3 min recording: export, alert 100103, FIM test, alert 100202
- [ ] Stored on cloud drive, link in README

### T22 (Both, due 2026-11-19)
As a **presenter**, I want **two mock Q&A rounds and a timed rehearsal**, so that **we can answer any question on the code and project**.

- [ ] Each explained the other's code without notes
- [ ] Timed rehearsal within the limit
- [ ] Slides checked against report

### T23 (Both, due 2026-11-20)
As a **team member**, I want **to submit everything on time**, so that **we get graded**.

- [ ] Report, slides and appendices submitted
- [ ] Confirmation saved
- [ ] git tag v1.0-submitted pushed
