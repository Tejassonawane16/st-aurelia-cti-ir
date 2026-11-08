# Tabletop exercise: "Operation Black Ward" (owner: Tejas; run together Sat 14 Nov, about 90 min)

**Format.** Tejas is the facilitator and reads each inject aloud at the time shown. The players decide what to do. Arjun logs every decision in `ir/decision-log.csv`. With only two people, Arjun plays the incident lead and Tejas voices the other roles from `ir/tabletop/roles.md`, or you can invite 2–3 classmates.

**Scenario time** starts on a Friday at 17:40, after office hours, because the SIEM is only watched 8–17.

| # | Exercise min | Scenario time | Inject (read aloud) | Questions for players | Expected good answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | Fri 17:40 | An on-call IT engineer sees a Wazuh email: "Sysmon: process opened LSASS memory" on an admin PC in Billing. | Real or false positive? Who do you call? | Triage per playbook 1.1; isolate the PC; call the incident lead |
| 2 | 10 | Fri 18:30 | Wazuh rule 100103: FULL patient export, 500 records, by account `it.admin` from that same PC. The admin is on holiday. | Is this an incident? What severity? Do any clocks start? | Declare Sev 1; disable the account; **the NIS2 24 h and GDPR 72 h clocks start now** |
| 3 | 20 | Fri 19:15 | VPN logs show `it.admin` logged in 19 days ago from an IP in another country. MFA was never enrolled for this account. | What does this tell you about scope? What else has this account touched? | Assume wide compromise; reset privileged accounts; hunt for persistence |
| 4 | 30 | Sat 02:10 | Night-shift nurses report: "the EHR shows errors, files are unreadable". Ransom notes appear on the file server. | Take the EHR offline? Who decides? | Clinical lead agrees; switch to paper procedures; cut admin-to-clinical routing |
| 5 | 40 | Sat 03:00 | The emergency department asks whether to divert ambulances: there are no lab results and no previous records. | Divert or not? Who informs the fire brigade? | Clinical lead decides; a partial diversion (stroke, trauma) is reasonable; document it |
| 6 | 50 | Sat 09:00 | An email from "Qilin": 500 GB of patient data stolen, pay USD 2 M in 72 h or it gets published. Sample attached: real patient names. | Pay? Who decides? Does this change the GDPR assessment? | No payment (policy); involve the police; high risk to individuals, so plan Art. 34 notices |
| 7 | 60 | Sat 14:00 | A journalist from a Berlin newspaper calls the press office about "a cyberattack on St. Aurelia". | What do you say? | Prepared holding statement; no technical detail; patients' safety first |
| 8 | 70 | Sat 17:30 | It is now 23 h since inject 2. | Has the BSI early warning been sent? What does it contain? | Early warning via the BSI portal before 24 h: suspected cause, possible cross-border impact |
| 9 | 80 | Mon 09:00 | Backups: the NAS is encrypted too, but Thursday's offline tape is intact. | Restore order? What about data entered on paper since Thursday? | AD, then EHR, then lab interface; reconcile paper records; verify the hosts are clean first |
| 10 | 85 | +4 weeks | The leak site publishes the data. | What now? | Patient helpline; update the Art. 34 notices; send the final NIS2 report within one month |

## Debrief (last 10–15 min)

For each question, write one sentence in `ir/decision-log.csv`:

1. What did we detect, and how late?
2. Which decision was hardest, and why?
3. Which control would have stopped this earliest? (Expected answer: MFA on every VPN account.)
4. Did we meet every regulatory deadline?
