import urllib.request, re, json
from bs4 import BeautifulSoup

def get_jobfound_jobs():
    url = "https://jobfound.org/?page=0&loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&work=remote%2Chybrid%2Consite&type=Full-time&q=Software+Engineer"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if '/job/' in href:
            links.append('https://jobfound.org' + href if href.startswith('/') else href)
    return list(dict.fromkeys(links))

print("Fetching jobfound jobs...")
jobs = get_jobfound_jobs()
print(f"Found {len(jobs)} jobs on search page")

ats_jobs = []
for j in jobs[:25]:
    try:
        req = urllib.request.Request(j, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        # Look for company name and title
        h1 = soup.find('h1')
        title = h1.get_text().strip() if h1 else ""
        
        # Find ATS link
        ats_links = re.findall(r'https?://[^\s\"\'\<\>]+', html)
        valid_ats = [
            l for l in ats_links 
            if any(ats in l for ats in ['myworkdayjobs', 'greenhouse.io', 'ashbyhq.com', 'lever.co', 'smartapply.indeed.com', 'oraclecloud.com', 'successfactors', 'taleo.net', 'breezy.hr', 'applytojob.com', 'pinpointhq.com', 'jobs.lever.co', 'workable.com'])
            and not 'jobfound.org' in l
        ]
        
        # Also check linkedin links to see if they are not excluded or if direct ATS exists
        other_links = [l for l in ats_links if 'http' in l and not 'jobfound' in l and not 'schema.org' in l and not 'w3.org' in l and not 'nextjs' in l]
        
        print(f"JOB: {j}")
        print(f"  Title: {title}")
        print(f"  ATS Links: {valid_ats}")
        if not valid_ats and other_links:
            print(f"  Other Links: {other_links[:2]}")
    except Exception as e:
        print(f"ERR on {j}: {e}")
