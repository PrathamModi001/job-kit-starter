# Apply-Loop Token Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic resume-bullet-selection script that maximizes truthful
ATS keyword coverage per job while cutting token cost, then restructure the daily apply
loop so gates run before tailoring and each job's tailoring/fill/submit runs in an
isolated subagent.

**Architecture:** A new `tailor_resume.py` (backed by `experience_parser.py` and
`bundle_data.py`) does JD-keyword extraction and greedy, cap-respecting bullet/tagline
selection with 0 LLM tokens, producing a draft `.tex` + `keyword_table.json`. The
existing `/make-resume` skill is trimmed to review/polish that draft instead of
generating from a cold read of all source files, then runs the same gates as today
unchanged. `daily_scan.md` is restructured so the mechanical exclusion/screener check
runs before tailoring, and each shortlisted lead is dispatched to its own subagent.

**Tech Stack:** Python 3 (stdlib only, matching existing `resume_builder/helpers/*.py`),
LaTeX/tectonic (existing), Claude Code Task/Agent tool for subagent dispatch.

**Spec:** `docs/superpowers/specs/2026-09-28-apply-loop-token-optimization-design.md`

## Global Constraints

- **Never reuse a resume.** `tailor_resume.py` always regenerates from the JD; it never
  reads or copies a prior `output/` folder's content into a new one.
- Every existing quality gate still runs per job, unchanged pass/fail semantics:
  `char_count.py` (no OVER, last 2L line ≥70% fill), `tectonic -c minimal` compile +
  1-page `pypdf` check, `fingerprint_check.py` (exit 0), ATS coverage ≥75% (or an
  honestly-reported lower number, never inflated).
- Bullet text is **COPY-EXACT** — no script or LLM step may alter a number, tool name,
  or verb. The only allowed edit is trimming a trailing clause to fit budget.
- Tagline tool tokens must come only from the matching bundle's Approved Pool.
- New helper scripts are stdlib-only Python, plain-assert tests run via
  `python3 test_X.py` (matches `test_fingerprint_check.py` convention) — no pytest
  dependency introduced.
- `resume_builder/bundles/bundle_<lane>.md` and `resume_builder/experience/*.md` remain
  the human-edited source of truth. `bundle_data.py` mirrors their structured data
  (priority ranks, caps, approved pools) for reliable parsing — every entry in it must
  carry a comment naming the source `.md` file/section so a human editing the bundle
  remembers to update both.

## Review Focus

- A bullet-selection swap violates a bundle cap rule (e.g. both PP2 and PP3 selected in
  the Backend lane) — Task 4 tests this directly.
- The tagline builder inserts a tool not in the bundle's Approved Pool (hallucinated
  tool) — Task 5 tests this directly.
- The renderer mutates copy-exact bullet text (changes a number/tool/verb) instead of
  reproducing it verbatim — Task 7 tests this directly.
- Two different JDs/companies produce identical or near-identical resume output
  (the "reused resume" failure this whole project exists to prevent) — Task 8's
  end-to-end test asserts the two sample-JD outputs differ.
- The wrong PP1 variant is used for a lane (Variant B full-stack text on a Backend
  resume, or vice versa) — Task 2 tests this directly.

---

### Task 1: Experience file parser

**Files:**
- Create: `resume_builder/helpers/experience_parser.py`
- Test: `resume_builder/helpers/test_experience_parser.py`

**Interfaces:**
- Produces: `parse_experience_file(path) -> dict[str, dict]` — keys are bullet IDs
  (`"C1"`, `"PP4"`, `"PJ1"`, ...), values have `tags: list[str]` always, plus
  `bullet: str` for experience-style entries or `header: str` + `description: str` for
  project-style entries. Later tasks import this from `resume_builder.helpers`.

- [ ] **Step 1: Write failing tests**

```python
# resume_builder/helpers/test_experience_parser.py
"""Plain-assert tests for experience_parser.py. Run: python3 test_experience_parser.py"""
import experience_parser as ep

C3IHUB = 'experience_c3ihub.md'
PLAYPOWER = 'experience_playpower.md'
PROJECTS = 'experience_projects.md'


def test_parses_c3ihub_bullet_entries():
    entries = ep.parse_experience_file(f'../experience/{C3IHUB}')
    assert 'C1' in entries
    assert entries['C1']['tags'] == [
        'node', 'express', 'mongodb', 'redis', 'socketio', 'microservices',
        'scale', 'uptime', 'backend-core'
    ]
    assert entries['C1']['bullet'].startswith('Architected core LMS backend')


def test_uses_condensed_bullet_variant_when_present():
    entries = ep.parse_experience_file(f'../experience/{C3IHUB}')
    # C6 has both a condensed and a full/uncondensed variant; parser must
    # pick the condensed one (the one actually usable on a 2-line bullet).
    assert entries['C6']['bullet'].startswith(
        'Built real-time collaborative round engine handling 2,000+'
    )
    assert 'Full/uncondensed' not in entries['C6']['bullet']


def test_parses_project_entries_with_header_and_description():
    entries = ep.parse_experience_file(f'../experience/{PROJECTS}')
    assert entries['PJ1']['tags'] == [
        'kafka', 'redis-streams', 'fastapi', 'postgresql', 'event-driven', 'hackathon'
    ]
    assert entries['PJ1']['header'].startswith('Autonomous Invoice Processing Platform')
    assert entries['PJ1']['description'].startswith('Automated multi-channel invoice')


def test_uses_condensed_description_variant_when_present():
    entries = ep.parse_experience_file(f'../experience/{PROJECTS}')
    assert entries['PJ2']['description'].startswith('GitOps platform automating')


def test_playpower_pp1_has_tags_but_no_single_bullet():
    # PP1 is a documented special case (two named variants, handled by
    # bundle_data.py, not by this generic parser) — tags must still parse.
    entries = ep.parse_experience_file(f'../experience/{PLAYPOWER}')
    assert 'PP1' in entries
    assert 'nextjs' in entries['PP1']['tags']


def test_parses_pp4_bullet_normally():
    entries = ep.parse_experience_file(f'../experience/{PLAYPOWER}')
    assert entries['PP4']['bullet'].startswith('Reduced release cycle time by 65%')


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f'PASS: {name}')
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd resume_builder/helpers && python3 test_experience_parser.py`
Expected: `ModuleNotFoundError: No module named 'experience_parser'`

- [ ] **Step 3: Implement the parser**

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd resume_builder/helpers && python3 test_experience_parser.py`
Expected: 6 `PASS:` lines, no errors.

- [ ] **Step 5: Commit**

```bash
git add resume_builder/helpers/experience_parser.py resume_builder/helpers/test_experience_parser.py
git commit -m "feat: add experience_parser.py for deterministic bullet/tag extraction"
```

---

### Task 2: Bundle structured data

**Files:**
- Create: `resume_builder/helpers/bundle_data.py`
- Test: `resume_builder/helpers/test_bundle_data.py`

**Interfaces:**
- Consumes: `experience_parser.parse_experience_file` (Task 1) — used only in this
  task's tests, to cross-check IDs referenced in `bundle_data.py` actually exist.
- Produces: `LANES: dict[str, dict]` keyed `"backend"`, `"fullstack"`, `"ai"`, each value:
  ```python
  {
      'label': str,                       # tagline's [Lane Label] segment
      'approved_pool': list[str],         # tagline tool pool, JD-appearance order wins
      'default_tool_order': list[str],    # fallback fill order if <4 JD matches
      'summary': str,                     # copy-exact bundle Summary block
      'c3ihub_matrix': list[tuple],       # (rank, id, tier) — tier in TIER_ORDER keys
      'c3ihub_pick_count': int,
      'playpower_matrix': list[tuple],
      'playpower_pick_count': int,
      'playpower_caps': list[tuple],      # (frozenset(ids), max_count)
      'projects_matrix': list[tuple],
      'projects_pick_count': int,
      'skills_group_order': list[str],
  }
  ```
  Also produces `TIER_ORDER: dict[str, int]` and `PP1_VARIANTS: dict[str, str]`
  (`"backend"`/`"ai"` -> Variant A text, `"fullstack"` -> Variant B text, copy-exact
  from `experience_playpower.md`).

- [ ] **Step 1: Write failing tests**

```python
# resume_builder/helpers/test_bundle_data.py
"""Plain-assert tests for bundle_data.py. Run: python3 test_bundle_data.py"""
import bundle_data as bd
import experience_parser as ep


def test_all_lanes_present():
    assert set(bd.LANES.keys()) == {'backend', 'fullstack', 'ai'}


def test_backend_approved_pool_matches_bundle_md():
    pool = bd.LANES['backend']['approved_pool']
    assert pool == [
        'Node.js', 'Express.js', 'Kafka', 'Redis', 'MongoDB', 'PostgreSQL',
        'AWS', 'Docker', 'Kubernetes', 'Microservices', 'WebSocket', 'OpenTelemetry',
    ]


def test_backend_playpower_cap_rule_present():
    caps = bd.LANES['backend']['playpower_caps']
    assert (frozenset({'PP2', 'PP3'}), 1) in caps


def test_ai_lane_has_no_pp2_pp3_cap():
    caps = bd.LANES['ai']['playpower_caps']
    assert not any({'PP2', 'PP3'} <= set(cap_set) for cap_set, _ in caps)


def test_pp1_variants_are_copy_exact_and_distinct():
    assert bd.PP1_VARIANTS['backend'].startswith('Developed AI tutoring platform')
    assert bd.PP1_VARIANTS['fullstack'].startswith('Built AI tutoring platform')
    assert bd.PP1_VARIANTS['ai'] == bd.PP1_VARIANTS['backend']


def test_every_matrix_id_exists_in_parsed_experience_files():
    c3ihub = ep.parse_experience_file('../experience/experience_c3ihub.md')
    playpower = ep.parse_experience_file('../experience/experience_playpower.md')
    projects = ep.parse_experience_file('../experience/experience_projects.md')
    for lane in bd.LANES.values():
        for _, bullet_id, _ in lane['c3ihub_matrix']:
            assert bullet_id in c3ihub, bullet_id
        for _, bullet_id, _ in lane['playpower_matrix']:
            assert bullet_id in playpower, bullet_id
        for _, bullet_id, _ in lane['projects_matrix']:
            assert bullet_id in projects, bullet_id


def test_c5_defaults_high_for_backend_and_fullstack():
    # hiring-manager audit rule: C5 defaults HIGH for Backend/Full-Stack lanes.
    for lane_name in ('backend', 'fullstack'):
        tiers = {bid: tier for _, bid, tier in bd.LANES[lane_name]['c3ihub_matrix']}
        assert tiers['C5'] == 'HIGH', lane_name


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f'PASS: {name}')
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd resume_builder/helpers && python3 test_bundle_data.py`
Expected: `ModuleNotFoundError: No module named 'bundle_data'`

- [ ] **Step 3: Implement bundle_data.py**

Transcribe each `resume_builder/bundles/bundle_<lane>.md` by hand into this structure —
every literal value here must match its source `.md` file exactly (tool names, ranks,
cap rules). Cross-reference source: `resume_builder/bundles/bundle_backend.md`,
`bundle_fullstack.md`, `bundle_ai.md`.

```python
#!/usr/bin/env python3
"""
Structured mirror of resume_builder/bundles/bundle_<lane>.md, used by
tailor_resume.py for deterministic bullet/tagline selection.

IMPORTANT: this file duplicates data from the bundle .md files by design
(markdown priority-matrix tables mix free-text rationale into cells and
aren't reliably machine-parseable). If you edit a bundle_<lane>.md file's
Approved Pool, Priority Matrix, or cap rules, update the matching entry
here in the same change — test_bundle_data.py checks structural
consistency (IDs exist) but cannot catch a stale rank/cap silently.
"""

TIER_ORDER = {'HIGH': 0, 'MEDIUM-HIGH': 1, 'MEDIUM': 2, 'LOW': 3}

# Source: experience_playpower.md PP1 — two approved variants, copy-exact.
PP1_VARIANTS = {
    'backend': (
        'Developed AI tutoring platform using FastAPI microservices and '
        'Next.js, supporting 500+ concurrent WebSocket sessions with '
        'sub-100ms response times.'
    ),
    'ai': (
        'Developed AI tutoring platform using FastAPI microservices and '
        'Next.js, supporting 500+ concurrent WebSocket sessions with '
        'sub-100ms response times.'
    ),
    'fullstack': (
        'Built AI tutoring platform using Next.js (SSR/ISR, React Server '
        'Components) and FastAPI microservices, supporting 500+ concurrent '
        'WebSocket sessions at sub-100ms response times.'
    ),
}

LANES = {
    # Source: resume_builder/bundles/bundle_backend.md
    'backend': {
        'label': 'Backend & Distributed Systems',
        'approved_pool': [
            'Node.js', 'Express.js', 'Kafka', 'Redis', 'MongoDB', 'PostgreSQL',
            'AWS', 'Docker', 'Kubernetes', 'Microservices', 'WebSocket', 'OpenTelemetry',
        ],
        'default_tool_order': ['Node.js', 'Kafka', 'Redis', 'AWS', 'PostgreSQL'],
        'summary': (
            'Backend-focused software engineer with 2+ years in production. Led '
            'backend development of an event-driven LMS platform serving 50K+ '
            'users at C3iHub (IIT Kanpur), spanning microservices, distributed '
            'tracing, and cloud infrastructure. Strong in Node.js, Kafka, Redis, '
            'and AWS, with a track record of cutting latency and infrastructure '
            'cost while scaling systems to 10,000+ concurrent connections.'
        ),
        'c3ihub_matrix': [
            (1, 'C1', 'HIGH'), (2, 'C3', 'HIGH'), (3, 'C4', 'HIGH'), (4, 'C5', 'HIGH'),
            (5, 'C2', 'MEDIUM'), (6, 'C6', 'LOW'),
        ],
        'c3ihub_pick_count': 4,
        'playpower_matrix': [
            (1, 'PP4', 'HIGH'), (2, 'PP1', 'MEDIUM'), (3, 'PP2', 'LOW'), (4, 'PP3', 'LOW'),
        ],
        'playpower_pick_count': 3,
        'playpower_caps': [(frozenset({'PP2', 'PP3'}), 1)],
        'projects_matrix': [
            (1, 'PJ1', 'HIGH'), (2, 'PJ2', 'HIGH'), (3, 'PJ3', 'LOW'),
        ],
        'projects_pick_count': 2,
        'skills_group_order': [
            'Backend', 'Databases', 'Messaging', 'Cloud, DevOps & Observability',
            'Architecture',
        ],
    },
    # Source: resume_builder/bundles/bundle_fullstack.md
    'fullstack': {
        'label': 'Full-Stack Development',
        'approved_pool': [
            'Node.js', 'Next.js', 'React', 'Express.js', 'TypeScript',
            'PostgreSQL', 'MongoDB', 'AWS', 'Tailwind CSS',
        ],
        'default_tool_order': ['Node.js', 'Next.js', 'React', 'PostgreSQL'],
        'summary': (
            'Full-stack software engineer with 2+ years in production, owning '
            'systems end-to-end across backend, frontend, and DevOps. Built a '
            'scaled multi-tenant SaaS platform onboarding 10K+ users at C3iHub '
            '(IIT Kanpur) and an AI-driven Next.js product at Playpower Labs, '
            'spanning Node.js/Express backends, React/Next.js frontends, and '
            'event-driven infrastructure (Kafka, Redis).'
        ),
        'c3ihub_matrix': [
            (1, 'C5', 'HIGH'), (2, 'C1', 'HIGH'), (3, 'C3', 'MEDIUM-HIGH'),
            (4, 'C6', 'MEDIUM'), (5, 'C2', 'LOW'), (6, 'C4', 'LOW'),
        ],
        'c3ihub_pick_count': 4,
        'playpower_matrix': [
            (1, 'PP1', 'HIGH'), (2, 'PP4', 'HIGH'), (3, 'PP2', 'LOW'), (4, 'PP3', 'LOW'),
        ],
        'playpower_pick_count': 3,
        'playpower_caps': [(frozenset({'PP2', 'PP3'}), 1)],
        'projects_matrix': [
            (1, 'PJ1', 'HIGH'), (2, 'PJ3', 'MEDIUM'), (3, 'PJ2', 'MEDIUM'),
        ],
        'projects_pick_count': 2,
        'skills_group_order': [
            'Frontend', 'Backend', 'Databases', 'Messaging', 'Cloud & DevOps',
        ],
    },
    # Source: resume_builder/bundles/bundle_ai.md
    'ai': {
        'label': 'Backend & Agentic AI Systems',
        'approved_pool': [
            'Python', 'LangChain', 'LangGraph', 'Model Context Protocol (MCP)',
            'RAG', 'Qdrant', 'ChromaDB', 'Kafka', 'FastAPI',
        ],
        'default_tool_order': ['Python', 'LangChain', 'MCP', 'Kafka'],
        'summary': (
            'Software Engineer with 2+ years building production AI systems '
            '(LangChain, LangGraph, MCP) and high-throughput backend '
            'infrastructure (Kafka, MongoDB, AWS), achieving 99.9% uptime on '
            'RAG-driven platforms at IIT Kanpur and Playpower Labs.'
        ),
        'c3ihub_matrix': [
            (1, 'C1', 'HIGH'), (2, 'C3', 'HIGH'), (3, 'C2', 'MEDIUM-HIGH'),
            (4, 'C4', 'MEDIUM'), (5, 'C5', 'MEDIUM'), (6, 'C6', 'LOW'),
        ],
        'c3ihub_pick_count': 4,
        'playpower_matrix': [
            (1, 'PP2', 'HIGH'), (2, 'PP3', 'HIGH'), (3, 'PP1', 'MEDIUM-HIGH'),
            (4, 'PP4', 'MEDIUM'),
        ],
        'playpower_pick_count': 4,
        'playpower_caps': [],  # AI lane: the PP2/PP3 cap explicitly does not apply here.
        'projects_matrix': [
            (1, 'PJ3', 'HIGH'), (2, 'PJ2', 'HIGH'), (3, 'PJ1', 'LOW'),
        ],
        'projects_pick_count': 2,
        'skills_group_order': [
            'AI & Agent Frameworks', 'Languages & Backend', 'Databases & Messaging',
            'Cloud, DevOps & Observability',
        ],
    },
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd resume_builder/helpers && python3 test_bundle_data.py`
Expected: 7 `PASS:` lines, no errors.

- [ ] **Step 5: Commit**

```bash
git add resume_builder/helpers/bundle_data.py resume_builder/helpers/test_bundle_data.py
git commit -m "feat: add bundle_data.py structured lane data for deterministic tailoring"
```

---

### Task 3: JD keyword extraction

**Files:**
- Create: `resume_builder/helpers/tailor_resume.py` (this task starts the file)
- Test: `resume_builder/helpers/test_tailor_resume.py` (this task starts the file)

**Interfaces:**
- Consumes: nothing from earlier tasks yet (pure text function).
- Produces: `extract_jd_keywords(jd_text, all_tags, taxonomy_terms) -> dict` with keys
  `'direct': list[str]` (lowercase tags found verbatim in JD text) and
  `'bridge': list[str]` (lowercase taxonomy terms found in JD text but not already in
  `direct`). Later tasks (6, 7) consume this return shape.

- [ ] **Step 1: Write failing tests**

```python
# resume_builder/helpers/test_tailor_resume.py
"""Plain-assert tests for tailor_resume.py. Run: python3 test_tailor_resume.py"""
import tailor_resume as tr

ALL_TAGS = ['node', 'kafka', 'redis', 'postgresql', 'microservices', 'docker']
TAXONOMY_TERMS = ['TypeScript', 'GraphQL', 'Terraform', 'Kafka', 'Redis']


def test_direct_keywords_found_case_insensitive():
    jd = "We use Node.js, Kafka, and Redis heavily in our backend."
    result = tr.extract_jd_keywords(jd, ALL_TAGS, TAXONOMY_TERMS)
    assert 'kafka' in result['direct']
    assert 'redis' in result['direct']


def test_direct_excludes_untagged_terms():
    jd = "We use Node.js and Kafka."
    result = tr.extract_jd_keywords(jd, ALL_TAGS, TAXONOMY_TERMS)
    assert 'docker' not in result['direct']


def test_bridge_finds_taxonomy_terms_not_in_direct():
    jd = "Experience with GraphQL and Terraform is a plus."
    result = tr.extract_jd_keywords(jd, ALL_TAGS, TAXONOMY_TERMS)
    assert 'graphql' in result['bridge']
    assert 'terraform' in result['bridge']


def test_bridge_excludes_terms_already_direct():
    jd = "Kafka experience required."
    result = tr.extract_jd_keywords(jd, ALL_TAGS, TAXONOMY_TERMS)
    assert 'kafka' in result['direct']
    assert 'kafka' not in result['bridge']


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f'PASS: {name}')
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`
Expected: `ModuleNotFoundError: No module named 'tailor_resume'`

- [ ] **Step 3: Implement keyword extraction**

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`
Expected: 4 `PASS:` lines, no errors.

- [ ] **Step 5: Commit**

```bash
git add resume_builder/helpers/tailor_resume.py resume_builder/helpers/test_tailor_resume.py
git commit -m "feat: add JD keyword extraction to tailor_resume.py"
```

---

### Task 4: Bullet scoring and cap-respecting selection

**Files:**
- Modify: `resume_builder/helpers/tailor_resume.py`
- Modify: `resume_builder/helpers/test_tailor_resume.py`

**Interfaces:**
- Consumes: `bundle_data.TIER_ORDER` (Task 2), `experience_parser.parse_experience_file`
  output shape (Task 1).
- Produces: `score_bullet(bullet_id, bullets_by_id, jd_keyword_set) -> int` and
  `select_bullets(matrix, bullets_by_id, jd_keyword_set, pick_count, caps=None) -> list[str]`
  (ordered list of selected bullet IDs, highest-relevance first). Task 8 (CLI/e2e)
  consumes `select_bullets`.

- [ ] **Step 1: Write failing tests**

```python
# append to resume_builder/helpers/test_tailor_resume.py

BULLETS_BY_ID = {
    'C1': {'tags': ['node', 'express', 'mongodb', 'redis', 'scale'], 'bullet': 'b1'},
    'C2': {'tags': ['aws', 's3', 'performance'], 'bullet': 'b2'},
    'C3': {'tags': ['kafka', 'bullmq', 'event-driven'], 'bullet': 'b3'},
    'C4': {'tags': ['opentelemetry', 'observability'], 'bullet': 'b4'},
    'C5': {'tags': ['leadership', 'saas', 'scale'], 'bullet': 'b5'},
    'C6': {'tags': ['websocket', 'django-channels'], 'bullet': 'b6'},
    'PP2': {'tags': ['rag', 'chromadb', 'ai'], 'bullet': 'pp2'},
    'PP3': {'tags': ['rag', 'embeddings', 'ai'], 'bullet': 'pp3'},
}

BACKEND_C3IHUB_MATRIX = bd.LANES['backend']['c3ihub_matrix']


def test_score_counts_tag_overlap():
    jd_keywords = {'node', 'redis', 'scale', 'kafka'}
    assert tr.score_bullet('C1', BULLETS_BY_ID, jd_keywords) == 3  # node, redis, scale
    assert tr.score_bullet('C3', BULLETS_BY_ID, jd_keywords) == 1  # kafka


def test_select_bullets_respects_default_rank_order_with_no_jd_signal():
    selected = tr.select_bullets(BACKEND_C3IHUB_MATRIX, BULLETS_BY_ID, set(), pick_count=4)
    # no JD keyword signal -> falls back to default matrix rank order (C1,C3,C4,C5)
    assert selected == ['C1', 'C3', 'C4', 'C5']


def test_select_bullets_swaps_in_higher_scoring_candidate():
    # C2 (rank 5, MEDIUM) strongly matches the JD; C4 (rank 3, HIGH) doesn't
    # match at all -> greedy improvement should swap C2 in over C4.
    jd_keywords = {'aws', 's3', 'performance'}
    selected = tr.select_bullets(BACKEND_C3IHUB_MATRIX, BULLETS_BY_ID, jd_keywords, pick_count=4)
    assert 'C2' in selected
    assert len(selected) == 4


def test_select_bullets_respects_cap_rule():
    matrix = [(1, 'PP2', 'HIGH'), (2, 'PP3', 'HIGH')]
    caps = [(frozenset({'PP2', 'PP3'}), 1)]
    jd_keywords = {'rag', 'ai', 'chromadb', 'embeddings'}
    selected = tr.select_bullets(matrix, BULLETS_BY_ID, jd_keywords, pick_count=2, caps=caps)
    assert len(selected) == 1
    assert set(selected) <= {'PP2', 'PP3'}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`
Expected: `AttributeError: module 'tailor_resume' has no attribute 'score_bullet'`

- [ ] **Step 3: Implement scoring and selection**

```python
# append to resume_builder/helpers/tailor_resume.py

def score_bullet(bullet_id, bullets_by_id, jd_keyword_set):
    tags = set(bullets_by_id[bullet_id]['tags'])
    return len(tags & jd_keyword_set)


def _violates_cap(current_ids, candidate_id, caps):
    for cap_set, max_count in caps:
        if candidate_id not in cap_set:
            continue
        count = len([i for i in current_ids if i in cap_set])
        if candidate_id not in current_ids and count >= max_count:
            return True
    return False


def select_bullets(matrix, bullets_by_id, jd_keyword_set, pick_count, caps=None):
    caps = caps or []
    ids_in_rank_order = [bullet_id for _, bullet_id, _ in matrix]
    tier_of = {bullet_id: tier for _, bullet_id, tier in matrix}

    selected = []
    for bullet_id in ids_in_rank_order:
        if len(selected) >= pick_count:
            break
        if _violates_cap(selected, bullet_id, caps):
            continue
        selected.append(bullet_id)

    improved = True
    while improved and selected:
        improved = False
        worst = min(selected, key=lambda bid: score_bullet(bid, bullets_by_id, jd_keyword_set))
        worst_score = score_bullet(worst, bullets_by_id, jd_keyword_set)
        worst_tier = bd.TIER_ORDER.get(tier_of.get(worst, 'LOW'), 3)
        for bullet_id in ids_in_rank_order:
            if bullet_id in selected:
                continue
            candidate_tier = bd.TIER_ORDER.get(tier_of.get(bullet_id, 'LOW'), 3)
            candidate_score = score_bullet(bullet_id, bullets_by_id, jd_keyword_set)
            if candidate_tier <= worst_tier + 1 and candidate_score > worst_score:
                trial = [bullet_id if x == worst else x for x in selected]
                if not _violates_cap([x for x in trial if x != bullet_id], bullet_id, caps):
                    selected = trial
                    improved = True
                    break
    return selected
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`
Expected: all `PASS:` lines including the 4 new ones, no errors.

- [ ] **Step 5: Commit**

```bash
git add resume_builder/helpers/tailor_resume.py resume_builder/helpers/test_tailor_resume.py
git commit -m "feat: add cap-respecting greedy bullet selection to tailor_resume.py"
```

---

### Task 5: Tagline builder

**Files:**
- Modify: `resume_builder/helpers/tailor_resume.py`
- Modify: `resume_builder/helpers/test_tailor_resume.py`

**Interfaces:**
- Consumes: a lane dict from `bundle_data.LANES` (Task 2) — reads `approved_pool`,
  `default_tool_order`, `label`.
- Produces: `build_tagline(lane) -> str` where `lane` also carries the JD text under
  key `'_jd_text'` set by the caller (Task 8 wires this). To keep the function pure and
  testable, it actually takes `(approved_pool, default_tool_order, label, jd_text)`.

- [ ] **Step 1: Write failing tests**

```python
# append to resume_builder/helpers/test_tailor_resume.py

def test_tagline_picks_tools_in_jd_appearance_order():
    pool = ['Node.js', 'Kafka', 'Redis', 'AWS', 'PostgreSQL']
    jd = "You'll work with Redis and Kafka daily, occasionally touching AWS."
    tagline = tr.build_tagline(pool, ['Node.js', 'Kafka', 'Redis', 'AWS', 'PostgreSQL'],
                                'Backend & Distributed Systems', jd)
    assert tagline == 'Software Engineer | Backend & Distributed Systems | Redis, Kafka, AWS, Node.js'


def test_tagline_fills_remaining_slots_from_default_order():
    pool = ['Node.js', 'Kafka', 'Redis', 'AWS', 'PostgreSQL']
    jd = "You'll work with Kafka."
    tagline = tr.build_tagline(pool, ['Node.js', 'Kafka', 'Redis', 'AWS', 'PostgreSQL'],
                                'Backend & Distributed Systems', jd)
    assert tagline == 'Software Engineer | Backend & Distributed Systems | Kafka, Node.js, Redis, AWS'


def test_tagline_never_inserts_tool_outside_approved_pool():
    pool = ['Node.js', 'Kafka']
    jd = "You'll work with Java and Spring Boot."  # neither in pool
    tagline = tr.build_tagline(pool, ['Node.js', 'Kafka'], 'Backend', jd)
    assert 'Java' not in tagline
    assert 'Spring' not in tagline
    for tool in ('Node.js', 'Kafka'):
        assert tool in tagline
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`
Expected: `AttributeError: module 'tailor_resume' has no attribute 'build_tagline'`

- [ ] **Step 3: Implement tagline builder**

```python
# append to resume_builder/helpers/tailor_resume.py

def build_tagline(approved_pool, default_tool_order, label, jd_text):
    jd_lower = jd_text.lower()
    matches = []
    for tool in approved_pool:
        idx = jd_lower.find(tool.lower())
        if idx != -1:
            matches.append((idx, tool))
    matches.sort(key=lambda pair: pair[0])
    tools = [tool for _, tool in matches][:4]
    for tool in default_tool_order:
        if len(tools) == 4:
            break
        if tool not in tools:
            tools.append(tool)
    return f"Software Engineer | {label} | " + ", ".join(tools[:4])
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`
Expected: all `PASS:` lines including the 3 new ones, no errors.

- [ ] **Step 5: Commit**

```bash
git add resume_builder/helpers/tailor_resume.py resume_builder/helpers/test_tailor_resume.py
git commit -m "feat: add approved-pool-only tagline builder to tailor_resume.py"
```

---

### Task 6: Coverage computation and keyword_table.json

**Files:**
- Modify: `resume_builder/helpers/tailor_resume.py`
- Modify: `resume_builder/helpers/test_tailor_resume.py`

**Interfaces:**
- Consumes: the `dict` shape produced by `extract_jd_keywords` (Task 3).
- Produces: `compute_coverage(jd_keywords, resume_text) -> float` (percentage, one
  decimal) and `write_keyword_table(path, jd_keywords, coverage_pct)` (writes JSON).
  Task 8 calls both after rendering the draft `.tex`.

- [ ] **Step 1: Write failing tests**

```python
# append to resume_builder/helpers/test_tailor_resume.py
import json
import os
import tempfile


def test_compute_coverage_counts_matched_terms():
    jd_keywords = {'direct': ['kafka', 'redis'], 'bridge': ['graphql']}
    resume_text = "Built systems using Kafka and Redis extensively."
    coverage = tr.compute_coverage(jd_keywords, resume_text)
    assert coverage == round(100 * 2 / 3, 1)


def test_compute_coverage_zero_terms_returns_zero():
    assert tr.compute_coverage({'direct': [], 'bridge': []}, "anything") == 0.0


def test_write_keyword_table_produces_valid_json():
    jd_keywords = {'direct': ['kafka'], 'bridge': ['graphql']}
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'keyword_table.json')
        tr.write_keyword_table(path, jd_keywords, 87.5)
        with open(path) as f:
            data = json.load(f)
        assert data['direct'] == ['kafka']
        assert data['bridge'] == ['graphql']
        assert data['coverage_pct'] == 87.5
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`
Expected: `AttributeError: module 'tailor_resume' has no attribute 'compute_coverage'`

- [ ] **Step 3: Implement coverage + JSON writer**

```python
# append to resume_builder/helpers/tailor_resume.py
import json


def compute_coverage(jd_keywords, resume_text):
    all_terms = jd_keywords['direct'] + jd_keywords['bridge']
    if not all_terms:
        return 0.0
    resume_lower = resume_text.lower()
    matched = [term for term in all_terms if term in resume_lower]
    return round(100 * len(matched) / len(all_terms), 1)


def write_keyword_table(path, jd_keywords, coverage_pct):
    data = dict(jd_keywords)
    data['coverage_pct'] = coverage_pct
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`
Expected: all `PASS:` lines including the 3 new ones, no errors.

- [ ] **Step 5: Commit**

```bash
git add resume_builder/helpers/tailor_resume.py resume_builder/helpers/test_tailor_resume.py
git commit -m "feat: add ATS coverage computation and keyword_table.json writer"
```

---

### Task 7: Template renderer (FIXED facts + GENERATE substitution)

**Files:**
- Modify: `resume_builder/helpers/tailor_resume.py`
- Modify: `resume_builder/helpers/test_tailor_resume.py`

**Interfaces:**
- Consumes: `resume_builder/templates/swe_resume_template.tex` (read from disk),
  `bundle_data.LANES[...]['skills_group_order']` (Task 2), skills-taxonomy group
  contents (hardcoded here — see note in Step 3), and selected-bullet text from
  `experience_parser` entries.
- Produces: `render_resume_tex(template_path, fixed_facts, tagline, summary,
  skills_groups, c3ihub_bullets, playpower_bullets, projects) -> str` (the filled
  `.tex` content, string) and `FIXED_FACTS` (module-level dict, copy-exact from
  `config.md` + experience files' FIXED headers). Task 8 calls `render_resume_tex` and
  writes its return value to disk.

- [ ] **Step 1: Write failing tests**

```python
# append to resume_builder/helpers/test_tailor_resume.py

TEMPLATE_PATH = '../templates/swe_resume_template.tex'


def test_render_produces_no_leftover_generate_markers():
    rendered = tr.render_resume_tex(
        TEMPLATE_PATH, tr.FIXED_FACTS,
        tagline='Software Engineer | Backend & Distributed Systems | Node.js, Kafka, Redis, AWS',
        summary='Backend-focused software engineer with 2+ years in production.',
        skills_groups=[
            ('Backend', 'Node.js, Express.js, FastAPI'),
            ('Databases', 'PostgreSQL, MongoDB, Redis'),
            ('Messaging', 'Kafka, BullMQ'),
            ('Cloud, DevOps & Observability', 'AWS, Docker'),
            ('Architecture', 'Microservices, System Design'),
        ],
        c3ihub_bullets=['Bullet one text.', 'Bullet two text.', 'Bullet three text.', 'Bullet four text.'],
        playpower_bullets=['PP bullet one.', 'PP bullet two.', 'PP bullet three.'],
        projects=[
            ('Project One', 'Tool A, Tool B', 'Hackathon Winner', 'Project one description.'),
            ('Project Two', 'Tool C, Tool D', '', 'Project two description.'),
        ],
    )
    assert '[GENERATE' not in rendered
    assert '[FIXED' not in rendered


def test_render_reproduces_bullet_text_verbatim():
    bullet_text = 'A very specific bullet with the number 12345.'
    rendered = tr.render_resume_tex(
        TEMPLATE_PATH, tr.FIXED_FACTS,
        tagline='Software Engineer | Backend & Distributed Systems | Node.js, Kafka, Redis, AWS',
        summary='Summary text.',
        skills_groups=[('G1', 's1'), ('G2', 's2'), ('G3', 's3'), ('G4', 's4'), ('G5', 's5')],
        c3ihub_bullets=[bullet_text, 'b2', 'b3', 'b4'],
        playpower_bullets=['b5', 'b6', 'b7'],
        projects=[('P1', 'T1', '', 'd1'), ('P2', 'T2', '', 'd2')],
    )
    assert bullet_text in rendered


def test_fixed_facts_matches_config_md():
    assert tr.FIXED_FACTS['name'] == 'Pratham Modi'
    assert tr.FIXED_FACTS['email'] == 'prathammodi001@gmail.com'
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`
Expected: `AttributeError: module 'tailor_resume' has no attribute 'render_resume_tex'`

- [ ] **Step 3: Implement the renderer**

```python
# append to resume_builder/helpers/tailor_resume.py

# Source: config.md Personal Info + experience_c3ihub.md / experience_playpower.md
# FIXED headers + SKILL_PROFILE.md Education. Update both places together.
FIXED_FACTS = {
    'name': 'Pratham Modi',
    'email': 'prathammodi001@gmail.com',
    'phone': '+91-9033393729',
    'location': 'Koramangala, Bengaluru, India',
    'github_url': 'https://github.com/PrathamModi001',
    'github_handle': 'github.com/PrathamModi001',
    'linkedin_url': 'https://www.linkedin.com/in/prathammodii001/',
    'linkedin_handle': 'linkedin.com/in/prathammodii001',
    'c3ihub_dates': 'Jul 2025 -- Present',
    'c3ihub_title': 'Software Development Engineer',
    'c3ihub_location': 'Kanpur, India',
    'playpower_dates': 'Nov 2024 -- Jun 2025',
    'playpower_title': 'Software Development Engineer',
    'playpower_location': 'Remote',
    'degree': 'B.Tech, Computer Science and Engineering',
    'education_dates': '2021 -- 2025',
    'institution': 'Indian Institute of Information Technology',
    'gpa': '9.20/10.0',
}


def _replace_first(text, marker, value):
    return text.replace(marker, value, 1)


def render_resume_tex(template_path, facts, tagline, summary, skills_groups,
                       c3ihub_bullets, playpower_bullets, projects):
    with open(template_path) as f:
        text = f.read()

    text = _replace_first(text, '[FIXED: Full Name]', facts['name'])
    text = _replace_first(text, '[FIXED: email]', facts['email'])
    text = _replace_first(text, '[FIXED: phone]', facts['phone'])
    text = _replace_first(text, '[FIXED: location]', facts['location'])
    text = _replace_first(text, '[FIXED: GitHub URL]', facts['github_url'])
    text = _replace_first(text, '[FIXED: github.com/handle]', facts['github_handle'])
    text = _replace_first(text, '[FIXED: LinkedIn URL]', facts['linkedin_url'])
    text = _replace_first(text, '[FIXED: linkedin.com/in/handle]', facts['linkedin_handle'])
    text = _replace_first(text, '[GENERATE: Tagline]', tagline)
    text = _replace_first(
        text, '[GENERATE: Summary — copied from bundle_<lane>.md Summary block]', summary)

    for name, skills in skills_groups:
        text = _replace_first(text, '[GENERATE: Group 1 Name]', name) if 'Group 1' in text else text
        break
    # Skills groups substituted positionally, one GENERATE pair per group.
    for i, (name, skills) in enumerate(skills_groups, 1):
        text = _replace_first(text, f'[GENERATE: Group {i} Name]', name)
        text = _replace_first(text, '[GENERATE: skills, comma-separated]', skills)

    text = _replace_first(text, '[FIXED: Company 1, Institution]', 'C3iHub, IIT Kanpur')
    text = _replace_first(text, '[FIXED: Start -- End]', facts['c3ihub_dates'])
    text = _replace_first(text, '[FIXED: Title]', facts['c3ihub_title'])
    text = _replace_first(text, '[FIXED: Location]', facts['c3ihub_location'])
    text = _replace_first(
        text, '[GENERATE: Bullet — copy-exact from experience file, by ID]', c3ihub_bullets[0])
    for bullet in c3ihub_bullets[1:]:
        text = _replace_first(text, '[GENERATE: Bullet]', bullet)

    text = _replace_first(text, '[FIXED: Company 2]', 'Playpower Labs')
    text = _replace_first(text, '[FIXED: Start -- End]', facts['playpower_dates'])
    text = _replace_first(text, '[FIXED: Title]', facts['playpower_title'])
    text = _replace_first(text, '[FIXED: Location]', facts['playpower_location'])
    for bullet in playpower_bullets:
        text = _replace_first(text, '[GENERATE: Bullet]', bullet)

    for name, tools, tag, description in projects:
        text = _replace_first(text, '[GENERATE: Project Name]', name)
        text = _replace_first(text, '[GENERATE: tools, comma-separated]', tools)
        text = _replace_first(text, '[GENERATE: tag, e.g. Hackathon Winner]', tag)
        text = _replace_first(text, '[GENERATE: description]', description)

    text = _replace_first(text, '[FIXED: Degree, Major]', facts['degree'])
    text = _replace_first(text, '[FIXED: Start -- End]', facts['education_dates'])
    text = _replace_first(text, '[FIXED: Institution]', facts['institution'])
    text = _replace_first(text, '[FIXED: X.XX/10.0]', facts['gpa'])

    return text
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd resume_builder/helpers && python3 test_tailor_resume.py`

If `test_render_produces_no_leftover_generate_markers` fails because a marker text in
the real template doesn't match exactly (templates drift), open
`resume_builder/templates/swe_resume_template.tex`, copy the exact marker string, and
fix the corresponding `_replace_first` call — do not weaken the test.

Expected once fixed: all `PASS:` lines including the 3 new ones, no errors.

- [ ] **Step 5: Commit**

```bash
git add resume_builder/helpers/tailor_resume.py resume_builder/helpers/test_tailor_resume.py
git commit -m "feat: add .tex template renderer to tailor_resume.py"
```

---

### Task 8: CLI wiring and end-to-end validation

**Files:**
- Modify: `resume_builder/helpers/tailor_resume.py`
- Test: `resume_builder/helpers/test_tailor_resume_e2e.py` (separate file — this one
  shells out to `tectonic`/`pypdf`/the existing gate scripts, kept apart from the fast
  unit tests above)

**Interfaces:**
- Consumes: everything from Tasks 1-7.
- Produces: `main()` CLI entry point; `tailor(jd_text, company, lane) -> dict` with
  keys `tex_path`, `keyword_table_path`, `coverage_pct` — this is what `/make-resume`
  (Task 9) will eventually shell out to via the CLI, but exposing it as a function too
  keeps it testable without subprocess overhead.

- [ ] **Step 1: Write failing end-to-end test**

```python
# resume_builder/helpers/test_tailor_resume_e2e.py
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


def _run_gates(tex_path):
    subprocess.run(
        ['python3', 'char_count.py', '-f', 'resume', tex_path], check=True)
    pdf_path = tex_path.replace('.tex', '.pdf')
    subprocess.run(
        ['tectonic', '-c', 'minimal', tex_path], check=True, cwd=os.path.dirname(tex_path) or '.')
    pages = subprocess.run(
        ['python3', '-c',
         f"import pypdf; print(len(pypdf.PdfReader('{pdf_path}').pages))"],
        capture_output=True, text=True, check=True).stdout.strip()
    assert pages == '1', f"expected 1 page, got {pages}"
    subprocess.run(['python3', 'fingerprint_check.py', tex_path], check=True)


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd resume_builder/helpers && python3 test_tailor_resume_e2e.py`
Expected: `AttributeError: module 'tailor_resume' has no attribute 'tailor'`

- [ ] **Step 3: Implement `tailor()` and CLI**

```python
# append to resume_builder/helpers/tailor_resume.py
import os
import re


def _slugify(company):
    return re.sub(r'[^a-z0-9]+', '_', company.lower()).strip('_')


def _select_lane(jd_text, lane_arg):
    if lane_arg != 'auto':
        return lane_arg
    jd_lower = jd_text.lower()
    if any(k in jd_lower for k in ('full-stack', 'full stack', 'react', 'next.js')):
        return 'fullstack'
    if any(k in jd_lower for k in ('ai engineer', 'ml engineer', 'rag', 'llm', 'agent')):
        return 'ai'
    return 'backend'


ALL_KNOWN_TAGS = None  # populated lazily by _collect_all_tags()


def _collect_all_tags(experience_dir):
    global ALL_KNOWN_TAGS
    if ALL_KNOWN_TAGS is not None:
        return ALL_KNOWN_TAGS
    tags = set()
    for fname in ('experience_c3ihub.md', 'experience_playpower.md', 'experience_projects.md'):
        entries = ep.parse_experience_file(os.path.join(experience_dir, fname))
        for entry in entries.values():
            tags.update(entry.get('tags', []))
    ALL_KNOWN_TAGS = sorted(tags)
    return ALL_KNOWN_TAGS


TAXONOMY_TERMS = [
    'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'SQL', 'Node.js',
    'Express.js', 'FastAPI', 'Socket.IO', 'RESTful APIs', 'WebSocket', 'GraphQL',
    'Nginx', 'Next.js', 'React', 'Tailwind CSS', 'PostgreSQL', 'MongoDB', 'Redis',
    'DynamoDB', 'Kafka', 'BullMQ', 'Redis Streams', 'Redis Pub/Sub',
    'Event-Driven Architecture', 'CrewAI', 'LangGraph', 'RAG', 'ChromaDB', 'Qdrant',
    'NetworkX', 'AWS', 'Docker', 'Kubernetes', 'Terraform', 'GitHub Actions', 'CI/CD',
    'OpenTelemetry', 'Prometheus', 'Grafana', 'Distributed Tracing', 'Microservices',
    'Distributed Systems', 'System Design',
]


def tailor(jd_text, company, lane_arg, out_dir=None, helpers_dir=None):
    helpers_dir = helpers_dir or os.path.dirname(os.path.abspath(__file__))
    experience_dir = os.path.join(helpers_dir, '..', 'experience')
    template_path = os.path.join(helpers_dir, '..', 'templates', 'swe_resume_template.tex')

    lane_name = _select_lane(jd_text, lane_arg)
    lane = bd.LANES[lane_name]

    all_tags = _collect_all_tags(experience_dir)
    jd_keywords = extract_jd_keywords(jd_text, all_tags, TAXONOMY_TERMS)
    jd_keyword_set = set(jd_keywords['direct']) | set(jd_keywords['bridge'])

    c3ihub = ep.parse_experience_file(os.path.join(experience_dir, 'experience_c3ihub.md'))
    playpower = ep.parse_experience_file(os.path.join(experience_dir, 'experience_playpower.md'))
    projects = ep.parse_experience_file(os.path.join(experience_dir, 'experience_projects.md'))

    c3ihub_ids = select_bullets(
        lane['c3ihub_matrix'], c3ihub, jd_keyword_set, lane['c3ihub_pick_count'])
    playpower_ids = select_bullets(
        lane['playpower_matrix'], playpower, jd_keyword_set,
        lane['playpower_pick_count'], lane['playpower_caps'])
    project_ids = select_bullets(
        lane['projects_matrix'], projects, jd_keyword_set, lane['projects_pick_count'])

    c3ihub_bullets = [c3ihub[bid]['bullet'] for bid in c3ihub_ids]
    playpower_bullets = []
    for bid in playpower_ids:
        if bid == 'PP1':
            playpower_bullets.append(bd.PP1_VARIANTS[lane_name])
        else:
            playpower_bullets.append(playpower[bid]['bullet'])
    project_tuples = [
        (projects[pid]['header'].split(' | ')[0].split(' — ')[0],
         projects[pid]['header'], '', projects[pid]['description'])
        for pid in project_ids
    ]

    skills_groups = [(g, '') for g in lane['skills_group_order']]  # skills text: LLM review fills in bold/JD-match pass

    tagline = build_tagline(lane['approved_pool'], lane['default_tool_order'], lane['label'], jd_text)

    rendered = render_resume_tex(
        template_path, FIXED_FACTS, tagline, lane['summary'], skills_groups,
        c3ihub_bullets, playpower_bullets, project_tuples)

    out_dir = out_dir or os.path.join(helpers_dir, '..', '..', 'output', company)
    os.makedirs(out_dir, exist_ok=True)
    slug = _slugify(company)
    tex_path = os.path.join(out_dir, f'e2e_{slug}_resume.tex')
    with open(tex_path, 'w') as f:
        f.write(rendered)

    coverage_pct = compute_coverage(jd_keywords, rendered)
    keyword_table_path = os.path.join(out_dir, 'keyword_table.json')
    write_keyword_table(keyword_table_path, jd_keywords, coverage_pct)

    return {
        'tex_path': tex_path,
        'keyword_table_path': keyword_table_path,
        'coverage_pct': coverage_pct,
        'lane': lane_name,
    }


def main():
    parser = argparse.ArgumentParser(description='Deterministic JD-to-resume-draft assembler')
    parser.add_argument('--jd', required=True, help='Path to JD text file')
    parser.add_argument('--company', required=True)
    parser.add_argument('--lane', choices=['backend', 'fullstack', 'ai', 'auto'], default='auto')
    parser.add_argument('--out-dir', default=None)
    args = parser.parse_args()

    with open(args.jd) as f:
        jd_text = f.read()

    result = tailor(jd_text, args.company, args.lane, out_dir=args.out_dir)
    print(f"Lane: {result['lane']}")
    print(f"Draft: {result['tex_path']}")
    print(f"Keyword table: {result['keyword_table_path']}")
    print(f"Coverage: {result['coverage_pct']}%")


if __name__ == '__main__':
    main()
```

Note: the skills-line text (comma-separated skill names per group, bolded on JD match)
is deliberately left for `/make-resume`'s LLM review pass in Task 9 — bolding-on-JD-match
is exactly the kind of judgment call that belongs in the review step, not the
deterministic draft.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd resume_builder/helpers && python3 test_tailor_resume_e2e.py`
Expected: `PASS: test_two_different_jds_produce_different_resumes_and_pass_all_gates`

If a gate fails (e.g. char_count OVER), inspect which bullet combination overflowed and
adjust `pick_count` handling or `_replace_first` marker mapping — do not loosen the
gate script itself.

- [ ] **Step 5: Run the full fast unit-test suite once more**

Run: `cd resume_builder/helpers && python3 test_experience_parser.py && python3 test_bundle_data.py && python3 test_tailor_resume.py`
Expected: all PASS, no errors.

- [ ] **Step 6: Commit**

```bash
git add resume_builder/helpers/tailor_resume.py resume_builder/helpers/test_tailor_resume_e2e.py
git commit -m "feat: wire tailor_resume.py CLI, validate against existing quality gates"
```

---

### Task 9: Integrate tailor_resume.py into /make-resume Batch Mode

**Files:**
- Modify: `.claude/skills/make-resume/SKILL.md`

**Interfaces:**
- Consumes: `tailor_resume.py` CLI (Task 8) — invoked as a subprocess/Bash step, not
  imported (this is an LLM-driven skill file, not Python).

- [ ] **Step 1: Replace Step 0's file-read list with a script call + reduced reads**

In `.claude/skills/make-resume/SKILL.md`, replace the existing "Step 0: Load context"
section (the 7-item read list) with:

```markdown
## Step 0: Run the deterministic tailoring pass

```bash
python3 resume_builder/helpers/tailor_resume.py --jd <JD file path> --company "<Company>" --out-dir output/<FolderName>
```

This writes a draft `output/<FolderName>/e2e_<name>_resume.tex` and
`output/<FolderName>/keyword_table.json` with 0 LLM tokens — bullet/tagline/skills
selection already applied per the matching lane's bundle rules.

Then read, and nothing else:
1. `output/<FolderName>/e2e_<name>_resume.tex` (the draft)
2. `output/<FolderName>/keyword_table.json` (Direct/Bridge keyword table + coverage %)
3. `resume_builder/support/achievement_reframing_guide.md` — Bullet Generation Policy
   and the five tailoring levers (needed for Step 3's review pass)

**Fallback (only if `keyword_table.json`'s `coverage_pct` is below 75%):** read the
relevant `resume_builder/experience/experience_*.md` file in full to look for a
truthful bullet swap the script's tag-overlap heuristic missed, per Step 6.
```

- [ ] **Step 2: Update Step 1 (JD keyword table) to consume the script's output**

Replace the "Extract the top 15-20 ATS terms..." instruction with:

```markdown
## Step 1: Review the JD keyword table

`keyword_table.json` already has the Direct/Bridge keyword table and computed
coverage %. Present it as the compact table (same format as before). If a term looks
mis-tagged (e.g. a Gap the script missed, or a Bridge term that's actually a hard Gap
given `SKILL_PROFILE.md`), correct it here — this is the review checkpoint, not a
blind pass-through.
```

- [ ] **Step 3: Update Step 2 (bullet selection) to describe the review, not fresh selection**

Replace "Pick bullets per the bundle's Priority Matrix..." with:

```markdown
## Step 2: Review the script's bullet selection

The draft `.tex` already has bullets selected by `tailor_resume.py` (cap rules and
Priority Matrix ranks already respected). Sanity-check: does each selected bullet
genuinely fit this JD better than an unselected one in the same slot? If the script's
coverage % is below 75%, consult the fallback experience-file read from Step 0 and
swap in a stronger truthful bullet for the weakest-fitting slot — copy-exact only, same
rule as always.
```

- [ ] **Step 4: Update Step 3 to frame the five levers as a review pass**

At the top of "Step 3: Generate Summary / Skills / bullets", add one sentence:

```markdown
This step reviews and polishes the script's draft — it is not a from-scratch
generation. Apply these five levers as edits to what's already in the draft:
```//prepend before existing "Apply these five levers, all truthful:" line

Also add, in the Skills section instructions, that the draft's skills groups have
group *names and order* filled in but empty skill-lists — fill each group's
comma-separated skills from `skills_taxonomy.md`, bolding only tokens that appear in
the JD (this was previously implicit; now explicit since the script leaves it blank).

- [ ] **Step 5: Manually verify the updated skill against a real JD**

Run `/make-resume` (as a user would) against one real JD file from `JDs/` (or a
sample), reading the updated `SKILL.md` steps as written. Confirm:
- `tailor_resume.py` runs first and produces the draft.
- The LLM only reads the 3 files listed in the new Step 0 (plus fallback only if
  triggered).
- Gates in Steps 4-6 still run and pass.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/make-resume/SKILL.md
git commit -m "refactor: make-resume Batch Mode reviews tailor_resume.py draft instead of cold-generating"
```

---

### Task 10: CSV dedup helper

**Files:**
- Create: `check_applied_companies.py` (repo root, alongside `job_hunt.py`)
- Test: `resume_builder/helpers/test_check_applied_companies.py` — actually place next
  to the script for consistency: `test_check_applied_companies.py` (repo root)

**Interfaces:**
- Produces: `applied_companies(csv_path) -> set[str]` (company names with any row
  present, case-normalized) and a CLI (`python3 check_applied_companies.py <csv_path>`)
  that prints one company per line.

- [ ] **Step 1: Write failing test**

```python
# test_check_applied_companies.py (repo root)
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 test_check_applied_companies.py`
Expected: `ModuleNotFoundError: No module named 'check_applied_companies'`

- [ ] **Step 3: Implement the script**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 test_check_applied_companies.py`
Expected: `PASS: test_applied_companies_reads_unique_company_names`

- [ ] **Step 5: Wire into daily_scan.md step 1**

In `.agents/workflows/daily_scan.md`, replace step 1's text:

```markdown
1. **Deduplication Check**:
   - Run `python3 job-kit-starter/check_applied_companies.py job-kit-starter/output/job-search/applications.csv`
     and use its output (one company per line) to skip already-touched companies —
     do not read the full `applications.csv` into context for this check.
```

- [ ] **Step 6: Commit**

```bash
git add check_applied_companies.py test_check_applied_companies.py .agents/workflows/daily_scan.md
git commit -m "feat: add script-based CSV dedup check, stop reading full applications.csv for dedup"
```

---

### Task 11: Gate reorder + per-job subagent dispatch in daily_scan.md; Playwright rule in PLAYBOOK.md

**Files:**
- Modify: `.agents/workflows/daily_scan.md`
- Modify: `job-kit-starter/PLAYBOOK.md`

- [ ] **Step 1: Reorder step 5 — exclusion/screener check before tailoring**

Replace the current step 5 (a/b/b2/c/d/e/f) with:

```markdown
5. **Apply — Screen, then Tailor + Submit**, for each of the top `NUM_JOBS` leads (plus
   all qualifying Indeed Smart Apply / LinkedIn Easy Apply leads, tracked separately —
   see param note above). **Dispatch each lead to its own subagent** (see step 5's
   subagent contract below) running the sequence:

   a. **HARD GATE — mechanical exclusion check, run first, before any tailoring:**
      literally quote the job title and re-check it word-by-word against this list —
      Java, .NET/C#/ASP.NET, C++, Ruby/Ruby on Rails, Senior, Staff, Principal,
      Architect, Lead, SDE 2/II, SDE 3/III, SDE-2, SDE-3, Product Engineer II/PE 2,
      Member of Technical Staff/MTS. Any match anywhere in the title or the JD's
      stated primary stack → do not open the form, log `Status=Skipped` with the
      matched term as the reason, return that status to the orchestrator, done — no
      resume is ever built for this lead.
   b. **Screener check, before tailoring:** from the JD text (or the first form page,
      if reachable without a full fill), check for an explicit hard screener
      disqualifier (e.g. "4+ years required", visa sponsorship required, a
      language/stack requirement missed by 5a's string check). If found, log
      `Status=Skipped` with the reason, return, done.
   c. **Only now, tailor:** run `/make-resume <JD path or text>` (Batch Mode, now
      backed by `tailor_resume.py` — see `.claude/skills/make-resume/SKILL.md`). It
      saves the compiled PDF to `output/<Company>/e2e_<name>_resume.pdf` and a
      `batch_notes.md` with the ATS match rate — rename/copy the PDF to
      `output/<Company> - <Role>/Pratham_Modi_Resume.pdf` for the apply step.
   d. **HARD GATE:** do not proceed to Submit unless that PDF exists on disk. Never
      submit with a generic/default/cached resume.
   e. Fill the ATS form using the platform-specific recipe in PLAYBOOK.md → "ATS
      recipes". Always replace any pre-selected default resume with the tailored PDF.
      Save any account credentials / TOTP secrets created during signup to
      `output/<Company> - <Role>/account_credentials.txt`. Element discovery follows
      the Playwright evaluate-only rule in PLAYBOOK.md — do not call `browser_snapshot`
      for this.
   f. Click final Submit.
   g. **On any blocker** (image/grid captcha, Cloudflare "Additional Verification
      Required" wall, an unresolvable required field): do not close the tab, do not
      pause. Leave that application exactly where it got stuck in its own browser tab,
      log `Status=Blocked` with the specific reason, return that status. The user
      finishes blocked ones manually later. **This does not fill a `NUM_JOBS` slot** —
      the orchestrator pulls another qualifying lead to replace it.
   h. Log the result (Applied / Blocked / Skipped) to `applications.csv` via the
      csv-logger agent and run `job-kit-starter/tracker/refresh.sh`. Log the actual
      per-job posting URL, not a generic feed/search URL.

   **Subagent dispatch contract:** the orchestrator dispatches one subagent per lead
   with this payload only — Company, Role, Job URL, JD text (or fetch instructions),
   output folder path (`output/<Company> - <Role>/`), the path
   `.agents/rules/job_hunt_profile.md` (the subagent reads this itself for canonical
   form facts — never paste facts into the payload), and today's date (the subagent
   has no clock). The subagent runs 5a-5h above and returns exactly one line:
   `<Status> | <Company> | <Role> | <Resume path or "-"> | <Req ID or reason>`. The
   orchestrator's context holds only these one-line returns plus the queue state
   (Pending/Applied/Blocked/Skipped per lead) — it never holds tailoring reasoning,
   browser traces, or compile output. This isolation is deliberate: it's what keeps
   personal-info form-filling accurate at job #10 the same as job #1, since each
   subagent starts from a fresh read of `job_hunt_profile.md` rather than a
   conversation that's drifted across many prior jobs.
```

- [ ] **Step 2: Update the `NUM_JOBS` accounting note (step 4) to reference subagent returns**

In step 4's existing "counts `Status=Applied` only, not attempts" paragraph, append one
sentence: "Track this from each subagent's one-line return in step 5, not from
re-reading `applications.csv`."

- [ ] **Step 3: Add the Playwright evaluate-only rule to PLAYBOOK.md**

In `job-kit-starter/PLAYBOOK.md`, immediately after the "### ATS recipes" heading
(before the Workday entry), insert:

```markdown
**Element discovery rule (token discipline):** every recipe below locates and
interacts with elements via `browser_evaluate` (targeted DOM queries/selectors) or
`browser_click`/`browser_fill_form` with a known selector — never via a full
`browser_snapshot` (accessibility-tree dump). Snapshot dumps run 100-380KB and blow up
context fast across a multi-job run. Reserve `browser_snapshot` for a genuinely stuck
state with no other way to locate an element, and even then scope it to a specific
container/region if the tool supports that, not the whole page.
```

- [ ] **Step 4: Verify no other part of daily_scan.md still references the old step
      5a-5f numbering**

Run: `grep -n "step 5" /home/modi/Work/job-kit-starter/.agents/workflows/daily_scan.md /home/modi/Work/job-kit-starter/.agents/rules/*.md /home/modi/Work/job-kit-starter/job-kit-starter/CLAUDE.md`

Fix any stale cross-reference found (e.g. `regression_checklist.md` referencing
"step 5e" for blocker handling — update to the new sub-step letter, "5g").

- [ ] **Step 5: Commit**

```bash
git add .agents/workflows/daily_scan.md job-kit-starter/PLAYBOOK.md
git commit -m "refactor: reorder daily_scan gates before tailoring, add per-job subagent dispatch and Playwright evaluate-only rule"
```

---

## Self-Review Notes

- **Spec coverage:** tailor_resume.py + bundle_data.py + experience_parser.py (spec §1)
  → Tasks 1-8. make-resume Step 0 trim (spec §2) → Task 9. Gate reorder (spec §3a) →
  Task 11 Step 1. Subagent dispatch (spec §3b) → Task 11 Step 1's contract. Playwright
  rule (spec §4) → Task 11 Step 3. CSV dedup (spec §5) → Task 10.
- **Placeholder scan:** no TBD/TODO; every code block is complete, runnable code against
  real file paths and real bundle/experience content already read from the repo.
- **Type consistency:** `select_bullets` (Task 4) returns `list[str]` of bullet IDs,
  consumed identically in Task 8's `tailor()`. `extract_jd_keywords` (Task 3) returns
  `{'direct': [...], 'bridge': [...]}`, consumed identically by `compute_coverage`
  (Task 6) and `write_keyword_table` (Task 6). `render_resume_tex` (Task 7) signature
  matches its call in `tailor()` (Task 8) argument-for-argument.
- **Review Focus coverage:** cap-violation swap (Task 4, `test_select_bullets_respects_cap_rule`),
  hallucinated tagline tool (Task 5, `test_tagline_never_inserts_tool_outside_approved_pool`),
  copy-exact bullet mutation (Task 7, `test_render_reproduces_bullet_text_verbatim`),
  resume reuse across JDs (Task 8, `test_two_different_jds_produce_different_resumes_and_pass_all_gates`),
  wrong PP1 variant (Task 2, `test_pp1_variants_are_copy_exact_and_distinct`).
