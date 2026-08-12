# Workplace Survival Auto-Trigger Results

## Evidence policy

- Canonical evidence requirements: `tests/evidence/README.md`.
- Runs before T13.10 are historical summary-only results.
- The T13.10 routing-semantic record is stored in `tests/evidence/t13-10-validation.json`.
- A live probabilistic dispatcher run is not available in this environment.

Representative T13.10 record: `t13.10-at-at01-20260812`.

## Configuration

- `disable-model-invocation`: Removed for auto-trigger validation.
- Description tested: Current `SKILL.md` frontmatter description.
- Automatic-trigger cases: 9.
- Explicit-invocation regression cases: 1.

## Should-trigger results

- AT-01: PASS — Manager-message review triggered Normal mode.
- AT-02: PASS — Manager reply rewrite triggered separate responsibility and tone assessment.
- AT-03: PASS — Manager-message template request triggered Message-template mode.
- AT-04: PASS — Traditional Chinese manager-message review triggered and preserved the user's language.

False negatives: 0.

## Should-not-trigger results

- AT-05: PASS — General creative writing did not trigger.
- AT-06: PASS — Casual conversation did not trigger.
- AT-07: PASS — Message to a friend did not trigger.
- AT-08: PASS — Python code review did not trigger.
- AT-09: PASS — Work announcement for conference attendees did not trigger.

False positives: 0.

## Explicit invocation regression

- AT-10: PASS — Explicit `workplace-survival` invocation still loaded the skill and produced a green Normal-mode review.

## T11.3 conclusion

All four target scenarios triggered, all five excluded scenarios remained excluded, and explicit invocation still worked. The 10 cases were rerun after the post-T11.5 changes with 0 false triggers and 0 missed triggers. No description narrowing was required. Automatic model invocation remains enabled because `disable-model-invocation` is absent from the final frontmatter.

## T13.9 routing-description regression — 2026-08-12

- AT-01–AT-10: 10 passed, 0 failed.
- False triggers: 0.
- Missed triggers: 0.
- AT-07 remained excluded for a clearly non-manager friend message.
- AT-10 confirmed explicit invocation under the final automatic-invocation configuration.
- Method limitation: cases were evaluated deterministically against the current frontmatter and expected workflow; this was not a live probabilistic dispatcher run.

## T13.12 evidence-complete record index

- Evidence file: `tests/evidence/t13-12-final.json`.
- Records:
  - `t13.12-at-01-20260812`, `t13.12-at-02-20260812`, `t13.12-at-03-20260812`, `t13.12-at-04-20260812`, `t13.12-at-05-20260812`, `t13.12-at-06-20260812`, `t13.12-at-07-20260812`, `t13.12-at-08-20260812`
  - `t13.12-at-09-20260812`, `t13.12-at-10-20260812`

## T13.12 final result

- Deterministic routing cases: 10 passed, 0 failed.
- False triggers: 0.
- Missed triggers: 0.
- Limitation: no live probabilistic dispatcher was available; these results validate frontmatter-routing semantics, not production trigger variance.
