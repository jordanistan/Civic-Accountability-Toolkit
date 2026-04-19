#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import re
from pathlib import Path
from datetime import datetime
import html

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
        content = p.read_text(encoding='utf-8')
        name_match = re.search(r'name:\s*"(.*?)"', content)
        if name_match:
            names.append(name_match.group(1))
    return names

def fetch_feed(url):
    try:
        # Using a more specific User-Agent to avoid bot-blocking
        headers = {'User-Agent': 'CivicAccountabilityBot/1.0 (https://github.com/jordanistan/Civic-Accountability-Toolkit)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_items(raw_xml):
    """Attempt to parse XML, fallback to Regex discovery if malformed."""
    items = []
    try:
        # Try standard XML parsing
        root = ET.fromstring(raw_xml)
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            items.append({'title': title, 'link': link})
    except ET.ParseError:
        print("XML Parse failed. Falling back to Regex discovery...")
        # Fallback: Extraction via regex for robust discovery even if feed is malformed
        titles = re.findall(r'<title>(.*?)</title>', raw_xml)
        links = re.findall(r'<link>(.*?)</link>', raw_xml)
        # Skip the first title/link if they belong to the channel metadata
        for t, l in zip(titles[1:], links[1:]):
            items.append({'title': html.unescape(t), 'link': l})
    return items

def main():
    print(f"Starting robust daily intake for {datetime.now().strftime('%Y-%m-%d')}...")
    tracked_names = get_tracked_names()
    matches = []

    for site, url in FEEDS.items():
        print(f"Checking {site}...")
        raw_content = fetch_feed(url)
        if not raw_content: continue

        items = parse_items(raw_content)
        for item in items:
            for name in tracked_names:
                if name.lower() in item['title'].lower():
                    matches.append({
                        'name': name,
                        'title': item['title'],
                        'link': item['link'],
                        'source': site
                    })

    if matches:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime('%Y-%m-%d')
        report_file = REPORT_DIR / f"intake-{date_str}.md"
        
        # Avoid duplicate reports for same day
        content = [f"# Daily Intake Report - {date_str}", 
                   "\nPotential new actions discovered in Tier 1 sources. **Review Required.**\n"]
        
        # Deduplicate matches
        seen = set()
        for m in matches:
            m_id = f"{m['name']}-{m['title']}"
            if m_id in seen: continue
            seen.add(m_id)
            
            content.append(f"## {m['name']}")
            content.append(f"- **Source:** {m['source']}")
            content.append(f"- **Action:** {m['title']}")
            content.append(f"- **Link:** {m['link']}")
            content.append(f"- **Next Step:** Create incident note if action has legal/constitutional impact.\n")
            
        report_file.write_text("\n".join(content), encoding='utf-8')
        print(f"Report generated: {report_file}")
    else:
        print("No new matches found in official feeds today.")

if __name__ == "__main__":
    main()
