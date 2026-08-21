# Blind Benchmark Methodology v3.3

Version 3.3 changes revision scoring and construction/gold-label contracts only. It must not modify `.cursor/skills/workplace-survival/`, reinterpret v3.2, or rescore archived v3.2 attempt 1–3, v3.1, or v2 holdouts.

## Why v3.3 exists

v3.2 attempt-3 scored `SCORED` with thresholds not passed. Triage (`tests/benchmark/v3_2-holdout/attempt-3/SCORE_TRIAGE.md`) showed:

- required question recall 6/6 after T14.15;
- required revision recall 9/41 driven by H-001 (`no-revision` vs empty claims on 12 Green-control turns) and H-003 (`preserve-intended-recipient` required but never claimed when the addressee stayed);
- responsibility 16/23 driven by gold Gray on established omissions (G-001) and Normal-mode gold on an occluded Data B token (G-003).

Those are scoring-contract and construction/gold-label defects. They are not Skill patches. v3.2 envelopes stay immutable.

## Scoring contract

v3.3 inherits the v3.2 freeze-chain scorer (`evaluation` → `outputs` → `gold`, ontology and scorer roles required, v2 `main()` never called).

Added revision rules:

- **H-001.** If gold requires `no-revision`, both gold ratings are Green, both SUT ratings are Green, and `revision_claims` is empty, credit `no-revision` as hit. Over-revision (any revision claim) does not get this credit.
- **H-003.** `preserve-intended-recipient` is never a scored required revision. Coverage counts and recall denominators exclude it. It may remain in `allowed_revision_concepts`. Keeping the addressee is implicit in a revision body.

Thresholds, zero-denominator `NOT_APPLICABLE`, coverage minima, and immutable reports are unchanged from v3.2.

Accepted freeze `version` values: `3.1`, `3.2`, `3.3`.

## Construction and gold-label contract

Still required: v3.1 question-candidate contract and v3.2 manager-recipient contract.

Added:

- gold `required_revision_concepts` must not include `preserve-intended-recipient`;
- an established omission question candidate (writer holds the answer, token absent from SUT-visible fields, Data B does not contain an unconfirmed invented token, message cannot be completed without the answer) must be gold responsibility **Red**, not Gray;
- `image_only` candidates must set `occluded_role` to `data_a`, `data_b`, or `none`;
  - `data_b`: gold route is `Intake` (Skill OCR: illegible Data B body is not reviewable);
  - `data_a`: Normal-mode Gray question is allowed;
- `data_b_contains_unconfirmed_token: true` keeps T14.15 Gray (do not force Red).

Do not Skill-patch toward gold Gray on established omissions, or toward Normal-mode review of an illegible Data B token.

## Version isolation

- v3.3 validation uses synthetic fixtures plus frozen attempt-3 gold/question-design as **negative** contract fixtures. It does not invoke `score_semantic_v3_2.py` or write a new attempt-3 report.
- Formal v3.3 scoring requires a fresh unseen holdout whose gold freeze includes ontology and `score_semantic_v3_3.py`.
- Denylist for that holdout: millinery, harpworks, Thornwick aerostat, Greaveholt cold-cathode, and any prior holdout domain.
