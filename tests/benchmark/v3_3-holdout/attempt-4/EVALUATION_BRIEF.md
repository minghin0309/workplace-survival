# v3.3 Attempt-4 Gold-Blind Extraction Adjudication Brief

Read only this file, `tests/benchmark/v3_3-holdout/attempt-4/EXTRACTION_BRIEF.md`, `tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/extractor-visible.json`, `tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/extractor-1-raw.json`, `tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/extractor-2-raw.json`, and the 18 `sut-inputs/V334-NNN.json` files listed in extractor-visible.

Do not read gold, oracle-notes, question-design, ontology, scorer, methodology, plans, score reports, other holdouts, TEST_CASES, Skill files, images, extractor attestations, outputs-v334-raw.json, or any file not listed above. Do not glob or `ls` the holdout tree. Do not run `git status` / `git ls-tree` / `git log` except the exact git commands needed to create a dedicated branch and commit your three output files. Do not open PNGs.

Do not push to `cursor/blind-v334-holdout-17a0`. If you name a branch, use `cursor/v334-extractor-adjudicator-17a0`. Do not merge into the holdout branch.

You are gold-blind. You adjudicate two gold-blind extractions into canonical evaluations. You do not score.

## Job

For every case and turn in both extractor-raw files (18 cases, 24 turns, order V334-001 … V334-018; multi-turn cases V334-014, V334-015, V334-016 have three turns each):

1. Compare extractor-1 (grok) and extractor-2 (gemini) on route, ratings, invariants, and claims.
2. Produce one canonical turn evaluation.
3. Record the per-turn comparison in the adjudication artifact.

Compare facts only against that case's SUT-visible input (`recipient_context`, `data_a`, `turns`) and that turn's `raw_output` in extractor-visible. Do not open PNGs.

## Do not rewrite claims

Copy `claim_id`, `text`, and `evidence_span` bytes from the chosen extractor. Do not rephrase `text`. Do not normalize or trim `evidence_span`. Do not invent claims. Do not drop a chosen extractor's claims.

Every canonical `evidence_span` must be a non-empty exact contiguous substring of that turn's `raw_output`.

## Disagreements

Parent construction counts are unknown until extraction exists. Recompute route and claim totals from the two extractor-raw files. Do not copy prior-attempt counts.

If routes or ratings disagree, resolve from the Skill output heading and rating labels in `raw_output`, using EXTRACTION_BRIEF.md label rules.

When extractors disagree on claim granularity and both sets of `evidence_span` values are exact substrings of that turn's `raw_output`: prefer the finer faithful split of distinct substantive facts. Do not manufacture additional claims that neither extractor recorded. Do not collapse a faithful split into a coarser bundle if the finer spans are valid.

Unresolved claim disagreements must be 0 if that is possible without manufacturing claims or rewriting spans.

## Canonical evaluations schema

Write `tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/evaluations-v334-canonical.json`:

```json
{
  "schema_version": "v3.3",
  "artifact": "gold-blind-evaluations",
  "evaluation_quality": {
    "extractors": [
      {
        "context_id": "<extractor-1 bc- id>",
        "model_id": "unverified",
        "model_family": "grok",
        "attestation_path": "tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/extractor-1-attestation.json",
        "attestation_sha256": "<sha256 of extractor-1-attestation.json>"
      },
      {
        "context_id": "<extractor-2 bc- id>",
        "model_id": "unverified",
        "model_family": "gemini",
        "attestation_path": "tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/extractor-2-attestation.json",
        "attestation_sha256": "<sha256 of extractor-2-attestation.json>"
      }
    ],
    "adjudicator": {
      "context_id": "<your bc- id if known, else unverified>",
      "model_id": "unverified",
      "model_family": "gpt"
    }
  },
  "source_outputs": {
    "path": "tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/extractor-visible.json",
    "sha256": "<sha256 of extractor-visible.json>"
  },
  "cases": [
    {
      "case_id": "V334-001",
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
              "<extractor-1 bc- id>",
              "<extractor-2 bc- id>"
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

`evaluation_quality.extractors` must contain exactly those five keys per extractor. Fill `context_id` and `attestation_sha256` from the extractor-raw envelopes and by hashing the attestation files on disk after they exist; do not copy prior-attempt ids or hashes. Do not omit `attestation_path` or `attestation_sha256`. Do not read the attestation files.

## Adjudication artifact

Write `tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/extraction-adjudication-v334.json` preserving each extractor's route, ratings, claim counts, and invariants per turn, plus your chosen canonical values.

Also write `tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/evaluator-attestation-v334.json` with files actually read (SHA-256), branch, commit, `gold_or_scoring_accessed: false`, `scoring_performed: false`.

Commit evaluations first, then adjudication, then attestation. Push only the dedicated branch. Open a draft PR with base `cursor/blind-v334-holdout-17a0`. Do not put cursor.com agent URLs in the PR body.
