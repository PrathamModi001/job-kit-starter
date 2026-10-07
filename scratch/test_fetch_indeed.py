import urllib.request, json, ssl, re

jk_list = [
    ('Kaistudio', 'eab1bd89410d17d7'),
    ('Mekansim', '1618497e4e59016e'),
    ('Zikrabyte', 'cdcbe9e78322d489'),
    ('OneRoot', '71bfc17e375d906c'),
    ('Noise', 'adb594c1e18e8b4e'),
    ('Workday', '030d87db6d6f93ff')
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for co, jk in jk_list:
    url = f'https://in.indeed.com/viewjob?jk={jk}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            m = re.search(r'<title>(.*?)</title>', content)
            title = m.group(1) if m else 'No title'
            print(f'{co} ({jk}): length={len(content)}, title={title}')
    except Exception as e:
        print(f'{co} ({jk}) err: {e}')
