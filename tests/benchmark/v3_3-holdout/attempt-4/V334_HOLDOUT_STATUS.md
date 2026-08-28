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
| Gold | `VALID_COVERAGE`; copied with `git show` from `cursor/v334-gold-adjudicator-17a0` @ `f1bd87b` (not merged). Uncertain 0/24. Adjudicator `bc-336c7d73-2281-5ca4-ac79-19399bd2c20f`. Draft PR #143. Freeze pending commit. |
| SUT | not started |
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

Do not invent the workplace domain on this branch. Copy cases with `git show` from the dedicated designer branch after it validates.
