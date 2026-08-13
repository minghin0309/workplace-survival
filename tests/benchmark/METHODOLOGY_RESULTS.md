# Blind Benchmark Methodology v2 Results

## Outcome

Status: `IMPLEMENTED — NOT YET USED FOR A NEW HOLDOUT`

## Changes

- Replaced exact question/revision token equality with concept and semantic-claim matching.
- Added a versioned ontology with deterministic aliases for common concepts.
- Separated SUT-visible `data_a` from evaluator-only construction notes.
- Added gold quality tiers, heterogeneous-family requirements, adjudication metadata, uncertainty caps, and a human-review template.
- Added two-family claim-extraction review before semantic matching.
- Added content-addressed cloud artifact manifests with non-overwrite behavior, required roles, and `gold → outputs → evaluations` parent chaining.
- Bound scoring inputs to the validated evaluation-stage manifest and its exact parent artifacts.
- Added unsupported-claim, weak-match, hidden-note, artifact-mutation, and gold-uncertainty rejection gates.
- Kept all runtime Skill files unchanged.

## Automated tests

```text
Ran 14 tests
OK
```

Covered:

- ontology alias matches;
- unsupported claim accounting;
- weak semantic match rejection;
- omitted claim-match rejection;
- `case_designer_notes` rejection;
- changed cloud artifact rejection;
- valid parent-chained cloud manifest acceptance;
- generator oracle-note access rejection;
- missing cloud artifact role rejection;
- invalid attestation-content rejection;
- attestation/model-family mismatch rejection;
- missing per-turn image artifact rejection.
- excessive gold uncertainty rejection;
- invalid human-review tier rejection.

## Isolation

```text
git diff main -- .cursor/skills/workplace-survival SPEC.md
```

Result: no runtime or product-specification changes.

## Limitations

- No new hidden holdout has been generated with methodology v2.
- Novel semantic matches still require a post-unblinding matcher or human decision.
- Human review is supported but was not available in this environment.
- Heterogeneous model adjudication reduces but does not remove correlated bias.
- Historical cloud blind scores remain unchanged and must not be rescored as headline results.
