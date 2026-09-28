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
