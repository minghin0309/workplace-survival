# Fresh v3.2 Holdout Attempt 2 Status

- Status: `GOLD_FROZEN`
- Methodology: v3.2
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Holdout branch: `cursor/blind-v322-holdout-17a0`
- Cases: 18 (`V322-001`–`V322-018`)
- Turns: 24
- Coverage: `VALID_COVERAGE` (6 question concepts / 6 cases; 41 revision concepts / 16 cases; 0 uncertain)
- Gold manifest: `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/gold-manifest-v322.json`
- Gold manifest SHA-256: `96c2ff593e42a0b909a5f4fd39a66835a5f12da4b95208d4464796cafa23a432`
- SUT execution authorized: yes
- Formal scorer invocations: 0

Gold freeze includes canonical gold, ontology, and `score_semantic_v3_2.py`. Gold was not rewritten.

Next: 18 distinct cloud SUT contexts. Dual gold-blind extractors and one matcher (not grok/gemini/gpt) after SUT copy. One v3.2 scorer invocation after evaluation freeze.

Attempt 1 remains `INVALID_COVERAGE` and will not be rescored.
