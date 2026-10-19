import json
import re
import urllib.request
from bs4 import BeautifulSoup

urls = [
    "https://jobfound.org/job/nymbleup-is-hiring-for-backend-engineer-mumbai-maharashtra-india-india-18-october-2026",
    "https://jobfound.org/job/generative-futures-is-hiring-for-software-engineer-india-remote-india-19-october-2026",
    "https://jobfound.org/job/umanist-na-is-hiring-for-software-development-engineer-1-gurugram-haryana-india-19-october-2026",
    "https://jobfound.org/job/mastercard-is-hiring-for-software-engineer-i-pune-india-18-october-2026",
    "https://jobfound.org/job/innovun-global-is-hiring-for-software-engineer-full-stack-remote-india-18-october-2026",
    "https://jobfound.org/job/dtcc-is-hiring-for-software-engineer-hyderabad-telangana-hybrid-india-19-october-2026",
    "https://jobfound.org/job/schr-dinger-is-hiring-for-software-developer-livedesign-infrastructure-hyderabad-hyderabad-telangana-india-india-18-october-2026",
    "https://jobfound.org/job/the-robotics-ledger-is-hiring-for-software-engineer-india-india-18-october-2026",
    "https://jobfound.org/job/hitachi-energy-is-hiring-for-ai-ml-engineer-chennai-tamil-nadu-india-india-18-october-2026",
    "https://jobfound.org/job/haystack-is-hiring-for-software-engineer-india-india-19-october-2026"
]

headers = {'User-Agent': 'Mozilla/5.0'}

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for apply button / outbound link
        apply_btn = soup.find('a', string=re.compile(r'Apply', re.I))
        apply_url = apply_btn['href'] if apply_btn and 'href' in apply_btn.attrs else 'N/A'
        
        # Check text content
        text = soup.get_text()
        # Find salary mention
        sal_match = re.search(r'(\d+[\s–-]+\d+\s*(?:LPA|INR|k|USD))', text, re.I)
        sal = sal_match.group(1) if sal_match else 'Not listed'
        
        # Check external redirect button
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if 'http' in href and not 'jobfound.org' in href:
                apply_url = href
                break

        print(f"URL: {url.split('/job/')[1][:40]}")
        print(f"  Salary: {sal}")
        print(f"  Outbound: {apply_url}")
    except Exception as e:
        print(f"Err {url}: {e}")
