import urllib.request, json, re, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gates

UA = {"User-Agent": "Mozilla/5.0"}
def fetch_url(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", "replace")

leads = [
    {
        "company": "HighLevel",
        "title": "Full Stack Builder (Team of One)",
        "loc": "India",
        "url": "https://jobs.lever.co/gohighlevel/ce928065-f2cf-4412-a5e7-32677e6f4e4b",
        "api_url": "https://api.lever.co/v0/postings/gohighlevel/ce928065-f2cf-4412-a5e7-32677e6f4e4b"
    },
    {
        "company": "Sarvam",
        "title": "Agent Engineer",
        "loc": "Bengaluru",
        "url": "https://jobs.ashbyhq.com/sarvam/36f89b00-2010-4d23-aae3-17a2f53d9eaa",
        "ashby_id": "36f89b00-2010-4d23-aae3-17a2f53d9eaa"
    },
    {
        "company": "Flex",
        "title": "Associate Software Engineer - IT",
        "loc": "Chennai",
        "url": "https://flextronics.wd1.myworkdayjobs.com/Careers/job/Chennai-India/Associate-Software-Engineer---IT_WD251842"
    },
    {
        "company": "ABB",
        "title": "Software Engineer",
        "loc": "Bangalore",
        "url": "https://careers.abb/global/en/job/97072506/Software-Engineer"
    },
    {
        "company": "Syntrace",
        "title": "Software Engineer",
        "loc": "Mumbai",
        "url": "https://wellfound.com/company/syntrace/jobs/3103444-software-engineer"
    },
    {
        "company": "Thinknovaa",
        "title": "Back-End Developer",
        "loc": "India",
        "url": "https://wellfound.com/company/thinknovaa/jobs/3142200-back-end-developer"
    }
]

for l in leads:
    co = l["company"]
    ti = l["title"]
    folder_name = f"{co} - {ti}".replace("/", "-")
    out_dir = ROOT / "output" / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)
    jd_path = out_dir / "jd.txt"
    
    # Check dedup
    dedup_st = gates.dedup(co)
    print(f"\n=== {co} - {ti} ===")
    print(f"Dedup check: {dedup_st or 'NEW'}")
    if dedup_st:
        print(f"Skipping duplicate: {dedup_st}")
        continue

    # Fetch JD
    jd_text = ""
    try:
        if "api_url" in l:
            d = json.loads(fetch_url(l["api_url"]))
            desc = d.get("descriptionPlain") or gates.strip_html(d.get("description", ""))
            lists = d.get("lists", [])
            for li in lists:
                desc += "\n\n" + li.get("text", "") + "\n" + gates.strip_html(li.get("content", ""))
            jd_text = f"{ti} at {co} ({l['loc']})\n\n{desc}"
        elif "ashby_id" in l:
            # fetch ashby posting api
            d = json.loads(fetch_url("https://api.ashbyhq.com/posting-api/job-board/sarvam?includeCompensation=true"))
            for j in d.get("jobs", []):
                if j.get("id") == l["ashby_id"]:
                    jd_text = f"{ti} at {co} ({l['loc']})\n\n" + (j.get("descriptionPlain") or gates.clean_html(j.get("descriptionHtml", "")))
                    break
        else:
            raw = fetch_url(l["url"])
            clean = gates.clean_html(raw)
            jd_text = clean
    except Exception as e:
        print(f"Fetch error: {e}")
        continue
        
    if len(jd_text) < 1000:
        print(f"JD text too short ({len(jd_text)} bytes), might need browser or direct ATS fetch")
    else:
        print(f"Fetched JD: {len(jd_text)} chars")
        jd_path.write_text(jd_text, encoding="utf-8")
        
        # Run preflight
        t_skip = gates.title_skip(ti)
        loc_stat, loc_why = gates.location_check(l["loc"], jd_text)
        y_stat, y_ev = gates.yoe_check(jd_text)
        sc, parts = gates.fit_score(ti, jd_text, l["loc"])
        flags = sorted({m.group(0).lower() for m in gates.JD_FLAG.finditer(gates.strip_html(jd_text))})
        
        print(f"preflight: title={'SKIP ('+t_skip+')' if t_skip else 'CLEAR'} | loc={loc_stat} ({loc_why}) | yoe={y_stat} ({y_ev}) | fit={sc}/15 (min {gates.MIN_FIT})")
        print(f"flags: {flags or 'none'}")
        
        passed = (not t_skip) and (loc_stat != "skip") and (y_stat != "skip") and (sc >= gates.MIN_FIT)
        print(f"Result: {'PASS' if passed else 'FAIL'}")
