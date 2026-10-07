import urllib.request
import json
import os
import html
import re

url = 'https://boards-api.greenhouse.io/v1/boards/observeai/jobs/5432596008?questions=true'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

out_dir = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer'
os.makedirs(out_dir, exist_ok=True)

content_raw = data.get('content', '')
content_unescaped = html.unescape(content_raw)

full_jd_text = f"Title: {data.get('title')}\nLocation: {data.get('location', {}).get('name')}\nURL: https://job-boards.greenhouse.io/observeai/jobs/5432596008\n\n{content_unescaped}"

jd_file = os.path.join(out_dir, 'jd.txt')
with open(jd_file, 'w', encoding='utf-8') as f:
    f.write(full_jd_text)

print(f"Written jd.txt to {jd_file}, length {len(full_jd_text)}")
