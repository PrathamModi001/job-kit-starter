import json, urllib.request, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gates

# Load seen companies
seen_co = set()
with open(ROOT / "output" / "job-search" / "applications.csv", encoding="utf-8") as f:
    import csv
    for r in csv.DictReader(f):
        seen_co.add(re.sub(r"[^a-z0-9]", "", r["Company"].lower()))

# Load SOURCES from job_hunt.py
import job_hunt

UA = {"User-Agent": "Mozilla/5.0"}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", "replace")

candidates = []

for typ, slug, name in job_hunt.SOURCES:
    norm_co = re.sub(r"[^a-z0-9]", "", name.lower())
    if norm_co in seen_co:
        continue
    try:
        jobs = []
        if typ == "gh":
            data = json.loads(get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"))
            for j in data.get("jobs", []):
                jobs.append({
                    "title": j.get("title", ""),
                    "loc": (j.get("location") or {}).get("name", ""),
                    "url": j.get("absolute_url", ""),
                    "desc": gates.strip_html(j.get("content", ""))
                })
        elif typ == "ashby":
            data = json.loads(get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"))
            for j in data.get("jobs", []):
                loc = j.get("location") or ("Remote" if j.get("isRemote") else "")
                sec = ", ".join(x.get("location", "") for x in (j.get("secondaryLocations") or []) if x.get("location"))
                if sec: loc = f"{loc} ({sec})"
                jobs.append({
                    "title": j.get("title", ""),
                    "loc": loc,
                    "url": j.get("jobUrl", ""),
                    "desc": j.get("descriptionPlain") or ""
                })
        elif typ == "lever":
            data = json.loads(get(f"https://api.lever.co/v0/postings/{slug}?mode=json"))
            for j in data:
                cat = j.get("categories") or {}
                loc = cat.get("location", "") or ""
                allloc = ", ".join(cat.get("allLocations") or [])
                if allloc and allloc != loc: loc = f"{loc} ({allloc})"
                if (cat.get("commitment") or "").lower() == "remote" or (j.get("workplaceType") or "") == "remote":
                    loc = (loc + " / Remote").strip(" /")
                jobs.append({
                    "title": j.get("text", ""),
                    "loc": loc,
                    "url": j.get("hostedUrl", ""),
                    "desc": j.get("descriptionPlain") or gates.strip_html(j.get("description", ""))
                })
                
        for job in jobs:
            t = job["title"]
            d = job["desc"]
            l = job["loc"]
            if gates.title_skip(t): continue
            reg, rwhy = gates.location_check(l, d)
            if reg == "skip": continue
            ystat, yev = gates.yoe_check(d)
            if ystat == "skip": continue
            sc, parts = gates.fit_score(t, d, l)
            if sc >= gates.MIN_FIT:
                candidates.append({
                    "company": name,
                    "title": t,
                    "loc": l,
                    "url": job["url"],
                    "fit": sc,
                    "channel": f"{typ.upper()} (Direct ATS)",
                    "desc": d
                })
    except Exception as e:
        pass

print(f"Total matching candidates across all 91 boards: {len(candidates)}")
for c in candidates:
    print(f"[{c['fit']}/15] {c['company']} | {c['title']} | {c['loc']} | {c['url']}")
