# Civic Accountability Toolkit

An evidence-first, high-detail research platform designed to empower citizens to organize public facts, track incidents with reliable sources, and send fact-based oversight requests.

## Project Architecture

This repository uses a dual-branch architecture to separate research source code from the public-facing website.

1. **`main` Branch (Source of Truth):**
   - Contains the core research vault (Markdown files with rich YAML frontmatter).
   - Optimized for local use, research, and **Obsidian** graph-view.
   - Houses the data pipeline, validation scripts, and site generators.

2. **`gh-pages` Branch (Website):**
   - Automatically generated and updated via GitHub Actions.
   - Serves the production website at: [https://jordanistan.github.io/Civic-Accountability-Toolkit/](https://jordanistan.github.io/Civic-Accountability-Toolkit/)

## Data Integrity Rules

- **Evidence-First:** Every claim must be linked to a verifiable source note.
- **Neutrality:** We distinguish clearly between "What is documented" (court findings, official records) and "What is alleged" (reported disputes).
- **Source Tiers:** Strict reliability ranking from Tier 1 (Official Records) to Tier 4 (Commentary).
- **Presumption of Innocence:** Guilt is never stated as fact without a final legal judgment.

## Getting Started for Researchers

1. **Clone the Repo:** `git clone https://github.com/jordanistan/Civic-Accountability-Toolkit.git`
2. **Local Browsing:** Use any Markdown editor. For the best experience, open the root folder in [Obsidian](https://obsidian.md/).
3. **Contribute:** Read `CONTRIBUTING.md` and `SOURCE_STANDARDS.md` before submitting updates.

## Engineering Workflow

- **Validation:** `python scripts/validator.py` ensures all records meet schema requirements and links are sound.
- **Local Build:** `python scripts/generator.py` prepares the site locally for testing.
- **Deploy:** Merging to `main` triggers the production build and deployment to GitHub Pages.
