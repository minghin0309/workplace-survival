# v3.3 Attempt-2 Gold Adjudication Brief

Fourth-family adjudication of three independent gold label sets.

- grok → `gold-labeler-1.json`
- gemini → `gold-labeler-2.json`
- gpt → `gold-labeler-3.json`

You are family `claude`. Do not relabel from scratch. Apply the v3.3 rating rules in `GOLD_LABELING_BRIEF.md` (established omission is Red; occluded Data B is Intake; `preserve-intended-recipient` is not required).

## Allowlist

Read only this brief, `GOLD_LABELING_BRIEF.md`, `tests/blind/GOLD_RUBRIC.md`, `tests/benchmark/SEMANTIC_ONTOLOGY.json`, `attempt-2/cloud-cases/cases.json`, case-referenced PNGs, and the three `gold-labeler-N.json` files.

Do not read `question-design.json`, oracle notes, Skill files, SPEC, scorers, attempt-1 `cloud-cases`, or any other PNG. Do not run the scorer.

## Outputs

On a dedicated branch, do not push `cursor/blind-v332-holdout-17a0`:

- `tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/gold-v332-raw.json`
- `tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/adjudication-v332-raw.json`
- `tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/adjudicator-v332-raw-attestation.json`

`gold_quality.labeler_model_families` = `["grok","gemini","gpt"]`; adjudicator family `claude`. Uncertainty ≤20% of 24 turns.

Open a draft PR with base `cursor/blind-v332-holdout-17a0`. Do not put cursor.com agent URLs in the PR body.
