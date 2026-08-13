# Benchmark v2 Isolated SUT Execution Results

- Status: `RAW_OUTPUTS_FROZEN`
- Frozen at: `2026-08-13T11:01:26.298529Z`
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Requested model: `gpt-5.6-sol-high-fast`
- Machine model ID: `unverified`
- Cases: 18
- Turns: 24
- Distinct cloud contexts: 18
- Direct image opens: 2
- Prohibited benchmark-content access: 0 cases
- Raw output SHA-256: `7755df7128e99f97245f7c62bb41f7ade80f9bd17e5fd177738076f3741dace4`
- Output manifest: `tests/benchmark/v2-holdout/cloud-cases/outputs-manifest-v2.json`
- Output manifest SHA-256: `5a9807579303a0002c0c2c0833d7b9f56fe57594895584e14b7cac0c3918d2e2`
- Parent gold manifest SHA-256: `0806da52e7414c1f30cb83fba3b257e630079102c9c50813ccf3dcad21796084`

Validation:

- Every case used a distinct cloud context.
- SUT-visible inputs excluded category, image specification, design intent, difficulty notes, gold, and oracle data.
- Every context read only its case input, the four frozen runtime files, and its assigned PNG when applicable.
- V2-011, V2-012, and V2-013 preserved three-turn sequential state in one context each.
- V2-017 and V2-018 opened their PNG paths directly.
- Transcript audits found no gold, adjudication, scorer, oracle, other-case, or expected-answer access.
- Raw source schemas varied; canonical aggregation preserves every exact Skill response string and source JSON pointer.
- Procedural and metadata deviations are recorded per case in `sut-protocol-audits.json`.
- All runtime and input hashes, source raw/attestation hashes, turn coverage, distinct contexts, aggregate hashes, and parent-manifest links passed validation.
- The 42-artifact output manifest passed recursive v2 validation.
- Semantic extraction and scoring have not started.
- Runtime Skill files were not modified.
