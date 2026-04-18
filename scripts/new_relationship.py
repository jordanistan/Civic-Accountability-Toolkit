#!/usr/bin/env python3
    import sys
    from pathlib import Path

    if len(sys.argv) != 3:
        print("usage: new_relationship.py FROM_SLUG TO_SLUG")
        raise SystemExit(1)

    rel_dir = Path(__file__).resolve().parent.parent / "relationships"
    rel_dir.mkdir(exist_ok=True)
    slug = f"{sys.argv[1]}--{sys.argv[2]}"
    path = rel_dir / f"{slug}.md"
    if path.exists():
        print(f"exists: {path}")
        raise SystemExit(0)
    path.write_text(f"---
type: relationship
status: intake
tags: [relationship, graph-edge]
from: {sys.argv[1]}
to: {sys.argv[2]}
---

# Relationship — {sys.argv[1]} ↔ {sys.argv[2]}

## Basis for link
- Add a source-backed explanation here.
")
    print(path)
