import urllib.request, json, os, re

out_dir = "job-kit-starter/output/Supabase - AI Platform Engineer"
os.makedirs(out_dir, exist_ok=True)

req = urllib.request.Request("https://api.ashbyhq.com/posting-api/job-board/supabase", headers={"User-Agent": "Mozilla/5.0"})
data = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))

target_job = None
for j in data["jobs"]:
    if "3b5d54ca" in j["jobUrl"]:
        target_job = j
        break

if target_job:
    desc = re.sub(r"<[^>]+>", " ", target_job.get("descriptionHtml", ""))
    desc = re.sub(r"\s+", " ", desc).strip()
    u = target_job["jobUrl"]
    t = target_job["title"]
    content = f"URL: {u}\nDate: 2026-09-29\nCompany: Supabase\nRole: {t}\nLocation: Remote\n\n{desc}\n"
    with open(os.path.join(out_dir, "jd.txt"), "w") as f:
        f.write(content)
    with open(os.path.join(out_dir, "jd.html"), "w") as f:
        f.write(target_job.get("descriptionHtml", ""))
    print("Saved Supabase JD successfully!")
else:
    print("Could not find Supabase job!")
