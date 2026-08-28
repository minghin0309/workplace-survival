# V3.3 holdout attempt 4 — T14.28

**Harness branch:** `cursor/blind-v334-holdout-17a0`  
**Skill runtime:** T14.27 @ `805ae2e414987e759c72b970c382d23686783f74` (`cursor/s009-s013-remediation-17a0`)  
**Methodology:** v3.3 (`cursor/benchmark-methodology-v33-17a0`)  
**Frozen attempt 1:** do not rescore. Report SHA-256 `447968a580bb87ca0433d1ce0f9e2ed70b596b5768ead73f4e4b2ad311414140`.  
**Frozen attempt 2:** do not rescore. Report SHA-256 `de7123b79fdaa35549d3ee7eaaa64f9cfdd2f1a7e47c584dcf0c4418daef321d`.  
**Frozen attempt 3:** do not rescore. Report SHA-256 `fa7c922c3b1868a5b809f14e68d97f2936b407d5f42f84a9e7888c38b26180e6`.

## Why a new attempt

Attempt 3 scored `SCORED` / `thresholds_passed: false`. Triage plus T14.27 Skill-fixed S-009/S-009b, S-011, S-012, S-013, and S-002 residual. H-004, G-007, and G-008 were not Skill-patched. Formal scoring remains one-shot. No rescore of attempt 1, attempt 2, or attempt 3. Runtime Skill is T14.27 and must not change during scoring.

## Isolation

Parent has seen millinery, harpworks, Thornwick aerostat, Greaveholt, Wetherlees turret-clock, Rowanleat cork, and Selkith aneroid / Cinderholt pressing-rooms gold. Parent must not design cases. Isolated cloud designer + `git show` copy; never merge the designer branch.

## Domain denylist

All prior holdout domains plus Wetherlees turret-clock restoration, Rowanleat cork works, Selkith aneroid / Cinderholt pressing rooms, and named attempt-1/attempt-2/attempt-3 entities. See `V334_ATTEMPT4_CASE_BRIEF.md`.

## Coverage

18 cases / 24 turns. IDs `V334-001`–`V334-018`. Only `V334-017` is non-manager. Question candidates `V334-004`–`V334-009`. Three-turn `V334-014`–`V334-016`. Image-only question prefers occluded Data A (`occluded_role: data_a`), conventionally `V334-009`. Readable image `V334-018`. If the designer puts the occluded question on another candidate, update `IMAGE_OPENS` in `assemble_sut_outputs.py` before assembly.

## Formal scoring

One write-once `score_semantic_v3_3.py` invocation after gold, SUT, extraction, and matching freezes. Gold freeze must include ontology and the v3.3 scorer. Attempt 1, attempt 2, and attempt 3 are not rescored. Report path `tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/score-report-v334.json` must not already exist.

```
python3 tests/benchmark/v3_3/score_semantic_v3_3.py \
  tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/evaluation-manifest-v334.json \
  tests/benchmark/SEMANTIC_ONTOLOGY.json \
  tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/gold-v334.json \
  tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/outputs-v334-raw.json \
  tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/evaluations-v334-canonical.json \
  tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/matches-v334.json \
  tests/benchmark/v3_3-holdout/attempt-4/cloud-cases/score-report-v334.json
```
