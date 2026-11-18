# Arjun: Student 2, incident response

**Your role per the assignment:** the incident-response playbook, containment and recovery actions, the simulation record, lessons learned, and the data-protection and breach-reporting considerations.

You do **not** need to build virtual machines any more. Everything runs on your laptop with Python.

Commit everything from **your own laptop and GitHub account**. That is how your contribution is shown.

## Step 1: Set up (Sunday, 30 min)

1. Install Git (https://git-scm.com/download/win) and Python 3 (https://www.python.org, tick "Add to PATH"). Then install the GitHub CLI: open PowerShell and run `winget install --id GitHub.cli`.
2. In **Git Bash**:
   ```bash
   gh auth login
   git config --global user.name "Arjun <surname>"
   git config --global user.email "<your noreply email from GitHub > Settings > Emails>"
   gh repo clone Tejassonawane16/st-aurelia-cti-ir
   cd st-aurelia-cti-ir
   git pull
   git switch -c arjun/ir-work
   ```
3. Unzip **arjun-pack.zip** into this folder. It adds this file, `ir/playbook-improvements.md` and `compliance/gdpr-mapping.md`.

## Step 2: Cross-check Tejas's detection test (Sunday, 30 min, required by the assignment)

After Tejas has merged his detection scripts, run `git pull`. Then:

```bash
python scripts/make_sample_logs.py
python scripts/detect.py
```

1. You should see **"9 of 11 observable attack steps detected"**, 2 missed and 1 false positive.
2. Screenshot the output as `evidence/screenshots/2026-11-15_arjun-reproduction.png`.
3. Commit it:
   ```bash
   git add evidence/screenshots
   git commit -m "test(T09): reproduce detection replay, same 9/11 result"
   git push -u origin arjun/ir-work
   ```
4. Be able to say in one sentence what each of the 2 misses means for the response.

## Step 3: Tabletop exercise (Mon 19:00–20:30, on a call with Tejas)

Tejas reads the injects; you are the **incident lead**. For every inject, write one row in `ir/decision-log.csv`: the time, the decision, who decided, why, and which regulatory clock it affects. Commit the file the same evening.

## Step 4: Your documents (Tuesday)

1. `evidence/timeline.csv`: copy `evidence/timeline-template.csv`. Fill one row per attack step from `evidence/results/alerts.csv` and `detection_matrix.csv`, and add your tabletop decisions next to them.
2. `ir/playbook-improvements.md`: compare the plan with what happened. Fill both tables.
3. `ir/playbook.md`: make the improvements, and note each change.
4. `compliance/gdpr-mapping.md`: answer the five questions.

Commit after each file, with messages like `ir(T14): playbook improvements after tabletop`.

## Step 5: Report and slides (Wednesday, by 18:00)

- Your report parts: incident response and playbook, simulation record, lessons learned, breach reporting. Tejas sends you the 3–5-page format.
- Your slides: playbook, timeline, tabletop decisions, lessons learned.
- **19:00, integration call:** explain Tejas's detection part in your own words. He explains yours.

## What to study for the questions

- `ir/playbook.md`: why "isolate, don't power off"; who decides to take the EHR offline (the clinical lead) and why.
- The deadlines: NIS2 24 h / 72 h / 1 month to the BSI; GDPR Art. 33 72 h to the authority; Art. 34 to patients when the risk is high.
- GDPR Presentation 1: legal bases (Art. 6 + 9), data subject rights, the seven principles (Art. 5).
- `CODE_EXPLAINED.md` section 0 (the big picture) and the detection matrix: what was detected, what was missed and why.
