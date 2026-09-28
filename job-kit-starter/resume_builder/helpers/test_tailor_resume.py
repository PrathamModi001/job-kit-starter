"""Plain-assert tests for tailor_resume.py. Run: python3 test_tailor_resume.py"""
import tailor_resume as tr
import bundle_data as bd

ALL_TAGS = ['node', 'kafka', 'redis', 'postgresql', 'microservices', 'docker']
TAXONOMY_TERMS = ['TypeScript', 'GraphQL', 'Terraform', 'Kafka', 'Redis']

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


def test_select_bullets_blocks_far_worse_tier_candidate_swap():
    # C6 (LOW tier, rank 6) scores higher than the current worst selected
    # bullet C1 (HIGH tier, rank 1), but the tier gap (LOW vs HIGH = 3 tiers)
    # exceeds the guardrail's 2-tier slack, so the swap must be blocked and
    # the original HIGH-tier default selection preserved.
    jd_keywords = {'websocket', 'django-channels', 'leadership'}
    selected = tr.select_bullets(BACKEND_C3IHUB_MATRIX, BULLETS_BY_ID, jd_keywords, pick_count=4)
    assert selected == ['C1', 'C3', 'C4', 'C5']
    assert 'C6' not in selected


def test_select_bullets_respects_cap_rule():
    matrix = [(1, 'PP2', 'HIGH'), (2, 'PP3', 'HIGH')]
    caps = [(frozenset({'PP2', 'PP3'}), 1)]
    jd_keywords = {'rag', 'ai', 'chromadb', 'embeddings'}
    selected = tr.select_bullets(matrix, BULLETS_BY_ID, jd_keywords, pick_count=2, caps=caps)
    assert len(selected) == 1
    assert set(selected) <= {'PP2', 'PP3'}


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


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f'PASS: {name}')
