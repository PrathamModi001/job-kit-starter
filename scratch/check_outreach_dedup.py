import json
import csv
from pathlib import Path

targets_path = Path(r"E:\Extra\job-kit-starter\scratch\today_20_outreach_targets.json")
outreach_path = Path(r"E:\Extra\job-kit-starter\job-kit-starter\output\job-search\outreach\startups_outreach.csv")

targets = json.loads(targets_path.read_text(encoding="utf-8"))
existing_emails = set()
existing_cos = set()

with outreach_path.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("Email"):
            existing_emails.add(row["Email"].strip().lower())
        if row.get("Company"):
            existing_cos.add(row["Company"].strip().lower())

print(f"Total existing emails in outreach CSV: {len(existing_emails)}")
print(f"Total existing companies in outreach CSV: {len(existing_cos)}")

dupes = []
clean = []
for t in targets:
    em = t["Email"].strip().lower()
    co = t["Company"].strip().lower()
    if em in existing_emails or co in existing_cos:
        dupes.append((t["Company"], t["Email"], em in existing_emails, co in existing_cos))
    else:
        clean.append(t)

print(f"Clean new targets: {len(clean)} / {len(targets)}")
for d in dupes:
    print(f"DUPE: {d}")
