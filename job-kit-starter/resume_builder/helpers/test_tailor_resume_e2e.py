#!/usr/bin/env python3
"""
End-to-end validation: run tailor_resume.py on two different real JDs and
confirm (a) both pass every existing quality gate, (b) their output
genuinely differs (the core "never reuse a resume" invariant).
Run: python3 test_tailor_resume_e2e.py
Requires: tectonic, pypdf installed.
"""
import subprocess
import sys
import tempfile
import os

import tailor_resume as tr

JD_BACKEND = """
Backend Engineer — Node.js
We're looking for a backend engineer strong in Node.js, Kafka, Redis, and
PostgreSQL to build our event-driven microservices platform on AWS.
0-2 years experience welcome.
"""

JD_FULLSTACK = """
Full-Stack Developer
Build features end-to-end across our Next.js/React frontend and Node.js/
Express backend, with PostgreSQL and Tailwind CSS. 0-3 YOE.
"""

HELPERS_DIR = os.path.dirname(os.path.abspath(__file__))


def _run_gates(tex_path):
    subprocess.run(
        ['python3', 'char_count.py', '-f', 'resume', tex_path],
        check=True, cwd=HELPERS_DIR)
    pdf_path = tex_path.replace('.tex', '.pdf')
    subprocess.run(
        ['tectonic', '-c', 'minimal', tex_path], check=True,
        cwd=os.path.dirname(tex_path) or '.')
    pages = subprocess.run(
        ['python3', '-c',
         f"import pypdf; print(len(pypdf.PdfReader('{pdf_path}').pages))"],
        capture_output=True, text=True, check=True).stdout.strip()
    assert pages == '1', f"expected 1 page, got {pages}"
    subprocess.run(
        ['python3', 'fingerprint_check.py', tex_path],
        check=True, cwd=HELPERS_DIR)


def test_two_different_jds_produce_different_resumes_and_pass_all_gates():
    with tempfile.TemporaryDirectory() as tmp:
        result_backend = tr.tailor(JD_BACKEND, 'TestCoBackend', 'backend', out_dir=tmp)
        result_fullstack = tr.tailor(JD_FULLSTACK, 'TestCoFullstack', 'fullstack', out_dir=tmp)

        with open(result_backend['tex_path']) as f:
            tex_backend = f.read()
        with open(result_fullstack['tex_path']) as f:
            tex_fullstack = f.read()
        assert tex_backend != tex_fullstack

        _run_gates(result_backend['tex_path'])
        _run_gates(result_fullstack['tex_path'])

        assert result_backend['coverage_pct'] > 0


if __name__ == '__main__':
    test_two_different_jds_produce_different_resumes_and_pass_all_gates()
    print('PASS: test_two_different_jds_produce_different_resumes_and_pass_all_gates')
