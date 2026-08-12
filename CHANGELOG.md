# Changelog

This file records completed outcomes. Detailed assertions and execution evidence remain in `tests/`.

## Unreleased

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
