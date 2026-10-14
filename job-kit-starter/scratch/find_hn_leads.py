import json, csv, re, os, sys
sys.stdout.reconfigure(encoding="utf-8")

applied = {r['Company'].strip().lower() for r in csv.DictReader(open('output/job-search/applications.csv', encoding='utf-8'))}

# Parse Algolia thread 49922569
import urllib.request
thread_id = "49922569"
url = f"https://hn.algolia.com/api/v1/items/{thread_id}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode("utf-8"))
    children = data.get("children", [])

print(f"Total children: {len(children)}")
sys.path.insert(0, ".")
from gates import strip_html, title_skip, location_check, yoe_check

for c in children:
    text = c.get("text") or ""
    clean = strip_html(text)
    
    # Must mention India or Remote
    if not re.search(r"\b(india|bengaluru|bangalore|pune|hyderabad|mumbai|gurgaon|delhi|remote)\b", clean, re.I):
        continue
    
    # Extract emails
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', clean)
    # Extract links
    urls = re.findall(r'https?://[^\s<>"]+', text)
    
    first_line = clean.split("\n")[0]
    m_co = re.match(r"^([^|–—\n]+)", first_line)
    co = m_co.group(1).strip() if m_co else "Unknown"
    
    if co.lower() in applied:
        continue
        
    print(f"ID: {c.get('id')} | Company: {co} | Emails: {emails} | URLs: {urls[:2]}")
    print(f"  Snippet: {clean[:160]}")
    print("-" * 60)
