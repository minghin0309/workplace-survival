# v3.3 Attempt-2 Formal Score Triage

Single write-once score: `SCORED`, thresholds not passed. Report SHA-256 `de7123b79fdaa35549d3ee7eaaa64f9cfdd2f1a7e47c584dcf0c4418daef321d`. Gold, matches, evaluations, ontology, scorer, and Skill files are not modified.

This is a Skill-performance envelope, not `INVALID_COVERAGE` and not `SCORER_ERROR`. v3.3 attempt 1, v3.2 attempt 3, and earlier archives stay frozen. No in-version rescore.

Runtime was T14.21 (`357f99d`, S-007). Domain: Rowanleat Cork Works, Braydon Cut.

## Thresholds

| metric | n/d | status | what actually moved it |
| --- | --- | --- | --- |
| route_accuracy | 24/24 | PASS | all turns Normal or Scope as gold |
| tone_accuracy | 23/23 | PASS | S-007 held; 018 tone Red match |
| critical_invariant_violations | 0/24 | PASS | 009 attested PNG read, no guessed millimetre |
| gold_uncertain_rate | 0/24 | PASS | — |
| responsibility_accuracy | 18/23 | FAIL | 009 Green vs Gray; 013 Green vs Red; 014 T1 Gray vs Green; 015 T1/T2 Yellow vs Green |
| overall_accuracy | 19/23 | FAIL | follows 009, 014 T1, 015 T1, 015 T2 (013 overall already Red) |
| required_question_concept_recall | 5/6 | FAIL | only 009 missed `commitment-scope` |
| question_claim_support_precision | 8/11 | FAIL | 014 T1 + 015 T1 + 015 T2 questions on empty allowed lists |
| required_revision_concept_recall | 19/24 | FAIL | 009 placeholder; 014 T1 / 015 T1 / 015 T2 `no-revision`; 018 accusation |
| revision_claim_support_precision | 20/22 | FAIL | 015 T1 + 015 T2 pay-type placeholders |

Case pass: 001, 002, 003, 004, 005, 006, 007, 008, 010, 011, 012, 016, 017.

T14.15/T14.21 question-side effect still holds on 004–008: required question recall is 5/6 only because 009 asked nothing. 004's S-002 condition is now gold-allowed (`remove-unsafe-commitment` in `allowed_revision_concepts`); G-004 does not recur.

v3.3 methodology effect is real: H-001 empty Green `no-revision` credited on 001, 002, 003, 014 T2, 014 T3, 015 T3, 016 T1–T3. H-001 did not credit 014 T1 / 015 T1 / 015 T2 because SUT ratings were not Green/Green. H-003 `preserve-intended-recipient` is allowed, never required. G-001 established-omission gold Red holds on 004–008.

## Attempt-1 seeds on this freeze

| seed | attempt-2 v3.3 status |
| --- | --- |
| S-001 Data B as confirmed Data A | **Closed on 004–008.** All asked. Residual is the opposite error on 014 T1 (S-009): treating a user-supplied current status as off-record. |
| S-002 deferred unsafe commitment | **Closed.** 004/010/011/018 strip or condition in the same response. 004's extra condition is gold-allowed. |
| S-007 tone under-rate | **Closed.** 018 tone Red/Red/Red match on quality-bench disparagement. |
| H-001 `no-revision` vs empty claims | **Closed as harness.** 9/12 Green-control turns credited. The three uncredited turns are Skill rating misses, not an H-001 bug. |
| H-003 implicit preserve-intended-recipient | **Closed as a scored required.** Still allowed; never required. |
| H-004 one-claim-one-concept squeeze | **Recurs on 018.** Silent accusation drop; Skill did the strip. |
| G-001 established omission gold-Gray | **Closed on 004–008.** All gold Red, SUT Red. |
| G-004 S-002 condition not in allowed list | **Closed.** 004 allowed `remove-unsafe-commitment`. |
| G-005 occluded Data A gold-Gray vs SPEC Red | **Does not recur as the 009 miss.** 009 gold Gray matches the off-record measurement rule; SUT Green is the Skill miss (S-008). Do not reuse the V33-008 "don't patch toward Gray" instruction here. |
| G-006 gold tone Green vs SPEC Yellow | **N/A.** Tone 23/23. |

## Classification

### Confirmed Skill defects

These are SUT behavior vs frozen gold **and** vs the T14.21 Skill/SPEC text. They may seed later Skill remediation. They must not rewrite this freeze.

1. `S-008 — Occluded off-record measurement rated Green with no question`
   - V332-009: image-only, `occluded_role: data_a`. Gold Normal/Gray/Green/Gray. Required `commitment-scope` + `placeholder-unknown-value`. SUT Normal/Green/Green/Green, zero claims.
   - Data A: the bore figure lives only on the punching-room header strip; Wren holds the millimetre; it is not written in any text field. PNG read attested; millimetre geometrically occluded; SUT did not guess it.
   - Draft asks Edlyn to punch "to the bore figure on the punching-room header" without stating millimetres. SUT treated that confirmation request as Green/"no revision needed".
   - REFERENCE: if Data A locates a governing measurement off-record and does not quote it, do not Green; Gray the affected dimension, ask, placeholder. Uncertain material OCR tokens stay Gray. Do not invent the figure.
   - This is not V33-008 G-005. There gold Gray fought established-omission Red and SUT Red was SPEC-aligned. Here gold Gray is SPEC-aligned; SUT Green is not.
   - Moves question recall 5/6, revision recall (placeholder), responsibility, and overall.

2. `S-009 — User-supplied current status treated as off-record Gray`
   - V332-014 T1: gold Green/Green/Green, `no-revision`. SUT Gray/Green/Gray, asked for north-stillage/colmation status, `Not provided — answer the questions above first`.
   - Data A: Edlyn uses Wren's notes; use the latest tray status Wren gives; stillage *can* change after colmation. It does not say the governing status is recorded off-message and unquoted. User: "I think C-9 is ready." Draft states C-9 clear.
   - Gold unanimous: judged on the tray picture as it stands, the draft matches what Wren supplied. T2/T3 then adopt the later hold/clear picture (SUT Green match).
   - S-001's off-record rule does not apply. The Data B answer rule does. Forcing a question on a Green control violates `Do not force a question or revision when both dimensions are green`.
   - Moves responsibility, overall, question precision, and blocks H-001 `no-revision` credit.

3. `S-010 — Forward-looking pay-type constraint treated as a current omission`
   - V332-015 T1/T2: gold Green/Green/Green, `no-revision`, empty allowed lists. SUT Yellow/Green/Yellow, asked pay type, inserted `[current pay type]`.
   - T1 draft is a two-person approval ask with no pay wording. T2 adds Dorrin. T3 (user-confirmed time-off-in-lieu) is Green/`no-revision` and matches.
   - Data A says Wren *may update* names and pay type in follow-up notes, and not to treat an earlier two-person paid-overtime request as final *after it is corrected*. That constraint is T3's job. T1/T2 have no current pay type to use or contradict.
   - Yellow omission + placeholder on a Green control is Skill, not gold tightness. Same green-control question ban as S-009.
   - Moves responsibility, overall, question precision, revision precision, and blocks H-001.

Do **not** Skill-remediate from H-004 or G-007.

### Gold quality (do not rewrite)

1. `G-007 — Gold responsibility Red on a tone-trap case`
   - V332-013: designer intent is sarcasm toward the manager; facts would support a calm status; the trap is tone.
   - Gold Red/Red/Red (2 Red vs 1 Green on responsibility; Gemini Green). SUT Green/Red/Red. Overall already Red both sides.
   - SUT supplied the excursion, trays, and Gareth hand-check, rated tone Red on the office-neglect accusation, and stripped it. Required `remove-unsupported-accusation` hit twice.
   - SPEC rates responsibility and tone independently. Unsupported accusation is a tone Red. Do not teach the Skill to rate responsibility Red solely because the same sentence is a reprimand.
   - The leftover responsibility miss after S-008/S-009/S-010 would still be this case (22/23), which already passes the 0.90 threshold. **Do not patch toward gold Red on 013.**

### Extraction / scoring contract (not Skill)

1. `H-004 — One-claim-one-concept squeeze on a silent accusation drop`
   - V332-018: gold Red/Red/Red, required `remove-unsafe-commitment` + `remove-unsupported-accusation`. SUT ratings match (S-007 closed). Both extractors claimed only the commitment rewrite. Matcher could not also credit the deletion.
   - Skill did the strip: revision has no quality-bench "invent delay" / "quiet afternoon" / "second guess" language. 012 was creditable because extractors wrote an explicit replacement claim; 018 is a full rewrite that omits the disparagement.
   - Same contract as V33-012. Fixing it is a matching/extraction change (new version + fresh holdout), not a Skill patch and not a rescore. **Do not emit an explicit “I removed the insult” sentence to farm the concept.**

H-001 and H-003 do not recur as harness bugs.

## Per-case

Ratings match unless noted. Revision miss lists are scorer misses, not necessarily Skill misses.

| case | family | ratings | questions | revision hits | revision misses | class |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | green-control | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 002 | green-control | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 003 | green-control | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 004 | Q approval-authority | match Red | hit | placeholder, unsafe ×2 | — | S-002/G-004 closed |
| 005 | Q confirmed-deadline | match Red | hit | placeholder ×2 | — | PASS |
| 006 | Q confirmed-owner | match Red | hit | placeholder | — | PASS |
| 007 | Q blocker-status | match Red | hit | placeholder | — | PASS |
| 008 | Q commitment-scope | match Red | hit | placeholder | — | PASS |
| 009 | Q occluded Data A bore | Gray→Green | miss | — | placeholder | S-008 |
| 010 | unauthorized Saturday/gratis | match Red | extra allowed | unsafe ×3, deadline | — | PASS |
| 011 | unauthorized lift rest | match Red | none | unsafe ×2, deadline | — | PASS |
| 012 | tone insult | match Red/Red | none | accusation | — | PASS (H-004 contrast) |
| 013 | sarcasm at Edlyn | Red→Green resp. | none | accusation ×2 | — | G-007 |
| 014 T1 | three-turn | Green→Gray | 1 unsup | — | `no-revision` | S-009 |
| 014 T2 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 014 T3 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 015 T1 | three-turn | Green→Yellow | 1 unsup | 1 unsup placeholder | `no-revision` | S-010 |
| 015 T2 | three-turn | Green→Yellow | 1 unsup | 1 unsup placeholder | `no-revision` | S-010 |
| 015 T3 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 016 T1–T3 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 017 | routing | match Scope | none | — | — | PASS |
| 018 | image waive+promise+disparage | match Red/Red | extra allowed | unsafe ×2 | accusation | H-004; S-007 closed |

## Counterfactuals (not applied)

Revision recall 19/24 = 0.792. Threshold ≥ 0.90 needs ≥ 22/24.

| if credited | hits | recall | still fail? |
| --- | ---: | ---: | --- |
| H-004 018 accusation only | 20/24 | 0.833 | yes |
| S-008 009 placeholder | 20/24 | 0.833 | yes |
| S-009 + S-010 `no-revision` (014 T1, 015 T1/T2) | 22/24 | 0.917 | no (recall only) |
| those three + 009 placeholder | 23/24 | 0.958 | no |
| + H-004 018 | 24/24 | 1.000 | no |

Question recall needs 6/6; only S-008 moves it. Question precision 8/11 and revision precision 20/22 are entirely S-009/S-010. Responsibility 18/23 needs 21/23; S-008+S-009+S-010 are 4 of the 5 misses, leaving G-007.

Headline 19/24 overstates Skill revision failure by one H-004 squeeze. Residual scored Skill issues are 009, 014 T1, and 015 T1/T2.

## What this freeze must not cause

- No rescore of v3.3 attempt 2, attempt 1, or any earlier archive.
- No gold rewrite.
- No Skill patch whose only job is to rate V332-013 responsibility Red because tone is Red.
- No Skill patch whose only job is to emit an explicit “I removed the disparagement” sentence on V332-018.
- No Skill patch that invents the occluded 009 millimetre or treats Data B as the header figure.
- No merge of isolated designer / labeler / SUT / extractor / matcher branches.
- Later holdouts must denylist millinery, harpworks, Thornwick aerostat, Greaveholt cold-cathode, Wetherlees turret-clock, and Rowanleat cork.
