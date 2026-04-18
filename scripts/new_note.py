#!/usr/bin/env python3
import sys, re
from pathlib import Path

TEMPLATES = {
    'incident': ('templates/incident-note-template.md', 'incidents'),
    'person': ('templates/person-note-template.md', 'people'),
    'evidence': ('templates/evidence-note-template.md', 'evidence/articles'),
}

def slugify(s):
    s = s.strip().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

if len(sys.argv) < 3 or sys.argv[1] not in TEMPLATES:
    print('Usage: python scripts/new_note.py [incident|person|evidence] "Title Here"')
    raise SystemExit(1)

kind, title = sys.argv[1], sys.argv[2]
tpl, outdir = TEMPLATES[kind]
text = Path(tpl).read_text()
text = text.replace('{{title}}', title)
out = Path(outdir) / f"{slugify(title)}.md"
out.write_text(text)
print(f"Created {out}")
