#!/usr/bin/env bash
# Install the mini EHR server on the Ubuntu lab VM (run as root from the repo root).
#   sudo bash lab/ehr-server/setup_ehr.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"

echo "[1/5] Generating synthetic data"
python3 "$REPO/scripts/generate_patients.py" -n 500 -o /srv/ehr/records

echo "[2/5] Creating service account and folders"
id ehr >/dev/null 2>&1 || useradd --system --no-create-home --shell /usr/sbin/nologin ehr
mkdir -p /opt/aurelia-ehr /var/log/aurelia-ehr /srv/ehr/backup
cp "$REPO/lab/ehr-server/ehr_app.py" /opt/aurelia-ehr/
cp /srv/ehr/records/*.csv /srv/ehr/backup/          # clean copy for restore after the exercise
chown -R ehr:ehr /srv/ehr /var/log/aurelia-ehr /opt/aurelia-ehr

echo "[3/5] Installing systemd service"
cat >/etc/systemd/system/aurelia-ehr.service <<'UNIT'
[Unit]
Description=St. Aurelia mini EHR (lab, synthetic data)
After=network.target

[Service]
User=ehr
ExecStart=/usr/bin/python3 /opt/aurelia-ehr/ehr_app.py --data /srv/ehr/records --log /var/log/aurelia-ehr/access.log --port 8080
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now aurelia-ehr

echo "[4/5] Health check"
sleep 1
curl -s http://127.0.0.1:8080/health && echo

echo "[5/5] Next: add the Wazuh agent blocks from lab/wazuh/agent-linux.conf to /var/ossec/etc/ossec.conf, then: systemctl restart wazuh-agent"
