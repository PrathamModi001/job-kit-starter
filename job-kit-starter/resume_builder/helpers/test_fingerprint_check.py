#!/usr/bin/env python3
"""Plain-assert tests for fingerprint_check.py. Run directly: python3 test_fingerprint_check.py"""

import fingerprint_check as fc


def test_banned_word_detected():
    found = fc.check_banned_words("Leveraged Kafka to seamlessly scale the pipeline.")
    assert "leverage" in found or "leveraged" in found, found
    assert "seamlessly" in found, found


def test_no_banned_words_clean_text():
    found = fc.check_banned_words(
        "Architected core LMS backend serving 50K+ users using Express.js, MongoDB, Redis, and Socket.IO."
    )
    assert found == [], found


def test_em_dash_over_limit():
    tex = r"\item Sentence one --- with an em-dash. \item Two --- more --- here."
    assert fc.check_em_dash_count(tex) == 3


def test_em_dash_within_limit():
    tex = r"\item Sentence one --- fine. \item Two --- also fine."
    assert fc.check_em_dash_count(tex) == 0


def test_ing_ending_flagged():
    bullets = ["Reduced latency 60% via caching and reducing"]
    flagged = fc.check_ing_endings(bullets)
    assert flagged == [(1, "Reduced latency 60% via caching and reducing")], flagged


def test_ing_ending_suffix_match_is_deterministic_not_nlp():
    # "Spring" ends in the letters "ing" — the check is a plain suffix
    # match (matches ai_fingerprint_rules.md's "cheap regex/grep pass"
    # intent), so a proper noun like this is flagged too. This is an
    # accepted false-positive tradeoff, not a bug — documented here so a
    # future reader doesn't try to "fix" it into an NLP check.
    bullets = ["Migrated the legacy service to Spring"]
    flagged = fc.check_ing_endings(bullets)
    assert flagged == [(1, bullets[0])], flagged


def test_ing_ending_flagged_on_realistic_bullet():
    # last word is "caching", a real analysis-style "-ing" ending per
    # ai_fingerprint_rules.md — must be flagged.
    bullets = ["Cut MongoDB p99 latency from 450ms to 135ms via compound indexing, sharding, and Redis caching"]
    flagged = fc.check_ing_endings(bullets)
    assert flagged == [(1, bullets[0])], flagged


def test_consecutive_same_verb():
    bullets = ["Built the API gateway", "Built the auth service", "Deployed the pipeline"]
    flagged = fc.check_consecutive_same_verb(bullets)
    assert flagged == [(1, 2, "built")], flagged


def test_consecutive_same_verb_case_insensitive():
    bullets = ["Built the API gateway", "built the auth service"]
    flagged = fc.check_consecutive_same_verb(bullets)
    assert flagged == [(1, 2, "built")], flagged


def test_run_checks_empty_document():
    results = fc.run_checks(r"\begin{itemize} \end{itemize}")
    assert results["banned_words"] == []
    assert results["em_dash_over_limit"] == 0
    assert results["ing_endings"] == []
    assert results["consecutive_same_verb"] == []
    assert fc.has_violations(results) is False


def test_run_checks_clean_document_from_real_bullets():
    tex = r"""
    \item Architected core LMS backend serving 50K+ users across microservices using Express.js, MongoDB, Redis, and Socket.IO, sustaining 99.9% uptime at 10,000+ concurrent connections.
    \item Engineered event-driven notification pipeline handling 75K+ daily events at 99.5% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub with consumer-side deduplication.
    """
    results = fc.run_checks(tex)
    assert fc.has_violations(results) is False, results


def test_run_checks_dirty_document_flags_everything():
    tex = r"""
    \item Leveraged a robust, seamless pipeline for reducing
    \item Built the API gateway
    \item Built the auth service --- fast --- reliable --- scalable
    """
    results = fc.run_checks(tex)
    assert fc.has_violations(results) is True
    assert len(results["banned_words"]) > 0
    assert results["em_dash_over_limit"] > 0
    assert len(results["ing_endings"]) > 0
    assert len(results["consecutive_same_verb"]) > 0


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
