#!/usr/bin/env python3
"""
HN "Who is hiring?" scanner with a persistent index.

- Auto-discovers the latest "Ask HN: Who is hiring?" thread (or pass a thread id as argv[1]).
- Fetches all comments, filters to your criteria (AI/agents + eligible-from-India-or-sponsors + stack),
  excluding companies already in applications.csv.
- Keeps an index at output/job-search/seen_hn.json of every comment id ever seen, so re-runs only
  surface GENUINELY NEW posts. Records a light per-company assessment log too.

Usage:  python3 hn_scan.py            # latest thread, show only NEW on-criteria posts
        python3 hn_scan.py <thread>   # specific thread id
        python3 hn_scan.py --all      # show ALL on-criteria posts (ignore the seen-index)
"""
import json, os, re, sys, html, urllib.request
try:  # Windows consoles default to cp1252 and crash on → / emoji; force UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "output", "job-search")
IDX  = os.path.join(OUT, "seen_hn.json")
CSV  = os.path.join(OUT, "applications.csv")

SHOW_ALL = "--all" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

def clean(t):
    t = html.unescape(t or ""); t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()

# --- applied companies (exclude) ---
seen_co = set()
if os.path.exists(CSV):
    import csv as _csv
    with open(CSV) as f:
        for row in _csv.DictReader(f):
            seen_co.add(row["Company"].strip().lower())

# --- load index ---
idx = {"threads": {}, "comment_ids": [], "assessed": {}}
if os.path.exists(IDX):
    idx = json.load(open(IDX))
known_ids = set(idx.get("comment_ids", []))

# --- find thread ---
if args:
    thread_id = args[0]
else:
    hits = get("https://hn.algolia.com/api/v1/search_by_date?query=%22Ask%20HN%3A%20Who%20is%20hiring%22&tags=story&hitsPerPage=5")["hits"]
    who = [h for h in hits if "who is hiring?" in h["title"].lower() and "freelance" not in h["title"].lower()]
    thread_id = who[0]["objectID"]
    print(f"Thread: {who[0]['title']}  (id {thread_id})")

data = get(f"https://hn.algolia.com/api/v1/items/{thread_id}")
comments = data.get("children", []) or []

# --- filters ---
pos = re.compile(r"\b(remote[\s,)]*(world|glob|any|every)|world\s?wide|anywhere in the world|globally|remote,? ?(?:emea|apac|asia)|\bapac\b|\bindia\b|bengaluru|bangalore|visa|sponsor|relocat)", re.I)
neg = re.compile(r"\b(no visa|not able to (?:offer )?(?:relocat|sponsor)|no sponsor|us only|u\.s\. only|citizens? only|green ?card|onsite only|no remote\b|must already be in)", re.I)
ai  = re.compile(r"\b(agent|agentic|llm|rag|mcp|gen ?ai|generative|ai[- ]native|ai engineer|ml eng|machine learning|inference|foundation model|vector|embedding)", re.I)
stk = re.compile(r"\b(python|typescript|node|react|next\.?js|fastapi|postgres|golang|\bgo\b|full[- ]?stack|backend)", re.I)

def company_of(t):
    return re.split(r"[|(—:]", t)[0].strip()[:42]

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", re.I)
# words that make a matched address a placeholder, not a real inbox
EMAIL_JUNK = re.compile(r"\b(example|test|noreply|no-reply|yourname|foo|domain)\b", re.I)

def emails_of(t):
    found = [m.group(0) for m in EMAIL_RE.finditer(t)]
    return [e for e in dict.fromkeys(found) if not EMAIL_JUNK.search(e)]

new_ids, matches_new, matches_all = [], [], []
for c in comments:
    cid = str(c.get("id") or c.get("objectID") or "")
    if not cid:
        continue
    is_new = cid not in known_ids
    if is_new:
        new_ids.append(cid)
    t = clean(c.get("text", ""))
    if len(t) < 40 or "who is hiring" in t.lower():
        continue
    if not (pos.search(t) and ai.search(t) and stk.search(t)):
        continue
    if neg.search(t):
        continue
    comp = company_of(t)
    if comp.lower() in seen_co:
        continue
    rec = {"id": cid, "company": comp, "text": t[:360], "emails": emails_of(t)}
    matches_all.append(rec)
    if is_new:
        matches_new.append(rec)
    idx.setdefault("assessed", {})[comp] = {"id": cid, "thread": thread_id, "surfaced": True}

# --- report ---
show = matches_all if SHOW_ALL else matches_new
label = "ALL on-criteria" if SHOW_ALL else "NEW (unseen) on-criteria"
print(f"\n{len(comments)} comments · {len(new_ids)} new since last scan · "
      f"{len(matches_all)} on-criteria total · {len(matches_new)} of them new\n")
print(f"=== {label} matches ===\n")
if not show:
    print("(none)\n")
for m in show:
    tag = f"  emails: {', '.join(m['emails'])}" if m["emails"] else "  emails: (none found — use HN profile 'about'/contact link)"
    print(f"### {m['company']}   [hn id {m['id']}]{tag}\n{m['text']} …\n")

# --- persist index ---
idx["comment_ids"] = sorted(known_ids | set(new_ids))
idx["threads"][thread_id] = {"count": len(comments)}
json.dump(idx, open(IDX, "w"), indent=2)
print(f"index updated -> {IDX}  ({len(idx['comment_ids'])} comment ids tracked)")
