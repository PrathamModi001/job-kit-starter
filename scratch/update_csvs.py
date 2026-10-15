import csv

# 1. Update startups_outreach.csv
outreach_csv = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\outreach\startups_outreach.csv'
updated_rows = []
outreach_updated_count = 0

with open(outreach_csv, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

for r in rows:
    # Update rows that were Drafted on 2026-10-14 or currently Drafted
    if r.get('Status') == 'Drafted':
        r['Status'] = 'Sent'
        notes = r.get('Notes', '')
        if 'Sent on 2026-10-15' not in notes:
            r['Notes'] = (notes + '; Sent on 2026-10-15 per user direction').strip('; ')
        outreach_updated_count += 1
    updated_rows.append(r)

with open(outreach_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"Updated {outreach_updated_count} outreach entries to Status=Sent in startups_outreach.csv")

# 2. Inspect applications.csv
app_csv = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv'
with open(app_csv, 'r', encoding='utf-8', errors='ignore') as f:
    app_reader = csv.DictReader(f)
    app_fieldnames = app_reader.fieldnames
    app_rows = list(app_reader)

app_updated_count = 0
for r in app_rows:
    company = r.get('Company', '')
    if company in ['Trackerbot', 'ChainSecurity']:
        # Update notes / next steps if appropriate
        notes = r.get('Notes', '')
        if 'Sent on 2026-10-15' not in notes:
            r['Notes'] = (notes + '; Sent via Gmail on 2026-10-15 per user direction').strip('; ')
            app_updated_count += 1

with open(app_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=app_fieldnames)
    writer.writeheader()
    writer.writerows(app_rows)

print(f"Updated {app_updated_count} applications entries in applications.csv")
