import urllib.request, json

for slug in ["groww", "observeai", "atlan", "zepto"]:
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
        for j in data.get("jobs", []):
            loc = j.get("location", {}).get("name", "")
            title = j.get("title", "")
            u = j.get("absolute_url")
            print(f"[{slug}] {title} | {loc} | {u}")
    except Exception as e:
        print(slug, e)
