# v3.2 Attempt-2 Semantic Matcher Brief

This file is operator documentation. The isolated matcher must not read it. The matcher prompt is the contract.

## Allowlist (exactly five files)

1. `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractions-manifest-v322.json` SHA-256 `e9945ace2da96d5d35bc4a98ffb901e0e553332a929d900ba672034387815ab1`
2. `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/evaluations-v322-canonical.json` SHA-256 `1a01b246c422bae55e3bf85f14fdc1f9ff4600f5d8636cec56d55f698d9170e8`
3. `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/outputs-v322-raw.json` SHA-256 `8e7aa031ebc6f919cf9bb401b8c70634d4a19f2bb6bc5b2ec4b742b8dd82db1f`
4. `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/gold-v322.json` SHA-256 `beda11643abeba9c578351ee8be9ec7713cfd5025fa304d3ca29c00c32b76a75`
5. `tests/benchmark/SEMANTIC_ONTOLOGY.json` SHA-256 `3e2520b736c25b79baaddb49c9291fde48eb8b98ea7fa39be2ca09fc7496e926`

Do not read any other repository file. Do not glob or `ls` the holdout tree. Do not open images, oracle-notes, question-design, construction-mutations, scorer, methodology, plans, extractor-raw files, this brief, or runtime Skill files. Do not run the scorer. Do not modify gold, ontology, evaluations, or claims.

## Branch

Create `cursor/v322-matcher-claude-17a0` from the holdout tip that contains the extraction freeze. Do not push `cursor/blind-v322-holdout-17a0`.

## Outputs

- `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/matches-v322.json`
- `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/matcher-attestation-v322.json`

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
