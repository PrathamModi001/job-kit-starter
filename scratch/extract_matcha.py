import re
import html as html_lib
import os

with open("scratch/matcha_fse.html", "r", encoding="utf-8") as f:
    html = f.read()

clean = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'<[^<]+?>', ' ', clean)
clean = html_lib.unescape(clean)
clean = '\n'.join([line.strip() for line in clean.splitlines() if line.strip()])

full_jd = f"""Company: Matcha.fm
Title: Founding Software Engineer
Location: Worldwide Remote
URL: https://matcha.fm/apply/fse

Job Description:
{clean}
"""

target_dir = "job-kit-starter/output/Matcha.fm - Founding Software Engineer"
os.makedirs(target_dir, exist_ok=True)
with open(os.path.join(target_dir, "jd.txt"), "w", encoding="utf-8") as f:
    f.write(full_jd)

print("Saved Matcha.fm jd.txt length:", len(full_jd))
print("Preview:\n", clean[:500])
