#!/usr/bin/env python3
"""One-command GitHub setup for the St. Aurelia project.

What it does (each step is skipped if it is already done, so it is safe to run twice):
  1. git init + first commit (if this folder is not a git repo yet)
  2. creates a PRIVATE GitHub repo and pushes the code
  3. invites Arjun as a collaborator (write access)
  4. creates labels (owner:*, area:*, user-story) and 4 milestones (one per phase)
  5. creates one issue per user story from project/user-stories.json

Requirements: git, GitHub CLI (https://cli.github.com) and one-time login: gh auth login
Run it from the repo folder:
    python3 scripts/setup_github.py --arjun <arjun-github-username>
    python3 scripts/setup_github.py --dry-run          # only print what would happen
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRY = False

LABELS = {  # name: (colour, description)
    "user-story": ("5319e7", "Task written as a user story"),
    "owner:tejas": ("1f6feb", "Owned by Tejas"),
    "owner:arjun": ("d97706", "Owned by Arjun"),
    "owner:both": ("6b7280", "Done together"),
    "area:docs": ("c5def5", "Hospital profile, requirements"),
    "area:cti": ("0e8a16", "Threat intelligence"),
    "area:lab": ("b60205", "Lab and detections"),
    "area:emulation": ("e99695", "Attack emulation"),
    "area:ir": ("fbca04", "Incident response"),
    "area:compliance": ("0052cc", "GDPR and NIS2"),
    "area:report": ("bfd4f2", "Report"),
    "area:slides": ("d4c5f9", "Slides and demo"),
}


def run(cmd, check=True, capture=False):
    """Run a command (or just print it in --dry-run). Returns stdout when capture=True."""
    print("  $", " ".join(cmd))
    if DRY:
        return ""
    r = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if check and r.returncode != 0:
        sys.exit(f"\nFailed: {' '.join(cmd)}\n{r.stderr.strip()}")
    return r.stdout.strip() if capture else r


def preflight():
    for tool in ("git", "gh"):
        if not shutil.which(tool):
            sys.exit(f"'{tool}' is not installed. Install it first (see SETUP_GITHUB.md).")
    if DRY:
        return "<your-github-user>"
    if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
        sys.exit("You are not logged in to GitHub CLI. Run:  gh auth login   then run this script again.")
    if not subprocess.run(["git", "config", "user.email"], cwd=ROOT, capture_output=True, text=True).stdout.strip():
        sys.exit('Set your git identity first:\n  git config --global user.name "Your Name"\n'
                 '  git config --global user.email "you@example.com"   (use the email of your GitHub account)')
    return run(["gh", "api", "user", "-q", ".login"], capture=True)


def init_and_push(owner, repo):
    print("\n[1/5] Local git repository")
    if not (ROOT / ".git").exists():
        run(["git", "init", "-b", "main"])
        run(["git", "add", "."])
        run(["git", "commit", "-m", "chore: initial project structure"])
    else:
        print("  already a git repo - skipping init")

    print("\n[2/5] Private GitHub repo")
    exists = not DRY and subprocess.run(["gh", "repo", "view", f"{owner}/{repo}"], capture_output=True).returncode == 0
    if exists:
        print(f"  {owner}/{repo} already exists - pushing latest commits")
        run(["git", "push", "-u", "origin", "main"], check=False)
    else:
        run(["gh", "repo", "create", repo, "--private", "--source", ".", "--remote", "origin", "--push",
             "--description", "St. Aurelia Klinikum - CTI and incident response simulation (Data Security & Privacy)"])


def invite(owner, repo, arjun):
    print("\n[3/5] Collaborator")
    if not arjun:
        print("  no --arjun given - skipping (invite later: GitHub > Settings > Collaborators)")
        return
    run(["gh", "api", "-X", "PUT", f"repos/{owner}/{repo}/collaborators/{arjun}", "-f", "permission=push"])
    print(f"  invite sent - {arjun} must accept it at https://github.com/{owner}/{repo}/invitations")


def labels_and_milestones(owner, repo, milestones):
    print("\n[4/5] Labels and milestones")
    for name, (colour, desc) in LABELS.items():
        run(["gh", "label", "create", name, "--color", colour, "--description", desc, "--force"])
    existing = set()
    if not DRY:
        out = run(["gh", "api", f"repos/{owner}/{repo}/milestones?state=all", "-q", ".[].title"], capture=True)
        existing = set(out.splitlines())
    due = {"P1": "2026-11-09", "P2": "2026-11-11", "P3": "2026-11-14", "P4": "2026-11-20"}
    for key, title in milestones.items():
        if title in existing:
            print(f"  milestone exists: {title}")
            continue
        run(["gh", "api", f"repos/{owner}/{repo}/milestones", "-f", f"title={title}",
             "-f", f"due_on={due[key]}T22:00:00Z"])


def issues(stories):
    print("\n[5/5] Issues (one per user story)")
    existing = set()
    if not DRY:
        out = run(["gh", "issue", "list", "--state", "all", "--limit", "300", "--json", "title", "-q", ".[].title"],
                  capture=True)
        existing = set(out.splitlines())
    for s in stories:
        if s["title"] in existing:
            print(f"  exists: {s['id']}")
            continue
        body = (f"{s['body_story']}\n\n**Owner:** {s['owner'].title()}  \n**Due:** {s['due']}\n\n"
                "### Acceptance criteria\n" + "\n".join(f"- [ ] {c}" for c in s["acceptance"]) +
                "\n\nDetails and steps: see `TASKS.md`, section " + s["id"] + ".")
        cmd = ["gh", "issue", "create", "--title", s["title"], "--body", body,
               "--label", f"user-story,owner:{s['owner']},area:{s['area']}", "--milestone", s["milestone"]]
        if s["owner"] in ("tejas", "both"):
            cmd += ["--assignee", "@me"]
        run(cmd)


def main():
    global DRY
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default="st-aurelia-cti-ir", help="GitHub repo name (default st-aurelia-cti-ir)")
    ap.add_argument("--arjun", help="Arjun's GitHub username, to invite him as collaborator")
    ap.add_argument("--dry-run", action="store_true", help="print the commands without running them")
    ap.add_argument("--skip-issues", action="store_true", help="do not create issues")
    a = ap.parse_args()
    DRY = a.dry_run
    data = json.loads((ROOT / "project" / "user-stories.json").read_text(encoding="utf-8"))
    owner = preflight()
    print(f"GitHub user: {owner}{'   (DRY RUN - nothing is changed)' if DRY else ''}")
    init_and_push(owner, a.repo)
    invite(owner, a.repo, a.arjun)
    labels_and_milestones(owner, a.repo, data["milestones"])
    if not a.skip_issues:
        issues(data["stories"])
    print(f"\nDone. Open https://github.com/{owner}/{a.repo}/issues")
    print("Arjun's issues are not assigned yet: once he accepts the invite, assign them with")
    print('  gh issue list --label owner:arjun --json number -q ".[].number" | xargs -I{} gh issue edit {} --add-assignee ' +
          (a.arjun or "<arjun-user>"))


if __name__ == "__main__":
    main()
