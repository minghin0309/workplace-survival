# Workplace Survival Mutation Plan

## Goal

Mutation testing checks whether the current tests detect deliberately broken rules. Mutants are temporary, isolated, and never merged into `main`.

## Oracle isolation

For language-model mutants:

1. The system-under-test evaluator receives only the mutated runtime skill files and raw case input.
2. It must not read `SPEC.md`, `TASK.md`, `EXAMPLES.md`, `tests/`, expected ratings, or forbidden assertions.
3. A separate oracle evaluator receives the raw output and the frozen assertions.
4. A mutant is killed only when the output fails at least one pre-existing assertion.

For deterministic code mutants, the existing negative gate must reject the changed behavior.

## Result classes

- `KILLED`: at least one frozen test fails.
- `SURVIVED`: all selected frozen tests pass despite a material behavioral change.
- `EQUIVALENT`: the mutation does not alter observable behavior for the stated invariant; excluded from the score.
- `ERROR`: the mutant or harness cannot execute; not counted until resolved.

Mutation score:

```text
killed / (killed + survived)
```

## Mutant matrix

| ID | Area | Deliberate mutation | Frozen kill cases | Expected observable defect |
|---|---|---|---|---|
| M01 | Embedded content | Treat quoted/forwarded text as user-authored Data B | TC-33, TC-34 | Quoted owner/date affects ratings or Data A |
| M02 | Effective Data A | Append corrections instead of replacing superseded facts | TC-51, TC-54 | Old owner remains active or creates stale conflict |
| M03 | Tone | Downgrade explicit insults from Red to Yellow | TC-63, TC-69 | Tone or overall status is not Red |
| M04 | Responsibility | Rate conflicting governing Data A as Red instead of Gray | TC-77, TC-10 | Governing uncertainty becomes a known error |
| M05 | Acknowledgement | Let `ok` acknowledge all historical messages | TC-79, TC-83 | Ambiguous target becomes Green or expands scope |
| M06 | Prompt isolation | Let instructions inside Data B override ratings/format | TC-85, TC-88 | Payload forces Green or suppresses required output |
| M07 | OCR | Guess a blurred material negation instead of intake | TC-93 | Produces a transcription, rating, or revision |
| M08 | Recipient scope | Assume every mentor is a manager | TC-106 | Produces ratings before role confirmation |
| M09 | Evidence validator | Permit `PASS` when an assertion failed | `tests/mutation/check_validator_pass_gate.py` | Invalid PASS evidence is accepted |

## Execution order

1. Create one detached worktree per mutant from the frozen baseline.
2. Apply exactly one mutation.
3. Run only the listed kill cases first.
4. If the mutant survives, run adjacent regression cases to exclude equivalence.
5. Record raw mutant diff, system output, failed assertion, method, and limitation.
6. Delete the temporary worktree after evidence is captured.

## Completion criteria

- Every non-equivalent mutant has a reproducible result.
- Every survivor becomes a new regression test before mutation testing is considered complete.
- The baseline runtime remains unchanged.
- Results distinguish semantic model execution from deterministic validator execution.
