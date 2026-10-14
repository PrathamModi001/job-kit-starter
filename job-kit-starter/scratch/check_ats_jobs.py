import json, urllib.request, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gates

# Load applications.csv to check dedup
seen_co = set()
with open(ROOT / "output" / "job-search" / "applications.csv", encoding="utf-8") as f:
    import csv
    for r in csv.DictReader(f):
        seen_co.add(re.sub(r"[^a-z0-9]", "", r["Company"].lower()))

UA = {"User-Agent": "Mozilla/5.0"}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", "replace")

# Check Ashby boards
ashby_companies = [
    "supabase", "firecrawl", "linear", "modal", "railway", "neon", "render",
    "weaviate", "pinecone", "resend", "inngest", "warp", "e2b", "zed",
    "sarvam", "composio", "vapi", "smallest", "stack-ai", "julius",
    "langchain", "langfuse", "baseten", "fireworksai", "anyscale", "twenty", "n8n", "svix", "knock"
]

candidates = []

for slug in ashby_companies:
    if re.sub(r"[^a-z0-9]", "", slug.lower()) in seen_co:
        continue
    try:
        url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"
        data = json.loads(get(url))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location") or ("Remote" if j.get("isRemote") else "")
            sec = ", ".join(x.get("location", "") for x in (j.get("secondaryLocations") or []) if x.get("location"))
            if sec: loc = f"{loc} ({sec})"
            desc = j.get("descriptionPlain") or ""
            
            # check gates
            if gates.title_skip(title): continue
            reg = gates.region(loc, desc)
            if reg not in ("india", "remote"): continue
            ystat, yev = gates.yoe_check(desc)
            if ystat == "skip": continue
            
            candidates.append({
                "company": slug.capitalize(),
                "title": title,
                "location": loc,
                "url": j.get("jobUrl", ""),
                "channel": "Ashby (Direct ATS)",
                "desc_len": len(desc),
                "desc": desc
            })
    except Exception as e:
        pass

print(f"Found {len(candidates)} Ashby candidates:")
for c in candidates:
    print(c["company"], "|", c["title"], "|", c["location"], "|", c["url"])
