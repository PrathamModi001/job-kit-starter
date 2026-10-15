import urllib.request
import re
import html as html_lib
import os

url = "https://typify.dev/jobs/view/189"
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

clean_text = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
clean_text = re.sub(r'<style.*?</style>', '', clean_text, flags=re.DOTALL)
clean_text = re.sub(r'<[^<]+?>', ' ', clean_text)
clean_text = html_lib.unescape(clean_text)
clean_text = '\n'.join([line.strip() for line in clean_text.splitlines() if line.strip()])

full_jd = f"Company: Typify.dev\nRole: AI Application Engineer\nURL: {url}\nHiring Contact: galen@typify.dev\nCompensation: $80-120K USD (Negotiable)\n\nJob Description:\n{clean_text}\n"

target_dir = "job-kit-starter/output/Typify - AI Application Engineer"
os.makedirs(target_dir, exist_ok=True)
with open(os.path.join(target_dir, "jd.txt"), "w", encoding="utf-8") as f:
    f.write(full_jd)

print("Saved Typify jd.txt length:", len(full_jd))
print("Preview:\n", clean_text[:400])
