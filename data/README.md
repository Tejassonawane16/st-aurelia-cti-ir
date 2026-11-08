# Data

## Synthetic patient data (`data/synthetic/`)

This folder holds **synthetic data only**. Every patient is invented by `scripts/generate_patients.py` (seed 42, 500 patients). IDs start with `SYN-`, and phone numbers use the fictional 555 range. Never put real patient data, or real data of any kind, in this repository. This is the GDPR data-minimisation principle (Art. 5(1)(c)) applied to our own project, and it is worth one sentence in chapter 1.

| File | Rows (seed 42) | Columns |
| --- | --- | --- |
| patients.csv | 500 | patient_id, first_name, last_name, date_of_birth, sex, address, phone, insurer, insurance_no, blood_type, synthetic |
| encounters.csv | about 1,250 | encounter_id, patient_id, department, admission_date, discharge_date, icd10_code, diagnosis, attending |
| lab_results.csv | about 1,900 | result_id, encounter_id, test_code, test_name, value, unit, flag (H/L) |

To regenerate the data, run `python3 scripts/generate_patients.py`. The same seed always gives identical files.

## Organization data

- `assets.csv`: the 11 critical assets, with their zone, data classification, criticality and lab stand-in.
- `risk-register.csv`: 8 risks scored as likelihood × impact (1–5 each). 15 or more counts as High, and 20 or more as Critical.
