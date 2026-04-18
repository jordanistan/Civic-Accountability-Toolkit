#!/usr/bin/env python3
from pathlib import Path

root = Path('.')
incident = root / 'incidents' / '2026-iran-war-powers-dispute.md'
template = root / 'templates' / 'citizen-letter-template.md'
out = root / 'packets' / 'examples' / 'generated-letter-example.md'

body = template.read_text().replace('[[INCIDENT TITLE]]', '2026 Iran war-powers dispute').replace('[[issue]]', 'war powers and international law').replace('[[statute]]', 'war powers framework')
out.write_text(body + '

---
Generated from starter script. Customize before sending.
')
print(f'Wrote {out}')
