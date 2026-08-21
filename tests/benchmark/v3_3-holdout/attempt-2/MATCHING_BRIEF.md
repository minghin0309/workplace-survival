# v3.3 Attempt-2 Semantic Matcher Brief

This file is operator documentation. The isolated matcher must not read it. The matcher prompt is the contract.

## Allowlist (exactly five files)

1. `tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/extractions-manifest-v332.json` SHA-256 `e61eb61d3861cab60036dd693d57cba3b56b740d615e49abd302532c7e489866`
2. `tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/evaluations-v332-canonical.json` SHA-256 `ecd6fd806c1743c1f57bf2dc9cbe03822ea2d48310dad9c4f432e37fb7a2b5a2`
3. `tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/outputs-v332-raw.json` SHA-256 `d61dde993d3c3a74b16a317b43b5656d3b3e76542fd15b1dc99e341a9ab251cb`
4. `tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/gold-v332.json` SHA-256 `9eed90da34b7b0be0e77c293f343a3983784406f1e818e85da0db18cd756b2d9`
5. `tests/benchmark/SEMANTIC_ONTOLOGY.json` SHA-256 `3e2520b736c25b79baaddb49c9291fde48eb8b98ea7fa39be2ca09fc7496e926`

Do not read any other repository file. Do not glob or `ls` the holdout tree. Do not open images, oracle-notes, question-design, construction-mutations, scorer, methodology, plans, extractor-raw files, this brief, or runtime Skill files. Do not run the scorer. Do not modify gold, ontology, evaluations, or claims.

## Branch

Create `cursor/v332-matcher-claude-17a0` from the holdout tip that contains the extraction freeze. Do not push `cursor/blind-v332-holdout-17a0`.

## Outputs

- `tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/matches-v332.json`
- `tests/benchmark/v3_3-holdout/attempt-2/cloud-cases/matcher-attestation-v332.json`

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
