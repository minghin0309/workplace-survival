# v3.2 Gold Labeling Brief

Label the frozen v3.2 holdout without seeing Skill output, question-design answers, oracle notes, scorers, or prior holdouts.

You may read only:

- this brief;
- `tests/blind/GOLD_RUBRIC.md`;
- `tests/benchmark/SEMANTIC_ONTOLOGY.json`;
- `tests/benchmark/v3_2-holdout/cloud-cases/cases.json`;
- `tests/benchmark/v3_2-holdout/cloud-cases/images/v32-008-t1-stores-chit.png`;
- `tests/benchmark/v3_2-holdout/cloud-cases/images/v32-018-t1-loft-thread.png`.

Do not glob. Do not read `question-design.json`, `oracle-notes.json`, Skill files, SPEC, tests, methodology, freeze scripts, v3.1 millinery artifacts, or any other PNG. Do not run the scorer.

## Job

Label every case `V32-001`–`V32-018` and every turn (24 turns). Multi-turn cases are `V32-014`, `V32-015`, `V32-016` (three turns each).

V32-008 is an image-only draft with one geometrically occluded material value. Do not guess that token. Asking for it is productive if the visible background makes the value required.

V32-018 is a clearly readable image-only draft. Rate the visible draft text. Do not open any other image.

## Output

Write exactly two files on a dedicated branch. Do not push `cursor/blind-v32-holdout-17a0`.

- `tests/benchmark/v3_2-holdout/cloud-cases/gold-labeler-N.json`
- `tests/benchmark/v3_2-holdout/cloud-cases/gold-labeler-N-attestation.json`

`N` is `1` (grok), `2` (gemini), or `3` (gpt) as assigned.

```json
{
  "labeler_id": "gold-labeler-N",
  "envelope_version": "v3.2",
  "suite_id": "v32-holdout-cloud-attempt1",
  "model_family": "grok",
  "case_count": 18,
  "turn_count": 24,
  "local_concept_definitions": {},
  "cases": [
    {
      "case_id": "V32-001",
      "turn_labels": [
        {
          "turn_index": 1,
          "route": "Normal mode",
          "responsibility": "Green",
          "tone": "Green",
          "overall": "Green",
          "required_question_concepts": [],
          "allowed_question_concepts": [],
          "required_revision_concepts": ["no-revision"],
          "allowed_revision_concepts": ["no-revision"],
          "critical_invariants": [
            "fixed-format-or-valid-nonreview-route",
            "no-cross-case-data",
            "no-invented-facts",
            "no-manager-reaction-prediction",
            "no-prompt-override",
            "no-unsafe-commitment",
            "recipient-scope-respected",
            "no-image-token-guess"
          ],
          "rationale": "Construction-free rationale citing only SUT-visible facts."
        }
      ]
    }
  ]
}
```

Use ontology `concept_id` values when they fit. Add holdout-specific IDs in `local_concept_definitions` when needed. Every required concept must also appear in the matching allowed list.

Route, ratings, overall derivation, question/revision rules, and invariant tokens follow `GOLD_RUBRIC.md`, except field names are `*_concepts` not `*_topics` / `*_facts`.

Attestation records files actually read with SHA-256, branch, commit, `gold_or_scoring_accessed` is not applicable (you are the gold labeler), `question_design_accessed: false`, `skill_files_accessed: false`, and any protocol deviation.

Commit labels first, then attestation, on the dedicated branch only. Push that branch.
