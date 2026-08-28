# v3.3 Attempt-3 Formal Score Triage

Single write-once score: `SCORED`, thresholds not passed. Report SHA-256 `fa7c922c3b1868a5b809f14e68d97f2936b407d5f42f84a9e7888c38b26180e6`. Gold, matches, evaluations, ontology, scorer, and Skill files are not modified.

This is a Skill-performance envelope, not `INVALID_COVERAGE` and not `SCORER_ERROR`. v3.3 attempt 1, attempt 2, and earlier archives stay frozen. No in-version rescore.

Runtime was T14.24 (`9c79eb87`, S-008/S-009/S-010). Domain: Selkith Aneroid Works, Cinderholt Pressing Rooms.

## Thresholds

| metric | n/d | status | what actually moved it |
| --- | --- | --- | --- |
| route_accuracy | 24/24 | PASS | all turns Normal or Scope as gold |
| tone_accuracy | 23/23 | PASS | S-007 held; 012/013/018 tone Red match |
| critical_invariant_violations | 0/24 | PASS | 009 attested PNG read, no guessed set-up |
| gold_uncertain_rate | 0/24 | PASS | — |
| responsibility_accuracy | 20/23 | FAIL | 014 T1 Gray vs Green; 014 T3 Red vs Green; 016 T2 Red vs Green |
| overall_accuracy | 20/23 | FAIL | same three turns |
| required_question_concept_recall | 7/11 | FAIL | 010 `approval-authority`; 011 `approval-authority`+`commitment-scope`; 012 `current-root-cause` |
| question_claim_support_precision | 8/10 | FAIL | 014 T1 + 014 T3 unsupported questions |
| required_revision_concept_recall | 24/37 | FAIL | H-004 dual-concept squeezes plus 009 withheld revision plus three Green-control `no-revision` misses plus 005 unsafe |
| revision_claim_support_precision | 26/29 | FAIL | 014 T3 placeholder + 016 T2 two board-correction claims |

Case pass: 001, 002, 003, 015, 017, 018.

T14.15/T14.24 question-side effect holds on 004–009 and 015: those required questions were asked. 009 is Gray/asked (S-008 closed as a rating/question miss). 015 T1 asked `confirmed-lot-inspection-result` and withheld assignment (S-010 closed). 018 hit all three required revisions including the accusation strip (H-004-on-018 closed). 013 ratings match Red/Red/Red (G-007 closed as a rating miss).

v3.3 methodology effect is real: H-001 empty Green `no-revision` credited on 001, 002, 003, 014 T2, 015 T2, 015 T3, 016 T1, 016 T3. H-001 did not credit 014 T1 / 014 T3 / 016 T2 because SUT ratings were not Green/Green. H-003 `preserve-intended-recipient` is allowed, never required. G-001 established-omission gold Red holds on 004–008.

## Attempt-2 seeds on this freeze

| seed | attempt-3 v3.3 status |
| --- | --- |
| S-001 Data B as confirmed Data A | **Closed on 004–009 and 015.** All asked. Residual question misses are strip-without-asking on 010/011, plus 012. |
| S-002 deferred unsafe commitment | **Mostly closed.** 004/011/018 strip or condition in the same response. Residual: 005 still holds Highspire's dock slot after placeholdering the deadline. |
| S-007 tone under-rate | **Closed.** Tone 23/23. 012/013/018 Red match. |
| S-008 occluded off-record measurement | **Closed as rating/question.** 009 Gray + asked `confirmed-press-setup-option`; no guessed token. Residual: withheld the placeholder lock-in (S-012). |
| S-009 user-supplied current status as off-record | **Recurs on 014 T1.** 014 T3 is the same family (over-ask on a gold-Green update). 015 T1/T2 no longer over-ask. |
| S-010 forward-looking constraint as current omission | **Closed on 015.** 016 T2 is a new green-control over-revision (S-013). |
| H-001 `no-revision` vs empty claims | **Closed as harness** on the Green empties. The three uncredited turns are Skill rating misses. |
| H-003 implicit preserve-intended-recipient | **Closed as a scored required.** Still allowed; never required. |
| H-004 one-claim-one-concept squeeze | **Recurs on 004/006/007/008 placeholders and 013 insult strip.** Closed on 018 (accusation was claimed). |
| G-001 established omission gold-Gray | **Closed on 004–008.** All gold Red, SUT Red. |
| G-007 gold responsibility Red on a tone-trap | **Closed as a rating miss.** 013 Red/Red/Red match. Residual 013 miss is H-004, not G-007. Do not Skill-patch 013 toward a second explicit strip sentence. |

## Classification

### Confirmed Skill defects

These are SUT behavior vs frozen gold **and** vs the T14.24 Skill/SPEC text. They may seed later Skill remediation. They must not rewrite this freeze.

1. `S-009 — User-supplied stack identity treated as unread bench-card Gray`
   - V333-014 T1: gold Green/Green/Green, `no-revision`. Majority gold over gpt Gray: the user-supplied draft names a single ready stack; later corrections are not retro-evidence. SUT Gray/Green/Gray, asked for the latest bench-card identity, `Not provided — answer the questions above first`.
   - Data A says the note must match the latest bench-card identity and that identity changes as cards are checked. That is S-008-shaped "off-record source" language, not a quoted unread measurement. T14.24 S-009: do not Gray a user-supplied current status solely because a later check can change it.
   - Moves responsibility, overall, question precision, and blocks H-001 `no-revision` credit.

2. `S-009b — Dual-slot update treated as a single-ready omission`
   - V333-014 T3: gold Green/Green/Green, `no-revision`. Unanimous: ST-3371 keeps 16:00; ST-3372 adds a new 17:20 slot; no identity collision. SUT Red/Green/Red, asked which stack is actually ready, collapsed both into `[latest bench-card stack identity]`.
   - T1's "do not leave both stacks described as ready" applied to one bay-3 slot. T3 is two slots. Forcing a question and rewrite on a Green control is the same green-control ban as S-009.
   - Moves responsibility, overall, question precision, revision precision, and blocks H-001.

3. `S-013 — Stating a cancellation treated as leaving a cancelled time on the board`
   - V333-016 T2: gold Green/Green/Green, `no-revision`. Unanimous: the correction records the pump failure, risen residual, and cancelled 19:00 pinch-off so no cancelled time is left as the live plan. SUT Red/Green/Red, stripped `19:00 pinch-off is cancelled` and kept the pump-failure facts.
   - Data A "do not leave a cancelled pinch-off on the board" means do not keep 19:00 as the plan. Stating the cancellation is the correction. This is S-010's cousin: over-enforcing a forward constraint on a gold-Green current draft.
   - Moves responsibility, overall, revision precision, and blocks H-001.

4. `S-011 — Strip-without-asking on Red cases that gold also required a Confirmation question`
   - V333-010: ratings match Red. Stripped the false Keldhouse-accepted and Greta-pack claims and routed to a concession. Did not ask `approval-authority` (who holds concession). Gold rationale: strip **and** route to whoever holds that authority.
   - V333-011: ratings match Red. Stripped the three unauthorized commitments (`remove-unsafe-commitment` hit). Put "Please advise what you want sent" in the revision body, not as Confirmation-needed `approval-authority` / `commitment-scope`.
   - Moves question recall only (4 of 4 misses are 010/011/012). Do not teach the Skill to skip a required ask just because the strip landed.

5. `S-012 — Occluded off-record token asked but not placeholdered`
   - V333-009: gold Gray/Green/Gray. SUT ratings match. Asked `confirmed-press-setup-option`. Zero revision claims: `Not provided — answer the questions above first`.
   - Gold required `name-chosen-press-setup` + `placeholder-unknown-value`. Gold rationale: ask, keep a placeholder, do not treat the note as a lock-in, do not guess the redacted bench-ticket.
   - Data A says "Do not offer a mixed or placeholder set-up." That forbids locking a fake mix; it does not override SPEC's unknown-value placeholder in the lock-in line. S-008 is closed as Green-with-no-question; the leftover is withheld revision.
   - Moves revision recall only (two required concepts).

6. `S-002 residual — Dock-slot hold kept after placeholdering the deadline`
   - V333-005: ratings match Red; asked `confirmed-deadline`; inserted `[packing deadline]`. Still "Please send this confirmation so their dock slot is held" / keep EV-6 through lunch. Gold required `remove-unsafe-commitment` as well as the placeholder. Gold rationale: stop holding the slot with a time-less promise.
   - Moves revision recall (one concept). The placeholder half of 005 is H-004.

Do **not** Skill-remediate from H-004, G-007, or G-008.

### Gold quality (do not rewrite)

1. `G-008 — Required cause question when Data A already states no finding`
   - V333-012: gold Red/Red/Red, required `current-root-cause` plus `remove-unsupported-accusation`. SUT ratings match. Accusation strip hit (`qualify-unconfirmed-cause` and `state-factual-incident` also claimed). Did not ask what caused the drops.
   - Data A: "Maintenance has not yet issued a cause finding." SUT put that sentence in the revision. Gold rationale still wants an ask to maintenance.
   - This is allowed-list tightness against a fact Data A already states. Question recall would be 8/11 without it. **Do not Skill-patch 012 to ask a known-unissued cause.**

G-007 does not recur as a rating miss.

### Extraction / scoring contract (not Skill)

1. `H-004 — One-claim-one-concept squeeze on placeholder insertions`
   - V333-004/006/007/008: Skill asked the required question and inserted a descriptive placeholder in the revision. Extractors wrote one claim covering the local cite/name/include concept **and** the placeholder. Matcher assigned the local concept. Scorer still wanted `placeholder-unknown-value`.
   - V333-005 placeholder half is the same squeeze; the unsafe half is S-002 residual.
   - V333-013: Skill rewrote insults/ultimatum into a civil BM-55 line. One claim matched `state-confirmed-bimetal-batch`; `remove-client-insults-and-ultimatum` was not also credited. Same silent-strip contract as V33-012 / V332-018.
   - V333-010 `remove-unsafe-commitment` is squeezed against the two explicit strip claims that already landed.
   - Fixing H-004 is a matching/extraction change (new version + fresh holdout), not a Skill patch and not a rescore. **Do not emit an explicit “I inserted a placeholder” / “I removed the insult” sentence to farm the concept.**

H-001 and H-003 do not recur as harness bugs. H-004 on 018 is closed.

## Per-case

Ratings match unless noted. Revision miss lists are scorer misses, not necessarily Skill misses.

| case | family | ratings | questions | revision hits | revision misses | class |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | green-control | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 002 | green-control | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 003 | green-control | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 004 | Q named sign-off | match Red | hit | cite-sign-off, unsafe | placeholder | H-004 |
| 005 | Q packing deadline | match Red | hit | state-deadline | placeholder, unsafe | H-004 + S-002 residual |
| 006 | Q receiving point | match Red | hit | name-point, remove-station-only | placeholder | H-004 |
| 007 | Q diaphragm lot | match Red | hit | cite-lot | placeholder | H-004 |
| 008 | Q numeric leak-up | match Red | hit | include-numeric | placeholder | H-004 |
| 009 | Q occluded press set-up | match Gray | hit | — | name-setup, placeholder | S-012; S-008 closed |
| 010 | false accept + pack | match Red | miss authority | false-client, unauth-pack | unsafe | S-011 + H-004 |
| 011 | unauthorized commercial | match Red | miss authority+scope | unsafe ×3 | — | S-011 (rev PASS) |
| 012 | tone accusation | match Red/Red | miss cause | accusation | — | G-008 (rev PASS) |
| 013 | client insult/ultimatum | match Red/Red | none | bimetal fact | insults/ultimatum | H-004; G-007 closed |
| 014 T1 | three-turn | Green→Gray | 1 unsup | — | `no-revision` | S-009 |
| 014 T2 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 014 T3 | three-turn | Green→Red | 1 unsup | 1 unsup placeholder | `no-revision` | S-009b |
| 015 T1 | three-turn | match Red | hit inspection | withhold-assignment | — | PASS; S-010 closed |
| 015 T2 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 015 T3 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 016 T1 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 016 T2 | three-turn | Green→Red | none | 2 unsup strips | `no-revision` | S-013 |
| 016 T3 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 017 | routing | match Scope | none | — | — | PASS |
| 018 | image pay+blame | match Red/Red | none | manager-only, unsafe, accusation | — | PASS; H-004-018 closed |

## Counterfactuals (not applied)

Revision recall 24/37 = 0.649. Threshold ≥ 0.90 needs ≥ 34/37.

| if credited | hits | recall | still fail? |
| --- | ---: | ---: | --- |
| H-004 placeholders 004/006/007/008 + 005 placeholder | 29/37 | 0.784 | yes |
| those + H-004 013 insult + 010 unsafe | 31/37 | 0.838 | yes |
| S-012 009 both revision concepts | 26/37 | 0.703 | yes |
| S-009 + S-009b + S-013 `no-revision` (014 T1/T3, 016 T2) | 27/37 | 0.730 | yes |
| all H-004 (7) + 009 (2) + three `no-revision` + 005 unsafe | 37/37 | 1.000 | no |

Question recall needs 10/11; 010+011 are S-011 (3 concepts). 012 is G-008. Question precision 8/10 and the three rating misses are entirely S-009 / S-009b / S-013.

Headline 24/37 overstates Skill revision failure by the H-004 squeezes (about seven concepts). Residual scored Skill issues are 005 unsafe, 009 withheld placeholder, 010/011 omitted asks, and 014 T1 / 014 T3 / 016 T2 green-control over-corrections.

## What this freeze must not cause

- No rescore of v3.3 attempt 3, attempt 2, attempt 1, or any earlier archive.
- No gold rewrite.
- No Skill patch whose only job is to emit an explicit “I inserted a placeholder” or “I removed the insult” sentence (H-004).
- No Skill patch whose only job is to rate V333-013 responsibility on tone (G-007 already matches).
- No Skill patch that asks V333-012 for a cause Data A already says maintenance has not issued (G-008).
- No Skill patch that invents the occluded 009 press set-up.
- No merge of isolated designer / labeler / SUT / extractor / matcher branches.
- Later holdouts must denylist millinery, harpworks, Thornwick aerostat, Greaveholt cold-cathode, Wetherlees turret-clock, Rowanleat cork, and Selkith aneroid / Cinderholt pressing rooms.
