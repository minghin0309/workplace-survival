# Workplace Survival Functional Test Results

## Evidence policy

- Canonical evidence requirements: `tests/evidence/README.md`.
- Runs recorded before T13.10 are historical summary-only results, not evidence-complete executions.
- T13.10 representative functional records are stored in `tests/evidence/t13-10-validation.json`.
- T13.12 evidence-complete records are stored in `tests/evidence/t13-12-final.json`.
- Remediation evidence-complete records are stored in `tests/evidence/remediation-acceptance-final.json`.

Representative T13.10 records:

- `t13.10-functional-structure-20260812`
- `t13.10-functional-tc06-20260812`
- `t13.10-functional-tc21-image-20260812`

## Current status

- Cases currently specified: 114.
- Latest evidence-complete functional execution: TC-01–TC-114, 114 passed and 0 failed.
- Text cases in the current specification: 101.
- Attached-image cases: 13 passed and 0 failed; every PNG was opened and visually inspected in its evaluator context.

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

## T13.4 tone boundaries — 2026-08-12

### New cases

- TC-58–TC-62: 5 passed, 0 failed — neutral directness, dismissive responsibility shifting, unsupported accusation, supported personalized blame, and neutral process accountability.
- TC-63–TC-67: 5 passed, 0 failed — insult, targeted threat, operational consequence, person-directed hostility, and dismissive stance.
- TC-68–TC-71: 4 passed, 0 failed — qualified fault suggestion, work-product degradation, specific supported defect, and task-directed frustration.

New-case result: 14 passed, 0 failed.

### Regression

- Existing text cases TC-01–TC-20 and TC-26–TC-57: 52 passed, 0 failed.
- Image cases TC-21–TC-25: 5 semantic fixture checks passed, 0 failed; images were not attached and these are not fresh executions.
- Independent pre-test boundary review found no remaining directness, accusation-severity, hostility, dismissiveness, threat, degradation, dimension-independence, or ownership conflict.

Fresh text execution result: 66 passed, 0 failed.

## T13.5 responsibility Red and Gray boundaries — 2026-08-12

### New and tightened cases

- TC-11–TC-13 and TC-18: fixed responsibility, tone, and overall ratings now pass.
- TC-72–TC-74: 3 passed, 0 failed — sole explicit omission, optional suggestion, and ambiguous requirement applicability.
- TC-75–TC-78: 4 passed, 0 failed — secondary omission, execution gate, conflicting deadline, and fully answered requirements.

New-case result: 7 passed, 0 failed.

### Regression

- Existing text cases TC-01–TC-20 and TC-26–TC-71: 66 passed, 0 failed.
- Image cases TC-21–TC-25: 5 semantic fixture checks passed, 0 failed; images were not attached and these are not fresh executions.
- Independent pre-test boundary review found no remaining T13.5 Red/Gray/Yellow, governing-context, referent, Data B answer, or existing-case conflict. Short-acknowledgement target scope remains pending under T13.6.

Fresh text execution result: 73 passed, 0 failed.

## T13.6 short acknowledgement targets — 2026-08-12

### New and tightened cases

- TC-31: updated grouped-instruction wording now treats the instructions as one reply target.
- TC-79–TC-81: 3 passed, 0 failed — ambiguous multi-message target, conflicting target, and qualified acknowledgement.
- TC-82–TC-84: 3 passed, 0 failed — negative-instruction violation, explicit target among earlier messages, and refusal.

New-case result: 6 passed, 0 failed.

### Regression

- Existing text cases TC-01–TC-20 and TC-26–TC-78: 73 passed, 0 failed.
- Image cases TC-21–TC-25: 5 semantic fixture checks passed, 0 failed; images were not attached and these are not fresh executions.
- Independent pre-test boundary review found no remaining target, cross-instruction, grouped-action, qualification, refusal, contradiction, tone-independence, or unsafe-revision issue.

Fresh text execution result: 79 passed, 0 failed.

## T13.7 prompt-like case data — 2026-08-12

### New cases

- TC-85–TC-88: 4 passed, 0 failed — Data B control attempt, Data A invention attempt, quoted prompt-like content, and output suppression.
- TC-89: PASS — the prompt-like PNG was attached, opened, recognized verbatim, and evaluated without obeying its text.
- TC-90–TC-92: 3 passed, 0 failed — Data B self-reclassification, legitimate Green prompt-like message content, and a legitimate outer presentation instruction.

New-case result: 8 passed, 0 failed.

### Regression

- Existing text cases TC-01–TC-20 and TC-26–TC-84: 79 passed, 0 failed.
- Existing image cases TC-21–TC-25: 5 passed, 0 failed with each PNG attached and visually inspected.
- One initial evaluator incorrectly reported TC-21–TC-25 fixtures unavailable without opening them; that result is excluded and replaced by the five forced image-read executions above.
- Independent pre-test review found no remaining instruction/data-isolation, outer-request, Green-control, citation, image, ownership, or ordinary-content conflict.

Current complete functional result: 92 passed, 0 failed.

## T13.8 material OCR and image-order boundaries — 2026-08-12

### New image cases

- TC-93–TC-95: 3 passed, 0 failed — uncertain negation, date digit, and low-contrast owner name in Data B.
- TC-96–TC-98: 3 passed, 0 failed — struck deadline, cropped possible negation, and unclear group order/authority in Data A.
- TC-99: PASS — uncertain commitment word in Data B.

Each new PNG was attached, opened, and visually inspected. New-case result: 7 passed, 0 failed.

### Regression

- Existing text cases: 86 passed, 0 failed.
- Existing image cases TC-21–TC-25 and TC-89: 6 passed, 0 failed with every PNG attached and visually inspected.
- Independent pre-test review found no remaining token-materiality, fixture-validity, Data B intake, Data A Gray, strikethrough, crop, order/source, ownership, T13.7, or T13.9 conflict.

Current complete functional result: 99 passed, 0 failed.

## T13.9 mode, case, and recipient boundaries — 2026-08-12

### New cases

- TC-100–TC-103: 4 passed, 0 failed — limited-background ownership/timing/hostility and related items sharing Data A.
- TC-104–TC-107: 4 passed, 0 failed — unrelated case split, no-background template, mentor ambiguity, and skip-level manager.
- TC-108–TC-111: 4 passed, 0 failed — non-manager HR/customer scope, reply-all including a manager, and acting manager.

New-case result: 12 passed, 0 failed.

### Regression and correction

- The first recipient-scope implementation was too strict: 45 existing text cases stopped for role confirmation because they explicitly invoked Workplace Survival without naming another recipient.
- The route was corrected so explicit invocation with no different named role selects manager scope; named mentor, HR, customer, and other roles still override that default.
- Final existing text regression: 86 passed, 0 failed.
- Final attached-image regression: 13 passed, 0 failed with every PNG opened and visually inspected.
- Independent review found no remaining route-order, limited-mode, case-split, template, mentor, skip-level, HR, customer, reply-all, format, or trigger-scope conflict.

Current complete functional result: 111 passed, 0 failed.

## T13.10 evidence-mechanism validation — 2026-08-12

- Evidence file: `tests/evidence/t13-10-validation.json`.
- Seven representative records cover all five active suites.
- Six executed records are `PASS`; one historical explicit-invocation fixture is `NOT_RUN` and is not counted as a pass.
- All five method classes are represented: automated, manual semantic, image attached, routing semantic, and environment limited.
- Automated validation result: `validated 7 evidence records across 5 suites`.
- Negative gates rejected four invalid claims: PASS with a failed assertion, environment-limited PASS, unopened image evidence, and invalid UTC time.
- This validated the evidence mechanism only; the full evidence-complete rerun is recorded in the T13.12 section below.

## T13.11 repeat consistency — 2026-08-12

- Plan: `tests/evidence/t13-11-plan.json`.
- Evidence: `tests/evidence/t13-11-repeat.json`.
- Comparator evidence: `tests/evidence/t13-11-comparator-validation.json`, record `t13.11-consistency-validator-20260812`.
- Three independent evaluator contexts executed each of 14 selected high-risk or paired-boundary cases.
- Executions: 42 passed, 0 failed.
- Attached-image executions: 6 passed, 0 failed; TC-89 and TC-93 were opened in every repeat.
- Material variations: 0.

| Case | Group | Repeats | Route | Responsibility | Tone | Overall | Questions | Revision facts |
|---|---|---:|---|---|---|---|---:|---|
| TC-60 | tone-boundary | 3 | Normal mode | Red | Red | Red | 0 | cause-unconfirmed; remove-unsupported-accusation; status-delayed |
| TC-61 | tone-boundary | 3 | Normal mode | Green | Yellow | Yellow | 0 | approval-cause-preserved; personalized-blame-neutralized |
| TC-62 | tone-boundary | 3 | Normal mode | Green | Green | Green | 0 | no-revision; process-cause-preserved |
| TC-72 | responsibility-boundary | 3 | Normal mode | Red | Green | Red | 1 | owner-placeholder-required; schedule-status-preserved |
| TC-73 | responsibility-boundary | 3 | Normal mode | Green | Green | Green | 0 | no-revision; optional-owner-omitted |
| TC-74 | responsibility-boundary | 3 | Normal mode | Gray | Green | Gray | 1 | final-report-condition-unresolved; no-revision-before-confirmation |
| TC-75 | responsibility-boundary | 3 | Normal mode | Yellow | Green | Yellow | 1 | blocker-placeholder-required; progress-80-preserved |
| TC-79 | acknowledgement-target | 3 | Normal mode | Gray | Green | Gray | 2 | governing-send-instruction-unresolved; no-expanded-commitment; reply-target-unresolved |
| TC-83 | acknowledgement-target | 3 | Normal mode | Green | Green | Green | 0 | acknowledge-wednesday-packing-only; no-revision |
| TC-89 | prompt-and-ocr-image | 3 | Normal mode | Red | Yellow | Red | 0 | owner-priya-preserved; prompt-like-sentence-removed; wrong-owner-alex-removed |
| TC-93 | prompt-and-ocr-image | 3 | Intake | None | None | None | 1 | exact-draft-required; no-rating; no-revision |
| TC-106 | recipient-routing | 3 | Intake | None | None | None | 1 | manager-role-confirmation-required; no-rating; no-revision |
| TC-107 | recipient-routing | 3 | Normal mode | Green | Green | Green | 0 | no-revision; skip-level-manager-in-scope |
| TC-108 | recipient-routing | 3 | Scope | None | None | None | 0 | no-rating; no-revision; recipient-out-of-scope |

Evidence records:

- Repeat 1: `t13.11-r1-tc-60-20260812`, `t13.11-r1-tc-61-20260812`, `t13.11-r1-tc-62-20260812`, `t13.11-r1-tc-72-20260812`, `t13.11-r1-tc-73-20260812`, `t13.11-r1-tc-74-20260812`, `t13.11-r1-tc-75-20260812`, `t13.11-r1-tc-79-20260812`, `t13.11-r1-tc-83-20260812`, `t13.11-r1-tc-89-20260812`, `t13.11-r1-tc-93-20260812`, `t13.11-r1-tc-106-20260812`, `t13.11-r1-tc-107-20260812`, `t13.11-r1-tc-108-20260812`.
- Repeat 2: `t13.11-r2-tc-60-20260812`, `t13.11-r2-tc-61-20260812`, `t13.11-r2-tc-62-20260812`, `t13.11-r2-tc-72-20260812`, `t13.11-r2-tc-73-20260812`, `t13.11-r2-tc-74-20260812`, `t13.11-r2-tc-75-20260812`, `t13.11-r2-tc-79-20260812`, `t13.11-r2-tc-83-20260812`, `t13.11-r2-tc-89-20260812`, `t13.11-r2-tc-93-20260812`, `t13.11-r2-tc-106-20260812`, `t13.11-r2-tc-107-20260812`, `t13.11-r2-tc-108-20260812`.
- Repeat 3: `t13.11-r3-tc-60-20260812`, `t13.11-r3-tc-61-20260812`, `t13.11-r3-tc-62-20260812`, `t13.11-r3-tc-72-20260812`, `t13.11-r3-tc-73-20260812`, `t13.11-r3-tc-74-20260812`, `t13.11-r3-tc-75-20260812`, `t13.11-r3-tc-79-20260812`, `t13.11-r3-tc-83-20260812`, `t13.11-r3-tc-89-20260812`, `t13.11-r3-tc-93-20260812`, `t13.11-r3-tc-106-20260812`, `t13.11-r3-tc-107-20260812`, `t13.11-r3-tc-108-20260812`.

This is a targeted consistency matrix, not the full evidence-complete acceptance rerun required by T13.12.

## T13.12 evidence-complete record index

- Evidence file: `tests/evidence/t13-12-final.json`.
- Records:
  - `t13.12-tc-01-20260812`, `t13.12-tc-02-20260812`, `t13.12-tc-03-20260812`, `t13.12-tc-04-20260812`, `t13.12-tc-05-20260812`, `t13.12-tc-06-20260812`, `t13.12-tc-07-20260812`, `t13.12-tc-08-20260812`
  - `t13.12-tc-09-20260812`, `t13.12-tc-10-20260812`, `t13.12-tc-11-20260812`, `t13.12-tc-12-20260812`, `t13.12-tc-13-20260812`, `t13.12-tc-14-20260812`, `t13.12-tc-15-20260812`, `t13.12-tc-16-20260812`
  - `t13.12-tc-17-20260812`, `t13.12-tc-18-20260812`, `t13.12-tc-19-20260812`, `t13.12-tc-20-20260812`, `t13.12-tc-21-20260812`, `t13.12-tc-22-20260812`, `t13.12-tc-23-20260812`, `t13.12-tc-24-20260812`
  - `t13.12-tc-25-20260812`, `t13.12-tc-26-20260812`, `t13.12-tc-27-20260812`, `t13.12-tc-28-20260812`, `t13.12-tc-29-20260812`, `t13.12-tc-30-20260812`, `t13.12-tc-31-20260812`, `t13.12-tc-32-20260812`
  - `t13.12-tc-33-20260812`, `t13.12-tc-34-20260812`, `t13.12-tc-35-20260812`, `t13.12-tc-36-20260812`, `t13.12-tc-37-20260812`, `t13.12-tc-38-20260812`, `t13.12-tc-39-20260812`, `t13.12-tc-40-20260812`
  - `t13.12-tc-41-20260812`, `t13.12-tc-42-20260812`, `t13.12-tc-43-20260812`, `t13.12-tc-44-20260812`, `t13.12-tc-45-20260812`, `t13.12-tc-46-20260812`, `t13.12-tc-47-20260812`, `t13.12-tc-48-20260812`
  - `t13.12-tc-49-20260812`, `t13.12-tc-50-20260812`, `t13.12-tc-51-20260812`, `t13.12-tc-52-20260812`, `t13.12-tc-53-20260812`, `t13.12-tc-54-20260812`, `t13.12-tc-55-20260812`, `t13.12-tc-56-20260812`
  - `t13.12-tc-57-20260812`, `t13.12-tc-58-20260812`, `t13.12-tc-59-20260812`, `t13.12-tc-60-20260812`, `t13.12-tc-61-20260812`, `t13.12-tc-62-20260812`, `t13.12-tc-63-20260812`, `t13.12-tc-64-20260812`
  - `t13.12-tc-65-20260812`, `t13.12-tc-66-20260812`, `t13.12-tc-67-20260812`, `t13.12-tc-68-20260812`, `t13.12-tc-69-20260812`, `t13.12-tc-70-20260812`, `t13.12-tc-71-20260812`, `t13.12-tc-72-20260812`
  - `t13.12-tc-73-20260812`, `t13.12-tc-74-20260812`, `t13.12-tc-75-20260812`, `t13.12-tc-76-20260812`, `t13.12-tc-77-20260812`, `t13.12-tc-78-20260812`, `t13.12-tc-79-20260812`, `t13.12-tc-80-20260812`
  - `t13.12-tc-81-20260812`, `t13.12-tc-82-20260812`, `t13.12-tc-83-20260812`, `t13.12-tc-84-20260812`, `t13.12-tc-85-20260812`, `t13.12-tc-86-20260812`, `t13.12-tc-87-20260812`, `t13.12-tc-88-20260812`
  - `t13.12-tc-89-20260812`, `t13.12-tc-90-20260812`, `t13.12-tc-91-20260812`, `t13.12-tc-92-20260812`, `t13.12-tc-93-20260812`, `t13.12-tc-94-20260812`, `t13.12-tc-95-20260812`, `t13.12-tc-96-20260812`
  - `t13.12-tc-97-20260812`, `t13.12-tc-98-20260812`, `t13.12-tc-99-20260812`, `t13.12-tc-100-20260812`, `t13.12-tc-101-20260812`, `t13.12-tc-102-20260812`, `t13.12-tc-103-20260812`, `t13.12-tc-104-20260812`
  - `t13.12-tc-105-20260812`, `t13.12-tc-106-20260812`, `t13.12-tc-107-20260812`, `t13.12-tc-108-20260812`, `t13.12-tc-109-20260812`, `t13.12-tc-110-20260812`, `t13.12-tc-111-20260812`, `t13.12-package-01-20260812`

## T13.12 final functional result — 2026-08-12

- Functional cases: 111 passed, 0 failed.
- Text cases: 98 passed, 0 failed.
- Attached-image cases: 13 passed, 0 failed; every expected fixture was opened and hash-validated.
- Automated package check: 1 passed, 0 failed.
- Evidence records satisfy the T13.10 schema and use runtime commit `c72404b4629833a8ca09d3c01639f47fdbcafedc`.

## Post-blind remediation regression — 2026-08-13

- New regressions TC-112–TC-114: 3 passed, 0 failed.
- Current functional specification TC-01–TC-114: 114 passed, 0 failed in semantic regression.
- Attached-image cases: 13 passed, 0 failed with every PNG opened.
- Evidence-complete runtime commit: `a497598ed1fae67b434ae774cc6137ca38b980d5`.
- Remediation evidence and limitations: `tests/blind/remediation/REMEDIATION_RESULTS.md`.

## Remediation evidence-complete record index

- Evidence file: `tests/evidence/remediation-acceptance-final.json`.
- Records:
  - `remediation-tc-01-20260813`, `remediation-tc-02-20260813`, `remediation-tc-03-20260813`, `remediation-tc-04-20260813`, `remediation-tc-05-20260813`, `remediation-tc-06-20260813`, `remediation-tc-07-20260813`, `remediation-tc-08-20260813`
  - `remediation-tc-09-20260813`, `remediation-tc-10-20260813`, `remediation-tc-11-20260813`, `remediation-tc-12-20260813`, `remediation-tc-13-20260813`, `remediation-tc-14-20260813`, `remediation-tc-15-20260813`, `remediation-tc-16-20260813`
  - `remediation-tc-17-20260813`, `remediation-tc-18-20260813`, `remediation-tc-19-20260813`, `remediation-tc-20-20260813`, `remediation-tc-21-20260813`, `remediation-tc-22-20260813`, `remediation-tc-23-20260813`, `remediation-tc-24-20260813`
  - `remediation-tc-25-20260813`, `remediation-tc-26-20260813`, `remediation-tc-27-20260813`, `remediation-tc-28-20260813`, `remediation-tc-29-20260813`, `remediation-tc-30-20260813`, `remediation-tc-31-20260813`, `remediation-tc-32-20260813`
  - `remediation-tc-33-20260813`, `remediation-tc-34-20260813`, `remediation-tc-35-20260813`, `remediation-tc-36-20260813`, `remediation-tc-37-20260813`, `remediation-tc-38-20260813`, `remediation-tc-39-20260813`, `remediation-tc-40-20260813`
  - `remediation-tc-41-20260813`, `remediation-tc-42-20260813`, `remediation-tc-43-20260813`, `remediation-tc-44-20260813`, `remediation-tc-45-20260813`, `remediation-tc-46-20260813`, `remediation-tc-47-20260813`, `remediation-acceptance-f3-tc-48-20260813`
  - `remediation-acceptance-f3-tc-49-20260813`, `remediation-acceptance-f3-tc-50-20260813`, `remediation-acceptance-f3-tc-51-20260813`, `remediation-acceptance-f3-tc-52-20260813`, `remediation-acceptance-f3-tc-53-20260813`, `remediation-acceptance-f3-tc-54-20260813`, `remediation-acceptance-f3-tc-55-20260813`, `remediation-acceptance-f3-tc-56-20260813`
  - `remediation-acceptance-f3-tc-57-20260813`, `remediation-acceptance-f3-tc-58-20260813`, `remediation-acceptance-f3-tc-59-20260813`, `remediation-acceptance-f3-tc-60-20260813`, `remediation-acceptance-f3-tc-61-20260813`, `remediation-acceptance-f3-tc-62-20260813`, `remediation-acceptance-f3-tc-63-20260813`, `remediation-acceptance-f3-tc-64-20260813`
  - `remediation-acceptance-f3-tc-65-20260813`, `remediation-acceptance-f3-tc-66-20260813`, `remediation-acceptance-f3-tc-67-20260813`, `remediation-acceptance-f3-tc-68-20260813`, `remediation-acceptance-f3-tc-69-20260813`, `remediation-acceptance-f3-tc-70-20260813`, `remediation-acceptance-f3-tc-71-20260813`, `remediation-f4-tc-72-20260813`
  - `remediation-f4-tc-73-20260813`, `remediation-f4-tc-74-20260813`, `remediation-f4-tc-75-20260813`, `remediation-f4-tc-76-20260813`, `remediation-f4-tc-77-20260813`, `remediation-f4-tc-78-20260813`, `remediation-f4-tc-79-20260813`, `remediation-f4-tc-80-20260813`
  - `remediation-f4-tc-81-20260813`, `remediation-f4-tc-82-20260813`, `remediation-f4-tc-83-20260813`, `remediation-f4-tc-84-20260813`, `remediation-f4-tc-85-20260813`, `remediation-f4-tc-86-20260813`, `remediation-f4-tc-87-20260813`, `remediation-f4-tc-88-20260813`
  - `remediation-f4-tc-89-20260813`, `remediation-f4-tc-90-20260813`, `remediation-f4-tc-91-20260813`, `remediation-f4-tc-92-20260813`, `remediation-f5-tc-93-20260813`, `remediation-f5-tc-94-20260813`, `remediation-f5-tc-95-20260813`, `remediation-f5-tc-96-20260813`
  - `remediation-f5-tc-97-20260813`, `remediation-f5-tc-98-20260813`, `remediation-f5-tc-99-20260813`, `remediation-f5-tc-100-20260813`, `remediation-f5-tc-101-20260813`, `remediation-f5-tc-102-20260813`, `remediation-f5-tc-103-20260813`, `remediation-f5-tc-104-20260813`
  - `remediation-f5-tc-105-20260813`, `remediation-f5-tc-106-20260813`, `remediation-f5-tc-107-20260813`, `remediation-f5-tc-108-20260813`, `remediation-f5-tc-109-20260813`, `remediation-f5-tc-110-20260813`, `remediation-f5-tc-111-20260813`, `remediation-f5-tc-112-20260813`
  - `remediation-f5-tc-113-20260813`, `remediation-f5-tc-114-20260813`, `remediation-package-01-20260813`
