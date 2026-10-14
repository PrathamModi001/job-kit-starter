import urllib.request, json, csv, os, sys

csv_path = "job-kit-starter/output/job-search/applications.csv"
applied = set()
if os.path.exists(csv_path):
    with open(csv_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            applied.add(r.get("Company", "").strip().lower())

print(f"Applied companies count: {len(applied)}")

# Let's query jobfound.org
url = "https://jobfound.org/api/jobs?loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&work=remote%2Chybrid%2Consite&type=Full-time"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode("utf-8"))
        jobs = data.get("jobs", [])
        print(f"Jobfound returned {len(jobs)} jobs")
        for j in jobs:
            co = j.get("companyName", "").strip()
            title = j.get("title", "").strip()
            loc = j.get("location", "").strip()
            apply_url = j.get("applyUrl", "").strip()
            if co.lower() in applied:
                continue
            print(f"JOBFOUND: {co} | {title} | {loc} | {apply_url}")
except Exception as e:
    print(f"Jobfound error: {e}")
