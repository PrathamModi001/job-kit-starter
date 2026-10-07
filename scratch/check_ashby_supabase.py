import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

req = urllib.request.Request('https://api.ashbyhq.com/posting-api/job-board/supabase/job/3b5d54ca-741b-45ac-bd3f-31605a0d3541', headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        data = json.loads(r.read().decode())
        print('Supabase job:', data.get('title'))
        print('Application form fields:')
        for field in data.get('applicationForm', {}).get('fields', []):
            print(field.get('title'), '| req:', field.get('isRequired'), '| type:', field.get('type'))
except Exception as e:
    print('Error:', e)
