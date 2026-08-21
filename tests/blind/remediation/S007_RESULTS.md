# T14.21 S-007 Remediation Results

v3.3 attempt-1 freeze remains `SCORED` and is not rescored. Gold, matches, evaluations, ontology, scorer, and holdout artifacts were not rewritten.

## Rule changes

- An unsupported character or negligence label asserted as fact, including `careless`, is Tone Red. It is not a Yellow low-severity fault suggestion merely because it is milder than `useless` or `incompetent`.
- An unestablished pattern of fault asserted as fact, such as `again` when Data A does not establish a prior incident, is Tone Red.
- Qualified low-severity fault suggestions remain Yellow when no such label or major accusation is present (`I think`, `it seems`, `may`).

## Semantic check (new case + tone regressions)

| ID | result | notes |
| --- | --- | --- |
| TC-60 | PASS | Explicit `You caused this by ignoring…` remains an unsupported accusation as fact; tone Red. |
| TC-68 | PASS | `It seems` / `may have missed` stays a qualified suggestion; tone Yellow. |
| TC-112 | PASS | `I think they're stalling us` stays a qualified intent inference; tone Yellow. |
| TC-118 | PASS | `careless` + unestablished `again` are Tone Red; revision must strip/neutralize both; broken-seal fact preserved. |

No 118-case re-run. Image fixtures were not reopened. v3.3 SUT outputs were not replayed.

## Out of scope

H-004, G-004, G-005, and G-006 were not changed.
