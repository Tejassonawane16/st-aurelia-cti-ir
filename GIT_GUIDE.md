# Git guide: what to push, what never to push

## One-time setup (Tejas, Sun 8 Nov)

The easiest way is `python3 scripts/setup_github.py --arjun <arjun-user>` (see SETUP_GITHUB.md), which does all of this plus the issues. The manual way:

```bash
# on GitHub: New repository -> name "st-aurelia-cti-ir" -> Private -> no README
cd st-aurelia-cti-ir
git init -b main
git add .
git commit -m "chore: initial project structure"
git remote add origin https://github.com/<your-user>/st-aurelia-cti-ir.git
git push -u origin main
# GitHub -> Settings -> Collaborators -> invite Arjun
```

Arjun then runs `git clone https://github.com/<tejas-user>/st-aurelia-cti-ir.git`.

## Daily workflow (keeps the history clean and shows who did what)

```bash
git pull                                  # always start with this
git switch -c tejas/t07-attack-mapping    # one branch per task: <name>/<task>-<short-desc>
# ... work ...
git add cti/attack-mapping.csv cti/navigator-layer.json
git commit -m "cti(T07): map Qilin chain to ATT&CK, add Navigator layer"
git push -u origin tejas/t07-attack-mapping
# on GitHub: open a Pull Request -> the other person skims it -> Merge
git switch main && git pull
```

**Commit message format:** `<area>(Txx): what you did`, for example `lab(T08): add Windows agent config` or `ir(T14): RACI for containment decisions`. The area is one of `cti`, `lab`, `emulation`, `ir`, `compliance`, `docs`, `data`, `report` or `slides`.

The commit history then serves as evidence of individual contribution. `git shortlog -sn` shows the commit count per person.

## What to push

| Push ✅ | Examples |
| --- | --- |
| Everything you write | Markdown chapters, playbook, injects, notices |
| Scripts and configs | `scripts/*.py`, `lab/**` (rules, agent snippets, setup scripts) |
| Structured CTI data | `cti/*.csv`, `cti/navigator-layer.json`, `cti/stix-bundle.json` |
| Synthetic data | `data/synthetic/*.csv` (small, invented, reproducible) |
| Organization data | `data/assets.csv`, `data/risk-register.csv` |
| Evidence needed for the report | Screenshots (PNG), **sanitised** alert exports under 5 MB, `evidence/timeline.csv`, `emulation/run-log.csv`, `ir/decision-log.csv` |
| Final deliverables | Report PDF, slides PDF/PPTX |

## Never push

| Never push ❌ | Why | Where it goes instead |
| --- | --- | --- |
| Passwords, the Wazuh admin password, API keys, `.env` | Anyone with the repo can use them | A password manager, or tell each other in person |
| VM images and ISOs (`.ova`, `.vdi`, `.vmdk`, `.iso`) | Many GB; GitHub rejects files over 100 MB | Your own disk |
| Memory dumps or credential dumps (`.dmp`, `.mem`, `.raw`) | They contain secrets, even from a lab | Delete after use |
| Atomic Red Team or other offensive tool downloads | Not our work; they bloat the repo; AV may flag the repo | Install from the official source on the lab VM |
| Real data of any kind (patients, classmates, your own accounts) | GDPR, and this is a privacy course | Nowhere: use the synthetic data |
| Large raw logs (over 5 MB) | Unreadable and bloated | Your disk; push a filtered export |
| Demo video (over 50 MB) | Size | Cloud drive link in the README |

The `.gitignore` in this repo already blocks most of these. Before every push, run `git status` and read the list.

## If you pushed a secret by mistake

1. **Change the password immediately.** It is compromised from the moment it was pushed.
2. Remove the file: `git rm --cached <file>`, add it to `.gitignore`, then commit.
3. The secret is still in the history. For a course repo, rotating the password is enough. Otherwise use `git filter-repo` and force-push.

## What to push, day by day

| Day | Tejas pushes | Arjun pushes |
| --- | --- | --- |
| Sun 8 | Repo setup (script), requirements in `report/outline.md`, `cti/threat-landscape.md` | `docs/hospital-profile.md` |
| Mon 9 | `cti/actor-profile-qilin.md`, `cti/diamond-model.md` | `docs/network-diagram.md`, `data/*.csv`, figures |
| Tue 10 | `cti/attack-mapping.csv`, `navigator-layer.json`, `iocs.csv`, `stix-bundle.json` | Lab progress notes |
| Wed 11 | Help with the lab | Config changes, `2026-11-11_agents-active.png`, detection screenshots |
| Thu 12 | `emulation/run-log.csv` + screenshots | Alert screenshots from the run |
| Fri 13 | `ir/tabletop/*`, `compliance/*` | `evidence/timeline.csv`, `ir/playbook.md`, `ir/raci.csv` |
| Sat 14 | `ir/decision-log.csv`; your code improvement branch | Your code improvement branch |
| Sun 15 | Ch. 1, 2, 4, 7 | Ch. 3, 5, 6 |
| Mon 16 | Ch. 8 (with Arjun), merged report | Slides |
| Tue 17 | Final report edits | Demo video link in README, final slides |
| Fri 20 | Final PDF + tag `v1.0-submitted` | Final slides |
