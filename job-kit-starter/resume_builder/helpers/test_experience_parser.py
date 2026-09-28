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
