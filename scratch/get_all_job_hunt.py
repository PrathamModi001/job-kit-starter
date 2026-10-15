import sys, os, csv, re
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "job-kit-starter")
import job_hunt
from gates import title_skip

applied_cos = set()
with open("job-kit-starter/output/job-search/applications.csv", encoding="utf-8", errors="ignore") as f:
    for row in csv.DictReader(f):
        c = (row.get("Company") or "").strip().lower()
        if c: applied_cos.add(c)

print(f"Applied companies: {len(applied_cos)}")

# Let's inspect all matches from job_hunt
matches = job_hunt.fetch_all(days_limit=3650)
print(f"Total raw matches from fetch_all: {len(matches)}")

qualifying = []
for m in matches:
    co = m.get("co", "").strip()
    title = m.get("role", "").strip()
    loc = m.get("loc", "").strip()
    url = m.get("url", "").strip()
    tag = m.get("loc_tag", "")
    
    if co.lower() in applied_cos:
        continue
    skip = title_skip(title)
    if skip:
        continue
    # Check location: must be India (🇮🇳) or worldwide remote (🌍)
    if tag in ("🇮🇳", "🌍"):
        qualifying.append(m)

print(f"Qualifying from job_hunt: {len(qualifying)}")
for q in qualifying:
    print(f"- {q['co']} | {q['role']} | {q['loc']} ({q['loc_tag']}) | score={q['score']} | {q['url']}")
