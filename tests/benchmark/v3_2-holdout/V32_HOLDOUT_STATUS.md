# Fresh v3.2 Holdout Status

- Status: `INVALID_COVERAGE`
- Attempt: `v32-holdout-cloud-attempt1`
- Methodology: v3.2
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Holdout branch: `cursor/blind-v32-holdout-17a0`
- Cases: 18 (`V32-001`–`V32-018`)
- Turns: 24
- Formal scorer invocations: 0
- SUT execution authorized: no

Coverage: 1 required question concept across 1 case (gate: ≥3 / ≥3). Revision coverage passed (6 / 3). Uncertainty 4.17%.

Question candidates were constructed as non-manager recipients and gold-routed `Scope`. Gold was not rewritten. Isolated branches were copied with `git show` and not merged.

v3.1 remains archived as `SCORER_ERROR` and will not be rescored.
