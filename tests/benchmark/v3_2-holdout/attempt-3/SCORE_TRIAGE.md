# v3.2 Attempt-3 Formal Score Triage

Single write-once score: `SCORED`, thresholds not passed. Report SHA-256 `4f9a30bc01f6e419a4cc173f3a1f49bb19feb5ce8206ef2bbeb852ddabe1c834`. Gold, matches, evaluations, ontology, scorer, and Skill files are not modified.

This is a Skill-performance envelope, not `INVALID_COVERAGE` and not `SCORER_ERROR`. Attempt 2, attempt 1, and v3.1 stay archived. No in-version rescore.

Runtime was T14.15 (`d37540b`, S-001/S-002). Domain: Greaveholt Cold-Cathode Works.

## Thresholds

| metric | n/d | status | what actually moved it |
| --- | --- | --- | --- |
| route_accuracy | 23/24 | PASS | V323-008 Intake vs gold Normal; see G-003 |
| tone_accuracy | 21/23 | PASS | V323-008 null ratings (route) + V323-018 Yellow vs Red |
| critical_invariant_violations | 0/24 | PASS | — |
| gold_uncertain_rate | 0/24 | PASS | all 24 turns `heterogeneous_adjudicated` |
| required_question_concept_recall | 6/6 | PASS | S-001 holdout miss is gone |
| responsibility_accuracy | 16/23 | FAIL | 7 mismatches: 004–009 gold Gray vs SUT Red; 008 null; 013 Yellow vs Red |
| overall_accuracy | 17/23 | FAIL | follows 004–009 (overall Gray vs Red); 013/018 overall still Red |
| question_claim_support_precision | 7/9 | FAIL | 2 unsupported questions, both V323-013, allowed list empty |
| required_revision_concept_recall | 9/41 | FAIL | 12 `no-revision` empty-claim + 11 `preserve-intended-recipient` + squeeze + 013/018 |
| revision_claim_support_precision | 12/13 | FAIL | 1 unsupported revision, V323-013 placeholder |

Case pass in the scorer: **V323-017 only** (Scope, null ratings, empty required lists).

If empty `revision_claims` on a gold-`no-revision` Green turn counted as a hit, **V323-001, 002, 003, 014, 015, 016 would pass**. That is H-001, not a Skill miss. It is not applied retroactively.

T14.15 question-side effect is real: required question recall 3/6 → **6/6**. 004–009 all hit their required question concept, including the image-occluded measurement on 008.

## Attempt-2 seeds on this freeze

| seed | attempt-3 status |
| --- | --- |
| S-001 Data B as confirmed Data A | **Closed.** No Green self-verify on 004–009. Questions asked. |
| S-002 deferred unsafe commitment | **Narrowed, not closed.** 004/007/009 now placeholder in the same response. 005/006 still emit `Not provided — answer the questions above first` because Data A bars placeholders (G-002). 018 keeps a complete/refuse fork (S-007). |
| S-003 off-list questions on Red | **Recurs on V323-013 only.** |
| S-005 Gray vs Red on missing required token | **Do not carry forward as Skill.** SUT Red cites SPEC omission-defeats-purpose. Gold Gray fights SPEC §4. See G-001. |
| H-001 `no-revision` vs empty claims | **Recurs, 12/12 Green-control turns.** |
| H-002 Intake questions not extracted | **Partially closed.** 008 Intake question was extracted and matched. Route still fails. |
| H-003 implicit preserve facts | **Recurs.** `preserve-intended-recipient` missed 11 times; addressee `Orrin` is in the revision on 8 of those. |

## Classification

### Confirmed Skill defects

These are SUT behavior vs frozen gold **and** vs the T14.15 Skill/SPEC text. They may seed later Skill remediation. They must not rewrite this freeze.

1. `S-003 — Off-list questions on a Red accusation draft` (recurrence)
   - V323-013: gold `allowed_question_concepts` = `[]`. Required questions empty. Required revisions: strip hostility, strip unsupported sabotage accusation, keep Orrin.
   - SUT asked (1) whether Tamsin’s intent is confirmed and (2) what action Orrin should take. Matcher: both unsupported.
   - Gold facts already establish a normal dimension-check revision. The questions are not needed to revise.

2. `S-006 — Responsibility under-rate plus placeholder instead of stripping a hostile demand`
   - V323-013 gold Red/Red/Red: sabotage accusation contradicts Data A; `deal with her` is a hostile demand.
   - SUT Yellow/Red/Red: treated `deal with her` as vague handoff (responsibility Yellow) and the accusation as tone-only Red.
   - Revision replaced the sabotage sentence (hit `remove-unsupported-accusation`) then added `[State the specific action…]`. That claim is unsupported (`placeholder-unknown-value` not allowed). `remove-hostile-language` missed because the demand became a stub instead of disappearing.
   - This is the residual of S-002 on a tone-Red draft: complete the strip in-response, do not convert the hostile ask into a placeholder question.

3. `S-007 — Tone under-rate and complete/refuse fork on a signed-duty dump`
   - V323-018 gold Red/Red/Red. Readable image. Mercury dosing is Lise’s signed duty; Orrin countersigns; Coppervine Cycles is booked.
   - Draft refuses the dose, orders Orrin to do it, forbids a reminder, blames rostering.
   - SUT responsibility Red (match). Tone Yellow (dismissive / blame-shift) vs gold Red (open hostility).
   - Extra allowed question `commitment-scope`: will you finish before 16:00 or report unfinished? Precision holds because the concept is allowed; it is still an unnecessary question on a Red draft with confirmed ownership.
   - Revision is an A/B stub: complete before 16:00 **or** do not plan to complete / ask Orrin how to proceed. Matcher credited `correct-duty-owner` and `remove-duty-refusal`. Required `remove-hostile-language`, `remove-unsafe-commitment`, and `remove-unsupported-accusation` missed. The refuse-and-dump path remains in the revision.
   - T14.15 closed deferral for unestablished-authorization commitments. It did not close a signed-duty dump that is rewritten as a user-choice fork.

Do **not** Skill-remediate from G-001, G-002, G-003, or H-001/H-002/H-003.

### Gold quality (do not rewrite)

1. `G-001 — Question-candidate omissions gold-Gray vs SPEC omission-Red`
   - V323-004, 005, 006, 007, 009: gold Gray/Green/Gray. SUT Red/Green/Red.
   - Gold 004 rationale: the request “cannot succeed as written.” That is SPEC responsibility Red #5 (omission defeats main purpose when Data A requires the token before a named execution step).
   - SPEC also: “Do not use Gray merely because the requested value is unknown.” T14.15 Gray is for an **unconfirmed Data B-only token**, not for a draft that never answers a clear requirement.
   - SUT evidence quotes the omission-defeats-purpose test. Questions all hit. 004/007/009 also hit `placeholder-unknown-value`.
   - This is gold leniency against SPEC. **Do not remediate the Skill toward Gray on established omissions.** Attempt-2 S-005 was the same pattern; do not revive it.

2. `G-002 — 005/006 bar placeholders while requiring a revision body`
   - Data A on 005: deadline “must not be estimated or represented by a placeholder.” 006: collector name “must not be omitted or replaced with a placeholder.”
   - Gold required only `preserve-intended-recipient`. Allowed `include-confirmed-deadline` / `include-confirmed-collector-name` (SUT-invisible tokens). Placeholder is **not** allowed.
   - SUT asked the right question then `Not provided — answer the questions above first`. That follows the case constraint. It cannot include the token without invention, and it cannot placeholder without violating Data A.
   - Do not treat this as S-002. Do not teach the Skill to invent the hidden date/name.

3. `G-003 — Occluded Data B token gold-Normal vs Skill OCR intake`
   - V323-008: one geometrically obliterated required figure; everything else readable.
   - Gold: Normal mode, Gray, required `measured-cold-fill-pressure`.
   - Frozen REFERENCE: if a material token in **Data B** is not reliably legible, treat the new body as not identifiable, use intake, produce no ratings.
   - SUT Intake `Image confirmation`, asked for the occluded mbar field. Extractors recorded the question; recall hit. Route/ratings fail.
   - Gold explicitly rejected intake (“not a rating-blocking intake gap”). That fights T13.8 OCR. **Do not patch the Skill to rate an illegible Data B token.**

### Extraction / scoring contract (not Skill)

1. `H-001 — Required `no-revision` cannot be hit by empty claims`
   - Extraction: Green + “No revision needed” → `revision_claims = []`.
   - Scorer: required concepts ⊆ matched claim concepts.
   - 12 turns, ratings match, empty claims, required `{no-revision}` miss: V323-001, 002, 003, 014×3, 015×3, 016×3.
   - Zero over-revise of gold-Green controls (unlike V322-016 T1).
   - 12/41 of the recall denominator. Fixing this is a methodology change (new version + fresh holdout), not a rescore.

2. `H-002 — Intake questions can now extract; route still scores`
   - Unlike V322-008, V323-008’s Information-needed question was claimed and matched.
   - Remaining fail is G-003 route, not silent question extraction.

3. `H-003 — Implicit revision facts are required but not claimed`
   - `preserve-intended-recipient` missed 11 times. Revisions that exist still open `Orrin —` or `To: Orrin Medwick` on 004, 007, 009, 010, 011, 012, 013, 018. Extractors do not emit a “kept the addressee” claim.
   - 005, 006, 008 have no revision body, so they are G-002/G-003, not H-003.
   - `preserve-confirmed-owner` missed on 010, 011, 018 while `correct-duty-owner` / `remove-duty-refusal` consumed the only owner claims (one-claim-one-concept squeeze).
   - Same squeeze: V323-010 `remove-unsafe-commitment` (manager-does-the-splice is gone; matcher used `remove-duty-refusal`); V323-012 `remove-unsupported-accusation` (hostility claim ate the “you didn’t look / tinkering the roster” strip).

## Per-case

Ratings match unless noted. Revision miss lists are scorer misses, not necessarily Skill misses.

| case | family | ratings | questions | revision hits | revision misses | class |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | green-control | match Green | none | — | `no-revision` | H-001 |
| 002 | green-control | match Green | none | — | `no-revision` | H-001 |
| 003 | green-control | match Green | none | — | `no-revision` | H-001 |
| 004 | Q approval-authority | Gray→Red | hit | placeholder | recipient | G-001 + H-003 |
| 005 | Q confirmed-deadline | Gray→Red | hit | — | recipient (no body) | G-001 + G-002 |
| 006 | Q collector-name | Gray→Red | hit | — | recipient (no body) | G-001 + G-002 |
| 007 | Q cylinder-id | Gray→Red | hit | placeholder | recipient | G-001 + H-003 |
| 008 | Q occluded mbar | Normal/Gray → Intake/null | hit | — | recipient | G-003 |
| 009 | Q repair-path | Gray→Red | hit | placeholder | recipient | G-001 + H-003 |
| 010 | duty dump splice | match Red/Yellow/Red | none | duty-owner | owner, recipient, unsafe-commitment | H-003 squeeze |
| 011 | duty dump spark-test | match Red/Yellow/Red | none | duty-owner, accusation | owner, recipient | H-003 squeeze |
| 012 | tone insult | match Green/Red/Red | none | hostile-language | recipient, accusation | H-003 squeeze |
| 013 | sabotage accusation | Red→Yellow resp | 2 unsupported | accusation | recipient, hostile-language; 1 unsup rev | S-003, S-006 |
| 014 T1–T3 | three-turn | match Green | none | — | `no-revision` ×3 | H-001 |
| 015 T1–T3 | three-turn | match Green | none | — | `no-revision` ×3 | H-001 |
| 016 T1–T3 | three-turn | match Green | none | — | `no-revision` ×3 | H-001 |
| 017 | routing | match Scope | none | — | — | PASS |
| 018 | image duty+hostility | tone Red→Yellow | extra allowed `commitment-scope` | duty-owner | owner, recipient, hostile, unsafe, accusation | S-007 + H-003 |

## Counterfactuals (not applied)

Revision recall 9/41 = 0.220. Threshold ≥ 0.90 needs ≥ 37/41.

| if credited | hits | recall | still fail? |
| --- | ---: | ---: | --- |
| H-001 empty `no-revision` | 21/41 | 0.512 | yes |
| + H-003 recipient when Orrin kept (8) | 29/41 | 0.707 | yes |
| + squeeze owner/unsafe/accusation on 010–012 (4) | 33/41 | 0.805 | yes |
| + Skill 013/018 remaining required (6) | 39/41 | 0.951 | would pass recall only |

Responsibility 16/23: six of seven misses are G-001 (004–009) or G-003 (008). Skill-only responsibility miss is V323-013. Patching Skill toward gold Gray would raise the score and fight SPEC.

Tone already passes. Question recall already passes.

Headline 9/41 overstates Skill revision failure. After H-001+H-003 the residual Skill revision problem is 013 and 018.

## What this freeze must not cause

- No rescore of attempt 3, attempt 2, attempt 1, or v3.1.
- No gold rewrite.
- No Skill patch whose only job is to match gold Gray on 004–009.
- No Skill patch whose only job is to review V323-008 as Normal mode with a guessed or Gray-rated occluded Data B token.
- No merge of isolated designer / labeler / SUT / extractor / matcher branches.
