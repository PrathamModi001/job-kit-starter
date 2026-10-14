import urllib.request, os, re
from bs4 import BeautifulSoup

url = "https://hp.wd5.myworkdayjobs.com/ExternalCareerSite/job/Bengaluru-Karntaka-India/Software-Applications_3166748-1"
# Workday pages typically have a public REST API: /ExternalCareerSite/job/... or the job text in JSON
# Let's test fetching the HTML or JSON from workday
api_url = "https://hp.wd5.myworkdayjobs.com/wday/cxs/hp/ExternalCareerSite/job/Bengaluru-Karntaka-India/Software-Applications_3166748-1"
req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept': 'application/json'})
try:
    with urllib.request.urlopen(req) as res:
        data = res.read().decode('utf-8')
        import json
        job_data = json.loads(data)
        desc = job_data.get('jobPostingInfo', {}).get('jobDescription', '')
        soup = BeautifulSoup(desc, 'html.parser')
        clean = soup.get_text(separator="\n").strip()
        out_dir = "output/HP - Software Applications"
        os.makedirs(out_dir, exist_ok=True)
        jd_path = os.path.join(out_dir, "jd.txt")
        with open(jd_path, "w", encoding="utf-8") as f:
            f.write(clean)
        print("Workday JSON fetch success! Size:", os.path.getsize(jd_path))
except Exception as e:
    print(f"Workday API fetch error: {e}")
    # Fallback to HTML
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style", "svg", "noscript"]):
        s.decompose()
    clean = re.sub(r"\n\s*\n+", "\n\n", soup.get_text(separator="\n")).strip()
    out_dir = "output/HP - Software Applications"
    os.makedirs(out_dir, exist_ok=True)
    jd_path = os.path.join(out_dir, "jd.txt")
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(clean)
    print("Workday HTML fallback size:", os.path.getsize(jd_path))
