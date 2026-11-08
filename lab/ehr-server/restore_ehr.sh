#!/usr/bin/env bash
# Restore the EHR records from the clean backup after a test run (or simply revert the VM snapshot).
set -euo pipefail
systemctl stop aurelia-ehr
rm -f /srv/ehr/records/*
cp /srv/ehr/backup/*.csv /srv/ehr/records/
chown -R ehr:ehr /srv/ehr/records
systemctl start aurelia-ehr
echo "EHR records restored from /srv/ehr/backup"
