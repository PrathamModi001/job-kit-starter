import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
    ('Accept', 'application/json, text/plain, */*')
]

unapplied = ['firecrawl', 'linear', 'modal', 'neon', 'render', 'weaviate', 'pinecone', 'resend', 'warp', 'e2b', 'zed', 'sarvam', 'vapi', 'smallest', 'stack-ai', 'julius', 'langfuse', 'baseten', 'twenty', 'n8n', 'svix', 'knock', 'writer', 'deepgram', 'atlan', 'sentry', 'replit', 'zapier', 'revenuecat', 'vanta', 'sierra', 'decagon', '1password', 'ashby', 'triggerdev']

for c in unapplied:
    url = f"https://api.ashbyhq.com/posting-api/job-board/{c}?includeCompensation=true"
    try:
        resp = opener.open(url, timeout=4)
        data = json.loads(resp.read().decode('utf-8'))
        jobs = data.get('jobs', [])
        for j in jobs:
            title = j.get('title', '')
            loc = j.get('location') or ('Remote' if j.get('isRemote') else '')
            sec = ", ".join(x.get("location", "") for x in (j.get("secondaryLocations") or []) if x.get("location"))
            if sec:
                loc = f"{loc} ({sec})"
            desc = j.get('descriptionPlain', '') or ''
            t_low = title.lower()
            l_low = loc.lower()
            if any(k in t_low for k in ['software', 'engineer', 'developer', 'frontend', 'backend', 'full stack', 'fullstack']):
                if ('india' in l_low or 'bengaluru' in l_low or 'bangalore' in l_low or 'delhi' in l_low or 'mumbai' in l_low or 'remote' in l_low) and not ('us only' in l_low or 'united states only' in l_low or 'americas only' in l_low or 'europe only' in l_low or 'latam' in l_low):
                    print(f"MATCH: [{c}] {title} | Loc: {loc} | URL: {j.get('jobUrl')}")
    except Exception as e:
        # print(f"Err {c}: {e}")
        pass

print("Ashby scan done.")
