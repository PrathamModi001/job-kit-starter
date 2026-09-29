import urllib.request, re, json

leads = [
    "https://jobfound.org/job/qualityai-is-hiring-for-full-stack-developer-bangalore-india-28-september-2026",
    "https://jobfound.org/job/lululemon-is-hiring-for-software-engineer-data-and-ai-platform-bengaluru-india-28-september-2026",
    "https://jobfound.org/job/servify-is-hiring-for-software-engineer-mumbai-maharashtra-india-28-september-2026",
    "https://jobfound.org/job/sia-is-hiring-for-forward-deployed-engineer-kurla-maharashtra-india-28-september-2026",
    "https://jobfound.org/job/mindbun-is-hiring-for-product-engineer-india-remote-india-28-september-2026",
    "https://jobfound.org/job/blackbaud-is-hiring-for-web-developer-india-remote-india-28-september-2026",
    "https://jobfound.org/job/commure-is-hiring-for-forward-deployed-engineer-remote-india-28-september-2026",
    "https://jobfound.org/job/magnitude-software-is-hiring-for-associate-software-engineer-hyderabad-remote-india-28-september-2026",
    "https://jobfound.org/job/digicert-is-hiring-for-software-engineer-bengaluru-karnataka-india-28-september-2026",
    "https://jobfound.org/job/oracle-is-hiring-for-application-software-engineer-1-bengaluru-karnataka-india-28-september-2026",
    "https://jobfound.org/job/continental-is-hiring-for-software-engineer-data-platform-bangalore-karnataka-hybrid-india-28-september-2026"
]

for url in leads:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        
        ats_candidates = re.findall(r"https?://[^\s\"'<>]+", html)
        clean_ats = [
            x.replace("\\u0026", "&").rstrip("\\").rstrip('"').rstrip("'")
            for x in ats_candidates
            if any(ats in x for ats in [
                "greenhouse.io", "lever.co", "ashbyhq.com", "myworkdayjobs.com", 
                "myworkdaysite.com", "successfactors", "freshteam.com", "smartrecruiters.com",
                "oraclecloud.com", "icims.com", "workable.com", "careers.", "jobs."
            ]) and "jobfound.org" not in x and "schema.org" not in x
        ]
        
        h1 = re.search(r"<h1[^>]*>([^<]+)</h1>", html)
        title = h1.group(1).strip() if h1 else "unknown"
        
        print("========================================")
        print("URL:", url)
        print("Title:", title)
        print("Direct ATS links found:", list(dict.fromkeys(clean_ats))[:3])
    except Exception as e:
        print("Error fetching", url, e)
