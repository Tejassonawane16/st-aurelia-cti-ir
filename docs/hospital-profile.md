# St. Aurelia Klinikum: organization profile (Ch. 3 draft, owner: Arjun)

> This organization is fictional. All figures are invented for the simulation. Keep them consistent across the report and slides.

| Item | Value |
| --- | --- |
| Type | Non-profit acute-care hospital, Berlin |
| Beds | 400 |
| Staff | about 2,400 (520 physicians, 1,100 nursing, 780 admin/support) |
| Inpatient cases | about 22,000 per year |
| Outpatient and emergency contacts | about 60,000 per year |
| Regulatory status | NIS2 "important entity" under the German NIS2 Implementation Act (health sector, more than 250 staff). Below the KRITIS hospital threshold of 30,000 inpatient cases per year. GDPR controller for special-category health data (Art. 9). |
| Supervisory authorities | BSI (cybersecurity incidents); Berlin Commissioner for Data Protection and Freedom of Information (personal-data breaches) |
| Security team | 1 CISO, 3 IT security staff, no 24/7 SOC (Wazuh SIEM introduced in 2025), external DFIR retainer |

## Departments

The clinical departments are Emergency, Cardiology, Oncology, Surgery, Paediatrics, Radiology, Internal Medicine, Maternity and Neurology. The central laboratory and pathology are outsourced to a regional lab provider, which adds a supply-chain dependency like the Synnovis case.

## Systems

| System | Purpose | Lab stand-in |
| --- | --- | --- |
| EHR (electronic health record) | All patient records, orders, results | `ehr-srv01` mini EHR, 500 synthetic patients |
| PACS | Radiology images | n/a (documented only) |
| LIS interface | Lab orders and results from the external provider | n/a |
| Active Directory | Identity for 2,400 users | n/a (tabletop) |
| Admin workstations | Billing, HR, scheduling | `ws-admin01` (Windows + Sysmon) |
| IoMT | Infusion pumps, patient monitors (about 900 devices, many unpatchable) | n/a |
| Patient portal | Appointments, results | n/a |
| Remote access | VPN for staff and 14 vendors; **MFA only for IT admins** (the deliberate weakness) | Tabletop |
| Backups | Nightly to an on-prem NAS; weekly offline tape | Restore script + VM snapshot |

## Patient data flow

1. A patient registers at admission, which creates an EHR record (demographics and insurance).
2. Clinicians add diagnoses (ICD-10), orders and notes.
3. Lab orders go to the external lab provider, and results come back into the EHR.
4. Billing exports go to the health insurers.
5. Patients view their results in the portal.

Every step stores or transmits special-category data (GDPR Art. 9). That is why a breach triggers both the GDPR and the NIS2 reporting duties.

See `docs/network-diagram.md`, `data/assets.csv` and `data/risk-register.csv`.
