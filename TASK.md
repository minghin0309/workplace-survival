# Workplace Survival — Active Tasks

`TASK.md` is an active queue, not a product specification or completed-work archive.

## Working rules

- Product behavior starts in `SPEC.md`.
- Runtime changes go only to the file that owns the affected rule, as defined in `ARCHITECTURE.md`.
- Do not repeat full product or runtime rules in a task.
- A task is complete only when its acceptance conditions pass and evidence is recorded in the applicable test result file.
- Move completed task summaries to `CHANGELOG.md`; do not retain completed checklists here.

## Current queue

No active tasks.

## Task template

Copy this block when adding work:

```markdown
### T[N] — [outcome]

Status: Pending

- Source requirement: [SPEC.md section or confirmed product decision]
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
