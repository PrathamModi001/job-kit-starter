import urllib.request
import re

url = 'https://job-boards.greenhouse.io/observeai/jobs/5432596008'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html_doc = resp.read().decode('utf-8')
        print('Fetched HTML length:', len(html_doc))
        forms = re.findall(r'<form[^>]*>', html_doc)
        print('Forms found:', forms)
        inputs = re.findall(r'name=["\']([^"\']+)["\']', html_doc)
        print('Input names found:', set(inputs))
        # Find if there are recaptcha, turnstile, or csrf tokens
        for term in ['csrf', 'token', 'captcha', 'turnstile', 'action']:
            matches = re.findall(rf'.{{0,50}}{term}.{{0,50}}', html_doc, re.IGNORECASE)
            print(f"Matches for {term} (count={len(matches)}):", matches[:3])
except Exception as e:
    print('Error:', e)
