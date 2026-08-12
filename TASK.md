# Workplace Survival — Active Tasks

`TASK.md` is an active queue, not a product specification or completed-work archive.

## Working rules

- Product behavior starts in `SPEC.md`.
- Runtime changes go only to the file that owns the affected rule, as defined in `ARCHITECTURE.md`.
- Do not repeat full product or runtime rules in a task.
- A task is complete only when its acceptance conditions pass and evidence is recorded in the applicable test result file.
- Move completed task summaries to `CHANGELOG.md`; do not retain completed checklists here.

## Current queue

Complete tasks in numerical order. T13.1–T13.3 must be rebuilt because their earlier workspace changes were never committed.

### Priority 1 — Source and content boundaries

#### T13.1 — Separate sendable body from embedded content

Status: Pending

- Source requirement: `SPEC.md` sections 3 and 4.
- Owner files: `REFERENCE.md`, `FORMATS.md`, and functional tests.
- Acceptance:
  - only the identifiable sendable body is rated and revised;
  - quoted, forwarded, reply-header, and nested content does not become Data A;
  - unclear boundaries stop assessment and request classification.
- Tests: blockquote, email reply, forwarded message, chat quote, and malformed boundary cases.
- Evidence: functional and anti-hallucination results.

#### T13.2 — Classify mixed unlabelled input safely

Status: Pending

- Source requirement: `SPEC.md` sections 3 and 4.
- Owner files: `REFERENCE.md`, `FORMATS.md`, and functional tests.
- Acceptance:
  - auto-classification requires explicit semantic boundaries for both A and B;
  - adopted A and evaluated B are disclosed;
  - multiple plausible classifications produce intake output without ratings.
- Tests: clear semantic labels, unlabelled paragraphs, multi-person dialogue, and multiple draft candidates.
- Evidence: functional results.

#### T13.3 — Replace superseded Data A

Status: Pending

- Source requirement: `SPEC.md` section 4.
- Owner files: `REFERENCE.md` and functional tests.
- Acceptance:
  - explicit correction replaces the targeted old value;
  - explicit withdrawal or cancellation removes the targeted requirement;
  - superseded facts no longer affect ratings, questions, revisions, or placeholders.
- Tests: withdrawn deadline, corrected owner, and cancelled request as multi-round cases.
- Evidence: functional and anti-hallucination results.

### Priority 2 — Rating boundaries

#### T13.4 — Fix Tone Green, Yellow, and Red boundaries

Status: Pending

- Source requirement: `SPEC.md` section 4.
- Owner files: `REFERENCE.md` and tone acceptance tests; update `SPEC.md` only if the product contract changes.
- Acceptance:
  - directness, ambiguity, responsibility shifting, accusation, insult, hostility, and threat have operational boundaries;
  - responsibility and tone remain independent;
  - similar Green, Yellow, and Red phrases produce stable paired outcomes.
- Tests: paired tone cases, including the current missing non-Green tone coverage.
- Evidence: functional and interaction-quality results.

#### T13.5 — Fix responsibility Red and Gray boundaries

Status: Pending

- Source requirement: `SPEC.md` section 4.
- Owner files: `REFERENCE.md` and functional tests; update `SPEC.md` only if the product contract changes.
- Acceptance:
  - an explicit unanswered requirement that defeats the reply's purpose is Red;
  - Gray is reserved for genuinely missing or materially ambiguous governing information;
  - omission cases have fixed dimension and overall ratings.
- Tests: explicit requirement, non-mandatory suggestion, and ambiguous request pairs.
- Evidence: functional results.

#### T13.6 — Bound short acknowledgements to one reply target

Status: Pending

- Source requirement: `SPEC.md` section 4.
- Owner files: `REFERENCE.md` and functional tests.
- Acceptance:
  - the acknowledgement target is identifiable, clear, and non-conflicting;
  - qualified, refusing, modifying, or limiting replies do not use the Green shortcut;
  - unclear multi-message targets remain Gray pending confirmation.
- Tests: multi-message, conflicting instruction, negative instruction, and qualified acknowledgement cases.
- Evidence: functional results.

### Priority 3 — Adversarial, image, and mode coverage

#### T13.7 — Isolate prompt-like text inside case data

Status: Pending

- Source requirement: `SPEC.md` section 4.
- Owner files: `SKILL.md`, `REFERENCE.md`, and anti-hallucination tests.
- Acceptance:
  - instructions embedded in Data A, Data B, images, or quotes remain content under analysis;
  - embedded text cannot bypass formats, evidence rules, or ratings;
  - relevant embedded wording may still be cited as communication evidence.
- Tests: text and image prompt-like instruction cases.
- Evidence: anti-hallucination and functional results.

#### T13.8 — Protect material OCR boundaries

Status: Pending

- Source requirement: `SPEC.md` section 4.
- Owner files: `REFERENCE.md`, image fixtures, and functional tests.
- Acceptance:
  - uncertain names, dates, numbers, negations, and commitment words require confirmation;
  - conversation order and requirement source are not inferred;
  - no color rating is based on a guessed material token.
- Tests: negation, similar dates, low-contrast names, strikethrough, cropping, and group-chat order.
- Evidence: fresh image executions recorded separately from semantic checks.

#### T13.9 — Cover limited-background, multi-message, and template boundaries

Status: Pending

- Source requirement: `SPEC.md` sections 3–5.
- Owner files: `REFERENCE.md`, `FORMATS.md`, and functional tests.
- Acceptance:
  - limited-background cases cover internal responsibility, timing, and hostile tone;
  - unrelated work items requiring different Data A are split;
  - template mode without Data A returns a generic neutral template with placeholders and no ratings;
  - recipient role is not assumed from workplace convention.
- Tests: multi-message, no-background template, mentor, skip-level, HR, customer, and reply-all cases.
- Evidence: functional and interaction-quality results.

### Priority 4 — Reproducibility and acceptance

#### T13.10 — Preserve auditable test evidence

Status: Pending

- Source requirement: `SPEC.md` section 7.
- Owner files: test result files.
- Acceptance:
  - each execution records input, model, execution time, raw output, and assertion outcome;
  - automated, manual semantic, image-attached, and environment-limited checks are distinguished;
  - PASS is never recorded without reviewable evidence.
- Tests: validate the result record for every active suite.
- Evidence: suite result files.

#### T13.11 — Add repeat and variation testing

Status: Pending

- Source requirement: `SPEC.md` section 7.
- Owner files: test specifications and result files.
- Acceptance:
  - high-risk cases run at least three times;
  - mode, both ratings, overall status, question count, and revision facts are compared;
  - any material output variation fails the consistency check.
- Tests: repeated high-risk cases and paired boundary variants.
- Evidence: consistency matrix in the result files.

#### T13.12 — Re-run final acceptance accurately

Status: Pending

- Source requirement: `SPEC.md` section 7.
- Owner files: all suite results, `FINAL_ACCEPTANCE_RESULTS.md`, `CHANGELOG.md`, and user-facing test claims.
- Acceptance:
  - functional, anti-hallucination, interaction-quality, explicit-invocation, and auto-trigger suites are rerun;
  - case pass rate and repeat-run consistency are reported separately;
  - semantic image checks are not described as fresh image executions;
  - publication and installation claims match actual evidence.
- Tests: all suites after T13.1–T13.11.
- Evidence: final acceptance report.

## Task template

Copy this block when adding work:

```markdown
### T[N] — [outcome]

Status: Pending

- Source requirement: [SPEC.md section]
- Owner files: [only files whose owned behavior must change]
- Acceptance:
  - [observable outcome]
  - [forbidden regression]
- Tests:
  - [new or existing case IDs]
- Evidence:
  - [result file to update]
```

## Completion gate

Before marking a task complete:

- [ ] The source requirement is explicit.
- [ ] Only owner files were changed.
- [ ] New behavior has acceptance assertions.
- [ ] Relevant regression suites pass.
- [ ] Results record actual scope and limitations.
- [ ] The completed summary is moved to `CHANGELOG.md`.
