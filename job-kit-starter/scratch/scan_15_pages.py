import urllib.request, json, csv, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from gates import title_skip, location_check, yoe_check

applied = {r['Company'].strip().lower() for r in csv.DictReader(open('output/job-search/applications.csv', encoding='utf-8'))}

all_jobs = {}
for page in range(15):
    url = f"https://jobfound.org/api/jobs?page={page}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            jobs = data.get('jobs', [])
            for j in jobs:
                jid = j.get('$id')
                if jid not in all_jobs:
                    all_jobs[jid] = j
    except Exception as e:
        print(f"Error page {page}: {e}")

print(f"Total jobs fetched across 15 pages: {len(all_jobs)}")

qualifying = []
for jid, j in all_jobs.items():
    co = (j.get('companyName') or '').strip()
    title = (j.get('title') or '').strip()
    loc = (j.get('location') or '').strip()
    country = (j.get('country') or '').strip()
    apply_url = (j.get('applyUrl') or '').strip()
    desc = j.get('description') or ''
    
    # Check if India eligible
    # Must be in India or remote explicitly open to India
    loc_full = f"{loc}, {country}" if country else loc
    r_type, r_why = location_check(loc_full, desc)
    if r_type == 'skip':
        continue
    if r_type == 'unknown' and not re.search(r'\b(india|bengaluru|bangalore|pune|hyderabad|mumbai|gurgaon|gurugram|noida|chennai|ahmedabad)\b', loc_full.lower()):
        continue
        
    if any(ex in apply_url.lower() for ex in ['indeed.', 'instahyre.', 'naukri.', 'linkedin.']):
        continue
    if co.lower() in applied:
        continue
    t_skip = title_skip(title)
    if t_skip:
        continue
    y_status, y_ev = yoe_check(desc)
    if y_status == 'skip':
        continue
        
    qualifying.append({
        'company': co,
        'title': title,
        'location': loc_full,
        'apply_url': apply_url,
        'yoe_status': y_status,
        'yoe_ev': y_ev,
        'loc_status': r_type,
        'desc': desc
    })

print(f"Total qualifying India/Remote from 15 pages: {len(qualifying)}")
for ql in qualifying:
    print(f"-> {ql['company']} | {ql['title']} | {ql['location']} | {ql['yoe_status']} ({ql['yoe_ev']}) | {ql['apply_url']}")
