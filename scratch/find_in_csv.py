import csv

with open(r"E:\Extra\job-kit-starter\job-kit-starter\output\job-search\outreach\startups_outreach.csv", encoding="utf-8") as f:
    for i, row in enumerate(csv.DictReader(f), 2):
        if any(term in row.get("Company", "").lower() for term in ["namespace", "toddle", "phonepe", "cashfree"]):
            print(f"Line {i}: {row.get('Company')} | {row.get('Email')} | {row.get('Status')} | {row.get('Drafted Date')}")
