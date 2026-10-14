import json, urllib.request, re, sys, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gates

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
        if norm == s: return True
        if len(norm) >= 4 and len(s) >= 4:
            if norm in s or s in norm: return True
    return False

UA = {"User-Agent": "Mozilla/5.0"}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=6) as resp:
        return resp.read().decode("utf-8", "replace")

# Let's test a broad set of Indian companies on Greenhouse
indian_gh = [
    "cred", "groww", "phonepe", "postman", "meesho", "swiggy", "zepto", "zomato",
    "blinkit", "urbancompany", "lenskart", "nykaa", "policybazaar", "delhivery",
    "shadowfax", "rapido", "spinny", "cars24", "ola", "atherenergy", "khatabook",
    "jupiter", "slice", "fi", "navi", "paytm", "bharatpe", "mobikwik", "credgenics",
    "clevertap", "moengage", "yellowai", "leenaai", "whatfix", "darwinbox", "leadsq",
    "leadsquared", "inmobi", "glance", "sharechat", "moj", "dream11", "mpl", "games24x7",
    "winzo", "zupee", "loco", "unacademy", "vedantu", "upgrad", "eruditus", "cuemath",
    "scaler", "simplilearn", "curefit", "cultfit", "healthifyme", "pharmeasy", "1mg",
    "tata1mg", "netmeds", "pristyncare", "mfine", "practo", "apollopharmacy", "medibuddy"
]

matching_jobs = []

for slug in indian_gh:
    if is_seen(slug): continue
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
        data = json.loads(get(url))
        for j in data.get("jobs", []):
            t = j.get("title", "")
            loc = (j.get("location") or {}).get("name", "")
            desc = gates.strip_html(j.get("content", ""))
            
            # Title
            if gates.title_skip(t): continue
            if re.search(r"\b(frontend|front-end|ui developer|intern|trainee|qa|test)\b", t, re.I): continue
            if not re.search(r"\b(software|developer|engineer|backend|full[- ]?stack|sde)\b", t, re.I): continue
            
            # Location
            reg, rwhy = gates.location_check(loc, desc)
            if reg == "skip": continue
            
            # YOE
            ystat, yev = gates.yoe_check(desc)
            if ystat == "skip": continue
            
            # Exclude Java, .NET, Ruby, C++
            blob = (t + " " + desc[:600]).lower()
            if re.search(r"\bjava\b|\.net\b|c\#|c\+\+|\bruby\b|\brails\b", blob): continue
            
            sc, parts = gates.fit_score(t, desc, loc)
            if sc >= gates.MIN_FIT:
                matching_jobs.append({
                    "company": slug.capitalize(),
                    "title": t,
                    "loc": loc,
                    "url": j.get("absolute_url", ""),
                    "fit": sc,
                    "parts": parts,
                    "channel": "Greenhouse (Direct ATS)",
                    "desc": desc
                })
    except Exception:
        pass

print(f"Total Indian tech matching jobs found: {len(matching_jobs)}")
for m in matching_jobs:
    print(f"[{m['fit']}/15] {m['company']} | {m['title']} | {m['loc']} | {m['url']}")

(ROOT / "scratch" / "indian_gh_matches.json").write_text(json.dumps(matching_jobs, indent=2), encoding="utf-8")
