import urllib.request, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from gates import clean_html

url = "https://ats.rippling.com/en-GB/alaan-careers/jobs/187d971b-6e4d-4cf7-bc10-e2be2dc2f917"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html_text = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    clean_text = clean_html(html_text)
    out_dir = "output/Alaan - AI Engineer"
    os.makedirs(out_dir, exist_ok=True)
    jd_path = os.path.join(out_dir, "jd.txt")
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(clean_text)
    size = os.path.getsize(jd_path)
    print(f"Saved {jd_path}, size = {size} bytes")
except Exception as e:
    print(f"Error: {e}")
