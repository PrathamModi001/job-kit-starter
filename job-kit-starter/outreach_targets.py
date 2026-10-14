#!/usr/bin/env python3
"""Find engineers (not founders) at a company from PUBLIC GitHub commit-author emails.
  python outreach_targets.py <github-org> [<github-org> ...] [--repos 3] [--per-repo 40]
Prints one line per person: org | name | email | commits | repo. Company-domain emails only (free-mail and
noreply dropped). Sorted by commit count -- pick active, mid-senior engineers on the team you'd join, then
log them with Confidence=Verified, Source=GitHub commit author. Unauthenticated API = 60 req/h; set GITHUB_TOKEN
for 5000/h. Founders show up too: skip anyone whose bio/title says founder/CEO."""
import collections, json, os, re, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
FREE = re.compile(r"@(gmail|googlemail|outlook|hotmail|live|yahoo|icloud|proton|protonmail|pm\.me|me)\.", re.I)
SKIP = re.compile(r"noreply|no-reply|\[bot\]|bot@|dependabot|github-actions|renovate", re.I)


def get(url):
    h = {"User-Agent": "outreach_targets", "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"): h["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=15) as r:
        return json.load(r)


def authors(org, repos=3, per_repo=40):
    rs = [r for r in get(f"https://api.github.com/orgs/{org}/repos?sort=pushed&per_page=15") if not r["fork"]][:repos]
    people = collections.defaultdict(lambda: [0, "", set()])
    for r in rs:
        for c in get(f"https://api.github.com/repos/{org}/{r['name']}/commits?per_page={per_repo}"):
            a = (c.get("commit") or {}).get("author") or {}
            email, name = a.get("email", ""), a.get("name", "")
            if not email or SKIP.search(email + name) or FREE.search(email): continue
            p = people[email.lower()]; p[0] += 1; p[1] = name; p[2].add(r["name"])
    return sorted(((n, e, v[0], ",".join(sorted(v[2]))) for e, v in people.items() for n in [v[1]]), key=lambda x: -x[2])


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda f, d: int(a[a.index(f) + 1]) if f in a else d
    for org in [x for x in a if not x.startswith("--") and not x.isdigit()]:
        try:
            for name, email, n, repo in authors(org, opt("--repos", 3), opt("--per-repo", 40)):
                print(f"{org} | {name} | {email} | {n} | {repo}")
        except Exception as e:
            print(f"{org} | ERROR {e}", file=sys.stderr)
