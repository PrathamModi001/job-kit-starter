import urllib.request, json, re, sys, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gates

# Load seen companies from applications.csv and startups_outreach.csv
seen_companies = set()
with open(ROOT / "output" / "job-search" / "applications.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        co = r.get("Company", "").strip()
        if co:
            seen_companies.add(re.sub(r"[^a-z0-9]", "", co.lower()))

outreach_csv = ROOT / "output" / "job-search" / "outreach" / "startups_outreach.csv"
if outreach_csv.exists():
    with open(outreach_csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            co = r.get("Company", "").strip()
            if co:
                seen_companies.add(re.sub(r"[^a-z0-9]", "", co.lower()))

def is_seen(company_name):
    norm = re.sub(r"[^a-z0-9]", "", company_name.lower())
    for s in seen_companies:
        if norm == s: return True, s
        if len(norm) >= 4 and len(s) >= 4:
            if norm in s or s in norm:
                return True, s
    return False, None

# Fetch jobfound pages 0 to 4
all_links = []
for p in range(5):
    url = f"https://jobfound.org/?page={p}&loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&work=remote%2Chybrid%2Consite&type=Full-time"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            text = resp.read().decode('utf-8', errors='replace')
        hrefs = re.findall(r'href="(/job/[^"]+)"', text)
        for h in hrefs:
            if h not in all_links: all_links.append(h)
    except Exception as e:
        print(f"Error page {p}:", e)

print(f"Total jobfound links collected: {len(all_links)}")

leads = []
for link in all_links:
    slug = link.replace('/job/', '')
    m = re.match(r'^([^-]+(?:-[^-]+)?)-is-hiring-for-(.*)$', slug)
    co_guess = m.group(1).replace('-', ' ') if m else slug.split('-is-hiring')[0]
    
    seen, match_co = is_seen(co_guess)
    if seen:
        continue
    
    # Check title
    t_skip = gates.title_skip(slug)
    if t_skip:
        continue
        
    leads.append({
        "slug": slug,
        "co": co_guess,
        "link": f"https://jobfound.org{link}"
    })

print(f"Surviving candidate leads ({len(leads)}):")
for l in leads:
    print(l["co"], "->", l["slug"])
