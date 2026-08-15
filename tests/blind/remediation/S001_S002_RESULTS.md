# T14.15 S-001 / S-002 Remediation Results

Attempt-2 freeze remains `SCORED` and is not rescored. Gold, matches, and v322 artifacts are not on this branch and were not rewritten.

## Rule changes

- Off-record governing tokens (notebook, locker note, card, board, unquoted source) that appear only in Data B are unconfirmed. Absence of conflict is not Green.
- The Data B answer rule still covers TC-07: a manager request to state a value in the message, with no off-record source.
- Unestablished authorization plus an asserted authority or client-agreed commitment is Red. Strip or condition it in the same response. Do not defer with `Not provided — answer the questions above first`.

## Semantic check (new cases + TC-07)

| ID | result | notes |
| --- | --- | --- |
| TC-07 | PASS | Manager asked for the responsible name; no off-record source; Data B may answer; Alex not promoted to Data A. |
| TC-115 | PASS | Notebook/board date unquoted; 26 August stays a Data B claim; Gray + question + placeholder. |
| TC-116 | PASS | Notebook-flap owner unquoted; Jordan Hale not confirmed; Gray + question; +2 correction preserved. |
| TC-117 | PASS | Locker note unquoted; "I have authority" + tell-the-client-agreed is Red; revision must strip/condition now. |

No 114-case re-run. Image fixtures were not reopened. v322 SUT outputs were not replayed.

## Out of scope

S-003 through S-006, H-001 through H-004, and G-001 were not changed.
