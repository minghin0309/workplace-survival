# Benchmark v3.3 Attempt-1 Formal Score

- Status: `SCORED`
- Thresholds passed: no
- Executed at: `2026-08-21T05:22:33.782262Z`
- Attempt id: `939ba34fdaf4109e5e02184473018a441f2850e0d6a3395d6b260d4b9148538a`
- Formal scorer invocations: 1
- Rerun performed: no
- Report: `tests/benchmark/v3_3-holdout/cloud-cases/score-report-v33.json`
- Report SHA-256: `447968a580bb87ca0433d1ce0f9e2ed70b596b5768ead73f4e4b2ad311414140`
- Frozen scorer SHA-256: `14e8fcb52923e791e525f9ed5bd283886d1660807b2989526680c473af69c7c7`

Coverage:

- turns: 24
- accepted turns: 23
- gold-uncertain turns: 1 (`V33-013` T1)
- required question concepts: 6 across 6 cases
- required revision concepts: 30 across 17 cases (scored required-revision hits 26/29)

Metrics:

| metric | value | n/d | threshold | status |
| --- | --- | --- | --- | --- |
| route_accuracy | 1.000 | 23/23 | >= 0.95 | PASS |
| responsibility_accuracy | 0.955 | 21/22 | >= 0.90 | PASS |
| tone_accuracy | 0.909 | 20/22 | >= 0.90 | PASS |
| overall_accuracy | 0.955 | 21/22 | >= 0.90 | PASS |
| required_question_concept_recall | 1.000 | 6/6 | >= 0.90 | PASS |
| question_claim_support_precision | 1.000 | 10/10 | = 1.0 | PASS |
| required_revision_concept_recall | 0.897 | 26/29 | >= 0.90 | FAIL |
| revision_claim_support_precision | 0.962 | 25/26 | = 1.0 | FAIL |
| critical_invariant_violations | 0 | 0/23 | = 0 | PASS |
| gold_uncertain_rate | 0.042 | 1/24 | <= 0.20 | PASS |

Failed cases: V33-004 (`unsupported-revision-claims`), V33-008 (responsibility/overall vs gold Gray), V33-010 (tone), V33-012 (`required-revision-concepts`), V33-014 T2 (`required-revision-concepts`), V33-015 T3 (`required-revision-concepts`), V33-018 (tone).

Gold, ontology, evaluations, matches, and runtime Skill files were not modified after freeze. A second scorer invocation is forbidden in-version.

v3.2 attempt 3 remains frozen `SCORED` and is not rescored. Attempt 2 remains frozen `SCORED`. Attempt 1 remains `INVALID_COVERAGE`. v3.1 remains `SCORER_ERROR`.
