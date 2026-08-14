# Benchmark v3.1 Semantic Match Results

- Status: `EVALUATIONS_FROZEN` then `SCORER_ERROR`
- Frozen at: `2026-08-14T05:17:25.221677Z`
- Matcher family: Claude
- Matcher context: `bc-5f0c3516-ef1c-5dcd-b9e9-1e797251d676`
- Source branch: `cursor/v31-matcher-claude-17a0@1e97d7cbbf0f222b14e897bc765df0c4f146476d` (copied with `git show`; not merged)
- Cases: 18
- Turns: 24
- Extracted claims: 59
- Semantic matches: 57
- Unsupported claims: 2 (`q-V31-015-1-1`, `q-V31-015-2-1`)
- Exact/alias matches: 0
- Canonical matches SHA-256: `d837eb00ecd87db9d59014c27038b075d77bdd6fffb311d78d95e18a71e6145e`
- Evaluation snapshot: `tests/benchmark/v3_1-holdout/cloud-cases/evaluation-manifest-v31.json`
- Evaluation snapshot SHA-256: `70ab4a3490a04ea68cd060502031712fe111479ce1ee8f5d6dad2e1526071f7d`
- Parent outputs manifest SHA-256: `993eb2a0429e8e4fddf4ac08c3617d1adc8373380a76c7701aef4c896d64403f`
- Parent extraction snapshot SHA-256: `a406161c1fac10f9c8b1f86c402891ac7dc81ac616abc8df0ebf9eb545c8b46e`

Validation:

- The matcher read exactly the frozen extraction snapshot, canonical evaluations, raw outputs, canonical gold, and ontology (SHA-256 verified).
- Every extracted claim has exactly one match decision. Non-null concept IDs are in that turn and domain's allowed gold list.
- Semantic decisions use confidence ≥ 0.8. Unsupported claims keep `concept_id: null`.
- V31-015 turns 1 and 2 ask a question while gold allows no question concepts, so those two claims are unsupported.
- Transcript audit: `gold_access=true`, `prohibited_content_access=false`. Re-reading authored `matches-v31.json` after write is `ACCEPTED_WITH_PROCEDURAL_DEVIATION`. Holdout was not pushed.
- The 12-artifact evaluation snapshot passed validation.
- Formal scoring ran once afterwards and recorded `SCORER_ERROR` (`manifest schema`). See `SCORE_RESULTS.md`.
- Runtime Skill files were not modified.
