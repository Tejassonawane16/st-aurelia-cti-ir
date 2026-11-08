# Healthcare threat landscape (Ch. 2 draft, owner: Tejas)

> Draft written as a starting point. Rewrite it in your own words, open every source yourself before you cite it, and add the ENISA health threat landscape report to the sources.

## Why hospitals are targeted

- **Downtime is life-critical.** When the EHR, labs or imaging go down, care stops. That raises the pressure on the hospital to pay.
- **Health data is valuable and permanent.** Diagnoses, insurance numbers and dates of birth cannot be changed like a password. That makes them useful for extortion and fraud. Health data is also a special category under GDPR Art. 9.
- **Large, old and flat IT estates.** Hospitals run legacy clinical systems, connected medical devices that cannot be patched quickly, many third-party vendors with remote access, and networks that are often poorly segmented.
- **Double extortion.** Attackers steal data *before* they encrypt it, so restoring from backup does not end the threat to publish.

## Case studies

| Case | Date | Group | Initial access | Impact | Lesson for St. Aurelia |
| --- | --- | --- | --- | --- | --- |
| Universitätsklinikum Düsseldorf | Sep 2020 | DoppelPaymer | Unpatched Citrix gateway vulnerability (CVE-2019-19781) | Emergency admissions suspended; a patient was redirected to a hospital further away and died, and prosecutors later did not attribute the death to the attack [add source] | Patch internet-facing gateways; plan clinical downtime |
| Change Healthcare (UnitedHealth Group) | Feb 2024 | ALPHV/BlackCat affiliate | Remote access protected without MFA ([GovInfoSecurity](https://www.govinfosecurity.com/change-healthcare-now-counts-190-million-data-breach-victims-a-27380)) | About 190 million people affected; ransom of about USD 22 million reportedly paid | MFA on every remote access path; third-party concentration risk |
| Synnovis (pathology for London NHS trusts) | Jun 2024 | Qilin | Not officially disclosed | Several London hospitals cancelled procedures and redirected patients. Stolen data was published, and over 900,000 people were affected by one analysis ([Security Affairs](https://securityaffairs.com/168480/data-breach/qilin-attack-on-synnovis-impacted-900000-patients.html)) | A supplier outage becomes a hospital outage; include vendors in IR plans |

## What this means for our scenario

St. Aurelia's main risks are stolen remote-access credentials, a flat network between the admin and clinical segments, and an EHR that holds every patient record in one place. Our scenario therefore models a Qilin-style intrusion: valid credentials on a VPN without MFA, then credential theft, then bulk data theft, then encryption.
