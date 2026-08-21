# Benchmark Methodology v3.3 Construction Contract Validation Results

- Executed at: `2026-08-21T03:54:22Z`
- Branch: `cursor/benchmark-methodology-v33-17a0`
- Runtime Skill changes: none
- Attempt-3 gold/question-design: read as negative fixtures only; not rewritten

Unit validation:

- Tests: 10
- Passed: 10
- Failed: 0

Covered behavior:

- required `preserve-intended-recipient` is rejected; allowed-list presence is not;
- established-omission question candidates must be gold Red;
- `data_b_contains_unconfirmed_token` keeps Gray and is not forced Red;
- `image_only` candidates require `occluded_role`;
- occluded Data B tokens require gold Intake;
- occluded Data A tokens may remain Normal-mode;
- frozen attempt-3 gold fails the required-revision contract;
- frozen attempt-3 question-design fails the omission/occlusion contract.

Mutation validation:

- Baseline passed: yes
- Mutants killed: 3/3
- Mutation score: 100%
- `M1_PRESERVE_RECIPIENT_MAY_BE_REQUIRED`: killed by required-recipient tests
- `M2_ESTABLISHED_OMISSION_MAY_BE_GRAY`: killed by omission-Red test
- `M3_OCCLUDED_ROLE_OPTIONAL`: killed by missing `occluded_role` test
