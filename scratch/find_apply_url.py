import json, re

with open('E:/Extra/job-kit-starter/scratch/amgen.html', encoding='utf-8') as f:
    html = f.read()

for script in re.findall(r'<script id="([^"]+)"[^>]*>(.*?)</script>', html, re.DOTALL):
    sid, scontent = script
    if sid == '__NEXT_DATA__':
        try:
            d = json.loads(scontent)
            print("Found __NEXT_DATA__")
            s = json.dumps(d)
            for hit in re.findall(r'"(?:url|applyUrl|jobUrl|link|externalUrl|sourceUrl|apply_url)":\s*"([^"]+)"', s):
                print("Hit:", hit)
        except Exception as e:
            print("NEXT_DATA error:", e)
    elif sid == 'job-posting-structured-data':
        try:
            d = json.loads(scontent)
            print("JobPosting structured data:")
            for k, v in d.items():
                if k != 'description':
                    print(f"  {k}: {v}")
                else:
                    print(f"  description len: {len(v)}")
            print("Direct Apply / URL:", d.get('directApply'), d.get('url'), d.get('sameAs'))
        except Exception as e:
            print("job-posting error:", e)
    elif "json" in sid or "data" in sid:
        print("Script id:", sid)

for script in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL):
    try:
        d = json.loads(script)
        if d.get('@type') == 'JobPosting':
            print("JobPosting keys:", d.keys())
            print("title:", d.get('title'))
            print("url:", d.get('url'))
            print("directApply:", d.get('directApply'))
            print("hiringOrganization:", d.get('hiringOrganization'))
    except:
        pass

# Check all links containing workday, greenhouse, lever, smartapply, or apply
matches = re.findall(r'href="([^"]+)"', html)
print("\nInteresting hrefs:")
for m in set(matches):
    if any(k in m.lower() for k in ['myworkday', 'greenhouse', 'lever', 'ashby', 'apply', 'career', 'job']):
        print(" ", m)
