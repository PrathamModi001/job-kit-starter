import json, urllib.request, re, subprocess

# Workday endpoints usually provide JSON search API:
# https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/jobs
# with POST {"appliedFacets":{},"limit":20,"offset":0,"searchText":"software engineer"}

workday_sites = [
    ("mastercard", "1", "CorporateCareers", "Mastercard"),
    ("autodesk", "1", "Ext", "Autodesk"),
    ("adobe", "5", "external_experienced", "Adobe"),
    ("walmart", "2", "WalmartExternal", "Walmart"),
    ("target", "1", "targetcareers", "Target"),
    ("dell", "1", "External", "Dell"),
    ("cisco", "1", "CiscoJobs", "Cisco"),
    ("salesforce", "12", "External_Career_Site", "Salesforce"),
    ("servicenow", "1", "ServiceNow", "ServiceNow"),
    ("vmware", "1", "VMware", "VMware"),
    ("intuit", "1", "Jobs", "Intuit")
]

LOC_INDIA = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|mumbai|chennai)\b", re.I)
TITLE_INCLUDE = re.compile(r"\b(software|backend|full[- ]?stack|platform|systems|developer|engineer)\b", re.I)
TITLE_EXCLUDE = re.compile(r"\b(senior|sr|lead|principal|staff|architect|manager|director|intern|qa|test|support|sales|account|marketing|mobile|ios|android|react[- ]native|customer|client|sde[- ]?[23ii]|sde\s*[23]|pe\s*2|product engineer\s*(?:2|ii)|mts|member of technical staff)\b", re.I)

def check_title(title):
    cmd = ["python", r"job-kit-starter/gates.py", "title", title]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return res.returncode == 0

out = []
for tenant, wd_num, site, co_name in workday_sites:
    url = f"https://{tenant}.wd{wd_num}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
    payload = json.dumps({"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "software engineer"}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read().decode("utf-8"))
        for j in data.get("jobPostings", []):
            title = j.get("title", "")
            loc = j.get("locationsText", "")
            external_path = j.get("externalPath", "")
            if LOC_INDIA.search(loc) and TITLE_INCLUDE.search(title) and not TITLE_EXCLUDE.search(title):
                if check_title(title):
                    job_url = f"https://{tenant}.wd{wd_num}.myworkdayjobs.com/en-US/{site}{external_path}"
                    out.append({
                        "company": co_name,
                        "title": title,
                        "location": loc,
                        "url": job_url,
                        "tenant": tenant,
                        "bullet_fields": j.get("bulletFields", [])
                    })
    except Exception as e:
        pass

print(f"Total Workday India roles found: {len(out)}")
for o in out:
    print(f"- [{o['company']}] {o['title']} ({o['location']}) -> {o['url']}")
