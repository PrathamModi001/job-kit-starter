import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

req = urllib.request.Request('https://boards-api.greenhouse.io/v1/boards/observeai/jobs/5432596008?questions=true', headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode())
    print('Questions count:', len(data.get('questions', [])))
    for q in data.get('questions', []):
        lbl = q.get('label')
        req_flag = q.get('required')
        fields = q.get('fields', [])
        f_type = fields[0].get('type') if fields else None
        f_name = fields[0].get('name') if fields else None
        print(f"Label: {lbl} | Req: {req_flag} | Type: {f_type} | Name: {f_name}")
