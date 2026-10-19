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

ashby_cos = [
    "sarvam", "composio", "smallest", "atlan", "vapi", "e2b", "browserbase", "firecrawl",
    "langchain", "langfuse", "resend", "inngest", "supabase", "deepgram", "replit",
    "modal", "linear", "twenty", "knock", "svix", "writer", "sentry", "ashby",
    "triggerdev", "infisical", "elevenlabs", "n8n", "highlevel", "vanta", "decagon",
    "blinkit", "zepto", "swiggy", "zomato", "curefit", "urbancompany"
]

lever_cos = [
    "gohighlevel", "metabase", "zeta", "fampay", "cleartax", "urbancompany",
    "curefit", "mpl", "browserstack", "inmobi", "leadsq"
]

greenhouse_cos = [
    "postman", "groww", "phonepe", "stripe", "coinbase", "gitlab", "databricks",
    "datadog", "samsara", "twilio", "affirm", "instacart", "grafanalabs", "reddit",
    "pinterest", "dropbox", "mongodb", "airbnb", "elastic", "discord", "asana", "figma",
    "observeai", "devrev", "razorpay", "cred", "swiggy", "zomato", "zepto"
]

results = []

def check_ashby(co):
    if co.lower() in applied_cos:
        return []
    url = f"https://api.ashbyhq.com/posting-api/job-board/{co}"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=3).read().decode("utf-8"))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", "")
            locs = [loc] + [sl.get("location", "") for sl in j.get("secondaryLocations", [])]
            loc_str = " | ".join(locs)
            if LOC_INDIA.search(loc_str) and TITLE_INCLUDE.search(title) and not TITLE_EXCLUDE.search(title):
                out.append({
                    "ats": "ashby",
                    "company": co.title(),
                    "title": title,
                    "location": loc_str,
                    "url": j.get("jobUrl", f"https://jobs.ashbyhq.com/{co}/{j.get('id')}")
                })
    except Exception:
        pass
    return out

def check_lever(co):
    if co.lower() in applied_cos:
        return []
    url = f"https://api.lever.co/v0/postings/{co}?mode=json"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=3).read().decode("utf-8"))
        for j in data:
            title = j.get("text", "")
            loc = j.get("categories", {}).get("location", "")
            all_locs = loc + " " + " ".join(j.get("categories", {}).get("allLocations", []))
            if LOC_INDIA.search(all_locs) and TITLE_INCLUDE.search(title) and not TITLE_EXCLUDE.search(title):
                out.append({
                    "ats": "lever",
                    "company": co.title(),
                    "title": title,
                    "location": loc,
                    "url": j.get("hostedUrl", "")
                })
    except Exception:
        pass
    return out

def check_gh(co):
    if co.lower() in applied_cos:
        return []
    url = f"https://boards-api.greenhouse.io/v1/boards/{co}/jobs"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=3).read().decode("utf-8"))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", {}).get("name", "")
            if LOC_INDIA.search(loc) and TITLE_INCLUDE.search(title) and not TITLE_EXCLUDE.search(title):
                out.append({
                    "ats": "greenhouse",
                    "company": co.title(),
                    "title": title,
                    "location": loc,
                    "url": j.get("absolute_url", "")
                })
    except Exception:
        pass
    return out

with ThreadPoolExecutor(max_workers=15) as pool:
    futures = [pool.submit(check_ashby, c) for c in ashby_cos] + \
              [pool.submit(check_lever, c) for c in lever_cos] + \
              [pool.submit(check_gh, c) for c in greenhouse_cos]
    for f in as_completed(futures):
        results.extend(f.result())

print(f"\n--- MATCHED LIVE ROLES ({len(results)}) ---", flush=True)
for r in results:
    print(f"[{r['ats']}] {r['company']} - {r['title']} ({r['location']}) -> {r['url']}", flush=True)
