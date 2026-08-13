# Blind Benchmark Methodology v2

## Separation from product behavior

This methodology changes benchmark construction and scoring only. It must not change `.cursor/skills/workplace-survival/`.

Historical blind scores remain unchanged.

## Input contract

Every case contains only SUT-visible fields:

- `case_id`;
- `category`;
- `recipient_context`: explicit recipient/audience scope;
- `data_a`: exact factual background available to the Skill;
- `turns`: ordered user inputs and optional image paths;
- `image_spec`.

`case_designer_notes` is forbidden.

Optional construction notes live in a separate `oracle-notes.json` file containing only:

- `case_id`;
- `design_intent`;
- `difficulty_notes`.

Gold labelers and SUT output generators must not read oracle notes. Any fact required for a rating, question, or revision must appear in `data_a`, a user turn, or a visible image.

## Semantic concepts

Gold question and revision requirements use concept objects:

- `concept_id`;
- `description`;
- ontology aliases where applicable.

Gold-blind output evaluation extracts actual claims with:

- `claim_id`;
- `text`;
- exact `evidence_span` copied from raw Skill output.

After unblinding, a semantic matcher maps claims to allowed gold concepts. Exact concept IDs and registered aliases are deterministic matches. Novel phrases require an explicit matcher decision with rationale and confidence.

One claim may satisfy at most one concept in each domain. Unmatched output claims are unsupported.

## Gold quality

Minimum gold:

- three labelers from distinct model families;
- a fourth-family adjudicator;
- model/context attestations and file hashes;
- all categorical and list-field disagreements recorded;
- vote distributions preserved.

Gold quality tiers:

- `human_reviewed`: a human reviewed every disagreement;
- `heterogeneous_adjudicated`: fourth-family model adjudication with no human;
- `gold_uncertain`: any three-way categorical disagreement, critical-invariant disagreement, or unresolved adjudication.

`gold_uncertain` turns are reported separately from primary accuracy. A benchmark is invalid when more than 20% of turns are `gold_uncertain`.

Human review is optional only when heterogeneous adjudication is available. Absence of human review must be reported.

## Scoring

Primary metrics use `accepted` turns only:

- route and rating accuracy;
- required question-concept recall;
- question-claim support precision;
- required revision-concept recall;
- revision-claim support precision;
- critical invariant violations.

Report uncertain-turn metrics separately.

Semantic synonym matching can fix ontology false negatives but cannot:

- change route or rating gold;
- remove raw output claims;
- mark an unsupported claim as allowed without a recorded concept match;
- alter the original frozen benchmark score.

## Artifact immutability

Freeze before SUT execution:

- cases;
- images;
- gold labels;
- adjudication;
- ontology;
- scorer and validators;
- runtime commit and runtime blobs.

Freeze raw outputs before semantic extraction. Every later artifact references the parent manifest SHA-256. Files use content hashes and non-overwrite semantics.

Cloud attestations record branch, commit, model, context ID, files read, and limitations. Attestations are evidence, not proof of filesystem non-access.

## Failure handling

- Preserve raw cases, outputs, gold, matches, and reports.
- Do not modify gold or ontology after unblinding.
- Scoring-method fixes require a new benchmark version and new holdout.
- Product defects require a separate remediation branch.
