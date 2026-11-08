# Report outline (target about 6,000–8,000 words; confirm the limit in task T01)

| Ch. | Title | Owner | Source files in this repo | Key figures and tables |
| --- | --- | --- | --- | --- |
| – | Executive summary (1 page) | Tejas (last, on day 8) | all | — |
| 1 | Introduction and methodology | Tejas draft, Arjun review | README.md, emulation/emulation-plan.md | Method diagram |
| 2 | Healthcare threat landscape | Tejas | cti/threat-landscape.md | Case-study table |
| 3 | The simulated organization | Arjun | docs/hospital-profile.md, docs/network-diagram.md, data/assets.csv, data/risk-register.csv | Network diagram, asset table, risk heat map |
| 4 | Threat intelligence | Tejas | cti/actor-profile-qilin.md, cti/diamond-model.md, cti/attack-mapping.csv, cti/navigator-layer.json, cti/iocs.csv | Diamond Model, ATT&CK Navigator screenshot, IOC table |
| 5 | Simulation and detection | Arjun (Tejas writes the emulation subsection) | lab/README.md, emulation/run-log.csv, evidence/ | Lab diagram, detection results table, alert screenshots, incident timeline |
| 6 | Incident response and tabletop exercise | Arjun | ir/playbook.md, ir/raci.csv, ir/tabletop/, ir/decision-log.csv | RACI, inject table, decision log |
| 7 | Privacy and regulatory response | Tejas | compliance/ | Notification timeline, notification excerpts |
| 8 | Lessons learned and recommendations | Both | debrief notes, risk register | Detected vs missed table, prioritised recommendations mapped to NIS2 Art. 21 measures |
| 9 | Conclusion | Both | — | — |
| A–D | Appendices: IOC list / STIX, playbook, notification drafts, evidence timeline | Both | cti/, ir/, compliance/, evidence/ | — |

**Writing rules:**
- Use the same names and numbers everywhere: 400 beds, 2,400 staff, 500 synthetic patients.
- Every claim about the simulation points to a figure or log.
- Use a single citation style; confirm which one in T01.
