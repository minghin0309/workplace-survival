# Benchmark v2 Gold Freeze Results

- Status: `INVALID_PROTOCOL`
- Frozen at: `2026-08-13T07:48:28.422888Z`
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Cases: 18
- Turns: 24
- Gold-uncertain turns: 2 (8.33%)
- Frozen artifacts: 18
- Manifest: `tests/benchmark/v2-holdout/cloud-cases/gold-manifest.json`
- Manifest SHA-256: `c2c1b742e51993f501582f4c74538f86d07cf9d0f8132c03780376331c237882`

Validation:

- This freeze passed the mechanical validator but was invalidated after transcript audit showed that gold labeler 2 read prohibited benchmark plan, methodology, scorer, and test files while its attestation claimed otherwise.
- It must not be used as the parent of SUT output or evaluation manifests.
- 17 methodology unit and negative tests passed.
- Canonical normalization was idempotent.
- Route, rating, question, revision, and invariant decisions were unchanged.
- The exact case and oracle-note envelope bytes used during cloud gold construction were restored and hash-verified.
- All labeler, adjudicator, designer, image, ontology, scorer, validator, and runtime-manifest artifacts passed the v2 validator.
- The manifest's non-overwrite gate rejected a second freeze attempt.
- Runtime Skill files were not modified.
