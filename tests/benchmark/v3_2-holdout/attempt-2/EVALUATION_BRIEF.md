# v3.2 Attempt-2 Gold-Blind Extraction Adjudication Brief

Read only this file, `tests/benchmark/v3_2-holdout/attempt-2/EXTRACTION_BRIEF.md`, `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractor-visible.json`, `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractor-1-raw.json`, `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractor-2-raw.json`, and the 18 `sut-inputs/V322-NNN.json` files listed in extractor-visible.

Do not read gold, oracle-notes, adjudication (except the files you write), question-design, ontology, scorer, methodology, plans, score reports, other holdouts, TEST_CASES, Skill files, images, extractor attestations, outputs-v322-raw.json, or any file not listed above. Do not glob or `ls` the holdout tree. Do not run `git status` / `git ls-tree` / `git log` except the exact git commands needed to create a dedicated branch and commit your three output files. Do not open PNGs.

Do not push to `cursor/blind-v322-holdout-17a0`. If you name a branch, use `cursor/v322-extractor-adjudicator-17a0`. Do not merge into the holdout branch.

You are gold-blind. You adjudicate two gold-blind extractions into canonical evaluations. You do not score.

## Job

For every case and turn in both extractor-raw files (18 cases, 24 turns, order V322-001 … V322-018; multi-turn cases V322-014, V322-015, V322-016 have three turns each):

1. Compare extractor-1 (grok) and extractor-2 (gemini) on route, ratings, invariants, and claims.
2. Produce one canonical turn evaluation.
3. Record the per-turn comparison in the adjudication artifact.

Compare facts only against that case's SUT-visible input (`recipient_context`, `data_a`, `turns`) and that turn's `raw_output` in extractor-visible. Do not open PNGs.

## Do not rewrite claims

Copy `claim_id`, `text`, and `evidence_span` bytes from the chosen extractor. Do not rephrase `text`. Do not normalize or trim `evidence_span`. Do not invent claims. Do not drop a chosen extractor's claims.

Every canonical `evidence_span` must be a non-empty exact contiguous substring of that turn's `raw_output`.

## Disagreements

Routes and ratings already agree across extractors (22 Normal mode, 1 Intake, 1 Scope). If you find a disagreement anyway, resolve it from the Skill output heading and rating labels in `raw_output`, using EXTRACTION_BRIEF.md label rules.

Revision claim counts differ (extractor-1: 24 total; extractor-2: 9 total). Question claim counts agree (7). The count disagreements are on V322-002, V322-009, V322-010, V322-011, V322-012, V322-016 turn 1, and V322-018.

When extractors disagree on claim granularity and both sets of `evidence_span` values are exact substrings of that turn's `raw_output`: prefer the finer faithful split of distinct substantive facts. Do not manufacture additional claims that neither extractor recorded. Do not collapse a faithful split into a coarser bundle if the finer spans are valid.

Unresolved claim disagreements must be 0 if that is possible without manufacturing claims or rewriting spans.

## Canonical evaluations schema

Write `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/evaluations-v322-canonical.json`:

```json
{
  "schema_version": "v3.2",
  "artifact": "gold-blind-evaluations",
  "evaluation_quality": {
    "extractors": [
      {
        "context_id": "bc-67e42ce2-6f4b-52df-af72-2ab315f76639",
        "model_id": "unverified",
        "model_family": "grok",
        "attestation_path": "tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractor-1-attestation.json",
        "attestation_sha256": "655f98fe0f256701401dfe79d78859cce246fbe19fbfef0d83bc5a24b231e569"
      },
      {
        "context_id": "bc-8c33fcfe-893c-57f6-b785-2a00056f1ad6",
        "model_id": "unverified",
        "model_family": "gemini",
        "attestation_path": "tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractor-2-attestation.json",
        "attestation_sha256": "d12759fdf8b3c4dc7ea3a38ba6245f2af737988cf79f5a74c0a06b3f8157b509"
      }
    ],
    "adjudicator": {
      "context_id": "<your bc- id if known, else unverified>",
      "model_id": "unverified",
      "model_family": "gpt"
    }
  },
  "source_outputs": {
    "path": "tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractor-visible.json",
    "sha256": "97d1a3e6cbd3cfd8b6d80bf4a0df4f0131846e559a950665055a94c9d86d2a1f"
  },
  "cases": [
    {
      "case_id": "V322-001",
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
              "bc-67e42ce2-6f4b-52df-af72-2ab315f76639",
              "bc-8c33fcfe-893c-57f6-b785-2a00056f1ad6"
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

`evaluation_quality.extractors` must contain exactly those five keys per extractor, with the attestation paths and SHA-256 values above (holdout copies). Do not omit `attestation_path` or `attestation_sha256`.

`route` vocabulary and rating vocabulary are defined in EXTRACTION_BRIEF.md. All eight invariant keys are required; values must be booleans.

`claim_extraction_review.reviewed_by_context_ids` must list both extractor context ids. `unresolved_claim_disagreements` must be 0 on every turn if possible without manufacturing.

## Adjudication artifact schema

Write `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extraction-adjudication-v322.json`:

```json
{
  "schema_version": "v3.2",
  "artifact": "gold-blind-extraction-adjudication",
  "source_extractors": [
    {
      "extractor": 1,
      "context_id": "bc-67e42ce2-6f4b-52df-af72-2ab315f76639",
      "model_family": "grok",
      "source_path": "tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractor-1-raw.json",
      "sha256": "980fb48b53ca2e6ed41c1273b6f27f06bdd142c2cd04d21fa2ba31bc33bde677"
    },
    {
      "extractor": 2,
      "context_id": "bc-8c33fcfe-893c-57f6-b785-2a00056f1ad6",
      "model_family": "gemini",
      "source_path": "tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractor-2-raw.json",
      "sha256": "e76c023d11fba1936132c9a56a67d07804d98be8a43df44c7d21678f25f7e9a5"
    }
  ],
  "adjudicator": {
    "context_id": "<your bc- id if known, else unverified>",
    "model_id": "unverified",
    "model_family": "gpt"
  },
  "source_outputs": {
    "path": "tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/extractor-visible.json",
    "sha256": "97d1a3e6cbd3cfd8b6d80bf4a0df4f0131846e559a950665055a94c9d86d2a1f"
  },
  "cases": [
    {
      "case_id": "V322-001",
      "turn_adjudications": [
        {
          "turn_index": 1,
          "extractor_1": {
            "route": "Normal mode",
            "ratings": {"responsibility": "Green", "tone": "Green", "overall": "Green"},
            "claim_counts": {"question_claims": 0, "revision_claims": 0},
            "critical_invariant_results": {}
          },
          "extractor_2": {
            "route": "Normal mode",
            "ratings": {"responsibility": "Green", "tone": "Green", "overall": "Green"},
            "claim_counts": {"question_claims": 0, "revision_claims": 0},
            "critical_invariant_results": {}
          },
          "resolution": {
            "route": "Normal mode",
            "ratings": {"responsibility": "Green", "tone": "Green", "overall": "Green"},
            "claim_counts": {"question_claims": 0, "revision_claims": 0},
            "claims_taken_from": "extractor-1",
            "critical_invariant_results": {},
            "unresolved_claim_disagreements": 0
          },
          "notes": "..."
        }
      ]
    }
  ]
}
```

`claims_taken_from` is `extractor-1`, `extractor-2`, or `both` when the chosen claim lists are identical. Copy the eight invariant keys on each extractor block and on `resolution`.

## Attestation

Write `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/evaluator-attestation-v322.json`.

Record files actually read with SHA-256, branch, output commits, `gold_or_scoring_accessed: false`, `scoring_performed: false`, coverage counts, limitations, and any protocol deviation. `model_family` is `gpt`. Do not embed this attestation's own digest.

Commit order on the dedicated branch only: evaluations JSON, then adjudication JSON, then attestation. Push that branch only. Do not create or merge a pull request into the holdout branch.
