import urllib.request, json, re

url = 'https://jobfound.org/?page=0&loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&work=remote%2Chybrid%2Consite&type=Full-time'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        m = re.search(r'<script id="job-list-structured-data" type="application/ld\+json">(.*?)</script>', html)
        if m:
            data = json.loads(m.group(1))
            for item in data.get('itemListElement', []):
                print(item.get('name'), '->', item.get('url'))
        else:
            print("No structured data found")
except Exception as e:
    print('Error:', e)
