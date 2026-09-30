import urllib.request, json

boards = [
    ("cursor", "https://api.ashbyhq.com/posting-api/job-board/cursor"),
    ("perplexity", "https://api.ashbyhq.com/posting-api/job-board/perplexity"),
    ("elevenlabs", "https://api.ashbyhq.com/posting-api/job-board/elevenlabs"),
    ("cohere", "https://api.ashbyhq.com/posting-api/job-board/cohere"),
    ("glean", "https://api.ashbyhq.com/posting-api/job-board/glean"),
    ("anthropic", "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs"),
    ("groq", "https://boards-api.greenhouse.io/v1/boards/groq/jobs"),
    ("postman", "https://boards-api.greenhouse.io/v1/boards/postman/jobs"),
    ("browserbase", "https://api.ashbyhq.com/posting-api/job-board/browserbase"),
    ("resend", "https://api.ashbyhq.com/posting-api/job-board/resend"),
    ("unify", "https://api.ashbyhq.com/posting-api/job-board/unify"),
    ("anyscale", "https://api.ashbyhq.com/posting-api/job-board/anyscale"),
    ("baseten", "https://api.ashbyhq.com/posting-api/job-board/baseten"),
    ("togetherai", "https://boards-api.greenhouse.io/v1/boards/togetherai/jobs"),
    ("scaleai", "https://boards-api.greenhouse.io/v1/boards/scaleai/jobs"),
    ("coherehealth", "https://boards-api.greenhouse.io/v1/boards/coherehealth/jobs"),
    ("samsara", "https://boards-api.greenhouse.io/v1/boards/samsara/jobs"),
    ("affirm", "https://boards-api.greenhouse.io/v1/boards/affirm/jobs"),
    ("rubrik", "https://boards-api.greenhouse.io/v1/boards/rubrik/jobs"),
    ("appliedintuition", "https://boards-api.greenhouse.io/v1/boards/appliedintuition/jobs")
]

for name, url in boards:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read().decode("utf-8"))
        jobs = data.get("jobs", []) or data.get("jobPostings", [])
        if isinstance(data, list): jobs = data
        for j in jobs:
            title = j.get("title", "")
            loc = ""
            if "locationName" in j:
                loc = j["locationName"]
            elif isinstance(j.get("location"), dict):
                loc = j["location"].get("name", "")
            else:
                loc = str(j.get("location", ""))
                
            t_low = title.lower()
            l_low = loc.lower()
            u = j.get("jobUrl") or j.get("absolute_url")
            if any(k in l_low for k in ["india", "bengaluru", "bangalore", "hyderabad", "remote"]):
                if any(k in t_low for k in ["software", "backend", "full stack", "engineer", "developer", "platform"]):
                    print(f"[{name}] {title} | {loc} -> {u}")
    except Exception as e:
        pass
