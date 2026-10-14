import json, urllib.request, re, sys, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gates, job_hunt

# Gather all seen companies from both applications.csv and startups_outreach.csv
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
        if norm == s: return True
        if len(norm) >= 4 and len(s) >= 4:
            if norm in s or s in norm:
                return True
    return False

UA = {"User-Agent": "Mozilla/5.0"}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=12) as resp:
        return resp.read().decode("utf-8", "replace")

candidates = []

print(f"Total seen companies in history: {len(seen_companies)}")

for typ, slug, name in job_hunt.SOURCES:
    if not slug: continue
    if is_seen(name) or is_seen(slug):
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
            
            # Title skip
            if gates.title_skip(t): continue
            
            # Location check
            reg, rwhy = gates.location_check(l, d)
            if reg == "skip": continue
            
            # YOE check
            ystat, yev = gates.yoe_check(d)
            if ystat == "skip": continue
            
            # Fit score
            sc, parts = gates.fit_score(t, d, l)
            if sc >= gates.MIN_FIT:
                candidates.append({
                    "company": name,
                    "title": t,
                    "loc": l,
                    "url": job["url"],
                    "fit": sc,
                    "parts": parts,
                    "channel": f"{typ.upper()} (Direct ATS)",
                    "desc": d,
                    "yoe": (ystat, yev)
                })
    except Exception as e:
        pass

print(f"Total matching qualified leads found: {len(candidates)}")
# sort by fit score descending
candidates.sort(key=lambda x: x["fit"], reverse=True)
for c in candidates:
    print(f"[{c['fit']}/15] {c['company']} | {c['title']} | {c['loc']} | {c['url']}")

(ROOT / "scratch" / "qualifying_leads.json").write_text(json.dumps(candidates, indent=2), encoding="utf-8")
