#!/usr/bin/env python3
"""
job_hunt.py — on-demand job-match digest for you.

Pulls openings from target companies' ATS boards (Greenhouse / Ashby) + Aiven,
filters to fit (backend / AI-infra roles, mid-level <=4 yrs), scores by stack
match, dedups against seen.json, and writes a markdown digest.

Priority baked in: (1) land a job, (2) comp floor, (3) location — edit to taste
(India + remote ranked first, but nothing dropped purely on location).

Usage:
  python3 job_hunt.py            # show only NEW matches since last run
  python3 job_hunt.py --all      # show all current matches (don't hide seen)
  python3 job_hunt.py --min 4    # only score >= 4
  python3 job_hunt.py --no-save  # don't update seen.json (dry run)

Edit SOURCES below to add/remove companies. No external deps.
"""
import json, re, sys, urllib.request, urllib.error, html, os
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "output", "job-search")
SEEN = os.path.join(OUT, "seen.json")
DIGEST = os.path.join(OUT, "digest.md")

# ---- SOURCES (verified working). type: gh=Greenhouse, ashby=Ashby, aiven=custom ----
SOURCES = [
    # remote-first dev-infra / AI (hire globally / from India for many)
    ("gh", "vercel", "Vercel"), ("gh", "gitlab", "GitLab"),
    ("gh", "cockroachlabs", "Cockroach Labs"), ("gh", "planetscale", "PlanetScale"),
    ("gh", "clickhouse", "ClickHouse"), ("gh", "temporaltechnologies", "Temporal"),
    ("gh", "databricks", "Databricks"), ("gh", "datadog", "Datadog"),
    ("ashby", "supabase", "Supabase"), ("ashby", "firecrawl", "Firecrawl"),
    ("ashby", "linear", "Linear"), ("ashby", "modal", "Modal"),
    ("ashby", "railway", "Railway"), ("ashby", "neon", "Neon"),
    ("ashby", "render", "Render"),
    # India product / fintech (Bucket A)
    ("gh", "postman", "Postman"), ("gh", "groww", "Groww"), ("gh", "phonepe", "PhonePe"),
    ("gh", "stripe", "Stripe"), ("lever", "cred", "CRED"),
    # dev-tool / AI startups — practical, portfolio-friendly interviews
    ("ashby", "weaviate", "Weaviate"), ("ashby", "pinecone", "Pinecone"),
    ("ashby", "resend", "Resend"), ("ashby", "inngest", "Inngest"),
    ("ashby", "warp", "Warp"), ("ashby", "e2b", "E2B"), ("ashby", "zed", "Zed"),
    # AI-native startups (incl. India) — agents / LLM / voice
    ("ashby", "sarvam", "Sarvam"), ("ashby", "composio", "Composio"),
    ("ashby", "vapi", "Vapi"), ("ashby", "smallest", "Smallest.ai"),
    ("ashby", "stack-ai", "Stack.ai"), ("ashby", "julius", "Julius"),
    ("gh", "observeai", "Observe.ai"),
    # AI infra / LLM tooling + more (added round 2)
    ("ashby", "langchain", "LangChain"), ("ashby", "langfuse", "Langfuse"),
    ("ashby", "baseten", "Baseten"), ("ashby", "fireworksai", "Fireworks AI"),
    ("ashby", "anyscale", "Anyscale"), ("ashby", "twenty", "Twenty"),
    ("lever", "tinybird", "Tinybird"), ("lever", "fampay", "Fampay"),
    # round 3 — AI + remote-first + India  (PostHog removed: confirmed no India hiring)
    ("ashby", "n8n", "n8n"),
    ("ashby", "svix", "Svix"), ("ashby", "knock", "Knock"),
    ("ashby", "writer", "Writer"), ("ashby", "deepgram", "Deepgram"),
    ("ashby", "atlan", "Atlan"), ("gh", "devrev", "DevRev"),
    ("lever", "zeta", "Zeta"),
    # round 4 — PostHog-like: remote-first / hire-anywhere / OSS
    ("gh", "mattermost", "Mattermost"), ("gh", "tailscale", "Tailscale"),
    ("ashby", "sentry", "Sentry"), ("ashby", "replit", "Replit"),
    ("ashby", "browserbase", "Browserbase"),
    # round 5 — from PostHog "Cool Tech Jobs" board (India / remote-global verified)
    ("ashby", "zapier", "Zapier"), ("ashby", "revenuecat", "RevenueCat"),
    # round 6 — bulk-verified live boards with India/remote roles (slugs checked against the API).
    # The region filter tags/penalizes US-only roles, so big US employers stay sortable, not noise.
    ("gh", "samsara", "Samsara"), ("gh", "twilio", "Twilio"),
    ("gh", "affirm", "Affirm"), ("gh", "instacart", "Instacart"),
    ("gh", "coinbase", "Coinbase"), ("gh", "grafanalabs", "Grafana Labs"),
    ("gh", "reddit", "Reddit"), ("gh", "pinterest", "Pinterest"),
    ("gh", "dropbox", "Dropbox"), ("gh", "mongodb", "MongoDB"),
    ("gh", "airbnb", "Airbnb"), ("gh", "anthropic", "Anthropic"),
    ("gh", "airtable", "Airtable"), ("gh", "webflow", "Webflow"),
    ("gh", "gusto", "Gusto"), ("gh", "elastic", "Elastic"),
    ("gh", "discord", "Discord"), ("gh", "asana", "Asana"),
    ("gh", "scaleai", "Scale AI"), ("gh", "figma", "Figma"),
    ("gh", "netlify", "Netlify"),
    ("ashby", "vanta", "Vanta"), ("ashby", "sierra", "Sierra"),
    ("ashby", "decagon", "Decagon"), ("ashby", "elevenlabs", "ElevenLabs"),
    ("lever", "gohighlevel", "HighLevel"),
    # round 7 — small remote-first startups (get-noticed-in-a-week list), verified live + India/remote
    ("ashby", "1password", "1Password"), ("ashby", "ashby", "Ashby"),
    ("lever", "metabase", "Metabase"), ("ashby", "livekit", "LiveKit"),
    ("ashby", "triggerdev", "Trigger.dev"), ("ashby", "infisical", "Infisical"),
    # relocation bonus
    ("aiven", "aiven", "Aiven"),
    # aggregators (breadth) — Arbeitnow dropped: almost all EU on-site, region/work-auth gated
    ("hn", "", "HN Who's Hiring"),
]

ROLE_INCLUDE = re.compile(
    r"\b(full[- ]?stack|software eng|software developer|application developer|"
    r"back[- ]?end|front[- ]?end|web developer|product eng|services eng|api eng|"
    r"ml engineer|machine learning|ai engineer|applied ai|deep learning|"
    r"computer vision|nlp engineer|data scien|"
    r"platform|distributed|systems eng|developer experience|\.net|dotnet|c#|"
    r"associate software|graduate engineer|junior (?:software|developer|engineer)|trainee)\b", re.I)
ROLE_EXCLUDE = re.compile(
    r"\b(manager|director|head|vp|president|principal|\bstaff\b|sales|account|"
    r"marketing|recruit|talent|people ops|legal|finance|content|writer|"
    r"evangelist|advocate|designer|design eng|intern|analyst|support|success|"
    r"solutions eng|field|security|data scien|ml research|research scien|"
    r"hardware|firmware|mobile|android|ios|qa\b|test eng)\b", re.I)

STACK = ["full stack", "full-stack", "react", "node", "typescript", "javascript",
         "angular", "python", "rest api", "sql", "web developer",
         "machine learning", "ml", "tensorflow", "pytorch", "computer vision",
         "nlp", "deep learning", "llm", "genai", "rag", "agent", "data scien",
         ".net", "dotnet", "c#", "asp.net", "web api", "azure", "microservice",
         "postgres", "mongodb", "docker", "microservices"]
LOC_INDIA  = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|noida|delhi|mumbai|chennai|apac)\b", re.I)
LOC_REMOTE = re.compile(r"\b(remote|anywhere|worldwide|distributed|work from home)\b", re.I)
# strong "remote with no borders" signal
LOC_GLOBAL = re.compile(r"\b(anywhere|worldwide|global(ly)?|any country|any location|fully remote|remote[- ]?first)\b", re.I)
# a specific US/EU/Canada place or region named in the LOCATION field => region-locked (not India-eligible)
LOC_LOCKED = re.compile(
    r"\b(united states|u\.?s\.?a?|usa|america|canada|canadian|united kingdom|\bu\.?k\.?\b|england|ireland|"
    r"germany|france|netherlands|spain|poland|portugal|sweden|switzerland|"
    r"berlin|munich|cologne|köln|london|dublin|amsterdam|paris|lisbon|madrid|warsaw|"
    r"new york|san francisco|seattle|austin|boston|chicago|denver|toronto|vancouver|"
    r"emea|namer|latam|est timezone|pst|pt timezone|eastern time|pacific time)\b", re.I)

def region(loc, desc=""):
    """india | remote | locked | unknown — used for scoring + the --india filter + the tag."""
    loc = loc or ""
    if LOC_INDIA.search(loc) or LOC_INDIA.search(desc[:400]): return "india"
    if LOC_GLOBAL.search(loc): return "remote"
    if LOC_LOCKED.search(loc): return "locked"
    if LOC_REMOTE.search(loc): return "remote"
    return "unknown"
YEARS = re.compile(r"(\d{1,2})\s*\+?\s*years", re.I)
MAX_YEARS = 4  # he's ~3; allow up to 4+, drop 5+

UA = {"User-Agent": "Mozilla/5.0 (job_hunt)"}

def get(url, timeout=12):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def strip_html(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()

def fetch_gh(slug):
    data = json.loads(get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"))
    for j in data.get("jobs", []):
        yield {"title": j.get("title", ""),
               "loc": (j.get("location") or {}).get("name", ""),
               "url": j.get("absolute_url", ""),
               "desc": strip_html(j.get("content", "")),
               "id": str(j.get("id"))}

def fetch_ashby(slug):
    data = json.loads(get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"))
    for j in data.get("jobs", []):
        loc = j.get("location") or ("Remote" if j.get("isRemote") else "")
        # include secondary locations: many roles list "US & Canada" primary but India
        # (or other regions) as eligible secondaries — without this they get mis-tagged locked.
        sec = ", ".join(x.get("location", "") for x in (j.get("secondaryLocations") or []) if x.get("location"))
        if sec:
            loc = f"{loc} ({sec})"
        yield {"title": j.get("title", ""), "loc": loc,
               "url": j.get("jobUrl", ""), "desc": j.get("descriptionPlain", "") or "",
               "id": j.get("id") or j.get("jobUrl", "")}

def fetch_lever(slug):
    data = json.loads(get(f"https://api.lever.co/v0/postings/{slug}?mode=json"))
    for j in data:
        cat = j.get("categories") or {}
        loc = cat.get("location", "") or ""
        # include allLocations: a role can list India among allLocations while the
        # primary `location` shows another city (same class of bug as Ashby secondaries).
        allloc = ", ".join(cat.get("allLocations") or [])
        if allloc and allloc != loc:
            loc = f"{loc} ({allloc})"
        if (cat.get("commitment") or "").lower() == "remote" or (j.get("workplaceType") or "") == "remote":
            loc = (loc + " / Remote").strip(" /")
        yield {"title": j.get("text", ""), "loc": loc, "url": j.get("hostedUrl", ""),
               "desc": j.get("descriptionPlain") or strip_html(j.get("description", "")),
               "id": j.get("id", "")}

def fetch_aiven(_):
    h = get("https://aiven.io/careers/job")
    for href, inner in re.findall(r'<a[^>]*href="(/careers/job/\d+)"[^>]*>(.*?)</a>', h, re.S):
        txt = strip_html(inner)
        if txt:
            yield {"title": txt, "loc": txt, "url": "https://aiven.io" + href, "desc": "", "id": href}

def fetch_hn(_):
    # newest "Ask HN: Who is hiring?" thread, then its top-level comments (job posts)
    s = json.loads(get("https://hn.algolia.com/api/v1/search_by_date?"
                       "tags=story,author_whoishiring&query=who%20is%20hiring&hitsPerPage=4"))
    story = next((h for h in s.get("hits", [])
                  if "who is hiring" in (h.get("title") or "").lower()), None)
    if not story:
        return
    item = json.loads(get(f"https://hn.algolia.com/api/v1/items/{story['objectID']}"))
    for c in (item.get("children") or []):
        text = strip_html(c.get("text") or "")
        if not text or not ROLE_INCLUDE.search(text):
            continue
        if not (LOC_REMOTE.search(text) or LOC_INDIA.search(text)):
            continue  # only remote/India posts from HN
        company = re.split(r"[|–\-\n(]", text, maxsplit=1)[0].strip()[:40] or "HN"
        yield {"title": text[:120], "company": company, "loc": text[:200],
               "url": f"https://news.ycombinator.com/item?id={c.get('id')}",
               "desc": text, "id": str(c.get("id")), "prefiltered": True}

def fetch_arbeitnow(_):
    for page in range(1, 4):
        try:
            d = json.loads(get(f"https://www.arbeitnow.com/api/job-board-api?page={page}"))
        except Exception:
            break
        for j in d.get("data", []):
            loc = j.get("location") or ""
            if j.get("remote"):
                loc = (loc + " / Remote").strip(" /")
            yield {"title": j.get("title", ""), "company": j.get("company_name", "Arbeitnow"),
                   "loc": loc, "url": j.get("url", ""),
                   "desc": strip_html(j.get("description", "")), "id": j.get("slug") or j.get("url", "")}

FETCH = {"gh": fetch_gh, "ashby": fetch_ashby, "aiven": fetch_aiven,
         "lever": fetch_lever, "hn": fetch_hn, "arbeitnow": fetch_arbeitnow}

def min_years(desc):
    ys = [int(x) for x in YEARS.findall(desc)]
    return min(ys) if ys else None

def score(title, desc, loc):
    blob = (title + " " + desc).lower()
    s = sum(2 for k in STACK if k in blob)
    if re.search(r"\b(back[- ]?end|platform|infra)", title, re.I): s += 3
    if any(k in blob for k in ("llm", "ai infra", "genai", "rag", "agent")): s += 3
    s += {"india": 4, "remote": 3, "locked": -6, "unknown": 0}[region(loc, desc)]
    return s

def loc_tag(loc, desc=""):
    r = region(loc, desc)
    if r == "india":  return "🇮🇳 India"
    if r == "remote": return "🌍 Remote"
    if r == "locked": return "🔒 " + ((loc or "")[:28] or "region-locked")
    return (loc or "")[:40] or "—"

def main():
    args = sys.argv[1:]
    show_all = "--all" in args
    save = "--no-save" not in args
    india_only = "--india" in args  # drop region-locked (US/EU/Canada-only) roles
    min_s = 0
    if "--min" in args:
        try: min_s = int(args[args.index("--min") + 1])
        except Exception: pass

    os.makedirs(OUT, exist_ok=True)
    seen = set()
    if os.path.exists(SEEN):
        try: seen = set(json.load(open(SEEN)))
        except Exception: seen = set()

    matches, errors, stats = [], [], {}

    # Phase 1: fetch every source concurrently, with a hard per-source timeout so
    # one slow/hung endpoint can never stall the whole run.
    def collect(typ, slug):
        return list(FETCH[typ](slug))
    fetched = {}
    ex = ThreadPoolExecutor(max_workers=12)
    futs = {ex.submit(collect, typ, slug): label for typ, slug, label in SOURCES}
    for fut, label in futs.items():
        try:
            fetched[label] = fut.result(timeout=25)
        except FutureTimeout:
            errors.append(f"{label}: timeout"); fetched[label] = []
        except Exception as e:
            errors.append(f"{label}: {type(e).__name__}"); fetched[label] = []
    ex.shutdown(wait=False)

    # Phase 2: filter + score (fast, in-memory).
    for typ, slug, label in SOURCES:
        n = 0
        for job in fetched.get(label, []):
            t = job["title"]
            if ROLE_EXCLUDE.search(t):
                continue
            if not job.get("prefiltered") and not ROLE_INCLUDE.search(t):
                continue
            my = min_years(job["desc"])
            if my is not None and my > MAX_YEARS:
                continue
            reg = region(job["loc"], job["desc"])
            if india_only and reg == "locked":
                continue
            sc = score(t, job["desc"], job["loc"])
            if sc < min_s:
                continue
            comp = job.get("company") or label
            key = f"{comp}:{job['id']}"
            matches.append({"company": comp, "title": t, "loc": job["loc"],
                            "url": job["url"], "score": sc, "years": my,
                            "region": reg, "key": key, "new": key not in seen})
            n += 1
        stats[label] = n

    matches.sort(key=lambda m: (m["new"], m["score"]), reverse=True)
    shown = matches if show_all else [m for m in matches if m["new"]]
    new_count = sum(1 for m in matches if m["new"])

    def tag_for(m):
        r = m.get("region", "unknown")
        if r == "india":  return "🇮🇳 India"
        if r == "remote": return "🌍 Remote"
        if r == "locked": return "🔒 " + ((m["loc"] or "")[:28] or "region-locked")
        return (m["loc"] or "")[:40] or "—"

    rc = {k: sum(1 for m in matches if m.get("region") == k)
          for k in ("india", "remote", "locked", "unknown")}
    ts = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    lines = [f"# Job digest — {ts}", "",
             f"Scanned {len(SOURCES)} sources · {len(matches)} matches total · "
             f"**{new_count} new** · showing {'all' if show_all else 'new only'} "
             f"(min score {min_s}{', India-eligible only' if india_only else ''}).",
             f"Region: 🇮🇳 {rc['india']} India · 🌍 {rc['remote']} remote · "
             f"🔒 {rc['locked']} region-locked · {rc['unknown']} unknown.", ""]
    if errors:
        lines.append("> source errors: " + ", ".join(errors) + "\n")
    if not shown:
        lines.append("_No new matches this run. Try `--all` to see everything._")
    else:
        lines.append("| ★ | Score | Role | Company | Location | Yrs req |")
        lines.append("|---|------:|------|---------|----------|--------|")
        for m in shown:
            star = "🆕" if m["new"] else ""
            yrs = f"{m['years']}+" if m["years"] else "—"
            title = f"[{m['title']}]({m['url']})"
            lines.append(f"| {star} | {m['score']} | {title} | {m['company']} | "
                         f"{tag_for(m)} | {yrs} |")
    lines += ["", "---", "Sources scanned: " +
              ", ".join(f"{k}({v})" for k, v in sorted(stats.items()))]
    open(DIGEST, "w", encoding="utf-8").write("\n".join(lines))

    if save:
        json.dump(sorted(seen | {m["key"] for m in matches}), open(SEEN, "w"), indent=0)

    print(f"{len(matches)} matches ({new_count} new) -> {DIGEST}")
    if errors: print("errors:", ", ".join(errors))
    # digest + seen.json are written; exit now instead of waiting on any straggler
    # fetch threads that timed out (avoids a multi-minute lingering shutdown).
    sys.stdout.flush()
    os._exit(0)

if __name__ == "__main__":
    main()
