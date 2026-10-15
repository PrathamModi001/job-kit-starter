import urllib.request, json, re, csv
from pathlib import Path

csv_path = Path('E:/Extra/job-kit-starter/job-kit-starter/output/job-search/outreach/startups_outreach.csv')
with open(csv_path, encoding='utf-8') as f:
    existing_emails = {row['Email'].strip().lower() for row in csv.DictReader(f) if row.get('Email')}

# Let's search HN Algolia for "Who is hiring" comments with emails
url = "https://hn.algolia.com/api/v1/search_by_date?query=%22Ask%20HN%3A%20Who%20is%20hiring%22&tags=story&hitsPerPage=2"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
hits = json.loads(resp.read().decode('utf-8'))['hits']
thread_id = hits[0]['objectID']
print("Thread:", hits[0]['title'], thread_id)

t_url = f"https://hn.algolia.com/api/v1/items/{thread_id}"
req2 = urllib.request.Request(t_url, headers={'User-Agent': 'Mozilla/5.0'})
thread_data = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))

comments = thread_data.get('children', [])
print(f"Total top-level comments: {len(comments)}")

candidates = []

for c in comments:
    text = c.get('text', '') or ''
    # find emails
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    valid_emails = [e for e in emails if not any(x in e.lower() for x in ['example.com', 'domain.com', 'ycombinator.com', '.png', '.jpg'])]
    if not valid_emails:
        continue
    # find company name from first line
    first_line = re.sub(r'<[^>]+>', ' ', text).splitlines()[0] if text else ''
    co = first_line.split('|')[0].strip() if '|' in first_line else first_line[:30].strip()
    
    for em in valid_emails:
        if em.lower() not in existing_emails and len(co) > 2:
            candidates.append((co, em, first_line[:100]))
            break

print(f"Found {len(candidates)} uncontacted HN candidates:")
for co, em, line in candidates[:20]:
    print(f"- {co:25} | {em:30} | {line}")
