#!/usr/bin/env python3
"""Mini EHR server for the St. Aurelia lab (synthetic data only, Python stdlib only).

It stands in for the hospital's electronic health record system so the
scenario has a real target, and it writes one JSON line per request to a
log that the Wazuh agent ships to the manager.

Endpoints (HTTP basic auth):
    GET /health               no auth, liveness check
    GET /patients/<id>        one patient record (normal clinical use)
    GET /search?q=<name>      search by last name (max 20 results)
    GET /export               full CSV export (admin role only)

Run:
    python3 ehr_app.py --data /srv/ehr/records --log /var/log/aurelia-ehr/access.log --port 8080
"""
import argparse
import base64
import csv
import io
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Lab accounts. Change these before the exercise and keep them out of git (see GIT_GUIDE.md).
USERS = {
    "dr.weber": ("Clinic-Lab-2026!", "clinician"),
    "nurse.koch": ("Ward-Lab-2026!", "clinician"),
    "it.admin": ("Admin-Lab-2026!", "admin"),
}


class EHR(BaseHTTPRequestHandler):
    patients: dict = {}
    log_path: Path = Path("access.log")

    def log_message(self, *args):  # silence default stderr logging
        pass

    def _audit(self, user, action, status, records=0, detail=""):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "app": "aurelia-ehr", "src_ip": self.client_address[0], "user": user or "-",
            "action": action, "path": self.path, "status": status, "records": records,
            "detail": detail,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _send(self, code, body, ctype="application/json"):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _auth(self):
        h = self.headers.get("Authorization", "")
        if not h.startswith("Basic "):
            return None, None
        try:
            user, pw = base64.b64decode(h[6:]).decode().split(":", 1)
        except Exception:
            return None, None
        if user in USERS and USERS[user][0] == pw:
            return user, USERS[user][1]
        self._audit(user, "login_failed", 401)
        return None, None

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/health":
            return self._send(200, '{"status":"ok"}')
        user, role = self._auth()
        if not user:
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Aurelia EHR"')
            self.end_headers()
            return
        if url.path.startswith("/patients/"):
            pid = url.path.split("/", 2)[2]
            rec = self.patients.get(pid)
            self._audit(user, "view_record", 200 if rec else 404, 1 if rec else 0, pid)
            return self._send(200 if rec else 404, json.dumps(rec or {"error": "not found"}))
        if url.path == "/search":
            q = parse_qs(url.query).get("q", [""])[0].lower()
            hits = [p for p in self.patients.values() if q and p["last_name"].lower().startswith(q)][:20]
            self._audit(user, "search", 200, len(hits), q)
            return self._send(200, json.dumps(hits))
        if url.path == "/export":
            if role != "admin":
                self._audit(user, "export_denied", 403)
                return self._send(403, '{"error":"admin only"}')
            buf = io.StringIO()
            rows = list(self.patients.values())
            w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
            self._audit(user, "bulk_export", 200, len(rows))
            return self._send(200, buf.getvalue(), "text/csv")
        self._send(404, '{"error":"unknown path"}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="/srv/ehr/records")
    ap.add_argument("--log", default="/var/log/aurelia-ehr/access.log")
    ap.add_argument("--port", type=int, default=8080)
    a = ap.parse_args()
    with open(Path(a.data) / "patients.csv", encoding="utf-8") as f:
        EHR.patients = {r["patient_id"]: r for r in csv.DictReader(f)}
    EHR.log_path = Path(a.log)
    EHR.log_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Aurelia EHR: {len(EHR.patients)} synthetic patients on port {a.port}, log {a.log}")
    ThreadingHTTPServer(("0.0.0.0", a.port), EHR).serve_forever()


if __name__ == "__main__":
    main()
