# Benchmark v3.1 Gold-Blind Extraction Results

- Status: `EXTRACTION_SNAPSHOT_FROZEN`
- Frozen at: `2026-08-14T04:33:32.377685Z`
- Parent outputs manifest SHA-256: `993eb2a0429e8e4fddf4ac08c3617d1adc8373380a76c7701aef4c896d64403f`
- Extractor-visible SHA-256: `bbb623be7ff3a33124cf4f5285e96a9d552e13477dd17b1b8a58d18f67c60633`
- Canonical copy commit: `573f4762facbcee362f7a4dc2bbbbdb56ee4f15a`
- Gold-blind extractors: 2 (Claude, Gemini)
- Extraction adjudicator: GPT
- Cases: 18
- Turns: 24
- Extracted claims: 59 (8 questions, 51 revisions)
- Unresolved claim disagreements: 0
- Claim-count disagreements adjudicated: 10 turns
- Routes: 23 `Normal mode`, 1 `Intake` (V31-008; ratings null)
- Images opened: 0
- Prohibited gold/oracle/ontology/scorer access: 0 contexts
- Extraction snapshot: `tests/benchmark/v3_1-holdout/cloud-cases/extractions-manifest-v31.json`
- Extraction snapshot SHA-256: `a406161c1fac10f9c8b1f86c402891ac7dc81ac616abc8df0ebf9eb545c8b46e`
- Canonical evaluations SHA-256: `63cc05f43da57a426bb252dc50b137f63e7f531697848d2ae5e367fc14841aa2`

Source branches (copied with `git show`; not merged):

- extractor-1 Claude `cursor/v31-extractor-claude-17a0@553ee9846bb09a40f44e5a6ea205cea56d9dedee` (`bc-d8bcdf8c-3937-5830-847c-cb085ded528e`); raw `d3d7359f…`
- extractor-2 Gemini `cursor/v31-extractor-gemini-17a0@ae5871023e7e3ddc0fd444fa9f66bd4196973767` (`bc-407b6129-b25d-5064-9d64-5523806bbeb3`); raw `78a3abb7…`
- evaluator GPT `cursor/v31-extractor-adjudicator-17a0@94c1d4bde49cb9a3ff02a17da15b34372fe873eb` (`bc-f001181e-4ec6-5746-aaad-b4bd3ba288e3`); evaluations `be4d13b4…`

Validation:

- Both extractors covered 18 cases / 24 turns. Every `evidence_span` is a non-empty exact substring of that turn's frozen `raw_output`.
- Extractor-2 raw JSON records `context_id: unverified`; canonical evaluations and adjudication use the cloud context ID. Claim bytes were not rewritten.
- GPT adjudication retained Claude's claim set on count disagreements (finer revision splits; V31-008 Intake Next-step is not a Confirmation-needed question claim).
- Transcript audits: `gold_access=false`, `prohibited_content_access=false` for all three contexts. Verdict `PASS_WITH_PROCEDURAL_DEVIATION` for shared-checkout collision, git-recovery commands, placeholder Gemini context ID, and scripted adjudication.
- Dedicated extractor/adjudicator branches are linear from `ee5ac56` and were not merged into this holdout.
- The 15-artifact extraction snapshot passed validation against parent outputs manifest `993eb2a0…`.
- Semantic matching and formal scoring have not started.
- Runtime Skill files were not modified.
