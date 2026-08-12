# Workplace Survival Mutation Results

## Summary

- Product baseline: `main@8ca59a8`.
- Mutation harness commit: `cfb155f`.
- Mutants executed: 9.
- Killed: 9.
- Survived: 0.
- Equivalent: 0 counted.
- Errors: 0.
- Mutation score: `9 / (9 + 0) = 100%`.

## Results

| ID | Classification | Killing case | Observable failure |
|---|---|---|---|
| M01 | KILLED | TC-33 | Quoted owner/tone became user-authored content and changed ratings |
| M02 | KILLED | TC-51 | Corrected owner remained in conflict with superseded owner |
| M03 | KILLED | TC-63, TC-69 | Explicit and work-product insults were downgraded to Yellow |
| M04 | KILLED | TC-77, TC-10 | Conflicting governing Data A was rated Red instead of Gray |
| M05 | KILLED | TC-79, TC-83 | `ok` acknowledged unrelated or ambiguous historical targets |
| M06 | KILLED | TC-85, TC-88 | Data B forced Green and suppressed the required format |
| M07 | KILLED | TC-93 | Blurred negation was guessed and rated instead of using intake |
| M08 | KILLED | TC-106 | Mentor was assumed to be a manager before confirmation |
| M09 | KILLED | Validator PASS gate | Invalid PASS evidence containing a failed assertion was accepted |

## Isolation

- M01–M09 ran in separate detached worktrees.
- M01–M08 output generators were placed in separate contexts and explicitly restricted to mutated runtime files and raw inputs.
- Separate oracle contexts were explicitly restricted to frozen assertions and raw system outputs.
- M09 used an executable deterministic gate.
- No mutant was committed, pushed, or merged.
- The baseline runtime files were unchanged.

The subagent API did not provide filesystem access logs. M01–M08 isolation is therefore auditable through context IDs and recorded access instructions, but remains prompt-enforced rather than cryptographically proven.

## Evidence

Each directory under `tests/mutation/evidence/` contains:

- `mutant.diff`;
- raw system-under-test output;
- frozen-oracle result;
- execution metadata.

M03 initially used an incomplete mutation that left a second Red degradation rule intact. That preliminary run survived because the observable behavior was unchanged. It was treated as an invalid under-mutated attempt, corrected before scoring, and then killed by TC-63 and TC-69.

## Interpretation

The 100% score means the selected frozen tests detected all nine deliberate defects. It does not establish real-world message accuracy, hidden-case coverage, cross-model robustness, or live Cursor routing behavior.

No surviving non-equivalent mutant required a new regression case. Blind holdout testing remains the next independent validation stage.
