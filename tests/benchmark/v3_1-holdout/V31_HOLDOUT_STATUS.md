# Fresh v3.1 Holdout Status

- Status: `VALID_COVERAGE_READY_FOR_SUT`
- Cases: 18
- Turns: 24
- Gold-uncertain turns: 1
- Gold uncertainty: 4.17%
- Required question concepts: 6
- Cases with required questions: 6
- Required revision concepts: 70
- Cases with required revisions: 18
- SUT execution authorized: yes
- SUT contexts executed: 0
- Formal scorer invocations: 0

Construction:

- attempt 1 was rejected for prior-domain reuse;
- attempt 2 uses a new bespoke millinery domain;
- six question candidates cover approval authority, deadline, recipient, source, measurement, and decision option;
- all 18 construction mutations passed;
- case content, gold, construction-only answers, and SUT-visible data remain separated.

Gold:

- three independent families: Grok, Kimi, GPT;
- fourth-family adjudicator: Claude;
- incomplete/contaminated labeler attempts were rejected;
- all votes and the one three-way turn remain preserved;
- v3 coverage gates passed before SUT execution.

Frozen evidence:

- canonical gold SHA-256: `bb8fbf70ac84e8718fef8abd0d2f7d53aee07213343b25f418db8329e1bedf2d`
- coverage report SHA-256: `576a3e116fe3119cbc55e4b75566b36975a72b074a690d43dccf59bf1ec067cd`
- gold manifest SHA-256: `2aea483242418bdf73a56b0fdb921a718d4ea54c66611a8eae8d7bf7cf8e0377`

No SUT output, extraction, match, or score artifact exists yet.
