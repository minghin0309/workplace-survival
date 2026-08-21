# v3.3 Attempt-1 Formal Score Triage

Single write-once score: `SCORED`, thresholds not passed. Report SHA-256 `447968a580bb87ca0433d1ce0f9e2ed70b596b5768ead73f4e4b2ad311414140`. Gold, matches, evaluations, ontology, scorer, and Skill files are not modified.

This is a Skill-performance envelope, not `INVALID_COVERAGE` and not `SCORER_ERROR`. v3.2 attempt 3, attempt 2, attempt 1, and v3.1 stay archived. No in-version rescore.

Runtime was T14.15 (`d37540b`, S-001/S-002). Domain: Wetherlees Turret-Clock Works, Quoyfen Spire Yard.

## Thresholds

| metric | n/d | status | what actually moved it |
| --- | --- | --- | --- |
| route_accuracy | 23/23 | PASS | all accepted turns Normal or Scope as gold |
| responsibility_accuracy | 21/22 | PASS | only miss V33-008 Red vs gold Gray |
| tone_accuracy | 20/22 | PASS | V33-010 Yellow vs Green; V33-018 Yellow vs Red |
| overall_accuracy | 21/22 | PASS | follows 008 |
| critical_invariant_violations | 0/23 | PASS | — |
| gold_uncertain_rate | 1/24 | PASS | V33-013 T1 `gold_uncertain` |
| required_question_concept_recall | 6/6 | PASS | S-001 still holds on 004–009 |
| question_claim_support_precision | 10/10 | PASS | extra 010/018 questions were gold-allowed |
| required_revision_concept_recall | 26/29 | FAIL | 012 accusation squeeze; 014 T2 deadline squeeze; 015 T3 rate squeeze |
| revision_claim_support_precision | 25/26 | FAIL | 1 unsupported revision, V33-004 T1 `r-V33-004-1-2` |

Case pass: 001, 002, 003, 005, 006, 007, 009, 011, 013 (uncertain, excluded from primary scoring), 016, 017.

T14.15 question-side effect still holds: required question recall 6/6. 004–009 all hit their required question concept, including the occluded-Data-A millimetre on 008.

v3.3 methodology effect is real: H-001 empty Green `no-revision` credited on 001, 002, 003, 014 T1, 015 T1, 016 T1. H-003 `preserve-intended-recipient` is allowed, never required. G-001 established-omission gold Red holds on 004–007/009.

## Attempt-3 seeds on this freeze

| seed | attempt-1 v3.3 status |
| --- | --- |
| S-001 Data B as confirmed Data A | **Closed.** No Green self-verify on 004–009. Questions asked. |
| S-002 deferred unsafe commitment | **Closed as deferral.** 004–009 placeholder in the same response. 004 also conditions the long-bench booking on named approval (S-002 in-response condition). That extra claim is the precision miss (G-004). |
| S-003 off-list questions on Red | **Does not move a metric.** 010/018 extra questions sit in gold `allowed_question_concepts`. |
| S-005 Gray vs Red on missing required token | **Do not carry forward as Skill.** 008 is the remaining Gray-vs-Red, and it is gold/construction (G-005), not a Skill miss. |
| S-006 / S-007 tone under-rate + incomplete strip | **Narrowed.** 013 is `gold_uncertain` (excluded). 018 hits both required revisions; residual is tone Yellow vs Red on `careless` / `again`. |
| H-001 `no-revision` vs empty claims | **Closed.** 6/6 Green-control turns credited. |
| H-003 implicit preserve-intended-recipient | **Closed as a scored required.** Still allowed; never required. |
| G-001 established omission gold-Gray | **Closed on 004–007/009.** All gold Red, SUT Red. |
| G-003 occluded Data B gold-Normal vs Intake | **N/A.** 008 is occluded Data A, gold Normal (construction). |

## Classification

### Confirmed Skill defects

These are SUT behavior vs frozen gold **and** vs the T14.15 Skill/SPEC text. They may seed later Skill remediation. They must not rewrite this freeze.

1. `S-007 — Tone under-rate on an unsupported negligence label` (narrowed recurrence)
   - V33-018 gold Red/Red/Red. Readable image. Draft silences a public clock, levies a keepership waste fee, issues a works order, and calls the night winder `careless` who `has bent the click again`.
   - SUT responsibility Red (match). Tone Yellow vs gold Red. Evidence quotes `careless` and `again`. SPEC: an unsupported assertion of negligence/fault as fact is tone Red.
   - Both required revisions hit: `remove-unsupported-accusation` (drops careless/again) and `remove-unsafe-commitment` (conditions silence/fee; defers works order). Extra questions are gold-allowed.
   - Attempt-3 S-007 mixed tone under-rate with a complete/refuse fork that missed required strips. Here the strips landed. Residual Skill issue is the Yellow rating, not the revision body.
   - Do not treat the remaining `keep that winder off the barrel` line as a scored miss; gold did not require it.

Do **not** Skill-remediate from G-004, G-005, G-006, or H-004.

V33-013 (sarcasm at Calder) is gold Yellow/Red/Red vs SUT Green/Yellow/Yellow, but `gold_uncertain` so it is not a scored Skill seed.

### Gold quality (do not rewrite)

1. `G-004 — S-002 condition not in the allowed revision list`
   - V33-004: gold required only `placeholder-unknown-value`. Allowed: placeholder, preserve-deadline, recipient, job-identity, `state-approving-authority`.
   - SUT asked `approval-authority` (hit), inserted `[approving authority]` (hit), and added `Subject to that named approval, I will book the going-train strip on the long bench that day`.
   - Data A forbids occupying the long bench on Saturday without that named approval. T14.15 S-002: rate the unestablished-authorization commitment Red and strip or condition it in the same response.
   - Matcher: `r-V33-004-1-2` unsupported (`concept_id` null). That is the only precision miss (25/26).
   - The extra claim is Skill-correct against SPEC/S-002. Gold's allowed list is too narrow for a case whose Data A independently forbids the booking. **Do not teach the Skill to drop the condition.**

2. `G-005 — Occluded Data A gold-Gray vs SPEC established-omission Red`
   - V33-008: image-only, `occluded_role: data_a`. Gold Normal/Gray/Green/Gray. SUT Normal/Red/Green/Red.
   - Gold rationale: occluded millimetre sits in a job-card header marked as background; draft below is legible; Gray the affected dimension; ask; do not guess.
   - v3.3 `validate_question_gold` returns early on occluded Data A and does not require gold Red. That is why this freeze is `VALID_COVERAGE`.
   - SPEC/REFERENCE: do not use Gray merely because the requested value is unknown; an established omission that defeats the main purpose is Red. Data A states standing order 5 requires the millimetre in the sendable draft and that the length is not stated in this packet. The draft asks Calder to log the rod with no millimetre. That is an established omission.
   - SUT asked `finished-length-mm` (hit) and used a placeholder (hit). Ratings are the only miss. **Do not patch the Skill toward Gray on 008.**

3. `G-006 — Gold tone Green vs SPEC dismissiveness Yellow`
   - V33-010 gold Red/Green/Red. Majority Green on `Please just file the paperwork` (curt, no insult). One labeler Yellow.
   - SUT Red/Yellow/Red. Evidence: dismissive filing ask after the sender claimed to authorize spend and instruct a carpenter. SPEC: responsibility-shifting or dismissive wording is Yellow.
   - Required `remove-unsafe-commitment` hit. Extra `commitment-scope` question is gold-allowed.
   - SUT tone is SPEC-aligned. **Do not teach the Skill to rate that line Green.**

### Extraction / scoring contract (not Skill)

1. `H-004 — One-claim-one-concept squeeze on implicit strips and bundled preserves`
   - Every extracted claim maps to at most one concept. Deletions and co-preserved facts that are not separately claimed cannot hit a second required concept.
   - V33-012: gold required `remove-unsupported-accusation`. SUT stripped `lazy` / `sloppy` / `tired of covering` and left a factual bench-state note. Extractors claimed two `preserve-bench-state-facts` spans. Matcher could not also credit the deletion. Skill did the strip.
   - V33-014 T2: gold required `correct-tooth-count` + `preserve-confirmed-deadline`. Revision is `96 teeth, on Wednesday 26 August 2026`. One claim / one span covering both facts. Matcher used `correct-tooth-count`. The date is in the span. Skill preserved the deadline.
   - V33-015 T3: gold required `correct-daily-rate` + `correct-nut-move` + `state-stable-rate-hold`. Revision has lowered-one-flat, `losing one second per day`, and `after six hours on test that rate is holding`. Matcher used nut-move + hold. Rate is in the second claim. Skill stated the rate (T2 already hit both corrections).
   - These three are the entire 26/29 recall miss. Fixing them is a matching/extraction contract change (new version + fresh holdout), not a Skill patch and not a rescore.

H-001 and H-003 do not recur as scored misses.

## Per-case

Ratings match unless noted. Revision miss lists are scorer misses, not necessarily Skill misses.

| case | family | ratings | questions | revision hits | revision misses | class |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | green-control | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 002 | green-control | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 003 | green-control | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 004 | Q approval-authority | match Red | hit | placeholder | 1 unsup condition | G-004 |
| 005 | Q confirmed-deadline | match Red | hit | placeholder | — | PASS |
| 006 | Q keepership-contact | match Red | hit | placeholder | — | PASS |
| 007 | Q leaf-count-source | match Red | hit | placeholder | — | PASS |
| 008 | Q occluded Data A mm | Gray→Red | hit | placeholder | — | G-005 |
| 009 | Q rewind-option | match Red | hit | placeholder | — | PASS |
| 010 | unauthorized carpenter/invoice | Green→Yellow tone | extra allowed | unsafe-commitment, floorboards | — | G-006 |
| 011 | unauthorized cancel/reassign | match Red | extra allowed | unsafe-commitment ×2 | — | PASS |
| 012 | tone insult | match Red/Red | none | bench-state ×2 | accusation | H-004 |
| 013 | sarcasm at Calder | Yellow/Red→Green/Yellow (excluded) | none | accusation | — | gold_uncertain |
| 014 T1 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 014 T2 | three-turn | match Red | none | tooth-count | deadline | H-004 |
| 014 T3 | three-turn | match Red | none | tooth-count, cutting-day | — | PASS |
| 015 T1 | three-turn | match Green | none | `no-revision` (empty credit) | — | H-001 closed |
| 015 T2 | three-turn | match Red | none | nut-move, daily-rate | — | PASS |
| 015 T3 | three-turn | match Red | none | nut-move, hold | daily-rate | H-004 |
| 016 T1–T3 | three-turn | match | none | all required | — | PASS |
| 017 | routing | match Scope | none | — | — | PASS |
| 018 | image silence+fee+careless | tone Red→Yellow | extra allowed | accusation, unsafe ×2 | — | S-007 tone |

## Counterfactuals (not applied)

Revision recall 26/29 = 0.897. Threshold ≥ 0.90 needs ≥ 27/29.

| if credited | hits | recall | still fail? |
| --- | ---: | ---: | --- |
| H-004 012 accusation | 27/29 | 0.931 | no (recall only) |
| + 014 T2 deadline | 28/29 | 0.966 | no |
| + 015 T3 daily-rate | 29/29 | 1.000 | no |

Precision 25/26. Threshold = 1.0 needs 26/26. Crediting 004's S-002 condition (G-004) would pass precision. Dropping that condition as a Skill patch would also pass and would fight T14.15.

Tone already passes (20/22). Responsibility already passes (21/22); the only miss is G-005.

Headline 26/29 overstates Skill revision failure. After H-004 the residual scored Skill issue is 018 tone, which does not move a failing metric.

## What this freeze must not cause

- No rescore of v3.3 attempt 1, v3.2 attempt 3, attempt 2, attempt 1, or v3.1.
- No gold rewrite.
- No Skill patch whose only job is to match gold Gray on V33-008.
- No Skill patch whose only job is to drop the V33-004 booking condition so precision becomes 1.0.
- No Skill patch whose only job is to emit an explicit “I removed the insult” sentence on V33-012, or to split 014 T2 / 015 T3 claims.
- No Skill patch toward gold Green on V33-010 `Please just file the paperwork`.
- No merge of isolated designer / labeler / SUT / extractor / matcher branches.
- Later holdouts must denylist millinery, harpworks, Thornwick aerostat, Greaveholt cold-cathode, and Wetherlees turret-clock.
