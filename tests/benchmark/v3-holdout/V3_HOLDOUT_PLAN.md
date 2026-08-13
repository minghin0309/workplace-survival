# Benchmark v3 Fresh Holdout Plan

- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Methodology base: `cursor/benchmark-methodology-v3-17a0@183812f`
- Cases: 18
- Turns: 24
- Images: 2 PNG fixtures
- Historical v1/v2 cases, gold, outputs, and scores are prohibited construction inputs.

Distribution:

- 3 Green controls;
- 4 material-information cases designed to require clarifying questions;
- 3 responsibility boundaries;
- 2 tone boundaries;
- 3 three-turn state/correction cases;
- 1 recipient-routing case;
- 2 image/OCR cases.

Gold:

- three independent labelers from distinct model families;
- fourth-family adjudicator;
- no human reviewer available;
- three-way categorical or unresolved critical-invariant disagreement becomes `gold_uncertain`;
- uncertainty must not exceed 20%.

Pre-SUT v3 coverage gates:

- required question concepts: at least 3 across at least 3 cases;
- required revision concepts: at least 3 across at least 3 cases;
- at least 1 accepted turn;
- gold uncertainty no more than 20%.

Execution:

- each case runs in a distinct cloud context;
- SUT receives only frozen runtime, explicit recipient context, Data A, ordered raw turns, and its assigned image;
- raw outputs freeze before extraction;
- two gold-blind extractor families review all claims;
- extraction freezes before matcher gold access;
- semantic matching freezes before scoring;
- the v3 scorer executes exactly once.

Thresholds:

- route accuracy ≥95%;
- responsibility, tone, and overall accuracy ≥90%;
- required question/revision concept recall ≥90%;
- question/revision claim support precision =100%;
- critical invariant violations =0;
- gold uncertainty ≤20%.

Failure handling:

- invalid coverage stops before SUT execution;
- every scorer invocation writes one immutable report;
- failures never trigger an in-version scorer fix or rerun;
- product, gold, matcher, and harness defects remain separately classified.
