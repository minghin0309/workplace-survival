# V3.3 holdout attempt 2 — status

| Field | Value |
| --- | --- |
| `suite_id` | `v332-holdout-cloud-attempt2` |
| Skill runtime | T14.21 `357f99d7da77c49e67b56e9827ba5b932add4ee7` |
| Methodology | v3.3 |
| Frozen attempt 1 | do not rescore |
| Construction | `VALID`; copied with `git show` from `cursor/v332-attempt2-cases-w4q9-17a0` @ `6e66158` (not merged). Draft PR #80. |
| Gold | `VALID_COVERAGE`; frozen SHA-256 `3ce86d5351b79b39f22f2277a04e40f14507ad52027b8bfa3d5271044cc37f53` (roles `gold` + `ontology` + `scorer`). Gold JSON SHA-256 `9eed90da34b7b0be0e77c293f343a3983784406f1e818e85da0db18cd756b2d9`. Uncertain 0/24. |
| SUT | frozen SHA-256 `7bf0eb2fc752620295da37f335eaaf5020549878b1bdfd8e7f363e077f9deeec`. 18 cases / 24 turns. Dedicated branches not merged. Extractors launching. |
| Formal score | not started |

Designer (do not merge): `cursor/v332-attempt2-cases-w4q9-17a0` @ `6e66158`. Domain: Rowanleat Cork Works, Braydon Cut. Image-only question V332-009 `occluded_role: data_a`. Readable image V332-018. V332-017 is the only non-manager recipient.

Gold labelers (do not merge):

| N | family | model | branch | agent id |
| --- | --- | --- | --- | --- |
| 1 | grok | `cursor-grok-4.5-high` | `cursor/v332-gold-labeler-1-17a0` @ `e8f0e07` (draft PR #82) | `bc-e6edc3fa-6cec-5a65-abf1-e8a9e1122860` |
| 2 | gemini | `gemini-3.7-flash-high` | `cursor/v332-gold-labeler-2-17a0` @ `cb691c1` (draft PR #83) | `bc-3d5eb3fe-978b-550d-b8f9-aaa3a2e1ce46` |
| 3 | gpt | `gpt-5.6-sol-high` | `cursor/v332-gold-labeler-3-17a0` @ `8be7825` (draft PR #81) | `bc-6d2a6736-8125-520b-aa7a-9129b11232d6` |

Adjudicator (do not merge): `cursor/v332-gold-adjudicator-17a0` @ `ee136c5` (draft PR #84). Family claude. Copied with `git show`.

SUT wave 1 (do not merge; copied with `git show`):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V332-001 | `cursor/v332-001-sut-17a0` @ `200a295` | `bc-26360eda-9c18-53b3-8dfd-02aa3dbccebd` | #87 |
| V332-002 | `cursor/v332-002-sut-17a0` @ `ea057ae` | `bc-d0ad2f0c-4f0b-5dbc-b184-9f1767dec196` | #85 |
| V332-003 | `cursor/v332-003-sut-17a0` @ `2e39753` | `bc-4a353ef9-3af0-5c91-bcc8-bf0cb18f44df` | #86 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true on all three. Skill SHA-256 matches T14.21.

SUT wave 2 (do not merge; copied with `git show`):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V332-004 | `cursor/v332-004-sut-17a0` @ `774e5fa` | `bc-449ab87e-33a7-5f64-b53f-a8fdc2f79493` | #90 |
| V332-005 | `cursor/v332-005-sut-17a0` @ `60db825` | `bc-c09f4d73-2477-545e-a84d-d7360a2c0bd9` | #89 |
| V332-006 | `cursor/v332-006-sut-17a0` @ `9f7cf5f` | `bc-660b0ddc-a33a-575b-bd8e-19f541b1e0ea` | #88 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true on all three. Skill SHA-256 matches T14.21.

SUT wave 3 (do not merge; copied with `git show`):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V332-007 | `cursor/v332-007-sut-17a0` @ `4dd7374` | `bc-2943695f-6356-5a76-82df-c8ce0952eba2` | #91 |
| V332-008 | `cursor/v332-008-sut-17a0` @ `95874ef` | `bc-47783ee1-ff71-53ff-8292-422c341b7f23` | #92 |
| V332-009 | `cursor/v332-009-sut-17a0` @ `3017c10` | `bc-400cfc7e-717d-5aca-8bae-9348b7f5f75d` | #93 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true on all three. V332-009 attested PNG read. Skill SHA-256 matches T14.21.

SUT wave 4 (do not merge; copied with `git show`):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V332-010 | `cursor/v332-010-sut-17a0` @ `a330d00` | `bc-375c6128-d790-5836-96f8-7573ecad627c` | #95 |
| V332-011 | `cursor/v332-011-sut-17a0` @ `d4bd6a3` | `bc-022740b3-60a1-5ceb-a1be-e98685d85a15` | #96 |
| V332-012 | `cursor/v332-012-sut-17a0` @ `6c2d5e2` | `bc-df0b26b4-4930-56b8-9a34-6a92d77da9ef` | #94 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true on all three. Skill SHA-256 matches T14.21.

SUT wave 5 (do not merge; copied with `git show`):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V332-013 | `cursor/v332-013-sut-17a0` @ `d64eefc` | `bc-1d83a396-7821-5e94-8348-526e90edf62c` | #97 |
| V332-014 | `cursor/v332-014-sut-17a0` @ `6d1f4a8` | `bc-05af00d7-1b2d-5c2e-8df8-1a3f9d9e874b` | #98 |
| V332-015 | `cursor/v332-015-sut-17a0` @ `98065ff` | `bc-67bb36a1-69c9-56ed-b555-203b342cea87` | #99 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true on all three. 014 and 015 have 3 turns. Skill SHA-256 matches T14.21.

SUT wave 6 (do not merge; copied with `git show`):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V332-016 | `cursor/v332-016-sut-17a0` @ `f898183` | `bc-c9de4a18-1b6e-503f-b578-f9001c3567ef` | #102 |
| V332-017 | `cursor/v332-017-sut-17a0` @ `72eb154` | `bc-e86de63f-3f86-5ce2-813c-4f405f59a06b` | #100 |
| V332-018 | `cursor/v332-018-sut-17a0` @ `263e43f` | `bc-2156fe7d-e89d-5eef-8b72-f227b32302a4` | #101 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true. V332-016 has 3 turns. V332-018 attested PNG read. Skill SHA-256 matches T14.21.

SUT freeze: `outputs-manifest-v332.json` SHA-256 `7bf0eb2fc752620295da37f335eaaf5020549878b1bdfd8e7f363e077f9deeec`. Extractor-visible SHA-256 `2cae5473e656b6956cd2ce059bcef1dbcbd70b9b0dc5b9fb06e1e55ce7c5dc6f`.

Gold-blind extractors (do not merge):

| N | family | intended branch | agent id |
| --- | --- | --- | --- |
| 1 | grok | `cursor/v332-extractor-grok-17a0` @ `797795c` (draft PR #103) | `bc-b8e0017c-0020-5e74-b9b3-3423fbdecb9f` |
| 2 | gemini | `cursor/v332-extractor-gemini-17a0` @ `82c0e23` (draft PR #104) | `bc-d058aaec-c92f-5b2b-8f2b-0c3b7d41240f` |

