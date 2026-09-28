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
            'systems end-to-end across backend, frontend, and DevOps. Built and '
            'scaled a multi-tenant SaaS platform onboarding 10K+ users at C3iHub '
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
            'Software Engineer with 2+ years of production experience engineering '
            'Python backend systems, agentic AI workflows (LangChain, LangGraph, MCP), '
            'and high-throughput distributed microservices (Kafka, Redis, MongoDB, AWS). '
            'Proven impact architecting platforms serving 50K+ users with 99.9% uptime '
            'at C3iHub (IIT Kanpur) and deploying production RAG and agent architectures '
            'at Playpower Labs.'
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
