import urllib.request
import re
import html as html_lib

url = "https://vvd.world/careers"
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

with open("scratch/vvd_careers.html", "w", encoding="utf-8") as f:
    f.write(html)

clean = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'<[^<]+?>', ' ', clean)
clean = html_lib.unescape(clean)
clean = '\n'.join([line.strip() for line in clean.splitlines() if line.strip()])

print("VVD preview:\n", clean[:600])
