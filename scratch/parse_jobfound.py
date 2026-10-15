import urllib.request, re, json, sys, csv

all_jobs = []
for page in range(0, 3):
    url = f'https://jobfound.org/?page={page}&loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&work=remote%2Chybrid%2Consite&type=Full-time'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html_doc = resp.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        continue
    chunks = re.findall(r'self\.__next_f\.push\(\[\d+,"(.*?)"\]\)', html_doc, re.DOTALL)
    full_text = ""
    for c in chunks:
        try:
            full_text += c.encode('utf-8').decode('unicode_escape')
        except Exception:
            full_text += c
    matches = re.finditer(r'\{[^{}]*?"companyName":"([^"]+)"[^{}]*?"applyUrl":"([^"]+)"[^{}]*?\}', full_text)
    for m in matches:
        chunk = m.group(0)
        co = m.group(1)
        apply_url = m.group(2)
        t_match = re.search(r'"title":"([^"]+)"', chunk)
        title = t_match.group(1) if t_match else "Unknown"
        l_match = re.search(r'"location":"([^"]+)"', chunk)
        loc = l_match.group(1) if l_match else ""
        all_jobs.append({"company": co, "title": title, "applyUrl": apply_url, "location": loc, "raw": chunk})

jobs = all_jobs


sys.stdout.reconfigure(encoding="utf-8")

# Deduplication against applications.csv
applied_cos = set()
with open("job-kit-starter/output/job-search/applications.csv", encoding="utf-8", errors="ignore") as f:
    for row in csv.DictReader(f):
        c = (row.get("Company") or "").strip().lower()
        if c:
            applied_cos.add(c)

print(f"Total extracted: {len(jobs)}")
print(f"Total already applied companies: {len(applied_cos)}")

sys.path.insert(0, "job-kit-starter")
from gates import title_skip

EXCLUDED_DOMAINS = ["indeed", "instahyre", "naukri", "linkedin"]

qualifying = []
for j in jobs:
    co = j["company"].strip()
    title = j["title"].strip()
    url = j["applyUrl"].strip()
    loc = j["location"].strip()
    
    # Check domain
    if any(ex in url.lower() for ex in EXCLUDED_DOMAINS):
        continue
    
    # Check dedup
    if co.lower() in applied_cos:
        continue
        
    # Title skip
    skip_term = title_skip(title)
    if skip_term:
        continue
        
    qualifying.append(j)

print(f"\nQualifying jobfound leads: {len(qualifying)}")
for q in qualifying:
    print(f"- {q['company']} | {q['title']} | {q['location']} | {q['applyUrl']}")

