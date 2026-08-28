# T14.24 S-008 / S-009 / S-010 Remediation Results

v3.3 attempt-2 freeze remains `SCORED` and is not rescored. Gold, matches, evaluations, ontology, scorer, and holdout artifacts were not rewritten.

## Rule changes

- An unquoted off-record measurement, including a header card or occluded image region, is not Green when Data B omits the token and points the recipient at that unread source. Gray, ask, placeholder; never invent the figure.
- A statement that a value can change later, or that the recipient uses the user's notes, does not locate a governing token off-record. A user-supplied current status in this turn uses the Data B answer rule.
- A note that a field may be updated in a later message is not a current explicit requirement. Do not Yellow/Red, ask, or placeholder that field when Data B does not assert it.

## Semantic check (new cases + regressions)

| ID | result | notes |
| --- | --- | --- |
| TC-07 | PASS | Manager asked for the responsible name; no off-record source; Data B may answer. |
| TC-115 | PASS | Notebook/board date unquoted; 26 August stays a Data B claim; Gray + question + placeholder. |
| TC-118 | PASS | `careless` + unestablished `again` remain Tone Red. |
| TC-119 | PASS | Unquoted header width; draft points at the card; Gray, not Green-by-omission; no invented millimetre. |
| TC-120 | PASS | Latest status C-9 is user-supplied this turn; Green; no stillage-record question. |
| TC-121 | PASS | Pay type only permitted as a later update; Green; no pay-type question or placeholder. |

No 118-case re-run. Image fixtures were not reopened. v3.3 SUT outputs were not replayed.

## Out of scope

H-004 and G-007 were not changed.
