#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
PEOPLE_DIR = ROOT / 'people'
REPORT_DIR = ROOT / 'incidents' / 'daily_reports'

# Official Tier 1 Feeds
FEEDS = {
    'White House Briefing Room': 'https://www.whitehouse.gov/briefing-room/feed/',
    'Federal Register (Executive Orders)': 'https://www.federalregister.gov/documents/feed?conditions%5Btype%5D%5B%5D=PRESDOCU'
}

def get_tracked_names():
    names = []
    for p in PEOPLE_DIR.glob('*.md'):
        # Extract name from filename or frontmatter
        content = p.read_text()
        name_match = re.search(r'name:\s*"(.*?)"', content)
        if name_match:
            names.append(name_match.group(1))
    return names

def fetch_feed(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.read()
    except:
        return None

def main():
    print(f"Starting daily intake for {datetime.now().strftime('%Y-%m-%d')}...")
    tracked_names = get_tracked_names()
    matches = []

    for site, url in FEEDS.items():
        print(f"Checking {site}...")
        raw_xml = fetch_feed(url)
        if not raw_xml: continue

        root = ET.fromstring(raw_xml)
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            
            for name in tracked_names:
                if name.lower() in title.lower():
                    matches.append({
                        'name': name,
                        'title': title,
                        'link': link,
                        'source': site
                    })

    if matches:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        report_file = REPORT_DIR / f"intake-{datetime.now().strftime('%Y-%m-%d')}.md"
        
        content = [f"# Daily Intake Report - {datetime.now().strftime('%Y-%m-%d')}", 
                   "\nPotential new actions discovered in Tier 1 sources. **Review Required.**\n"]
        
        for m in matches:
            content.append(f"## {m['name']}")
            content.append(f"- **Source:** {m['source']}")
            content.append(f"- **Action:** {m['title']}")
            content.append(f"- **Link:** {m['link']}")
            content.append(f"- **Next Step:** Create incident note if action has legal/constitutional impact.\n")
            
        report_file.write_text("\n".join(content))
        print(f"Report generated: {report_file}")
    else:
        print("No new matches found in official feeds today.")

if __name__ == "__main__":
    main()
