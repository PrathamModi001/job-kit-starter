import urllib.request, json, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

companies = [
    ("gh", "vercel"), ("gh", "cockroachlabs"), ("gh", "planetscale"),
    ("gh", "temporaltechnologies"), ("gh", "databricks"), ("gh", "datadog"),
    ("ashby", "linear"), ("ashby", "railway"), ("ashby", "render"),
    ("gh", "phonepe"), ("ashby", "warp"), ("ashby", "zed"),
    ("ashby", "sarvam"), ("ashby", "smallest"), ("ashby", "stack-ai"),
    ("ashby", "julius"), ("ashby", "langfuse"), ("ashby", "anyscale"),
    ("ashby", "twenty"), ("lever", "tinybird"), ("ashby", "svix"), ("ashby", "knock")
]

for btype, bname in companies:
    try:
        if btype == 'ashby':
            url = f'https://api.ashbyhq.com/posting-api/job-board/{bname}'
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                for j in data.get('jobs', []):
                    title = j.get('title', '')
                    loc = str(j.get('location', ''))
                    # check if engineering
                    if any(k in title.lower() for k in ['engineer', 'developer', 'software', 'backend', 'fullstack', 'full stack']):
                        print(f"[{bname}] {title} | {loc} | {j.get('jobUrl')}")
        elif btype == 'gh':
            url = f'https://boards-api.greenhouse.io/v1/boards/{bname}/jobs'
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                for j in data.get('jobs', []):
                    title = j.get('title', '')
                    loc = str(j.get('location', {}).get('name', ''))
                    if any(k in title.lower() for k in ['engineer', 'developer', 'software', 'backend', 'fullstack', 'full stack']):
                        print(f"[{bname}] {title} | {loc} | {j.get('absolute_url')}")
        elif btype == 'lever':
            url = f'https://api.lever.co/v0/postings/{bname}'
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                for j in data:
                    title = j.get('text', '')
                    loc = str(j.get('categories', {}).get('location', ''))
                    if any(k in title.lower() for k in ['engineer', 'developer', 'software', 'backend', 'fullstack', 'full stack']):
                        print(f"[{bname}] {title} | {loc} | {j.get('hostedUrl')}")
    except Exception as e:
        # pass errors
        pass
