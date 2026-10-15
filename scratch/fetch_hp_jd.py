import urllib.request, json, os
from bs4 import BeautifulSoup

url = 'https://hp.wd5.myworkdayjobs.com/wday/cxs/hp/ExternalCareerSite/job/Bengaluru-Karntaka-India/Software-Applications_3166748-1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

info = data['jobPostingInfo']
title = info.get('title', '')
desc_html = info.get('jobDescription', '')
soup = BeautifulSoup(desc_html, 'html.parser')

lines = [
    f"Job Title: {title}",
    f"Location: {info.get('location', '')}",
    f"Job Req ID: {info.get('jobReqId', '')}",
    "",
    soup.get_text(separator='\n')
]
clean_text = '\n'.join(lines)

out_dir = 'job-kit-starter/output/HP - Software Applications'
os.makedirs(out_dir, exist_ok=True)
with open(f'{out_dir}/jd.txt', 'w', encoding='utf-8') as f:
    f.write(clean_text)

print(f"Written HP jd.txt length: {len(clean_text)} bytes")
