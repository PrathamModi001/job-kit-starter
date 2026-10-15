import urllib.request, json, re, sys
from bs4 import BeautifulSoup

urls = [
    ("Amgen", "Software Engineer, Full Stack - Decision Intelligence", "https://jobfound.org/job/amgen-is-hiring-for-software-engineer-full-stack-decision-intelligence-hyderabad-india-15-october-2026"),
    ("Deltek", "Software Engineer", "https://jobfound.org/job/deltek-is-hiring-for-software-engineer-bengaluru-karnataka-remote-india-15-october-2026"),
    ("ServiceNow", "Software Engineer", "https://jobfound.org/job/servicenow-is-hiring-for-software-engineer-hyderabad-hybrid-india-15-october-2026"),
    ("Mechademy", "Software Development Engineer -1", "https://jobfound.org/job/mechademy-is-hiring-for-software-development-engineer-1-gurugram-haryana-hybrid-india-15-october-2026"),
    ("Cisco", "Software Engineer, Delivery Platform", "https://jobfound.org/job/cisco-is-hiring-for-software-engineer-delivery-platform-bengaluru-karnataka-india-india-15-october-2026"),
    ("Innova ESI", "Full Stack Developer", "https://jobfound.org/job/innova-esi-is-hiring-for-full-stack-developer-pune-maharashtra-india-15-october-2026"),
    ("codExalters", "Angular - Node Js Developer", "https://jobfound.org/job/codexalters-is-hiring-for-angular-node-js-developer-ahmedabad-gujarat-india-india-15-october-2026")
]

for co, title, u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as resp:
            html_txt = resp.read().decode('utf-8')
            # Look for apply button / external link
            # Often jobfound has a direct apply link or redirect button
            ext_links = re.findall(r'href="([^"]+)"[^>]*>.*?Apply', html_txt, re.I | re.DOTALL)
            all_http = re.findall(r'https?://[^\s"\'<>]+', html_txt)
            cand_links = [l for l in all_http if not any(x in l for x in ['jobfound.org', 'schema.org', 'google', 'facebook', 'twitter', 'linkedin.com/showcase', 'w3.org', 'nextjs', 'vercel'])]
            print(f"=== {co} : {title} ===")
            print("Apply button links:", ext_links)
            print("Candidate external links:", list(set(cand_links))[:5])
    except Exception as e:
        print(f"Error {co}: {e}")
