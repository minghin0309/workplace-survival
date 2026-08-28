# v3.3 Attempt-3 SUT Brief

Run Workplace Survival Skill on exactly one holdout case. You are the system under test.

## Allowlist

Read only:

- this brief;
- `.cursor/skills/workplace-survival/SKILL.md`
- `.cursor/skills/workplace-survival/REFERENCE.md`
- `.cursor/skills/workplace-survival/FORMATS.md`
- `.cursor/skills/workplace-survival/EXAMPLES.md`
- the single assigned file `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/sut-inputs/V333-NNN.json`
- that case's image, and only if `image_path` is present in that input file.

Do not glob. Do not read `cases.json`, gold, labels, question-design, oracle notes, other `sut-inputs`, other PNGs, tests, methodology, scorers, or prior holdouts.

## Job

Follow the Skill. `recipient_context` and `data_a` are Data A. Each turn's `input_raw` is the user turn, including any embedded draft. If `image_path` is set, the draft exists only in that PNG; `Read` the image.

Process turns in order. For turn n>1, keep your previous Skill outputs in context (correction/state). Do not invent facts. Do not guess geometrically occluded image tokens.

## Output

On dedicated branch `cursor/v333-NNN-sut-17a0` (replace NNN). Do not push `cursor/blind-v333-holdout-17a0`. Do not merge.

- `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/sut-raw/V333-NNN.json`
- `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/sut-attestations/V333-NNN.json`

```json
{
  "schema_version": "v3.3",
  "case_id": "V333-NNN",
  "turns": [
    {"turn_index": 1, "output_raw": "exact Skill output text"}
  ]
}
```

Attestation records files actually read with SHA-256, branch, commit, `gold_accessed: false`, `other_cases_accessed: false`, `question_design_accessed: false`, `skill_files_accessed: true`.

Commit raw first, then attestation. Push the dedicated branch. Open a draft PR with base `cursor/blind-v333-holdout-17a0`. Do not put cursor.com agent URLs in the PR body.
