# Civic Accountability Repo v5 v4

Evidence-first civic accountability toolkit for public-record review, constituent outreach, and oversight requests.

## What is new in v4
- Public-facing docs site starter with guided navigation
- Generated people / incident / issue / statute reference pages for GitHub Pages
- Search-friendly JSON data exports for future site upgrades
- GitHub Actions workflows for docs deployment and repo validation
- Better dashboards for daily use in Obsidian
- Packet generator scripts for daily outreach and issue-based summaries
- Contribution rules, review labels, and intake templates

## Core principles
- Do not state guilt unless there is a final finding or conviction.
- Link every claim to a source note.
- Separate **what happened**, **what may apply legally**, and **what still needs proof**.
- Prefer official records and court orders over commentary.
- Use respectful, non-defamatory outreach.

## Quick start
1. Clone the repo.
2. Open it in Obsidian or your editor.
3. Start at `00_HOME.md` or `docs/index.md`.
4. Review one incident note in `incidents/`.
5. Use `templates/citizen-letter-template.md` or generate a draft packet.
6. Run `python scripts/sync_docs.py` after adding or editing notes.

## Recommended daily flow
1. Open `dashboards/DAILY_ACTION_BOARD.md`.
2. Pick one incident with solid sourcing.
3. Review linked evidence and open questions.
4. Generate or adapt a neutral outreach letter.
5. Send it to your Representative, Senators, or the relevant oversight office.
6. Log what you sent and what still needs evidence.

## Deployment
- GitHub Pages via MkDocs + GitHub Actions
- Works locally as a Markdown vault in Obsidian
- Future-ready for GitHub Pages search and data-driven views

## Safety and credibility
This repo is designed for **civic accountability and oversight requests**, not for harassment or unsupported accusations. Keep claims tied to sources, separate allegations from findings, and use official contact channels.


## v5 roster expansion
This version expands the people layer to 25 current administration figures listed on the official White House administration and cabinet pages. The people index, docs site, and JSON exports were refreshed so users can browse, tag, and connect incident notes more easily.
## New in v6

- relationship notes for graph-friendly links
- person-to-agency and person-to-issue routing
- incident stubs for uncovered roster figures
- docs exports for people, incidents, issues, statutes, agencies, and relationships
- Dataview starter queries for Obsidian
- JSON exports for future site filters
