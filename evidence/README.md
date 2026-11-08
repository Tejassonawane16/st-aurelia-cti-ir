# Evidence

Store all evidence from the lab and the tabletop here. **Only what is needed for the report goes into git** (see GIT_GUIDE.md).

| Folder | Content | Naming |
| --- | --- | --- |
| screenshots/ | Dashboard and alert screenshots (PNG) | `YYYY-MM-DD_<what>.png`, e.g. `2026-11-07_rule-100103-export.png` |
| logs/ | **Small, sanitised** alert exports (CSV/JSON, under 5 MB each) | `YYYY-MM-DD_<source>.csv` |
| timeline.csv | Final incident timeline (copy timeline-template.csv) | — |

**Sanitise before committing:**
- Replace any real home or university IP addresses with `[redacted]`.
- Remove your real usernames, machine names and any passwords.
- Lab IPs (10.10.50.x) and synthetic data are fine.
