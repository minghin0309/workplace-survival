# Workplace Survival — Active Tasks

`TASK.md` is an active queue, not a product specification or completed-work archive.

## Working rules

- Product behavior starts in `SPEC.md`.
- Runtime changes go only to the file that owns the affected rule, as defined in `ARCHITECTURE.md`.
- Do not repeat full product or runtime rules in a task.
- A task is complete only when its acceptance conditions pass and evidence is recorded in the applicable test result file.
- Keep completed items checked in the current phase so progress stays visible; also summarize completed outcomes in `CHANGELOG.md`. Archive the phase after every item is complete.
- Use each task's checkbox as the visible status: `[ ]` means pending and `[x]` means completed.

## Current queue

Complete tasks in numerical order. T13.1–T13.3 must be rebuilt because their earlier workspace changes were never committed.

### Priority 1 — Source and content boundaries

#### T13.1 — Separate sendable body from embedded content

- [x] Completed

- Source requirement: `SPEC.md` section 3, `Embedded content in Data B`.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, `.cursor/skills/workplace-survival/FORMATS.md`, and `tests/TEST_CASES.md`.
- Acceptance:
  - only the identifiable sendable body is rated and revised;
  - quoted, forwarded, reply-header, and nested content does not become Data A solely because it appears inside Data B;
  - unclear boundaries stop assessment and request classification.
- Tests: blockquote, email reply, forwarded message, chat quote, and malformed boundary cases.
- Evidence: functional and anti-hallucination results.

#### T13.2 — Classify mixed unlabelled input safely

- [x] Completed

- Source requirement: `SPEC.md` sections 3 and 5, mixed-input classification and provenance disclosure.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, `.cursor/skills/workplace-survival/FORMATS.md`, and `tests/TEST_CASES.md`.
- Acceptance:
  - auto-classification requires explicit semantic boundaries for both A and B;
  - adopted A and evaluated B are disclosed;
  - multiple plausible classifications produce intake output without ratings.
- Tests: clear semantic labels, unlabelled paragraphs, multi-person dialogue, and multiple draft candidates.
- Evidence: functional results.

#### T13.3 — Replace superseded Data A

- [x] Completed

- Source requirement: `SPEC.md` section 4, `Effective Data A`.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, and `tests/TEST_CASES.md`.
- Acceptance:
  - explicit correction replaces the targeted old value;
  - explicit withdrawal or cancellation removes the targeted requirement;
  - superseded facts no longer affect ratings, questions, revisions, or placeholders.
- Tests: withdrawn deadline, corrected owner, and cancelled request as multi-round cases.
- Evidence: functional and anti-hallucination results.

### Priority 2 — Rating boundaries

#### T13.4 — Fix Tone Yellow and Red boundaries

- [x] Completed

- Source requirement: `SPEC.md` section 4.
- Owner files: `.cursor/skills/workplace-survival/REFERENCE.md` and `tests/TEST_CASES.md`; update `SPEC.md` first only if the product contract changes.
- Acceptance:
  - directness, ambiguity, responsibility shifting, accusation, insult, hostility, and threat have operational boundaries;
  - responsibility and tone remain independent;
  - similar safe control, Yellow, and Red phrases produce stable paired outcomes.
- Tests: paired Tone Yellow and Red cases with similar Green controls, covering the current missing non-Green tone assertions.
- Evidence: functional and interaction-quality results.

#### T13.5 — Fix responsibility Red and Gray boundaries

- [x] Completed

- Source requirement: `SPEC.md` section 4.
- Owner files: `.cursor/skills/workplace-survival/REFERENCE.md` and `tests/TEST_CASES.md`; update `SPEC.md` first only if the product contract changes.
- Acceptance:
  - an explicit unanswered requirement that defeats the reply's purpose is Red;
  - Gray is reserved for genuinely missing or materially ambiguous governing information;
  - omission cases have fixed dimension and overall ratings.
- Tests: explicit requirement, non-mandatory suggestion, and ambiguous request pairs.
- Evidence: functional results.

#### T13.6 — Bound short acknowledgements to one reply target

- [x] Completed

- Source requirement: `SPEC.md` section 4.
- Owner files: `.cursor/skills/workplace-survival/REFERENCE.md` and `tests/TEST_CASES.md`.
- Acceptance:
  - the acknowledgement target is identifiable, clear, and non-conflicting;
  - qualified, refusing, modifying, or limiting replies do not use the Green shortcut;
  - unclear multi-message targets remain Gray pending confirmation.
- Tests: multi-message, conflicting instruction, negative instruction, and qualified acknowledgement cases.
- Evidence: functional results.

### Priority 3 — Adversarial, image, and mode coverage

#### T13.7 — Isolate prompt-like text inside case data

- [x] Completed

- Source requirement: `SPEC.md` section 4, `Evidence and isolation`.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, `tests/TEST_CASES.md`, `tests/fixtures/generate_fixtures.py`, the generated prompt-like image fixture, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - instructions embedded in Data A, Data B, images, or quotes remain content under analysis;
  - embedded text cannot bypass formats, evidence rules, or ratings;
  - relevant embedded wording may still be cited as communication evidence.
- Tests: text and image prompt-like instruction cases.
- Evidence: anti-hallucination and functional results.

#### T13.8 — Protect material OCR boundaries

- [x] Completed

- Source requirement: `SPEC.md` section 4.
- Owner files: `.cursor/skills/workplace-survival/REFERENCE.md`, `tests/fixtures/generate_fixtures.py`, generated image fixtures, `tests/TEST_CASES.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - uncertain names, dates, numbers, negations, and commitment words require confirmation;
  - materially uncertain conversation order or requirement source is not inferred;
  - no color rating is based on a guessed material token.
- Tests: negation, similar dates, low-contrast names, strikethrough, cropping, and group-chat order.
- Evidence: fresh image executions recorded separately from semantic checks.

#### T13.9 — Cover limited-background, multi-message, and template boundaries

- [x] Completed

- Source requirement: `SPEC.md` sections 3–5.
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/SKILL.md`, `.cursor/skills/workplace-survival/REFERENCE.md`, `.cursor/skills/workplace-survival/FORMATS.md`, and `tests/TEST_CASES.md`.
- Acceptance:
  - limited-background cases cover internal responsibility, timing, and hostile tone;
  - unrelated work items requiring different Data A are split;
  - template mode without Data A returns a generic neutral template with placeholders and no ratings;
  - recipient role is not assumed from workplace convention.
- Tests: multi-message, no-background template, mentor, skip-level, HR, customer, and reply-all cases.
- Evidence: functional and interaction-quality results.

### Priority 4 — Reproducibility and acceptance

#### T13.10 — Preserve auditable test evidence

- [x] Completed

- Source requirement: Engineering evidence gap — `SPEC.md` section 7 requires passing suites, while current result files do not preserve enough execution evidence to reproduce every PASS. No product behavior change.
- Owner files: existing suite files matching `tests/*_RESULTS.md`, `tests/evidence/`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - each execution records input, model, execution time, raw output, and assertion outcome;
  - automated, manual semantic, image-attached, and environment-limited checks are distinguished;
  - PASS is never recorded without reviewable evidence.
- Tests: validate the result record for every active suite.
- Evidence: suite result files.

#### T13.11 — Add repeat and variation testing

- [x] Completed

- Source requirement: Engineering consistency gap — current high-risk cases have no repeated-run stability requirement. No product behavior change.
- Owner files: `tests/TEST_CASES.md`, `tests/TEST_RESULTS.md`, `tests/evidence/`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - high-risk cases run at least three times;
  - mode, both ratings, overall status, question count, and revision facts are compared;
  - any material output variation fails the consistency check.
- Tests: repeated high-risk cases and paired boundary variants.
- Evidence: consistency matrix in the result files.

#### T13.12 — Re-run final acceptance accurately

- [x] Completed

- Source requirement: `SPEC.md` section 7 acceptance requirement plus the evidence and consistency gaps tracked by T13.10–T13.11.
- Owner files: all suite case/result files, `tests/evidence/`, `tests/FINAL_ACCEPTANCE_RESULTS.md`, `CHANGELOG.md`, `README.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - functional, anti-hallucination, interaction-quality, explicit-invocation, and auto-trigger suites are rerun;
  - case pass rate and repeat-run consistency are reported separately;
  - semantic image checks are not described as fresh image executions;
  - publication and installation claims match actual evidence.
- Tests: all suites after T13.1–T13.11.
- Evidence: final acceptance report.

### Phase 14 — Independent test-strength validation

#### T14.1 — Mutation testing

- [x] Completed

- Source requirement: Test-quality follow-up after T13 final acceptance; no product behavior change.
- Owner files: `tests/mutation/`, surviving-mutant regression cases, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - each mutant changes one observable rule in an isolated worktree;
  - system output generation cannot read test expectations;
  - every non-equivalent survivor becomes a regression test;
  - mutation score and method limitations are recorded;
  - no mutant is merged into the baseline runtime.
- Evidence: mutation plan, raw outputs, mutant diffs, and final mutation report.

#### T14.2 — Cloud-isolated blind holdout testing

- [x] Completed

- Source requirement: Independent accuracy follow-up after mutation testing; no product behavior change during scoring.
- Owner files: `tests/blind/`, `TASK.md`, `CHANGELOG.md`, `README.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - unseen cases are generated in a cloud branch without prior holdout artifacts;
  - heterogeneous gold labels are frozen before Skill output generation;
  - Skill output generators cannot read gold labels or scoring thresholds;
  - cases, gold, runtime, raw outputs, and images are hash-linked;
  - critical invariant, route, rating, question, and revision metrics are reported;
  - failures are preserved before any product or test change.
- Evidence: cloud agent branch, frozen artifacts, raw outputs, adjudication, score report, and method limitations.

#### T14.3 — Blind defect remediation

- [x] Completed

- Source requirement: Confirmed product defects from the cloud blind diagnostic.
- Owner files: `SPEC.md`, runtime Skill files, public regression cases, and `tests/blind/remediation/`.
- Acceptance:
  - all 18 diagnostic cases are re-triaged before product changes;
  - benchmark/gold ambiguities do not become production rules;
  - confirmed defects receive generalized rules and public regressions;
  - existing functional and targeted suites do not regress;
  - each remediation rule is protected by a killed mutant.
- Evidence: triage, regression summary, remediation mutant diffs, raw outputs, and oracle results.

#### T14.4 — Evidence-complete remediation acceptance

- [x] Completed

- Source requirement: Validate remediation runtime with the T13.10 evidence contract before merging to `main`.
- Owner files: suite result files, `tests/evidence/`, remediation reports, `README.md`, `CHANGELOG.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - Functional TC-01–TC-114 and every active targeted suite are rerun;
  - all 13 image cases are opened and hash-linked;
  - every PASS has raw input/output, assertions, runtime commit, and exact result citation;
  - package validation is reported separately from behavioral cases;
  - summary-only remediation results are replaced by evidence-complete current results.
- Evidence: remediation acceptance plan, full evidence JSON, package record, validator output, and updated acceptance report.

#### T14.5 — Blind benchmark methodology v2

- [x] Completed

- Source requirement: Separate benchmark/scoring defects from product behavior before a new hidden holdout.
- Owner files: `tests/benchmark/`, `TASK.md`, `CHANGELOG.md`, `README.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - SUT-visible Data A is explicit and evaluator-only notes cannot affect gold;
  - question and revision claims use ontology/semantic matching rather than exact token equality;
  - gold disagreement, adjudication, uncertainty, and optional human review are represented;
  - cloud cases, images, gold, outputs, and evaluations are content-addressed and immutable;
  - scorer rejects unsupported claims, missing required concepts, changed artifacts, and excessive gold uncertainty;
  - methodology tests and negative gates pass without changing runtime Skill files.
- Evidence: methodology contract, ontology, validators/scorer, synthetic fixtures, unit results, and runtime diff check.

#### T14.6 — Fresh benchmark v2 cloud holdout

- [ ] Completed

- Source requirement: Measure post-remediation unseen-case performance with methodology v2.
- Owner files: `tests/benchmark/v2-holdout/`, benchmark result summaries, `TASK.md`, `CHANGELOG.md`, `README.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - runtime is frozen at `main@9d48b04`;
  - unseen cases contain explicit SUT-visible Data A and separate oracle notes;
  - heterogeneous gold and cloud artifacts satisfy methodology v2;
  - each case uses an independent cloud SUT context;
  - dual extraction and semantic matching precede scoring;
  - preregistered metrics and failures are preserved without modifying gold.
- Evidence: frozen manifests, cases/images, labels/adjudication, raw outputs, matches, score report, and cloud attestations.

#### T14.7 — Benchmark methodology v3 scorer hardening

- [x] Completed

- Source requirement: Preserve the v2 `SCORER_ERROR` outcome and prevent zero-denominator metrics or scorer exceptions from destroying formal evidence. No product behavior change.
- Owner files: `tests/benchmark/v3/`, `TASK.md`, `CHANGELOG.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - v2 remains archived and is never rescored;
  - zero denominators produce `NOT_APPLICABLE`, never 0, 1, or an exception;
  - preregistered coverage gates reject holdouts without question and revision coverage before SUT execution;
  - every scorer invocation writes one immutable success or failure envelope;
  - unit and mutation tests kill zero-denominator, disabled-coverage, and missing-failure-envelope defects;
  - validation uses synthetic fixtures and does not supply v2 artifacts to the v3 scorer.
- Evidence: v3 methodology contract, unit results, mutation results, validation report, and empty runtime diff.

#### T14.8 — Fresh benchmark v3 unseen holdout

- [x] Completed

- Source requirement: Exercise methodology v3 on a fresh unseen case set and enforce coverage before SUT execution.
- Owner files: `tests/benchmark/v3-holdout/`, `TASK.md`, and `CHANGELOG.md`.
- Acceptance:
  - cases and images are generated in an isolated cloud context without prior benchmark content;
  - three independent gold families and a fourth-family adjudicator preserve all votes;
  - v3 question/revision coverage gates execute before SUT;
  - invalid coverage prevents SUT, extraction, matching, and formal scoring;
  - the complete invalid-coverage evidence chain is immutable.
- Evidence: holdout plan/brief, cases/images, labels/adjudication, transcript audits, coverage report, result summary, and invalid-coverage manifest.

#### T14.9 — v3.1 required-question case-design remediation

- [x] Completed

- Source requirement: Correct the benchmark-design cause of v3 `INVALID_COVERAGE` without changing frozen v3 cases or gold.
- Owner files: `tests/benchmark/v3_1/`, `TASK.md`, `CHANGELOG.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - the invalid v3 holdout remains immutable and no case content is reused;
  - six distinct question candidates are overprovisioned;
  - placeholder, qualification, omission, and dominant-Red escape routes reject a candidate;
  - removing dependency or supplying the answer removes question necessity;
  - unit and mutation tests protect every construction transition.
- Evidence: coverage triage, v3.1 case brief, executable contract, unit results, and mutation results.

#### T14.10 — Fresh benchmark v3.1 unseen holdout

- [x] Completed

- Source requirement: Measure unseen-case performance with methodology v3 plus the v3.1 question-case construction contract. No product behavior change during scoring.
- Owner files: `tests/benchmark/v3_1-holdout/`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - unseen millinery-domain cases satisfy the v3.1 construction contract and coverage gates before SUT;
  - each case uses a distinct cloud SUT context;
  - SUT artifacts are extracted from per-case source commits; shared-holdout delivery commits are a log, not the freeze parent;
  - dual extraction and semantic matching precede a single v3 scorer invocation;
  - preregistered metrics and failures are preserved without modifying gold or runtime Skill files.
- Evidence: gold/output manifests, protocol audits, source index, delivery log, score report.
- Progress: archived as `SCORER_ERROR` after one v3 scorer invocation (`manifest schema`); not rerun.

#### T14.11 — Benchmark methodology v3.2 freeze-chain scoring

- [x] Completed

- Source requirement: Preserve the v3.1 `SCORER_ERROR` outcome and score v3.1-compatible freeze documents without requiring a v2 exact-key manifest. Gold freeze must include ontology. No product behavior change.
- Owner files: `tests/benchmark/v3_2/`, `TASK.md`, `CHANGELOG.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - v3.1 remains archived and is never rescored;
  - extra freeze-document keys are allowed and `version` `3.1`/`3.2` is accepted;
  - a gold freeze without `ontology` is `INVALID_SCORING_INPUT`;
  - v2 manifests are rejected;
  - zero denominators remain `NOT_APPLICABLE`;
  - every scorer invocation writes one immutable success or failure envelope;
  - unit and mutation tests kill extra-key rejection, optional-ontology, and missing-envelope defects;
  - validation uses synthetic fixtures and does not supply v2/v3.1 holdout artifacts.
- Evidence: v3.2 methodology contract, unit results, mutation results, validation report, and empty runtime diff.

#### T14.12 — Fresh benchmark v3.2 unseen holdout

- [x] Completed

- Source requirement: Measure unseen-case performance with methodology v3.2. Gold freeze must include ontology and the v3.2 scorer. No product behavior change during scoring.
- Owner files: `tests/benchmark/v3_2-holdout/`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - unseen cases use a domain that is not millinery and is not on the v3.1 denylist;
  - cases satisfy the v3.1 construction contract and coverage gates before SUT;
  - gold freeze includes `SEMANTIC_ONTOLOGY.json` and `score_semantic_v3_2.py`;
  - each case uses a distinct cloud SUT context;
  - dual extraction and semantic matching precede a single v3.2 scorer invocation;
  - v3.1 is not rescored and runtime Skill files are not modified.
- Evidence: gold/output/evaluation manifests, protocol audits, and one v3.2 score report.
- Progress: archived as `INVALID_COVERAGE` after gold freeze; SUT and the v3.2 scorer were not invoked. Question candidates used non-manager recipients and gold-routed `Scope`. Gold was not rewritten.

#### T14.13 — v3.2 manager-recipient case-design remediation

- [x] Completed

- Source requirement: Correct the benchmark-design cause of v3.2 `INVALID_COVERAGE` without changing frozen attempt-1 cases or gold.
- Owner files: `tests/benchmark/v3_2/`, `TASK.md`, `CHANGELOG.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - the invalid v3.2 attempt-1 holdout remains immutable and no case content is reused;
  - exactly one non-manager recipient is allowed and it is the routing case;
  - question candidates cannot be Scope-routed by construction;
  - a role without a `manager` token fails the gate;
  - unit and mutation tests kill routing-as-question, non-manager question candidates, and manager-token-optional defects;
  - validation uses synthetic fixtures plus the frozen attempt-1 envelope as a negative fixture.
- Evidence: coverage triage, attempt-2 case brief, executable contract, unit results, and mutation results.

#### T14.14 — Fresh benchmark v3.2 unseen holdout attempt 2

- [x] Completed

- Source requirement: Measure unseen-case performance with methodology v3.2 plus the manager-recipient construction contract. No product behavior change during scoring.
- Owner files: `tests/benchmark/v3_2-holdout/attempt-2/`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - unseen cases use a domain that is not millinery, harpworks, or any denylisted prior domain;
  - every case except the routing case is a manager recipient;
  - cases satisfy the v3.1 question-candidate contract and coverage gates before SUT;
  - gold freeze includes `SEMANTIC_ONTOLOGY.json` and `score_semantic_v3_2.py`;
  - each case uses a distinct cloud SUT context;
  - dual extraction and semantic matching precede a single v3.2 scorer invocation;
  - v3.1 and v3.2 attempt 1 are not rescored; runtime Skill files are not modified.
- Evidence: gold/output/evaluation manifests, protocol audits, and one v3.2 score report.
- Progress: archived as `SCORED` with thresholds not passed. Triage is `tests/benchmark/v3_2-holdout/attempt-2/SCORE_TRIAGE.md` on `cursor/blind-v322-holdout-17a0`. Freeze is not rescored.

#### T14.15 — S-001/S-002 Skill remediation

- [x] Completed

- Source requirement: `SPEC.md` Data B and ratings. Attempt-2 triage S-001 (Data B as confirmed Data A) and S-002 (unauthorized commitment deferred).
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/`, `tests/TEST_CASES.md`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - an off-record governing token that Data A does not quote is Gray plus a question, not Green, when it appears only in Data B;
  - TC-07 still treats a manager-requested value stated in Data B as an answer when no off-record source exists;
  - an unestablished authorization plus an external client/authority commitment is Red and is stripped in the same response;
  - v3.2 attempt 2 is not rescored and its gold is not rewritten.
- Tests: TC-115, TC-116, TC-117; TC-07 must still pass.
- Evidence: functional results for the new cases.

#### T14.16 — Fresh benchmark v3.2 unseen holdout attempt 3

- [x] Completed

- Source requirement: Measure unseen-case performance after T14.15 on methodology v3.2. No in-version rescore of attempt 2.
- Owner files: `tests/benchmark/v3_2-holdout/attempt-3/`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - unseen cases use a domain that is not millinery, harpworks, Thornwick aerostat, or any denylisted prior domain;
  - every case except the routing case is a manager recipient;
  - cases satisfy the v3.1 question-candidate contract, manager-recipient contract, and coverage gates before SUT;
  - gold freeze includes `SEMANTIC_ONTOLOGY.json` and `score_semantic_v3_2.py`;
  - each case uses a distinct cloud SUT context against the T14.15 runtime;
  - dual extraction and semantic matching precede a single v3.2 scorer invocation;
  - v3.1, v3.2 attempt 1, and v3.2 attempt 2 are not rescored.
- Evidence: gold/output/evaluation manifests, protocol audits, and one v3.2 score report.
- Progress: archived as `SCORED` with thresholds not passed. Report SHA-256 `4f9a30bc01f6e419a4cc173f3a1f49bb19feb5ce8206ef2bbeb852ddabe1c834`. Attempt 2 is not rescored. Triage is `tests/benchmark/v3_2-holdout/attempt-3/SCORE_TRIAGE.md`.

#### T14.17 — v3.2 attempt-3 score triage

- [x] Completed

- Source requirement: Split Skill defects from methodology and gold on the frozen attempt-3 score. No product behavior change. No in-version rescore.
- Owner files: `tests/benchmark/v3_2-holdout/attempt-3/SCORE_TRIAGE.md`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - every failed metric is attributed to Skill, gold quality, or extraction/scoring contract;
  - S-001 is recorded as closed on this freeze; S-002 is recorded as narrowed;
  - H-001, H-003, G-001, and G-003 are not treated as Skill seeds;
  - gold, matches, evaluations, ontology, scorer, and runtime Skill files are unchanged.
- Evidence: `tests/benchmark/v3_2-holdout/attempt-3/SCORE_TRIAGE.md`.

#### T14.18 — Benchmark methodology v3.3 revision scoring

- [x] Completed

- Source requirement: Attempt-3 triage H-001, H-003, G-001, and G-003. No product behavior change. No rescore of v3.2 attempt 1–3, v3.1, or v2.
- Owner files: `tests/benchmark/v3_3/`, `TASK.md`, `CHANGELOG.md`, and `PUBLISH_MANIFEST.md`.
- Acceptance:
  - empty Green `revision_claims` credit required `no-revision`;
  - `preserve-intended-recipient` is not a scored required revision and cannot appear in gold required lists;
  - established-omission question candidates must be gold Red; occluded Data B tokens must be gold Intake;
  - v3.2 freeze-chain rules, thresholds, and `NOT_APPLICABLE` zero denominators remain;
  - v3.2 attempt-3 score report and v3.2 scorer bytes are unchanged;
  - unit and mutation tests kill disabled empty-credit, still-required recipient, and missing-envelope defects;
  - validation uses synthetic fixtures plus frozen attempt-3 gold as a negative contract fixture.
- Evidence: v3.3 methodology contract, unit results, mutation results, validation report, and archive note.

#### T14.19 — Fresh benchmark v3.3 unseen holdout

- [x] Completed

- Source requirement: Measure unseen-case performance with methodology v3.3. No product behavior change during scoring. No in-version rescore of v3.2 attempt 3.
- Owner files: `tests/benchmark/v3_3-holdout/`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - unseen cases use a domain that is not millinery, harpworks, Thornwick aerostat, Greaveholt cold-cathode, or any denylisted prior domain;
  - every case except the routing case is a manager recipient;
  - question candidates omit the required token from Data B and set `data_b_contains_unconfirmed_token` false;
  - image-only question candidates set `occluded_role`; Data B occlusion is not treated as Normal-mode review;
  - gold freeze includes `SEMANTIC_ONTOLOGY.json` and `score_semantic_v3_3.py`;
  - gold required revisions omit `preserve-intended-recipient`; established omissions are gold Red;
  - each case uses a distinct cloud SUT context against the T14.15 runtime;
  - dual extraction and semantic matching precede a single v3.3 scorer invocation;
  - v3.2 attempt 3 is not rescored.
- Evidence: gold/output/evaluation manifests, protocol audits, and one v3.3 score report.
- Progress: `SCORED`; thresholds not passed. Report SHA-256 `447968a580bb87ca0433d1ce0f9e2ed70b596b5768ead73f4e4b2ad311414140`. Formal scorer invocations: 1. Do not rescore. v3.2 attempt 3 is not rescored. Triage is `tests/benchmark/v3_3-holdout/SCORE_TRIAGE.md`.

#### T14.20 — v3.3 attempt-1 score triage

- [x] Completed

- Source requirement: Split Skill defects from methodology and gold on the frozen v3.3 attempt-1 score. No product behavior change. No in-version rescore.
- Owner files: `tests/benchmark/v3_3-holdout/SCORE_TRIAGE.md`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - every failed metric is attributed to Skill, gold quality, or extraction/scoring contract;
  - S-001 and S-002 deferral are recorded as closed on this freeze; H-001, H-003, and G-001 are recorded as closed;
  - H-004, G-004, G-005, and G-006 are not treated as Skill seeds;
  - gold, matches, evaluations, ontology, scorer, and runtime Skill files are unchanged.
- Evidence: `tests/benchmark/v3_3-holdout/SCORE_TRIAGE.md`.

#### T14.21 — S-007 Skill remediation

- [x] Completed

- Source requirement: `SPEC.md` Ratings. Attempt-1 triage S-007 (tone Yellow vs Red on an unsupported negligence/character label asserted as fact).
- Owner files: `SPEC.md`, `.cursor/skills/workplace-survival/`, `tests/TEST_CASES.md`, `TASK.md`, `CHANGELOG.md`.
- Acceptance:
  - an unsupported character or negligence label asserted as fact, including `careless`, is Tone Red, not Yellow;
  - an unestablished `again` pattern of fault asserted as fact is Tone Red;
  - qualified low-severity fault suggestions remain Yellow (TC-68, TC-112);
  - TC-60 still rates an explicit unsupported accusation Red;
  - v3.3 attempt 1 is not rescored and its gold is not rewritten;
  - H-004, G-004, G-005, and G-006 are not Skill-patched.
- Tests: TC-118; TC-60, TC-68, and TC-112 must still pass.
- Evidence: functional results for the new case.

#### T14.22 — Fresh benchmark v3.3 unseen holdout attempt 2

- [ ] Completed

- Source requirement: Measure unseen-case performance after T14.21 on methodology v3.3. No in-version rescore of v3.3 attempt 1.
- Owner files: `tests/benchmark/v3_3-holdout/attempt-2/`, `TASK.md`, and `CHANGELOG.md`.
- Acceptance:
  - unseen cases use a domain that is not millinery, harpworks, Thornwick aerostat, Greaveholt cold-cathode, Wetherlees turret-clock, or any denylisted prior domain;
  - every case except the routing case is a manager recipient;
  - question candidates omit the required token from Data B and set `data_b_contains_unconfirmed_token` false;
  - image-only question candidates set `occluded_role`; Data B occlusion is not treated as Normal-mode review;
  - gold freeze includes `SEMANTIC_ONTOLOGY.json` and `score_semantic_v3_3.py`;
  - gold required revisions omit `preserve-intended-recipient`; established omissions are gold Red;
  - each case uses a distinct cloud SUT context against the T14.21 runtime;
  - dual extraction and semantic matching precede a single v3.3 scorer invocation;
  - v3.3 attempt 1 is not rescored.
- Evidence: gold/output/evaluation manifests, protocol audits, and one v3.3 score report.
- Progress: gold/SUT/extraction frozen. Matcher copied via `git show` from `cursor/v332-matcher-claude-17a0` (PR #106). Evaluation freeze then one v3.3 score remaining. Attempt 1 is not rescored.

## Task template

Copy this block when adding work:

```markdown
### T[N] — [outcome]

- [ ] Completed

- Source requirement: [SPEC.md section / engineering evidence gap with no product behavior change]
- Owner files: [only files whose owned behavior must change]
- Acceptance:
  - [observable outcome]
  - [forbidden regression]
- Tests:
  - [new or existing case IDs]
- Evidence:
  - [result file to update]
```

## Completion gate

Before marking a task complete:

- [ ] The source requirement is explicit.
- [ ] Only owner files were changed.
- [ ] New behavior has acceptance assertions.
- [ ] Relevant regression suites pass.
- [ ] Results record actual scope and limitations.
- [ ] The completed summary is moved to `CHANGELOG.md`.
