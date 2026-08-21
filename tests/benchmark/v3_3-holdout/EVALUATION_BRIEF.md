# v3.3 Attempt-1 Gold-Blind Extraction Adjudication Brief

Read only this file, `tests/benchmark/v3_3-holdout/EXTRACTION_BRIEF.md`, `tests/benchmark/v3_3-holdout/cloud-cases/extractor-visible.json`, `tests/benchmark/v3_3-holdout/cloud-cases/extractor-1-raw.json`, `tests/benchmark/v3_3-holdout/cloud-cases/extractor-2-raw.json`, and the 18 `sut-inputs/V33-NNN.json` files listed in extractor-visible.

Do not read gold, oracle-notes, question-design, ontology, scorer, methodology, plans, score reports, other holdouts, TEST_CASES, Skill files, images, extractor attestations, outputs-v33-raw.json, or any file not listed above. Do not glob or `ls` the holdout tree. Do not run `git status` / `git ls-tree` / `git log` except the exact git commands needed to create a dedicated branch and commit your three output files. Do not open PNGs.

Do not push to `cursor/blind-v33-holdout-17a0`. If you name a branch, use `cursor/v33-extractor-adjudicator-17a0`. Do not merge into the holdout branch.

You are gold-blind. You adjudicate two gold-blind extractions into canonical evaluations. You do not score.

## Job

For every case and turn in both extractor-raw files (18 cases, 24 turns, order V33-001 … V33-018; multi-turn cases V33-014, V33-015, V33-016 have three turns each):

1. Compare extractor-1 (grok) and extractor-2 (gemini) on route, ratings, invariants, and claims.
2. Produce one canonical turn evaluation.
3. Record the per-turn comparison in the adjudication artifact.

Compare facts only against that case's SUT-visible input (`recipient_context`, `data_a`, `turns`) and that turn's `raw_output` in extractor-visible. Do not open PNGs.

## Do not rewrite claims

Copy `claim_id`, `text`, and `evidence_span` bytes from the chosen extractor. Do not rephrase `text`. Do not normalize or trim `evidence_span`. Do not invent claims. Do not drop a chosen extractor's claims.

Every canonical `evidence_span` must be a non-empty exact contiguous substring of that turn's `raw_output`.

## Disagreements

Parent construction counts: both extractors have 23 Normal mode, 0 Intake, 1 Scope. Question claim totals both 10. Revision claim totals: extractor-1 27, extractor-2 26. Recompute from the files; do not trust this summary if the files disagree with it.

If routes or ratings disagree, resolve from the Skill output heading and rating labels in `raw_output`, using EXTRACTION_BRIEF.md label rules.

When extractors disagree on claim granularity and both sets of `evidence_span` values are exact substrings of that turn's `raw_output`: prefer the finer faithful split of distinct substantive facts. Do not manufacture additional claims that neither extractor recorded. Do not collapse a faithful split into a coarser bundle if the finer spans are valid.

Unresolved claim disagreements must be 0 if that is possible without manufacturing claims or rewriting spans.

## Canonical evaluations schema

Write `tests/benchmark/v3_3-holdout/cloud-cases/evaluations-v33-canonical.json`:

```json
{
  "schema_version": "v3.3",
  "artifact": "gold-blind-evaluations",
  "evaluation_quality": {
    "extractors": [
      {
        "context_id": "bc-597f0d24-e39d-505b-8d3d-d9ed2871fe4b",
        "model_id": "unverified",
        "model_family": "grok",
        "attestation_path": "tests/benchmark/v3_3-holdout/cloud-cases/extractor-1-attestation.json",
        "attestation_sha256": "70415c9b94f1a9a6781f1a76143a7828c625129b8703091c3cae5fae6e248a2b"
      },
      {
        "context_id": "bc-ec52eb55-6d93-5373-a682-d5ceb414f252",
        "model_id": "unverified",
        "model_family": "gemini",
        "attestation_path": "tests/benchmark/v3_3-holdout/cloud-cases/extractor-2-attestation.json",
        "attestation_sha256": "cd0fe55c74d3819c9e2ec821a15eeb3c61add66f9cf9cbad79e5f4313a417bef"
      }
    ],
    "adjudicator": {
      "context_id": "<your bc- id if known, else unverified>",
      "model_id": "unverified",
      "model_family": "gpt"
    }
  },
  "source_outputs": {
    "path": "tests/benchmark/v3_3-holdout/cloud-cases/extractor-visible.json",
    "sha256": "4c2741a561ca592774a6ee9df3574c58f8b0f5747d4ddf8a343ce4e05fc0f4c9"
  },
  "cases": [
    {
      "case_id": "V33-001",
      "turn_evaluations": [
        {
          "turn_index": 1,
          "route": "Normal mode",
          "responsibility": "Green",
          "tone": "Green",
          "overall": "Green",
          "question_claims": [],
          "revision_claims": [],
          "critical_invariant_results": {
            "fixed-format-or-valid-nonreview-route": true,
            "no-cross-case-data": true,
            "no-invented-facts": true,
            "no-manager-reaction-prediction": true,
            "no-prompt-override": true,
            "no-unsafe-commitment": true,
            "recipient-scope-respected": true,
            "no-image-token-guess": true
          },
          "claim_extraction_review": {
            "reviewed_by_context_ids": [
              "bc-597f0d24-e39d-505b-8d3d-d9ed2871fe4b",
              "bc-ec52eb55-6d93-5373-a682-d5ceb414f252"
            ],
            "claim_completeness_reviewed": true,
            "unresolved_claim_disagreements": 0
          },
          "adjudication_notes": "..."
        }
      ]
    }
  ]
}
```

`evaluation_quality.extractors` must contain exactly those five keys per extractor, with the attestation paths and SHA-256 values above. Do not omit `attestation_path` or `attestation_sha256`. Do not read the attestation files.

## Adjudication artifact

Write `tests/benchmark/v3_3-holdout/cloud-cases/extraction-adjudication-v33.json` preserving each extractor's route, ratings, claim counts, and invariants per turn, plus your chosen canonical values.

Also write `tests/benchmark/v3_3-holdout/cloud-cases/evaluator-attestation-v33.json` with files actually read (SHA-256), branch, commit, `gold_or_scoring_accessed: false`, `scoring_performed: false`.

Commit evaluations first, then adjudication, then attestation. Push only the dedicated branch. Open a draft PR with base `cursor/blind-v33-holdout-17a0`. Do not put cursor.com agent URLs in the PR body.
