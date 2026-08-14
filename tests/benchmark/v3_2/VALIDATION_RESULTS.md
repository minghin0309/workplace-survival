# Benchmark Methodology v3.2 Validation Results

- Executed at: `2026-08-14T09:15:00Z`
- Branch: `cursor/benchmark-methodology-v32-17a0`
- Base: `cursor/blind-v31-holdout-17a0`
- Runtime Skill changes: none
- v2 artifact changes: none
- v3 scorer changes: none
- v3.1 holdout artifact changes: none
- v3.1 scorer invocations during v3.2 validation: 0

Unit validation:

- Tests: 12
- Passed: 12
- Failed: 0
- Fixtures: synthetic only

Covered behavior:

- zero denominators return `value: null` and `status: NOT_APPLICABLE`;
- zero or sparse required-question coverage fails before freeze-chain validation;
- minimum question and revision coverage passes;
- v3.1-style extra manifest keys and gold genesis without `parent_manifest` can `SCORED`;
- gold freeze without an `ontology` role is `INVALID_SCORING_INPUT`;
- v2 manifest `version` is rejected;
- invalid coverage writes an immutable `INVALID_COVERAGE` envelope;
- unexpected exceptions write an immutable `SCORER_ERROR` envelope;
- existing reports cannot be overwritten.

Mutation validation:

- Baseline passed: yes
- Mutants killed: 3/3
- Mutation score: 100%
- `M1_REJECT_EXTRA_MANIFEST_KEYS`: killed by extra-key scoring tests
- `M2_ONTOLOGY_ROLE_OPTIONAL`: killed by missing-ontology `INVALID_SCORING_INPUT` test
- `M3_EXCEPTION_ENVELOPE_DISABLED`: killed by failure-envelope test
- Import or harness failures are explicitly rejected and cannot count as mutant kills.

Isolation:

- No v2, v3, or v3.1 holdout path is supplied to the v3.2 scorer.
- The scorer does not call v2 `main()` or v2 `validate_manifest`.
- Frozen v2/v3 scorers and the archived v3.1 `SCORER_ERROR` envelope are unchanged.
- Formal v3.2 scoring still requires a fresh unseen holdout whose gold freeze includes ontology and this scorer.
