import json, urllib.request, re, csv

# Load already contacted companies and emails
contacted_cos = set()
contacted_emails = set()
with open("job-kit-starter/output/job-search/outreach/startups_outreach.csv", encoding="utf-8", errors="ignore") as f:
    for row in csv.DictReader(f):
        co = (row.get("Company") or "").strip().lower()
        em = (row.get("Email") or "").strip().lower()
        if co: contacted_cos.add(co)
        if em: contacted_emails.add(em)

# Also check applications.csv
with open("job-kit-starter/output/job-search/applications.csv", encoding="utf-8", errors="ignore") as f:
    for row in csv.DictReader(f):
        co = (row.get("Company") or "").strip().lower()
        if co: contacted_cos.add(co)

# 1. Fetch HN Who is hiring thread
url = 'https://hn.algolia.com/api/v1/items/49922569'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.load(resp)
    comments = data.get('children', [])
except Exception as e:
    comments = []
    print("Error fetching HN:", e)

hn_candidates = []
for c in comments:
    text = c.get('text') or ''
    # Find emails
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if not emails:
        continue
    # Extract company name from first line
    # Standard HN format: Company | Role | Location
    first_line = text.split('\n')[0]
    parts = [p.strip() for p in re.split(r'\||&#x2F;|<p>', first_line) if p.strip()]
    co = parts[0] if parts else "Unknown"
    # Clean up company name
    co = re.sub(r'<[^>]+>', '', co).strip()
    if len(co) > 35 or len(co) < 2:
        continue
    if co.lower() in contacted_cos:
        continue
    email = emails[0].lower()
    if email in contacted_emails or "example" in email or "ycombinator" in email:
        continue
    
    hn_candidates.append({
        "company": co,
        "email": email,
        "author": c.get("author", "Founder"),
        "first_line": first_line[:100],
        "full_text": text[:500]
    })

print(f"Eligible HN candidates found: {len(hn_candidates)}")
for h in hn_candidates[:15]:
    print(f"- {h['company']} | {h['email']} | {h['author']} | {h['first_line']}")
