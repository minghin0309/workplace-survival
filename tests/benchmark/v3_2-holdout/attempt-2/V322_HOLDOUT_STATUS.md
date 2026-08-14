# Fresh v3.2 Holdout Attempt 2 Status

- Status: `GOLD_LABELS_COPIED`
- Methodology: v3.2
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Holdout branch: `cursor/blind-v322-holdout-17a0`
- Cases: 18 (`V322-001`–`V322-018`)
- Turns: 24
- Formal scorer invocations: 0

Construction `VALID`. Isolated designer `bc-f611a232-52e9-5f7a-b29b-17b77b53b375` copied with `git show`.

Gold labels copied with `git show` (labeler branches not merged):

- grok `cursor/v322-gold-labeler-1-17a0` @ `f7c765a`
- gemini `cursor/v322-gold-labeler-2-17a0` @ `10fdfd3`
- gpt `cursor/v322-gold-labeler-3-17a0` @ `4a7f9f8`

Next: isolated Claude adjudication, then `finalize_gold.py` / coverage. SUT only if `VALID_COVERAGE`.

Attempt 1 remains `INVALID_COVERAGE` and will not be rescored.
