#!/usr/bin/env python3
from pathlib import Path
import json, re
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
FOLDERS = ['people', 'incidents', 'issues', 'statutes', 'agencies']

def parse_frontmatter(text: str):
    if text.startswith('---
'):
        end = text.find('
---
', 4)
        if end != -1:
            return text[4:end], text[end+5:]
    return '', text

def parse_yamlish(fm: str):
    data = {}
    for line in fm.splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        key = key.strip(); value = value.strip()
        if value.startswith('[') and value.endswith(']'):
            data[key] = [x.strip().strip('"'') for x in value[1:-1].split(',') if x.strip()]
        else:
            data[key] = value.strip('"')
    return data

for folder in FOLDERS:
    folder_path = ROOT / folder
    docs_folder = DOCS / folder
    docs_folder.mkdir(parents=True, exist_ok=True)
    items = []
    for note in sorted(folder_path.glob('*.md')):
        text = note.read_text(encoding='utf-8')
        fm, body = parse_frontmatter(text)
        meta = parse_yamlish(fm)
        title_match = re.search(r'^#\s+(.+)$', body, re.M)
        title = title_match.group(1).strip() if title_match else note.stem
        (docs_folder / f'{note.stem}.md').write_text(body, encoding='utf-8')
        items.append({'slug': note.stem, 'title': title, 'meta': meta})
    (DOCS / 'data').mkdir(exist_ok=True)
    (DOCS / 'data' / f'{folder}.json').write_text(json.dumps(items, indent=2), encoding='utf-8')

print('Docs synced.')
