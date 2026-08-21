# V3.3 holdout attempt 2 — T14.22

**Harness branch:** `cursor/blind-v332-holdout-17a0`  
**Skill runtime:** T14.21 @ `357f99d` (`cursor/s007-tone-17a0`)  
**Methodology:** v3.3 (`cursor/benchmark-methodology-v33-17a0`)  
**Frozen attempt 1:** do not rescore. Report SHA-256 `447968a580bb87ca0433d1ce0f9e2ed70b596b5768ead73f4e4b2ad311414140`.

## Why a new attempt

Attempt 1 scored `SCORED` / `thresholds_passed: false`. Triage plus T14.21 Skill-fixed S-007 (unsupported `careless` / unestablished `again` as Tone Red). H-004, G-004, G-005, and G-006 were not Skill-patched. Formal scoring remains one-shot. No rescore of attempt 1. Runtime Skill is T14.21 and must not change during scoring.

## Isolation

Parent has seen millinery, harpworks, Thornwick aerostat, Greaveholt, and Wetherlees turret-clock gold. Parent must not design cases. Isolated cloud designer + `git show` copy; never merge the designer branch.

## Domain denylist

All prior holdout domains plus Wetherlees turret-clock restoration and named attempt-1 entities. See `V332_ATTEMPT2_CASE_BRIEF.md`.

## Coverage

18 cases / 24 turns. IDs `V332-001`–`V332-018`. Only `V332-017` is non-manager. Question candidates `V332-004`–`V332-009`. Three-turn `V332-014`–`V332-016`. Image-only question prefers occluded Data A (`occluded_role: data_a`). Readable image `V332-018`.

## Formal scoring

One write-once `score_semantic_v3_3.py` invocation after gold, SUT, extraction, and matching freezes. Gold freeze must include ontology and the v3.3 scorer. Attempt 1 is not rescored.
