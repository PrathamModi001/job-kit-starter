import urllib.request, json, csv, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from gates import title_skip, location_check, yoe_check

applied = {r['Company'].strip().lower() for r in csv.DictReader(open('output/job-search/applications.csv', encoding='utf-8'))}

# Greenhouse tester
def check_gh(slug, name):
    if name.lower() in applied: return []
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode('utf-8'))
            jobs = data.get('jobs', [])
            out = []
            for j in jobs:
                title = j.get('title', '')
                loc = (j.get('location') or {}).get('name', '')
                url = j.get('absolute_url', '')
                out.append({'co': name, 'title': title, 'loc': loc, 'url': url, 'type': 'gh', 'id': j.get('id')})
            return out
    except Exception:
        return []

# Ashby tester
def check_ashby(slug, name):
    if name.lower() in applied: return []
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode('utf-8'))
            jobs = data.get('jobs', [])
            out = []
            for j in jobs:
                title = j.get('title', '')
                loc = j.get('location', '')
                url = j.get('jobUrl', '')
                out.append({'co': name, 'title': title, 'loc': loc, 'url': url, 'type': 'ashby', 'id': j.get('id')})
            return out
    except Exception:
        return []

# Lever tester
def check_lever(slug, name):
    if name.lower() in applied: return []
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode('utf-8'))
            out = []
            for j in data:
                title = j.get('text', '')
                loc = (j.get('categories') or {}).get('location', '')
                url = j.get('hostedUrl', '')
                out.append({'co': name, 'title': title, 'loc': loc, 'url': url, 'type': 'lever', 'id': j.get('id'), 'desc': j.get('descriptionPlain', '')})
            return out
    except Exception:
        return []

candidates = [
    ("gh", "zepto", "Zepto"),
    ("gh", "urbancompany", "Urban Company"),
    ("gh", "clevertap", "CleverTap"),
    ("gh", "browserstack", "BrowserStack"),
    ("gh", "chargebee", "Chargebee"),
    ("gh", "hasura", "Hasura"),
    ("gh", "postman", "Postman"),
    ("ashby", "appsmith", "Appsmith"),
    ("ashby", "tooljet", "ToolJet"),
    ("ashby", "dyte", "Dyte"),
    ("ashby", "100ms", "100ms"),
    ("ashby", "openphone", "OpenPhone"),
    ("ashby", "falconx", "FalconX"),
    ("ashby", "mudrex", "Mudrex"),
    ("ashby", "pocketfm", "Pocket FM"),
    ("ashby", "dhiwise", "DhiWise"),
    ("lever", "cred", "CRED"),
    ("lever", "whatfix", "Whatfix"),
    ("lever", "leadsquared", "LeadSquared"),
    ("gh", "moengage", "MoEngage"),
    ("gh", "meesho", "Meesho"),
    ("gh", "inmobi", "InMobi"),
    ("gh", "coindcx", "CoinDCX"),
    ("ashby", "atlan", "Atlan"),
    ("gh", "dream11", "Dream11"),
    ("ashby", "curefit", "Cult.fit"),
    ("gh", "slice", "Slice"),
    ("gh", "jupiter", "Jupiter"),
    ("gh", "navi", "Navi"),
    ("gh", "khatabook", "Khatabook"),
    ("gh", "cars24", "Cars24"),
    ("gh", "atherenergy", "Ather Energy"),
    ("ashby", "swiggy", "Swiggy"),
]

all_found = []
for typ, slug, name in candidates:
    if typ == "gh":
        res = check_gh(slug, name)
    elif typ == "ashby":
        res = check_ashby(slug, name)
    elif typ == "lever":
        res = check_lever(slug, name)
    else:
        res = []
    for item in res:
        # Check title & location
        t_skip = title_skip(item['title'])
        if t_skip: continue
        loc_s, loc_why = location_check(item['loc'], item.get('desc', ''))
        if loc_s == 'skip': continue
        if loc_s == 'unknown' and not re.search(r'\b(india|bengaluru|bangalore|pune|hyderabad|mumbai|gurgaon|gurugram|noida|chennai|ahmedabad|remote)\b', item['loc'].lower()):
            continue
        all_found.append(item)

print(f"Total matching roles from Indian tech companies: {len(all_found)}")
for it in all_found:
    print(f"{it['co']} | {it['title']} | {it['loc']} | {it['url']}")
