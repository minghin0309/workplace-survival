# v3.2 Attempt-3 Semantic Matcher Brief

This file is operator documentation. The isolated matcher must not read it. The matcher prompt is the contract.

## Allowlist (exactly five files)

1. `tests/benchmark/v3_2-holdout/attempt-3/cloud-cases/extractions-manifest-v323.json` SHA-256 `7be3f8cc2c7a0c37b95e3b0f15343a8c591d007822847e2d1e567dc07868933d`
2. `tests/benchmark/v3_2-holdout/attempt-3/cloud-cases/evaluations-v323-canonical.json` SHA-256 `15b6c34992c7388f9db201b5f297ce9d27e4810d3a2589db74862df4000e2455`
3. `tests/benchmark/v3_2-holdout/attempt-3/cloud-cases/outputs-v323-raw.json` SHA-256 `609ca3b53d79fe3b743eac134d514bea3d8f33c66cd2734de268f5ed5f14ead5`
4. `tests/benchmark/v3_2-holdout/attempt-3/cloud-cases/gold-v323.json` SHA-256 `ed5bc77a5bb1839d45659d800aaaf3abc04212b044eedf08d6e6539c788d998f`
5. `tests/benchmark/SEMANTIC_ONTOLOGY.json` SHA-256 `3e2520b736c25b79baaddb49c9291fde48eb8b98ea7fa39be2ca09fc7496e926`

Do not read any other repository file. Do not glob or `ls` the holdout tree. Do not open images, oracle-notes, question-design, construction-mutations, scorer, methodology, plans, extractor-raw files, this brief, or runtime Skill files. Do not run the scorer. Do not modify gold, ontology, evaluations, or claims.

## Branch

Create `cursor/v323-matcher-claude-17a0` from the holdout tip that contains the extraction freeze. Do not push `cursor/blind-v323-holdout-17a0`.

## Outputs

- `tests/benchmark/v3_2-holdout/attempt-3/cloud-cases/matches-v323.json`
- `tests/benchmark/v3_2-holdout/attempt-3/cloud-cases/matcher-attestation-v323.json`

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
