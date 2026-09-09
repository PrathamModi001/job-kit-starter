#!/usr/bin/env python3
"""
Work-at-a-Startup (YC) triage + index.

WaaS is login-gated with no public API, so this script does NOT fetch on its own.
Daily flow:
  1. In the Playwright browser (logged into YC), open the filtered companies URL:
     https://www.workatastartup.com/companies?role=eng&jobType=fulltime&sortBy=created_desc&layout=list-compact
  2. Extract the job cards to output/job-search/waas_jobs.json as a list of:
       {"company","batch","title","location","comp","url"}
     (browser_run_code_unsafe can return this array; write it to the file.)
  3. Run:  python3 waas_scan.py
     -> filters against your bar, drops companies already in applications.csv,
        keeps a seen-index (seen_waas.json), prints only NEW on-criteria roles.

  python3 waas_scan.py --all   # show all on-criteria (ignore seen-index)
"""
import json, os, re, sys, csv

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "output", "job-search")
JOBS = os.path.join(OUT, "waas_jobs.json")       # produced by the Playwright extract
IDX  = os.path.join(OUT, "seen_waas.json")
CSV  = os.path.join(OUT, "applications.csv")
SHOW_ALL = "--all" in sys.argv

# --- bar ---
US_ONLY = re.compile(r"remote \(us|us only|united states only|^us /|, us$|\bNY\b|\bCA\b|\bTX\b|\bSF\b|San Francisco|New York|Los Angeles|Austin|Denver|Seattle|Mountain View", re.I)
INDIA   = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|\bIN\b)\b", re.I)
GLOBAL  = re.compile(r"world\s?wide|globally|anywhere|remote \(.*\bIN\b|/ ?IN ?/|;\s*IN\b|\bAPAC\b|international", re.I)
OVERLVL = re.compile(r"\b(principal|staff|distinguished|chief|officer|\bCTO\b|\bVP\b|head of|director|engineering manager|founding team lead)\b", re.I)
MOBILE  = re.compile(r"\b(ios|android|react native|mobile engineer)\b", re.I)
def parse_k(comp):
    m=re.search(r"\$(\d{2,3})[kK]?\s*[-–]\s*\$?(\d{2,3})[kK]", comp or "")
    if m: return int(m.group(2))            # top of USD-K band
    r=re.search(r"₹\s?(\d+)[Mm]\s*[-–]\s*₹?\s?(\d+)[Mm]", comp or "")
    if r: return int(r.group(2))*10          # ₹XM -> ~X0 LPA
    return None
FLOOR_USD_K = 72   # ~₹60L
FLOOR_LPA   = 60

def eligible(loc):
    if INDIA.search(loc): return "india"
    if "remote" in loc.lower() and GLOBAL.search(loc): return "global"
    if "remote" in loc.lower() and not US_ONLY.search(loc): return "remote?"  # verify
    return None

def load(p, d):
    return json.load(open(p)) if os.path.exists(p) else d

def main():
    if not os.path.exists(JOBS):
        print(f"No {JOBS}. Extract WaaS cards from the logged-in browser first (see header)."); return
    jobs = load(JOBS, [])
    idx  = load(IDX, {"seen_urls": [], "assessed": {}})
    seen = set(idx.get("seen_urls", []))
    applied = set()
    if os.path.exists(CSV):
        for r in csv.DictReader(open(CSV)):
            applied.add((r.get("Company") or "").strip().lower())

    hits, new_urls = [], []
    for j in jobs:
        url = j.get("url",""); co = j.get("company","").strip()
        loc = j.get("location",""); title = j.get("title",""); comp = j.get("comp","")
        is_new = url not in seen
        if is_new: new_urls.append(url)
        elig = eligible(loc)
        if not elig: continue
        if OVERLVL.search(title): continue
        if MOBILE.search(title): continue
        if co.lower() in applied: continue
        pay = parse_k(comp)
        below = (pay is not None) and ((("₹" in (comp or "")) and pay < FLOOR_LPA) or (("$" in (comp or "")) and pay < FLOOR_USD_K))
        rec = {"company":co,"batch":j.get("batch",""),"title":title,"loc":loc,"comp":comp,
               "url":url,"elig":elig,"below_floor":below,"new":is_new}
        idx.setdefault("assessed", {})[url] = {"company":co,"elig":elig}
        hits.append(rec)

    idx["seen_urls"] = sorted(seen | set(new_urls))
    json.dump(idx, open(IDX,"w"), indent=2)

    show = [h for h in hits if (SHOW_ALL or h["new"])]
    show.sort(key=lambda h: (h["below_floor"], h["elig"]!="india" and h["elig"]!="global"))
    print(f"{len(jobs)} WaaS cards · {len(new_urls)} new since last · "
          f"{len(hits)} on-criteria · {sum(h['new'] for h in hits)} of them new\n")
    print("=== NEW on-criteria (India / global-remote) ===\n" if not SHOW_ALL else "=== ALL on-criteria ===\n")
    if not show: print("(none)\n")
    for h in show:
        tag = f"[{h['elig']}]" + ("  ⚠️below-floor" if h["below_floor"] else "") + ("" if h["comp"] else "  (no comp shown)")
        print(f"• {h['company']} ({h['batch']}) — {h['title']}\n    {h['loc']} | {h['comp'] or '—'} {tag}\n    {h['url']}")
    print(f"\nindex -> {IDX} ({len(idx['seen_urls'])} urls tracked)")

if __name__ == "__main__":
    main()
