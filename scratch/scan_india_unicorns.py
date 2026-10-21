import json
import urllib.request
import re
import csv
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

LOC_INDIA = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|mumbai|chennai|ahmedabad|remote)\b", re.I)
FOREIGN = re.compile(r"\b(us|usa|united states|canada|uk|united kingdom|poland|germany|france|spain|mexico|singapore|australia|malaysia|ireland|netherlands|romania|sweden|switzerland)\b", re.I)
TITLE_INCLUDE = re.compile(r"\b(software|backend|full[- ]?stack|platform|systems|developer|engineer)\b", re.I)

# Target boards to check
gh_boards = [
    ("browserstack", "BrowserStack"),
    ("chargebee", "Chargebee"),
    ("clevertap", "CleverTap"),
    ("moengage", "MoEngage"),
    ("inmobi", "InMobi"),
    ("meesho", "Meesho"),
    ("groww", "Groww"),
    ("phonepe", "PhonePe"),
    ("swiggy", "Swiggy"),
    ("zomato", "Zomato"),
    ("zepto", "Zepto"),
    ("urbancompany", "Urban Company"),
    ("curefit", "Curefit"),
    ("cleartax", "ClearTax"),
    ("lenskart", "Lenskart"),
    ("nykaa", "Nykaa"),
    ("spinny", "Spinny"),
    ("cars24", "Cars24"),
    ("simpl", "Simpl"),
    ("slice", "Slice"),
    ("jupiter", "Jupiter"),
    ("smallcase", "Smallcase"),
    ("khatabook", "Khatabook"),
    ("dream11", "Dream11"),
    ("games24x7", "Games24x7"),
    ("winzo", "WinZO"),
    ("sharechat", "ShareChat"),
    ("pocketfm", "Pocket FM"),
    ("pratilipi", "Pratilipi"),
    ("yellowai", "Yellow.ai"),
    ("sprinklr", "Sprinklr"),
    ("razorpay", "Razorpay"),
    ("cred", "CRED"),
    ("postman", "Postman"),
    ("hasura", "Hasura"),
    ("signoz", "SigNoz")
]

lever_boards = [
    ("browserstack", "BrowserStack"),
    ("cleartax", "ClearTax"),
    ("urbancompany", "Urban Company"),
    ("curefit", "Curefit"),
    ("inmobi", "InMobi"),
    ("leadsq", "LeadSquared"),
    ("fampay", "FamPay"),
    ("zeta", "Zeta"),
    ("unacademy", "Unacademy"),
    ("upgrad", "upGrad"),
    ("cred", "CRED"),
    ("mpl", "MPL")
]

def check_title_gate(title):
    cmd = ["python", r"job-kit-starter/gates.py", "title", title]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0

results = []

def check_gh(slug, co_name):
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
                            "company": co_name,
                            "title": title,
                            "location": loc,
                            "url": j.get("absolute_url", ""),
                            "id": str(j.get("id"))
                        })
    except Exception:
        pass
    return out

def check_lever(slug, co_name):
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=4).read().decode("utf-8"))
        for j in data:
            title = j.get("text", "")
            loc = j.get("categories", {}).get("location", "")
            if LOC_INDIA.search(loc) and not (FOREIGN.search(loc) and "india" not in loc.lower()):
                if TITLE_INCLUDE.search(title) and not re.search(r"\b(sales|support|escalation|manager|director|intern|lead|senior|sr)\b", title, re.I):
                    if check_title_gate(title):
                        out.append({
                            "ats": "lever",
                            "company": co_name,
                            "title": title,
                            "location": loc,
                            "url": j.get("hostedUrl", ""),
                            "id": j.get("id")
                        })
    except Exception:
        pass
    return out

with ThreadPoolExecutor(max_workers=30) as pool:
    futures = [pool.submit(check_gh, s, n) for s, n in gh_boards] + [pool.submit(check_lever, s, n) for s, n in lever_boards]
    for f in as_completed(futures):
        results.extend(f.result())

print(f"Total Unicorn roles found: {len(results)}")
for r in results:
    print(f"[{r['ats']}] {r['company']} - {r['title']} ({r['location']}) -> {r['url']}")

with open("scratch/unicorn_leads.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)
