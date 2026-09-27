#!/usr/bin/env python3
"""
Scan a compiled resume .tex file for AI-fingerprint violations:
Tier-1 banned words, em-dash overuse, "-ing" bullet endings, and
consecutive bullets starting with the same verb.

Ports the checklist in resume_builder/support/ai_fingerprint_rules.md
into a deterministic gate script (no LLM read required).

Usage:
  python3 fingerprint_check.py output/Acme/e2e_acme_resume.tex
"""

import re
import sys
import argparse

from char_count import strip_latex, extract_items, count_em_dashes

BANNED_PHRASES = [
    "delve", "tapestry", "multifaceted", "pivotal", "robust", "seamless",
    "seamlessly", "leverage", "leveraged", "boasts", "showcase", "showcases",
    "fast-paced", "ever-evolving", "cutting-edge", "synergy", "game-changer",
    "unlock", "unlocking", "holistic", "paradigm shift",
]

EM_DASH_LIMIT = 2


def check_banned_words(rendered_text):
    """Return the list of Tier-1 banned phrases found (case-insensitive)."""
    lower = rendered_text.lower()
    return [phrase for phrase in BANNED_PHRASES if phrase in lower]


def strip_latex_comment_lines(text):
    """Drop lines that are pure LaTeX comments (first non-whitespace char
    is '%'), e.g. the template's '% ------...' divider rules. These are
    not resume content and must not feed the em-dash count."""
    return '\n'.join(
        line for line in text.splitlines() if not line.lstrip().startswith('%')
    )


def check_em_dash_count(raw_tex_text):
    """Return the em-dash count if it exceeds the limit, else 0."""
    count = count_em_dashes(strip_latex_comment_lines(raw_tex_text))
    return count if count > EM_DASH_LIMIT else 0


def check_ing_endings(rendered_bullets):
    """Return (1-based index, bullet text) for bullets whose last word ends in 'ing'."""
    flagged = []
    for i, bullet in enumerate(rendered_bullets, 1):
        words = bullet.strip().rstrip('.').split()
        if words and words[-1].lower().endswith('ing'):
            flagged.append((i, bullet))
    return flagged


def check_consecutive_same_verb(rendered_bullets):
    """Return (i, i+1, verb) for consecutive bullets sharing the same first word."""
    flagged = []
    prev_verb = None
    for i, bullet in enumerate(rendered_bullets, 1):
        words = bullet.strip().split()
        verb = words[0].lower() if words else ''
        if verb and verb == prev_verb:
            flagged.append((i - 1, i, verb))
        prev_verb = verb
    return flagged


def run_checks(tex_text):
    """Run all fingerprint checks against raw .tex text."""
    raw_items = extract_items(tex_text)
    rendered_bullets = [strip_latex(item) for item in raw_items]
    full_rendered = ' '.join(rendered_bullets)

    return {
        'banned_words': check_banned_words(full_rendered),
        'em_dash_over_limit': check_em_dash_count(tex_text),
        'ing_endings': check_ing_endings(rendered_bullets),
        'consecutive_same_verb': check_consecutive_same_verb(rendered_bullets),
    }


def has_violations(results):
    return bool(
        results['banned_words']
        or results['em_dash_over_limit']
        or results['ing_endings']
        or results['consecutive_same_verb']
    )


def format_report(results):
    lines = []
    if results['banned_words']:
        lines.append(f"BANNED WORDS: {', '.join(results['banned_words'])}")
    if results['em_dash_over_limit']:
        lines.append(f"EM-DASH COUNT: {results['em_dash_over_limit']} (limit {EM_DASH_LIMIT})")
    for i, bullet in results['ing_endings']:
        lines.append(f'BULLET {i} ENDS IN "-ing": {bullet}')
    for i, j, verb in results['consecutive_same_verb']:
        lines.append(f'BULLETS {i} & {j} BOTH START WITH "{verb}"')
    return '\n'.join(lines) if lines else 'PASS: no fingerprint violations found.'


def main():
    parser = argparse.ArgumentParser(
        description='Scan a resume .tex file for AI-fingerprint violations')
    parser.add_argument('tex_file', help='.tex file to scan')
    args = parser.parse_args()

    with open(args.tex_file) as f:
        tex_text = f.read()

    results = run_checks(tex_text)
    print(format_report(results))
    sys.exit(1 if has_violations(results) else 0)


if __name__ == '__main__':
    main()
