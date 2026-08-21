# Benchmark Methodology v3.3 Validation Results

- Executed at: `2026-08-21T03:54:22Z`
- Branch: `cursor/benchmark-methodology-v33-17a0`
- Base: `cursor/v323-attempt3-triage-17a0`
- Runtime Skill changes: none
- v3.2 scorer changes: none
- v3.2 attempt-3 holdout artifact changes: none
- v3.2 scorer invocations during v3.3 validation: 0

Unit validation:

- Tests: 20 scorer + 10 construction/gold-label
- Passed: 30
- Failed: 0
- Fixtures: synthetic, plus frozen attempt-3 gold/question-design as negative contract fixtures

Covered behavior:

- zero denominators return `value: null` and `status: NOT_APPLICABLE`;
- zero or sparse required-question coverage fails before freeze-chain validation;
- v3.1-style extra manifest keys and gold genesis without `parent_manifest` can `SCORED`;
- gold freeze without an `ontology` role is `INVALID_SCORING_INPUT`;
- v2 manifest `version` is rejected;
- invalid coverage writes an immutable `INVALID_COVERAGE` envelope;
- unexpected exceptions write an immutable `SCORER_ERROR` envelope;
- existing reports cannot be overwritten;
- empty Green revision claims credit required `no-revision`;
- empty claims do not credit `no-revision` when SUT ratings are not Green;
- nonempty unmatched revision claims do not use empty-credit;
- `preserve-intended-recipient` is excluded from scored required revisions and coverage counts;
- v3.2 scorer bytes and the attempt-3 score report remain the archived hashes;
- v3.3 scoring does not call v2 `main()`.

Scorer mutation validation:

- Baseline passed: yes
- Mutants killed: 3/3
- Mutation score: 100%
- `M1_EMPTY_NO_REVISION_CREDIT_DISABLED`: killed by empty-Green `no-revision` credit test
- `M2_PRESERVE_RECIPIENT_STILL_REQUIRED`: killed by H-003 exclusion test
- `M3_EXCEPTION_ENVELOPE_DISABLED`: killed by failure-envelope test
- Import or harness failures are explicitly rejected and cannot count as mutant kills.

Isolation:

- No v2, v3, v3.1, or v3.2 holdout path is supplied to the v3.3 scorer as a scoring input.
- Frozen attempt-3 gold is used only as a negative construction-contract fixture.
- Formal v3.3 scoring still requires a fresh unseen holdout whose gold freeze includes ontology and this scorer.
