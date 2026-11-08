#!/usr/bin/env python3
"""Generate the synthetic patient dataset for St. Aurelia Klinikum.

Every record is invented. Names are drawn at random from small lists,
identifiers carry the prefix SYN- so nobody can mistake them for real
insurance numbers, and the same seed always gives the same data.

Usage:
    python3 scripts/generate_patients.py                # 500 patients -> data/synthetic/
    python3 scripts/generate_patients.py -n 2000 -s 7   # 2000 patients, seed 7
"""
import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

FIRST = ["Anna", "Lukas", "Mia", "Leon", "Emma", "Noah", "Sofia", "Paul", "Lena", "Felix",
         "Hannah", "Jonas", "Lea", "Elias", "Marie", "Ben", "Clara", "Finn", "Ida", "Emil",
         "Aylin", "Mehmet", "Priya", "Arjun", "Olga", "Piotr", "Fatima", "Yusuf", "Chen", "Lina"]
LAST = ["Mueller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker",
        "Schulz", "Hoffmann", "Koch", "Richter", "Klein", "Wolf", "Neumann", "Schwarz",
        "Yilmaz", "Kowalski", "Nowak", "Sharma", "Ivanova", "Haddad", "Wang", "Novak"]
STREETS = ["Lindenweg", "Am Park", "Birkenallee", "Hauptstrasse", "Seestrasse", "Gartenweg"]
DEPARTMENTS = ["Emergency", "Cardiology", "Oncology", "Surgery", "Paediatrics",
               "Radiology", "Internal Medicine", "Maternity", "Neurology"]
# (ICD-10 code, description) - real codes, invented patients
DIAGNOSES = [("I10", "Essential hypertension"), ("E11.9", "Type 2 diabetes mellitus"),
             ("J18.9", "Pneumonia, unspecified"), ("S72.0", "Fracture of neck of femur"),
             ("I21.9", "Acute myocardial infarction"), ("C50.9", "Malignant neoplasm of breast"),
             ("O80", "Single spontaneous delivery"), ("K35.8", "Acute appendicitis"),
             ("G40.9", "Epilepsy, unspecified"), ("N39.0", "Urinary tract infection")]
LAB_TESTS = [("HGB", "Haemoglobin", "g/dL", 12.0, 17.5), ("CRP", "C-reactive protein", "mg/L", 0.0, 5.0),
             ("GLU", "Glucose (fasting)", "mg/dL", 70.0, 99.0), ("CREA", "Creatinine", "mg/dL", 0.6, 1.2),
             ("K", "Potassium", "mmol/L", 3.5, 5.1), ("TROP", "Troponin T", "ng/L", 0.0, 14.0)]
INSURERS = ["AOK Nordost", "TK", "Barmer", "DAK", "IKK", "Private"]


def make(n: int, seed: int, out: Path) -> None:
    rnd = random.Random(seed)
    out.mkdir(parents=True, exist_ok=True)
    today = date(2026, 11, 1)
    patients, encounters, labs = [], [], []
    for i in range(1, n + 1):
        pid = f"SYN-P{i:06d}"
        dob = today - timedelta(days=rnd.randint(0, 95 * 365))
        patients.append({
            "patient_id": pid,
            "first_name": rnd.choice(FIRST),
            "last_name": rnd.choice(LAST),
            "date_of_birth": dob.isoformat(),
            "sex": rnd.choice(["F", "M", "D"]),
            "address": f"{rnd.choice(STREETS)} {rnd.randint(1, 140)}, {rnd.randint(10115, 14199)} Berlin",
            "phone": f"+49 30 5550{rnd.randint(1000, 9999)}",  # 555 range: fictional
            "insurer": rnd.choice(INSURERS),
            "insurance_no": f"SYN-{rnd.choice('ABCDEFGHKLMNPRSTVWZ')}{rnd.randint(100000000, 999999999)}",
            "blood_type": rnd.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"]),
            "synthetic": "true",
        })
        for _ in range(rnd.randint(1, 4)):
            eid = f"SYN-E{len(encounters) + 1:07d}"
            adm = today - timedelta(days=rnd.randint(0, 730))
            code, desc = rnd.choice(DIAGNOSES)
            encounters.append({
                "encounter_id": eid, "patient_id": pid,
                "department": rnd.choice(DEPARTMENTS),
                "admission_date": adm.isoformat(),
                "discharge_date": (adm + timedelta(days=rnd.randint(0, 14))).isoformat(),
                "icd10_code": code, "diagnosis": desc,
                "attending": f"Dr. {rnd.choice(LAST)}",
            })
            for _ in range(rnd.randint(0, 3)):
                t, name, unit, lo, hi = rnd.choice(LAB_TESTS)
                val = round(rnd.uniform(lo * 0.7, hi * 1.4), 1)
                labs.append({
                    "result_id": f"SYN-L{len(labs) + 1:07d}", "encounter_id": eid,
                    "test_code": t, "test_name": name, "value": val, "unit": unit,
                    "flag": "H" if val > hi else ("L" if val < lo else ""),
                })
    for name, rows in (("patients.csv", patients), ("encounters.csv", encounters),
                       ("lab_results.csv", labs)):
        with open(out / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print(f"Wrote {len(patients)} patients, {len(encounters)} encounters, "
          f"{len(labs)} lab results to {out}/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-n", type=int, default=500, help="number of patients (default 500)")
    ap.add_argument("-s", "--seed", type=int, default=42, help="random seed (default 42)")
    ap.add_argument("-o", "--out", default=str(Path(__file__).resolve().parent.parent / "data" / "synthetic"))
    a = ap.parse_args()
    make(a.n, a.seed, Path(a.out))
