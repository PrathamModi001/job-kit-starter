import urllib.request, json, csv, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from gates import title_skip, location_check, yoe_check

applied = {r['Company'].strip().lower() for r in csv.DictReader(open('output/job-search/applications.csv', encoding='utf-8'))}

ashby_slugs = [
    ("inngest", "Inngest"), ("weaviate", "Weaviate"), ("neon", "Neon"), ("modal", "Modal"),
    ("linear", "Linear"), ("railway", "Railway"), ("warp", "Warp"), ("e2b", "E2B"),
    ("zed", "Zed"), ("vapi", "Vapi"), ("smallest", "Smallest.ai"), ("stack-ai", "Stack.ai"),
    ("julius", "Julius"), ("langchain", "LangChain"), ("langfuse", "Langfuse"), ("baseten", "Baseten"),
    ("anyscale", "Anyscale"), ("twenty", "Twenty"), ("n8n", "n8n"), ("svix", "Svix"),
    ("knock", "Knock"), ("openphone", "OpenPhone"), ("pinecone", "Pinecone"), ("deepgram", "Deepgram"),
    ("decagon", "Decagon"), ("sarvam", "Sarvam"), ("perplexity", "Perplexity"), ("scaleai", "Scale AI"),
    ("sierra", "Sierra"), ("cohere", "Cohere"), ("cursor", "Cursor"), ("cognition", "Cognition"),
    ("factory", "Factory"), ("arize", "Arize AI"), ("vellum", "Vellum"), ("humanloop", "Humanloop"),
    ("portkey", "Portkey"), ("wandb", "Weights & Biases"), ("lamini", "Lamini"), ("chroma", "Chroma"),
    ("qdrant", "Qdrant"), ("zilliz", "Zilliz"), ("voyageai", "Voyage AI"), ("unstructured", "Unstructured"),
    ("llamaindex", "LlamaIndex"), ("mem0", "Mem0"), ("crewai", "CrewAI"), ("braintrust", "Braintrust"),
    ("cartesia", "Cartesia"), ("elevenlabs", "ElevenLabs"), ("resend", "Resend"), ("replit", "Replit"),
    ("composio", "Composio"), ("supabase", "Supabase"), ("firecrawl", "Firecrawl"), ("render", "Render")
]

gh_slugs = [
    ("togetherai", "Together AI"), ("groq", "Groq"), ("cerebras", "Cerebras"), ("coactive", "Coactive"),
    ("mistral", "Mistral AI"), ("runwayml", "Runway"), ("pika", "Pika"), ("character", "Character.AI"),
    ("glean", "Glean"), ("c3ai", "C3 AI"), ("abacusai", "Abacus.AI"), ("snorkel", "Snorkel AI")
]

results = []

for slug, name in ashby_slugs:
    if name.lower() in applied:
        continue
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=4) as res:
            data = json.loads(res.read().decode('utf-8'))
            for j in data.get('jobs', []):
                title = j.get('title', '')
                loc = j.get('location', '')
                desc = j.get('descriptionHtml', '')
                t_skip = title_skip(title)
                if t_skip: continue
                loc_s, loc_why = location_check(loc, desc)
                if loc_s == 'skip': continue
                y_s, y_ev = yoe_check(desc)
                if y_s == 'skip': continue
                results.append({
                    'co': name,
                    'title': title,
                    'loc': loc,
                    'url': j.get('jobUrl', ''),
                    'desc': desc,
                    'type': 'ashby',
                    'slug': slug,
                    'id': j.get('id')
                })
    except Exception:
        pass

for slug, name in gh_slugs:
    if name.lower() in applied:
        continue
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=4) as res:
            data = json.loads(res.read().decode('utf-8'))
            for j in data.get('jobs', []):
                title = j.get('title', '')
                loc = (j.get('location') or {}).get('name', '')
                t_skip = title_skip(title)
                if t_skip: continue
                loc_s, loc_why = location_check(loc, '')
                if loc_s == 'skip': continue
                results.append({
                    'co': name,
                    'title': title,
                    'loc': loc,
                    'url': j.get('absolute_url', ''),
                    'desc': '',
                    'type': 'gh',
                    'slug': slug,
                    'id': j.get('id')
                })
    except Exception:
        pass

print(f"Total matching roles from top AI/dev tools: {len(results)}")
for r in results:
    print(f"{r['co']} | {r['title']} | {r['loc']} | {r['url']}")
