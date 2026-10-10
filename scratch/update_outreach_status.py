import csv
from pathlib import Path

csv_path = Path("job-kit-starter/output/job-search/outreach/startups_outreach.csv")

with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# The last 20 rows were dated 2026-10-10
updated = 0
for r in rows:
    if r.get("Drafted Date") == "2026-10-10" and r.get("Status") == "Drafted in Gmail":
        r["Status"] = "Sent"
        r["Notes"] = r.get("Notes", "") + "; Sent via Gmail on 2026-10-10 per user direction"
        updated += 1

fieldnames = list(rows[0].keys())
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {updated} outreach rows to 'Sent' in {csv_path}")
