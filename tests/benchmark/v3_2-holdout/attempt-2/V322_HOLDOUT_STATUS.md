# Fresh v3.2 Holdout Attempt 2 Status

- Status: `EXTRACTIONS_COPIED`
- Dual gold-blind extractors copied with `git show` (not merged): grok, gemini. Routes/ratings agree (22 Normal, 1 Intake, 1 Scope). Revision claim counts differ (24 vs 9); GPT adjudication is next.

- Methodology: v3.2
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Holdout branch: `cursor/blind-v322-holdout-17a0`
- Cases: 18
- Turns: 24
- Distinct SUT contexts: 18
- Coverage: `VALID_COVERAGE`
- Formal scorer invocations: 0

All 18 SUT cases copied with `git show` from dedicated branches. Those branches were not merged. Direct image opens: V322-008, V322-018.

Extractor-1 (grok) protocol deviation: off-allowlist read of `SKILL.md`; Skill was not modified.

Next: isolated GPT extraction adjudicator, freeze extraction snapshot, Claude matcher (not grok/gemini/gpt), freeze evaluations, one v3.2 scorer invocation.

Attempt 1 remains `INVALID_COVERAGE` and will not be rescored.
