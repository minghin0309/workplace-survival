# Blind Benchmark Methodology v3.2

Version 3.2 changes freeze-chain scoring only. It must not modify `.cursor/skills/workplace-survival/`, reinterpret v2, or rescore the archived v3.1 holdout.

## Why v3.2 exists

v3 wraps the v2 scorer `main()`, which requires a v2 manifest object with exactly:

- keys `{version, immutable, stage, parent_manifest, frozen_at_utc, artifacts}`
- `version == "2"`

v3.1 freeze documents use `version: "3.1"` and additional fields. The single v3 scorer invocation against the v3.1 holdout therefore recorded `SCORER_ERROR` (`manifest schema`) before metrics. That envelope is immutable. v3.2 does not repair it.

## Freeze-chain contract

The v3.2 scorer validates evaluation → outputs → gold manifests itself. It never calls v2 `validate_manifest`.

Required keys on every stage:

- `version`
- `immutable`
- `stage`
- `frozen_at_utc`
- `artifacts`

Additional keys are allowed (for example `sut_execution_authorized`, `shared_delivery`, `parent_extraction_snapshot`, `canonical_parent_commit`).

`version` must be `3.1` or `3.2`. v2 manifests are rejected.

`parent_manifest` with `{path, sha256}` is required for `evaluations` and `outputs`. Gold may omit it (genesis). Extra parent fields are allowed.

Each artifact entry must include `role`, `path`, `sha256`, `cloud_branch`, and `cloud_commit`. Additional artifact fields are allowed.

Required roles:

- gold: `gold`, `ontology`, `scorer`
- outputs: `outputs`
- evaluations: `evaluations`, `matches`

The CLI ontology and scorer paths must match the frozen gold artifacts. A gold freeze without `ontology` is `INVALID_SCORING_INPUT`, not a Skill failure.

## Metric policy

Unchanged from v3:

- zero denominators are `NOT_APPLICABLE`, never 0, 1, a threshold pass, or an exception;
- coverage gates run before semantic scoring;
- every required threshold must be `EVALUATED` or the status is `INVALID_SCORING_INPUT`;
- thresholds remain the v3 preregistered set.

Semantic claim matching still uses the frozen v2 validators (`validate_claims`, `validate_match_set`, ontology aliases). v3.2 does not call v2 `main()`.

## Failure envelopes

Unchanged statuses: `SCORED`, `INVALID_COVERAGE`, `INVALID_SCORING_INPUT`, `SCORER_ERROR`.

Freeze-chain failures are `INVALID_SCORING_INPUT`. Unexpected exceptions remain `SCORER_ERROR`. Reports are written once and never overwritten.

## Version isolation

- v3.2 validation uses synthetic fixtures only.
- v2, v3, and v3.1 holdout artifacts must not be supplied to the v3.2 scorer.
- A successful v3.2 implementation does not repair or replace archived v2 or v3.1 outcomes.
- Formal v3.2 scoring requires a fresh unseen holdout whose gold freeze includes ontology and this scorer.
