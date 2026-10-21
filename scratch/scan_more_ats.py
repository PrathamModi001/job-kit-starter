import json
import urllib.request
import re
import csv
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

apps_csv = Path(r"job-kit-starter/output/job-search/applications.csv")
applied_cos = set()
with apps_csv.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("Company"):
            applied_cos.add(row["Company"].strip().lower())

LOC_INDIA = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|mumbai|chennai|ahmedabad|remote)\b", re.I)
FOREIGN = re.compile(r"\b(us|usa|united states|canada|uk|united kingdom|poland|germany|france|spain|mexico|singapore|australia|malaysia|ireland|netherlands|romania|sweden|switzerland)\b", re.I)
TITLE_INCLUDE = re.compile(r"\b(software|backend|full[- ]?stack|platform|systems|developer|engineer)\b", re.I)

extra_gh = [
    "uber", "rippling", "jumptrading", "rubrik", "nutanix", "purestorage", "cohesity",
    "confluent", "couchbase", "elastic", "snyk", "datadog", "postman", "cred", "swiggy",
    "zomato", "meesho", "slice", "jupiter", "smallcase", "yellowai", "sprinklr", "qubole",
    "fivetran", "airbyte", "prefect", "dagster", "hex", "deepset", "anomalo", "montecarlo",
    "acceldata", "castai", "vantage", "komodor", "cloudera", "snowflake", "palantir",
    "crowdstrike", "sentinelone", "paloaltonetworks", "splunk", "hashicorp", "pagerduty",
    "newrelic", "freshworks", "chargebee", "whatfix", "innovaccer", "leadsq", "clevertap",
    "moengage", "browserstack", "inmobi", "udaan", "khatabook", "dream11", "mpl", "cars24",
    "spinny", "simpl", "loco", "games24x7", "winzo", "sharechat", "inshorts", "pocketfm",
    "pratilipi", "urbancompany", "curefit", "cleartax", "lenskart", "nykaa", "zepto"
]

extra_ashby = [
    "replit", "modal", "linear", "twenty", "knock", "svix", "writer", "sentry",
    "triggerdev", "infisical", "elevenlabs", "n8n", "highlevel", "vanta", "decagon",
    "perplexity", "glean", "cursor", "coda", "pylon", "dust", "bland", "cartesia",
    "tome", "mintlify", "speakeasy", "unstructured", "pinecone", "weaviate", "chroma",
    "together", "anyscale", "runway", "luma", "midjourney", "mistral", "cohere", "harvey"
]

def check_title_gate(title):
    cmd = ["python", r"job-kit-starter/gates.py", "title", title]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0

results = []

def scan_gh(slug):
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
            if LOC_INDIA.search(loc) and not (FOREIGN.search(loc) and "india" not in loc.lower()):
                if TITLE_INCLUDE.search(title) and not re.search(r"\b(sales|support|escalation|manager|director|intern|lead|senior|sr)\b", title, re.I):
                    if check_title_gate(title):
                        out.append({
                            "ats": "greenhouse",
                            "company": slug.title(),
                            "title": title,
                            "location": loc,
                            "url": j.get("absolute_url", ""),
                            "id": str(j.get("id"))
                        })
    except Exception:
        pass
    return out

def scan_ashby(slug):
    if slug.lower() in applied_cos:
        return []
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=4).read().decode("utf-8"))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", "")
            locs = [loc] + [sl.get("location", "") for sl in j.get("secondaryLocations", [])]
            loc_str = " | ".join(locs)
            if LOC_INDIA.search(loc_str) and not (FOREIGN.search(loc_str) and "india" not in loc_str.lower()):
                if TITLE_INCLUDE.search(title) and not re.search(r"\b(sales|support|escalation|manager|director|intern|lead|senior|sr)\b", title, re.I):
                    if check_title_gate(title):
                        out.append({
                            "ats": "ashby",
                            "company": slug.title(),
                            "title": title,
                            "location": loc_str,
                            "url": j.get("jobUrl", f"https://jobs.ashbyhq.com/{slug}/{j.get('id')}"),
                            "id": j.get("id")
                        })
    except Exception:
        pass
    return out

with ThreadPoolExecutor(max_workers=30) as pool:
    futures = [pool.submit(scan_gh, s) for s in extra_gh] + [pool.submit(scan_ashby, s) for s in extra_ashby]
    for f in as_completed(futures):
        results.extend(f.result())

print(f"Total new qualifying roles: {len(results)}")
for r in results:
    print(f"[{r['ats']}] {r['company']} - {r['title']} ({r['location']}) -> {r['url']}")

with open("scratch/more_ats_leads.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)
