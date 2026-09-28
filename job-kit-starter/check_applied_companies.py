#!/usr/bin/env python3
"""
Print the set of companies already present in applications.csv (any status),
lowercased for case-insensitive dedup matching. Used by daily_scan.md step 1
instead of reading the full CSV into the LLM's context.

Usage:
  python3 check_applied_companies.py output/job-search/applications.csv
"""
import argparse
import csv
import sys


def applied_companies(csv_path):
    companies = set()
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = row.get('Company', '').strip()
            if company:
                companies.add(company.lower())
    return companies


def main():
    parser = argparse.ArgumentParser(
        description='List companies already in applications.csv')
    parser.add_argument('csv_path')
    args = parser.parse_args()

    for company in sorted(applied_companies(args.csv_path)):
        print(company)


if __name__ == '__main__':
    main()
