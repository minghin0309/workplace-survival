# v3.2 Attempt-1 Coverage Triage

The first v3.2 holdout failed only the preregistered question-coverage gates:

- required question concepts: 1, minimum 3;
- cases with required questions: 1, minimum 3.

Revision coverage (6 concepts / 3 cases), accepted-turn coverage, and uncertainty coverage (4.17%) passed. The Skill was never executed. Gold was not rewritten.

## Why the six question candidates did not yield required questions

`V32-004`–`V32-009` set `recipient_context` to a colleague, supplier, librarian, or client. Independent grok/gpt gold, and Claude adjudication, routed those turns `Scope` with null ratings.

`GOLD_RUBRIC.md` defines Scope as: recipient is explicitly not a manager and no manager is included.

A Scope decline is not a manager-message review. Required-question gold on those turns would penalize a correct Scope response.

`V32-017` was the designated routing case. Attempt 1 used non-manager recipients on 16 of 18 cases, including every question candidate and the image-only responsibility/tone case.

Mechanical construction validation checked mutations, denylist, and PNG headers. It did not require a manager recipient except by an envelope example the designer was free to vary.

## Remediation

v3.2 attempt 1 remains immutable. A later holdout must enforce:

1. exactly one non-manager recipient, and it is the routing case;
2. every question candidate is a manager-message review (`relationship_to_user` = `direct line manager`, `audience_scope` = `manager only`, `recipient_role` contains `manager` without negation, no additional recipients);
3. the routing case is not a question candidate.

The executable contract is `tests/benchmark/v3_2/recipient_manager_contract.py`. It rejects the frozen attempt-1 envelope as a negative fixture and does not modify those files.
