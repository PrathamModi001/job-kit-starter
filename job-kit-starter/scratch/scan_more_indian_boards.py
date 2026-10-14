import urllib.request, json, csv, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from gates import title_skip, location_check, yoe_check

applied = {r['Company'].strip().lower() for r in csv.DictReader(open('output/job-search/applications.csv', encoding='utf-8'))}

# Extended list of companies
companies = [
    # Greenhouse
    ("gh", "juspay", "Juspay"),
    ("gh", "groww", "Groww"),
    ("gh", "rapido", "Rapido"),
    ("gh", "spinny", "Spinny"),
    ("gh", "bluestone", "BlueStone"),
    ("gh", "mpl", "Mobile Premier League"),
    ("gh", "unacademy", "Unacademy"),
    ("gh", "upstox", "Upstox"),
    ("gh", "zerodha", "Zerodha"),
    ("gh", "credgenics", "Credgenics"),
    ("gh", "rebel", "Rebel Foods"),
    ("gh", "shadowfax", "Shadowfax"),
    ("gh", "shiprocket", "Shiprocket"),
    ("gh", "porter", "Porter"),
    ("gh", "lenskart", "Lenskart"),
    ("gh", "cuemath", "Cuemath"),
    ("gh", "loconav", "LocoNav"),
    ("gh", "classplus", "Classplus"),
    ("gh", "invideo", "InVideo"),
    ("gh", "yellowai", "Yellow.ai"),
    ("gh", "haptik", "Haptik"),
    ("gh", "glance", "Glance"),
    ("gh", "sharechat", "ShareChat"),
    ("gh", "dailyhunt", "Dailyhunt"),
    ("gh", "ola", "Ola"),
    ("gh", "olaelectric", "Ola Electric"),
    ("gh", "bounce", "Bounce"),
    ("gh", "acko", "Acko"),
    ("gh", "navi", "Navi"),
    ("gh", "turtlemint", "Turtlemint"),
    ("gh", "bankbazaar", "BankBazaar"),
    ("gh", "policybazaar", "Policybazaar"),
    ("gh", "paisabazaar", "Paisabazaar"),
    ("gh", "moneyview", "Money View"),
    ("gh", "rupeek", "Rupeek"),
    ("gh", "indwealth", "INDmoney"),
    ("gh", "scripbox", "Scripbox"),
    ("gh", "smallcase", "smallcase"),
    ("gh", "tijori", "Tijori"),
    ("gh", "dezerv", "Dezerv"),
    ("gh", "stable", "Stable Money"),
    ("gh", "wealthy", "Wealthy"),
    # Ashby
    ("ashby", "hyperverge", "HyperVerge"),
    ("ashby", "greyorange", "GreyOrange"),
    ("ashby", "kula", "Kula"),
    ("ashby", "toplyne", "Toplyne"),
    ("ashby", "privado", "Privado"),
    ("ashby", "sprinto", "Sprinto"),
    ("ashby", "scrut", "Scrut Automation"),
    ("ashby", "stride", "Stride"),
    ("ashby", "atomicwork", "Atomicwork"),
    ("ashby", "devzero", "DevZero"),
    ("ashby", "restate", "Restate"),
    ("ashby", "augment", "Augment"),
    ("ashby", "cursor", "Cursor"),
    ("ashby", "cognition", "Cognition"),
    ("ashby", "poolside", "Poolside"),
    ("ashby", "magic", "Magic"),
    ("ashby", "factory", "Factory"),
    ("ashby", "braintrust", "Braintrust"),
    ("ashby", "arize", "Arize AI"),
    ("ashby", "phoenix", "Phoenix"),
    ("ashby", "honeycomb", "Honeycomb"),
    ("ashby", "chronosphere", "Chronosphere"),
    ("ashby", "signoz", "SigNoz"),
    ("ashby", "coralogix", "Coralogix"),
    ("ashby", "betterstack", "Better Stack"),
    ("ashby", "highlight", "Highlight"),
    ("ashby", "posthog", "PostHog"),
    ("ashby", "mixpanel", "Mixpanel"),
    ("ashby", "amplitude", "Amplitude"),
    ("ashby", "statsig", "Statsig"),
    ("ashby", "growthbook", "GrowthBook"),
    ("ashby", "launchdarkly", "LaunchDarkly"),
    ("ashby", "unleash", "Unleash"),
    ("ashby", "flagsmith", "Flagsmith"),
    ("ashby", "flipt", "Flipt"),
]

def check_board(typ, slug, name):
    if name.lower() in applied: return []
    out = []
    if typ == "gh":
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as res:
                data = json.loads(res.read().decode('utf-8'))
                for j in data.get('jobs', []):
                    out.append({'co': name, 'title': j.get('title',''), 'loc': (j.get('location') or {}).get('name',''), 'url': j.get('absolute_url',''), 'type': 'gh', 'id': j.get('id')})
        except Exception:
            pass
    elif typ == "ashby":
        url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as res:
                data = json.loads(res.read().decode('utf-8'))
                for j in data.get('jobs', []):
                    out.append({'co': name, 'title': j.get('title',''), 'loc': j.get('location',''), 'url': j.get('jobUrl',''), 'type': 'ashby', 'id': j.get('id')})
        except Exception:
            pass
    return out

found = []
for typ, slug, name in companies:
    jobs = check_board(typ, slug, name)
    for j in jobs:
        t_skip = title_skip(j['title'])
        if t_skip: continue
        loc_s, loc_why = location_check(j['loc'], '')
        if loc_s == 'skip': continue
        if loc_s == 'unknown' and not re.search(r'\b(india|bengaluru|bangalore|pune|hyderabad|mumbai|gurgaon|gurugram|noida|chennai|ahmedabad|remote)\b', j['loc'].lower()):
            continue
        found.append(j)

print(f"Total matching roles found: {len(found)}")
for f in found:
    print(f"{f['co']} | {f['title']} | {f['loc']} | {f['url']}")
