import urllib.request, json, ssl, re, html

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

req = urllib.request.Request('https://api.ashbyhq.com/posting-api/job-board/anyscale', headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode())
    for j in data.get('jobs', []):
        if j.get('title') == 'Software Engineer, Platform Infrastructure (Foundations)':
            desc = re.sub('<[^<]+?>', '', html.unescape(j.get('descriptionHtml', '')))
            print(desc)
