# Benchmark v3.1 Isolated SUT Execution Results

- Status: `RAW_OUTPUTS_FROZEN`
- Frozen at: `2026-08-14T04:02:30.377606Z`
- Canonical parent: `f609800eba5f3e8f20b541f7776c1a427ca8aed2` (prepare SUT inputs; gold freeze parent)
- Shared delivery: `cursor/v31-sut-shared-delivery-17a0@a65e26961880130f237345c4ea74843b06399c22` (log only; not merged)
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Requested model: `gpt-5.6-sol-high-fast`
- Machine model ID: `unverified`
- Cases: 18
- Turns: 24
- Distinct cloud contexts: 18
- Direct image opens: 2 (`V31-008`, `V31-018`)
- Prohibited v3.1 gold/oracle/other-case content access: 0 cases
- Raw output SHA-256: `cf5ef7e28ca5bacd6e4e28e6bd2d92dfb5be61b34f51ce67bb4b40a7071be7b8`
- Output manifest: `tests/benchmark/v3_1-holdout/cloud-cases/outputs-manifest-v31.json`
- Output manifest SHA-256: `993eb2a0429e8e4fddf4ac08c3617d1adc8373380a76c7701aef4c896d64403f`
- Parent gold manifest SHA-256: `2aea483242418bdf73a56b0fdb921a718d4ea54c66611a8eae8d7bf7cf8e0377`

Validation:

- Every case used a distinct cloud context.
- Canonical files were extracted with `git show` from each case's own source commit. The seven shared-holdout commits were not merged.
- JSON deliveries were path-canonicalized without changing bytes. Markdown deliveries were wrapped so `raw_skill_output` equals the original Markdown.
- V31-008 and V31-018 opened their PNG paths directly.
- Transcript audits found no v3.1 gold, adjudication, oracle-notes, or other-case Skill-output content opens.
- Procedural deviations (shared-branch push, filename glob, historical-doc grep, schema path drift) are recorded in `sut-protocol-audits.json`.
- All runtime and input hashes, source raw/attestation hashes, turn coverage, distinct contexts, aggregate hashes, and parent-manifest links passed validation.
- The 46-artifact output manifest passed validation. `shared_delivery.not_canonical_parent` is true.
- Semantic extraction and scoring have not started.
- Runtime Skill files were not modified.
