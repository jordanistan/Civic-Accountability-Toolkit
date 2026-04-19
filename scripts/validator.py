#!/usr/bin/env python3
import os
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ['people', 'incidents', 'issues', 'statutes', 'agencies', 'evidence']

# Required fields for each type
SCHEMAS = {
    'person': ['name', 'role', 'group', 'office_status', 'summary', 'confidence', 'source_reliability'],
    'incident': ['title', 'status', 'confidence', 'source_reliability', 'documented_facts', 'alleged_facts'],
    'statute': ['title', 'summary', 'relevance'],
    'evidence': ['title', 'url', 'source_tier', 'summary']
}

def parse_frontmatter(text):
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---\n', 4)
    if end == -1:
        return {}
    fm_text = text[4:end]
    data = {}
    for line in fm_text.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"\'')
    return data

def validate():
    errors = []
    print("Starting data validation...")
    
    for folder in FOLDERS:
        dir_path = ROOT / folder
        if not dir_path.exists(): continue
        
        for md_file in dir_path.glob('**/*.md'):
            # Basic Obsidian note check
            content = md_file.read_text(encoding='utf-8')
            fm = parse_frontmatter(content)
            
            note_type = fm.get('type')
            if not note_type:
                # Some files like README aren't data records
                if md_file.name in ['index.md', 'README.md']: continue
                errors.append(f"{md_file.relative_to(ROOT)}: Missing 'type' in frontmatter")
                continue
            
            if note_type in SCHEMAS:
                for field in SCHEMAS[note_type]:
                    if field not in fm:
                        errors.append(f"{md_file.relative_to(ROOT)} ({note_type}): Missing required field '{field}'")

            # Link validation: Check [[Wiki-links]]
            links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
            for link in links:
                # Handle root-relative or slug-only
                target = link.split('/')[-1]
                # Search for target .md anywhere in the data tree
                found = False
                for f in FOLDERS:
                    if (ROOT / f / f"{target}.md").exists():
                        found = True
                        break
                    # Also check nested articles
                    if (ROOT / f / "articles" / f"{target}.md").exists():
                        found = True
                        break
                if not found:
                    errors.append(f"{md_file.relative_to(ROOT)}: Broken link to [[{link}]]")

    if errors:
        print("\nValidation FAILED:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    
    print("\nValidation PASSED: Data integrity verified.")

if __name__ == "__main__":
    validate()
