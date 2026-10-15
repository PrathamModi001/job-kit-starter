import csv
import sys

# 1. Update startups_outreach.csv
outreach_csv = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\outreach\startups_outreach.csv'
with open(outreach_csv, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

outreach_count = 0
for r in rows:
    if r.get('Status') == 'Drafted':
        r['Status'] = 'Sent'
        notes = r.get('Notes', '')
        if 'Sent on 2026-10-15' not in notes:
            r['Notes'] = (notes + '; Sent on 2026-10-15 per user direction').strip('; ')
        outreach_count += 1

with open(outreach_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"startups_outreach.csv: updated {outreach_count} rows to Status=Sent.")

# 2. Update applications.csv
app_csv = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv'
with open(app_csv, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    app_fieldnames = list(reader.fieldnames)
    app_rows = list(reader)

app_count = 0
for r in app_rows:
    if r.get('Company') in ['Trackerbot', 'ChainSecurity']:
        step = r.get('Next step', '')
        if 'Sent via Gmail on 2026-10-15' not in step:
            r['Next step'] = step + '; Sent via Gmail on 2026-10-15 per user direction'
            app_count += 1

with open(app_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=app_fieldnames)
    writer.writeheader()
    writer.writerows(app_rows)

print(f"applications.csv: updated {app_count} rows with sent notes.")
