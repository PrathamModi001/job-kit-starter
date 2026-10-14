import urllib.request, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from gates import clean_html

url = "https://careers.idfcfirst.bank.in/in/en/job/IFBAINP224954ENIN/Backend-Engineer-AI-Labs"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html_text = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
clean_text = clean_html(html_text)

out_dir = "output/IDFC FIRST Bank - Backend Engineer - AI Labs"
os.makedirs(out_dir, exist_ok=True)
jd_path = os.path.join(out_dir, "jd.txt")
with open(jd_path, "w", encoding="utf-8") as f:
    f.write(clean_text)

size = os.path.getsize(jd_path)
print(f"Saved {jd_path}, size = {size} bytes")
