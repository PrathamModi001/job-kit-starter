import json

with open(r'C:\Users\prathamm\.gemini\antigravity-cli\brain\edc45ac8-5c9f-4948-9a84-d45540b2cea8\.system_generated\steps\24\output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = '### Result\n'
if text.startswith(prefix):
    text = text[len(prefix):]

first_line = text.split('\n### Ran Playwright code')[0].strip()
content = json.loads(first_line)

with open(r'E:\Extra\job-kit-starter\job-kit-starter\output\FutureStrive - AI Engineer\jd.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(content)

print(f"Successfully written {len(content)} chars to jd.txt")
