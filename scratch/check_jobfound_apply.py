import urllib.request, re, json

url = "https://jobfound.org/job/sia-is-hiring-for-forward-deployed-engineer-kurla-maharashtra-india-28-september-2026"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")

# Let's search for "http" or "apply" or next-data
m = re.findall(r'"applyUrl":\s*"([^"]+)"', html)
print("applyUrl in json:", m)

m2 = re.findall(r'href="([^"]+)"[^>]*>.*?[aA]pply', html)
print("href with apply:", m2)

# Look for __NEXT_DATA__
next_data = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
if next_data:
    data = json.loads(next_data.group(1))
    print("Found NEXT_DATA!")
    # dump keys or search for urls
    s = json.dumps(data)
    urls = re.findall(r'https?://[^\s",\\]+', s)
    ats = [u for u in urls if any(k in u for k in ["greenhouse", "lever", "workday", "ashby", "smartrecruiters", "oracle", "successfactors", "careers", "jobs", "apply"])]
    print("ATS from NEXT_DATA:", list(dict.fromkeys(ats))[:5])
else:
    print("No NEXT_DATA")
