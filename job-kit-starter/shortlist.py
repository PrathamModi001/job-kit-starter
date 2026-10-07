#!/usr/bin/env python3
"""Orchestrator helper: turn the scan digests into a gated, deduped shortlist (no LLM turns needed).

  python shortlist.py [N=15]     (run AFTER job_hunt.py / job_hunt_india.py / hn_scan.py)
Reads output/job-search/digest*.md rows, drops: hard-skip titles (gates.py), non-India/non-approved-city
locations, companies already in applications.csv. Prints top N by scan score.
"""
import csv, re, sys
from pathlib import Path
from gates import title_skip

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output/job-search"
ROW2 = re.compile(r"\|\s*(\d+)\s*\|\s*([^|\[]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|[^\n]*?\[link\]\((\S+?)\)")  # digest_india.md
CITY = re.compile(r"(?:KA|TG|MH|TN|GJ|HR),\s*IN|india|bengaluru|bangalore|hyderabad|secunderabad|pune|gurgaon|gurugram|mumbai|ahmedabad|chennai", re.I)
ROW = re.compile(r"\|\s*\S*\s*\|\s*(\d+)\s*\|\s*\[(.+?)\]\((\S+?)\)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|")


def main(n):
    done = {r["Company"].strip().lower() for r in csv.DictReader(open(OUT / "applications.csv", encoding="utf-8"))}
    seen, out = set(), []
    for f in sorted(OUT.glob("digest*.md")):
        text = f.read_text(encoding="utf-8")
        rows = [(int(m[1]), m[2], m[3], m[4], m[5]) for m in ROW.finditer(text)]
        rows += [(int(m[1]), m[2], m[5], m[3], m[4]) for m in ROW2.finditer(text)]
        for score, title, url, company, loc in rows:
            if url in seen or company.strip().lower() in done:
                continue
            seen.add(url)
            if title_skip(title) or not CITY.search(loc + " " + title):
                continue
            out.append((score, title[:70], company, loc[:30], url))
    for s, t, c, l, u in sorted(out, reverse=True)[:n]:
        print(f"{s:>3} | {c} | {t} | {l} | {u}")  # KA/TG/MH.. = state only: confirm city is on the approved list
    print(f"-- {len(out)} candidates after gates; JD YOE/claim gates still run per lead (gates.py yoe)")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 15)
