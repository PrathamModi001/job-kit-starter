import csv

csv_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\outreach\startups_outreach.csv'

with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

updated_count = 0
for r in rows:
    if r.get('Drafted Date') == '2026-10-19' and 'Drafts' in r.get('Status', ''):
        r['Status'] = 'Sent'
        r['Notes'] = r['Notes'] + '; Sent via Gmail on 2026-10-21 with base resume attached'
        updated_count += 1

print(f"Updated {updated_count} outreach rows to 'Sent'!")

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("startups_outreach.csv saved successfully!")
