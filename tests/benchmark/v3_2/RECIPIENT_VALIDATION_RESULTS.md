# v3.2 Manager-Recipient Construction Validation

- Executed at: `2026-08-14T12:25:00Z`
- Branch: `cursor/v32-recipient-contract-17a0`
- Unit tests: 14 passed
- Mutation tests: 3/3 killed
- Mutation score: 100%
- Attempt-1 cases modified: no
- SUT executions: 0
- Formal scorer invocations: 0
- Runtime Skill changes: none

Validated construction behavior:

- a manager recipient requires `direct line manager`, `manager only`, empty additional recipients, and a `manager` role token without negation;
- reply-all and non-manager roles fail the gate;
- exactly one non-manager case is allowed and it must be the routing case;
- the routing case cannot be a question candidate;
- question candidates, Green controls, and the image-only case cannot be non-manager recipients;
- the frozen v3.2 attempt-1 envelope fails the gate and is not modified.

Killed mutants:

- `M1_ROUTING_MAY_BE_QUESTION_CANDIDATE`;
- `M2_NON_MANAGER_QUESTION_CANDIDATES_ALLOWED`;
- `M3_ROLE_WITHOUT_MANAGER_ALLOWED`.

An extra count-check mutant overlapping `validate_single_non_manager` was not counted; the envelope gate is that single check plus the routing/question-id rule.

v3.1 remains `SCORER_ERROR`. v3.2 attempt 1 remains `INVALID_COVERAGE`. Neither is rescored.
