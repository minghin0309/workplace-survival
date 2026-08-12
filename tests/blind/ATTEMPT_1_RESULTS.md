# Blind Holdout Attempt 1

## Outcome

Status: `INVALID — HARNESS FAILURE`

No accuracy metric or pass/fail conclusion is reported for the Skill.

## What completed

- 30 unseen synthetic cases were generated.
- Four image fixtures were rendered and hashed.
- Three heterogeneous model families independently produced gold labels.
- A fourth model family adjudicated all 240 field-level disagreements.
- Cases, images, provisional labels, adjudication, final gold, rubric, scorer, and runtime were frozen before Skill execution.
- Thirty separate Skill contexts produced 37 raw turn outputs.
- Raw Skill output text was frozen before semantic evaluation.
- A gold-blind Claude evaluator mapped all outputs to semantic fields.

## Why scoring stopped

The preregistered scorer rejected the evidence before calculating accuracy:

1. Attempt 1 used the hash of `outputs.json` where the schema required the hash of `outputs-freeze.json`. This was a mechanical evaluator metadata error and was corrected without changing semantic evaluations.
2. Attempt 2 then rejected `BH-001` because the normalized `case_input_sha256` used a different serialization from the preregistered scorer.

The second mismatch means the output evidence envelope does not satisfy the frozen input-linkage contract. Changing the frozen scorer or re-freezing metadata after unblinding would violate the preregistered chronology, so the run was stopped.

## Unscored evaluator observation

Before scoring, the gold-blind semantic evaluator marked `BH-006` turn 1 as failing `fixed-format-or-valid-nonreview-route`: the Skill returned a bare rewrite without mode, ratings, or required review sections. This is preserved as an observation, not reported as a scored holdout failure because the run did not pass its evidence-linkage gate.

## Integrity statement

- No gold label was edited after Skill output generation.
- No raw Skill output was edited.
- No metric was calculated selectively.
- The consumed holdout will not be reused as a fresh blind set.
- Both failed score reports and all available artifacts are preserved in `tests/blind/attempt-1/`.

## Method lessons

- Raw outputs should be normalized by deterministic code, not by a free-form normalizer agent.
- The output schema and scorer must share one serialization helper.
- Evidence metadata must be validated before freezing outputs.
- A future retry requires newly generated unseen cases and gold.
