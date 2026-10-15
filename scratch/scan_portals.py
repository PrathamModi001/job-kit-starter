import urllib.request, json, re, sys
from pathlib import Path

# Add job-kit-starter to sys.path
sys.path.insert(0, str(Path("job-kit-starter").resolve()))
import gates

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# 1. Hirist
print("--- Scanning Hirist ---")
try:
    url = "https://www.hirist.tech/search/node-js-developer"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        cards = re.findall(r'<a[^>]+href="(/job/[^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
        print(f"Hirist job links: {len(cards)}")
        for href, text in cards[:10]:
            print(" ", href, "->", re.sub(r'\s+', ' ', text).strip()[:80])
except Exception as e:
    print("Hirist error:", e)

# 2. Cutshort public search
print("\n--- Scanning Cutshort ---")
try:
    url = "https://cutshort.io/jobs/software-engineer-jobs"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        # check json-ld or links
        jobs = re.findall(r'<a[^>]+href="(/job/[^"]+)"', html)
        print(f"Cutshort public links: {len(jobs)}")
        for j in set(jobs)[:10]:
            print(" ", j)
except Exception as e:
    print("Cutshort error:", e)

# 3. Wellfound / AngelList public
print("\n--- Scanning Wellfound ---")
try:
    url = "https://wellfound.com/role/l/software-engineer/india"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        print("Wellfound response len:", len(html))
except Exception as e:
    print("Wellfound error:", e)
