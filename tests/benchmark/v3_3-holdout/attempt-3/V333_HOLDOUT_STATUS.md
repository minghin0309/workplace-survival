# V3.3 holdout attempt 3 — status

| Field | Value |
| --- | --- |
| `suite_id` | `v333-holdout-cloud-attempt3` |
| Skill runtime | T14.24 `9c79eb87b624f75d1c0d9fe26ddba56994bffbd9` |
| Methodology | v3.3 |
| Frozen attempt 1 | do not rescore |
| Frozen attempt 2 | do not rescore |
| Construction | `VALID`; copied with `git show` from `cursor/v333-attempt3-cases-k7m2-17a0` @ `446a20b` (artifacts `2738181`, not merged). Designer `bc-891cc11a-21f6-5e13-abc4-ca17369cbf10`. |
| Gold | `VALID_COVERAGE`; frozen SHA-256 `669d089a602cac71889e85aea84bc84eeafc0df77a38c4c2c17e6870d29e923e` (roles `gold` + `ontology` + `scorer`). Gold JSON SHA-256 `f47bd218c185a076444d12eb270f41cb2658c2312d5086ac9a4e0d07556fbc08`. Uncertain 0/24. Copied from `cursor/v333-gold-adjudicator-17a0` @ `6eece7a` (not merged). |
| SUT | wave 1 copied (001–003). Wave 2 (004–006) launched. |
| Extraction | not started |
| Matching | not started |
| Formal score | not started; one-shot after freezes |

Designer (do not merge): `cursor/v333-attempt3-cases-k7m2-17a0` @ `446a20b`. Domain: Selkith Aneroid Works, Cinderholt Pressing Rooms. Image-only question V333-009 `occluded_role: data_a`. Readable image V333-018. V333-017 is the only non-manager recipient. Isolation: five allowlisted files only.

Gold labelers (do not merge):

| N | family | model | branch | agent id |
| --- | --- | --- | --- | --- |
| 1 | grok | `cursor-grok-4.5-high` | `cursor/v333-gold-labeler-1-17a0` @ `1c5c39e` | `bc-8953d067-d02d-5202-b8b5-7b48dbecf052` |
| 2 | gemini | `gemini-3.7-flash-high` | `cursor/v333-gold-labeler-2-17a0` @ `dee1d04` | `bc-50b62d40-cc75-580b-ad43-4baa4434022e` |
| 3 | gpt | `gpt-5.6-sol-high` | `cursor/v333-gold-labeler-3-17a0` @ `b804783` | `bc-b7c43f0e-59ed-5a25-91a8-092070816448` |

Adjudicator (do not merge): `cursor/v333-gold-adjudicator-17a0` @ `6eece7a`. Family claude. Copied with `git show`. Isolation: question-design and Skill not read. Uncertain 0/24. Draft PR #114.

SUT wave 1 (do not merge):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V333-001 | `cursor/v333-001-sut-17a0` @ `00b2204` | `bc-6b4f2c89-585a-5227-b608-e807123328e8` | #115 |
| V333-002 | `cursor/v333-002-sut-17a0` @ `42ac275` | `bc-8bd0aa6d-b7f7-5985-b054-2b6a77bc37b1` | #117 |
| V333-003 | `cursor/v333-003-sut-17a0` @ `c6c55c2` | `bc-efbfd8e8-bc83-539c-8857-2107d35b8bf8` | #116 |

SUT wave 2 (do not merge):

| case | agent id |
| --- | --- |
| V333-004 | `bc-afef334f-f227-5002-830a-51cb5b6515b9` |
| V333-005 | `bc-fa8301cd-23c8-5b2b-bc2d-056244b3afb0` |
| V333-006 | `bc-200b68ff-b0e7-5bd4-a695-93ddd2183a76` |
