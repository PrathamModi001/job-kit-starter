import urllib.request, os, re
from bs4 import BeautifulSoup

url = "https://ats.rippling.com/en-GB/alaan-careers/jobs/187d971b-6e4d-4cf7-bc10-e2be2dc2f917"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, "html.parser")
for s in soup(["script", "style", "svg", "noscript"]):
    s.decompose()

text = soup.get_text(separator="\n")
clean = re.sub(r"[ \t]+", " ", text)
clean = re.sub(r"\n\s*\n+", "\n\n", clean).strip()

out_path = "output/Alaan - AI Engineer/jd.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(clean)

print("Saved clean Alaan jd.txt size:", os.path.getsize(out_path))
