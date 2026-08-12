# Changelog

This file records completed outcomes. Detailed assertions and execution evidence remain in `tests/`.

## Unreleased

### Blind holdout attempt 2 — invalid frozen-image run

- Detected a frozen image whose bytes changed before output normalization.
- Rejected the run without calculating accuracy.
- Preserved unauthorized subagent branch/commit incidents and mechanical-envelope failures in the attempt report.
- Stopped local prompt-only retries pending genuinely external hidden cases.

### Blind holdout attempt 1 — invalid harness run

- Generated and gold-labelled a 30-case unseen holdout with four images.
- Stopped scoring after frozen evidence metadata failed the preregistered input-linkage contract.
- Reported no Skill accuracy metric and preserved both failed score attempts.
- Retired the consumed holdout and required a fresh-case retry with deterministic output normalization.

### T14.1 — Mutation testing

- Added nine isolated mutants across runtime rules and evidence validation.
- Separated mutated output generation from frozen-assertion oracle evaluation.
- Killed all nine non-equivalent mutants for a targeted mutation score of 100%.
- Preserved raw mutant diffs, system outputs, oracle failures, and context metadata.
- Confirmed that no mutant changed the baseline runtime or was merged.
- Recorded that the score validates only the selected defects; blind holdout testing remains pending.

### T13.12 — Evidence-complete final acceptance

- Executed all five active behavioral suites with T13.10-compliant raw evidence.
- Added current final-configuration explicit-invocation cases FCI-01–FCI-03.
- Passed 136 behavioral cases and one separate automated package check.
- Opened and validated all 13 image fixtures.
- Reported T13.11 repeat consistency separately: 14 cases × 3 runs with zero material variations.
- Replaced stale acceptance claims with current counts, runtime commit, evidence links, and dispatcher limitations.

### T13.11 — Repeat and variation testing

- Defined canonical expected observations for 14 high-risk and paired-boundary cases.
- Ran every selected case three times in distinct evaluator contexts.
- Compared route, both dimension ratings, overall status, question count, and canonical revision facts.
- Opened TC-89 and TC-93 images in all six image-repeat executions.
- Added validator gates for missing repeats, reused evaluator contexts, and material observation variation.
- Result: 42 passed executions and zero material variations.

### T13.10 — Auditable test evidence

- Added a canonical structured evidence schema with ordered raw input/output turns, model availability, UTC time, hashes, artifacts, assertions, results, limitations, and exact result citations.
- Distinguished automated, manual semantic, image-attached, routing-semantic, and environment-limited methods.
- Added a validator that rejects invalid timestamps, hashes, artifacts, citations, assertion states, method/result combinations, and repository-path escapes.
- Marked pre-T13.10 test summaries as historical summary-only evidence.
- Validated seven representative records across all five active suites; six passed and one historical explicit-invocation fixture was correctly recorded as `NOT_RUN`.
- Full evidence-complete suite execution remains pending under T13.12.

### T13.9 — Mode, case, and recipient boundaries

- Applied ordinary internal responsibility, timing, and tone ratings in Limited-background mode without inferring manager requirements.
- Kept related items sharing Data A in one case and split unrelated work matters before rating.
- Added a generic no-background manager template with placeholders and no ratings.
- Defined direct, skip-level, acting-manager, mentor, HR, customer, and reply-all scope boundaries.
- Preserved automatic-trigger narrowing while allowing explicit invocation to return scope guidance for named non-manager recipients.
- Added TC-100–TC-111.
- After correcting an initially over-strict recipient check, all 111 functional cases passed, including 13 attached-image executions.

### T13.8 — Material OCR and image-order boundaries

- Required confirmation for uncertain names, dates, numbers, negations, commitments, strikethrough status, and material crops.
- Stopped image-based Data B assessment when its new body could not be recognized reliably.
- Kept only affected dimensions Gray when material uncertainty was confined to Data A.
- Prevented order and authority inference from bubble position, side, color, avatar, or expected chat layout.
- Added seven reproducible ambiguous-image fixtures and TC-93–TC-99.
- All 99 functional cases passed, including 13 attached-image executions; targeted anti-hallucination remained 6 passed with zero unsupported facts.

### T13.7 — Prompt-like case data

- Treated instructions inside Data A, Data B, images, quotations, and forwarded content only as case data.
- Prevented payload text from overriding workflow, formats, evidence, ratings, classification, or confirmed facts.
- Preserved and cited prompt-like wording when ordinary responsibility or tone rules made it relevant.
- Distinguished legitimate outer user instructions and legitimate Green message content from control-like payload text.
- Added a portable prompt-like PNG fixture and TC-85–TC-92.
- All 92 functional cases passed, including six attached-image executions; targeted anti-hallucination remained 6 passed with zero unsupported facts.

### T13.6 — Short acknowledgement targets

- Limited pure short acknowledgements to one identifiable, clear, non-conflicting reply target.
- Allowed multiple grouped actions inside that one target without requiring restatement.
- Kept ambiguous or conflicting targets Gray and routed specific unanswered requests through T13.5 omission rules.
- Assessed qualifications, refusals, limitations, modifications, and negative-instruction violations without the Green shortcut.
- Prevented revisions from turning refusal or noncompliance into unsupported acceptance.
- Updated TC-31 and added TC-79–TC-84; 6 new and 73 existing text cases passed, with five image cases receiving semantic checks only.

### T13.5 — Responsibility Red and Gray boundaries

- Defined ordered responsibility Green, Yellow, Red, and Gray conditions.
- Classified unanswered sole requests, no-answer replies, and execution-gating omissions as Red.
- Reserved Gray for conflicting or materially ambiguous governing context and unresolved referents.
- Classified secondary non-critical omissions as Yellow and optional omissions as Green.
- Added fixed ratings to TC-11–TC-13 and TC-18 plus TC-72–TC-78; 7 new and 66 existing text cases passed, with five image cases receiving semantic checks only.

### T13.4 — Tone boundaries

- Defined ordered Green, Yellow, and Red tone conditions for directness, ambiguity, responsibility shifting, accusation, insult, hostility, threat, and degradation.
- Distinguished supported personalized blame from neutral process accountability and major unsupported accusations from qualified fault suggestions.
- Separated person-directed hostility, task-directed frustration, global work-product degradation, and specific operational defects.
- Kept responsibility and tone ratings independent.
- Added TC-58–TC-71; 14 new and 52 existing text cases passed, with five image cases receiving semantic checks only.

### T13.3 — Effective Data A replacement

- Maintained one current set of effective Data A for each case.
- Replaced explicitly corrected facts and removed explicitly withdrawn requirements, facts, and commitments.
- Preserved unrelated background and kept unmarked conflicting statements unresolved.
- Rebuilt follow-up output without stale ratings, questions, revisions, or placeholders.
- Added TC-50–TC-57; 8 new and 44 existing text cases passed, with five image cases receiving semantic checks only.

### T13.2 — Mixed-input classification

- Auto-classified background and draft text only when explicit semantic wording identifies both roles and boundaries.
- Preserved already-unambiguous input while requesting only unresolved roles or draft selection.
- Added exact adopted-background and evaluated-body provenance without recursively reclassifying phrases inside an outer payload.
- Combined mixed classification with embedded-content exclusion using one evaluated-body entry.
- Added TC-44–TC-49; 6 new and 38 existing text cases passed, with five image cases receiving semantic checks only.

### T13.1 — Embedded-content boundaries

- Limited ratings and revisions to the identifiable new body.
- Excluded clearly marked quotations, forwarded messages, reply headers, original-message blocks, nested forwarding, and chat previews.
- Allowed embedded content to become Data A only after separate explicit user designation.
- Added intake behavior for malformed boundaries and quote-only Data B.
- Added TC-33–TC-43; 11 new and 27 existing text cases passed, with five image cases receiving semantic checks only.

### Documentation consolidation

- Established one owner for each rule category.
- Retired the derivative implementation summary.
- Reduced `SPEC.md` to product intent, scope, and non-negotiable behavior.
- Converted `TASK.md` from an 800-line completed checklist into an active-only queue.
- Reduced runtime examples to representative edge cases; acceptance scenarios remain in `tests/TEST_CASES.md`.
- Re-ran 27 text cases after consolidation: 27 passed, 0 failed; five image cases passed semantic fixture checks without fresh image attachment.

## Initial release

### Product and runtime

- Created the `workplace-survival` Cursor skill.
- Implemented normal, limited-background, and message-template modes.
- Added independent responsibility-clarity and tone ratings with fixed overall-status priority.
- Added material, neutral follow-up questions with a three-question limit.
- Added minimal revisions, unknown-value placeholders, and same-language/register preservation.
- Added image input handling, multi-round state, and case isolation.
- Added bounded short-acknowledgement behavior.

### Validation

- Functional: 32 passed, 0 failed.
- Anti-hallucination: 6 passed, 0 failed.
- Interaction quality: 6 passed, 0 failed.
- Explicit invocation under the development configuration: 3 passed, 0 failed.
- Automatic trigger: 10 passed, 0 failed.
- Final recorded total: 57 passed, 0 failed.

### Distribution

- Added project and personal installation instructions.
- Added reproducible image fixtures and a publication manifest.
- Enabled automatic invocation after trigger validation.

See `tests/FINAL_ACCEPTANCE_RESULTS.md` for the release-level rollup and suite-specific result files for execution details.
