# Workplace Survival Compaction Results

## Changes

- Added three core safeguards to `SKILL.md`: independent dimensions, fixed-format intake enforcement, and revision-to-Data-B adoption.
- Removed the limited-background entry sequence and template routing duplication from `REFERENCE.md`; routing remains owned by `SKILL.md`.
- Removed rating semantics from `FORMATS.md`; rating semantics remain owned by `REFERENCE.md`.
- Kept case isolation and follow-up summaries in `SKILL.md` because they are part of its core workflow and high-priority safeguards.
- Kept detailed rating criteria in `REFERENCE.md`, fixed structures in `FORMATS.md`, and non-normative examples in `EXAMPLES.md`.

## Size

- `SKILL.md`: 107 to 110 lines.
- `REFERENCE.md`: 351 to 347 lines.
- `FORMATS.md`: 129 to 123 lines.
- `EXAMPLES.md`: unchanged at 322 lines.
- Normative files combined: 587 to 580 lines.
- `SKILL.md` remains within the 100–150-line target and below the 500-line maximum.

The main skill file gained three explicit safeguards while duplicated normative content was removed from supporting files. Net normative documentation decreased by seven lines.

## Terminology audit

- `Data A`: consistent.
- `Data B`: consistent.
- `Normal mode`: consistent.
- `Limited-background mode`: consistently hyphenated.
- `Message-template mode`: consistently hyphenated.
- No deprecated or mixed mode-name variant was found.

## Full regression

- Functional cases TC-01 through TC-30: 30 passed, 0 failed.
- Anti-hallucination cases AH-01 through AH-06: 6 passed, 0 failed.
- Interaction-quality cases IQ-01 through IQ-06: 6 passed, 0 failed.
- Total: 42 passed, 0 failed.
- Unsupported facts: 0.
- Interaction defects: 0.
- Behavior changes against expected results: 0.

## T10.4 conclusion

Rule ownership is clearer, `SKILL.md` retains the core safeguards and workflow, terminology is consistent, and the complete 42-case regression shows no loss of existing behavior.

## Post-T11.5 note

This file preserves the historical T10.4 compaction snapshot and its then-current TC-01–TC-30 regression. The later short-acknowledgement and register-preservation changes, current TC-01–TC-32 regression, and 57-case acceptance result are recorded in `TASK.md`, `tests/TEST_RESULTS.md`, and `tests/FINAL_ACCEPTANCE_RESULTS.md`.
