import csv

csv_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv'
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    print("Fieldnames:", reader.fieldnames)
    rows = list(reader)

print(f"Total rows: {len(rows)}")
for r in rows[-10:]:
    print(r)
