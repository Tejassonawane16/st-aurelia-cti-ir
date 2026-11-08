# Lab setup guide (owner: Arjun, deadline Wed 11 Nov)

The lab is three virtual machines on an isolated network:

- a Wazuh manager, which is the SIEM
- a Windows endpoint with Sysmon, standing in for a clinical or admin workstation
- an Ubuntu server running the mini EHR with synthetic patients

Everything the attack emulation touches lives inside this network.

```
           isolated VirtualBox network "aurelia-lab" (10.10.50.0/24, no route to the internet)
 ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
 │ wazuh-mgr 10.10.50.10│◄──│ ws-admin01 10.10.50.21│   │ ehr-srv01 10.10.50.30│
 │ Wazuh 4.x all-in-one │◄──┼── Windows 10/11+Sysmon│   │ Ubuntu 22.04/24.04   │
 │ dashboard :443       │◄──┴───────────────────────┴───│ mini EHR :8080       │
 └──────────────────────┘        agents → 1514/1515     └──────────────────────┘
```

## What you need

| VM | vCPU | RAM | Disk | Image |
| --- | --- | --- | --- | --- |
| wazuh-mgr | 2 | 4–8 GB | 50 GB | Official Wazuh OVA, or Ubuntu with the Wazuh quickstart installer |
| ws-admin01 | 2 | 4 GB | 40 GB | Windows 10/11 Enterprise evaluation (90-day, free from Microsoft) |
| ehr-srv01 | 1 | 1–2 GB | 15 GB | Ubuntu Server 22.04 or 24.04 LTS |

The total is about 10–14 GB of RAM for the VMs, so the host needs 16 GB or more. If one laptop is too small, put Wazuh on one laptop and the endpoints on the other, joined by a host-only network over a direct cable or a private switch. Never use the university Wi-Fi for this.

## Step 1: Network

1. In VirtualBox, create a **NAT Network** called `aurelia-lab` (10.10.50.0/24) and use it only during installs. Before any test run, switch every VM's adapter to an **Internal Network** called `aurelia-lab`, which has no internet access.
2. Give each VM the static IP shown in the diagram.

## Step 2: Wazuh manager

1. Import the Wazuh OVA, or on Ubuntu run the official quickstart from documentation.wazuh.com ("Quickstart", all-in-one install).
2. Open `https://10.10.50.10` and log in with the admin password the installer prints. Save that password in your **password manager, never in git**.
3. Copy `lab/wazuh/local_rules.xml` to `/var/ossec/etc/rules/local_rules.xml`, then run `sudo systemctl restart wazuh-manager`.

## Step 3: EHR server (Ubuntu)

```bash
sudo apt update && sudo apt install -y python3 git curl
git clone <your-repo-url> st-aurelia && cd st-aurelia
sudo bash lab/ehr-server/setup_ehr.sh
```

Then install the Wazuh agent. In the dashboard, open Agents, then Deploy new agent, choose Linux, and run the command it prints. Next, add the blocks from `lab/wazuh/agent-linux.conf` to `/var/ossec/etc/ossec.conf` and run `sudo systemctl restart wazuh-agent`.

## Step 4: Windows endpoint

1. Install Sysmon from Microsoft Sysinternals with a community configuration such as the SwiftOnSecurity `sysmonconfig-export.xml` (download it from the project's GitHub page, then run `sysmon64.exe -accepteula -i sysmonconfig-export.xml`).
2. Enable PowerShell Script Block Logging. Open `gpedit.msc`, go to Administrative Templates, then Windows Components, then Windows PowerShell, and turn on Script Block Logging.
3. Install the Wazuh agent using Deploy new agent, then Windows, then add the blocks from `lab/wazuh/agent-windows.conf` and restart the agent.
4. In the dashboard, check that both agents show as **Active**.

## Step 5: Snapshots

Take a snapshot of every VM called `clean-baseline`. Revert to it after each test run.

## Step 6: Prove the detections work (defender-side tests)

These tests use only the EHR app's own features, so they are safe to run anywhere in the lab. Run them from the Windows VM (PowerShell) or any lab machine. Each rule should appear in the dashboard under Threat Hunting.

| Test | How | Expected rule |
| --- | --- | --- |
| Failed logins | Run `curl.exe -u dr.weber:wrong http://10.10.50.30:8080/patients/SYN-P000001` about 10 times | 100101, then 100102 |
| Bulk export | Run `curl.exe -u it.admin:<password> http://10.10.50.30:8080/export -o export.csv` | 100103 (level 12) |
| Record scraping | Request 30+ `/patients/SYN-P0000xx` records in a loop as dr.weber | 100105 |
| Non-admin export | Run `curl.exe -u nurse.koch:<password> http://10.10.50.30:8080/export` | 100104 |
| FIM change | On ehr-srv01, run `sudo sh -c 'for f in /srv/ehr/records/*.csv; do echo "#fim-test" >> $f; done'`, then `sudo bash lab/ehr-server/restore_ehr.sh` | 100200, then 100202 |

To check a rule's logic without the agent, run `sudo /var/ossec/bin/wazuh-logtest` on the manager and paste a log line, for example one line from `/var/log/aurelia-ehr/access.log`.

The Windows rules (100300–100305) fire during the attack emulation on Thu 12 Nov (`emulation/emulation-plan.md`).

## Step 7: Evidence for the report

- Screenshot the dashboard with all agents Active. Name it `evidence/screenshots/2026-11-11_agents-active.png`.
- Screenshot every rule firing during the tests above.
- Export alerts as CSV from Threat Hunting. Remove any real IPs or real names first (`GIT_GUIDE.md`).
