import json
import csv
import re
import subprocess
from pathlib import Path

output_file = Path(r"C:\Users\prathamm\.gemini\antigravity-cli\brain\9d441164-96d8-4a07-9f77-bc49f337b978\.system_generated\steps\105\output.txt")
content = output_file.read_text(encoding="utf-8")
links = re.findall(r'"link":\s*"(https://jobfound\.org/job/[^"]+)"', content)

apps_csv = Path(r"E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv")
existing_cos = set()
with apps_csv.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("Company"):
            existing_cos.add(row["Company"].strip().lower())

print(f"Total jobfound links: {len(links)}")
leads = []
for link in links:
    # URL format: .../job/<company>-is-hiring-for-<role>-<location>-...
    m = re.search(r"/job/(.+?)-is-hiring-for-(.+?)-(?:bengaluru|bangalore|hyderabad|pune|mumbai|gurgaon|gurugram|chennai|noida|india|remote)", link)
    if m:
        company_raw = m.group(1).replace("-", " ").title()
        role_raw = m.group(2).replace("-", " ").title()
    else:
        # fallback parsing
        slug = link.split("/job/")[-1]
        parts = slug.split("-is-hiring-for-")
        if len(parts) == 2:
            company_raw = parts[0].replace("-", " ").title()
            role_raw = parts[1].replace("-", " ").title()
        else:
            continue

    # Clean up company name
    co_clean = company_raw.lower().strip()
    if co_clean in existing_cos:
        print(f"DEDUP SKIP: {company_raw} already in applications.csv")
        continue

    # Test gates.py title
    cmd = ["python", r"E:\Extra\job-kit-starter\job-kit-starter\gates.py", "title", role_raw]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"TITLE SKIP ({res.stdout.strip()}): {company_raw} - {role_raw}")
        continue

    leads.append({
        "company": company_raw,
        "role": role_raw,
        "link": link
    })

print(f"\n--- QUALIFYING LEADS ({len(leads)}) ---")
for l in leads:
    print(f"- {l['company']} | {l['role']} | {l['link']}")
