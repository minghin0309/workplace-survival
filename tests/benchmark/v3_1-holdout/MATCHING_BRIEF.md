# v3.1 Semantic Matcher Brief

This file is operator documentation. The isolated matcher must not read it. The matcher prompt is the contract.

## Allowlist (exactly five files)

1. `tests/benchmark/v3_1-holdout/cloud-cases/extractions-manifest-v31.json` SHA-256 `a406161c1fac10f9c8b1f86c402891ac7dc81ac616abc8df0ebf9eb545c8b46e`
2. `tests/benchmark/v3_1-holdout/cloud-cases/evaluations-v31-canonical.json` SHA-256 `63cc05f43da57a426bb252dc50b137f63e7f531697848d2ae5e367fc14841aa2`
3. `tests/benchmark/v3_1-holdout/cloud-cases/outputs-v31-raw.json` SHA-256 `cf5ef7e28ca5bacd6e4e28e6bd2d92dfb5be61b34f51ce67bb4b40a7071be7b8`
4. `tests/benchmark/v3_1-holdout/cloud-cases/gold-v31.json` SHA-256 `bb8fbf70ac84e8718fef8abd0d2f7d53aee07213343b25f418db8329e1bedf2d`
5. `tests/benchmark/SEMANTIC_ONTOLOGY.json` SHA-256 `3e2520b736c25b79baaddb49c9291fde48eb8b98ea7fa39be2ca09fc7496e926`

Do not read any other repository file. Do not glob or `ls` the holdout tree. Do not open images, oracle-notes, question-design, construction-mutations, scorer, methodology, plans, extractor-raw files, this brief, or runtime Skill files. Do not run the scorer. Do not modify gold, ontology, evaluations, or claims.

## Branch

Create `cursor/v31-matcher-claude-17a0` from holdout tip `5c5e236`. Do not push `cursor/blind-v31-holdout-17a0`.

## Outputs

- `tests/benchmark/v3_1-holdout/cloud-cases/matches-v31.json`
- `tests/benchmark/v3_1-holdout/cloud-cases/matcher-attestation-v31.json`

Commit matches first, then attestation. Push only the dedicated branch.

## Decision rules

- Every extracted claim gets exactly one match decision.
- `concept_id` must be in that turn's `allowed_question_concepts` / `allowed_revision_concepts`, or `null` if unsupported.
- Local gold `concept_definitions` IDs are valid semantic targets when present in the allowed list. They are not ontology exact/alias matches.
- `match_type`: `exact` | `alias` | `semantic` | `unsupported`.
- `exact`/`alias` require claim `text == evidence_span` and an ontology alias hit. Confidence for `semantic` must be ≥ 0.8. Unsupported keeps `concept_id: null`.
- One claim maps to at most one concept. Do not invent concepts. Do not drop claims.
- Gold access is required and must be attested `gold_access: true`.

Matcher family must not be a gold labeler family (`grok`, `kimi`, `gpt`). Assigned family: `claude`.
