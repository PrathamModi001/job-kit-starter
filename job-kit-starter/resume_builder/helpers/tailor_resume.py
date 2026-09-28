#!/usr/bin/env python3
"""
tailor_resume.py — deterministic, 0-LLM JD-to-resume-draft assembler.

Given a JD, extracts keywords, selects bullets/tagline/skills per the
matching lane's bundle_data.py rules (maximizing truthful keyword
coverage within cap constraints), and writes a draft .tex +
keyword_table.json for /make-resume to review and polish.

Usage:
  python3 tailor_resume.py --jd <path> --company "<Company>" \
      [--lane backend|fullstack|ai|auto] [--out-dir output/<Company>]
"""
import argparse

import bundle_data as bd
import experience_parser as ep


def extract_jd_keywords(jd_text, all_tags, taxonomy_terms):
    jd_lower = jd_text.lower()
    direct = sorted({tag for tag in all_tags if tag.lower() in jd_lower})
    bridge = sorted({
        term.lower() for term in taxonomy_terms
        if term.lower() in jd_lower and term.lower() not in direct
    })
    return {'direct': direct, 'bridge': bridge}
