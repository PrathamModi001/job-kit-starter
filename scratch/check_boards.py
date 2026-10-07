import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

boards = [
    ('ashby', 'composio'),
    ('ashby', 'sarvam'),
    ('ashby', 'smallest'),
    ('ashby', 'vapi'),
    ('ashby', 'langchain'),
    ('ashby', 'weaviate'),
    ('ashby', 'inngest'),
    ('lever', 'fampay'),
    ('lever', 'cred'),
    ('gh', 'observeai'),
    ('gh', 'groww'),
    ('gh', 'postman'),
]

for btype, bname in boards:
    try:
        if btype == 'ashby':
            url = f'https://api.ashbyhq.com/posting-api/job-board/{bname}'
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                for j in data.get('jobs', []):
                    title = j.get('title')
                    loc = j.get('location')
                    print(f"[{bname}] {title} | {loc} | {j.get('jobUrl')}")
        elif btype == 'lever':
            url = f'https://api.lever.co/v0/postings/{bname}'
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                for j in data:
                    title = j.get('text')
                    loc = j.get('categories', {}).get('location')
                    print(f"[{bname}] {title} | {loc} | {j.get('hostedUrl')}")
        elif btype == 'gh':
            url = f'https://boards-api.greenhouse.io/v1/boards/{bname}/jobs'
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                for j in data.get('jobs', []):
                    title = j.get('title')
                    loc = j.get('location', {}).get('name')
                    print(f"[{bname}] {title} | {loc} | {j.get('absolute_url')}")
    except Exception as e:
        print(f"[{bname}] error: {e}")
