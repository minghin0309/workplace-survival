# v3.3 Attempt-1 Gold Labeling Brief

Label the frozen v3.3 attempt-1 holdout without seeing Skill output, question-design answers, oracle notes, scorers, or prior holdouts.

You may read only:

- this brief;
- `tests/blind/GOLD_RUBRIC.md`;
- `tests/benchmark/SEMANTIC_ONTOLOGY.json`;
- `tests/benchmark/v3_3-holdout/cloud-cases/cases.json`;
- image paths referenced by those cases (only those PNGs).

Do not glob. Do not read `question-design.json`, `oracle-notes.json`, `construction-mutations.json`, `designer-attestation.json`, Skill files, SPEC, tests, methodology, freeze scripts, or any other PNG. Do not run the scorer.

## v3.3 rating rules (override Gray-vs-omission habits)

- If Data A makes a named execution step depend on token X, and the identifiable Data B body omits X, responsibility is **Red** (omission defeats purpose). Do not use Gray merely because the writer still holds X off-record.
- Gray remains correct when Data B contains an unconfirmed token that Data A locates off-record and does not quote, or when governing requirements conflict.
- If a material token in **Data B** is not reliably legible, route is **Intake** and ratings are null. Do not guess the token.
- If only a Data A / background token is unreadable and the sendable draft is identifiable, stay in Normal mode, Gray the affected dimension, and ask.
- Do **not** put `preserve-intended-recipient` in `required_revision_concepts`. It may appear in `allowed_revision_concepts`.
- Green/Green reviews use `required_revision_concepts: ["no-revision"]` and no rewrite.

## Job

Label every case `V33-001`–`V33-018` and every turn (24 turns). Multi-turn cases are `V33-014`, `V33-015`, `V33-016` (three turns each).

## Output

Write exactly two files on a dedicated branch. Do not push `cursor/blind-v33-holdout-17a0`.

- `tests/benchmark/v3_3-holdout/cloud-cases/gold-labeler-N.json`
- `tests/benchmark/v3_3-holdout/cloud-cases/gold-labeler-N-attestation.json`

`N` is `1` (grok), `2` (gemini), or `3` (gpt) as assigned.

Envelope: `envelope_version` `v3.3`, `suite_id` `v33-holdout-cloud-attempt1`. Field names are `*_concepts`. Every required concept must also appear in the matching allowed list.

Route, overall derivation (`Red > Gray > Yellow > Green`), question/revision rules, and invariant tokens follow `GOLD_RUBRIC.md` except the v3.3 rating rules above.

Attestation records files actually read with SHA-256, branch, commit, `question_design_accessed: false`, `skill_files_accessed: false`.

Commit labels first, then attestation, on the dedicated branch only. Push that branch. Open a draft PR with base `cursor/blind-v33-holdout-17a0`. Do not put cursor.com agent URLs in the PR body.
