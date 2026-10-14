import json, urllib.request, re, sys, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gates

# Seen companies
seen_companies = set()
with open(ROOT / "output" / "job-search" / "applications.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        co = r.get("Company", "").strip()
        if co: seen_companies.add(re.sub(r"[^a-z0-9]", "", co.lower()))

outreach_csv = ROOT / "output" / "job-search" / "outreach" / "startups_outreach.csv"
if outreach_csv.exists():
    with open(outreach_csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            co = r.get("Company", "").strip()
            if co: seen_companies.add(re.sub(r"[^a-z0-9]", "", co.lower()))

def is_seen(company_name):
    norm = re.sub(r"[^a-z0-9]", "", company_name.lower())
    for s in seen_companies:
        if norm == s: return True, s
        if len(norm) >= 4 and len(s) >= 4:
            if norm in s or s in norm: return True, s
    return False, None

UA = {"User-Agent": "Mozilla/5.0"}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", "replace")

# Top tech companies with active engineering in India
slugs = [
    ("ashby", "deepgram", "Deepgram"),
    ("ashby", "atlan", "Atlan"),
    ("ashby", "sentry", "Sentry"),
    ("ashby", "zapier", "Zapier"),
    ("ashby", "vanta", "Vanta"),
    ("ashby", "decagon", "Decagon"),
    ("ashby", "postman", "Postman"),
    ("ashby", "groww", "Groww"),
    ("ashby", "cred", "CRED"),
    ("ashby", "zepto", "Zepto"),
    ("ashby", "swiggy", "Swiggy"),
    ("ashby", "meesho", "Meesho"),
    ("gh", "couchbase", "Couchbase"),
    ("gh", "druva", "Druva"),
    ("gh", "cloudera", "Cloudera"),
    ("gh", "thoughtspot", "ThoughtSpot"),
    ("gh", "hubspot", "HubSpot"),
    ("gh", "box", "Box"),
    ("gh", "purestorage", "Pure Storage"),
    ("gh", "confluent", "Confluent"),
    ("gh", "datadog", "Datadog"),
    ("gh", "samsara", "Samsara"),
    ("gh", "twilio", "Twilio"),
    ("gh", "affirm", "Affirm"),
    ("gh", "instacart", "Instacart"),
    ("gh", "grafanalabs", "Grafana Labs"),
    ("gh", "reddit", "Reddit"),
    ("gh", "pinterest", "Pinterest"),
    ("gh", "dropbox", "Dropbox"),
    ("gh", "mongodb", "MongoDB"),
    ("gh", "airtable", "Airtable"),
    ("gh", "webflow", "Webflow"),
    ("gh", "gusto", "Gusto"),
    ("gh", "elastic", "Elastic"),
    ("gh", "discord", "Discord"),
    ("gh", "asana", "Asana"),
    ("gh", "scaleai", "Scale AI"),
    ("gh", "figma", "Figma"),
    ("gh", "netlify", "Netlify"),
    ("gh", "clevertap", "CleverTap"),
    ("gh", "chargebee", "Chargebee"),
    ("gh", "yellowai", "Yellow.ai"),
    ("gh", "leenaai", "Leena AI"),
    ("gh", "zeta", "Zeta"),
    ("gh", "inmobi", "InMobi"),
    ("gh", "glance", "Glance"),
    ("gh", "dream11", "Dream11"),
    ("gh", "mpl", "MPL"),
    ("gh", "delhivery", "Delhivery"),
    ("gh", "shadowfax", "Shadowfax"),
    ("gh", "rapido", "Rapido"),
    ("gh", "spinny", "Spinny"),
    ("gh", "cars24", "Cars24"),
    ("gh", "urbancompany", "Urban Company"),
    ("gh", "slice", "Slice"),
    ("gh", "jupiter", "Jupiter"),
    ("gh", "fi", "Fi Money"),
    ("gh", "khatabook", "Khatabook"),
    ("gh", "apna", "Apna"),
    ("gh", "loco", "Loco"),
    ("gh", "winzo", "WinZO"),
    ("gh", "navi", "Navi"),
    ("gh", "credgenics", "Credgenics"),
    ("gh", "leadsq", "LeadSquared"),
    ("gh", "leadsquared", "LeadSquared"),
    ("gh", "whatfix", "Whatfix"),
    ("gh", "darwinbox", "Darwinbox")
]

valid = []

for typ, slug, name in slugs:
    seen, match = is_seen(name)
    if seen: continue
    seen_s, match_s = is_seen(slug)
    if seen_s: continue
    
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
                
        for j in jobs:
            t = j["title"]
            l = j["loc"]
            d = j["desc"]
            
            # Title gate
            if gates.title_skip(t): continue
            # Exclude frontend
            if re.search(r"\bfrontend|front-end|ui developer|react developer\b", t, re.I): continue
            # Exclude intern
            if re.search(r"\bintern|internship|trainee|apprentice\b", t, re.I): continue
            
            # Location check
            reg, rwhy = gates.location_check(l, d)
            if reg == "skip": continue
            
            # YOE check
            ystat, yev = gates.yoe_check(d)
            if ystat == "skip": continue
            
            # Exclude Java, .NET, Ruby, C++
            blob = (t + " " + d[:600]).lower()
            if re.search(r"\bjava\b|\.net\b|c\#|c\+\+|\bruby\b|\brails\b", blob): continue
            
            # Fit score
            sc, parts = gates.fit_score(t, d, l)
            if sc >= gates.MIN_FIT:
                valid.append({
                    "company": name,
                    "title": t,
                    "loc": l,
                    "url": j["url"],
                    "fit": sc,
                    "parts": parts,
                    "channel": f"{typ.upper()} (Direct ATS)",
                    "desc": d
                })
    except Exception as e:
        pass

print(f"Total verified valid candidates found: {len(valid)}")
valid.sort(key=lambda x: x["fit"], reverse=True)
for v in valid:
    print(f"[{v['fit']}/15] {v['company']} | {v['title']} | {v['loc']} | {v['url']}")

(ROOT / "scratch" / "verified_valid.json").write_text(json.dumps(valid, indent=2), encoding="utf-8")
