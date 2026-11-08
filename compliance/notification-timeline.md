# Regulatory notification timeline (Ch. 7 draft, owner: Tejas)

St. Aurelia has **two parallel reporting duties**:

- **NIS2 / BSIG:** the incident is a significant cybersecurity incident, so it is reported to the BSI.
- **GDPR:** health data was stolen, so the breach is reported to the data protection authority and to patients.

Germany's NIS2 Implementation Act (NIS2UmsuCG) has been **in force since 6 December 2025** ([IHK](https://www.ihk.de/nordwestfalen/wirtschaftsspiegel-online/unternehmen-und-maerkte/neues-cybersicherheitsgesetz-gilt-seit-anfang-dezember-6840576)). It implements NIS2 Directive Art. 23 in the revised BSIG.

> Before submitting, check the exact BSIG section numbers in the official text on gesetze-im-internet.de, because secondary sources number them differently.

## Clock start

T0 is Fri 18:30 (inject 2). At that point we know of a significant incident, so the NIS2 clock starts. We also become aware of a personal-data breach, so the GDPR clock starts. The NIS2 24-hour clock runs from **knowledge of a suspected significant incident, not from confirmation** ([Legiscope](https://www.legiscope.com/blog/nis2-meldepflicht-bsi-24-stunden.html)).

| Deadline | Law | Recipient | Content | Template |
| --- | --- | --- | --- | --- |
| T0 + 24 h (Sat 18:30) | NIS2 Art. 23(4)(a) / BSIG | BSI reporting portal | **Early warning:** significant incident suspected; possible malicious cause; possible cross-border impact | `bsi-early-warning.md` |
| T0 + 72 h (Mon 18:30) | NIS2 Art. 23(4)(b) / BSIG | BSI | **Incident notification:** update with initial severity and impact assessment and IOCs | `bsi-early-warning.md` (part 2) |
| T0 + 72 h (Mon 18:30) | GDPR Art. 33 | Berlin Commissioner for Data Protection and Freedom of Information | Nature of the breach, categories and approximate numbers of people and records, DPO contact, likely consequences, measures taken | `gdpr-art33-notification.md` |
| Without undue delay | GDPR Art. 34 | Affected patients | Plain-language notice, because health data plus extortion means **high risk** | `patient-notice-art34.md` |
| On request of the BSI | NIS2 Art. 23(4)(c) | BSI | Intermediate status report | n/a |
| T0 + 1 month | NIS2 Art. 23(4)(d) / BSIG | BSI | **Final report:** root cause, threat type, mitigations, cross-border impact | Write at lessons learned |

## Key points for the report

- **Two regulators, two purposes.** The BSI report is about the security of the service. The GDPR notification is about the risk to people. Both are due on the same weekend.
- **Art. 33(4)** allows information to be provided in phases. Send what we know on time and complete it later; never miss the deadline while waiting for certainty.
- **Art. 34 exception (Art. 34(3)(a)):** no notice to individuals is needed if the data was unintelligible to the attacker, for example encrypted at rest with the keys safe. That does not apply here, because the data was exported in clear text. This is a strong argument for encrypting the EHR at rest.
- **Record keeping (Art. 33(5)):** document every breach, even one that is not reported. Our decision log does this.
- **Fines:** under NIS2, important entities face fines of up to EUR 7 million or 1.4% of turnover (see the Legiscope source above). Under GDPR Art. 83(4), failing the Art. 33/34 duties can cost up to EUR 10 million or 2% of turnover.
