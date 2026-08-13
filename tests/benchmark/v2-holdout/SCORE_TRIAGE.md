# Benchmark v2 Formal Score Triage

## Outcome

The single formal scoring attempt ended with `SCORER_ERROR` before the frozen scorer wrote metrics or case-level results.

Confirmed cause:

- Gold contains zero required question concepts across 24 turns.
- `score_semantic.py` calls `ratio(0, 0)` for `required_question_concept_recall`.
- Its frozen `ratio` helper rejects every zero denominator with `ValueError: metric denominator must be nonzero`.

The score is therefore unavailable, not a benchmark pass or failure.

## Preregistered thresholds

- Gold uncertainty: pre-score gate passed at 1/24, or 4.17%, against the 20% maximum.
- Required question-concept recall: undefined because the denominator is zero.
- Route, responsibility, tone, overall, claim precision, revision recall, and critical-invariant thresholds: not formally evaluated because no score report was emitted.

No threshold is inferred from partial in-memory scorer work.

## Classification

### Confirmed harness defects

1. `H-001 — Zero-denominator policy missing`
   - The scorer treats an inapplicable recall metric as a fatal error rather than `null`/`N/A` or another preregistered convention.
   - This is the direct cause of the failed formal attempt.

2. `H-002 — Failure evidence is not emitted by the scorer`
   - The scorer writes its report only after every metric is constructed.
   - An exception discards case-level mismatch and partial metric evidence instead of writing an immutable failure envelope.

### Confirmed Skill defects

None can be confirmed from this run because formal case results were not emitted. Raw outputs and evaluations remain frozen for future methodology work, but they are not promoted to product defects.

### Gold ambiguity or coverage

- V2-013 turn 1 remains explicitly `gold_uncertain`; this was already represented before scoring and is not a new defect.
- Zero required question concepts is a benchmark coverage limitation. It is not by itself evidence that any individual gold label is wrong.
- No frozen gold label was changed after unblinding.

### Ontology or matcher findings

Seven frozen revision claims are marked unsupported:

- V2-002 turn 1: `r-V2-002-1-2`
- V2-005 turn 1: `r-V2-005-1-5`
- V2-006 turn 1: `r-V2-006-1-4`
- V2-011 turn 1: `r-V2-011-1-1`
- V2-011 turn 2: `r-V2-011-2-1`
- V2-011 turn 3: `r-V2-011-3-1`
- V2-014 turn 1: `r-V2-014-1-4`

These are preserved triage candidates, not automatically matcher or ontology defects. Each may be a genuinely unsupported output claim, an allowed-gold coverage gap, or a semantic-matching error. Formal claim-precision consequences were not reported because scoring aborted.

## Failed and unscored cases

- Formal failed cases: unavailable; the scorer emitted no `case_results`.
- Unscored cases: V2-001 through V2-018.
- No case is relabelled as passed or failed outside the frozen scorer.

## Limitations and next methodology action

- The scorer was executed once and was not rerun.
- Frozen gold, outputs, evaluations, matches, ontology, scorer, and manifests remain unchanged.
- Fixing zero-denominator handling is a scoring-method change. Under the methodology contract it requires a new benchmark version and a fresh holdout; this v2 attempt must remain recorded as `SCORER_ERROR`.
- Runtime Skill remediation must not start from this failed scoring attempt.
