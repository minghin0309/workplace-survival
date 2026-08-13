# Benchmark v2 Replacement Gold Freeze Results

- Status: `VALID`
- Frozen at: `2026-08-13T08:34:20.947011Z`
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Cases: 18
- Turns: 24
- Gold-uncertain turns: 1 (4.17%)
- Frozen artifacts: 23
- Manifest: `tests/benchmark/v2-holdout/cloud-cases/gold-manifest-v2.json`
- Manifest SHA-256: `0806da52e7414c1f30cb83fba3b257e630079102c9c50813ccf3dcad21796084`

Validation:

- The invalidated first manifest remains preserved and is rejected by content hash.
- Replacement Grok labeler transcript isolation audit passed.
- Replacement GPT adjudicator transcript isolation audit passed.
- Machine model IDs unavailable from cloud run metadata are recorded as `unverified`; no model ID was guessed.
- Canonical normalization was idempotent and changed no adjudicated turn decision.
- All 18 cases and 24 turns passed schema and coverage validation.
- Every categorical vote distribution totals three.
- Gold and adjudication final-turn parity mismatches: zero.
- Required question and revision concepts are subsets of their allowed sets.
- Flat ratings and overall derivation are scorer-compatible.
- Gold uncertainty is below the 20% validity threshold.
- The manifest includes raw and canonical gold, adjudication, audit, invalidation, image, ontology, scorer, validator, runtime, labeler, and attestation evidence.
- Runtime Skill files were not modified.
