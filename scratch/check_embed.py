import urllib.request
import re

urls = [
    'https://boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008',
    'https://boards.greenhouse.io/observeai/jobs/5432596008',
    'https://www.observe.ai/position?gh_jid=5432596008'
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            forms = re.findall(r'<form[^>]*>', content)
            print(f"URL: {u}\nStatus: {resp.status}, Final URL: {resp.geturl()}, Length: {len(content)}, Forms: {forms}")
            if forms:
                inputs = re.findall(r'name=["\']([^"\']+)["\']', content)
                print("  Inputs:", [i for i in inputs if not i.startswith('viewport')])
    except Exception as e:
        print(f"URL: {u} Error: {e}")
