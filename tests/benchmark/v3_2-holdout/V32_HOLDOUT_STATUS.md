# Fresh v3.2 Holdout Status

- Status: `GOLD_LABELING_IN_PROGRESS`
- Methodology: v3.2
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Holdout branch: `cursor/blind-v32-holdout-17a0`
- Cases: 18 (`V32-001`–`V32-018`)
- Turns: 24
- Formal scorer invocations: 0

Construction remains valid. Designer branch was copied with `git show` and not merged.

Gold:

- labeler-3 (gpt) copied from `cursor/v32-gold-labeler-gpt-17a0-f8ea` @ `e1d8085`; not merged;
- 18 cases / 24 turns; allowlist-only reads; `question_design_accessed=false`; `skill_files_accessed=false`;
- labeler-1 (grok) and labeler-2 (gemini) still running;
- adjudication not started.

v3.1 remains archived as `SCORER_ERROR` and will not be rescored.
