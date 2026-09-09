#!/usr/bin/env python3
"""
India-aggregator job scan (complements job_hunt.py, which only hits company ATS boards).
Scrapes Indeed-India + LinkedIn-India via JobSpy, scores by your stack, dedupes against
already-applied companies (applications.csv) and prior runs (seen_india.json), writes a digest.

Naukri / Glassdoor / Google block scrapers from this environment, so they're skipped.
"""
import json, os, re, warnings, sys
from datetime import datetime, timezone
import pandas as pd
from jobspy import scrape_jobs

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "output", "job-search")
SEEN_PATH = os.path.join(OUT, "seen_india.json")
CSV_PATH = os.path.join(OUT, "applications.csv")

HOURS_OLD = int(sys.argv[1]) if len(sys.argv) > 1 else 168  # default last 7 days
RESULTS = 30

# (site, search_term, is_remote, location)
# Tuned for Anjali: FULL-STACK / SOFTWARE DEVELOPER / AI-ML first (NOT ".NET developer").
# .NET/C#/React are tools she brings; the search targets broad full-stack + SDE + AI/ML, fresher/entry, Bengaluru+India.
QUERIES = [
    ("indeed",   "full stack developer",          False, "Bengaluru, India"),
    ("indeed",   "software developer",            False, "Bengaluru, India"),
    ("indeed",   "software engineer fresher",     False, "Bengaluru, India"),
    ("indeed",   "full stack developer react",    False, "India"),
    ("indeed",   "ai ml engineer",                False, "India"),
    ("indeed",   "machine learning engineer",     False, "India"),
    ("indeed",   "software developer",            True,  "India"),   # remote-biased
    ("linkedin", "full stack developer",          False, "India"),
    ("linkedin", "software engineer fresher",     False, "India"),
    ("linkedin", "associate software engineer",   False, "India"),
    ("linkedin", "ai ml engineer",                False, "India"),
    ("linkedin", "full stack developer remote",   True,  "India"),
]

# --- scoring keywords ---
POS = {
    # primary lanes: full-stack / general software / AI-ML
    "full stack": 5, "fullstack": 5, "full-stack": 5,
    "software engineer": 4, "software developer": 4, "software development": 3,
    "ai": 3, " ai/ml": 4, "ai/ml": 4, "ml engineer": 4, "machine learning": 4, "deep learning": 3,
    "computer vision": 3, "nlp": 3, "genai": 3, "generative ai": 3, "llm": 3, "data scien": 2,
    "react": 4, "node": 3, "nodejs": 3, "javascript": 3, "typescript": 3, "angular": 3,
    "python": 3, "tensorflow": 3, "pytorch": 3, "rest": 2, "api": 2, "backend": 2, "frontend": 2,
    # supporting skills she has (positive but NOT the driver)
    ".net": 2, "dotnet": 2, "c#": 2, "asp.net": 2, "web api": 2, "ef core": 1, "sql server": 1,
    "sql": 1, "azure": 2, "microservice": 2, "microservices": 2, "mongodb": 1, "postgres": 1,
    # level fit
    "fresher": 3, "entry level": 3, "graduate engineer": 3, "trainee": 2, "associate": 2, "junior": 2,
    "0-1 year": 3, "0-2 year": 3, "0 to 2 year": 3,
}
NEG = {
    "qa ": -5, "test engineer": -5, "manual test": -7, "sdet": -3,
    "salesforce": -6, "sap ": -6, "sap-": -6,
    "sales ": -5, "wordpress": -6, "php": -3, "intern ": -3, "internship": -3,
    "manager": -3, "principal": -3, "staff engineer": -2, "architect": -2,
    "10+ years": -6, "12+ years": -7, "8+ years": -4, "7+ years": -3, "6+ years": -2,
    "5+ years": -1, "android developer": -1, "ios developer": -1,
}

def already_applied_companies():
    names = set()
    try:
        with open(CSV_PATH) as f:
            for line in f.readlines()[1:]:
                c = line.split(",")[0].strip().lower()
                if c:
                    names.add(c)
    except FileNotFoundError:
        pass
    return names

def load_seen():
    try:
        return set(json.load(open(SEEN_PATH)))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def score(row):
    hay = " ".join(str(row.get(k, "")) for k in ("title", "company", "description")).lower()
    hay = " " + re.sub(r"[^a-z0-9+.# ]", " ", hay) + " "
    s = 0
    for k, v in POS.items():
        if k in hay:
            s += v
    for k, v in NEG.items():
        if k in hay:
            s += v
    if row.get("is_remote") is True:
        s += 4
    # seniority sweet-spot for a fresher: reward 0-2 yrs / entry level, penalize high-YOE gates
    if re.search(r"\b0\s*(?:-|to)?\s*[12]?\s*year|\bentry[- ]level|\bfresher|\bgraduate\b", hay):
        s += 3
    elif re.search(r"\b[12]\s*(?:-|to)?\s*[23]?\s*year", hay):
        s += 1
    if re.search(r"\b([7-9]|1\d)\+?\s*year", hay):  # 7+ years = too senior
        s -= 3
    return s

def main():
    applied = already_applied_companies()
    seen = load_seen()
    frames = []
    log = []
    for site, term, remote, loc in QUERIES:
        try:
            kw = dict(site_name=[site], search_term=term, location=loc,
                      results_wanted=RESULTS, hours_old=HOURS_OLD, verbose=0)
            if site == "indeed":
                kw["country_indeed"] = "India"
            if remote:
                kw["is_remote"] = True
            df = scrape_jobs(**kw)
            n = 0 if df is None else len(df)
            log.append(f"{site} · '{term}'{' · remote' if remote else ''} → {n}")
            if n:
                frames.append(df)
        except Exception as e:
            log.append(f"{site} · '{term}' → FAIL ({type(e).__name__})")

    if not frames:
        print("No results from any source.")
        return

    df = pd.concat(frames, ignore_index=True)
    # dedupe
    df["_key"] = (df.get("title", "").astype(str).str.lower().str.strip() + "|" +
                  df.get("company", "").astype(str).str.lower().str.strip())
    df = df.drop_duplicates("_key").drop_duplicates("job_url")
    df["_score"] = df.apply(score, axis=1)

    # comp string
    def comp(r):
        lo, hi, cur = r.get("min_amount"), r.get("max_amount"), r.get("currency") or ""
        if pd.notna(lo) or pd.notna(hi):
            lo = f"{int(lo):,}" if pd.notna(lo) else "?"
            hi = f"{int(hi):,}" if pd.notna(hi) else "?"
            return f"{cur} {lo}-{hi}".strip()
        return ""

    df["_comp"] = df.apply(comp, axis=1)
    df["_applied"] = df["company"].astype(str).str.lower().str.strip().isin(applied)
    df["_new"] = ~df["job_url"].isin(seen)

    df = df[df["_score"] >= 4].sort_values("_score", ascending=False)

    rows_new = df[df["_new"]]
    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    lines = [f"# India-aggregator digest — {stamp}",
             "",
             f"Indeed-India + LinkedIn-India · last {HOURS_OLD}h · score >= 4 · "
             f"{len(df)} relevant ({len(rows_new)} new).  _Naukri/Glassdoor/Google block scrapers, skipped._",
             "",
             "| Score | Role | Company | Location | Remote | Comp | Link | Note |",
             "|------:|------|---------|----------|:------:|------|------|------|"]
    for _, r in df.head(45).iterrows():
        note = "🆕 new" if r["_new"] else "seen"
        if r["_applied"]:
            note = "⚠️ already applied"
        rem = "🌍" if r.get("is_remote") is True else ""
        title = str(r.get("title", ""))[:70].replace("|", "/")
        comp_c = str(r.get("company", ""))[:28].replace("|", "/")
        locn = str(r.get("location", ""))[:24].replace("|", "/")
        url = r.get("job_url", "")
        lines.append(f"| {int(r['_score'])} | {title} | {comp_c} | {locn} | {rem} | "
                     f"{r['_comp']} | [link]({url}) | {note} |")

    with open(os.path.join(OUT, "digest_india.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # update seen
    json.dump(sorted(set(seen) | set(df["job_url"].dropna())), open(SEEN_PATH, "w"), indent=0)

    print("SCRAPE LOG:")
    for l in log:
        print("  " + l)
    print(f"\n{len(df)} relevant roles ({len(rows_new)} new) -> output/job-search/digest_india.md")

if __name__ == "__main__":
    main()
