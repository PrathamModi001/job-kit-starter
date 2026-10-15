import re

with open("scratch/vvd_careers.html", "r", encoding="utf-8") as f:
    html = f.read()

# search for links
links = re.findall(r'href="([^"]+)"', html)
for l in links:
    if "career" in l or "job" in l or "apply" in l or "junior" in l:
        print("Link:", l)
