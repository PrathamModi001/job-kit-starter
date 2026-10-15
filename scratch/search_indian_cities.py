import urllib.request
import json

terms = ['bengaluru', 'bangalore', 'mumbai', 'pune', 'gurgaon', 'delhi', 'noida', 'hyderabad', 'chennai']
for term in terms:
    url = f"https://hn.algolia.com/api/v1/search?query={term}&tags=comment,story_49922569"
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get("hits", [])
            if hits:
                print(f"Term: {term} -> {len(hits)} hits")
                for h in hits[:2]:
                    header = (h.get('comment_text') or '').split('<p>')[0]
                    print(f"   [{h.get('objectID')}] {header[:120]}")
    except Exception as e:
        print(f"Error {term}: {e}")
