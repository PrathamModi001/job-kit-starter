#!/usr/bin/env python3
"""Convert output/job-search/applications.csv into tracker/src/data.json (+meta.json).

Run from repo root or tracker/: derives "applied on" platform and "found via"
source per row. Re-run + `npm run deploy` for the daily refresh.
"""
import csv, json, re, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / 'output/job-search/applications.csv'
OUT = Path(__file__).resolve().parent / 'src'

ATS_NAMES = {
    'ashbyhq': 'Ashby', 'greenhouse': 'Greenhouse', 'lever': 'Lever',
    'workatastartup': 'Work at a Startup', 'wellfound': 'Wellfound',
    'indeed': 'Indeed', 'linkedin': 'LinkedIn', 'cutshort': 'Cutshort',
    'darwinbox': 'Darwinbox', 'myworkdayjobs': 'Workday', 'oraclecloud': 'Oracle',
    'mlp.com': 'Eightfold', 'ycombinator': 'Hacker News',
    'nike.com': 'Workday', 'higher.gs.com': 'Oracle', 'instahyre': 'Instahyre',
}
REFERRAL_COMPANIES = set()  # companies found via a personal referral list — fill in your own
OVERRIDES_FOUND = {
    'Millennium': 'LinkedIn', 'Goldman Sachs': 'Indeed', 'NIKE': 'Indeed',
    'Upstox': 'Indeed', 'The Auction Collective': 'Indeed', 'Cartesia': 'LinkedIn',
    'Lumen Labs': 'Hacker News', 'Logen.io': 'Hacker News', 'MixRank': 'Hacker News',
}
OVERRIDES_VIA = {'Cartesia': 'Ashby', 'Goldman Sachs': 'GS careers (Oracle)'}


def domain_name(url):
    host = urlparse(url or '').netloc.lower()
    for k, v in ATS_NAMES.items():
        if k in host or k in (url or '').lower():
            return v
    return None


def derive(r):
    ch, url, co = r['Channel'], r['Job URL'], r['Company']
    if '→' in ch or '->' in ch:
        left, right = re.split(r'→|->', ch, maxsplit=1)
        found, via = left.strip(), right.strip()
        if 'company ATS' in via:
            via = domain_name(url) or 'Company ATS'
    else:
        base = ch.split('(')[0].strip()
        via = {'WaaS': 'Work at a Startup'}.get(base, base)
        if base in ('Ashby', 'Greenhouse', 'Lever'):
            found = 'Referral list' if co in REFERRAL_COMPANIES else 'ATS board scan'
        elif 'JobSpy' in ch:
            found = 'Indeed (JobSpy digest)'
        elif base.startswith('Email'):
            via = 'Email (founder)'
            found = 'Hacker News' if 'ycombinator' in (url or '') else 'Outreach'
        elif base == 'Company site':
            found = 'Hacker News'
        else:
            found = base
    found = OVERRIDES_FOUND.get(co, found)
    via = OVERRIDES_VIA.get(co, via)
    if co in REFERRAL_COMPANIES:
        found = 'Referral list'
    return via, found


def main():
    rows = list(csv.DictReader(open(CSV)))
    data = []
    for r in rows:
        via, found = derive(r)
        data.append({
            'co': r['Company'], 'role': r['Role'], 'loc': r['Location'],
            'via': via, 'found': found, 'comp': r['Comp'],
            'status': r['Status'], 'date': r['Applied'] or r['Updated'] or r['Added'],
            'url': r['Job URL'], 'resume': r.get('Resume', ''),
        })
    order = {'Applied': 0, 'Drafting': 1, 'Lead': 2, 'Closed': 3, 'Skipped': 4}
    data.sort(key=lambda d: (order.get(d['status'], 5), d['date'], d['co'].lower()))
    json.dump(data, open(OUT / 'data.json', 'w'), ensure_ascii=False, indent=0)
    json.dump({'updated': datetime.date.today().strftime('%d %b %Y')},
              open(OUT / 'meta.json', 'w'))
    print(f'{len(data)} rows -> {OUT}/data.json')


if __name__ == '__main__':
    main()
