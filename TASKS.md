# Every task explained

The task numbers match the project board. For each task you'll find:

- **Why:** what it adds to the grade
- **How:** the concrete steps
- **Files:** where the work lives in this repo
- **Done when:** the check before you mark it Done on the board
- **Push:** what goes into git

Owners: **T** = Tejas, **A** = Arjun, **T+A** = together.

---

## Phase 1: Foundations (Sun 8 – Mon 9 Nov)

### T01: Confirm course requirements (T+A, Sun 8 Nov)
- **Why:** everything else is sized to this.
- **How:**
  1. Read the module handbook or assignment brief.
  2. Note the word limit, slide count and presentation time, and whether a live demo is expected.
  3. Note the citation style, the submission format (PDF? zip? repo link?) and whether an individual-contribution statement is required.
- **Files:** add a short "Requirements" section at the top of `report/outline.md`.
- **Done when:** both of you agree on the list.
- **Push:** the updated `report/outline.md`.

### T02: Shared repo and reading list (T+A, Sun 8 Nov)
- **Why:** one source of truth, plus a git history that shows who did what. That history is useful evidence of individual contribution.
- **How:**
  1. Tejas runs `python3 scripts/setup_github.py --arjun <arjun-user>` (see SETUP_GITHUB.md). It creates the private repo, pushes this folder, invites Arjun and creates one issue per user story.
  2. Both clone it.
  3. Skim the four core sources: NIST SP 800-61r3, MITRE ATT&CK (Enterprise), GDPR Art. 9/33/34, and the NIS2 Directive Art. 21/23.
- **Done when:** both of you can push.
- **Push:** the initial commit.

### T03: Hospital profile (A, Sun 8 Nov)
- **Why:** chapter 3. Without a concrete victim, the threat analysis and IR have nothing to anchor to.
- **How:** review `docs/hospital-profile.md`, adjust the numbers if you like, and **keep them consistent everywhere**. Rewrite it in your own words.
- **Done when:** the size, systems, data flows and regulatory status are filled in.
- **Push:** `docs/hospital-profile.md`.

### T04: Threat landscape and actor choice (T, Sun 8 Nov)
- **Why:** chapter 2, which justifies the scenario.
- **How:**
  1. Read `cti/threat-landscape.md` and open every source.
  2. Add the ENISA health threat landscape report and a source for the Düsseldorf case.
  3. Confirm Qilin as the modelled group.
  4. **Tell Arjun the technique list by Monday** (handoff 1).
- **Done when:** the three cases are cited and the group is chosen.
- **Push:** `cti/threat-landscape.md`.

### T05: Network diagram, asset list, risk register (A, Mon 9 Nov)
- **Why:** shows where the crown jewels are and which weaknesses the attack uses. The risk register links directly to the lessons learned.
- **How:**
  1. Review `docs/network-diagram.md`, `data/assets.csv` and `data/risk-register.csv`.
  2. Export the diagram as a PNG (mermaid.live or draw.io).
  3. Make a 5×5 risk heat map from the register in Excel or Python.
- **Done when:** the diagram PNG and the heat map are in `report/figures/`.
- **Push:** the CSVs and the figure PNGs.

### T06: Actor profile and Diamond Model (T, Mon 9 Nov)
- **Why:** chapter 4. The Diamond Model is a standard CTI analysis method, and examiners look for it.
- **How:** review `cti/actor-profile-qilin.md` and `cti/diamond-model.md`, and add two more sources, such as CISA or vendor reports. After the emulation, fill in the lab values in the Diamond table.
- **Done when:** all four features and the meta-features are filled.
- **Push:** both files.

## Phase 2: Threat intelligence and lab build (Tue 10 – Wed 11 Nov)

### T07: ATT&CK mapping and IOC list (T, Tue 10 Nov)
- **Why:** turns the intelligence into something defenders can use, which is the core of CTI.
- **How:**
  1. Check `cti/attack-mapping.csv`.
  2. Open https://mitre-attack.github.io/attack-navigator/, choose "Open existing layer", and upload `cti/navigator-layer.json`. Screenshot the result for the report.
  3. Keep `cti/iocs.csv` up to date.
- **Done when:** the Navigator screenshot is saved and the IOCs are listed.
- **Push:** the CSV, the JSON and the screenshot.

### T08: Lab infrastructure (A, Wed 11 Nov), the critical path
- **Why:** this is what makes the project "run". Tejas cannot start T11 without it.
- **How:** follow `lab/README.md`, steps 1–5: network, Wazuh manager, EHR server (`sudo bash lab/ehr-server/setup_ehr.sh`), Windows endpoint with Sysmon, snapshots.
- **Done when:** all agents are **Active** in the dashboard and the `clean-baseline` snapshots exist. **Message Tejas** (handoff 2).
- **Push:** any config you changed, plus the screenshot `evidence/screenshots/2026-11-11_agents-active.png`. **Never push VM images or passwords.**

### T09: Detections and dashboard (A, Wed 11 Nov)
- **Why:** shows the defence actually works, and gives measurable results.
- **How:**
  1. Install `lab/wazuh/local_rules.xml`.
  2. Run the defender-side tests in `lab/README.md` step 6 and confirm rules 100101–100105 and 100200–100202 fire.
  3. Build a dashboard filtered on `rule.groups: aurelia`.
- **Done when:** every testable rule has a screenshot.
- **Push:** the rule file, if you tuned it, and the screenshots.

### T10: Intelligence sharing in STIX (T, Tue 10 Nov, optional)
- **Why:** shows how a hospital would share IOCs with CERTs and other hospitals. It earns marks for going beyond the minimum.
- **How:** run `python3 scripts/iocs_to_stix.py`, which writes `cti/stix-bundle.json`. Optionally, import it into a MISP demo instance and take a screenshot.
- **Done when:** the bundle is generated.
- **Push:** the script output.

## Phase 3: Simulation (Thu 12 – Sat 14 Nov)

### T11: Attack emulation (T, Thu 12 Nov)
- **Why:** produces the real telemetry the detection and timeline chapters are built on.
- **How:**
  1. Read `emulation/emulation-plan.md`, especially the **rules of engagement**.
  2. Install Invoke-AtomicRedTeam on `ws-admin01` per the project's own docs, while the VM is still on NAT.
  3. Switch to the isolated network.
  4. For each technique in the table, list its tests, read the description and cleanup, run one test, and log it **immediately** in `emulation/run-log.csv`.
  5. Arjun watches the alerts during the run.
- **Done when:** every lab row in the table has a run-log line with Detected / Partly detected / Missed.
- **Push:** `emulation/run-log.csv` and screenshots. **Hand the log to Arjun the same evening** (handoff 3).

### T12: Tabletop injects and roles (T, Fri 13 Nov)
- **Why:** tests people and decisions, not just tools. The privacy and clinical dilemmas are here.
- **How:** review `ir/tabletop/injects.md` and `roles.md` against Arjun's playbook draft. Make sure each inject tests at least one playbook step.
- **Done when:** the injects are final and the role cards are printed or shared.
- **Push:** both files.

### T13: Incident timeline from evidence (A, Fri 13 Nov)
- **Why:** this is real forensic work: rebuilding what happened from logs.
- **How:**
  1. Copy `evidence/timeline-template.csv` to `evidence/timeline.csv`.
  2. For each run-log line, find the matching Wazuh alert and record both times.
  3. Calculate the **time to detect** for each technique.
- **Done when:** every emulated step has a row and an evidence file.
- **Push:** `evidence/timeline.csv` and the referenced screenshots.

### T14: IR playbook (A, Fri 13 Nov)
- **Why:** chapter 6. It shows that you can apply NIST 800-61r3 to a specific organization.
- **How:**
  1. Review `ir/playbook.md` and `ir/raci.csv`.
  2. Adjust the steps to match what your lab showed.
  3. **Send the draft to Tejas on Friday** (handoff 4).
  4. Turn the RACI into a formatted table for the report.
- **Done when:** the phases, communication tree and RACI are final.
- **Push:** both files.

### T15: Run the tabletop exercise (T+A, Sat 14 Nov, about 90 min)
- **Why:** this is the "simulation" in the project title.
- **How:** follow `ir/tabletop/injects.md`. Tejas reads the injects, Arjun answers as incident lead and logs each decision in `ir/decision-log.csv` with the time. Finish with the debrief questions.
- **Done when:** the decision log has an entry for every inject and the debrief answers are written.
- **Push:** `ir/decision-log.csv`.

### T16: GDPR and NIS2 reporting (T, Fri 13 Nov)
- **Why:** chapter 7 is the "privacy" half of the course title. Do not underweight it.
- **How:**
  1. Review `compliance/notification-timeline.md` and check the BSIG section numbers in the official law text.
  2. Fill the three templates with the times from the tabletop.
- **Done when:** all deadlines are calculated from the T0 of your tabletop, and the three notices are filled.
- **Push:** the `compliance/` files.

## Phase 4: Report and presentation (Sun 15 – Fri 20 Nov)

### T17: Draft own chapters (T+A, Sun 15 Nov)
- **How:** follow `report/outline.md`. Tejas writes Ch. 1, 2, 4, 7 and the emulation part of Ch. 5. Arjun writes Ch. 3, 5 and 6. Use the repo files as your notes, but **write the prose yourselves**.
- **Push:** your chapters in `report/` as Markdown or .docx.

### T18: Lessons learned (T+A, Mon 16 Nov)
- **How:**
  1. Each of you lists 5 findings.
  2. Merge them into one table with columns: finding, evidence, recommendation, NIS2 Art. 21 measure, priority.
  3. Update `data/risk-register.csv` with the planned treatments.
- **Push:** the chapter 8 draft.

### T19: Integrate and edit the report (T, Mon 16 Nov)
- **How:** merge the chapters, use one voice, check that every number matches, add the references, and write the executive summary last.
- **Push:** the final report and its PDF.

### T20: Slide deck (A, Mon 16 Nov)
- **How:** follow `slides/outline.md`. Take the figures straight from the report.
- **Push:** the deck (.pptx or PDF).

### T21: Demo video (A, Tue 17 Nov)
- **How:** make a 2–3 minute screen recording (OBS Studio) showing:
  1. the EHR export
  2. alert 100103 firing
  3. the FIM test
  4. alert 100202
- **Push:** **not to git** if over 50 MB. Put it on a cloud drive and add the link to the README.

### T22: Rehearse and final review (T+A, Thu 19 Nov)
- **How:** on Wed 18 and Thu 19, run two mock Q&A rounds. In each, explain the *other* person's code without notes while they ask questions from the Defence Prep doc and CODE_EXPLAINED.md. Then do a timed run-through (each person presents their own parts) and check every slide number against the report.

### T23: Submit (T+A, Fri 20 Nov)
- **How:** submit the report PDF, the slides, and the appendices or repo link, as T01 requires.
- **Done when:** the submission confirmation is saved.
- **Push:** tag the final version with `git tag v1.0-submitted && git push --tags`.
