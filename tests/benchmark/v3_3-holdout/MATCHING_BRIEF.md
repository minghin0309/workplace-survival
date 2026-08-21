# v3.3 Attempt-1 Semantic Matcher Brief

This file is operator documentation. The isolated matcher must not read it. The matcher prompt is the contract.

## Allowlist (exactly five files)

1. `tests/benchmark/v3_3-holdout/cloud-cases/extractions-manifest-v33.json` SHA-256 `cbf785a36aec53dc0e2a34ca7e1ca6a270345091c110c099e75bf6f7dfb4ed12`
2. `tests/benchmark/v3_3-holdout/cloud-cases/evaluations-v33-canonical.json` SHA-256 `76f55a591bae0ee750c03fc5f8ad2667c80b9cc1b4309d9534548a62d0bcdfe2`
3. `tests/benchmark/v3_3-holdout/cloud-cases/outputs-v33-raw.json` SHA-256 `cd9713d1bcd91d896b11f8df814b1efcb6e9f3be977a8ad9b46df89384e6ef57`
4. `tests/benchmark/v3_3-holdout/cloud-cases/gold-v33.json` SHA-256 `aeb9f00a78d08cac58ad058dd77db51d8d40c01418762a36f611a86608ad0704`
5. `tests/benchmark/SEMANTIC_ONTOLOGY.json` SHA-256 `3e2520b736c25b79baaddb49c9291fde48eb8b98ea7fa39be2ca09fc7496e926`

Do not read any other repository file. Do not glob or `ls` the holdout tree. Do not open images, oracle-notes, question-design, construction-mutations, scorer, methodology, plans, extractor-raw files, this brief, or runtime Skill files. Do not run the scorer. Do not modify gold, ontology, evaluations, or claims.

## Branch

Create `cursor/v33-matcher-claude-17a0` from the holdout tip that contains the extraction freeze. Do not push `cursor/blind-v33-holdout-17a0`.

## Outputs

- `tests/benchmark/v3_3-holdout/cloud-cases/matches-v33.json`
- `tests/benchmark/v3_3-holdout/cloud-cases/matcher-attestation-v33.json`

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
