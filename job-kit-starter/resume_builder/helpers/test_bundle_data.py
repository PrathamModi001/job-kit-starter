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
