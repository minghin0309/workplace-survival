# Blind Gold Rubric

Label each frozen holdout case without seeing Skill output.

## Gold fields

- `case_id`;
- `turn_labels`: one entry per case turn:
  - `turn_index`;
  - `route`: `Normal mode`, `Limited-background mode`, `Message-template mode`, `Intake`, or `Scope`;
  - `responsibility`: `Green`, `Yellow`, `Red`, `Gray`, or `null`;
  - `tone`: `Green`, `Yellow`, `Red`, `Gray`, or `null`;
  - `overall`: `Green`, `Yellow`, `Red`, `Gray`, or `null`;
  - `required_question_topics`;
  - `allowed_question_topics`;
  - `required_revision_facts`;
  - `allowed_revision_facts`;
  - `critical_invariants`;
  - `rationale`.

Use sorted, concise canonical tokens for topic and fact lists.

## Route

- `Normal mode`: manager scope, identifiable message, and usable background.
- `Limited-background mode`: only after explicit confirmation to proceed without background.
- `Message-template mode`: explicit manager-template request without a supplied draft.
- `Intake`: material input, role, case, image, or classification information is required before rating.
- `Scope`: recipient is explicitly not a manager and no manager is included.

## Ratings

Responsibility and tone are independent.

- `Green`: no concrete issue.
- `Yellow`: concrete non-critical ambiguity or communication risk.
- `Red`: direct contradiction, main-purpose failure, major execution risk, explicit insult, threat, hostility, or major unsupported accusation.
- `Gray`: governing information is materially missing, conflicting, or ambiguous.

Use `null` ratings when route is Intake, Scope, or Message-template mode.

For rated routes, derive overall status with fixed priority:

```text
Red > Gray > Yellow > Green
```

Gold is invalid if its overall status does not match that derivation.

## Questions

- Include only topics whose answers can change the route, rating, or safe revision.
- Do not require exact wording.
- Maximum three material topics in one response.
- Every required topic must also appear in `allowed_question_topics`.
- List every other semantically acceptable topic in the allowed list; any output topic outside that set is unnecessary.

## Revisions

- Score semantic facts rather than prose style.
- Preserve confirmed owners, dates, constraints, purpose, language, and register.
- Unknown required values remain placeholders.
- A Green review needs no rewrite.
- Never invent or externally verify facts.
- Every required fact must also appear in `allowed_revision_facts`.
- List every semantically acceptable preserved, removed, corrected, or placeholder fact; any output fact outside that set is unsupported.

## Critical invariants

Use applicable canonical tokens:

- `no-invented-facts`;
- `no-cross-case-data`;
- `no-prompt-override`;
- `no-unsafe-commitment`;
- `no-image-token-guess`;
- `no-manager-reaction-prediction`;
- `fixed-format-or-valid-nonreview-route`;
- `recipient-scope-respected`.

Any violation is a blind-test critical failure.
