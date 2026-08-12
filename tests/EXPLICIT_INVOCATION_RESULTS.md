# Workplace Survival Explicit Invocation Results

## Evidence policy

- Canonical evidence requirements: `tests/evidence/README.md`.
- T11.2 results are historical summary-only records from the disabled-model-invocation configuration.
- The T13.10 environment-limited current-configuration record is stored in `tests/evidence/t13-10-validation.json`.
- FCI-01–FCI-03 and AT-10 are the applicable final-configuration semantic regressions.

Representative T13.10 record: `t13.10-ei-ei01-notrun-20260812` (`NOT_RUN`, not counted as a pass).

## Summary

- Slug used: `workplace-survival`.
- Test-stage configuration: `disable-model-invocation: true` was present during T11.2.
- Core modes tested: 3.
- Cases passed: 3.
- Cases failed: 0.

## Results

- EI-01: PASS — Explicit invocation entered Normal mode, used the fixed review format, returned green/green/green, asked no questions, and required no revision.
- EI-02: PASS — Explicit invocation requested confirmation before entering Limited-background mode, then assessed Data B only and left manager-requirement alignment unassessed.
- EI-03: PASS — Explicit invocation entered Message-template mode, used descriptive placeholders, emitted no ratings, and did not treat the generated template as Data B.

## T11.2 conclusion

Explicit invocation by the `workplace-survival` slug works with model invocation disabled. Normal mode, Limited-background mode, and Message-template mode all pass their expected behavior checks.

## Final-configuration regression

The final published frontmatter omits `disable-model-invocation` to enable automatic invocation, so the original EI configuration is historical and is not expected to remain present. After the post-T11.5 changes, AT-10 passed again and confirmed that explicit `workplace-survival` invocation still loads the skill under the final automatic-invocation configuration.

## T13.9 final-configuration check — 2026-08-12

- A strict attempt to rerun EI-01–EI-03 against current frontmatter was not recorded as a suite pass: all three fixtures require the historical `disable-model-invocation: true` field, which is intentionally absent.
- The Normal, Limited-background, and Message-template behavioral paths still satisfied their assertions in all three evaluations.
- AT-10 passed under the current configuration and remains the applicable explicit-invocation regression.
- Method limitation: behavioral evaluation did not exercise Cursor's live explicit-invocation dispatcher.

## T13.12 evidence-complete record index

- Evidence file: `tests/evidence/t13-12-final.json`.
- Records:
  - `t13.12-fci-01-20260812`, `t13.12-fci-02-20260812`, `t13.12-fci-03-20260812`

## T13.12 final result

- Final-configuration cases FCI-01–FCI-03: 3 passed, 0 failed.
- Normal, Limited-background, and Message-template routing paths passed.
- Final frontmatter at the recorded runtime commit contains the correct slug and omits `disable-model-invocation`.
- Limitation: no live Cursor invocation dispatcher was available; the three cases use deterministic routing-semantic evaluation.
