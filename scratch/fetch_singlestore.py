import urllib.request
import json
import os
import re
import html as html_lib

url = "https://boards-api.greenhouse.io/v1/boards/singlestore/jobs/7573638"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

content = data.get('content', '')
clean_text = re.sub(r'<[^<]+?>', ' ', content)
clean_text = html_lib.unescape(clean_text)
clean_text = '\n'.join([line.strip() for line in clean_text.splitlines() if line.strip()])

full_jd = f"""Company: SingleStore
Title: {data.get('title')}
Location: {data.get('location', {}).get('name')}
URL: https://job-boards.greenhouse.io/singlestore/jobs/7573638

Job Description:
{clean_text}
"""

target_dir = "job-kit-starter/output/SingleStore - Software Engineer, AI Platform"
os.makedirs(target_dir, exist_ok=True)
with open(os.path.join(target_dir, "jd.txt"), "w", encoding="utf-8") as f:
    f.write(full_jd)
print("Saved SingleStore jd.txt length:", len(full_jd))
