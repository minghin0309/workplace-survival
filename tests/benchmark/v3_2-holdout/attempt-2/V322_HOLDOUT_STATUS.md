# Fresh v3.2 Holdout Attempt 2 Status

- Status: `CONSTRUCTION_VALID`
- Methodology: v3.2
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Holdout branch: `cursor/blind-v322-holdout-17a0`
- Cases: 18 (`V322-001`–`V322-018`)
- Turns: 24
- Formal scorer invocations: 0

Isolated designer `bc-f611a232-52e9-5f7a-b29b-17b77b53b375` on `cursor/v322-attempt2-cases-b375` @ `d68a006`. Copied with `git show`; that branch was not merged. PNGs hashed as bytes and not opened as images.

Manager-recipient gate passed: V322-017 is the only non-manager recipient. Construction validator: `tests/benchmark/v3_2-holdout/attempt-2/validate_holdout.py`.

Next: three isolated gold labelers (grok, gemini, gpt), then Claude adjudication, coverage, freeze, SUT only if `VALID_COVERAGE`.

Attempt 1 remains `INVALID_COVERAGE` and will not be rescored.
