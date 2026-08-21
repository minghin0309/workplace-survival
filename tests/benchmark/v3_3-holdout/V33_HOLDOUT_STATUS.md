# V3.3 holdout attempt 1 — status

| Field | Value |
| --- | --- |
| `suite_id` | `v33-holdout-cloud-attempt1` |
| Skill runtime | T14.15 `d37540b33db3005daddab705c1f108c4c5eb9be9` |
| Methodology | v3.3 |
| Frozen attempt 3 | do not rescore |
| Construction | `VALID`; copied with `git show` from `cursor/v33-attempt1-cases-r8n3-17a0` @ `1c9a8da` (not merged) |
| Gold | `VALID_COVERAGE`; frozen SHA-256 `b3e08901063eb2377285f0dac02501a9e07b34631182425e719addedb0d15bc7` (roles `gold` + `ontology` + `scorer`) |
| SUT | wave 1 copied: V33-001/002/003 (`git show`, not merged). 004–018 queued (VM cap 3; 003 agent still wrapping). |
| Formal score | not started |

SUT wave 1 (do not merge):

| case | branch | agent id |
| --- | --- | --- |
| V33-001 | `cursor/v33-001-sut-17a0` @ `690e2ce` (draft PR #56) | `bc-7f8abf82-614c-55ea-bcfa-69dfbf78afc1` |
| V33-002 | `cursor/v33-002-sut-17a0` @ `dd2e5e4` (draft PR #55) | `bc-05aed183-eab3-51ae-84ee-f0aac9f1f053` |
| V33-003 | `cursor/v33-003-sut-17a0` @ `a4f9f1f` (draft PR #57) | `bc-1d281964-ccf4-542e-9e02-e8af775c299a` |

Gold labelers (do not merge these branches):

| N | family | model | branch | agent id |
| --- | --- | --- | --- | --- |
| 1 | grok | `cursor-grok-4.5-high` | `cursor/v33-gold-labeler-1-17a0` @ `332d289` (draft PR #53, do not merge) | `bc-bebb1f57-000e-58af-92c0-9b4c79a38ddd` |
| 2 | gemini | `gemini-3.7-flash-high` | `cursor/v33-gold-labeler-2-17a0` @ `b6ec2ee` (draft PR #52, do not merge) | `bc-13bfabd7-ed7a-5efd-991b-63011b351d56` |
| 3 | gpt | `gpt-5.6-sol-high` | `cursor/v33-gold-labeler-3-17a0` @ `6482685` (draft PR #51, do not merge) | `bc-dea0250b-6f80-538e-bfa6-0f9be2c8273b` |

Adjudicator (do not merge): `cursor/v33-gold-adjudicator-17a0` @ `3afe8c5` (draft PR #54). Copied with `git show`. Coverage: 6 question concepts / 6 cases, 30 revision concepts / 17 cases, uncertain 1/24.
