# Changelog

This file records completed outcomes. Detailed assertions and execution evidence remain in `tests/`.

## Unreleased

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
