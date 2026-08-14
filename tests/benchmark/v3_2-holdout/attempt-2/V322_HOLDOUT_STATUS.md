# Fresh v3.2 Holdout Attempt 2 Status

- Status: `GOLD_ADJUDICATION_COPIED`
- Methodology: v3.2
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Holdout branch: `cursor/blind-v322-holdout-17a0`
- Cases: 18 (`V322-001`–`V322-018`)
- Turns: 24
- Formal scorer invocations: 0

Isolated Claude adjudicator `bc-e04fe64d-78e0-5f19-89f2-a5a3548ab8b4` on `cursor/v322-gold-adjudicator-claude-17a0` @ `187767e`. Copied with `git show`; that branch was not merged. Gold was not rewritten.

Next: `finalize_gold.py` coverage. Freeze (ontology + `score_semantic_v3_2.py`) only if `VALID_COVERAGE`. SUT only if authorized.

Attempt 1 remains `INVALID_COVERAGE` and will not be rescored.
