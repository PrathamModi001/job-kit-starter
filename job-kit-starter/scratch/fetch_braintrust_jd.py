import urllib.request, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from gates import clean_html

req = urllib.request.Request('https://api.ashbyhq.com/posting-api/job-board/braintrust', headers={'User-Agent': 'Mozilla/5.0'})
data = json.loads(urllib.request.urlopen(req).read())
for j in data['jobs']:
    if 'sdk' in j['title'].lower():
        clean = clean_html(j['descriptionHtml'])
        out_dir = "output/Braintrust - Software Engineer, SDK"
        os.makedirs(out_dir, exist_ok=True)
        jd_path = os.path.join(out_dir, "jd.txt")
        with open(jd_path, "w", encoding="utf-8") as f:
            f.write(clean)
        print("Saved Braintrust JD size:", os.path.getsize(jd_path))
        break
