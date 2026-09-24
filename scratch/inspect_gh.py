import urllib.request, json, html, re

def check_job(slug, jid):
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs/{jid}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req).read().decode())
        content = data.get("content", "")
        content = re.sub(r"<[^>]+>", " ", content)
        content = html.unescape(content)
        content = re.sub(r"\s+", " ", content).strip()
        print("="*60)
        print(slug, jid, data.get("title"))
        print("LOCATION:", data.get("location"))
        print("CONTENT:", content[:2000])
    except Exception as e:
        print(slug, jid, e)

check_job("stripe", "7543868")
check_job("stripe", "8209970")
check_job("gitlab", "8556658002")
