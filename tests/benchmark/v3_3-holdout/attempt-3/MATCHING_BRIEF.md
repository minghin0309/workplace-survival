# v3.3 Attempt-3 Semantic Matcher Brief

This file is operator documentation. The isolated matcher must not read it. The matcher prompt is the contract.

Fill SHA-256 values after the extraction freeze. Do not launch the matcher before that freeze exists.

## Allowlist (exactly five files)

1. `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/extractions-manifest-v333.json` SHA-256 `FILL_AFTER_EXTRACTION_FREEZE`
2. `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/evaluations-v333-canonical.json` SHA-256 `FILL_AFTER_EXTRACTION_FREEZE`
3. `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/outputs-v333-raw.json` SHA-256 `FILL_AFTER_SUT_FREEZE`
4. `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/gold-v333.json` SHA-256 `FILL_AFTER_GOLD_FREEZE`
5. `tests/benchmark/SEMANTIC_ONTOLOGY.json` SHA-256 `3e2520b736c25b79baaddb49c9291fde48eb8b98ea7fa39be2ca09fc7496e926`

Do not read any other repository file. Do not glob or `ls` the holdout tree. Do not open images, oracle-notes, question-design, construction-mutations, scorer, methodology, plans, extractor-raw files, this brief, or runtime Skill files. Do not run the scorer. Do not modify gold, ontology, evaluations, or claims.

## Branch

Create `cursor/v333-matcher-claude-17a0` from the holdout tip that contains the extraction freeze. Do not push `cursor/blind-v333-holdout-17a0`.

## Outputs

- `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/matches-v333.json`
- `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/matcher-attestation-v333.json`

Commit matches first, then attestation. Push only the dedicated branch.

## Decision rules

- Every extracted claim gets exactly one match decision.
- `concept_id` must be in that turn's `allowed_question_concepts` / `allowed_revision_concepts`, or `null` if unsupported.
- Local gold `concept_definitions` IDs are valid semantic targets when present in the allowed list. They are not ontology exact/alias matches.
- `match_type`: `exact` | `alias` | `semantic` | `unsupported`.
- `exact`/`alias` require claim `text == evidence_span` and an ontology alias hit. Confidence for `semantic` must be ≥ 0.8. Unsupported keeps `concept_id: null`.
- One claim maps to at most one concept. Do not invent concepts. Do not drop claims.
- Gold access is required and must be attested `gold_access: true`.

Matcher family must not be a gold labeler family (`grok`, `gemini`, `gpt`). Assigned family: `claude`.
