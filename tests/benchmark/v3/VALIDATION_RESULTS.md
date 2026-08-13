# Benchmark Methodology v3 Validation Results

- Executed at: `2026-08-13T12:47:42Z`
- Branch: `cursor/benchmark-methodology-v3-17a0`
- Base: `cursor/blind-v2-holdout-17a0`
- Runtime Skill changes: none
- v2 artifact changes: none
- v2 scorer invocations during v3 validation: 0

Unit validation:

- Tests: 10
- Passed: 10
- Failed: 0
- Fixtures: synthetic only

Covered behavior:

- zero denominators return `value: null` and `status: NOT_APPLICABLE`;
- zero or sparse required-question coverage fails before SUT execution;
- minimum question and revision coverage passes;
- invalid coverage writes an immutable `INVALID_COVERAGE` envelope;
- unexpected exceptions write an immutable `SCORER_ERROR` envelope;
- successful synthetic scoring writes evaluated threshold records;
- a required threshold with zero output-claim denominator produces `INVALID_SCORING_INPUT`;
- existing reports cannot be overwritten.

Mutation validation:

- Baseline passed: yes
- Mutants killed: 3/3
- Mutation score: 100%
- `M1_ZERO_DENOMINATOR_DIVIDES`: killed by zero-denominator tests
- `M2_COVERAGE_MINIMUM_DISABLED`: killed by zero/sparse coverage tests
- `M3_EXCEPTION_ENVELOPE_DISABLED`: killed by failure-envelope test
- Import or harness failures are explicitly rejected and cannot count as mutant kills.

Isolation:

- No v2 holdout path appears in v3 scorer or test code.
- v3 validation did not supply v2 gold, outputs, evaluations, matches, manifests, or score evidence to the scorer.
- Frozen v2 scorer and validator files are unchanged.
- The archived v2 result remains `SCORER_ERROR` and was not rescored.
