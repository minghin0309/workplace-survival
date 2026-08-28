# V3.3 holdout attempt 4 — status

| Field | Value |
| --- | --- |
| `suite_id` | `v334-holdout-cloud-attempt4` |
| Skill runtime | T14.27 `805ae2e414987e759c72b970c382d23686783f74` |
| SKILL.md SHA-256 | `d67d64da68006d6f1502516eb39241a3d76a15bde35aac91e7dd279ee940e5af` |
| REFERENCE.md SHA-256 | `731e9001834fe1f4c8b201fd2a963cd6ec0c99b517c8abb43e4a083247c1fd02` |
| Methodology | v3.3 |
| Frozen attempt 1 | do not rescore |
| Frozen attempt 2 | do not rescore |
| Frozen attempt 3 | do not rescore |
| Construction | `VALID`; copied with `git show` from `cursor/v334-attempt4-cases-m4q7-17a0` @ `1513607` (artifacts `d460f3e`, not merged). Designer `bc-e26d9b6b-9931-516e-be55-5c2fc5db4a18`. |
| Gold | `VALID_COVERAGE`; frozen SHA-256 `2f78ce0662e2d0d885d5fe50a6c550d393afd61a08d5e661335e5ba60c398a18` (roles `gold` + `ontology` + `scorer`). Gold JSON SHA-256 `c3f4504b4f40ba86cc45d3ff006a5cdf42d6096a49af4dce877e211abe3aba41`. Uncertain 0/24. Copied from `cursor/v334-gold-adjudicator-17a0` @ `f1bd87b` (not merged). |
| SUT | waves 1–3 copied with `git show` (not merged). Wave 4 launching. |
| Extraction | not started |
| Matching | not started |
| Formal score | not started; one-shot after freezes |

Designer (do not merge): `cursor/v334-attempt4-cases-m4q7-17a0` @ `1513607`. Domain: Idleacre Nib Works, The Grind Loft. Image-only question V334-009 `occluded_role: data_a`. Readable image V334-018. V334-017 is the only non-manager recipient. Isolation: five allowlisted files only.

Gold labelers (do not merge):

| N | family | model | branch | agent id | draft PR |
| --- | --- | --- | --- | --- | --- |
| 1 | grok | `cursor-grok-4.5-high` | `cursor/v334-gold-labeler-1-17a0` @ `f6391e2` | `bc-71267ed7-00b7-5b7e-9a7f-98cf05712ec1` | #142 |
| 2 | gemini | `gemini-3.7-flash-high` | `cursor/v334-gold-labeler-2-17a0` @ `27235d7` | `bc-45804b0b-558e-541a-b2e2-0f33002e11e4` | #141 |
| 3 | gpt | `gpt-5.6-sol-high` | `cursor/v334-gold-labeler-3-17a0` @ `4f08836` | `bc-1b3b1f64-8753-5f26-92d0-09473d76c141` | #140 |

Isolation: `question_design_accessed` false, `skill_files_accessed` false on 1–3. Envelope: 18 cases / 24 turns each. Labeler 1 stores cases under `labels`; 2 and 3 use `cases`.

Adjudicator (do not merge): `cursor/v334-gold-adjudicator-17a0` @ `f1bd87b`. Family claude. Copied with `git show`. Isolation: question-design and Skill not read. Uncertain 0/24. Draft PR #143. Parent added ontology `definitions` to the holdout `gold-v334-raw.json` copy only; labels unchanged.

SUT wave 1 (do not merge):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V334-001 | `cursor/v334-001-sut-17a0` @ `cb681c9` | `bc-7f6f43e4-8244-50ab-8b09-4b62a5d7f071` | #145 |
| V334-002 | `cursor/v334-002-sut-17a0` @ `e2972d6` | `bc-dfc036f2-16f3-5753-8c1b-f0f8417af256` | #144 |
| V334-003 | `cursor/v334-003-sut-17a0` @ `cab876d` | `bc-1ef0f2ca-99dc-58c9-a31b-7523f2902550` | #146 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true. Skill SHA-256 matches T14.27.

SUT wave 2 (do not merge):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V334-004 | `cursor/v334-004-sut-17a0` @ `3c633f8` | `bc-d5c7067c-77ef-5f3e-948b-b09b67556333` | #149 |
| V334-005 | `cursor/v334-005-sut-17a0` @ `ffd9d9f` | `bc-d89c8122-d38e-51d9-9068-02f54e95b8d3` | #148 |
| V334-006 | `cursor/v334-006-sut-17a0` @ `542ca16` | `bc-d0539f69-a312-50ab-a355-355775b56605` | #147 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true on 004–006.

SUT wave 3 (do not merge):

| case | branch | agent id | draft PR |
| --- | --- | --- | --- |
| V334-007 | `cursor/v334-007-sut-17a0` @ `cea71e4` | `bc-03f09aa3-72b3-5a5d-8baf-40bb30e331fa` | #152 |
| V334-008 | `cursor/v334-008-sut-17a0` @ `f27df9b` | `bc-e5c50344-1bb3-5285-9dd2-1ea9beb54c76` | #150 |
| V334-009 | `cursor/v334-009-sut-17a0` @ `3ba6a7d` | `bc-8d964f87-d971-542d-8e75-aa5e1ee59f3e` | #151 |

Isolation: `gold_accessed` false, `other_cases_accessed` false, `question_design_accessed` false, `skill_files_accessed` true. V334-009 attested PNG read; hash matches construction.

Do not invent the workplace domain on this branch. Copy cases with `git show` from the dedicated designer branch after it validates.
