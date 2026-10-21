import urllib.request
import json
import re
import subprocess
from pathlib import Path

# Candidates to fetch and test
candidates = [
    {
        "company": "Databricks",
        "role": "Software Engineer, Infrastructure",
        "gh_id": "8829029002",
        "url": "https://boards-api.greenhouse.io/v1/boards/databricks/jobs/8829029002",
        "apply_url": "https://databricks.com/company/careers/open-positions/job?gh_jid=8829029002",
        "ats": "greenhouse"
    },
    {
        "company": "Starburst",
        "role": "AI Platform Engineer",
        "gh_id": "5416975008",
        "url": "https://boards-api.greenhouse.io/v1/boards/starburst/jobs/5416975008",
        "apply_url": "https://job-boards.greenhouse.io/starburst/jobs/5416975008",
        "ats": "greenhouse"
    },
    {
        "company": "Stripe",
        "role": "Software Engineer, Stripe Data Pipeline",
        "gh_id": "8209970",
        "url": "https://boards-api.greenhouse.io/v1/boards/stripe/jobs/8209970",
        "apply_url": "https://stripe.com/jobs/search?gh_jid=8209970",
        "ats": "greenhouse"
    },
    {
        "company": "Stripe",
        "role": "Software Engineer, Internal Systems",
        "gh_id": "7543868",
        "url": "https://boards-api.greenhouse.io/v1/boards/stripe/jobs/7543868",
        "apply_url": "https://stripe.com/jobs/search?gh_jid=7543868",
        "ats": "greenhouse"
    },
    {
        "company": "Cerebras",
        "role": "Full Stack Machine Learning Engineer",
        "ashby_id": "c2198d42-ccad-4bee-aa43-83027aa5e46e",
        "url": "https://api.ashbyhq.com/posting-api/job-board/cerebras",
        "apply_url": "https://jobs.ashbyhq.com/cerebras/c2198d42-ccad-4bee-aa43-83027aa5e46e",
        "ats": "ashby"
    },
    {
        "company": "Cerebras",
        "role": "Cluster Operations Software Engineer",
        "ashby_id": "f25b9677-32fa-41ed-84d1-0ed704a98533",
        "url": "https://api.ashbyhq.com/posting-api/job-board/cerebras",
        "apply_url": "https://jobs.ashbyhq.com/cerebras/f25b9677-32fa-41ed-84d1-0ed704a98533",
        "ats": "ashby"
    },
    {
        "company": "Twilio",
        "role": "Machine Learning Engineer (L3)",
        "gh_id": "8258587",
        "url": "https://boards-api.greenhouse.io/v1/boards/twilio/jobs/8258587",
        "apply_url": "https://job-boards.greenhouse.io/twilio/jobs/8258587",
        "ats": "greenhouse"
    },
    {
        "company": "Jump Trading",
        "role": "Infrastructure Engineer",
        "gh_id": "7606254",
        "url": "https://boards-api.greenhouse.io/v1/boards/jumptrading/jobs/7606254",
        "apply_url": "https://www.jumptrading.com/hr/job?gh_jid=7606254",
        "ats": "greenhouse"
    },
    {
        "company": "Pure Storage",
        "role": "Application Engineer (AI Automation)",
        "gh_id": "8002123",
        "url": "https://boards-api.greenhouse.io/v1/boards/purestorage/jobs/8002123",
        "apply_url": "https://job-boards.greenhouse.io/purestorage/jobs/8002123",
        "ats": "greenhouse"
    }
]

out_base = Path("job-kit-starter/output")

for c in candidates:
    co = c["company"]
    role = c["role"]
    folder_name = f"{co} - {role}"
    dir_path = out_base / folder_name
    dir_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Title gate
    cmd = ["python", "job-kit-starter/gates.py", "title", role]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"TITLE SKIP ({res.stdout.strip()}): {folder_name}")
        continue
    
    # 2. Fetch JD text
    jd_text = ""
    try:
        if c["ats"] == "greenhouse":
            req = urllib.request.Request(c["url"], headers={"User-Agent": "Mozilla/5.0"})
            data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
            content = data.get("content", "")
            # clean via gates.py clean
            clean_cmd = ["python", "job-kit-starter/gates.py", "clean"]
            res = subprocess.run(clean_cmd, input=content, capture_output=True, text=True)
            jd_text = res.stdout.strip()
        elif c["ats"] == "ashby":
            req = urllib.request.Request(c["url"], headers={"User-Agent": "Mozilla/5.0"})
            data = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
            for j in data.get("jobs", []):
                if j.get("id") == c.get("ashby_id"):
                    content = j.get("descriptionHtml", "")
                    clean_cmd = ["python", "job-kit-starter/gates.py", "clean"]
                    res = subprocess.run(clean_cmd, input=content, capture_output=True, text=True)
                    jd_text = res.stdout.strip()
                    break
    except Exception as e:
        print(f"FETCH ERROR ({folder_name}): {e}")
        continue
    
    jd_file = dir_path / "jd.txt"
    jd_file.write_text(jd_text, encoding="utf-8")
    sz = len(jd_text.encode("utf-8"))
    
    # 3. YOE gate
    yoe_cmd = ["python", "job-kit-starter/gates.py", "yoe", str(jd_file)]
    yoe_res = subprocess.run(yoe_cmd, capture_output=True, text=True)
    yoe_verdict = yoe_res.stdout.strip()
    
    # Check forbidden stack words in primary focus
    forbidden = []
    for term in [r"\bjava\b", r"\.net\b", r"\bc#", r"asp\.net", r"c\+\+", r"\bruby\b", r"\brails\b"]:
        if re.search(term, jd_text[:1200], re.I):
            forbidden.append(term)
    
    print(f"{folder_name} | Size: {sz}B | YOE: {yoe_verdict} | Stack Flags: {forbidden}")
