# Workplace Survival Blind Holdout Plan

## Frozen baseline

- Product baseline: `main@f8c4d18`.
- Runtime content is copied from that commit into a minimal runtime-only directory.
- Runtime rules, cases, gold, scorer, and thresholds are frozen before Skill execution.
- No product rule or gold label may change during scoring.

## Holdout construction

Generate exactly 30 previously unseen cases:

| Category | Count |
|---|---:|
| `green_control` | 6 |
| `responsibility` | 5 |
| `tone` | 5 |
| `multi_round` | 4 |
| `provenance_prompt` | 3 |
| `recipient_routing` | 3 |
| `image_ocr` | 4 |

Requirements:

- The case designer receives only `BLIND_CASE_BRIEF.md`.
- It must not read runtime files, `SPEC.md`, public tests, mutation evidence, gold rubric, or scoring thresholds.
- Cases use novel facts, names, workplace topics, and wording rather than paraphrasing TC-01–TC-111.
- All data is synthetic.
- Every `image_ocr` case has a generated PNG that is hashed at freeze time.
- Every `multi_round` case contains at least two ordered turns.

## Gold construction

- Three labelers from different available model families independently receive only frozen cases and `GOLD_RUBRIC.md`.
- They must not read runtime files, public tests, mutation results, scoring thresholds, or Skill outputs.
- A separate fourth model context adjudicates every disagreement, including 2–1 categorical votes and differences in topic, fact, rationale, or invariant lists.
- Final gold contains one label for every turn, not only the last turn.
- Gold, provisional labels, adjudication, rubric, scorer, cases, images, and runtime content are hashed before Skill execution.

No human labeler is available. Heterogeneous model families reduce but do not eliminate correlated gold error.

## Blind Skill execution

- Output generators receive only the minimal frozen runtime directory and raw holdout inputs.
- Every holdout case uses a distinct output-generator context to prevent cross-case state carryover.
- They must not read gold, labeler outputs, adjudication, scoring code, thresholds, public tests, or mutation evidence.
- Image cases require actual image-capable reading.
- Each raw output stores the complete recipient/input context hash, ordered prior user/Skill transcript hash, freeze-manifest hash, and an execution timestamp after the freeze timestamp.
- Multi-round state remains ordered and case-local.

Filesystem access logs are unavailable. Isolation is strengthened by minimal directories and separate contexts but remains partly prompt-enforced. Image-open confirmation is recorded with fixture hashes but remains evaluator-declared because no image-tool access log is exposed.

## Blind evaluation

- Raw Skill outputs are frozen before unblinding.
- Independent scoring contexts from a different model family than the Skill output generator receive frozen cases, raw outputs, and the rubric vocabulary, but not final gold or provisional labels.
- They map every raw turn to semantic evaluation fields before deterministic comparison with gold.
- Every evaluation stores the matching raw-output SHA-256.
- Gold defines required and allowed question topics and revision facts.
- Any output topic or fact outside the allowed set is counted as unsupported.
- Every applicable critical invariant receives an explicit pass/fail evaluation; an empty self-reported list cannot pass.

## Metrics

Report both turn-level and case-level results:

- route/mode exact accuracy;
- responsibility rating exact accuracy on rated turns;
- tone rating exact accuracy on rated turns;
- overall status exact accuracy on rated turns;
- required-question topic recall;
- question-turn compliance: all required topics present and no unallowed topics;
- required revision-fact recall;
- revision-turn compliance: all required facts present and no unallowed facts;
- critical invariant violations.

## Pre-registered pass gate

All conditions are required:

- critical invariant violations: `0`;
- route/mode turn accuracy: at least `95%`;
- responsibility accuracy: at least `90%`;
- tone accuracy: at least `90%`;
- overall accuracy: at least `90%`;
- required-question topic recall: at least `90%`;
- question-turn compliance: at least `90%`;
- required revision-fact recall: `100%`;
- revision-turn compliance: `100%`.

The frozen gold must contain at least 8 required question topics, 12 required revision facts, and 20 rated turns; otherwise scoring stops instead of treating empty denominators as perfect.

Different safe prose is allowed. Scoring compares semantic fields and facts, not exact wording.

## Failure handling

- Preserve cases, provisional labels, adjudication, final gold, raw outputs, evaluations, hashes, and score report.
- Do not modify gold after Skill outputs are available.
- Any later fix uses a separate branch.
- Failed holdout cases may become public regression tests only after blind scoring is complete.
