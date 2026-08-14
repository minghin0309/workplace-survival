# v3.2 Gold Adjudication Brief

Fourth-family adjudication of three independent gold label sets. Family mapping is declared here:

- grok → `gold-labeler-1.json`
- gemini → `gold-labeler-2.json`
- gpt → `gold-labeler-3.json`

You are family `claude`. Do not relabel from scratch and discard votes. Preserve every family's route, ratings, and concept sets in `adjudication-v32-raw.json`.

## Allowlist

Read only these paths (no glob, no other holdout files):

- this brief;
- `tests/benchmark/v3_2-holdout/GOLD_LABELING_BRIEF.md`;
- `tests/blind/GOLD_RUBRIC.md`;
- `tests/benchmark/SEMANTIC_ONTOLOGY.json`;
- `tests/benchmark/v3_2-holdout/cloud-cases/cases.json`;
- `tests/benchmark/v3_2-holdout/cloud-cases/images/v32-008-t1-stores-chit.png`;
- `tests/benchmark/v3_2-holdout/cloud-cases/images/v32-018-t1-loft-thread.png`;
- `tests/benchmark/v3_2-holdout/cloud-cases/gold-labeler-1.json`;
- `tests/benchmark/v3_2-holdout/cloud-cases/gold-labeler-2.json`;
- `tests/benchmark/v3_2-holdout/cloud-cases/gold-labeler-3.json`.

Do not read `question-design.json`, `oracle-notes.json`, Skill files, SPEC, scorers, methodology, freeze scripts, or any other PNG. Do not run the scorer. Do not guess the occluded V32-008 token.

## Tiers

- `tier_1_unanimous`: all three families agree on route and all three ratings.
- `tier_2_majority`: 2-1 on at least one rating; you agree with the majority.
- `tier_3_adjudicated`: 2-1 resolved against the majority on the merits, or concept sets adjudicated beyond token majority. Still gold.
- `tier_4_uncertain`: three-way categorical disagreement or otherwise unresolved. Set `gold_uncertain: true`.

Human review is unavailable. Uncertainty must stay ≤20% of 24 turns. Do not manufacture unanimity to hit the gate.

## Canonical gold fields

`gold-v32-raw.json` must be consumable by `finalize_gold.py`:

- top-level `gold_quality.labeler_model_families` = `["grok","gemini","gpt"]`;
- top-level `gold_quality.adjudicator_model_family` = `"claude"`;
- top-level `definitions.question` and `definitions.revision` maps (ontology IDs plus any local IDs you keep);
- every turn has `turn_index`, `route`, `responsibility`, `tone`, `overall`, `required_question_concepts`, `allowed_question_concepts`, `required_revision_concepts`, `allowed_revision_concepts`, `critical_invariants`, `rationale`, `gold_uncertain`;
- every required concept is also in the matching allowed list;
- overall matches `Red > Gray > Yellow > Green`;
- Intake/Scope/template routes use `null` ratings.

Cover all 18 cases / 24 turns. Multi-turn cases: V32-014, V32-015, V32-016.

## Outputs

On a dedicated branch, do not push `cursor/blind-v32-holdout-17a0`:

- `tests/benchmark/v3_2-holdout/cloud-cases/gold-v32-raw.json`
- `tests/benchmark/v3_2-holdout/cloud-cases/adjudication-v32-raw.json`
- `tests/benchmark/v3_2-holdout/cloud-cases/adjudicator-v32-raw-attestation.json`

Attestation records files actually read with SHA-256, branch, commits, `question_design_accessed: false`, `skill_files_accessed: false`, `scorer_run: false`.

Commit gold-v32-raw first, then adjudication, then attestation. Push only the dedicated branch.
