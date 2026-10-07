import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    req = urllib.request.Request('https://aiven.io/careers/open-positions', headers=headers)
    with urllib.request.urlopen(req, context=ctx) as r:
        html_text = r.read().decode('utf-8', errors='ignore')
        print('Aiven careers page length:', len(html_text))
except Exception as e:
    print('Aiven err:', e)
