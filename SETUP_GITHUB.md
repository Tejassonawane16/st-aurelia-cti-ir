# Put the project on GitHub (about 15 minutes)

`scripts/setup_github.py` does everything in one command:

- creates the private repo
- pushes the code
- invites Arjun
- creates the labels and milestones
- creates 23 issues, one per user story

The steps below are for Tejas. Arjun's steps are at the end.

## 1. Install the tools (once)

| Tool | Windows | macOS | Ubuntu |
| --- | --- | --- | --- |
| Git | https://git-scm.com/download/win (also installs **Git Bash**) | `brew install git` | `sudo apt install git` |
| GitHub CLI | `winget install --id GitHub.cli` | `brew install gh` | `sudo apt install gh` |
| Python 3 | https://www.python.org/downloads/ (tick "Add to PATH") | already installed | already installed |

On Windows, run every command below in **Git Bash**.

## 2. Log in and set your identity (once)

```bash
gh auth login                      # choose GitHub.com > HTTPS > Login with a web browser
git config --global user.name "Tejas Sonawane"
git config --global user.email "<the email of your GitHub account>"
```

Git identity matters: every commit carries this name. That is how the git history shows who did what.

## 3. Run the setup

```bash
cd path/to/st-aurelia-cti-ir                                  # the unzipped folder
python3 scripts/setup_github.py --dry-run --arjun <arjun-user> # preview only, changes nothing
python3 scripts/setup_github.py --arjun <arjun-user>           # do it
```

On Windows, use `python` instead of `python3` if `python3` is not found.

When the script finishes, open `https://github.com/<you>/st-aurelia-cti-ir/issues`. You should see 23 issues, each with a user story, acceptance criteria as checkboxes, owner and area labels, and a milestone for its phase.

If something fails halfway, fix the error it prints and run the script again. Steps that are already done are skipped.

## 4. Optional: a Kanban board on GitHub

1. Open the repo, then the **Projects** tab, then **New project**, then choose **Board**.
2. Name the board "St. Aurelia".
3. Click **Add items**, type `#`, and add all 23 issues.
4. Columns: Todo, In Progress, Done. Drag each card as you work. Closing an issue moves it to Done.

## 5. Arjun's steps

1. Install Git and the GitHub CLI, then run `gh auth login`. Set his own `user.name` and `user.email`.
2. Accept the invite. It arrives by email, or he can open `https://github.com/<tejas-user>/st-aurelia-cti-ir/invitations`.
3. Clone the repo:

```bash
gh repo clone <tejas-user>/st-aurelia-cti-ir
cd st-aurelia-cti-ir
```

4. Tejas then assigns Arjun's issues to him with one command, run in Git Bash:

```bash
gh issue list --label owner:arjun --json number -q ".[].number" | xargs -I{} gh issue edit {} --add-assignee <arjun-user>
```

## 6. Daily work: issue, branch, pull request

```bash
git pull
git switch -c arjun/t08-lab-build            # branch named after the task
# ... work, then:
git add lab/
git commit -m "lab(T08): Wazuh manager and agents running"
git push -u origin arjun/t08-lab-build
gh pr create --fill --body "Closes #8"         # 'Closes #8' closes issue 8 when merged
```

On a fresh repo, the issues are created in order, so issue #1 is T01 and issue #8 is T08.

The other person reviews the pull request on GitHub, then clicks **Merge**. Everyone then runs `git switch main && git pull`.

For what may and may not be pushed, see `GIT_GUIDE.md`.
