#!/usr/bin/env python3
"""
Parse resume_builder/experience/*.md files into {id: {tags, bullet|header+description}}.

Entries follow one of two shapes:
  - Experience-style: **Tags:** ... then **Bullet:** or
    **Bullet (condensed ...):** ... (condensed variant preferred when both exist).
  - Project-style: **Tags:** ... then **Header:** ... then **Description:** or
    **Description (condensed ...):** ... (condensed variant preferred when both exist).

PP1 in experience_playpower.md is a documented exception (two named variants,
no single **Bullet:** line) — this parser returns its tags only; variant
selection lives in bundle_data.py / tailor_resume.py.
"""
import re

HEADER_RE = re.compile(r'^### (\S+) — ', re.MULTILINE)
TAGS_RE = re.compile(r'\*\*Tags:\*\* (.+)')
BULLET_CONDENSED_RE = re.compile(r'\*\*Bullet \(condensed[^)]*\):\*\* (.+)')
BULLET_RE = re.compile(r'\*\*Bullet:\*\* (.+)')
HEADER_LINE_RE = re.compile(r'\*\*Header:\*\* (.+)')
DESC_CONDENSED_RE = re.compile(r'\*\*Description \(condensed[^)]*\):\*\* (.+)')
DESC_RE = re.compile(r'\*\*Description:\*\* (.+)')


def parse_experience_file(path):
    with open(path) as f:
        text = f.read()

    blocks = re.split(r'\n(?=### )', text)
    result = {}
    for block in blocks:
        m = HEADER_RE.match(block) or re.match(r'### (\S+) — ', block)
        if not m:
            continue
        bullet_id = m.group(1)

        tags_m = TAGS_RE.search(block)
        tags = [t.strip() for t in tags_m.group(1).split(',')] if tags_m else []
        entry = {'tags': tags}

        bullet_m = BULLET_CONDENSED_RE.search(block) or BULLET_RE.search(block)
        if bullet_m:
            entry['bullet'] = bullet_m.group(1).strip()

        header_m = HEADER_LINE_RE.search(block)
        if header_m:
            entry['header'] = header_m.group(1).strip()

        desc_m = DESC_CONDENSED_RE.search(block) or DESC_RE.search(block)
        if desc_m:
            entry['description'] = desc_m.group(1).strip()

        result[bullet_id] = entry
    return result
