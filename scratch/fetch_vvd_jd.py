import urllib.request
import re
import html as html_lib
import os

url = "https://vvd.world/careers/junior-product-engineer"
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

clean = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'<[^<]+?>', ' ', clean)
clean = html_lib.unescape(clean)
clean = '\n'.join([line.strip() for line in clean.splitlines() if line.strip()])

full_jd = f"""Company: vvd (vvd.world)
Title: Junior Product Engineer
Location: Remote (EU/NA timezones)
URL: {url}

Job Description:
{clean}
"""

target_dir = "job-kit-starter/output/vvd - Junior Product Engineer"
os.makedirs(target_dir, exist_ok=True)
with open(os.path.join(target_dir, "jd.txt"), "w", encoding="utf-8") as f:
    f.write(full_jd)

print("Saved vvd jd.txt length:", len(full_jd))
print("Preview:\n", clean[:600])
