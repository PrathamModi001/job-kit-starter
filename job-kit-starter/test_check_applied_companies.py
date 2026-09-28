"""Plain-assert test for check_applied_companies.py. Run: python3 test_check_applied_companies.py"""
import csv
import tempfile
import os

import check_applied_companies as cac


def test_applied_companies_reads_unique_company_names():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'applications.csv')
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Company', 'Role', 'Location', 'Channel', 'Comp', 'Status', 'Added',
                'Applied', 'Updated', 'Resume', 'Job URL', 'Next step', 'Personal Info Filled',
            ])
            writer.writerow(['Acme', 'SDE', '', '', '', 'Applied'] + [''] * 7)
            writer.writerow(['Acme', 'SDE 2', '', '', '', 'Skipped'] + [''] * 7)
            writer.writerow(['Beta Co', 'Backend', '', '', '', 'Blocked'] + [''] * 7)

        companies = cac.applied_companies(path)
        assert companies == {'acme', 'beta co'}


if __name__ == '__main__':
    test_applied_companies_reads_unique_company_names()
    print('PASS: test_applied_companies_reads_unique_company_names')
