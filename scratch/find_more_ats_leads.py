import json
import urllib.request
import re
import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

apps_csv = Path(r"E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv")
applied_cos = set()
with apps_csv.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("Company"):
            applied_cos.add(row["Company"].strip().lower())

print(f"Loaded {len(applied_cos)} applied companies for dedup.", flush=True)

LOC_INDIA = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|noida|mumbai|chennai|delhi|remote)\b", re.I)
TITLE_INCLUDE = re.compile(r"\b(software|backend|full[- ]?stack|platform|systems|developer|engineer)\b", re.I)
TITLE_EXCLUDE = re.compile(r"\b(senior|sr|lead|principal|staff|architect|manager|director|sde[- ]?[23ii]|sde\s*[23]|pe\s*2|product engineer\s*(?:2|ii)|mts|member of technical staff|intern|qa|test|support|sales|account|marketing|mobile|ios|android|react[- ]native|customer|client|java|\.net|c#|c\+\+|ruby|rails)\b", re.I)

gh_slugs = [
    "clevertap", "moengage", "browserstack", "chargebee", "hasura", "signoz",
    "inmobi", "udaan", "khatabook", "dream11", "mpl", "cars24", "spinny",
    "meesho", "smallcase", "slice", "jupiter", "simpl", "loco", "games24x7",
    "winzo", "glance", "sharechat", "inshorts", "pocketfm", "pratilipi",
    "yellowai", "sprinklr", "qubole", "druva", "cohesity", "rubrik",
    "nutanix", "purestorage", "tanium", "zscaler", "cloudflare", "okta",
    "confluent", "couchbase", "elastic", "snyk", "dynatrace", "appdynamics",
    "sumologic", "scylladb", "yugabyte", "aerospike", "starburst", "dbtlabs",
    "fivetran", "airbyte", "prefect", "dagster", "hex", "deepset", "anomalo",
    "monte-carlo", "montecarlo", "acceldata", "castai", "vantage", "komodor"
]

results = []

def check_gh(slug):
    if slug.lower() in applied_cos:
        return []
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=4).read().decode("utf-8"))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", {}).get("name", "")
            if LOC_INDIA.search(loc) and TITLE_INCLUDE.search(title) and not TITLE_EXCLUDE.search(title):
                out.append({
                    "ats": "greenhouse",
                    "company": slug.title(),
                    "title": title,
                    "location": loc,
                    "url": j.get("absolute_url", "")
                })
    except Exception:
        pass
    return out

with ThreadPoolExecutor(max_workers=20) as pool:
    futures = [pool.submit(check_gh, s) for s in gh_slugs]
    for f in as_completed(futures):
        results.extend(f.result())

print(f"\n--- MATCHED LIVE GREENHOUSE ROLES ({len(results)}) ---", flush=True)
for r in results:
    print(f"[{r['ats']}] {r['company']} - {r['title']} ({r['location']}) -> {r['url']}", flush=True)
