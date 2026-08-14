# Fresh v3.1 Holdout Status

- Status: `EXTRACTION_SNAPSHOT_FROZEN`
- Cases: 18
- Turns: 24
- Gold-uncertain turns: 1
- Gold uncertainty: 4.17%
- Required question concepts: 6
- Cases with required questions: 6
- Required revision concepts: 70
- Cases with required revisions: 18
- SUT execution authorized: yes
- SUT contexts executed: 18
- Distinct SUT contexts: 18
- Gold-blind extractors: 2
- Extraction adjudicator: 1
- Unresolved claim disagreements: 0
- Formal scorer invocations: 0

Construction:

- attempt 1 was rejected for prior-domain reuse;
- attempt 2 uses a new bespoke millinery domain;
- six question candidates cover approval authority, deadline, recipient, source, measurement, and decision option;
- all 18 construction mutations passed;
- case content, gold, construction-only answers, and SUT-visible data remain separated.

Gold:

- three independent families: Grok, Kimi, GPT;
- fourth-family adjudicator: Claude;
- incomplete/contaminated labeler attempts were rejected;
- all votes and the one three-way turn remain preserved;
- v3 coverage gates passed before SUT execution.

SUT:

- 18 isolated cloud contexts produced raw Skill outputs;
- five cases raced onto the shared holdout branch; those seven commits are preserved on `cursor/v31-sut-shared-delivery-17a0` as a delivery log and were not merged;
- each case's two files were extracted from its own source commit and path-canonicalized;
- protocol audits record glob/rebase/schema deviations; no v3.1 gold content was opened;
- canonical parent remains `f609800` / gold manifest `2aea483242418bdf73a56b0fdb921a718d4ea54c66611a8eae8d7bf7cf8e0377`.

Extraction:

- two gold-blind extractors (Claude, Gemini) plus a GPT adjudicator ran on dedicated branches;
- those branches were copied with `git show` and were not merged into this holdout;
- all three contexts: `gold_access=false`, `prohibited_content_access=false`;
- shared-checkout harness collision is recorded as `PASS_WITH_PROCEDURAL_DEVIATION`;
- canonical evaluations keep 8 question claims and 51 revision claims (Claude's finer splits; V31-008 Intake Next-step is not a Confirmation-needed claim);
- extractor-2 raw `context_id` remains `unverified`; canonical evaluations record `bc-407b6129-b25d-5064-9d64-5523806bbeb3`.

Frozen evidence:

- canonical gold SHA-256: `bb8fbf70ac84e8718fef8abd0d2f7d53aee07213343b25f418db8329e1bedf2d`
- coverage report SHA-256: `576a3e116fe3119cbc55e4b75566b36975a72b074a690d43dccf59bf1ec067cd`
- gold manifest SHA-256: `2aea483242418bdf73a56b0fdb921a718d4ea54c66611a8eae8d7bf7cf8e0377`
- raw SUT outputs SHA-256: `cf5ef7e28ca5bacd6e4e28e6bd2d92dfb5be61b34f51ce67bb4b40a7071be7b8`
- outputs manifest SHA-256: `993eb2a0429e8e4fddf4ac08c3617d1adc8373380a76c7701aef4c896d64403f`
- gold-blind extractor-visible SHA-256: `bbb623be7ff3a33124cf4f5285e96a9d552e13477dd17b1b8a58d18f67c60633`
- canonical evaluations SHA-256: `63cc05f43da57a426bb252dc50b137f63e7f531697848d2ae5e367fc14841aa2`
- extraction snapshot SHA-256: `a406161c1fac10f9c8b1f86c402891ac7dc81ac616abc8df0ebf9eb545c8b46e`

Matching and formal scoring have not started.
