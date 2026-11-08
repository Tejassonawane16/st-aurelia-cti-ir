#!/usr/bin/env python3
"""Convert cti/iocs.csv into a STIX 2.1 bundle (cti/stix-bundle.json) for sharing, e.g. via MISP.

Python stdlib only. Validate the output at https://oasis-open.github.io/cti-stix-validator/
or import it into MISP (Event actions > Import from > STIX 2.x).
"""
import csv
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
PATTERNS = {
    "ipv4-addr": "[ipv4-addr:value = '{v}']",
    "domain-name": "[domain-name:value = '{v}']",
    "url": "[url:value = '{v}']",
    "file-name": "[file:name = '{v}']",
    "sha256": "[file:hashes.'SHA-256' = '{v}']",
    "md5": "[file:hashes.MD5 = '{v}']",
}
TLP_CLEAR = "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487"


def sid(kind):
    return f"{kind}--{uuid.uuid4()}"


def main():
    identity = {"type": "identity", "spec_version": "2.1", "id": sid("identity"), "created": NOW,
                "modified": NOW, "name": "St. Aurelia Klinikum CSIRT (simulated)", "identity_class": "organization",
                "sectors": ["healthcare"]}
    actor = {"type": "intrusion-set", "spec_version": "2.1", "id": sid("intrusion-set"), "created": NOW,
             "modified": NOW, "name": "Qilin", "aliases": ["Agenda"], "created_by_ref": identity["id"],
             "description": "Ransomware-as-a-service group modelled in the St. Aurelia scenario.",
             "primary_motivation": "personal-gain", "object_marking_refs": [TLP_CLEAR]}
    objects = [identity, actor]
    with open(ROOT / "cti" / "iocs.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tmpl = PATTERNS.get(row["type"])
            if not tmpl:
                print(f"skipped unsupported type: {row['type']}")
                continue
            ind = {"type": "indicator", "spec_version": "2.1", "id": sid("indicator"), "created": NOW,
                   "modified": NOW, "name": row["value"], "description": row["description"],
                   "indicator_types": ["malicious-activity"],
                   "pattern": tmpl.format(v=row["value"].replace("'", "\\'")), "pattern_type": "stix",
                   "valid_from": NOW, "created_by_ref": identity["id"], "object_marking_refs": [TLP_CLEAR]}
            rel = {"type": "relationship", "spec_version": "2.1", "id": sid("relationship"), "created": NOW,
                   "modified": NOW, "relationship_type": "indicates", "source_ref": ind["id"],
                   "target_ref": actor["id"]}
            objects += [ind, rel]
    bundle = {"type": "bundle", "id": sid("bundle"), "objects": objects}
    out = ROOT / "cti" / "stix-bundle.json"
    out.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    print(f"Wrote {len(objects)} STIX objects to {out}")


if __name__ == "__main__":
    main()
