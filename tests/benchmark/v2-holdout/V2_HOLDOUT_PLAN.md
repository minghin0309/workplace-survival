# Benchmark v2 Fresh Holdout Plan

- Frozen runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`.
- Cases: 18.
- Turns: at least 21.
- Images: 2 actual PNG fixtures.

Distribution:

- 4 Green controls;
- 3 responsibility boundaries;
- 3 tone boundaries;
- 3 multi-round cases;
- 2 provenance/prompt cases;
- 1 recipient-routing case;
- 2 image/OCR cases.

Gold:

- Claude, Grok, and Kimi label independently.
- GPT fourth-family adjudication.
- No human reviewer is available.
- Three-way categorical or critical-invariant disagreements without human review become `gold_uncertain`.
- Gold-uncertain turns must not exceed 20%.

Execution:

- Each case runs in a distinct cloud context.
- SUT receives only runtime files plus explicit `recipient_context`, `data_a`, and raw turns.
- `oracle-notes.json` is unavailable to SUT and gold labelers.
- Raw outputs freeze before extraction.
- Two gold-blind extractor families review claim completeness.
- Semantic matcher runs only after output and gold freeze.

Pass thresholds:

- route accuracy ≥95%;
- responsibility, tone, and overall accuracy ≥90%;
- required question/revision concept recall ≥90%;
- question/revision claim support precision =100%;
- critical invariant violations =0;
- gold uncertainty ≤20%.

Historical blind results remain unchanged.
