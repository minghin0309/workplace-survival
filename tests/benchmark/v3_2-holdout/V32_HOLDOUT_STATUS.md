# Fresh v3.2 Holdout Status

- Status: `GOLD_ADJUDICATION_PENDING`
- Methodology: v3.2
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Holdout branch: `cursor/blind-v32-holdout-17a0`
- Cases: 18 (`V32-001`–`V32-018`)
- Turns: 24
- Formal scorer invocations: 0

Construction remains valid. Designer branch was copied with `git show` and not merged.

Gold labelers (all copied with `git show`, not merged):

- grok: `cursor/v32-gold-labeler-grok-17a0` @ `795d5b4`
- gemini: `cursor/v32-gold-labeler-gemini-17a0` @ `cc92b2d`
- gpt: `cursor/v32-gold-labeler-gpt-17a0-f8ea` @ `e1d8085`

All three: 18/24 coverage; allowlist-only; `question_design_accessed=false`; `skill_files_accessed=false`.

Adjudication has not started. Gold freeze (ontology + v3.2 scorer) has not started.

v3.1 remains archived as `SCORER_ERROR` and will not be rescored.
