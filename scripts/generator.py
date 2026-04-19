#!/usr/bin/env python3
import os
import shutil
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SRC_FOLDERS = ['people', 'incidents', 'issues', 'statutes', 'agencies', 'evidence/articles']

def sync():
    print("Preparing production documentation site...")
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)
    
    # 1. Copy root index and standards
    shutil.copy(ROOT / 'README.md', DOCS / 'index.md')
    shutil.copy(ROOT / 'SOURCE_STANDARDS.md', DOCS / 'SOURCE_STANDARDS.md')
    
    # 2. Map all slugs for clean cross-linking
    slug_to_folder = {}
    for folder in SRC_FOLDERS:
        src_path = ROOT / folder
        if not src_path.exists(): continue
        for record in src_path.glob('**/*.md'):
            slug_to_folder[record.stem] = folder.replace('evidence/articles', 'evidence')

    # 3. Process all record folders
    all_items = {}
    for folder in SRC_FOLDERS:
        src_path = ROOT / folder
        if not src_path.exists(): continue
        
        docs_sub = folder.replace('evidence/articles', 'evidence')
        dest_path = DOCS / docs_sub
        dest_path.mkdir(parents=True, exist_ok=True)
        items = []

        for record in src_path.glob('**/*.md'):
            if record.name in ['README.md', 'index.md']: continue
            
            content = record.read_text(encoding='utf-8')
            
            # Convert [[Wiki-links]] to standard Markdown relative links
            def link_repl(m):
                target = m.group(1).strip()
                label = target
                if '|' in target:
                    target, label = target.split('|', 1)
                
                slug = target.split('/')[-1]
                if slug in slug_to_folder:
                    f = slug_to_folder[slug]
                    # Link from folder/page.md to other/target.md is ../other/target.md
                    return f"[{label}](../{f}/{slug}.md)"
                return f"[{label}]({target})"

            content = re.sub(r'\[\[([^\]]+)\]\]', link_repl, content)
            
            # Inject metadata UI (optional: could add custom badges here)
            
            # Save to staging
            (dest_path / record.name).write_text(content, encoding='utf-8')
            
            # For Index Page
            title_match = re.search(r'^#\s+(.+)$', content, re.M)
            title = title_match.group(1).strip() if title_match else record.stem
            items.append({'slug': record.stem, 'title': title})
        
        all_items[docs_sub] = items

    # 4. Generate clean Markdown Index Pages
    for folder, items in all_items.items():
        index_file = DOCS / f"{folder}.md"
        if index_file.exists(): continue
        
        content = f"# {folder.title()} Database\n\n"
        content += f"Browse documented {folder} in the Civic Accountability Toolkit.\n\n"
        for item in sorted(items, key=lambda x: x['title']):
            content += f"- [{item['title']}]({folder}/{item['slug']}.md)\n"
        index_file.write_text(content)

    print("Site staging complete.")

if __name__ == "__main__":
    sync()
