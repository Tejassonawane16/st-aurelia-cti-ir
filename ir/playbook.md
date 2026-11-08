# Ransomware and data-theft incident response playbook (owner: Arjun)

**Framework.** NIST SP 800-61 Rev. 3 (April 2025) replaces Rev. 2. It ties incident response to the six NIST CSF 2.0 functions:

- **Govern, Identify and Protect** are the preparation work done before an incident.
- **Detect, Respond and Recover** are the work during and after an incident.

This playbook uses the last three as its phases. Source: [NIST CSRC](https://csrc.nist.gov/pubs/sp/800/61/r3/final).

**Trigger.** Any of these Wazuh alerts starts the playbook:

- 100103 bulk export
- 100202 or 100203 mass file change or ransom note
- 100300 LSASS access
- 100301 shadow-copy deletion

The playbook also starts on a ransom note or an extortion email.

## 0. Preparation (Govern / Identify / Protect)

- [ ] Contact list for the IR team, the DFIR retainer, BSI, the data protection authority and the police (LKA Berlin cybercrime unit). Keep a printed copy, because email may be down.
- [ ] Offline backup tested in the last 90 days.
- [ ] Clinical downtime procedures (paper forms, lab order slips) are in every ward.
- [ ] Out-of-band communication channel prepared, such as a Signal group.

## 1. Detect and analyse

| Step | Action | Owner | Time target |
| --- | --- | --- | --- |
| 1.1 | Triage the alert: real or false positive? Check the host, user, time and related alerts in Wazuh | On-duty IT security | 30 min |
| 1.2 | Declare an incident and open a log (`ir/decision-log.csv`) with a UTC timeline | Incident lead | at declaration |
| 1.3 | Scope: which hosts and accounts are affected? Was patient data accessed or exported? (EHR audit log, rule 100103) | Security analyst | 2 h |
| 1.4 | Classify severity. **Sev 1** = clinical systems unavailable or patient data exfiltrated | Incident lead + CISO | 2 h |
| 1.5 | **Start the regulatory clocks**: when we become aware of a significant incident, the NIS2 24-hour early warning and the GDPR 72-hour deadline begin (`compliance/notification-timeline.md`) | DPO + CISO | at awareness |

## 2. Respond: contain, eradicate

| Step | Action | Clinical impact to weigh |
| --- | --- | --- |
| 2.1 | Isolate the affected hosts with the EDR or by switch port. **Do not power them off**, because memory evidence would be lost | Low |
| 2.2 | Disable the compromised accounts; force a password reset for privileged accounts; revoke VPN sessions | Medium: staff locked out |
| 2.3 | Block the exfiltration IPs and domains at the firewall; add them to `cti/iocs.csv` | Low |
| 2.4 | Decide whether to cut the admin-to-clinical routing or take the EHR offline. **The clinical lead must agree** | **High: switch to paper processes** |
| 2.5 | Preserve evidence: memory images, disk images, logs, with a chain-of-custody form | None |
| 2.6 | Eradicate: remove persistence (scheduled tasks, GPOs), reset the krbtgt account twice, rebuild the affected hosts from known-good images | Medium |
| 2.7 | Ransom: hospital policy is **not to pay**. The board decides with legal advice and the police | n/a |

## 3. Recover

1. Restore from offline backups in priority order: identity (AD), then the EHR, then the lab interface, then PACS, then admin systems.
2. Verify each system is clean (IOC scan, Wazuh agents reporting) before reconnecting it.
3. Return clinical services in stages and reconcile the paper records into the EHR.
4. Monitor at a raised level for 30 days and watch the leak site for publication of our data.

## 4. Post-incident (lessons learned)

- Hold a review within 2 weeks: what worked, what failed, time to detect and time to contain.
- Send the NIS2 final report to the BSI within one month.
- Update the risk register (`data/risk-register.csv`) and this playbook.

## Communication tree

```
Incident lead ──► CISO ──► Executive board (CEO, Medical Director)
     │              ├──► DPO ──► Berlin data protection authority (Art. 33) and patients (Art. 34)
     │              ├──► BSI reporting portal (NIS2)
     │              └──► Police (LKA Berlin)
     ├──► Clinical lead ──► Ward managers (downtime procedures), emergency department (ambulance diversion)
     └──► Communications ──► Staff intranet/SMS, press statement, patient hotline
```

See `ir/raci.csv` for who is Responsible, Accountable, Consulted and Informed.
