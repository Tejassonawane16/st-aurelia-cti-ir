#!/usr/bin/env python3
"""Run the four EHR test cases against OUR OWN mini EHR running on this laptop.

Start the EHR first (terminal 1, from the repo folder):
    python3 lab/ehr-server/ehr_app.py --data data/synthetic --log evidence/sample-logs/ehr_live.jsonl --port 8080
Then run (terminal 2):
    python3 scripts/ehr_tests.py
    python3 scripts/detect.py --ehr evidence/sample-logs/ehr_live.jsonl --no-truth

Test cases (authorised testing of our own app only):
  1. Authorised access   - clinician opens one record         -> 200, logged view_record
  2. Unauthorised access - nurse tries the bulk export        -> 403, rule 100104
  3. Password guessing   - 10 wrong passwords in a few seconds -> 401, rules 100101 + 100102
  4. Bulk export         - admin exports all records          -> 200, rule 100103
  5. Scraping            - 35 record requests in a few seconds -> rule 100105
"""
import argparse
import base64
import urllib.error
import urllib.request

PASSWORDS = {"dr.weber": "Clinic-Lab-2026!", "nurse.koch": "Ward-Lab-2026!", "it.admin": "Admin-Lab-2026!"}


def get(base, path, user, pw):
    req = urllib.request.Request(base + path)
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode())
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, len(r.read())
    except urllib.error.HTTPError as e:
        return e.code, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8080")
    a = ap.parse_args()
    results = []

    code, _ = get(a.base, "/patients/SYN-P000001", "dr.weber", PASSWORDS["dr.weber"])
    results.append(("1 Authorised access (clinician views a record)", "200", code))

    code, _ = get(a.base, "/export", "nurse.koch", PASSWORDS["nurse.koch"])
    results.append(("2 Unauthorised access (nurse tries export)", "403", code))

    codes = {get(a.base, "/patients/SYN-P000001", "dr.weber", "wrong-password")[0] for _ in range(10)}
    results.append(("3 Password guessing (10 wrong passwords)", "401", ",".join(map(str, sorted(codes)))))

    code, size = get(a.base, "/export", "it.admin", PASSWORDS["it.admin"])
    results.append((f"4 Bulk export by admin ({size} bytes, not saved)", "200", code))

    codes = {get(a.base, f"/patients/SYN-P{i:06d}", "dr.weber", PASSWORDS["dr.weber"])[0] for i in range(1, 36)}
    results.append(("5 Scraping (35 records in a few seconds)", "200", ",".join(map(str, sorted(codes)))))

    print(f"{'TEST':<52}{'EXPECTED':<10}GOT")
    for name, exp, got in results:
        ok = "PASS" if str(got) == exp else "CHECK"
        print(f"{name:<52}{exp:<10}{got}   {ok}")
    print("\nNext: python3 scripts/detect.py --ehr evidence/sample-logs/ehr_live.jsonl --no-truth")


if __name__ == "__main__":
    main()
