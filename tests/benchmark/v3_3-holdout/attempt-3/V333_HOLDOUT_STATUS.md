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
| SUT | wave 1–3 copied (001–009). Wave 4: 011–012 copied, 010 running. Wave 5: 013–014 launched; 015 queued on VM slot. |
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

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V333-004 | `cursor/v333-004-sut-17a0` @ `e52453a` | `bc-afef334f-f227-5002-830a-51cb5b6515b9` | #118 |
| V333-005 | `cursor/v333-005-sut-17a0` @ `ae3a01b` | `bc-fa8301cd-23c8-5b2b-bc2d-056244b3afb0` | #120 |
| V333-006 | `cursor/v333-006-sut-17a0` @ `20c8414` | `bc-200b68ff-b0e7-5bd4-a695-93ddd2183a76` | #119 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true on 001–009. V333-009 attested PNG read. Skill SHA-256 matches T14.24.

SUT wave 3 (do not merge):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V333-007 | `cursor/v333-007-sut-17a0` @ `429d76a` | `bc-d204ab5d-e17c-51d5-95da-bfef6acd5864` | #121 |
| V333-008 | `cursor/v333-008-sut-17a0` @ `b274bb2` | `bc-fb41388e-3e33-5efe-ad33-76d882448450` | #122 |
| V333-009 | `cursor/v333-009-sut-17a0` @ `d9b37ea` | `bc-bed461eb-f327-55b4-b48b-a7afdba50730` | #123 |

SUT wave 4 (do not merge):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V333-010 | pending | `bc-47e162df-7f2a-5aea-b4c9-7259ca57360f` | |
| V333-011 | `cursor/v333-011-sut-17a0` @ `d4ebab1` | `bc-2355f2bc-7bec-5404-b8ca-eb25797fa41c` | #124 |
| V333-012 | `cursor/v333-012-sut-17a0` @ `e88fe55` | `bc-0d8ecd6f-0a17-54bb-b4b1-cf4660420452` | #125 |

SUT wave 5 (do not merge):

| case | agent id |
| --- | --- |
| V333-013 | `bc-c0449c62-1ad4-5a4f-8779-1c9fcdca1ac4` |
| V333-014 | `bc-e5040126-4690-52ad-a26b-253dc5b92984` |
| V333-015 | queued (VM slot) |
