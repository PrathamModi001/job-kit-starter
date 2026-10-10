import json, csv, base64
from pathlib import Path

# 1. Append rows to startups_outreach.csv
csv_path = Path("job-kit-starter/output/job-search/outreach/startups_outreach.csv")

with open("scratch/today_20_outreach_targets.json") as f:
    targets = json.load(f)

# Fieldnames: Company,Founder,Email,Confidence,Role Pitch,Subject,Status,Drafted Date,Notes,Source,Tier
fieldnames = [
    "Company", "Founder", "Email", "Confidence", "Role Pitch",
    "Subject", "Status", "Drafted Date", "Notes", "Source", "Tier"
]

rows_to_append = []
for t in targets:
    rows_to_append.append({
        "Company": t["Company"],
        "Founder": t["Founder"],
        "Email": t["Email"],
        "Confidence": t["Confidence"],
        "Role Pitch": t["Role Pitch"],
        "Subject": t["Subject"],
        "Status": "Drafted in Gmail",
        "Drafted Date": "2026-10-10",
        "Notes": t["Notes"],
        "Source": t["Source"],
        "Tier": t["Tier"]
    })

with open(csv_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    for r in rows_to_append:
        writer.writerow(r)

print(f"Successfully appended {len(rows_to_append)} rows to {csv_path}")
