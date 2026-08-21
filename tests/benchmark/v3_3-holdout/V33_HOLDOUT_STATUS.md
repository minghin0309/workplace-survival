# V3.3 holdout attempt 1 — status

| Field | Value |
| --- | --- |
| `suite_id` | `v33-holdout-cloud-attempt1` |
| Skill runtime | T14.15 `d37540b33db3005daddab705c1f108c4c5eb9be9` |
| Methodology | v3.3 |
| Frozen attempt 3 | do not rescore |
| Construction | `VALID`; copied with `git show` from `cursor/v33-attempt1-cases-r8n3-17a0` @ `1c9a8da` (not merged) |
| Gold | labelers in flight (isolated, not merged). Labelers 2 and 3 pushed; 1 still running. Adjudicator not launched. |
| SUT | not started |
| Formal score | not started |

Gold labelers (do not merge these branches):

| N | family | model | intended branch | agent id |
| --- | --- | --- | --- | --- |
| 1 | grok | `cursor-grok-4.5-high` | `cursor/v33-gold-labeler-1-17a0` | `bc-bebb1f57-000e-58af-92c0-9b4c79a38ddd` |
| 2 | gemini | `gemini-3.7-flash-high` | `cursor/v33-gold-labeler-2-17a0` @ `b6ec2ee` (draft PR #52, do not merge) | `bc-13bfabd7-ed7a-5efd-991b-63011b351d56` |
| 3 | gpt | `gpt-5.6-sol-high` | `cursor/v33-gold-labeler-3-17a0` @ `6482685` (draft PR #51, do not merge) | `bc-dea0250b-6f80-538e-bfa6-0f9be2c8273b` |

Copy onto holdout with `git show` after all three finish. Then launch one Claude-family gold adjudicator.
