import urllib.request, json

gh_all = [
    "vercel", "gitlab", "cockroachlabs", "planetscale", "clickhouse",
    "temporaltechnologies", "databricks", "datadog", "stripe",
    "postman", "groww", "phonepe", "observeai", "togetherai",
    "affirm", "sentry", "twilio", "reddit", "elastic", "asana"
]

for slug in gh_all:
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
        for j in data.get("jobs", []):
            loc = j.get("location", {}).get("name", "")
            title = j.get("title", "")
            loc_str = str(loc).lower()
            if any(k in loc_str for k in ["india", "bengaluru", "bangalore", "pune", "mumbai", "hyderabad"]):
                u = j.get("absolute_url")
                print(f"[{slug}] {title} | {loc} | {u}")
    except Exception as e:
        pass
