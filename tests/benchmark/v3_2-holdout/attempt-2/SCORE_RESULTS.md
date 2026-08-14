# Benchmark v3.2 Attempt-2 Formal Score

- Status: `SCORED`
- Thresholds passed: no
- Executed at: `2026-08-14T14:18:57.548762Z`
- Attempt id: `7fe61f20f228857076968a064c2e69e4bf793ce47f0be41ed40f64750dc36c0a`
- Formal scorer invocations: 1
- Rerun performed: no
- Report: `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/score-report-v322.json`
- Report SHA-256: `3b646bac33b84ec798eb53e779b716237fb7fa0cd1fdcc532a7f0ef93593cc03`
- Frozen scorer SHA-256: `9785066efce1f14ac071d05fe040a34c8be075b3ba28bcf9540054fde6f28fad`

Coverage:

- turns: 24
- accepted turns: 24
- gold-uncertain turns: 0
- required question concepts: 6 across 6 cases
- required revision concepts: 41 across 16 cases

Metrics:

| metric | value | n/d | threshold | status |
| --- | --- | --- | --- | --- |
| route_accuracy | 1.0 | 24/24 | >= 0.95 | PASS |
| responsibility_accuracy | 0.682 | 15/22 | >= 0.90 | FAIL |
| tone_accuracy | 0.955 | 21/22 | >= 0.90 | PASS |
| overall_accuracy | 0.727 | 16/22 | >= 0.90 | FAIL |
| required_question_concept_recall | 0.500 | 3/6 | >= 0.90 | FAIL |
| question_claim_support_precision | 0.571 | 4/7 | = 1.0 | FAIL |
| required_revision_concept_recall | 0.268 | 11/41 | >= 0.90 | FAIL |
| revision_claim_support_precision | 0.875 | 21/24 | = 1.0 | FAIL |
| critical_invariant_violations | 0 | 0/24 | = 0 | PASS |
| gold_uncertain_rate | 0.0 | 0/24 | <= 0.20 | PASS |

Case pass: V322-017 only. Gold, ontology, evaluations, matches, and runtime Skill files were not modified after freeze. A second scorer invocation is forbidden in-version.

Attempt 1 remains `INVALID_COVERAGE`. v3.1 remains `SCORER_ERROR`. Neither is rescored.
