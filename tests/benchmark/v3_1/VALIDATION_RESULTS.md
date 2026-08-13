# v3.1 Question-Case Construction Validation

- Unit tests: 11 passed
- Mutation tests: 4/4 killed
- Mutation score: 100%
- v3.1 cases generated: 0
- SUT executions: 0
- Formal scorer invocations: 0
- Runtime Skill changes: none

Validated construction behavior:

- six distinct primary missing concepts are required;
- a clean baseline candidate requires a question;
- placeholder-safe, qualification-safe, or omission-safe candidates are rejected;
- removing the recipient requirement or decision dependency removes question necessity;
- supplying the answer enables safe completion without the question;
- adding an independent direct Red defect rejects clean question-candidate status;
- an extra duplicate-concept candidate is rejected.

Killed mutants:

- `M1_PLACEHOLDER_ESCAPE_IGNORED`;
- `M2_DOMINANT_RED_IGNORED`;
- `M3_SUPPLIED_ANSWER_STILL_MISSING`;
- `M4_DUPLICATE_CONCEPT_ALLOWED`.

An initial minimum-count mutant survived because it was equivalent: requiring all six unique concepts already implied at least six candidates. It was removed rather than counted and replaced with the observable duplicate-concept mutant.

The invalid v3 holdout remains immutable and no case content, image, label, or oracle note is reused by the v3.1 brief.
