# Fresh Benchmark v3.2 Holdout Results

- Status: `INVALID_COVERAGE`
- Attempt: `v32-holdout-cloud-attempt1`
- Cases: 18
- Turns: 24
- Images: 2
- Required question concepts: 1
- Cases with required question concepts: 1
- Required revision concepts: 6
- Cases with required revision concepts: 3
- Accepted turns: 23
- Gold-uncertain turns: 1 (`V32-008-T1`, 4.17%)
- SUT execution authorized: no
- SUT contexts executed: 0
- Formal scorer invocations: 0

Coverage failure:

- v3.2 requires at least 3 required question concepts across at least 3 cases;
- adjudicated gold contains a required question only for `V32-014-T1`;
- `required_question_concepts` and `required_question_cases` therefore fail.

Cause:

- the six question-candidate cases (`V32-004`–`V32-009`) set `recipient_context` to a colleague, supplier, librarian, or client, not a manager;
- independent grok/gpt gold, and Claude adjudication, routed those turns `Scope` with null ratings and no required questions;
- that follows `GOLD_RUBRIC.md` (`recipient is explicitly not a manager and no manager is included`);
- mechanical construction validation passed mutations/denylist but did not require a manager recipient except on the routing case;
- gold was not rewritten to fit the gate.

Isolation and provenance:

- designer: `cursor/isolated-v32-case-design-975e` @ `466fd70`, copied with `git show`, not merged;
- gold: grok / gemini / gpt on dedicated branches, copied with `git show`, not merged;
- adjudicator: `cursor/v32-gold-adjudicator-claude-17a0-9afb` @ `0858de4`, copied with `git show`, not merged;
- all accepted gold contexts: `question_design_accessed=false`, `skill_files_accessed=false`;
- adjudicator `ls` of `cloud-cases/` file names is a recorded procedural deviation.

Classification:

- Skill defect: none; the Skill was never executed;
- gold defect: none confirmed; Scope on non-manager recipients matches the rubric; votes preserved;
- benchmark design/coverage defect: confirmed — question candidates were not manager-message reviews;
- scorer defect: none exercised; v3.2 scorer was not invoked;
- harness defect: construction validator missed the manager-recipient invariant.

Frozen gold SHA-256: see `gold-v32.json` after this freeze commit. Ontology and the v3.2 scorer are recorded in the invalid-coverage manifest and were not used to emit metrics.

A later holdout must require `relationship_to_user` = direct line manager on every case except the single recipient-routing case, and must not reuse this harpworks domain or attempt-1 entities. This attempt is immutable.
