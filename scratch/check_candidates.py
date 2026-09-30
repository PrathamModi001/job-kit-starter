import urllib.request
import re

slugs = [
    "phenom-is-hiring-for-product-development-engineer-1-hyderabad-telangana-india-28-september-2026",
    "nua-is-hiring-for-application-developer-india-29-september-2026",
    "simbian-inc-is-hiring-for-frontend-engineer-bangalore-remote-india-28-september-2026",
    "cohere-health-is-hiring-for-associate-software-engineer-hyderabad-telangana-india-29-september-2026",
    "eternup-is-hiring-for-founding-engineer-kolkata-metropolitan-area-west-bengal-hybrid-india-29-september-2026"
]

for s in slugs:
    url = f"https://jobfound.org/job/{s}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        ats_candidates = re.findall(r"https?://[^\s\"<>]+", html)
        clean_ats = [
            x.replace("\\u0026", "&").rstrip("\\").rstrip('"').rstrip("'")
            for x in ats_candidates
            if any(ats in x for ats in [
                "greenhouse.io", "lever.co", "ashbyhq.com", "myworkdayjobs.com", 
                "myworkdaysite.com", "successfactors", "freshteam.com", "smartrecruiters.com",
                "oraclecloud.com", "icims.com", "workable.com", "careers.", "jobs.", "phenompeople"
            ]) and "jobfound.org" not in x and "schema.org" not in x
        ]
        print(s)
        print("  ATS:", list(dict.fromkeys(clean_ats))[:3])
    except Exception as e:
        print("  Error:", e)
