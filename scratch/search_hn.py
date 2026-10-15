import urllib.request
import json

queries = ['junior', 'intern', 'graduate', 'associate', 'software engineer', 'backend', 'full stack']
for q in queries:
    url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(q)}&tags=comment,story_49922569"
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get("hits", [])
            print(f"Query: {q} -> {len(hits)} hits")
            for h in hits[:2]:
                header = (h.get('comment_text') or '').split('<p>')[0]
                print(f"   [{h.get('objectID')}] {header[:120]}")
    except Exception as e:
        print(f"Error {q}: {e}")
