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
            if worst_tier <= candidate_tier + 1 and candidate_score > worst_score:
                trial = [bullet_id if x == worst else x for x in selected]
                if not _violates_cap([x for x in trial if x != bullet_id], bullet_id, caps):
                    selected = trial
                    improved = True
                    break
    return selected
