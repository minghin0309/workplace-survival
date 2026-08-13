# Workplace Survival Final Acceptance Results

## Current remediation acceptance — 2026-08-13

- Functional TC-01–TC-114: 114 passed, 0 failed.
- Anti-hallucination AH-01–AH-06: 6 passed, 0 failed.
- Interaction quality IQ-01–IQ-06: 6 passed, 0 failed.
- Final-config explicit invocation FCI-01–FCI-03: 3 passed, 0 failed.
- Auto-trigger AT-01–AT-10: 10 passed, 0 failed.
- Total behavioral cases: 139 passed, 0 failed.
- Automated package check: 1 passed, 0 failed, reported separately.
- Attached-image cases: 13 passed, 0 failed.
- Runtime commit: `a497598ed1fae67b434ae774cc6137ca38b980d5`.
- Plan: `tests/evidence/remediation-acceptance-plan.json`.
- Evidence: `tests/evidence/remediation-acceptance-final.json`.
- Package record: `remediation-package-01-20260813`.

AT and FCI remain deterministic routing-semantic evaluations rather than live dispatcher tests. The original cloud blind score is unchanged, and no fresh hidden holdout has measured post-remediation unseen-case accuracy.

## T13.12 outcome — 2026-08-12

### Behavioral case pass rate

- Functional TC-01–TC-111: 111 passed, 0 failed.
- Anti-hallucination AH-01–AH-06: 6 passed, 0 failed.
- Interaction quality IQ-01–IQ-06: 6 passed, 0 failed.
- Final-configuration explicit invocation FCI-01–FCI-03: 3 passed, 0 failed.
- Automatic trigger AT-01–AT-10: 10 passed, 0 failed.
- Total behavioral cases: 136 passed, 0 failed.

The package check is reported separately and is not counted as a behavioral case.

### Image execution

- Attached-image cases: 13 passed, 0 failed.
- Every expected case-to-fixture mapping was validated.
- Every PNG was opened with image-capable reading.
- No semantic-only image check is counted as an attached-image execution.

### Repeat consistency

- Selected high-risk cases: 14.
- Independent evaluator contexts per case: 3.
- Repeat executions: 42 passed, 0 failed.
- Material variations in route, ratings, overall status, question count, or revision facts: 0.

Repeat executions are reported separately and are not added to the 136-case pass count.

## Evidence

- Final plan: `tests/evidence/t13-12-plan.json`.
- Evidence-complete case records: `tests/evidence/t13-12-final.json`.
- Final evidence records: 137 total:
  - 136 behavioral cases;
  - 1 automated package check.
- Runtime commit: `c72404b4629833a8ca09d3c01639f47fdbcafedc`.
- Package evidence record: `t13.12-package-01-20260812`.
- Repeat plan: `tests/evidence/t13-11-plan.json`.
- Repeat records: `tests/evidence/t13-11-repeat.json`.

Every final record contains ordered raw input/output, UTC execution time, model availability, source snapshot, runtime commit and blob hashes, assertion outcomes, result, limitations, and exact result citations.

Validation output:

```text
validated 137 evidence records across 5 suites
case acceptance: 136/136 passed
automated package checks: 1/1 passed
repeat consistency: 14 cases × 3 runs; 0 material variations
attached-image cases: 13/13 passed
```

## Package and publication

- Automated package check: 1 passed, 0 failed.
- Runtime package contains exactly `SKILL.md`, `REFERENCE.md`, `FORMATS.md`, and `EXAMPLES.md`.
- Runtime Markdown links, frontmatter, and installation paths are valid.
- Automatic invocation is enabled by the absence of `disable-model-invocation`.
- `PUBLISH_MANIFEST.md` exactly matches the publishable Git working set at execution.
- Functional IDs are contiguous from TC-01 through TC-111.
- All 13 PNG fixtures exist and are manifested.

## Method limitations

- AT-01–AT-10 and FCI-01–FCI-03 use deterministic routing-semantic evaluation. A live probabilistic Cursor dispatcher was not available, so production trigger or invocation variance is not measured.
- The evaluator API exposed the `inherit` selector and display name but not the exact resolved backend model slug; each affected evidence record states this.
- T13.11 covers selected high-risk cases, not three repetitions of every functional case.

## Historical results

Results before T13.10 are retained in suite files as historical summary-only records. EI-01–EI-03 remain historical tests of the old `disable-model-invocation: true` configuration and are not counted in current final-configuration acceptance.

## Conclusion

The repository passes the evidence-complete T13.12 acceptance plan for project use, personal installation, and publication. Live probabilistic dispatcher behavior remains an explicitly documented environment limitation.
