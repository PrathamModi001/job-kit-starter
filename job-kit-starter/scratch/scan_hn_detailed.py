import json, csv, re, os

csv_path = "output/job-search/applications.csv" if os.path.exists("output/job-search/applications.csv") else "job-kit-starter/output/job-search/applications.csv"
applied = {r['Company'].strip().lower() for r in csv.DictReader(open(csv_path, encoding='utf-8'))}

# Let's inspect hn_scan.py logic or cache
seen_hn_path = "job-kit-starter/output/job-search/seen_hn.json"
if os.path.exists(seen_hn_path):
    seen_hn = json.load(open(seen_hn_path, encoding="utf-8"))
    print(f"seen_hn keys: {list(seen_hn.keys()) if isinstance(seen_hn, dict) else len(seen_hn)}")

# Let's query Algolia for Ask HN: Who is hiring? (October 2026) thread id 49922569 comments
import urllib.request
thread_id = "49922569"
url = f"https://hn.algolia.com/api/v1/items/{thread_id}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, ".")
    from gates import strip_html, title_skip, location_check, yoe_check
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode("utf-8"))
        children = data.get("children", [])
        print(f"Total top-level comments: {len(children)}")
        # Check comments
        for c in children:
            text = c.get("text") or ""
            first_line = text.split("\n")[0] if text else ""
            clean = strip_html(text)
            first_p = clean[:400]
            
            # Simple keyword check: remote or india
            if not re.search(r"\b(remote|india|bengaluru|bangalore|pune|hyderabad|mumbai|gurgaon|delhi)\b", clean, re.I):
                continue
            if not re.search(r"\b(engineer|developer|backend|full[- ]?stack|software|node|python)\b", clean, re.I):
                continue
            
            # Extract company name (usually first token before pipe or hyphen)
            co_match = re.match(r"^([^|–—\n]+)", strip_html(first_line))
            co = co_match.group(1).strip() if co_match else "Unknown"
            co_clean = re.sub(r"\(.*?\)", "", co).strip()
            if co_clean.lower() in applied or any(a in co_clean.lower() for a in applied if len(a) > 3):
                continue
            
            # Check title / roles mentioned
            print(f"HN ID: {c.get('id')} | Company: {co_clean} | Applied: {co_clean.lower() in applied}")
            print(f"  Snippet: {clean[:200]}")
            print("-" * 50)
except Exception as e:
    print("Error:", e)
