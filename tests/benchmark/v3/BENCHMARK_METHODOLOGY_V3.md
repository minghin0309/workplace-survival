# Blind Benchmark Methodology v3

## Scope

Version 3 changes benchmark construction and scoring only. It must not modify `.cursor/skills/workplace-survival/` or reinterpret any v2 result.

## Metric applicability

Every metric records:

- `value`: a number when its denominator is positive, otherwise `null`;
- `numerator`;
- `denominator`;
- `status`: `EVALUATED` or `NOT_APPLICABLE`.

A zero denominator is never:

- a score of 0;
- a score of 1;
- a threshold pass;
- a runtime exception.

`NOT_APPLICABLE` metrics are reported and excluded from threshold pass/fail aggregation.

## Pre-execution coverage gates

Coverage is validated and frozen before any SUT execution.

Minimum gold coverage:

- required question concepts: at least 3 concepts across at least 3 distinct cases;
- required revision concepts: at least 3 concepts across at least 3 distinct cases;
- accepted, non-uncertain turns: at least 1;
- gold-uncertain turns: no more than 20% of all turns.

Failure of a coverage gate makes the benchmark `INVALID_COVERAGE`. It is not a Skill failure and SUT execution must not start.

## Threshold policy

For a valid holdout:

- route accuracy ≥95%;
- responsibility accuracy ≥90%;
- tone accuracy ≥90%;
- overall accuracy ≥90%;
- required question-concept recall ≥90%;
- question-claim support precision =100%;
- required revision-concept recall ≥90%;
- revision-claim support precision =100%;
- critical invariant violations =0;
- gold uncertainty ≤20%.

Every required threshold metric must be `EVALUATED`. If a required metric becomes `NOT_APPLICABLE` despite passing pre-execution coverage, the score status is `INVALID_SCORING_INPUT`.

## Failure envelopes

The scorer writes exactly one immutable report for every invocation:

- `SCORED`: all validation and metric construction completed;
- `INVALID_COVERAGE`: preregistered gold coverage failed;
- `INVALID_SCORING_INPUT`: frozen inputs are internally inconsistent;
- `SCORER_ERROR`: an unexpected exception occurred.

Failure reports include:

- UTC execution time;
- scorer version and SHA-256;
- invocation arguments;
- frozen input paths and SHA-256 values;
- error type, message, and stage;
- coverage facts available at failure;
- `metrics: null` and `case_results: null` unless scoring completed;
- limitations;
- an explicit no-rerun identifier.

The scorer writes to a temporary location and atomically creates the requested report once. Existing reports are never overwritten.

## Version isolation

- v3 scorer validation uses synthetic fixtures only.
- v2 artifacts must not be supplied to the v3 scorer.
- A successful v3 implementation does not repair or replace the archived v2 outcome.
- Formal v3 scoring requires a fresh unseen holdout with a newly frozen artifact chain.
