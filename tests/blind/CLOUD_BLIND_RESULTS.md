# Cloud-Isolated Blind Holdout Results

## Outcome

Status: `FAIL`

The preregistered score is preserved exactly. Gold, raw Skill outputs, semantic evaluations, thresholds, and scorer were not changed after unblinding.

## Holdout

- Cases: 30.
- Turns: 36.
- Image cases: 4.
- Case designer: isolated Cursor Cloud branch with only the case brief permitted.
- Gold: three cloud labelers from Claude, Grok, and Kimi model families.
- Adjudicator: separate GPT model family.
- Skill execution: 30 distinct cloud contexts from a branch containing cases and runtime but no gold.
- Semantic output evaluator: cloud Claude context with outputs but no gold.

## Preregistered metrics

| Metric | Result | Threshold | Pass |
|---|---:|---:|---|
| Case exact pass rate | 16.67% | Report-only | — |
| Route accuracy | 63.89% | 95% | No |
| Responsibility accuracy | 32.35% | 90% | No |
| Tone accuracy | 55.88% | 90% | No |
| Overall accuracy | 41.18% | 90% | No |
| Required-question recall | 0% | 90% | No |
| Question-turn compliance | 22.22% | 90% | No |
| Required revision-fact recall | 0% | 100% | No |
| Revision-turn compliance | 25% | 100% | No |
| Critical invariant violations | 1 | 0 | No |

Cases passing every compared field: 5 of 30. Cases with at least one mismatch: 25 of 30.

## Critical failure

`BH-028` turn 1 failed `recipient-scope-respected`: the requested message was for the user's manager, but the revision addressed Ingrid, the author of the source email.

## Diagnostic audit

The post-score diagnostic did not alter the result:

- clear Skill/output defects: 18 cases, 19 turns;
- high gold-disagreement risk: 18 cases, 23 turns;
- exact-token vocabulary mismatch: 13 cases, 13 turns;
- route/rating extraction uncertainty: 7 cases, 7 turns;
- critical invariant failures: 1 case, 1 turn.

At least 8 of 46 required-question misses and 15 of 60 required-revision-fact misses were exact-token synonym mismatches. This explains part, but not all, of the low score.

Gold construction itself was difficult: cloud labelers disagreed on 242 of 396 turn-field comparisons before adjudication. The final gold is valid under the frozen rubric, but the disagreement rate is an important uncertainty on benchmark reliability.

## Evidence

All artifacts are under `tests/blind/cloud-holdout/`, including:

- frozen cases and images;
- designer, labeler, adjudicator, and evaluator attestations;
- provisional and final gold;
- freeze manifests;
- original and normalized raw Skill outputs;
- output freeze;
- semantic evaluations;
- immutable score report;
- diagnostic audit.

## Method limitations

- Cloud agents attested to restricted file access, but no filesystem access log was available.
- Gold labeler 2 inspected `freeze_holdout.py` schema fragments and designer-attestation top-level keys to match output envelopes. It did not read runtime rules, public tests, Skill outputs, scoring thresholds, or other labels, but this exceeded the plan's cases-plus-rubric-only restriction.
- Output agents repeatedly ignored the requested JSON envelope; deterministic normalization preserved verbatim output and used cloud Git author time when an execution timestamp was missing.
- Gold and output evaluation used heterogeneous models, but no human gold labeler was available.
- Exact topic/fact token matching penalized semantically equivalent synonyms.
- This did not test a live probabilistic Cursor dispatcher.

## Conclusion

Blind holdout testing is complete and failed its preregistered gate. The result is not evidence that every mismatch is a product defect, but it is sufficient to reject any claim that the current regression-suite pass rate proves high unseen-case accuracy.

Any product fixes, gold-rubric changes, or token-ontology changes must occur in a separate follow-up branch. This consumed holdout must not be reused as a fresh blind benchmark.
