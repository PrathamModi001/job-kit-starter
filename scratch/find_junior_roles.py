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
FOREIGN = re.compile(r"\b(us|usa|united states|canada|uk|united kingdom|poland|germany|france|spain|mexico|singapore|australia|malaysia|ireland|netherlands|romania|sweden|switzerland|remote - us|remote - usa|remote us|remote - canada)\b", re.I)
TITLE_INCLUDE = re.compile(r"\b(software|backend|full[- ]?stack|platform|systems|developer|engineer)\b", re.I)
TITLE_EXCLUDE = re.compile(r"\b(sales|support|escalation|manager|director|intern|lead|senior|sr|staff|principal|architect|sde[- ]?[23ii]|sde\s*[23]|pe\s*2|product engineer\s*(?:2|ii)|mts|member of technical staff|mobile|react[- ]native|forward deployed)\b", re.I)

boards_to_check = [
    "gitlab", "elastic", "cockroachlabs", "mongodb", "cloudflare", "okta", "confluent",
    "couchbase", "snyk", "postman", "airbnb", "asana", "figma", "dropbox", "box",
    "atlassian", "twilio", "stripe", "datadog", "databricks", "hashicorp", "pagerduty",
    "newrelic", "freshworks", "chargebee", "innovaccer", "whatfix", "browserstack",
    "rubrik", "cohesity", "nutanix", "cloudera", "snowflake", "palantir", "crowdstrike",
    "sentinelone", "paloaltonetworks", "splunk", "dynatrace", "sumologic", "yugabyte",
    "aerospike", "dbtlabs", "fivetran", "airbyte", "prefect", "dagster", "hex",
    "deepset", "anomalo", "montecarlo", "acceldata", "castai", "vantage", "komodor"
]

def check_title(title):
    cmd = ["python", r"job-kit-starter/gates.py", "title", title]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return res.returncode == 0

def clean_jd(html):
    cmd = ["python", r"job-kit-starter/gates.py", "clean"]
    res = subprocess.run(cmd, input=html, capture_output=True, text=True, encoding="utf-8")
    return res.stdout.strip()

def check_yoe(text):
    temp = Path("scratch/temp_jd.txt")
    temp.write_text(text, encoding="utf-8")
    cmd = ["python", r"job-kit-starter/gates.py", "yoe", str(temp)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return res.returncode == 0, res.stdout.strip()

results = []

def check_board(slug):
    if slug.lower() in applied_cos:
        return []
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", {}).get("name", "")
            if LOC_INDIA.search(loc) and not (FOREIGN.search(loc) and "india" not in loc.lower()):
                if TITLE_INCLUDE.search(title) and not TITLE_EXCLUDE.search(title):
                    if check_title(title):
                        jd_clean = clean_jd(j.get("content", ""))
                        if len(jd_clean) >= 1500:
                            yoe_ok, yoe_msg = check_yoe(jd_clean)
                            if yoe_ok:
                                out.append({
                                    "company": slug.title(),
                                    "title": title,
                                    "location": loc,
                                    "url": j.get("absolute_url", ""),
                                    "id": str(j.get("id")),
                                    "yoe": yoe_msg,
                                    "jd": jd_clean
                                })
    except Exception:
        pass
    return out

with ThreadPoolExecutor(max_workers=30) as pool:
    futures = [pool.submit(check_board, b) for b in boards_to_check]
    for f in as_completed(futures):
        results.extend(f.result())

print(f"Total matching roles with YOE OK: {len(results)}")
for r in results:
    print(f"- [{r['company']}] {r['title']} ({r['location']}) | YOE: {r['yoe']} | URL: {r['url']}")

with open("scratch/junior_gh_roles.json", "w", encoding="utf-8") as f:
    # write metadata without the large jd dump
    meta = [{k: v for k, v in r.items() if k != "jd"} for r in results]
    json.dump(meta, f, indent=2)
