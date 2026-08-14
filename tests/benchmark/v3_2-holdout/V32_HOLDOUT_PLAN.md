# Fresh Benchmark v3.2 Holdout Plan

- Methodology: benchmark v3.2 freeze-chain scorer plus the v3.1 question-case construction contract.
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`.
- Cases: 18 (`V32-001`–`V32-018`).
- Turns: 24.
- Required-question candidates: 6 across six distinct concepts.
- Historical v1/v2/v3/v3.1 case content is prohibited.
- v3.1 millinery holdout is archived `SCORER_ERROR` and is never rescored.
- v3.1 holdout artifacts must not be supplied to the v3.2 scorer.

Gold freeze must include:

- canonical gold;
- `tests/benchmark/SEMANTIC_ONTOLOGY.json`;
- `tests/benchmark/v3_2/score_semantic_v3_2.py`.

Manifest `version` is `3.2`. Extra freeze keys are allowed. Gold may omit `parent_manifest`.

Pre-SUT gates:

- construction contract and all candidate mutations pass;
- required question concepts ≥3 across ≥3 adjudicated gold cases;
- required revision concepts ≥3 across ≥3 cases;
- accepted turns ≥1;
- gold uncertainty ≤20%.

If any gate fails, SUT, extraction, matching, and scoring stop. If all gates pass, every case executes in a distinct cloud context. Dual gold-blind extractors and one matcher (not grok/kimi/gpt if those families labeled gold) run on dedicated branches and are copied with `git show`; those branches are never merged. The v3.2 scorer runs exactly once after evaluation freeze.

Isolation:

- this parent has seen millinery gold/cases and must not author cases;
- the case designer is an isolated cloud agent that may read only `V32_CASE_BRIEF.md`;
- designer artifacts land on a dedicated branch and are copied onto this holdout with `git show`;
- Task subagents share the parent checkout unless `environment: cloud`; extractors, matcher, and case designer must be cloud-isolated.

Thresholds remain those preregistered by Methodology v3 / v3.2.
