# T14.27 S-009 / S-011 / S-012 / S-013 / S-002 Residual Remediation Results

v3.3 attempt-3 freeze remains `SCORED` and is not rescored. Gold, matches, evaluations, ontology, scorer, and holdout artifacts were not rewritten.

## Rule changes

- A requirement that the note match the latest card or board check does not Gray a user-supplied current identity for this turn when Data A quotes no conflicting recorded value.
- Two items with distinct current slots are not the same-slot dual-ready fault.
- Stating that a time or commitment is cancelled satisfies a constraint not to leave that cancelled item as the live plan.
- After stripping an unauthorized commitment, Confirmation needed still asks remaining authority or scope when that fact is not already explicit in Data A.
- Gray for an unquoted off-record token that the outgoing note must name gets a placeholdered revision. Case-data "do not offer a placeholder mix" does not forbid that placeholder.
- Placeholdering a missing deadline does not leave a time-less dock-slot hold sendable.
- A cause Data A says has not been issued is not asked.

## Semantic check (new cases + regressions)

| ID | result | notes |
| --- | --- | --- |
| TC-07 | PASS | Manager asked for the responsible name; no off-record source; Data B may answer. |
| TC-115 | PASS | Notebook/board date unquoted; 26 August stays a Data B claim; Gray + question + placeholder. |
| TC-117 | PASS | Unestablished authorization stripped now; remaining locker-note ask still allowed. |
| TC-119 | PASS | Unquoted header width; draft points at the card; Gray, not Green-by-omission. |
| TC-120 | PASS | Latest status C-9 is user-supplied this turn; Green; no stillage-record question. |
| TC-122 | PASS | Bench-card-match language does not Gray user-supplied R-4 identity. |
| TC-123 | PASS | Distinct 16:00 and 17:20 slots stay Green; no collapse to one ready identity. |
| TC-124 | PASS | `19:00 pinch-off is cancelled` is the correction, not a live cancelled plan. |
| TC-125 | PASS | False accept/pack claims stripped; Confirmation needed still asks remaining authority. |
| TC-126 | PASS | Gray + ask + `[chosen press set-up]` revision; case-data mix ban does not withhold it. |
| TC-127 | PASS | Deadline placeholder plus dock-slot hold stripped or conditioned. |
| TC-128 | PASS | Accusation stripped; unissued cause finding is not asked. |

No 128-case re-run. Image fixtures were not reopened. v3.3 SUT outputs were not replayed.

## Out of scope

H-004, G-007, and G-008 were not changed as Skill patches. TC-128 only locks the existing "do not ask a fact already explicit in Data A" rule.
