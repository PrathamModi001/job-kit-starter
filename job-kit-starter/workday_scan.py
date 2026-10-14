#!/usr/bin/env python3
"""India jobs from companies' public Workday career sites (no login, no scraping): big India hirers like Mastercard,
Adobe, Cadence, KLA, Micron, Intel, Cisco, Salesforce. Searches each tenant, keeps India roles, fetches the real JD,
and runs the same gates.py rules the apply step uses (title / location / yoe / lane / fit / dedup).
  python workday_scan.py [--min-fit 11] [--days 30]      -> output/job-search/digest_workday.md
Add tenants: (tenant, wdN host, site) from the company's careers URL  https://<tenant>.<wdN>.myworkdayjobs.com/<site>
NOTE: Workday application forms usually need an account + email OTP; expect many to end Blocked at the apply step."""
import json, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
from gates import MIN_FIT, dedup, fit_score, location_check, strip_html, title_skip, yoe_check

OUT = Path(__file__).resolve().parent / "output" / "job-search"
TENANTS = [("mastercard", "wd1", "CorporateCareers"), ("target", "wd5", "targetcareers"), ("kla", "wd1", "Search"),
           ("db", "wd3", "DBWebsite"), ("adobe", "wd5", "external_experienced"), ("micron", "wd1", "External"),
           ("cadence", "wd1", "External_Careers"), ("intel", "wd1", "External"), ("hp", "wd5", "ExternalCareerSite"),
           ("autodesk", "wd1", "Ext"), ("cisco", "wd5", "Cisco_Careers"), ("salesforce", "wd12", "External_Career_Site"),
           ("workday", "wd5", "Workday"), ("pwc", "wd3", "Global_Experienced_Careers"), ("nvidia", "wd5", "NVIDIAExternalCareerSite"),
           ("redhat", "wd5", "Jobs"), ("paypal", "wd1", "jobs"), ("mckesson", "wd3", "External_Careers"),
           ("maersk", "wd3", "Maersk_Careers"), ("blackrock", "wd1", "BlackRock_Professional"), ("thomsonreuters", "wd5", "External_Career_Site")]
QUERIES = ["software engineer", "backend developer", "full stack developer", "software developer", "node.js", "python developer"]
INDIA = re.compile(r"india|bengaluru|bangalore|pune|hyderabad|mumbai|gurgaon|gurugram|chennai|noida|ahmedabad|delhi", re.I)
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}


def call(url, body=None):
    req = urllib.request.Request(url, json.dumps(body).encode() if body else None, H)
    return json.load(urllib.request.urlopen(req, timeout=20))


def search(t):
    ten, host, site = t
    base = f"https://{ten}.{host}.myworkdayjobs.com"
    seen, out = set(), []
    for q in QUERIES:
        for off in range(0, 60, 20):  # 3 pages of 20 per query
            try:
                d = call(f"{base}/wday/cxs/{ten}/{site}/jobs", {"appliedFacets": {}, "limit": 20, "offset": off, "searchText": q + " india"})
            except Exception:
                break
            for j in d.get("jobPostings", []):
                p = j.get("externalPath")
                if p and p not in seen and INDIA.search(j.get("locationsText", "")):
                    seen.add(p); out.append((ten, ten.title(), j["title"], j["locationsText"], f"{base}/wday/cxs/{ten}/{site}{p}", f"{base}/{site}{p}"))
            if len(d.get("jobPostings", [])) < 20:
                break
    return out


def judge(c):
    ten, comp, title, loc, api, apply_url = c
    if title_skip(title) or dedup(comp):
        return None
    try:
        info = call(api)["jobPostingInfo"]
    except Exception:
        return None
    jd = strip_html(info.get("jobDescription", ""))
    loc_full = info.get("location", loc) or loc
    if location_check(loc_full, jd)[0] == "skip" or yoe_check(jd)[0] == "skip":
        return None
    sc, parts = fit_score(title, jd, loc_full)
    return (sc, parts["lane"], comp, title, loc_full[:30], apply_url, info.get("jobReqId", ""), yoe_check(jd)[0]) if (sc >= MIN_FIT and parts["lane"] == 3) else None


if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        cands = [c for r in ex.map(search, TENANTS) for c in r]
        print(f"India roles found across {len(TENANTS)} tenants: {len(cands)}")
        good = [g for g in ex.map(judge, cands) if g]
    best = {}
    for g in sorted(good, reverse=True):  # one best-fit role per company
        best.setdefault(g[2].lower(), g)
    rows = sorted(best.values(), reverse=True)
    lines = [f"# Workday India digest — {datetime.now():%Y-%m-%d %H:%M}", "",
             f"{len(cands)} India roles -> {len(good)} passed title/location/yoe/lane/fit gates -> {len(rows)} companies (one best role each).",
             "", "| Fit | Company | Role | Location | Req | YOE | Apply |", "|--:|---|---|---|---|---|---|"]
    lines += [f"| {r[0]} | {r[2]} | {r[3][:60]} | {r[4]} | {r[6]} | {r[7]} | [apply]({r[5]}) |" for r in rows]
    (OUT / "digest_workday.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(good)} passed gates, {len(rows)} companies -> output/job-search/digest_workday.md")
    for r in rows[:12]: print(r[:5], r[7])
