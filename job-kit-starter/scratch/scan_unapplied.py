import json, csv, os, re, sys

csv_path = "job-kit-starter/output/job-search/applications.csv"
applied = set()
if os.path.exists(csv_path):
    with open(csv_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            applied.add(r.get("Company", "").strip().lower())

print(f"Applied companies: {len(applied)}")

# Let's inspect seen.json or run job_hunt's fetchers
from pathlib import Path
ROOT = Path("job-kit-starter")
sys.path.insert(0, str(ROOT))
import job_hunt

# Let's see what matches job_hunt finds
matches = []
# Run scan logic from job_hunt
for t, ident, name in job_hunt.SOURCES:
    # check if name already applied
    if name.lower() in applied:
        continue
    # Let's fetch for this company
    try:
        if t == "gh":
            jobs = job_hunt.fetch_greenhouse(ident, name)
        elif t == "ashby":
            jobs = job_hunt.fetch_ashby(ident, name)
        elif t == "lever":
            jobs = job_hunt.fetch_lever(ident, name)
        elif t == "aiven":
            jobs = job_hunt.fetch_aiven(ident, name)
        else:
            jobs = []
        for j in jobs:
            s = job_hunt.score(j)
            if s >= 0:
                matches.append((s, name, j))
    except Exception as e:
        # print(f"Error {name}: {e}")
        pass

print(f"Total unapplied matches: {len(matches)}")
matches.sort(key=lambda x: x[0], reverse=True)
for s, name, j in matches[:25]:
    print(f"Score {s:2d} | {name:15s} | {j['title']} | {j.get('location','')} | {j['url']}")
