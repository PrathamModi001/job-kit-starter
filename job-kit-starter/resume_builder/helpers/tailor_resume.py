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
