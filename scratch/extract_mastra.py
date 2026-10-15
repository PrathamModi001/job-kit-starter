import urllib.request
import json
import html as html_lib
import re

api_url = "https://api.ashbyhq.com/posting-api/job-board/mastra"
req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    for j in data.get("jobs", []):
        if "AI Engineer" in j.get("title", ""):
            print("Found job:", j.get("title"), "id:", j.get("id"))
            desc = j.get("descriptionHtml", "")
            clean_text = re.sub(r'<[^<]+?>', ' ', desc)
            clean_text = html_lib.unescape(clean_text)
            clean_text = '\n'.join([line.strip() for line in clean_text.splitlines() if line.strip()])
            full_jd = f"Company: Mastra\nTitle: {j.get('title')}\nLocation: {j.get('locationName')}\nDepartment: {j.get('departmentName')}\n\nJob Description:\n{clean_text}\n"
            with open("job-kit-starter/output/Mastra - AI Engineer/jd.txt", "w", encoding="utf-8") as out_f:
                out_f.write(full_jd)
            print("Saved jd.txt length:", len(full_jd))
