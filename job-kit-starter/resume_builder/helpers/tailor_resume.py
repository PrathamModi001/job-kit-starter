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
import json
import os
import re

import bundle_data as bd
import experience_parser as ep
import fingerprint_check as fc


def _word_search(term, text_lower):
    """Whole-word/phrase search — avoids 'rag' matching 'storage', 'ai' matching
    'maintain', 'sql' matching 'postgresql', etc. Terms with non-alphanumeric
    edges (e.g. 'c#', '.net') can't take a \\b boundary there, so those fall
    back to plain substring matching on that edge only. Returns the Match object
    (for callers that need match position) or None."""
    term_lower = term.lower()
    if not term_lower:
        return None
    prefix = '' if not term_lower[0].isalnum() else r'\b'
    suffix = '' if not term_lower[-1].isalnum() else r'\b'
    pattern = prefix + re.escape(term_lower) + suffix
    return re.search(pattern, text_lower)


def _word_in_text(term, text_lower):
    return _word_search(term, text_lower) is not None


# Common tech terms the candidate does NOT possess (absent from every bundle's
# approved_pool and from skills_taxonomy.md) — used only to detect Gap terms so
# coverage_pct reflects requirements the candidate is missing, not just ones met.
# Excludes plain-English filler that would false-positive even under whole-word
# matching (e.g. 'go' in "go the extra mile", 'chef'/'storm'/'vault'/'swift' as
# ordinary adjectives/nouns) — those stay out even though the tools are real gaps,
# since a spurious gap only ever deflates coverage_pct, never inflates it.
GAP_CANDIDATE_TERMS = [
    'golang', 'rust', 'elixir', 'scala', 'ruby', 'ruby on rails', 'php',
    'c#', '.net', 'asp.net', 'kotlin', 'angular', 'vue', 'svelte',
    'hadoop', 'apache spark', 'flink', 'cassandra', 'snowflake', 'redshift',
    'bigquery', 'airflow', 'dbt', 'mysql', 'sqlite', 'neo4j', 'solr',
    'elasticsearch', 'rabbitmq', 'activemq', 'grpc', 'protobuf', 'istio',
    'envoy', 'pulsar', 'hashicorp vault', 'argocd', 'jenkins',
    'circleci', 'travis ci', 'gitlab ci', 'gcp', 'azure', 'ansible',
    'puppet',
]


def extract_jd_keywords(jd_text, all_tags, taxonomy_terms):
    jd_lower = jd_text.lower()
    direct = sorted({tag for tag in all_tags if _word_in_text(tag, jd_lower)})
    direct_set = set(direct)
    bridge = sorted({
        term.lower() for term in taxonomy_terms
        if _word_in_text(term, jd_lower) and term.lower() not in direct_set
    })
    bridge_set = set(bridge)
    gap = sorted({
        term for term in GAP_CANDIDATE_TERMS
        if _word_in_text(term, jd_lower) and term not in direct_set and term not in bridge_set
    })
    return {'direct': direct, 'bridge': bridge, 'gap': gap}


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
            # Bound tier degradation to at most 2 tiers; always allow tier-improving swaps.
            if candidate_tier <= worst_tier + 2 and candidate_score > worst_score:
                trial = [bullet_id if x == worst else x for x in selected]
                if not _violates_cap([x for x in trial if x != bullet_id], bullet_id, caps):
                    selected = trial
                    improved = True
                    break
    return selected


def build_tagline(approved_pool, default_tool_order, label, jd_text):
    jd_lower = jd_text.lower()
    matches = []
    for tool in approved_pool:
        match = _word_search(tool, jd_lower)
        if match:
            matches.append((match.start(), tool))
    matches.sort(key=lambda pair: pair[0])
    tools = [tool for _, tool in matches][:4]
    for tool in default_tool_order:
        if len(tools) == 4:
            break
        if tool not in tools:
            tools.append(tool)
    return f"Software Engineer | {label} | " + ", ".join(tools[:4])


def compute_coverage(jd_keywords, resume_text):
    matchable_terms = jd_keywords['direct'] + jd_keywords['bridge']
    all_terms = matchable_terms + jd_keywords.get('gap', [])
    if not all_terms:
        return 0.0
    resume_lower = resume_text.lower()
    matched = [term for term in matchable_terms if _word_in_text(term, resume_lower)]
    return round(100 * len(matched) / len(all_terms), 1)


def write_keyword_table(path, jd_keywords, coverage_pct):
    data = dict(jd_keywords)
    data['coverage_pct'] = coverage_pct
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


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
    # NOTE: brief's Step 3 hardcoded 'Indian Institute of Information Technology' here,
    # which does not match any source file. SKILL_PROFILE.md's Education section (the
    # only place this fact appears) says 'Pandit Deendayal Energy University' — used here.
    'institution': 'Pandit Deendayal Energy University',
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

    # Project 1 and Project 2 use different exact marker text in the real template
    # (verified against resume_builder/templates/swe_resume_template.tex) — handle
    # each explicitly rather than looping with one assumed-shared marker set.
    name1, tools1, tag1, description1 = projects[0]
    text = _replace_first(text, '[GENERATE: Project Name]', name1)
    text = _replace_first(text, '[GENERATE: tools, comma-separated]', tools1)
    text = _replace_first(text, '[GENERATE: tag, e.g. Hackathon Winner]', tag1)
    text = _replace_first(
        text, '[GENERATE: 1-line description — copy-exact from experience_projects.md]',
        description1)

    name2, tools2, tag2, description2 = projects[1]
    text = _replace_first(text, '[GENERATE: Project Name]', name2)
    text = _replace_first(text, '[GENERATE: tools]', tools2)
    text = _replace_first(text, '[GENERATE: tag]', tag2)
    text = _replace_first(text, '[GENERATE: description]', description2)

    text = _replace_first(text, '[FIXED: Degree, Major]', facts['degree'])
    text = _replace_first(text, '[FIXED: Start -- End]', facts['education_dates'])
    text = _replace_first(text, '[FIXED: Institution]', facts['institution'])
    text = _replace_first(text, '[FIXED: X.XX/10.0]', facts['gpa'])

    return text


def _slugify(company):
    return re.sub(r'[^a-z0-9]+', '_', company.lower()).strip('_')


def _select_lane(jd_text, lane_arg):
    if lane_arg != 'auto':
        return lane_arg
    jd_lower = jd_text.lower()
    if any(_word_in_text(k, jd_lower) for k in ('full-stack', 'full stack', 'react', 'next.js')):
        return 'fullstack'
    if any(_word_in_text(k, jd_lower) for k in
           ('ai engineer', 'ml engineer', 'rag', 'llm', 'agentic', 'langchain', 'langgraph')):
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


# experience_projects.md **Header:** lines have the shape
#   Name | *Tools, comma-separated*[ — Tag]
# The optional " — Tag" suffix appears ONLY after the closing '*' (PJ1 alone has
# one). Project NAMES may themselves contain a stylistic em-dash (PJ2
# "DeployMind — AI-Powered GitOps Platform", PJ3 "Mnemoniq — Multi-Tier Memory
# AI Agent"), so the name must be taken verbatim as everything before the first
# ' | ' and must NOT be split further on ' — '.
PROJECT_HEADER_RE = re.compile(r'^(.+?) \| \*(.+?)\*(?: — (.+))?$')


def parse_project_header(header):
    """Split a projects-file header into (name, tools, tag).

    Fails loudly on an unexpected shape rather than silently emitting empty or
    garbage fields — every field here is COPY-EXACT resume content.
    """
    m = PROJECT_HEADER_RE.match(header.strip())
    if not m:
        raise ValueError(
            'Unparseable project header (expected "Name | *Tools*[ — Tag]"): '
            f'{header!r}')
    name, tools, tag = m.group(1), m.group(2), m.group(3)
    return name.strip(), tools.strip(), (tag.strip() if tag else '')


# The copy-exact source text (experience/*.md bullets and project headers,
# bundle_data.py summaries / lane labels / skills-group names) is plain prose,
# not LaTeX, and really does contain LaTeX-special characters:
#   '%'  — every quantified claim ("99.9% uptime", "38%"); unescaped it silently
#          comments out the rest of the line (CLAUDE.md: "Escape % in .tex output")
#   '&'  — lane labels and skills groups ("Backend & Distributed Systems",
#          "Cloud, DevOps & Observability"); unescaped it is a hard XeTeX error
#          ("Misplaced alignment tab character &")
#   '|'  — the tagline separator built by build_tagline(); the template's own
#          convention for a literal bar is '$\vert$'
# Substituted values are therefore escaped here, on the way into
# render_resume_tex(), never in the template (whose own '%' comment lines and
# LaTeX markup must stay untouched).
_TEX_ESCAPE_MAP = {
    '\\': r'\textbackslash{}',
    '&': r'\&',
    '%': r'\%',
    '#': r'\#',
    '_': r'\_',
    '$': r'\$',
    '{': r'\{',
    '}': r'\}',
    '|': r'$\vert$',
}
_TEX_ESCAPE_RE = re.compile('[' + re.escape(''.join(_TEX_ESCAPE_MAP)) + ']')


def _escape_tex(text):
    """Escape LaTeX-special characters in plain-prose resume content.

    Single-pass, so a replacement's own backslashes/braces are never re-escaped.
    """
    return _TEX_ESCAPE_RE.sub(lambda m: _TEX_ESCAPE_MAP[m.group(0)], text)


def _bullet_text(bullet_id, bullets_by_id, lane_name):
    """The exact prose that would be emitted for this bullet id, or None if the
    entry carries no bullet (projects, and PP1's two-variant entry)."""
    if bullet_id == 'PP1':
        return bd.PP1_VARIANTS[lane_name]
    return bullets_by_id.get(bullet_id, {}).get('bullet')


def _is_fingerprint_clean(text):
    """True if this bullet on its own trips none of fingerprint_check.py's
    POSITION-INDEPENDENT rules (Tier-1 banned words, '-ing' analysis closer).

    Reuses fingerprint_check's own predicates so there is exactly one
    definition of each rule — the gate is respected, never relaxed.
    """
    return not fc.check_banned_words(text) and not fc.check_ing_endings([text])


def _fingerprint_clean_matrix(matrix, bullets_by_id, lane_name):
    """Drop priority-matrix rows whose bullet text can never pass the gate.

    A bullet that violates a position-independent rule fails fingerprint_check
    wherever it lands, so the only correct place to handle it is selection.
    Rank order of the survivors is preserved.
    """
    kept = []
    for row in matrix:
        text = _bullet_text(row[1], bullets_by_id, lane_name)
        if text is None or _is_fingerprint_clean(text):
            kept.append(row)
    return kept


def _first_verb(text):
    words = text.strip().split()
    return words[0].lower() if words else ''


def _order_without_verb_repeats(bullets, prev_verb):
    """Emit bullets in priority order, deferring one whose opening verb repeats
    the previous bullet's (fingerprint_check's consecutive-same-verb rule).

    The c3iHub and Playpower lists render as one contiguous run of \\item lines,
    so the check spans the company boundary — hence prev_verb is threaded in.
    Falls back to priority order when no non-repeating bullet is available.
    """
    remaining = list(bullets)
    ordered = []
    while remaining:
        pick = next((b for b in remaining if _first_verb(b) != prev_verb), remaining[0])
        ordered.append(pick)
        remaining.remove(pick)
        prev_verb = _first_verb(pick)
    return ordered, prev_verb


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
        _fingerprint_clean_matrix(lane['c3ihub_matrix'], c3ihub, lane_name),
        c3ihub, jd_keyword_set, lane['c3ihub_pick_count'])
    playpower_ids = select_bullets(
        _fingerprint_clean_matrix(lane['playpower_matrix'], playpower, lane_name),
        playpower, jd_keyword_set,
        lane['playpower_pick_count'], lane['playpower_caps'])
    project_ids = select_bullets(
        lane['projects_matrix'], projects, jd_keyword_set, lane['projects_pick_count'])

    c3ihub_bullets, last_verb = _order_without_verb_repeats(
        [_bullet_text(bid, c3ihub, lane_name) for bid in c3ihub_ids], None)
    playpower_bullets, _ = _order_without_verb_repeats(
        [_bullet_text(bid, playpower, lane_name) for bid in playpower_ids], last_verb)

    c3ihub_bullets = [_escape_tex(b) for b in c3ihub_bullets]
    playpower_bullets = [_escape_tex(b) for b in playpower_bullets]

    project_tuples = []
    for pid in project_ids:
        name, tools, tag = parse_project_header(projects[pid]['header'])
        project_tuples.append((
            _escape_tex(name), _escape_tex(tools), _escape_tex(tag),
            _escape_tex(projects[pid]['description'])))

    # skills text: left blank on purpose — /make-resume's LLM review pass fills in
    # the comma-separated skill names and decides which to bold on JD match.
    skills_groups = [(_escape_tex(g), '') for g in lane['skills_group_order']]

    tagline = build_tagline(
        lane['approved_pool'], lane['default_tool_order'], lane['label'], jd_text)

    rendered = render_resume_tex(
        template_path, FIXED_FACTS, _escape_tex(tagline), _escape_tex(lane['summary']),
        skills_groups, c3ihub_bullets, playpower_bullets, project_tuples)

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
