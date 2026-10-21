import csv
import json
import os

csv_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\outreach\startups_outreach.csv'
targets_path = r'E:\Extra\job-kit-starter\scratch\today_20_outreach_targets.json'

with open(targets_path, 'r', encoding='utf-8') as f:
    targets = json.load(f)

# Read existing rows
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"Total existing rows in startups_outreach.csv: {len(rows)}")

# Filter out any placeholder rows added today that mentioned prepared_drafts.json
clean_rows = []
for r in rows:
    notes = r.get('Notes', '')
    if 'prepared_drafts.json' in notes:
        continue
    clean_rows.append(r)

print(f"Rows after removing placeholders: {len(clean_rows)}")

# Add the 20 verified drafts
for t in targets:
    clean_rows.append({
        'Company': t['Company'],
        'Founder': t['Founder'],
        'Email': t['Email'],
        'Confidence': t['Confidence'],
        'Role Pitch': t['Role Pitch'],
        'Subject': t['Subject'],
        'Status': 'Saved in Gmail Drafts with Resume Attached',
        'Drafted Date': '2026-10-19',
        'Notes': f"Attached Pratham_Modi_Base_Resume.pdf; {t.get('Notes', '')}",
        'Source': t['Source'],
        'Tier': t['Tier']
    })

print(f"Total rows after adding 20 verified drafts: {len(clean_rows)}")

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(clean_rows)

print("startups_outreach.csv successfully updated with 20 verified drafts!")
