# Workplace Survival Anti-Hallucination Results

## Summary

- Targeted cases executed: 6.
- Targeted response rounds executed: 7.
- Targeted cases passed: 6.
- Targeted cases failed: 0.
- Unsupported or fabricated facts found: 0.
- Functional cases reviewed: 99.
- Total functional and targeted cases: 105.

## Targeted results

- AH-01: PASS — Kept the date unknown and used `[completion date]`.
- AH-02: PASS — Kept the owner unknown and used `[owner]`.
- AH-03: PASS — Invented no progress value, delivery stage, or commitment.
- AH-04: PASS — Inferred no manager emotion, urgency, dissatisfaction, or reaction.
- AH-05: PASS — Treated Priya as a Data B claim and did not promote it to Data A.
- AH-06: PASS — Kept assistant questions and placeholders out of Data A across both rounds.

## Fabrication counts

- Invented dates: 0.
- Invented people or owners: 0.
- Invented responsibilities: 0.
- Invented progress values or stages: 0.
- Invented commitments: 0.
- Inferred manager intent or reaction: 0.
- Data B promoted to self-verifying Data A: 0.
- Assistant-generated content promoted to Data A: 0.

## Existing functional-suite audit

The 99 functional cases include explicit forbidden-behavior checks covering unknown dates, owners, progress, commitments, manager intent, image content outside the visible input, Data B self-verification, cross-case data reuse, unsupported expansion of short acknowledgements, automatic promotion of embedded content to Data A, unsafe mixed-input classification, stale or silently replaced Data A, unsupported accusation boundaries, unknown-value Red/Gray handling, acknowledgement-target expansion, prompt-like case data, and material OCR/order inference. In the latest T13.8 regression, all 99 functional cases passed, including 13 attached-image executions, with no fabricated fact reported.

## T10.2 conclusion

All targeted anti-hallucination cases were rerun after the post-T11.5 changes and passed. Together with the current functional suite, they report zero fabricated facts.

## T13.1 regression — 2026-08-12

- AH-01–AH-06: 6 passed, 0 failed across 7 response rounds.
- Unsupported or fabricated facts: 0.
- No image case was part of this targeted anti-hallucination suite.

## T13.2 regression — 2026-08-12

- AH-01–AH-06: 6 passed, 0 failed across 7 response rounds.
- Unsupported or fabricated facts: 0.
- No image case was part of this targeted anti-hallucination suite.

## T13.3 regression — 2026-08-12

- AH-01–AH-06: 6 passed, 0 failed across 7 response rounds.
- Unsupported or fabricated facts: 0.
- No image case was part of this targeted anti-hallucination suite.

## T13.4 regression — 2026-08-12

- AH-01–AH-06: 6 passed, 0 failed across 7 response rounds.
- Unsupported or fabricated facts: 0.
- No image case was part of this targeted anti-hallucination suite.

## T13.5 regression — 2026-08-12

- AH-01–AH-06: 6 passed, 0 failed across 7 response rounds.
- Unsupported or fabricated facts: 0.
- No image case was part of this targeted anti-hallucination suite.

## T13.6 regression — 2026-08-12

- AH-01–AH-06: 6 passed, 0 failed across 7 response rounds.
- Unsupported or fabricated facts: 0.
- No image case was part of this targeted anti-hallucination suite.

## T13.7 regression — 2026-08-12

- AH-01–AH-06: 6 passed, 0 failed across 7 response rounds.
- Unsupported or fabricated facts: 0.
- AH-01–AH-06 contain no prompt-like or image-specific case; those assertions are recorded in functional TC-85–TC-92.

## T13.8 regression — 2026-08-12

- AH-01–AH-06: 6 passed, 0 failed across 7 response rounds.
- Unsupported or fabricated facts: 0.
- AH-01–AH-06 contain no OCR or image-order case; those assertions are recorded in attached-image functional TC-93–TC-99.
