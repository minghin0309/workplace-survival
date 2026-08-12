# Workplace Survival Interaction Quality Results

## Evidence policy

- Canonical evidence requirements: `tests/evidence/README.md`.
- Runs before T13.10 are historical summary-only results.
- The T13.10 representative interaction-quality record is stored in `tests/evidence/t13-10-validation.json`.
- T13.12 evidence-complete records are stored in `tests/evidence/t13-12-final.json`.

Representative T13.10 record: `t13.10-iq-iq01-20260812`.

## Summary

- Cases executed: 6.
- Response rounds executed: 10.
- Cases passed: 6.
- Cases failed: 0.
- Required assertions passed: 18 of 18.

## Results

- IQ-01: PASS — Ignored irrelevant lunch uncertainty, asked no question, and did not rewrite a green message.
- IQ-02: PASS — Asked no question and used `No revision needed` without an optional rewrite.
- IQ-03: PASS — Asked one material question with balanced confirmation options and no preferred answer.
- IQ-04: PASS — Added the explicit owner answer to Data A and did not repeat the owner question.
- IQ-05: PASS — Identified the owner contradiction and responsibility-shifting wording without predicting the manager's reaction.
- IQ-06: PASS — Retained the confirmed date and did not repeat or paraphrase the resolved date question.

## Defect counts

- Unnecessary questions: 0.
- Leading answer structures or suggestions: 0.
- Repeated questions, including paraphrases: 0.
- Forced rewrites of green messages: 0.
- Definite manager-reaction predictions: 0.

## Existing functional-suite audit

The 111 functional cases also verify question limits, neutral answer structures, resolved-question handling, green-message behavior, minimal revision, risk wording, one-target short acknowledgements, paired Tone controls, responsibility boundaries, prompt-like data isolation, material OCR/order confirmation, limited-background internal issues, case splitting, and recipient scope. In the latest T13.9 regression, all 111 functional cases passed, including 13 attached-image executions.

## T10.3 conclusion

All targeted interaction-quality cases were rerun after the post-T11.5 changes and passed. Every question and revision was traceable to a specific requirement, ambiguity, contradiction, or missing value in the test input.

## T13.4 regression — 2026-08-12

- IQ-01–IQ-06: 6 passed, 0 failed across 10 response rounds.
- Required assertions: 18 of 18 passed.
- IQ-05 Tone rating: Yellow for responsibility-shifting wording; the owner contradiction remained independently Red under responsibility clarity.

## T13.5 regression — 2026-08-12

- IQ-01–IQ-06: 6 passed, 0 failed across 10 response rounds.
- Required assertions: 18 of 18 passed.
- Unknown values remained placeholders and unresolved questions remained neutral.

## T13.6 regression — 2026-08-12

- IQ-01–IQ-06: 6 passed, 0 failed across 10 response rounds.
- Required assertions: 18 of 18 passed.
- IQ-01–IQ-06 contain no acknowledgement-target-specific case; T13.6 clarification-question assertions are recorded in functional TC-79–TC-84.

## T13.7 regression — 2026-08-12

- IQ-01–IQ-06: 6 passed, 0 failed across 10 response rounds.
- Required assertions: 18 of 18 passed.
- IQ-01–IQ-06 contain no prompt-like case; T13.7 format, evidence, citation, and outer-request assertions are recorded in functional TC-85–TC-92.

## T13.8 regression — 2026-08-12

- IQ-01–IQ-06: 6 passed, 0 failed across 10 response rounds.
- Required assertions: 18 of 18 passed.
- IQ-01–IQ-06 contain no OCR or image-order case; T13.8 confirmation assertions are recorded in attached-image functional TC-93–TC-99.

## T13.9 regression — 2026-08-12

- IQ-01–IQ-06: 6 passed, 0 failed across 10 response rounds.
- Required assertions: 18 of 18 passed.
- IQ-01–IQ-06 contain no explicit recipient-scope case; T13.9 role and scope assertions are recorded in functional TC-106–TC-111.

## T13.12 evidence-complete record index

- Evidence file: `tests/evidence/t13-12-final.json`.
- Records:
  - `t13.12-iq-01-20260812`, `t13.12-iq-02-20260812`, `t13.12-iq-03-20260812`, `t13.12-iq-04-20260812`, `t13.12-iq-05-20260812`, `t13.12-iq-06-20260812`

## T13.12 final result

- Cases: 6 passed, 0 failed.
- Response rounds: 10.
- Required assertions: 18 of 18 passed.
- All records satisfy the T13.10 evidence schema.
