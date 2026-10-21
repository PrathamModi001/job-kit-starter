import json, urllib.request, re, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

ashby_slugs = [
    "sarvam", "composio", "smallest", "atlan", "vapi", "e2b", "browserbase", "firecrawl",
    "langchain", "langfuse", "resend", "inngest", "supabase", "deepgram", "replit",
    "modal", "linear", "twenty", "knock", "svix", "writer", "sentry", "ashby",
    "triggerdev", "infisical", "elevenlabs", "n8n", "highlevel", "vanta", "decagon",
    "perplexity", "glean", "cursor", "coda", "pylon", "dust", "bland", "cartesia",
    "tome", "mintlify", "speakeasy", "unstructured", "pinecone", "weaviate", "chroma",
    "together", "anyscale", "runway", "luma", "midjourney", "mistral", "cohere", "harvey",
    "braintrust", "hyperbolic", "cognition", "poolside", "magic",
    "wandb", "scaleai", "voyage", "octoai", "groq",
    "etched", "sambanova", "cerebras", "modular", "lamini", "abacus", "fal", "replicate"
]

LOC_INDIA = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|mumbai|chennai|ahmedabad|remote)\b", re.I)
FOREIGN = re.compile(r"\b(us|usa|united states|canada|uk|united kingdom|poland|germany|france|spain|mexico|singapore|australia|malaysia|ireland|netherlands|romania|sweden|switzerland|remote - us|remote - usa|remote us|remote - canada)\b", re.I)
TITLE_INCLUDE = re.compile(r"\b(software|backend|full[- ]?stack|platform|systems|developer|engineer)\b", re.I)
TITLE_EXCLUDE = re.compile(r"\b(sales|support|escalation|manager|director|intern|lead|senior|sr)\b", re.I)

def check_title_gate(title):
    cmd = ["python", r"job-kit-starter/gates.py", "title", title]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0

def fetch_slug(slug):
    res = []
    try:
        url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=4).read().decode("utf-8"))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", "")
            locs = [loc] + [sl.get("location", "") for sl in j.get("secondaryLocations", [])]
            loc_str = " | ".join(locs)
            if LOC_INDIA.search(loc_str) and not (FOREIGN.search(loc_str) and "india" not in loc_str.lower()):
                if TITLE_INCLUDE.search(title) and not TITLE_EXCLUDE.search(title):
                    if check_title_gate(title):
                        res.append({
                            "company": slug.title(),
                            "title": title,
                            "location": loc_str,
                            "url": j.get("jobUrl", f"https://jobs.ashbyhq.com/{slug}/{j.get('id')}"),
                            "id": j.get("id")
                        })
    except Exception:
        pass
    return res

out = []
with ThreadPoolExecutor(max_workers=30) as pool:
    futures = [pool.submit(fetch_slug, s) for s in set(ashby_slugs)]
    for f in as_completed(futures):
        out.extend(f.result())

print(f"Total Ashby India roles: {len(out)}")
for o in out:
    print(f"- {o['company']} | {o['title']} | {o['location']} | {o['url']}")
