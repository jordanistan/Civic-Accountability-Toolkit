#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if len(sys.argv) < 2:
    print('Usage: python scripts/build_daily_packet.py incidents/<file>.md')
    raise SystemExit(1)
note = ROOT / sys.argv[1]
if not note.exists():
    print(f'Not found: {note}')
    raise SystemExit(1)
body = note.read_text(encoding='utf-8')
out = ROOT / 'packets' / f'{note.stem}-daily-packet.md'
out.parent.mkdir(exist_ok=True)
packet = f'''# Daily Outreach Packet

## Incident
{note.stem}

## Source note summary
Review the linked evidence in the incident note before sending anything.

## Suggested outreach prompt
I am writing as a constituent to request review of the incident summarized in `{note.name}`. Please review the linked public sources, distinguish any court findings from open allegations, and advise what oversight steps your office can take.

## Incident content

{body}
'''
out.write_text(packet, encoding='utf-8')
print(f'Wrote {out}')
