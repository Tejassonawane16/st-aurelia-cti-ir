# Threat actor profile: Qilin (also called Agenda), Ch. 4 draft, owner: Tejas

> Draft. Open each source, rewrite in your own words, and add at least two more sources, such as vendor reports or government advisories.

| Field | Summary |
| --- | --- |
| Type | Ransomware-as-a-service (RaaS): core developers rent the ransomware to affiliates, who carry out the intrusions |
| Motivation | Financial, through double extortion (encrypt the data and threaten to publish it on a leak site) |
| Active since | 2022, first under the name "Agenda" |
| Targets | Many sectors, including healthcare. The June 2024 Synnovis attack disrupted pathology services for London NHS hospitals ([Security Affairs](https://securityaffairs.com/168480/data-breach/qilin-attack-on-synnovis-impacted-900000-patients.html)) |
| Encryptors | Windows and Linux/VMware ESXi variants; later versions are written in Rust |

## Documented intrusion (Sophos X-Ops, July 2024 activity)

Source: [Sophos, "Qilin ransomware caught stealing credentials stored in Google Chrome"](https://www.sophos.com/en-us/blog/qilin-ransomware-caught-stealing-credentials-stored-in-google-chrome)

1. **Initial access:** compromised credentials on a VPN portal **without MFA**.
2. **Dwell time:** about 18 days before further activity, which suggests an initial access broker sold the access.
3. **Lateral movement:** to a domain controller, using the stolen credentials.
4. **Credential harvesting:** the attackers edited the default domain Group Policy to run a logon script (`IPScanner.ps1`, launched by `logon.bat`). The script collected passwords saved in Chrome from every machine that logged on.
5. **Anti-forensics:** after exfiltration, they deleted the harvested files and cleared the event logs.
6. **Impact:** a second Group Policy object created a scheduled task to download and run the ransomware. Ransom notes were left in every directory.

## Why this group fits our scenario

- It is a proven attacker of healthcare supply chains (Synnovis).
- Its documented techniques can be tested with Sysmon and Wazuh in a student lab.
- Its entry point, remote access without MFA, is the same control failure seen at Change Healthcare. That gives the report one clear recommendation backed by three cases.

The technique list is in `cti/attack-mapping.csv`.
