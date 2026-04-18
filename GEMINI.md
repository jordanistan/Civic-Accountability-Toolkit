# GEMINI.md - Civic Accountability Toolkit

This directory contains the **Civic Accountability Toolkit**, an evidence-first repository for organizing public facts, linking incidents to sources, and facilitating fact-based oversight requests. It is designed to be used locally (via Obsidian or a Markdown editor) and published as a web-accessible documentation site (via MkDocs).

## Directory Overview

The project is organized into functional modules representing the core entities of civic accountability:

- `people/`: Profiles of public figures and administration officials.
- `incidents/`: Fact-based records of specific events or actions.
- `issues/`: Categorized themes (e.g., Civil Rights, Public Integrity).
- `agencies/`: Profiles of government bodies and oversight offices.
- `statutes/`: Notes on relevant laws and constitutional provisions.
- `relationships/`: Linkage notes connecting people, agencies, and issues.
- `evidence/`: Supporting articles and source documentation.
- `dashboards/`: Obsidian-optimized views for daily workflows (e.g., `DAILY_ACTION_BOARD.md`).
- `templates/`: Standardized structures for all new notes and outreach letters.
- `scripts/`: Automation for maintenance, validation, and deployment.
- `docs/`: The staging area for the MkDocs site, updated via `sync_docs.py`.

## Key Files

- `00_HOME.md`: The primary entry point for local navigation within an Obsidian vault.
- `README.md`: High-level project overview, principles, and quick start.
- `mkdocs.yml`: Configuration file for the public-facing documentation site.
- `scripts/new_note.py`: CLI tool for generating new notes from templates.
- `scripts/validate_repo.py`: Script to check for broken `[[Wiki-links]]` across the repository.
- `scripts/sync_docs.py`: Script that processes root-level notes, extracts metadata, and prepares them for MkDocs deployment.

## Usage & Development Conventions

### Creating New Content
Always use the `new_note.py` script to ensure consistent metadata and structure:
```bash
python scripts/new_note.py [incident|person|evidence] "Title of Note"
```

### Validation
Before committing changes, ensure all internal links are valid:
```bash
python scripts/validate_repo.py
```

### Syncing for Deployment
To update the `docs/` folder and generate JSON data exports after making changes:
```bash
python scripts/sync_docs.py
```

### Core Principles
1. **Evidence-First:** Every claim must be linked to a source note in `evidence/`.
2. **Neutrality:** Distinguish clearly between "What is documented" and "What remains alleged."
3. **Structured Data:** Use YAML frontmatter in notes for categorization (type, tags, status, source_tier).
4. **Wiki-Links:** Use `[[Note Name]]` for all internal cross-references to maintain graph integrity.
