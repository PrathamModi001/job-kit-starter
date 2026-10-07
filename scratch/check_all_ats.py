import urllib.request, json, ssl, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Read job_hunt.py SOURCES
sources_file = os.path.join('job-kit-starter', 'job_hunt.py')
sources = []
with open(sources_file, 'r', encoding='utf-8') as f:
    text = f.read()
    import re
    # find tuples like ("gh", "vercel", "Vercel")
    matches = re.findall(r'\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\)', text)
    sources = matches

print(f"Loaded {len(sources)} sources from job_hunt.py")

results = []

def check_source(stype, slug, name):
    found = []
    try:
        if stype == 'gh':
            url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                data = json.loads(r.read().decode())
                for j in data.get('jobs', []):
                    title = j.get('title', '')
                    loc = str(j.get('location', {}).get('name', ''))
                    found.append((name, title, loc, j.get('absolute_url'), 'gh'))
        elif stype == 'ashby':
            url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                data = json.loads(r.read().decode())
                for j in data.get('jobs', []):
                    title = j.get('title', '')
                    loc = str(j.get('location', ''))
                    found.append((name, title, loc, j.get('jobUrl'), 'ashby'))
        elif stype == 'lever':
            url = f"https://api.lever.co/v0/postings/{slug}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                data = json.loads(r.read().decode())
                for j in data:
                    title = j.get('text', '')
                    loc = str(j.get('categories', {}).get('location', ''))
                    found.append((name, title, loc, j.get('hostedUrl'), 'lever'))
    except Exception as e:
        pass
    return found

import concurrent.futures
all_jobs = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    futs = [ex.submit(check_source, s[0], s[1], s[2]) for s in sources]
    for fut in concurrent.futures.as_completed(futs):
        all_jobs.extend(fut.result())

print(f"Total jobs pulled: {len(all_jobs)}")

# Filter for India or Remote and SWE/Backend/Fullstack/AI
kw = ['engineer', 'developer', 'software']
india_kw = ['india', 'bengaluru', 'bangalore', 'hyderabad', 'pune', 'mumbai', 'gurgaon', 'gurugram', 'remote']

filtered = []
for co, title, loc, url, stype in all_jobs:
    t_lower = title.lower()
    l_lower = loc.lower()
    if any(k in t_lower for k in kw):
        if any(ik in l_lower for ik in india_kw) or 'remote' in l_lower:
            filtered.append((co, title, loc, url, stype))

print(f"Filtered relevant roles: {len(filtered)}")
for f in sorted(filtered, key=lambda x: x[0]):
    print(f"{f[0]} | {f[1]} | {f[2]} | {f[3]}")
