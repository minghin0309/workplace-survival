# Workplace Survival Functional Test Results

## Current status

- Cases currently specified: 57.
- Latest T13.3 text execution: TC-01–TC-20 and TC-26–TC-57, 52 passed and 0 failed.
- Latest T13.3 image regression: TC-21–TC-25 received semantic checks only, 5 passed and 0 failed; no fresh image execution is claimed.
- Most recent attached-image execution remains the post-T11.5 run recorded below: 5 passed and 0 failed.

## Initial T10.1 run summary

- Scope: T10.1 functional validation.
- Test specification: `tests/TEST_CASES.md`.
- Skill under test: `.cursor/skills/workplace-survival/`.
- Cases executed: 32.
- Passed: 32.
- Failed: 0.
- Final pass rate: 100%.
- Post-acceptance skill-rule changes: short-acknowledgement semantics and stronger register preservation.
- Test-fixture corrections: TC-30 specifies its existing tone rating; five missing PNG fixtures were regenerated.

## Method

- Six isolated evaluator contexts executed the six test suites.
- Fresh case state was used unless the test explicitly required a continuation or existing case.
- Evaluators read `SKILL.md`, `REFERENCE.md`, `FORMATS.md`, and the exact test definitions before producing the test response.
- Results were checked against every `Expected` and `Forbidden` assertion.
- TC-21 through TC-25 used generated PNG fixtures from `tests/fixtures/`.
- This run validates skill behavior when the instructions are explicitly loaded. Automatic discovery and invocation remain outside T10.1.

## T9.1 — Input and mode routing

- TC-01: PASS — Requested only missing Data B; no rating, revision, or template.
- TC-02: PASS — Requested Data A and stopped; did not enter limited mode.
- TC-03: PASS — Asked for limited-background confirmation after refusal; did not rate.
- TC-04: PASS — Assessed Data B only, marked manager alignment not assessed, and returned green/green/green.
- TC-05: PASS — Entered template mode with placeholders and no ratings.

Suite result: 5 passed, 0 failed.

## T9.2 — Normal-mode ratings

- TC-06: PASS — Matching owner and date produced green/green/green and no revision.
- TC-07: PASS — Data B answered the owner request without external-verification demand or promotion to Data A.
- TC-08: PASS — Contradictory owner and date produced red/green/red and a required correction.
- TC-09: PASS — Non-critical `we` ambiguity produced yellow/green/yellow and a minimal clarification.
- TC-10: PASS — Conflicting Data A produced gray/green/gray and a governing-owner question.

Suite result: 5 passed, 0 failed.

## T9.3 — Grill me interaction

- TC-11: PASS — Asked one neutral owner question using an unknown placeholder.
- TC-12: PASS — Asked exactly three prioritized questions and deferred lower-impact uncertainties.
- TC-13: PASS — Suggested answer structures contained no invented owner or deadline.
- TC-14: PASS — Added only the user's explicit owner answer to Data A and reassessed the case.
- TC-15: PASS — Replaced Data B, reassessed both dimensions, and did not repeat the resolved question.

Suite result: 5 passed, 0 failed.

## T9.4 — Revision policy

- TC-16: PASS — Applied only a minimal handoff clarification and preserved timing and purpose.
- TC-17: PASS — Replaced the known-wrong Thursday deadline with confirmed Tuesday.
- TC-18: PASS — Used an expected-completion-date placeholder and kept the review incomplete.
- TC-19: PASS — Green output used `No revision needed` with no alternative draft.
- TC-20: PASS — Preserved Cantonese written Chinese and informal register while clarifying responsibility.

Suite result: 5 passed, 0 failed.

## T9.5 — Image input

- TC-21: PASS — Extracted only `Priya owns the deployment.`, ignored interface content, and rated it directly.
- TC-22: PASS — Detected two possible drafts, requested selection, and produced no rating.
- TC-23: PASS — Kept responsibility gray, tone green, and did not infer participant identity.
- TC-24: PASS — Ignored the immaterial cropped notification without asking a question.
- TC-25: PASS — Reviewed only visible content and did not reconstruct anything outside the crop.

Suite result: 5 passed, 0 failed.

## T9.6 — State and case isolation

- TC-26: PASS — Reused same-case Data A, replaced Data B, and reassessed both dimensions.
- TC-27: PASS — Started a new case and did not carry report context into the migration message.
- TC-28: PASS — Requested case classification before reusing Data A.
- TC-29: PASS — Adopted the revision as new Data B but kept the unresolved placeholder and non-green state.
- TC-30: PASS — Preserved gray responsibility, green tone, and gray overall status, then stopped questions.

Suite result: 5 passed, 0 failed.

## Difference and regression log

### TC-30 fixture precision

Initial observation:

- The test required preservation of the current tone rating but did not specify that rating.
- The evaluator could only express the result parametrically.

Correction:

- Updated TC-30 state to specify an existing green tone rating.
- Updated its expected output to require green tone and gray overall status.
- No skill rule was changed because the skill behavior was correct.

Regression:

- Re-ran TC-30 after the fixture correction.
- Result: PASS, 7 of 7 assertions satisfied.
- The prior fixture ambiguity is resolved.

## T10.1 conclusion

All 32 functional cases pass. The post-T11.5 regression added two short-acknowledgement cases, strengthened register preservation after an initial TC-20 failure, regenerated the five missing PNG fixtures, and then passed the complete functional suite.

## Post-T11.5 regression

### Short acknowledgements

- TC-31: PASS — `okok` acknowledged all directly preceding clear instructions; responsibility clarity, tone, and overall status were green; no expanded revision or unsupported action was added.
- TC-32: PASS — `okok` did not supply an explicitly requested owner or deadline; responsibility clarity and overall status were red; neutral placeholder questions introduced no facts.

### Existing-suite regression

- TC-01–TC-19: 19 passed, 0 failed.
- TC-20 initially failed because the revision converted informal Cantonese to formal written Chinese.
- The specification and runtime reference/examples were tightened to preserve visible register markers and replace only the problematic responsibility wording.
- TC-20 rerun: PASS — revision remained informal Cantonese: `阿明搞掂啲資料之後，我會交。`
- TC-21–TC-25 initially could not run because the five generated PNG fixtures were absent.
- Installed Pillow for the local Python launcher and regenerated all five fixtures with `tests/fixtures/generate_fixtures.py`.
- TC-21–TC-25 rerun: 5 passed, 0 failed.
- TC-26–TC-30: 5 passed, 0 failed.

Final post-acceptance functional result: 32 passed, 0 failed.

## Documentation consolidation regression — 2026-08-12

- Scope: verify that retiring duplicate engineering documents and reducing non-normative examples did not change runtime behavior.
- Normative runtime files checked against `main`: `SKILL.md`, `REFERENCE.md`, and `FORMATS.md` are unchanged.
- Six isolated evaluator contexts re-ran the 27 text cases in TC-01–TC-32 against the current runtime files and exact assertions.
- TC-21–TC-25 received semantic regression checks against their visual-fixture definitions; the PNGs were not attached in this consolidation run, so these checks are not recorded as fresh case executions.
- Fresh execution result: 27 passed, 0 failed. Additional semantic visual-fixture checks: 5 passed, 0 failed.

## T13.1 embedded-content boundaries — 2026-08-12

### New cases

- TC-33–TC-36: 4 passed, 0 failed — clear blockquote, email reply, forwarded message, and chat preview boundaries.
- TC-37–TC-39: 3 passed, 0 failed — malformed boundary intake, quote-only missing Data B, and limited-background exclusion.
- TC-40–TC-43: 4 passed, 0 failed — inline-quote control, body-only revision, nested forwarding, and explicit Data A designation.

New-case result: 11 passed, 0 failed.

### Regression

- Existing text cases TC-01–TC-20 and TC-26–TC-32: 27 passed, 0 failed.
- Image cases TC-21–TC-25: 5 semantic fixture checks passed, 0 failed; images were not attached and these are not fresh executions.
- Independent pre-test consistency review found no remaining T13.1 ownership conflict, rule contradiction, or uncovered acceptance condition.

Fresh text execution result: 38 passed, 0 failed.

## T13.2 mixed-input classification — 2026-08-12

### New cases

- TC-44–TC-46: 3 passed, 0 failed — explicit semantic boundaries, unlabelled paragraphs, and unclear multi-person roles.
- TC-47–TC-49: 3 passed, 0 failed — multiple draft candidates, explicit-label precedence, and mixed classification with embedded content.

New-case result: 6 passed, 0 failed.

### Regression

- Existing text cases TC-01–TC-20 and TC-26–TC-43: 38 passed, 0 failed.
- Image cases TC-21–TC-25: 5 semantic fixture checks passed, 0 failed; images were not attached and these are not fresh executions.
- Independent pre-test consistency review found no remaining classification, provenance, outer-label, embedded-content, or ownership conflict.

Fresh text execution result: 44 passed, 0 failed.

## T13.3 effective Data A replacement — 2026-08-12

### New cases

- TC-50–TC-53: 4 passed, 0 failed — deadline withdrawal, owner correction, request cancellation, and unmarked conflict.
- TC-54–TC-57: 4 passed, 0 failed — targeted correction, unclear target, fact retraction, and commitment withdrawal.

New-case result: 8 passed, 0 failed.

### Regression

- Existing text cases TC-01–TC-20 and TC-26–TC-49: 44 passed, 0 failed.
- Image cases TC-21–TC-25: 5 semantic fixture checks passed, 0 failed; images were not attached and these are not fresh executions.
- Independent pre-test consistency review found no remaining correction, conflict, target-scope, stale-state, Data B isolation, or ownership issue.

Fresh text execution result: 52 passed, 0 failed.
