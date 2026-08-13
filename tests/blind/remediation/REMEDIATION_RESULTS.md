# Blind Defect Remediation Results

## Scope

The blind diagnostic's 18-case "clear defect" set was re-triaged before product changes.

- Confirmed generalized product defects: 3.
- Benchmark/input-contract or gold ambiguities: 15.
- Product rules changed only for the three confirmed defects.

See `tests/blind/REMEDIATION_TRIAGE.md`.

## Confirmed fixes

| Root cause | Blind case | Public regression | Result |
|---|---|---|---|
| Qualified non-severe bad-faith inference overcalled Red | BH-018 | TC-112 | PASS |
| Pronoun wording outranked causal basis before accepting remediation ownership | BH-023 | TC-113 | PASS |
| Revision redirected from intended manager to source author | BH-028 | TC-114 | PASS |

## Regression

- Functional TC-01–TC-114: 114 passed, 0 failed.
- Attached-image cases: 13 passed, 0 failed; every PNG was opened.
- Anti-hallucination AH-01–AH-06: 6 passed, 0 failed; unsupported facts: 0.
- Interaction quality IQ-01–IQ-06: 6 passed, 0 failed.
- Auto-trigger AT-01–AT-10: 10 passed, 0 failed in deterministic routing evaluation.
- Final-config explicit invocation FCI-01–FCI-03: 3 passed, 0 failed in deterministic routing evaluation.
- Total behavioral cases: 139 passed, 0 failed.
- Automated package check: 1 passed, 0 failed, reported separately.

All 140 records satisfy the T13.10 evidence schema and are stored in `tests/evidence/remediation-acceptance-final.json`. Runtime commit: `a497598ed1fae67b434ae774cc6137ca38b980d5`.

## Remediation mutation checks

- R1 reintroduced Tone Red for qualified non-severe intent inference: killed by TC-112.
- R2 made pronoun identity outrank current causal basis: killed by TC-113.
- R3 redirected revisions to source-email authors: killed by TC-114.
- Remediation mutation score: 3/3 killed.

Raw mutant diffs, SUT outputs, and oracle failures are stored under `tests/blind/remediation/evidence/`.

## Limitations

- Fifteen disputed blind cases were not converted into product rules or regression tests.
- The original cloud blind score remains unchanged.
- No fresh hidden holdout was run after remediation.
- Auto-trigger and explicit-invocation checks remain deterministic semantic tests rather than live dispatcher executions.

## Remediation evidence-complete record index

- Evidence file: `tests/evidence/remediation-acceptance-final.json`.
- Records:
  - `remediation-package-01-20260813`
