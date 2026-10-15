import re
import html as html_lib
import os

with open("scratch/chainsecurity.html", "r", encoding="utf-8") as f:
    html = f.read()

clean = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'<[^<]+?>', ' ', clean)
clean = html_lib.unescape(clean)
clean = '\n'.join([line.strip() for line in clean.splitlines() if line.strip()])

full_jd = f"""Company: ChainSecurity
Title: Blockchain Security Engineer
Location: Remote / Zurich, Switzerland
URL: https://www.chainsecurity.com/jobs/blockchain-security-engineer/
Contact: jobs@chainsecurity.com

Job Description:
{clean}
"""

target_dir = "job-kit-starter/output/ChainSecurity - Blockchain Security Engineer"
os.makedirs(target_dir, exist_ok=True)
with open(os.path.join(target_dir, "jd.txt"), "w", encoding="utf-8") as f:
    f.write(full_jd)

print("Saved ChainSecurity jd.txt length:", len(full_jd))
print("Preview:\n", clean[:600])
