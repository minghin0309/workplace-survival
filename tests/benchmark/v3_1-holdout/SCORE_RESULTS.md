# Benchmark v3.1 Formal Score Attempt

- Status: `SCORER_ERROR`
- Executed at: `2026-08-14T05:18:03.754174Z`
- Attempt id: `254be648659135915ebb99d76304dd42733bb84744a8ca724b60a12cf447358c`
- Formal scorer invocations: 1
- Rerun performed: no
- Report: `tests/benchmark/v3_1-holdout/cloud-cases/score-report-v31.json`
- Report SHA-256: `3ce1834894dd1007e4929ad4da0f44c5592264c49358f89473c4882101e4e8c2`
- Frozen scorer SHA-256: `9877d0e914960262c676616ba4eeff4d24bd831c7ca1228dcdf943dd4e252e61`
- Failure: `ValueError: manifest schema` at v2 `validate_benchmark.validate_manifest`

Coverage facts computed before the v2 core failed:

- turns: 24
- accepted turns: 23
- gold-uncertain turns: 1 (4.17%)
- required question concepts: 6 across 6 cases
- required revision concepts: 70 across 18 cases

`metrics` and `case_results` are null.

Cause:

- The frozen v3 scorer wraps the v2 core, which requires a v2 manifest object with exactly `{version, immutable, stage, parent_manifest, frozen_at_utc, artifacts}` and `version == "2"`.
- The frozen v3.1 evaluation, outputs, and gold manifests use `version: "3.1"` and additional freeze fields. The v2 schema check fails before any threshold metric is computed.
- Gold, ontology, evaluations, matches, and runtime Skill files were not modified.
- A second scorer invocation is forbidden in-version.

This is a harness/schema incompatibility between frozen v3.1 freeze documents and the frozen v2-shaped scorer core. It is not a Skill defect and not a match-decision defect.
