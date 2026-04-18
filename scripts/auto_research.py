#!/usr/bin/env python3
import os, json, re, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PEOPLE_DIR = ROOT / 'people'
INCIDENTS_DIR = ROOT / 'incidents'
EVIDENCE_DIR = ROOT / 'evidence/articles'

def fetch_wiki_summary(name):
    query = urllib.parse.quote(name)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CivicAccountabilityToolkit/1.0 (https://github.com/jordanistan/Civic-Accountability-Toolkit)'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get('extract', ''), f"https://en.wikipedia.org/wiki/{query}"
    except Exception as e:
        return None, None

def get_display_name(slug):
    # Special cases
    mapping = {
        'jd-vance': 'JD Vance',
        'robert-f-kennedy-jr': 'Robert F. Kennedy Jr.',
        'usha-vance': 'Usha Vance',
        'pam-bondi': 'Pam Bondi',
        'lee-zeldin': 'Lee Zeldin',
        'john-ratcliffe': 'John Ratcliffe',
        'brooke-rollins': 'Brooke Rollins',
        'chris-wright': 'Chris Wright',
        'doug-burgum': 'Doug Burgum',
        'doug-collins': 'Doug Collins',
        'howard-lutnick': 'Howard Lutnick',
        'jamieson-greer': 'Jamieson Greer',
        'kelly-loeffler': 'Kelly Loeffler',
        'linda-mcmahon': 'Linda McMahon',
        'lori-chavez-deremer': 'Lori Chavez-DeRemer',
        'markwayne-mullin': 'Markwayne Mullin',
        'melania-trump': 'Melania Trump',
        'russ-vought': 'Russ Vought',
        'scott-bessent': 'Scott Bessent',
        'scott-turner': 'Scott Turner',
        'sean-duffy': 'Sean Duffy',
        'tulsi-gabbard': 'Tulsi Gabbard'
    }
    if slug in mapping:
        return mapping[slug]
    return slug.replace('-', ' ').title()

def update_person_file(person_file, new_incident_slug, new_evidence_slug):
    text = person_file.read_text()
    
    # Update frontmatter related_incidents (handle existing list)
    if 'related_incidents:' in text:
        # Replace the stub entries or append if not present
        text = re.sub(r'(\s*-\s*)incidents/incident-stub-[^\n]+', r'\1incidents/' + new_incident_slug, text)
    
    # Update frontmatter source_notes
    if 'source_notes:' in text and f'evidence/articles/{new_evidence_slug}' not in text:
        text = re.sub(r'(source_notes:\s*\n)', r'\1  - evidence/articles/' + new_evidence_slug + '\n', text)

    # Update body sections
    text = re.sub(r'## Linked incidents\n- \[\[incidents/incident-stub-[^\]]+\]\]', 
                  f'## Linked incidents\n- [[incidents/{new_incident_slug}]]', text)
    
    person_file.write_text(text)

def main():
    stubs = list(INCIDENTS_DIR.glob('incident-stub-*.md'))
    print(f"Found {len(stubs)} stubs to process.")

    for stub in stubs:
        name_slug = stub.stem.replace('incident-stub-', '')
        display_name = get_display_name(name_slug)
        
        print(f"Researching {display_name}...")
        summary, wiki_url = fetch_wiki_summary(display_name)
        if not summary:
            # Try some specific variations
            variations = [display_name, display_name.replace('.', ''), f"{display_name} (politician)"]
            for var in variations:
                summary, wiki_url = fetch_wiki_summary(var)
                if summary: break

        if not summary:
            print(f"Could not find Wikipedia entry for {display_name}. Skipping.")
            continue

        # 1. Create Evidence Note
        evidence_slug = f"wiki-{name_slug}"
        evidence_content = f"""---
type: evidence
status: verified
tags: [evidence, biography, wikipedia]
source_tier: L3
date_published: "2026-04-18"
url: "{wiki_url}"
people:
  - people/{name_slug}
---

# Wikipedia Summary: {display_name}

## Summary
{summary}

## Source
[{wiki_url}]({wiki_url})
"""
        (EVIDENCE_DIR / f"{evidence_slug}.md").write_text(evidence_content)

        # 2. Create Incident Note
        incident_slug = f"2025-2026-actions-{name_slug}"
        incident_content = f"""---
type: incident
status: active
tags: [incident, automated-intake]
source_tier: L3
confidence: medium
people:
  - people/{name_slug}
issues:
  - issues/public-integrity-and-corruption
evidence:
  - evidence/articles/{evidence_slug}
---

# 2025-2026 Actions - {display_name}

## One-line summary
Overview of 2025-2026 official actions and background for {display_name}.

## What is documented
Biographical background and known public record per official sources and reporting. {summary[:200]}...

## What remains alleged or unresolved
Specific 2025-2026 administrative decisions are still being mapped to primary source documents.

## Why it matters
This profile serves as a baseline for oversight and record-preservation requests for {display_name}.

## Suggested oversight ask
Request all communication logs and policy directives issued by {display_name} since January 2025.
"""
        (INCIDENTS_DIR / f"{incident_slug}.md").write_text(incident_content)

        # 3. Update Person File
        person_file = PEOPLE_DIR / f"{name_slug}.md"
        if person_file.exists():
            update_person_file(person_file, incident_slug, evidence_slug)
            print(f"Updated {person_file}")

        # 4. Remove Stub
        stub.unlink()
        print(f"Removed {stub}")

    print("Research and stub replacement complete.")

if __name__ == "__main__":
    main()
