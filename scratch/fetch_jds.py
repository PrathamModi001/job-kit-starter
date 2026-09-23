import urllib.request
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        return urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f"ERROR: {e}"

# 1. Avoca (Ashby)
print("=== 1. AVOCA (Ashby) ===")
ashby_html = fetch("https://api.ashbyhq.com/posting-api/job-board/avoca")
try:
    data = json.loads(ashby_html)
    job = [j for j in data.get('jobs', []) if '6758ee84' in j.get('id', '') or 'Deployment' in j.get('title', '')]
    if job:
        print("Avoca Job Title:", job[0].get('title'))
        print("Location:", job[0].get('location'))
        print("Description snippet:", job[0].get('descriptionPlain', '')[:1000])
    else:
        print("Avoca job not found in job-board list, fetching direct Ashby...")
        direct = fetch("https://jobs.ashbyhq.com/avoca/6758ee84-51b4-4d0d-a3a6-d40ec164de49")
        print("Direct Ashby snippet:", direct[:500])
except Exception as e:
    print("Avoca error:", e)

# 2. Hevo Data (Lever)
print("\n=== 2. HEVO DATA (Lever) ===")
lever_json = fetch("https://api.lever.co/v0/postings/hevodata/6cbbe304-e065-4711-bf3e-756795d2bc2a")
try:
    ldata = json.loads(lever_json)
    print("Hevo Title:", ldata.get('text'))
    print("Categories:", ldata.get('categories'))
    print("Description snippet:", ldata.get('descriptionPlain', '')[:1000])
    print("Lists:", ldata.get('lists'))
except Exception as e:
    print("Lever error or direct HTML...")
    direct_lever = fetch("https://jobs.lever.co/hevodata/6cbbe304-e065-4711-bf3e-756795d2bc2a")
    print("Lever direct snippet:", direct_lever[:1000])

# 3. Wells Fargo
print("\n=== 3. WELLS FARGO ===")
wf_html = fetch("https://www.wellsfargojobs.com/en/jobs/r-570569/software-engineer/")
print("Wells Fargo snippet:", re.sub(r'\s+', ' ', wf_html[:1500]))

# 4. Cargill
print("\n=== 4. CARGILL ===")
cargill_html = fetch("https://careers.cargill.com/en/job/-/-/23251/96288117680")
print("Cargill snippet:", re.sub(r'\s+', ' ', cargill_html[:1500]))

# 5. Caterpillar
print("\n=== 5. CATERPILLAR ===")
cat_html = fetch("https://careers.caterpillar.com/en/jobs/r0000386730/software-engineer-d365-fo/")
print("Caterpillar snippet:", re.sub(r'\s+', ' ', cat_html[:1500]))
