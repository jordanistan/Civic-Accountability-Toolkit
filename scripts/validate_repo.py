#!/usr/bin/env python3
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
missing = []
link_re = re.compile(r'\[\[([^\]]+)\]\]')
for md in ROOT.rglob('*.md'):
    text = md.read_text(encoding='utf-8', errors='ignore')
    for raw in link_re.findall(text):
        target = raw.split('|', 1)[0]
        tgt = ROOT / (target + '.md' if not target.endswith('.md') else target)
        if not tgt.exists():
            missing.append((str(md.relative_to(ROOT)), target))
if missing:
    print('Missing wiki-links:')
    for src, tgt in missing:
        print(f'- {src} -> {tgt}')
    raise SystemExit(1)
print('Repo validation passed.')
