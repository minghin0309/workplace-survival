# v3.2 Attempt-2 Formal Score Triage

Single write-once score: `SCORED`, thresholds not passed. Report SHA-256 `3b646bac33b84ec798eb53e779b716237fb7fa0cd1fdcc532a7f0ef93593cc03`. Gold, matches, evaluations, ontology, scorer, and Skill files are not modified.

This is a Skill-performance envelope, not `INVALID_COVERAGE` and not `SCORER_ERROR`. Attempt 1 and v3.1 stay archived. No in-version rescore.

## Thresholds

| metric | n/d | status | what actually moved it |
| --- | --- | --- | --- |
| route_accuracy | 24/24 | PASS | — |
| tone_accuracy | 21/22 | PASS | V322-010 Green→Yellow only |
| critical_invariant_violations | 0/24 | PASS | — |
| gold_uncertain_rate | 0/24 | PASS | all 24 turns `heterogeneous_adjudicated` |
| responsibility_accuracy | 15/22 | FAIL | 7 mismatches; see S-\* and G-001 |
| overall_accuracy | 16/22 | FAIL | follows responsibility except V322-010 (tone) and V322-013 (overall still Red) |
| required_question_concept_recall | 3/6 | FAIL | 005, 006 Skill; 008 extraction |
| question_claim_support_precision | 4/7 | FAIL | 3 unsupported questions, all off gold allowed-list |
| required_revision_concept_recall | 11/41 | FAIL | mixed Skill / `no-revision` scoring gap / implicit facts |
| revision_claim_support_precision | 21/24 | FAIL | 3 unsupported revisions |

Case pass in the scorer: **V322-017 only** (Scope, null ratings, empty required lists).

If empty `revision_claims` on a gold-`no-revision` Green turn counted as a hit, **V322-001, V322-003, V322-014, V322-015 would pass**. That is a scoring-contract gap, not a Skill miss. It is not applied retroactively.

## Classification

### Confirmed Skill defects

These are SUT behavior vs frozen gold. They may seed later Skill remediation. They must not rewrite this freeze.

1. `S-001 — Data B treated as confirmed Data A`
   - V322-005: Data A has a notebook date, not `26 August 2026`. Gold Gray + required `confirmed-deadline`. SUT Green, no question, “Data A contains no conflicting date.”
   - V322-006: Data A has a notebook owner name, not `Bram Cotrell`. Gold Gray + required `confirmed-owner`. SUT Green, no question.
   - Direct Skill-rule miss: Data B must not verify itself; unknown required values stay questions/placeholders.

2. `S-002 — Unauthorized commitment rated Gray and revision deferred`
   - V322-004: draft asserts authority and “I will tell Pellwick … agreed.” Gold Red + required `remove-unsafe-commitment`. SUT asked `approval-authority` (hit) then Gray / “Not provided — answer the questions above first.”
   - Question was right. Leaving the send-to-client commitment in place until the locker note is quoted is the miss.

3. `S-003 — Off-list questions on Red drafts`
   - V322-012: gold `allowed_question_concepts` = `{current-root-cause}` only; required questions empty. SUT asked what action Saira should take and what “or I will” means.
   - V322-013: gold `allowed_question_concepts` = `[]`. SUT asked complete-vs-attempt. Responsibility gold Red, SUT Yellow.

4. `S-004 — Over-revision of a gold-Green first attribution`
   - V322-016 T1: gold Green + required `no-revision` (later turns replace the line). SUT Yellow, asked `complete-work-attribution` (allowed, not required), wrote placeholders. Those two revision claims are unsupported because the only allowed revision concept is `no-revision`.
   - T2/T3 ratings match Green; they fail only the `no-revision` empty-claim gap (H-001).

5. `S-005 — Gray vs Red calibration on a named-document constraint`
   - V322-007: gold Gray (unnamed bench-drawer paper). SUT Red, asked `source-document-name` (hit), placeholder revision (hit `placeholder-unknown-value`). Over-rate, not a question miss.

6. `S-006 — Conditional revision instead of placeholder (ratings already Gray)`
   - V322-009: ratings match. Required `placeholder-unknown-value` + `preserve-intended-recipient`. SUT asked `permitted-repair-path` (hit) then wrote an if-listed / else-select revision, matched only to `remove-unsafe-commitment`.

### Gold quality (do not rewrite)

1. `G-001 — V322-002 gold Green vs Data A “staging confirmation only”`
   - Constraint: keep the note to a staging confirmation; do not change the staged lot.
   - Draft adds TW-508 10:00 and “if you want a different staging bay.”
   - Gold Green + required `no-revision`, but **allows** `remove-staging-change-offer`.
   - SUT Red and stripped the extras (allowed concepts, so precision holds).
   - This is gold leniency against its own constraint. **Do not remediate the Skill toward leaving that extra scope.**

### Extraction / scoring contract (not Skill)

1. `H-001 — Required `no-revision` cannot be hit by empty claims`
   - Extraction brief: “No revision needed yields `[]`.”
   - Scorer: required concepts ⊆ matched claim concepts.
   - 10 turns where SUT correctly emitted no revision still miss: V322-001, 003, 014×3, 015×3, 016 T2, 016 T3.
   - Plus Skill over-revise misses of `no-revision`: 002, 016 T1.
   - Fixing this is a methodology change (new version + fresh holdout), not a rescore.

2. `H-002 — Intake questions are not `question_claims``
   - V322-008 route Intake matches gold. SUT asked for the occluded finished-length figure under Information needed. Gold required `measured-finished-length`. Extractors recorded 0 question claims (Confirmation needed only). **Skill asked; recall still 0.**

3. `H-003 — Implicit revision facts are required but not claimed`
   - `preserve-intended-recipient` missed 9 times. Revisions still open `Saira —`. Extractors do not emit a “kept the addressee” claim.
   - V322-018 required `remove-hostile-language` and `remove-unsupported-accusation`. The frozen revision is already a factual mouth-tape note with no insult or false promise; extractors claimed the remaining sentences (`preserve-factual-mouth-tape-update`, `remove-unsafe-commitment`, `restore-manager-certificate-authority`).
   - Same one-claim-one-concept squeeze: V322-013’s single revision both strips competence jokes and keeps noon timing; matcher took `preserve-stock-count-timing`, so `remove-hostile-language` recall misses even though the jokes are gone.

4. `H-004 — `placeholder-unknown-value` omitted from V322-012 allowed revisions`
   - SUT inserted `[specific action you want Saira to take…]`. Matcher correctly marked unsupported: that concept is not in the turn’s allowed list. Candidate gold under-allow, not a matcher error. Frozen.

### Matcher

No matcher defect. `gold_access` true, family `claude`, not a gold labeler family.

- 25 semantic, 0 exact/alias (`text` never equals `evidence_span`).
- All 6 unsupported decisions match empty or non-covering allowed lists (012×3, 013 q, 016 T1×2).
- Dual readings recorded in rationales; one claim → one concept as the scorer requires.

### Harness

None. Freeze chain validated. Envelope is `SCORED`. Invariants 0.

## Rating mismatches (7 responsibility + 1 tone)

| case | gold R/T/O | SUT R/T/O | class |
| --- | --- | --- | --- |
| V322-002 | G/G/G | R/G/R | G-001 |
| V322-004 | R/G/R | Gray/G/Gray | S-002 |
| V322-005 | Gray/G/Gray | G/G/G | S-001 |
| V322-006 | Gray/G/Gray | G/G/G | S-001 |
| V322-007 | Gray/G/Gray | R/G/R | S-005 |
| V322-010 | R/G/R | R/Y/R | Skill tone false Yellow (weak; draft “You do not need to get involved”) |
| V322-013 | R/R/R | Y/R/R | S-003 |
| V322-016 T1 | G/G/G | Y/G/Y | S-004 |

## Required-question misses

| case | required | SUT | class |
| --- | --- | --- | --- |
| V322-005 | `confirmed-deadline` | none | S-001 |
| V322-006 | `confirmed-owner` | none | S-001 |
| V322-008 | `measured-finished-length` | Intake asked the occluded figure | H-002 |
| V322-004 | `approval-authority` | hit | — |
| V322-007 | `source-document-name` | hit | — |
| V322-009 | `permitted-repair-path` | hit | — |

## Unsupported claims (precision)

| claim | why unsupported | class |
| --- | --- | --- |
| q-V322-012-1-1, q-V322-012-1-2 | allowed only `current-root-cause` | S-003 |
| r-V322-012-1-5 | `placeholder-unknown-value` not allowed | H-004 |
| q-V322-013-1-1 | `allowed_question_concepts` empty | S-003 |
| r-V322-016-1-1, r-V322-016-1-2 | allowed only `no-revision` | S-004 |

## What may start Skill work

Start from **S-001 and S-002 only** (Data B as evidence; unauthorized client/authority commitments left standing).

Do not start from:

- H-001–H-003 (claim/recall contract);
- G-001 (gold vs staging constraint);
- V322-008 (Intake already asked);
- V322-018 hostile/accusation recall (revision already cleaned);
- this freeze’s gold, matches, or a second `score_semantic_v3_2.py` run.

A Skill change is a product change. It needs a new unseen holdout (new domain; millinery / harpworks / Thornwick aerostat denylisted). This parent has seen those golds and must not author cases.

## Failed / passed cases

- Passed: V322-017.
- Failed only via H-001: V322-001, V322-003, V322-014, V322-015.
- Failed with Skill or mixed causes: the rest.
- Unscored: none.

## Limitations

- Human review was not available (`human_review_available: false`).
- Matcher was a single Claude context.
- Extractor-1 read `SKILL.md` off-allowlist; claims were not rewritten on copy.
- Triage reads frozen gold after unblinding. It does not change labels.
