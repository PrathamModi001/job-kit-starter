import urllib.request, re, json

slugs = [
    "servify-is-hiring-for-software-engineer-mumbai-maharashtra-india-28-september-2026",
    "digicert-is-hiring-for-software-engineer-bengaluru-karnataka-india-28-september-2026",
    "electroglobal-solutions-private-limited-is-hiring-for-associate-embedded-systems-engineer-jaipur-rajasthan-india-28-september-2026",
    "blackbaud-is-hiring-for-web-developer-india-remote-india-28-september-2026",
    "cohere-health-is-hiring-for-associate-software-engineer-hyderabad-telangana-india-29-september-2026",
    "phenom-is-hiring-for-product-development-engineer-1-hyderabad-telangana-india-28-september-2026",
    "nua-is-hiring-for-application-developer-india-29-september-2026",
    "simbian-inc-is-hiring-for-frontend-engineer-bangalore-remote-india-28-september-2026",
    "blue-machines-ai-is-hiring-for-ml-research-engineer-speech-bengaluru-karnataka-hybrid-india-29-september-2026",
    "eternup-is-hiring-for-founding-engineer-kolkata-metropolitan-area-west-bengal-hybrid-india-29-september-2026"
]

for s in slugs:
    url = f"https://jobfound.org/job/{s}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        h1 = re.search(r"<h1[^>]*>([^<]+)</h1>", html)
        title = h1.group(1).strip() if h1 else s
        m = re.findall(r'"applyUrl":\s*"([^"]+)"', html)
        print("TITLE:", title)
        print("SLUG:", s)
        print("APPLY URL:", m[0] if m else "None")
        print("---")
    except Exception as e:
        print("ERR:", s, e)
