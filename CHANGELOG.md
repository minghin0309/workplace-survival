# Changelog

This file records completed outcomes. Detailed assertions and execution evidence remain in `tests/`.

## Unreleased

### S-001/S-002 Skill remediation

- Did not rescore or rewrite v3.2 attempt 2.
- Stopped treating a Data B-only date, name, or similar token as confirmed when Data A locates the governing value off-record and does not quote it.
- Kept the Data B answer rule for manager-requested values with no off-record source (TC-07).
- Rated unestablished authorization plus an external client/authority commitment Red, and required stripping or conditioning it in the same response.
- Added TC-115–TC-117.

### v3.2 manager-recipient case-design remediation

- Preserved v3.2 attempt 1 unchanged as `INVALID_COVERAGE`.
- Triaged why non-manager question candidates gold-routed `Scope` and produced one required question concept.
- Added a manager-recipient contract: exactly one non-manager routing case; question candidates cannot be that case.
- Passed 14 unit tests, including a negative fixture against the frozen attempt-1 envelope.
- Killed all 3 targeted recipient-contract mutants.
- Confirmed no Skill, gold, or attempt-1 case files changed.

### Fresh benchmark v3.2 unseen holdout

- Generated 18 concert-harpworks cases in an isolated cloud context and copied them with `git show`.
- Built audited Grok/Gemini/GPT gold with Claude-family adjudication; one gold-uncertain turn (4.17%).
- Applied v3.2 coverage before SUT: revision and uncertainty gates passed, but required questions covered only 1 concept across 1 case.
- Root cause: question candidates used non-manager recipients and were gold-routed `Scope`. Gold was not rewritten.
- Marked the attempt `INVALID_COVERAGE`, froze the evidence chain, and correctly prevented SUT and formal scoring.
- Confirmed no Skill defect because the runtime was never executed.

### Benchmark methodology v3.2 freeze-chain scoring

- Archived the v3.1 holdout as `SCORER_ERROR` and did not rescore it.
- Added a v3.2 scorer that validates evaluation → outputs → gold freeze documents itself and never calls v2 `main()`.
- Allowed extra freeze keys and `version` `3.1`/`3.2`; rejected v2 manifests.
- Required gold freeze roles `gold`, `ontology`, and `scorer`. Missing ontology is `INVALID_SCORING_INPUT`.
- Kept v3 metric policy: zero denominators are `NOT_APPLICABLE`; coverage gates run first; reports are immutable.
- Passed 12 synthetic unit tests and killed all 3 targeted scorer mutants.
- Confirmed no Skill, v2, v3 scorer, or v3.1 holdout files changed.
- Formal v3.2 scoring still requires a fresh unseen holdout.

### Fresh benchmark v3.1 single v3 scorer invocation

- Invoked frozen `score_semantic_v3.py` once against the evaluation snapshot.
- Coverage gates computed: 24 turns, 23 accepted, 6 question concepts / 6 cases, 70 revision concepts / 18 cases.
- v2 core aborted on `manifest schema` before metrics. Status `SCORER_ERROR`.
- Preserved the immutable envelope. No rerun. Gold, ontology, matches, and runtime Skill files were not modified.

### Fresh benchmark v3.1 semantic match freeze

- Ran one isolated Claude matcher with gold access on `cursor/v31-matcher-claude-17a0`; copied with `git show` and did not merge that branch.
- Mapped all 59 extracted claims; 57 semantic, 2 unsupported.
- Allowlisted inputs: extraction snapshot, canonical evaluations, raw outputs, canonical gold, ontology.
- Transcript audit: no prohibited content; authored-output re-read is `ACCEPTED_WITH_PROCEDURAL_DEVIATION`.
- Froze 12 evaluation artifacts against outputs manifest `993eb2a0…` and extraction snapshot `a406161c…`.
- Formal scoring ran once afterwards and recorded `SCORER_ERROR`. Runtime Skill files were not modified.

### Fresh benchmark v3.1 gold-blind extraction freeze

- Copied Claude and Gemini extractor blobs plus GPT adjudication from dedicated branches with `git show`; did not merge those branches.
- Covered 18 cases / 24 turns with exact-span claims; 0 unresolved disagreements.
- Kept Claude's 8 question / 51 revision claims after 10 count disagreements.
- Recorded transcript audits: no gold/oracle/ontology/scorer/image opens; shared-checkout harness collision is `PASS_WITH_PROCEDURAL_DEVIATION`.
- Froze 15 extraction artifacts against outputs manifest `993eb2a0…`.
- Matching and formal scoring have not started. Runtime Skill files were not modified.

### Fresh benchmark v3.1 isolated SUT freeze

- Executed 18 cases / 24 turns in distinct cloud contexts after valid gold coverage.
- Extracted each case from its own source commit; did not merge the seven shared-holdout delivery commits.
- Path-canonicalized heterogeneous raw/attestation files and wrapped Markdown without changing Skill text.
- Recorded transcript protocol audits: 0 prohibited v3.1 gold-content opens; procedural deviations preserved.
- Froze 46 output artifacts against gold manifest `2aea4832…`; canonical parent remains `f609800`.
- Extraction, matching, and formal scoring have not started. Runtime Skill files were not modified.

### v3.1 required-question case-design remediation

- Preserved the first v3 holdout unchanged as `INVALID_COVERAGE`.
- Triaged why direct Red defects, placeholder-safe gaps, and safely qualified provenance claims failed to yield required-question gold.
- Added a v3.1 brief with six distinct overprovisioned question candidates.
- Added mechanical dependency-removal, answer-supply, and dominant-Red design mutations.
- Passed 11 unit tests and killed all 4 non-equivalent case-design mutants.
- Removed an equivalent minimum-count mutant instead of counting a false mutation kill.

### Fresh benchmark v3 unseen holdout

- Generated 18 unseen cases, 24 turns, and two deterministic image-only drafts in an isolated cloud context.
- Built audited Grok/Kimi/GPT gold with Claude-family adjudication and preserved all vote distributions.
- Rejected an incomplete labeler attempt that read runtime Skill files.
- Applied v3 coverage before SUT execution: revision and uncertainty gates passed, but required questions covered only 2 concepts across 2 cases.
- Marked the holdout `INVALID_COVERAGE`, froze 25 evidence artifacts, and correctly prevented SUT execution and formal scoring.
- Confirmed no Skill defect because the runtime was never executed.

### Benchmark methodology v3 scorer hardening

- Archived benchmark v2 permanently as `SCORER_ERROR` without rescoring.
- Defined `NOT_APPLICABLE` zero-denominator semantics and preregistered minimum question/revision coverage gates.
- Added atomic, non-overwriting success and failure envelopes for every v3 scorer invocation.
- Added synthetic success, invalid-coverage, invalid-input, exception, and overwrite tests.
- Passed 10 unit tests and killed all 3 targeted scorer mutants after rejecting an initial import-error false kill.
- Confirmed no v2 holdout or runtime Skill files changed during v3 validation.

### Blind benchmark methodology v2

- Separated explicit SUT-visible Data A from evaluator-only construction notes.
- Replaced exact question/revision token equality with ontology aliases and semantic claim matching.
- Added gold uncertainty tiers, heterogeneous adjudication requirements, and a human-review template.
- Added content-addressed cloud artifact freezing and mutation checks.
- Passed six methodology tests without changing runtime Skill files.
- Preserved all historical blind scores unchanged.

### Blind defect remediation

- Re-triaged 18 diagnostic cases into 3 confirmed product defects and 15 benchmark/gold ambiguities.
- Fixed qualified intent-inference severity, causal-basis question priority, and intended-recipient preservation.
- Added TC-112–TC-114 without encoding disputed gold behavior.
- Passed the 114-case functional regression and targeted suites.
- Killed all three remediation-specific mutants.
- Completed evidence-backed acceptance: 139 behavioral cases and one separate package check passed.

### Cloud-isolated blind holdout — failed preregistered gate

- Generated 30 unseen cases and four images in a clean cloud branch without prior holdout artifacts.
- Built heterogeneous cloud gold with three labelers and a fourth-family adjudicator.
- Executed 36 turns in 30 distinct cloud SUT contexts without gold.
- Preserved raw outputs, hashes, attestations, final gold, semantic evaluations, and the immutable score report.
- Failed every preregistered accuracy threshold and recorded one critical recipient-scope violation.
- Recorded high gold disagreement and exact-token synonym penalties as benchmark limitations without changing the frozen score.

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
