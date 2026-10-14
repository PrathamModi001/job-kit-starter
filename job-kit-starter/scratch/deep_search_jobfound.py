import urllib.request, json, csv, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from gates import title_skip, location_check, yoe_check

applied = {r['Company'].strip().lower() for r in csv.DictReader(open('output/job-search/applications.csv', encoding='utf-8'))}

queries = ["", "Software", "Developer", "Engineer", "Node", "Backend", "Full+Stack", "Python", "AI", "FastAPI"]
all_jobs = {}

for q in queries:
    for page in range(5):
        q_param = f"&q={q}" if q else ""
        url = f"https://jobfound.org/api/jobs?loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&page={page}{q_param}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode('utf-8'))
                for j in data.get('jobs', []):
                    jid = j.get('$id')
                    if jid not in all_jobs:
                        all_jobs[jid] = j
        except Exception as e:
            pass

print(f"Total unique jobs fetched: {len(all_jobs)}")

qualifying = []
for jid, j in all_jobs.items():
    co = (j.get('companyName') or '').strip()
    title = (j.get('title') or '').strip()
    loc = (j.get('location') or '').strip()
    apply_url = (j.get('applyUrl') or '').strip()
    desc = j.get('description') or ''
    
    if any(ex in apply_url.lower() for ex in ['indeed.', 'instahyre.', 'naukri.', 'linkedin.']):
        continue
    if co.lower() in applied:
        continue
    t_skip = title_skip(title)
    if t_skip:
        continue
    loc_status, loc_why = location_check(loc, desc)
    if loc_status == 'skip':
        continue
    y_status, y_ev = yoe_check(desc)
    if y_status == 'skip':
        continue
    qualifying.append({
        'company': co,
        'title': title,
        'location': loc,
        'apply_url': apply_url,
        'yoe_status': y_status,
        'yoe_ev': y_ev,
        'loc_status': loc_status,
        'desc_len': len(desc)
    })

print(f"Total qualifying: {len(qualifying)}")
for ql in qualifying[:20]:
    print(f"{ql['company']} | {ql['title']} | {ql['location']} | {ql['yoe_status']} ({ql['yoe_ev']}) | {ql['apply_url']}")
