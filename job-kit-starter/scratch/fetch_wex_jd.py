import urllib.request, os, re
from bs4 import BeautifulSoup

url = "https://careers.wexinc.com/us/en/job/WEXWEXUSR22748EXTERNALENUS/Software-Development-Engineer-1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, "html.parser")
for s in soup(["script", "style", "svg", "noscript"]):
    s.decompose()

text = soup.get_text(separator="\n")
clean = re.sub(r"[ \t]+", " ", text)
clean = re.sub(r"\n\s*\n+", "\n\n", clean).strip()

out_dir = "output/WEX - Software Development Engineer 1"
os.makedirs(out_dir, exist_ok=True)
jd_path = os.path.join(out_dir, "jd.txt")
with open(jd_path, "w", encoding="utf-8") as f:
    f.write(clean)

print("Saved clean WEX jd.txt size:", os.path.getsize(jd_path))
