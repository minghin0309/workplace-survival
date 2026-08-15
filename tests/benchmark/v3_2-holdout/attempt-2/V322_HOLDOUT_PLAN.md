# Fresh Benchmark v3.2 Holdout Attempt 2 Plan

- Methodology: v3.2 freeze-chain scorer plus v3.1 question-candidate contract plus manager-recipient contract.
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`.
- Cases: 18 (`V322-001`–`V322-018`).
- Turns: 24.
- Attempt 1 remains `INVALID_COVERAGE` and is not rescored.
- v3.1 remains `SCORER_ERROR` and is not rescored.
- Millinery and harpworks domains are denylisted.

Gold freeze must include canonical gold, `tests/benchmark/SEMANTIC_ONTOLOGY.json`, and `tests/benchmark/v3_2/score_semantic_v3_2.py`.

Pre-SUT gates:

- construction contract, manager-recipient envelope, and candidate mutations pass;
- required question concepts ≥3 across ≥3 adjudicated gold cases;
- required revision concepts ≥3 across ≥3 cases;
- accepted turns ≥1;
- gold uncertainty ≤20%.

If any gate fails, SUT, extraction, matching, and scoring stop. If all gates pass, every case executes in a distinct cloud context. Dual gold-blind extractors and one matcher (not a gold-labeler family) run on dedicated branches and are copied with `git show`. The v3.2 scorer runs exactly once after evaluation freeze.

Isolation: this parent has seen millinery and harpworks gold and must not author cases. The case designer is an isolated cloud agent that may read only `tests/benchmark/v3_2/V32_ATTEMPT2_CASE_BRIEF.md`.
