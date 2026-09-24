import urllib.request, json

ashby_slugs = [
    "sarvam", "composio", "smallest", "vapi", "stack-ai", "julius",
    "langchain", "langfuse", "twenty", "n8n", "svix", "knock",
    "weaviate", "pinecone", "inngest", "warp", "e2b", "zed", "firecrawl"
]

lever_slugs = ["cred", "fampay", "tinybird", "metabase", "gohighlevel"]

gh_slugs = ["postman", "groww", "phonepe", "stripe", "observeai", "togetherai", "doordashindia", "affirm"]

print("=== ASHBY ===")
for slug in ashby_slugs:
    try:
        url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
        jobs = data.get("jobs", [])
        for j in jobs:
            loc = j.get("location", "")
            title = j.get("title", "")
            loc_str = str(loc).lower()
            if any(k in loc_str for k in ["india", "bengaluru", "bangalore", "pune", "mumbai", "hyderabad", "delhi", "gurgaon", "remote"]):
                u = j.get("jobUrl")
                print(f"[{slug}] {title} | {loc} | {u}")
    except Exception as e:
        pass

print("\n=== LEVER ===")
for slug in lever_slugs:
    try:
        url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
        for j in data:
            loc = j.get("categories", {}).get("location", "")
            title = j.get("text", "")
            loc_str = str(loc).lower()
            if any(k in loc_str for k in ["india", "bengaluru", "bangalore", "pune", "mumbai", "hyderabad", "delhi", "gurgaon", "remote"]):
                u = j.get("hostedUrl")
                print(f"[{slug}] {title} | {loc} | {u}")
    except Exception as e:
        pass

print("\n=== GREENHOUSE ===")
for slug in gh_slugs:
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
        for j in data.get("jobs", []):
            loc = j.get("location", {}).get("name", "")
            title = j.get("title", "")
            loc_str = str(loc).lower()
            if any(k in loc_str for k in ["india", "bengaluru", "bangalore", "pune", "mumbai", "hyderabad", "delhi", "gurgaon", "remote"]):
                u = j.get("absolute_url")
                print(f"[{slug}] {title} | {loc} | {u}")
    except Exception as e:
        pass
