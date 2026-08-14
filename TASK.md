# Workplace Survival — Active Tasks

`TASK.md` is an active queue, not a product specification or completed-work archive.

## Working rules

- Product behavior starts in `SPEC.md`.
- Runtime changes go only to the file that owns the affected rule, as defined in `ARCHITECTURE.md`.
- Do not repeat full product or runtime rules in a task.
- A task is complete only when its acceptance conditions pass and evidence is recorded in the applicable test result file.
- Keep completed items checked in the current phase so progress stays visible; also summarize completed outcomes in `CHANGELOG.md`. Archive the phase after every item is complete.
- Use each task's checkbox as the visible status: `[ ]` means pending and `[x]` means completed.

## Current queue

Complete tasks in numerical order. T13.1–T13.3 must be rebuilt because their earlier workspace changes were never committed.

### Priority 1 — Source and content boundaries

#### T13.1 — Separate sendable body from embedded content

- [x] Completed

- Source requirement: `SPEC.md` section 3, `Embedded content in Data B`.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, `.cursor/skills/workplace-survival/FORMATS.md`, and `tests/TEST_CASES.md`.
- Acceptance:
  - only the identifiable sendable body is rated and revised;
  - quoted, forwarded, reply-header, and nested content does not become Data A solely because it appears inside Data B;
  - unclear boundaries stop assessment and request classification.
- Tests: blockquote, email reply, forwarded message, chat quote, and malformed boundary cases.
- Evidence: functional and anti-hallucination results.

#### T13.2 — Classify mixed unlabelled input safely

- [x] Completed

- Source requirement: `SPEC.md` sections 3 and 5, mixed-input classification and provenance disclosure.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, `.cursor/skills/workplace-survival/FORMATS.md`, and `tests/TEST_CASES.md`.
- Acceptance:
  - auto-classification requires explicit semantic boundaries for both A and B;
  - adopted A and evaluated B are disclosed;
  - multiple plausible classifications produce intake output without ratings.
- Tests: clear semantic labels, unlabelled paragraphs, multi-person dialogue, and multiple draft candidates.
- Evidence: functional results.

#### T13.3 — Replace superseded Data A

- [x] Completed

- Source requirement: `SPEC.md` section 4, `Effective Data A`.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, and `tests/TEST_CASES.md`.
- Acceptance:
  - explicit correction replaces the targeted old value;
  - explicit withdrawal or cancellation removes the targeted requirement;
  - superseded facts no longer affect ratings, questions, revisions, or placeholders.
- Tests: withdrawn deadline, corrected owner, and cancelled request as multi-round cases.
- Evidence: functional and anti-hallucination results.

### Priority 2 — Rating boundaries

#### T13.4 — Fix Tone Yellow and Red boundaries

- [x] Completed

- Source requirement: `SPEC.md` section 4.
- Owner files: `.cursor/skills/workplace-survival/REFERENCE.md` and `tests/TEST_CASES.md`; update `SPEC.md` first only if the product contract changes.
- Acceptance:
  - directness, ambiguity, responsibility shifting, accusation, insult, hostility, and threat have operational boundaries;
  - responsibility and tone remain independent;
  - similar safe control, Yellow, and Red phrases produce stable paired outcomes.
- Tests: paired Tone Yellow and Red cases with similar Green controls, covering the current missing non-Green tone assertions.
- Evidence: functional and interaction-quality results.

#### T13.5 — Fix responsibility Red and Gray boundaries

- [x] Completed

- Source requirement: `SPEC.md` section 4.
- Owner files: `.cursor/skills/workplace-survival/REFERENCE.md` and `tests/TEST_CASES.md`; update `SPEC.md` first only if the product contract changes.
- Acceptance:
  - an explicit unanswered requirement that defeats the reply's purpose is Red;
  - Gray is reserved for genuinely missing or materially ambiguous governing information;
  - omission cases have fixed dimension and overall ratings.
- Tests: explicit requirement, non-mandatory suggestion, and ambiguous request pairs.
- Evidence: functional results.

#### T13.6 — Bound short acknowledgements to one reply target

- [x] Completed

- Source requirement: `SPEC.md` section 4.
- Owner files: `.cursor/skills/workplace-survival/REFERENCE.md` and `tests/TEST_CASES.md`.
- Acceptance:
  - the acknowledgement target is identifiable, clear, and non-conflicting;
  - qualified, refusing, modifying, or limiting replies do not use the Green shortcut;
  - unclear multi-message targets remain Gray pending confirmation.
- Tests: multi-message, conflicting instruction, negative instruction, and qualified acknowledgement cases.
- Evidence: functional results.

### Priority 3 — Adversarial, image, and mode coverage

#### T13.7 — Isolate prompt-like text inside case data

- [x] Completed

- Source requirement: `SPEC.md` section 4, `Evidence and isolation`.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, `tests/TEST_CASES.md`, `tests/fixtures/generate_fixtures.py`, the generated prompt-like image fixture, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - instructions embedded in Data A, Data B, images, or quotes remain content under analysis;
  - embedded text cannot bypass formats, evidence rules, or ratings;
  - relevant embedded wording may still be cited as communication evidence.
- Tests: text and image prompt-like instruction cases.
- Evidence: anti-hallucination and functional results.

#### T13.8 — Protect material OCR boundaries

- [x] Completed

- Source requirement: `SPEC.md` section 4.
- Owner files: `.cursor/skills/workplace-survival/REFERENCE.md`, `tests/fixtures/generate_fixtures.py`, generated image fixtures, `tests/TEST_CASES.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - uncertain names, dates, numbers, negations, and commitment words require confirmation;
  - materially uncertain conversation order or requirement source is not inferred;
  - no color rating is based on a guessed material token.
- Tests: negation, similar dates, low-contrast names, strikethrough, cropping, and group-chat order.
- Evidence: fresh image executions recorded separately from semantic checks.

#### T13.9 — Cover limited-background, multi-message, and template boundaries

- [x] Completed

- Source requirement: `SPEC.md` sections 3–5.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, `.cursor/skills/workplace-survival/FORMATS.md`, and `tests/TEST_CASES.md`.
- Acceptance:
  - limited-background cases cover internal responsibility, timing, and hostile tone;
  - unrelated work items requiring different Data A are split;
  - template mode without Data A returns a generic neutral template with placeholders and no ratings;
  - recipient role is not assumed from workplace convention.
- Tests: multi-message, no-background template, mentor, skip-level, HR, customer, and reply-all cases.
- Evidence: functional and interaction-quality results.

### Priority 4 — Reproducibility and acceptance

#### T13.10 — Preserve auditable test evidence

- [x] Completed

- Source requirement: Engineering evidence gap — `SPEC.md` section 7 requires passing suites, while current result files do not preserve enough execution evidence to reproduce every PASS. No product behavior change.
- Owner files: existing suite files matching `tests/*_RESULTS.md`, `tests/evidence/`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - each execution records input, model, execution time, raw output, and assertion outcome;
  - automated, manual semantic, image-attached, and environment-limited checks are distinguished;
  - PASS is never recorded without reviewable evidence.
- Tests: validate the result record for every active suite.
- Evidence: suite result files.

#### T13.11 — Add repeat and variation testing

- [x] Completed

- Source requirement: Engineering consistency gap — current high-risk cases have no repeated-run stability requirement. No product behavior change.
- Owner files: `tests/TEST_CASES.md`, `tests/TEST_RESULTS.md`, `tests/evidence/`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - high-risk cases run at least three times;
  - mode, both ratings, overall status, question count, and revision facts are compared;
  - any material output variation fails the consistency check.
- Tests: repeated high-risk cases and paired boundary variants.
- Evidence: consistency matrix in the result files.

#### T13.12 — Re-run final acceptance accurately

- [x] Completed

- Source requirement: `SPEC.md` section 7 acceptance requirement plus the evidence and consistency gaps tracked by T13.10–T13.11.
- Owner files: all suite case/result files, `tests/evidence/`, `tests/FINAL_ACCEPTANCE_RESULTS.md`, `CHANGELOG.md`, `README.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - functional, anti-hallucination, interaction-quality, explicit-invocation, and auto-trigger suites are rerun;
  - case pass rate and repeat-run consistency are reported separately;
  - semantic image checks are not described as fresh image executions;
  - publication and installation claims match actual evidence.
- Tests: all suites after T13.1–T13.11.
- Evidence: final acceptance report.

### Phase 14 — Independent test-strength validation

#### T14.1 — Mutation testing

- [x] Completed

- Source requirement: Test-quality follow-up after T13 final acceptance; no product behavior change.
- Owner files: `tests/mutation/`, surviving-mutant regression cases, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - each mutant changes one observable rule in an isolated worktree;
  - system output generation cannot read test expectations;
  - every non-equivalent survivor becomes a regression test;
  - mutation score and method limitations are recorded;
  - no mutant is merged into the baseline runtime.
- Evidence: mutation plan, raw outputs, mutant diffs, and final mutation report.

#### T14.2 — Cloud-isolated blind holdout testing

- [x] Completed

- Source requirement: Independent accuracy follow-up after mutation testing; no product behavior change during scoring.
- Owner files: `tests/blind/`, `TASK.md`, `CHANGELOG.md`, `README.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - unseen cases are generated in a cloud branch without prior holdout artifacts;
  - heterogeneous gold labels are frozen before Skill output generation;
  - Skill output generators cannot read gold labels or scoring thresholds;
  - cases, gold, runtime, raw outputs, and images are hash-linked;
  - critical invariant, route, rating, question, and revision metrics are reported;
  - failures are preserved before any product or test change.
- Evidence: cloud agent branch, frozen artifacts, raw outputs, adjudication, score report, and method limitations.

#### T14.3 — Blind defect remediation

- [x] Completed

- Source requirement: Confirmed product defects from the cloud blind diagnostic.
- Owner files: `SPEC.md`, runtime Skill files, public regression cases, and `tests/blind/remediation/`.
- Acceptance:
  - all 18 diagnostic cases are re-triaged before product changes;
  - benchmark/gold ambiguities do not become production rules;
  - confirmed defects receive generalized rules and public regressions;
  - existing functional and targeted suites do not regress;
  - each remediation rule is protected by a killed mutant.
- Evidence: triage, regression summary, remediation mutant diffs, raw outputs, and oracle results.

#### T14.4 — Evidence-complete remediation acceptance

- [x] Completed

- Source requirement: Validate remediation runtime with the T13.10 evidence contract before merging to `main`.
- Owner files: suite result files, `tests/evidence/`, remediation reports, `README.md`, `CHANGELOG.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - Functional TC-01–TC-114 and every active targeted suite are rerun;
  - all 13 image cases are opened and hash-linked;
  - every PASS has raw input/output, assertions, runtime commit, and exact result citation;
  - package validation is reported separately from behavioral cases;
  - summary-only remediation results are replaced by evidence-complete current results.
- Evidence: remediation acceptance plan, full evidence JSON, package record, validator output, and updated acceptance report.

#### T14.5 — Blind benchmark methodology v2

- [x] Completed

- Source requirement: Separate benchmark/scoring defects from product behavior before a new hidden holdout.
- Owner files: `tests/benchmark/`, `TASK.md`, `CHANGELOG.md`, `README.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - SUT-visible Data A is explicit and evaluator-only notes cannot affect gold;
  - question and revision claims use ontology/semantic matching rather than exact token equality;
  - gold disagreement, adjudication, uncertainty, and optional human review are represented;
  - cloud cases, images, gold, outputs, and evaluations are content-addressed and immutable;
  - scorer rejects unsupported claims, missing required concepts, changed artifacts, and excessive gold uncertainty;
  - methodology tests and negative gates pass without changing runtime Skill files.
- Evidence: methodology contract, ontology, validators/scorer, synthetic fixtures, unit results, and runtime diff check.

#### T14.6 — Fresh benchmark v2 cloud holdout

- [ ] Completed

- Source requirement: Measure post-remediation unseen-case performance with methodology v2.
- Owner files: `tests/benchmark/v2-holdout/`, benchmark result summaries, `TASK.md`, `CHANGELOG.md`, `README.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - runtime is frozen at `main@9d48b04`;
  - unseen cases contain explicit SUT-visible Data A and separate oracle notes;
  - heterogeneous gold and cloud artifacts satisfy methodology v2;
  - each case uses an independent cloud SUT context;
  - dual extraction and semantic matching precede scoring;
  - preregistered metrics and failures are preserved without modifying gold.
- Evidence: frozen manifests, cases/images, labels/adjudication, raw outputs, matches, score report, and cloud attestations.

#### T14.7 — Benchmark methodology v3 scorer hardening

- [x] Completed

- Source requirement: Preserve the v2 `SCORER_ERROR` outcome and prevent zero-denominator metrics or scorer exceptions from destroying formal evidence. No product behavior change.
- Owner files: `tests/benchmark/v3/`, `TASK.md`, `CHANGELOG.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - v2 remains archived and is never rescored;
  - zero denominators produce `NOT_APPLICABLE`, never 0, 1, or an exception;
  - preregistered coverage gates reject holdouts without question and revision coverage before SUT execution;
  - every scorer invocation writes one immutable success or failure envelope;
  - unit and mutation tests kill zero-denominator, disabled-coverage, and missing-failure-envelope defects;
  - validation uses synthetic fixtures and does not supply v2 artifacts to the v3 scorer.
- Evidence: v3 methodology contract, unit results, mutation results, validation report, and empty runtime diff.

#### T14.8 — Fresh benchmark v3 unseen holdout

- [x] Completed

- Source requirement: Exercise methodology v3 on a fresh unseen case set and enforce coverage before SUT execution.
- Owner files: `tests/benchmark/v3-holdout/`, `TASK.md`, and `CHANGELOG.md`.
- Acceptance:
  - cases and images are generated in an isolated cloud context without prior benchmark content;
  - three independent gold families and a fourth-family adjudicator preserve all votes;
  - v3 question/revision coverage gates execute before SUT;
  - invalid coverage prevents SUT, extraction, matching, and formal scoring;
  - the complete invalid-coverage evidence chain is immutable.
- Evidence: holdout plan/brief, cases/images, labels/adjudication, transcript audits, coverage report, result summary, and invalid-coverage manifest.

#### T14.9 — v3.1 required-question case-design remediation

- [x] Completed

- Source requirement: Correct the benchmark-design cause of v3 `INVALID_COVERAGE` without changing frozen v3 cases or gold.
- Owner files: `tests/benchmark/v3_1/`, `TASK.md`, `CHANGELOG.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - the invalid v3 holdout remains immutable and no case content is reused;
  - six distinct question candidates are overprovisioned;
  - placeholder, qualification, omission, and dominant-Red escape routes reject a candidate;
  - removing dependency or supplying the answer removes question necessity;
  - unit and mutation tests protect every construction transition.
- Evidence: coverage triage, v3.1 case brief, executable contract, unit results, and mutation results.

#### T14.10 — Fresh benchmark v3.1 unseen holdout

- [ ] Completed

- Source requirement: Measure unseen-case performance with methodology v3 plus the v3.1 question-case construction contract. No product behavior change during scoring.
- Owner files: `tests/benchmark/v3_1-holdout/`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - unseen millinery-domain cases satisfy the v3.1 construction contract and coverage gates before SUT;
  - each case uses a distinct cloud SUT context;
  - SUT artifacts are extracted from per-case source commits; shared-holdout delivery commits are a log, not the freeze parent;
  - dual extraction and semantic matching precede a single v3 scorer invocation;
  - preregistered metrics and failures are preserved without modifying gold or runtime Skill files.
- Evidence: gold/output manifests, protocol audits, source index, delivery log, score report.
- Progress: gold freeze, SUT output freeze, extraction snapshot freeze, and evaluation/match freeze are done; scoring is not.

## Task template

Copy this block when adding work:

```markdown
### T[N] — [outcome]

- [ ] Completed

- Source requirement: [SPEC.md section / engineering evidence gap with no product behavior change]
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
