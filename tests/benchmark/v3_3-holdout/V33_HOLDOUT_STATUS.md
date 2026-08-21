# V3.3 holdout attempt 1 — status

| Field | Value |
| --- | --- |
| `suite_id` | `v33-holdout-cloud-attempt1` |
| Skill runtime | T14.15 `d37540b33db3005daddab705c1f108c4c5eb9be9` |
| Methodology | v3.3 |
| Frozen attempt 3 | do not rescore |
| Construction | `VALID`; copied with `git show` from `cursor/v33-attempt1-cases-r8n3-17a0` @ `1c9a8da` (not merged) |
| Gold | `VALID_COVERAGE`; frozen SHA-256 `b3e08901063eb2377285f0dac02501a9e07b34631182425e719addedb0d15bc7` (roles `gold` + `ontology` + `scorer`) |
| SUT | wave 1–4 copied (V33-001–012); V33-014 and V33-015 copied. V33-013 still running. 016–018 queued. |
| Formal score | not started |

SUT wave 1 (do not merge):

| case | branch | agent id |
| --- | --- | --- |
| V33-001 | `cursor/v33-001-sut-17a0` @ `690e2ce` (draft PR #56) | `bc-7f8abf82-614c-55ea-bcfa-69dfbf78afc1` |
| V33-002 | `cursor/v33-002-sut-17a0` @ `dd2e5e4` (draft PR #55) | `bc-05aed183-eab3-51ae-84ee-f0aac9f1f053` |
| V33-003 | `cursor/v33-003-sut-17a0` @ `a4f9f1f` (draft PR #57) | `bc-1d281964-ccf4-542e-9e02-e8af775c299a` |

SUT wave 2 (do not merge):

| case | branch | agent id |
| --- | --- | --- |
| V33-004 | `cursor/v33-004-sut-17a0` @ `e27bec0` (draft PR #59) | `bc-1d375675-1943-528d-977a-7a6468c4040b` |
| V33-005 | `cursor/v33-005-sut-17a0` @ `c585546` (draft PR #60) | `bc-94411713-75b4-54fa-8f9a-ba2be808e8b5` |
| V33-006 | `cursor/v33-006-sut-17a0` @ `998d5b7` (draft PR #58) | `bc-1e556a03-877b-54ed-8b7e-0465bb64fc92` |

SUT wave 3 (do not merge):

| case | branch | agent id |
| --- | --- | --- |
| V33-007 | `cursor/v33-007-sut-17a0` @ `4528848` (draft PR #61) | `bc-91ce3dab-914d-5456-a5ab-7eb726a4fa5e` |
| V33-008 | `cursor/v33-008-sut-17a0` @ `a100ad5` (draft PR #62) | `bc-672d2e1d-7861-5352-bc5d-7b56ba4141f3` |
| V33-009 | `cursor/v33-009-sut-17a0` @ `2bfdf5e` (draft PR #63) | `bc-dc842e47-c25f-5277-9168-8819fc882064` |

SUT wave 4 (do not merge):

| case | branch | agent id |
| --- | --- | --- |
| V33-010 | `cursor/v33-010-sut-17a0` @ `913dcd7` (draft PR #64) | `bc-028d6530-587a-5450-9206-5bbfa0035d7b` |
| V33-011 | `cursor/v33-011-sut-17a0` @ `cf6734b` (draft PR #65) | `bc-fa7e26b9-e683-5016-94af-02fb69725239` |
| V33-012 | `cursor/v33-012-sut-17a0` @ `dacd0f9` (draft PR #66) | `bc-70faf7e6-b3e2-5855-bb26-b2e4d2d5a36f` |

SUT wave 5 (do not merge):

| case | branch | agent id |
| --- | --- | --- |
| V33-013 | `cursor/v33-013-sut-17a0` | `bc-23cdcc5d-6327-5b4b-a398-ff6e0eb99707` |
| V33-014 | `cursor/v33-014-sut-17a0` @ `5d0a14f` (draft PR #68) | `bc-1a10f2f2-1cfe-564a-a583-8450ef1d7d52` |
| V33-015 | `cursor/v33-015-sut-17a0` @ `fdd9af5` (draft PR #67) | `bc-5a99ccfd-3baa-5d24-a262-c6f4dbeb1b6b` |

Gold labelers (do not merge these branches):

| N | family | model | branch | agent id |
| --- | --- | --- | --- | --- |
| 1 | grok | `cursor-grok-4.5-high` | `cursor/v33-gold-labeler-1-17a0` @ `332d289` (draft PR #53, do not merge) | `bc-bebb1f57-000e-58af-92c0-9b4c79a38ddd` |
| 2 | gemini | `gemini-3.7-flash-high` | `cursor/v33-gold-labeler-2-17a0` @ `b6ec2ee` (draft PR #52, do not merge) | `bc-13bfabd7-ed7a-5efd-991b-63011b351d56` |
| 3 | gpt | `gpt-5.6-sol-high` | `cursor/v33-gold-labeler-3-17a0` @ `6482685` (draft PR #51, do not merge) | `bc-dea0250b-6f80-538e-bfa6-0f9be2c8273b` |

Adjudicator (do not merge): `cursor/v33-gold-adjudicator-17a0` @ `3afe8c5` (draft PR #54). Copied with `git show`. Coverage: 6 question concepts / 6 cases, 30 revision concepts / 17 cases, uncertain 1/24.
