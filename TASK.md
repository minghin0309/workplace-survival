# Workplace Survival — Active Tasks

`TASK.md` is an active queue, not a product specification or completed-work archive.

## Working rules

- Product behavior starts in `SPEC.md`.
- Runtime changes go only to the file that owns the affected rule, as defined in `ARCHITECTURE.md`.
- Do not repeat full product or runtime rules in a task.
- A task is complete only when its acceptance conditions pass and evidence is recorded in the applicable test result file.
- Move completed task summaries to `CHANGELOG.md`; do not retain completed checklists here.

## Current queue

### T1 — Close known acceptance-coverage gaps

Status: Pending

- Source requirement: `SPEC.md` sections 3 and 4.
- Owner files: `tests/TEST_CASES.md` and applicable result files.
- Acceptance:
  - fixed cases distinguish Green, Yellow, and Red tone boundaries;
  - template mode without Data A produces a generic neutral template with placeholders and no ratings.
- Tests:
  - add paired tone-boundary cases;
  - add a no-background message-template case.
- Evidence:
  - update suite results only after the cases are executed.

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
