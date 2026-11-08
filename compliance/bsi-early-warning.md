# BSI report: St. Aurelia Klinikum (simulated)

> This is a training template. Real reports go through the BSI reporting portal, and its form fields take priority over this layout.

## Part 1: Early warning (within 24 h), sent Sat [time] UTC

| Field | Entry |
| --- | --- |
| Entity | St. Aurelia Klinikum gGmbH, Berlin; health sector; important entity |
| Contact | CISO, [name], [phone], available 24/7 for this incident |
| Time of awareness | Fri [date] 18:30 CET |
| Description | Suspected ransomware attack with data exfiltration. A privileged account was compromised through VPN access; a bulk export of patient records was detected; encryption of clinical systems started on Sat around 02:00 |
| Suspected malicious / unlawful act? | Yes |
| Possible cross-border impact? | Not known at this time; no cross-border services identified |
| Service impact | EHR unavailable; paper downtime procedures active; partial ambulance diversion since Sat 03:00 |

## Part 2: Incident notification (within 72 h), sent Mon [time] UTC

| Field | Entry |
| --- | --- |
| Severity | High. Clinical IT unavailable for more than 24 h; health data of patients exfiltrated |
| Affected systems | EHR, file server, about [n] admin workstations, backup NAS |
| Attack vector | Valid account (VPN without MFA) → credential theft → bulk export → encryption |
| Indicators of compromise | See attached STIX bundle (`cti/stix-bundle.json`) |
| Measures taken | Hosts isolated; accounts reset; exfiltration IPs blocked; restore from offline backup in progress; police informed |
| Threat actor (if known) | Extortion message claims to be from Qilin; not verified |
