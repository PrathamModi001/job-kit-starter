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


def test_select_bullets_respects_cap_rule():
    matrix = [(1, 'PP2', 'HIGH'), (2, 'PP3', 'HIGH')]
    caps = [(frozenset({'PP2', 'PP3'}), 1)]
    jd_keywords = {'rag', 'ai', 'chromadb', 'embeddings'}
    selected = tr.select_bullets(matrix, BULLETS_BY_ID, jd_keywords, pick_count=2, caps=caps)
    assert len(selected) == 1
    assert set(selected) <= {'PP2', 'PP3'}


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f'PASS: {name}')
