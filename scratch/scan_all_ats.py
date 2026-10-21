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

print(f"Loaded {len(applied_cos)} applied companies for dedup.")

LOC_INDIA = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|mumbai|chennai|ahmedabad|remote)\b", re.I)
TITLE_INCLUDE = re.compile(r"\b(software|backend|full[- ]?stack|platform|systems|developer|engineer)\b", re.I)

# List of Ashby companies to check
ashby_cos = [
    "sarvam", "composio", "smallest", "atlan", "vapi", "e2b", "browserbase", "firecrawl",
    "langchain", "langfuse", "resend", "inngest", "supabase", "deepgram", "replit",
    "modal", "linear", "twenty", "knock", "svix", "writer", "sentry", "ashby",
    "triggerdev", "infisical", "elevenlabs", "n8n", "highlevel", "vanta", "decagon",
    "perplexity", "glean", "cursor", "coda", "pylon", "dust", "bland", "cartesia",
    "tome", "cursor", "mintlify", "speakeasy", "unstructured", "pinecone", "weaviate",
    "chroma", "qdrant", "together", "anyscale", "runway", "luma", "midjourney"
]

# List of Greenhouse companies to check
gh_cos = [
    "postman", "groww", "phonepe", "stripe", "coinbase", "gitlab", "databricks",
    "datadog", "samsara", "twilio", "affirm", "instacart", "grafanalabs", "reddit",
    "pinterest", "dropbox", "mongodb", "airbnb", "elastic", "discord", "asana", "figma",
    "observeai", "devrev", "razorpay", "cred", "swiggy", "zomato", "zepto", "clevertap",
    "moengage", "browserstack", "chargebee", "hasura", "signoz", "inmobi", "udaan",
    "khatabook", "dream11", "mpl", "cars24", "spinny", "meesho", "smallcase", "slice",
    "jupiter", "simpl", "loco", "games24x7", "winzo", "glance", "sharechat", "inshorts",
    "pocketfm", "pratilipi", "yellowai", "sprinklr", "qubole", "druva", "cohesity",
    "rubrik", "nutanix", "purestorage", "tanium", "zscaler", "cloudflare", "okta",
    "confluent", "couchbase", "snyk", "dynatrace", "sumologic", "yugabyte", "aerospike",
    "starburst", "dbtlabs", "fivetran", "airbyte", "prefect", "dagster", "hex",
    "deepset", "anomalo", "montecarlo", "acceldata", "castai", "vantage", "komodor",
    "cloudera", "snowflake", "palantir", "crowdstrike", "sentinelone", "paloaltonetworks",
    "splunk", "datadoghq", "hashicorp", "pagerduty", "newrelic", "dynatrace"
]

# List of Lever companies to check
lever_cos = [
    "zeta", "gohighlevel", "metabase", "fampay", "cleartax", "urbancompany",
    "curefit", "mpl", "inmobi", "leadsq", "browserstack", "unacademy", "upgrad"
]

def check_title_gate(title):
    cmd = ["python", r"job-kit-starter/gates.py", "title", title]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0

results = []

def scan_ashby(co):
    if co.lower() in applied_cos:
        return []
    url = f"https://api.ashbyhq.com/posting-api/job-board/{co}"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=4).read().decode("utf-8"))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", "")
            locs = [loc] + [sl.get("location", "") for sl in j.get("secondaryLocations", [])]
            loc_str = " | ".join(locs)
            if LOC_INDIA.search(loc_str) and TITLE_INCLUDE.search(title):
                if check_title_gate(title):
                    out.append({
                        "ats": "ashby",
                        "company": co.title(),
                        "title": title,
                        "location": loc_str,
                        "url": j.get("jobUrl", f"https://jobs.ashbyhq.com/{co}/{j.get('id')}"),
                        "id": j.get("id")
                    })
    except Exception:
        pass
    return out

def scan_gh(co):
    if co.lower() in applied_cos:
        return []
    url = f"https://boards-api.greenhouse.io/v1/boards/{co}/jobs"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=4).read().decode("utf-8"))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", {}).get("name", "")
            if LOC_INDIA.search(loc) and TITLE_INCLUDE.search(title):
                if check_title_gate(title):
                    out.append({
                        "ats": "greenhouse",
                        "company": co.title(),
                        "title": title,
                        "location": loc,
                        "url": j.get("absolute_url", ""),
                        "id": str(j.get("id"))
                    })
    except Exception:
        pass
    return out

def scan_lever(co):
    if co.lower() in applied_cos:
        return []
    url = f"https://api.lever.co/v0/postings/{co}?mode=json"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=4).read().decode("utf-8"))
        for j in data:
            title = j.get("text", "")
            loc = j.get("categories", {}).get("location", "")
            if LOC_INDIA.search(loc) and TITLE_INCLUDE.search(title):
                if check_title_gate(title):
                    out.append({
                        "ats": "lever",
                        "company": co.title(),
                        "title": title,
                        "location": loc,
                        "url": j.get("hostedUrl", ""),
                        "id": j.get("id")
                    })
    except Exception:
        pass
    return out

with ThreadPoolExecutor(max_workers=25) as pool:
    futures = []
    for co in ashby_cos:
        futures.append(pool.submit(scan_ashby, co))
    for co in gh_cos:
        futures.append(pool.submit(scan_gh, co))
    for co in lever_cos:
        futures.append(pool.submit(scan_lever, co))
    for f in as_completed(futures):
        results.extend(f.result())

print(f"\nTotal qualifying roles found: {len(results)}")
with open("scratch/qualifying_ats_leads.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)

for r in results:
    print(f"[{r['ats']}] {r['company']} - {r['title']} ({r['location']}) -> {r['url']}")
