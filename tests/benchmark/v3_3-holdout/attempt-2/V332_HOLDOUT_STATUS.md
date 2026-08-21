# V3.3 holdout attempt 2 — status

| Field | Value |
| --- | --- |
| `suite_id` | `v332-holdout-cloud-attempt2` |
| Skill runtime | T14.21 `357f99d7da77c49e67b56e9827ba5b932add4ee7` |
| Methodology | v3.3 |
| Frozen attempt 1 | do not rescore |
| Construction | `VALID`; copied with `git show` from `cursor/v332-attempt2-cases-w4q9-17a0` @ `6e66158` (not merged). Draft PR #80. |
| Gold | `VALID_COVERAGE`; frozen SHA-256 `3ce86d5351b79b39f22f2277a04e40f14507ad52027b8bfa3d5271044cc37f53` (roles `gold` + `ontology` + `scorer`). Gold JSON SHA-256 `9eed90da34b7b0be0e77c293f343a3983784406f1e818e85da0db18cd756b2d9`. Uncertain 0/24. |
| SUT | not started |
| Formal score | not started |

Designer (do not merge): `cursor/v332-attempt2-cases-w4q9-17a0` @ `6e66158`. Domain: Rowanleat Cork Works, Braydon Cut. Image-only question V332-009 `occluded_role: data_a`. Readable image V332-018. V332-017 is the only non-manager recipient.

Gold labelers (do not merge):

| N | family | model | branch | agent id |
| --- | --- | --- | --- | --- |
| 1 | grok | `cursor-grok-4.5-high` | `cursor/v332-gold-labeler-1-17a0` @ `e8f0e07` (draft PR #82) | `bc-e6edc3fa-6cec-5a65-abf1-e8a9e1122860` |
| 2 | gemini | `gemini-3.7-flash-high` | `cursor/v332-gold-labeler-2-17a0` @ `cb691c1` (draft PR #83) | `bc-3d5eb3fe-978b-550d-b8f9-aaa3a2e1ce46` |
| 3 | gpt | `gpt-5.6-sol-high` | `cursor/v332-gold-labeler-3-17a0` @ `8be7825` (draft PR #81) | `bc-6d2a6736-8125-520b-aa7a-9129b11232d6` |

Adjudicator (do not merge): `cursor/v332-gold-adjudicator-17a0` @ `ee136c5` (draft PR #84). Family claude. Copied with `git show`.
