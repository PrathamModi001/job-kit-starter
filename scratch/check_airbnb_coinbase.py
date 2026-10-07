import urllib.request, json, ssl, re, html

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

jobs = [
    ('airbnb', 8245428),
    ('coinbase', 8165441),
    ('coinbase', 7985187)
]

for co, jid in jobs:
    try:
        url = f'https://boards-api.greenhouse.io/v1/boards/{co}/jobs/{jid}'
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            data = json.loads(r.read().decode())
            desc = re.sub('<[^<]+?>', '', html.unescape(data.get('content', '')))
            print(f"=== {co} - {data.get('title')} ({jid}) ===")
            print(f"Location: {data.get('location', {}).get('name')}")
            print(desc[:1500])
    except Exception as e:
        print(f"{co} {jid} err: {e}")
