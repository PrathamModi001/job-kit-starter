import urllib.request, json, csv, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from gates import title_skip, location_check, yoe_check

applied = {r['Company'].strip().lower() for r in csv.DictReader(open('output/job-search/applications.csv', encoding='utf-8'))}

queries = ["Node", "Backend", "Full+Stack", "Python", "Software+Engineer", "AI+Engineer", "FastAPI"]
all_jobs = {}

for q in queries:
    for page in range(2):
        url = f"https://jobfound.org/api/jobs?q={q}&loc=India&page={page}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode('utf-8'))
                for j in data.get('jobs', []):
                    jid = j.get('$id')
                    if jid not in all_jobs:
                        all_jobs[jid] = j
        except Exception as e:
            print(f"Error fetching q={q} p={page}: {e}")

print(f"Total unique jobs fetched from jobfound: {len(all_jobs)}")

qualifying = []
skipped = []

for jid, j in all_jobs.items():
    co = (j.get('companyName') or '').strip()
    title = (j.get('title') or '').strip()
    loc = (j.get('location') or '').strip()
    apply_url = (j.get('applyUrl') or '').strip()
    desc = j.get('description') or ''
    
    # Exclude platforms: indeed, instahyre, naukri, linkedin
    if any(ex in apply_url.lower() for ex in ['indeed.', 'instahyre.', 'naukri.', 'linkedin.']):
        continue
    
    # Check if company already in applications.csv
    if co.lower() in applied or any(co.lower() == a for a in applied):
        continue
    
    # Title check
    t_skip = title_skip(title)
    if t_skip:
        skipped.append((co, title, f"title_skip: {t_skip}"))
        continue
        
    # Location check
    loc_status, loc_why = location_check(loc, desc)
    if loc_status == 'skip':
        skipped.append((co, title, f"loc_skip: {loc_why}"))
        continue
        
    # YOE check
    y_status, y_ev = yoe_check(desc)
    if y_status == 'skip':
        skipped.append((co, title, f"yoe_skip: {y_ev}"))
        continue
        
    qualifying.append({
        'company': co,
        'title': title,
        'location': loc,
        'apply_url': apply_url,
        'desc': desc,
        'yoe_status': y_status,
        'yoe_ev': y_ev,
        'loc_status': loc_status,
        'slug': j.get('slug')
    })

print(f"\n--- QUALIFYING LEADS ({len(qualifying)}) ---")
for ql in qualifying:
    print(f"Company: {ql['company']} | Title: {ql['title']} | Loc: {ql['location']} | YOE: {ql['yoe_status']} ({ql['yoe_ev']}) | URL: {ql['apply_url']}")

print(f"\nTotal qualifying: {len(qualifying)}")
