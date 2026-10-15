import urllib.request, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path("E:/Extra/job-kit-starter/job-kit-starter").resolve()))
import gates

gh_boards = [
    "postman", "atlan", "hasura", "browserstack", "blinkit", "urbancompany",
    "cred", "groww", "sliceit", "meesho", "swiggy", "hevodata",
    "signoz", "infisical", "composio", "cartesia", "livekit", "doordashindia",
    "rubrik", "crunchyroll", "okta", "airbnb", "airtable", "sentry", "affirm",
    "stripe", "gusto", "ramp", "brex", "coinbase", "brevo", "invideo"
]

headers = {'User-Agent': 'Mozilla/5.0'}

hits = []

for b in gh_boards:
    url = f"https://boards-api.greenhouse.io/v1/boards/{b}/jobs?content=true"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            jobs = data.get('jobs', [])
            for j in jobs:
                title = j.get('title', '')
                loc = (j.get('location') or {}).get('name', '')
                jid = j.get('id')
                jurl = j.get('absolute_url', '')
                content = j.get('content', '')
                cleaned = gates.clean_html(content)
                
                # Check title
                tskip = gates.title_skip(title)
                if tskip:
                    continue
                    
                # Check dedup
                dup = gates.dedup(b.title())
                if dup:
                    continue
                    
                # Check location
                loc_st, loc_why = gates.location_check(loc, cleaned)
                if loc_st == 'skip':
                    continue
                    
                # Check YOE
                yoe_st, yoe_ev = gates.yoe_check(cleaned)
                if yoe_st == 'skip':
                    continue
                    
                sc, parts = gates.fit_score(title, cleaned, loc)
                if sc < 11 or parts['lane'] < 3:
                    continue
                    
                print(f"GH HIT: {b} | {title} | {loc} | YOE: {yoe_st} ({yoe_ev}) | Fit: {sc} | {jurl}")
                hits.append({
                    "board": b,
                    "company": b.title(),
                    "title": title,
                    "location": loc,
                    "apply_url": jurl,
                    "yoe_st": yoe_st,
                    "yoe_ev": yoe_ev,
                    "fit_score": sc,
                    "desc": cleaned
                })
    except Exception as e:
        # print(f"Error {b}: {e}")
        pass

# Ashby boards
ashby_boards = [
    "supabase", "replit", "resend", "railway", "elevenlabs", "livekit",
    "smallest", "posthog", "vapi", "cartesia", "langfuse", "modal", "neon",
    "avoca", "braintrust", "cursor"
]

for b in ashby_boards:
    url = f"https://api.ashbyhq.com/posting-api/job-board/{b}?includeCompensation=true"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            jobs = data.get('jobs', [])
            for j in jobs:
                title = j.get('title', '')
                loc = j.get('location', '')
                jurl = j.get('jobUrl', '')
                desc = j.get('descriptionHtml', '')
                cleaned = gates.clean_html(desc)
                
                tskip = gates.title_skip(title)
                if tskip:
                    continue
                    
                dup = gates.dedup(b.title())
                if dup:
                    continue
                    
                loc_st, loc_why = gates.location_check(loc, cleaned)
                if loc_st == 'skip':
                    continue
                    
                yoe_st, yoe_ev = gates.yoe_check(cleaned)
                if yoe_st == 'skip':
                    continue
                    
                sc, parts = gates.fit_score(title, cleaned, loc)
                if sc < 11 or parts['lane'] < 3:
                    continue
                    
                print(f"ASHBY HIT: {b} | {title} | {loc} | YOE: {yoe_st} ({yoe_ev}) | Fit: {sc} | {jurl}")
                hits.append({
                    "board": b,
                    "company": b.title(),
                    "title": title,
                    "location": loc,
                    "apply_url": jurl,
                    "yoe_st": yoe_st,
                    "yoe_ev": yoe_ev,
                    "fit_score": sc,
                    "desc": cleaned
                })
    except Exception as e:
        # print(f"Error ashby {b}: {e}")
        pass

print(f"\nTotal ATS hits: {len(hits)}")
with open("E:/Extra/job-kit-starter/scratch/ats_hits.json", "w", encoding="utf-8") as f:
    json.dump(hits, f, indent=2)
