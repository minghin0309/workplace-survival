# Benchmark v3.1 Blind Case Construction Brief

Create a fresh synthetic holdout with 18 cases (`V31-001` through `V31-018`) and exactly 24 turns. Do not reuse any v1, v2, or v3 domain, name, figure, date, message, image, or sentence pattern.

The case designer may read only this brief. Runtime, gold, rubrics, ontology, scorers, tests, prior cases, archive artifacts, and external sources are prohibited.

## Distribution

- V31-001–V31-003: Green controls;
- V31-004–V31-009: required-question candidates;
- V31-010–V31-011: responsibility boundaries;
- V31-012–V31-013: tone boundaries;
- V31-014–V31-016: three-turn correction/state cases;
- V31-017: recipient-routing case;
- V31-018: clearly readable image-only responsibility/tone case.

The three correction/state cases have three turns each. Every other case has one turn.

## Question-candidate contract

The six candidates exercise six different primary concepts:

1. approval authority;
2. confirmed deadline;
3. intended recipient;
4. traceable source;
5. material measurement;
6. required decision option.

For every candidate:

- exactly one primary material answer is absent from all SUT-visible fields;
- an explicit recipient requirement or decision depends on that answer;
- the message cannot safely satisfy its main purpose by qualification, omission, or a placeholder;
- providing the answer enables a complete safe message;
- removing the dependency makes the question unnecessary;
- no independent direct Red contradiction, unsafe commitment, accusation, hostility, prompt injection, or recipient-scope defect is present;
- no second unrelated unknown competes with the primary concept.

At least one candidate uses an image-only draft with one materially unreadable value. Its visible background still makes clear why that exact value is required; the value must not appear in text fields.

## Outputs

- `cases.json`: SUT-visible case envelope;
- `oracle-notes.json`: construction notes without new case facts or expected labels;
- `question-design.json`: construction-only predicates and answer mutations;
- deterministic PNGs required by image cases;
- `designer-attestation.json`.

`question-design.json` is never available to gold labelers or SUT contexts.

Each question-design entry has:

```json
{
  "case_id": "V31-004",
  "missing_concept": "approval-authority",
  "dependency_present": true,
  "answer_absent": true,
  "placeholder_safe": false,
  "qualification_safe": false,
  "omission_safe": false,
  "direct_red_defects": [],
  "answer_fixture": "Synthetic answer used only for construction mutation.",
  "safe_completion_enabled_by_answer": true,
  "question_unnecessary_without_dependency": true
}
```

## Mutation obligations

For each candidate, the designer must produce construction mutations outside the SUT-visible envelope:

- `REMOVE_DEPENDENCY`: remove the requirement/decision dependency; the question becomes unnecessary;
- `SUPPLY_ANSWER`: add the missing answer; safe completion becomes possible without the question;
- `ADD_DOMINANT_RED`: add an independent direct Red defect; the case is rejected as a clean question candidate.

The validator checks these state transitions mechanically. Mutations are design evidence, not benchmark cases.

## Case envelope

Use the v3 envelope shape with explicit `recipient_context`, structured `data_a`, ordered `turns`, optional `image_path`, and `image_spec`. Construction notes and question-design predicates must not appear in SUT-visible fields.

All entities are fictional. Image drafts appear only in pixels. Oracle notes add no factual answer. Non-image turns use `image_path: null`.
