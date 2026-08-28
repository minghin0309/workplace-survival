# V3.3 holdout attempt 3 — T14.25

**Harness branch:** `cursor/blind-v333-holdout-17a0`  
**Skill runtime:** T14.24 @ `9c79eb87b624f75d1c0d9fe26ddba56994bffbd9` (`cursor/s008-s010-green-control-17a0`)  
**Methodology:** v3.3 (`cursor/benchmark-methodology-v33-17a0`)  
**Frozen attempt 1:** do not rescore. Report SHA-256 `447968a580bb87ca0433d1ce0f9e2ed70b596b5768ead73f4e4b2ad311414140`.  
**Frozen attempt 2:** do not rescore. Report SHA-256 `de7123b79fdaa35549d3ee7eaaa64f9cfdd2f1a7e47c584dcf0c4418daef321d`.

## Why a new attempt

Attempt 2 scored `SCORED` / `thresholds_passed: false`. Triage plus T14.24 Skill-fixed S-008, S-009, and S-010. H-004 and G-007 were not Skill-patched. Formal scoring remains one-shot. No rescore of attempt 1 or attempt 2. Runtime Skill is T14.24 and must not change during scoring.

## Isolation

Parent has seen millinery, harpworks, Thornwick aerostat, Greaveholt, Wetherlees turret-clock, and Rowanleat cork gold. Parent must not design cases. Isolated cloud designer + `git show` copy; never merge the designer branch.

## Domain denylist

All prior holdout domains plus Wetherlees turret-clock restoration, Rowanleat cork works, and named attempt-1/attempt-2 entities. See `V333_ATTEMPT3_CASE_BRIEF.md`.

## Coverage

18 cases / 24 turns. IDs `V333-001`–`V333-018`. Only `V333-017` is non-manager. Question candidates `V333-004`–`V333-009`. Three-turn `V333-014`–`V333-016`. Image-only question prefers occluded Data A (`occluded_role: data_a`), conventionally `V333-009`. Readable image `V333-018`. If the designer puts the occluded question on another candidate, update `IMAGE_OPENS` in `assemble_sut_outputs.py` before assembly.

## Formal scoring

One write-once `score_semantic_v3_3.py` invocation after gold, SUT, extraction, and matching freezes. Gold freeze must include ontology and the v3.3 scorer. Attempt 1 and attempt 2 are not rescored. Report path `tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/score-report-v333.json` must not already exist.

```
python3 tests/benchmark/v3_3/score_semantic_v3_3.py \
  tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/evaluation-manifest-v333.json \
  tests/benchmark/SEMANTIC_ONTOLOGY.json \
  tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/gold-v333.json \
  tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/outputs-v333-raw.json \
  tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/evaluations-v333-canonical.json \
  tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/matches-v333.json \
  tests/benchmark/v3_3-holdout/attempt-3/cloud-cases/score-report-v333.json
```
