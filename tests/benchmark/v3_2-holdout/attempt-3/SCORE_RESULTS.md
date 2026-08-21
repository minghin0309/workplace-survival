# Benchmark v3.2 Attempt-3 Formal Score

- Status: `SCORED`
- Thresholds passed: no
- Executed at: `2026-08-15T02:39:55.560203Z`
- Attempt id: `6d76451402768e28f120525bf538edb3edfc5e163ef30bd15b9bf1850c12f341`
- Formal scorer invocations: 1
- Rerun performed: no
- Report: `tests/benchmark/v3_2-holdout/attempt-3/cloud-cases/score-report-v323.json`
- Report SHA-256: `4f9a30bc01f6e419a4cc173f3a1f49bb19feb5ce8206ef2bbeb852ddabe1c834`
- Frozen scorer SHA-256: `9785066efce1f14ac071d05fe040a34c8be075b3ba28bcf9540054fde6f28fad`

Coverage:

- turns: 24
- accepted turns: 24
- gold-uncertain turns: 0
- required question concepts: 6 across 6 cases
- required revision concepts: 41 across 17 cases

Metrics:

| metric | value | n/d | threshold | status |
| --- | --- | --- | --- | --- |
| route_accuracy | 0.958 | 23/24 | >= 0.95 | PASS |
| responsibility_accuracy | 0.696 | 16/23 | >= 0.90 | FAIL |
| tone_accuracy | 0.913 | 21/23 | >= 0.90 | PASS |
| overall_accuracy | 0.739 | 17/23 | >= 0.90 | FAIL |
| required_question_concept_recall | 1.000 | 6/6 | >= 0.90 | PASS |
| question_claim_support_precision | 0.778 | 7/9 | = 1.0 | FAIL |
| required_revision_concept_recall | 0.220 | 9/41 | >= 0.90 | FAIL |
| revision_claim_support_precision | 0.923 | 12/13 | = 1.0 | FAIL |
| critical_invariant_violations | 0 | 0/24 | = 0 | PASS |
| gold_uncertain_rate | 0.0 | 0/24 | <= 0.20 | PASS |

Case pass: V323-017 only. Gold, ontology, evaluations, matches, and runtime Skill files were not modified after freeze. A second scorer invocation is forbidden in-version.

Triage (no rescore): `tests/benchmark/v3_2-holdout/attempt-3/SCORE_TRIAGE.md`.

Attempt 2 remains frozen `SCORED` and is not rescored. Attempt 1 remains `INVALID_COVERAGE`. v3.1 remains `SCORER_ERROR`.
