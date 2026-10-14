import json, urllib.request, re, sys, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gates

# Load seen companies from applications.csv and startups_outreach.csv
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
        if norm == s: return True, s
        if len(norm) >= 4 and len(s) >= 4:
            if norm in s or s in norm:
                return True, s
    return False, None

UA = {"User-Agent": "Mozilla/5.0"}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=8) as resp:
        return resp.read().decode("utf-8", "replace")

gh_slugs = [
    "samsara", "affirm", "instacart", "grafanalabs", "reddit", "pinterest",
    "dropbox", "mongodb", "airtable", "webflow", "gusto", "elastic",
    "discord", "asana", "figma", "netlify", "purestorage", "confluent",
    "datadog", "groww", "phonepe", "postman", "devrev", "observeai",
    "couchbase", "nutanix", "thoughtspot", "druva", "browserstack",
    "swiggy", "zepto", "slice", "meesho", "urbancompany", "dream11",
    "cars24", "spinny", "delhivery", "shadowfax", "hubspot", "box", "twiliocareers",
    "dbtlabs", "retool", "sourcegraph", "calcom", "prisma"
]

ashby_slugs = [
    "e2b", "modal", "linear", "railway", "neon", "render", "resend", "warp", "zed",
    "vapi", "stack-ai", "julius", "langfuse", "baseten", "fireworksai", "twenty",
    "n8n", "svix", "knock", "writer", "deepgram", "atlan", "sentry", "replit",
    "zapier", "revenuecat", "vanta", "sierra", "decagon", "1password", "ashby",
    "triggerdev", "calcom", "postman"
]

lever_slugs = [
    "zeta", "tinybird", "harness", "clevertap", "moengage", "yellowai",
    "leenaai", "chargebee", "darwinbox", "browserstack"
]

candidates = []

def check_job(co, title, loc, url, desc, channel):
    seen, match = is_seen(co)
    if seen: return
    if gates.title_skip(title): return
    reg, rwhy = gates.location_check(loc, desc)
    if reg == "skip": return
    ystat, yev = gates.yoe_check(desc)
    if ystat == "skip": return
    sc, parts = gates.fit_score(title, desc, loc)
    if sc >= gates.MIN_FIT:
        candidates.append({
            "company": co,
            "title": title,
            "loc": loc,
            "url": url,
            "fit": sc,
            "parts": parts,
            "channel": channel,
            "desc": desc
        })

print("Scanning Greenhouse...")
for slug in gh_slugs:
    seen, match = is_seen(slug)
    if seen: continue
    try:
        data = json.loads(get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"))
        for j in data.get("jobs", []):
            check_job(
                slug.capitalize(),
                j.get("title", ""),
                (j.get("location") or {}).get("name", ""),
                j.get("absolute_url", ""),
                gates.strip_html(j.get("content", "")),
                "Greenhouse (Direct ATS)"
            )
    except Exception:
        pass

print("Scanning Ashby...")
for slug in ashby_slugs:
    seen, match = is_seen(slug)
    if seen: continue
    try:
        data = json.loads(get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"))
        for j in data.get("jobs", []):
            loc = j.get("location") or ("Remote" if j.get("isRemote") else "")
            sec = ", ".join(x.get("location", "") for x in (j.get("secondaryLocations") or []) if x.get("location"))
            if sec: loc = f"{loc} ({sec})"
            check_job(
                slug.capitalize(),
                j.get("title", ""),
                loc,
                j.get("jobUrl", ""),
                j.get("descriptionPlain") or "",
                "Ashby (Direct ATS)"
            )
    except Exception:
        pass

print("Scanning Lever...")
for slug in lever_slugs:
    seen, match = is_seen(slug)
    if seen: continue
    try:
        data = json.loads(get(f"https://api.lever.co/v0/postings/{slug}?mode=json"))
        for j in data:
            cat = j.get("categories") or {}
            loc = cat.get("location", "") or ""
            allloc = ", ".join(cat.get("allLocations") or [])
            if allloc and allloc != loc: loc = f"{loc} ({allloc})"
            if (cat.get("commitment") or "").lower() == "remote" or (j.get("workplaceType") or "") == "remote":
                loc = (loc + " / Remote").strip(" /")
            check_job(
                slug.capitalize(),
                j.get("text", ""),
                loc,
                j.get("hostedUrl", ""),
                j.get("descriptionPlain") or gates.strip_html(j.get("description", "")),
                "Lever (Direct ATS)"
            )
    except Exception:
        pass

print(f"\nTotal qualifying candidates found: {len(candidates)}")
candidates.sort(key=lambda x: x["fit"], reverse=True)
for c in candidates:
    print(f"[{c['fit']}/15] {c['company']} | {c['title']} | {c['loc']} | {c['url']}")

(ROOT / "scratch" / "wide_candidates.json").write_text(json.dumps(candidates, indent=2), encoding="utf-8")
