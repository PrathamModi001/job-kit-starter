import urllib.request, re, json

with open('.playwright-mcp/page-2026-09-23T11-56-10-771Z.yml') as f:
    text = f.read()

urls = list(dict.fromkeys(re.findall(r'- /url:\s*(/job/[^\n]+)', text)))
print(f'Scanning {len(urls)} jobfound pages for direct ATS links...')

results = []
for u in urls:
    full_url = 'https://jobfound.org' + u
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        
        # look for json-ld or script containing original job link
        # e.g. "https://job-boards.greenhouse.io/..."
        m = re.findall(r'https?://[^\s\"\'<>]+', html)
        ats_candidates = [
            x for x in m 
            if any(ats in x for ats in [
                'greenhouse.io', 'lever.co', 'ashbyhq.com', 'myworkdayjobs.com', 
                'myworkdaysite.com', 'successfactors', 'freshteam.com', 'smartrecruiters.com',
                'oraclecloud.com', 'icims.com', 'workable.com', 'careers.'
            ]) and not x.startswith('https://jobfound.org') and not 'schema.org' in x
        ]
        
        h1 = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        title = h1.group(1).strip() if h1 else u
        clean_ats = None
        if ats_candidates:
            clean_ats = ats_candidates[0].replace('\\u0026', '&').rstrip('\\').rstrip('"').rstrip("'")
        
        results.append({'slug': u, 'title': title, 'ats_url': clean_ats})
        print(f'{title} -> {clean_ats}')
    except Exception as e:
        print(f'Error {u}: {e}')

with open('scratch/jobfound_ats_links.json', 'w') as f:
    json.dump(results, f, indent=2)

print('Saved scratch/jobfound_ats_links.json')
