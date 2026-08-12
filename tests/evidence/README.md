# Test Evidence

This directory owns the auditable evidence format for Workplace Survival test executions.

## Evidence status

Test summaries recorded before T13.10 are historical, summary-only results. They remain useful regression history but are not retroactively described as evidence-complete.

From T13.10 onward, a `PASS` or `FAIL` added to a suite result file must cite a reviewable evidence record. `NOT_RUN` documents an unavailable execution and must never be counted as a pass.

## Record schema

Evidence files contain a JSON array. Every record requires:

- `schema_version`: currently `1`;
- `run_id`: unique stable identifier;
- `suite`: `functional`, `anti_hallucination`, `interaction_quality`, `auto_trigger`, or `explicit_invocation`;
- `case_id`: exact case identifier or deterministic check identifier;
- `executed_at_utc`: valid ISO-8601 UTC timestamp ending in `Z`;
- `model`:
  - `id`: exact backend slug when available, otherwise the configured selector such as `inherit`;
  - `display_name`;
  - `exact_backend_slug_available`: boolean;
  - `unavailable_reason`: required when the exact slug is unavailable;
- `method`:
  - `automated`;
  - `manual_semantic`;
  - `image_attached`;
  - `routing_semantic`;
  - `environment_limited`;
- `input_source`:
  - `reference`: case-file path and optional heading;
  - `snapshot_raw`: exact case/source excerpt used for execution;
  - `snapshot_sha256`: SHA-256 of that snapshot;
- `turns`: ordered execution turns, each containing:
  - `index`;
  - `executed_at_utc`;
  - `input_raw`;
  - `input_sha256`;
  - `raw_output`;
  - `output_sha256`;
- `artifacts`: each used artifact contains:
  - `path`;
  - `sha256`;
  - `usage`;
  - `opened_with_image_reader`;
- `assertions`: each checked requirement contains:
  - `id`;
  - `text`;
  - `assessment`: `automatic` or `manual`;
  - `passed`: boolean for executed records, `null` for `NOT_RUN`;
- `result`: `PASS`, `FAIL`, or `NOT_RUN`;
- `limitations`: explicit method and environment limitations;
- `result_citations`: suite-result files that cite this record's `run_id`.

Repeat-run records additionally require:

- `consistency`:
  - `group`;
  - `repeat_index`;
  - `evaluator_context_id`;
- `observations`:
  - `route`;
  - `responsibility`;
  - `tone`;
  - `overall`;
  - `question_count`;
  - `revision_facts`: sorted factual effects, preserved values, and unresolved placeholders.

Hashes make later evidence mutation detectable. Source files may evolve after a run, so validation checks the preserved snapshot rather than requiring the current file hash to remain unchanged. Reviewers must compare `turns[].input_raw` with `input_source.snapshot_raw`.

## Method rules

- `automated`: a command or deterministic assertion produced the result.
- `manual_semantic`: an evaluator applied semantic assertions to text input.
- `image_attached`: every claimed image has `opened_with_image_reader: true`, plus a matching artifact hash.
- `routing_semantic`: frontmatter and prompts were evaluated deterministically; this is not a live probabilistic dispatcher run.
- `environment_limited`: the requested configuration or environment was unavailable. Its result must be `NOT_RUN`, every assertion outcome must be `null`, and the limitation must explain why.

`NOT_RUN` is allowed only with `environment_limited`. An executed method may report only `PASS` or `FAIL`.

## PASS gate

A record may say `PASS` only when:

- exact ordered raw inputs and outputs are present;
- hashes match all raw content, source snapshots, and artifacts;
- every assertion has a unique ID and passed;
- the method is identified;
- image artifacts were actually opened when image execution is claimed;
- limitations are disclosed;
- every listed suite-result file cites the evidence file and `run_id`.

The T13.10 validation set must cover every active suite and all five method classes. It validates the evidence mechanism with representative records; it does not make historical suite summaries evidence-complete. The full evidence-complete rerun remains T13.12 work.

T13.11 repeat evidence may cover a subset of suites and methods. Every consistency record must cite a plan containing expected canonical observations, and each repeat of a case must use a distinct evaluator context. Records are compared with `compare_consistency.py`; different raw prose is allowed, but any difference from planned canonical observations fails.

Validate evidence with:

```bash
python3 tests/evidence/validate_evidence.py tests/evidence/t13-10-validation.json
```
