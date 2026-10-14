import urllib.request, os, re
from bs4 import BeautifulSoup

url = "https://careers.cmco.com/job/Tamil-Nadu-Engineer%2C-Software-600032/1432441400/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style", "svg", "noscript"]):
        s.decompose()
    clean = re.sub(r"[ \t]+", " ", soup.get_text(separator="\n"))
    clean = re.sub(r"\n\s*\n+", "\n\n", clean).strip()
    out_dir = "output/Columbus McKinnon - Software Engineer"
    os.makedirs(out_dir, exist_ok=True)
    jd_path = os.path.join(out_dir, "jd.txt")
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(clean)
    print("Columbus McKinnon size:", os.path.getsize(jd_path))
except Exception as e:
    print(f"Error fetching Columbus McKinnon: {e}")
