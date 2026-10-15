import urllib.request, json, html
from bs4 import BeautifulSoup

url = 'https://hacker-news.firebaseio.com/v0/item/49922569.json'
with urllib.request.urlopen(url) as resp:
    thread = json.loads(resp.read().decode('utf-8'))

kids = thread.get('kids', [])
print(f'Total HN comments in thread: {len(kids)}')

results = []
for kid in kids[:80]:
    try:
        k_url = f'https://hacker-news.firebaseio.com/v0/item/{kid}.json'
        with urllib.request.urlopen(k_url) as k_resp:
            k_data = json.loads(k_resp.read().decode('utf-8'))
            text = k_data.get('text', '')
            if not text:
                continue
            first_line = text.split('<p>')[0] if '<p>' in text else text[:120]
            first_clean = BeautifulSoup(html.unescape(first_line), 'html.parser').get_text().strip()
            
            # Check engineering keywords and remote/India
            fl_lower = first_clean.lower()
            if any(role in fl_lower for role in ['engineer', 'developer', 'backend', 'full stack', 'full-stack', 'software', 'platform']):
                if any(loc in fl_lower for loc in ['remote', 'india', 'bengaluru', 'bangalore']):
                    results.append({'id': kid, 'first_line': first_clean, 'by': k_data.get('by')})
    except Exception:
        continue

print(f"Found {len(results)} engineering leads:")
for r in results:
    print(f"  - [{r['id']}] {r['first_line']}")
