import urllib.request, re

u = "https://jobfound.org/job/american-express-is-hiring-for-software-engineer-i-gurugram-hr-hybrid-india-19-october-2026"
req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
urls = set(re.findall(r'https?://[^\s"\'<>]+', html))
for link in sorted(urls):
    if "jobfound.org" not in link and "w3.org" not in link and "schema.org" not in link:
        print(link)
