import json
import urllib.request
import re
import csv
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

apps_csv = Path(r"job-kit-starter/output/job-search/applications.csv")
applied_cos = set()
with apps_csv.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("Company"):
            applied_cos.add(row["Company"].strip().lower())

LOC_INDIA = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|mumbai|chennai|ahmedabad|remote)\b", re.I)
FOREIGN = re.compile(r"\b(us|usa|united states|canada|uk|united kingdom|poland|germany|france|spain|mexico|singapore|australia|malaysia|ireland|netherlands|romania|sweden|switzerland|remote - us|remote - usa|remote us|remote - canada)\b", re.I)
TITLE_INCLUDE = re.compile(r"\b(software|backend|full[- ]?stack|platform|systems|developer|engineer)\b", re.I)
TITLE_EXCLUDE = re.compile(r"\b(sales|support|escalation|manager|director|intern|lead|senior|sr|staff|principal|architect|sde[- ]?[23ii]|sde\s*[23]|pe\s*2|product engineer\s*(?:2|ii)|mts|member of technical staff|mobile|react[- ]native|forward deployed)\b", re.I)

ashby_slugs = [
    "sarvam", "composio", "smallest", "atlan", "vapi", "e2b", "browserbase", "firecrawl",
    "langchain", "langfuse", "resend", "inngest", "supabase", "deepgram", "replit",
    "modal", "linear", "twenty", "knock", "svix", "writer", "sentry", "ashby",
    "triggerdev", "infisical", "elevenlabs", "n8n", "highlevel", "vanta", "decagon",
    "perplexity", "glean", "cursor", "coda", "pylon", "dust", "bland", "cartesia",
    "tome", "mintlify", "speakeasy", "unstructured", "pinecone", "weaviate", "chroma",
    "together", "anyscale", "runway", "luma", "midjourney", "mistral", "cohere", "harvey",
    "braintrust", "hyperbolic", "cognition", "poolside", "magic", "cerebras",
    "wandb", "scaleai", "voyage", "octoai", "groq", "etched", "sambanova", "cerebras",
    "modular", "lamini", "abacus", "fal", "replicate", "valtown", "openpipe", "outerbounds"
]

def check_title(title):
    cmd = ["python", r"job-kit-starter/gates.py", "title", title]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return res.returncode == 0

def clean_jd(html):
    cmd = ["python", r"job-kit-starter/gates.py", "clean"]
    res = subprocess.run(cmd, input=html, capture_output=True, text=True, encoding="utf-8")
    return res.stdout.strip()

def check_yoe(text):
    temp = Path("scratch/temp_jd_ashby.txt")
    temp.write_text(text, encoding="utf-8")
    cmd = ["python", r"job-kit-starter/gates.py", "yoe", str(temp)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return res.returncode == 0, res.stdout.strip()

results = []

def check_ashby(slug):
    if slug.lower() in applied_cos:
        return []
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    out = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
        for j in data.get("jobs", []):
            title = j.get("title", "")
            loc = j.get("location", "")
            locs = [loc] + [sl.get("location", "") for sl in j.get("secondaryLocations", [])]
            loc_str = " | ".join(locs)
            if LOC_INDIA.search(loc_str) and not (FOREIGN.search(loc_str) and "india" not in loc_str.lower()):
                if TITLE_INCLUDE.search(title) and not TITLE_EXCLUDE.search(title):
                    if check_title(title):
                        jd_clean = clean_jd(j.get("descriptionHtml", ""))
                        if len(jd_clean) >= 1500:
                            yoe_ok, yoe_msg = check_yoe(jd_clean)
                            if yoe_ok:
                                out.append({
                                    "company": slug.title(),
                                    "title": title,
                                    "location": loc_str,
                                    "url": j.get("jobUrl", f"https://jobs.ashbyhq.com/{slug}/{j.get('id')}"),
                                    "id": str(j.get("id")),
                                    "yoe": yoe_msg,
                                    "jd": jd_clean
                                })
    except Exception:
        pass
    return out

with ThreadPoolExecutor(max_workers=30) as pool:
    futures = [pool.submit(check_ashby, s) for s in set(ashby_slugs)]
    for f in as_completed(futures):
        results.extend(f.result())

print(f"Total matching Ashby roles with YOE OK: {len(results)}")
for r in results:
    print(f"- [{r['company']}] {r['title']} ({r['location']}) | YOE: {r['yoe']} | URL: {r['url']}")

with open("scratch/junior_ashby_roles.json", "w", encoding="utf-8") as f:
    meta = [{k: v for k, v in r.items() if k != "jd"} for r in results]
    json.dump(meta, f, indent=2)
