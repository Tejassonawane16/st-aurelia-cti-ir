# Threat model of the St. Aurelia EHR (owner: Tejas)

> Draft linking the course activities (4-question framework, STRIDE, FIPS 199, policy vs. mechanism) to our project. Review it, change anything you would say differently, and be ready to explain every line.

## 1. What are we building? (4-question framework, Q1)

The EHR serves patient records to clinicians and lets administrators export them. Its data flow:

- **Users** (clinicians, admin), from the admin and clinical networks
- go over **HTTP Basic auth** to the **EHR app** (`ehr_app.py`)
- which reads the **record store** (`/srv/ehr/records`) and writes the **audit log**
- which the **Wazuh agent** ships to the **SIEM**.

Trust boundaries:

- internet to VPN
- admin network to clinical network
- app to record store

## 2. Security categorization (NIST SP 800-60 / FIPS 199)

| Information type | Confidentiality | Integrity | Availability | Why |
| --- | --- | --- | --- | --- |
| Patient health records (diagnoses, lab results) | High | High | High | Art. 9 health data; wrong or missing data can harm patients; care stops without it |
| Patient identity and insurance data | High | Moderate | Moderate | Enables identity and insurance fraud |
| Audit / security logs | Moderate | High | Moderate | Must be trustworthy to reconstruct an incident |

**Security category of the EHR system:** SC = {(confidentiality, HIGH), (integrity, HIGH), (availability, HIGH)}. By the **high-water mark**, the overall impact level is **HIGH**. That justifies strong controls: MFA, export approval, offline backups and 24/7 alerting.

## 3. What can go wrong? (STRIDE against the EHR)

| STRIDE | Threat in our scenario | ATT&CK | Our control or detection |
| --- | --- | --- | --- |
| **S**poofing | Attacker logs in with phished VPN or EHR credentials | T1078, T1110 | Rules 100101/100102; recommendation: MFA |
| **T**ampering | Ransomware changes the record files | T1486 | FIM rules 100200/100202/100203; offline backups |
| **R**epudiation | Attacker clears the event logs to hide actions | T1070.001 | Rule 100305; logs shipped off-host to the SIEM in near real time |
| **I**nformation disclosure | Bulk export of all 500 patient records | T1213 | Rule 100103; recommendation: export approval |
| **D**enial of service | Encryption makes the EHR unavailable; shadow copies deleted | T1486, T1490 | Rule 100301; clinical downtime procedures |
| **E**levation of privilege | Credentials from LSASS or the browser give admin rights | T1003.001, T1555.003 | Rules 100300/100304; LSA protection |

## 4. What are we going to do about it? (Q3): policy vs. mechanism

| Policy (what) | Mechanism (how) |
| --- | --- |
| Only administrators may export all patient records | Role check in `ehr_app.py` (`role != "admin"` returns HTTP 403) |
| Every access to patient data is recorded | JSON audit line per request in `_audit()` |
| Bulk exports are reviewed immediately | Wazuh rule 100103 (level 12) alerting the on-call analyst |
| Remote access requires MFA (recommended) | VPN gateway MFA (not in the lab: tabletop and recommendation) |
| The service runs with least privilege | `ehr` system account with no login shell (`setup_ehr.sh`) |

## 5. Did we do a good job? (Q4)

The scenario replay (`scripts/detect.py`, results in `evidence/results/detection_matrix.csv`) gives:

- **Detected:** 9 of 11 observable attack steps.
- **Missed (2):** domain discovery (T1087.002) and the exfiltration upload (T1048). We had no rule for either.
- **False positive (1):** rule 100302 fired on the legitimate backup task.
- **Not observable:** the initial VPN login, because there is no VPN log source.

**Improvements:**

- Add a rule for `net group ... /domain`.
- Alert on outbound connections from workstations to unknown external IPs.
- Exclude the backup service account from rule 100302.
- Add VPN logs to the SIEM.
