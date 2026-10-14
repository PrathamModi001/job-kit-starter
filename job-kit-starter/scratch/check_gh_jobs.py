import json, urllib.request, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gates

seen_co = set()
with open(ROOT / "output" / "job-search" / "applications.csv", encoding="utf-8") as f:
    import csv
    for r in csv.DictReader(f):
        seen_co.add(re.sub(r"[^a-z0-9]", "", r["Company"].lower()))

UA = {"User-Agent": "Mozilla/5.0"}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", "replace")

gh_companies = [
    "vercel", "gitlab", "cockroachlabs", "planetscale", "clickhouse",
    "databricks", "datadog", "postman", "groww", "phonepe", "stripe",
    "observeai"
]

candidates = []

for slug in gh_companies:
    if re.sub(r"[^a-z0-9]", "", slug.lower()) in seen_co:
        continue
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
        data = json.loads(get(url))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = (j.get("location") or {}).get("name", "")
            desc = gates.strip_html(j.get("content", ""))
            
            # check gates
            if gates.title_skip(title): continue
            reg = gates.region(loc, desc)
            if reg not in ("india", "remote"): continue
            ystat, yev = gates.yoe_check(desc)
            if ystat == "skip": continue
            
            candidates.append({
                "company": slug.capitalize(),
                "title": title,
                "location": loc,
                "url": j.get("absolute_url", ""),
                "channel": "Greenhouse (Direct ATS)",
                "desc_len": len(desc)
            })
    except Exception as e:
        pass

print(f"Found {len(candidates)} Greenhouse candidates:")
for c in candidates:
    print(c["company"], "|", c["title"], "|", c["location"], "|", c["url"])
