import json
import csv

json_path = '/home/modi/Work/job-kit-starter/scratch/outreach_10_targets_20260924.json'
csv_path = '/home/modi/Work/job-kit-starter/job-kit-starter/output/job-search/outreach/startups_outreach.csv'

with open(json_path, 'r') as f:
    targets = json.load(f)

# Header: Company,Founder,Email,Confidence,Role Pitch,Subject,Status,Drafted Date,Notes,Source,Tier
fieldnames = [
    'Company', 'Founder', 'Email', 'Confidence', 'Role Pitch',
    'Subject', 'Status', 'Drafted Date', 'Notes', 'Source', 'Tier'
]

new_rows = []
for t in targets:
    row = {
        'Company': t['company'],
        'Founder': t['founder'],
        'Email': t['email'],
        'Confidence': t.get('confidence', 'Verified'),
        'Role Pitch': t['role_pitch'],
        'Subject': t['subject'],
        'Status': 'Saved in Gmail Drafts with Resume Attached',
        'Drafted Date': '2026-09-24',
        'Notes': t['notes'],
        'Source': t.get('source', 'Founder Outreach'),
        'Tier': t.get('tier', 'A')
    }
    new_rows.append(row)

with open(csv_path, 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    for r in new_rows:
        writer.writerow(r)

print(f"Successfully appended {len(new_rows)} rows to {csv_path}")
