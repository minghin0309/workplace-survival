# V3.3 holdout attempt 1 — T14.19

**Harness branch:** `cursor/blind-v33-holdout-17a0`  
**Skill runtime:** T14.15 @ `d37540b` (`cursor/s001-s002-remediation-17a0`)  
**Methodology:** v3.3 (`cursor/benchmark-methodology-v33-17a0`)  
**Frozen attempt 3:** do not rescore. Report SHA-256 `4f9a30bc01f6e419a4cc173f3a1f49bb19feb5ce8206ef2bbeb852ddabe1c834`.

## Why a new attempt

Attempt 3 scored `SCORED` / `thresholds_passed: false`. Triage plus v3.3 fixed H-001/H-003 scoring and G-001/G-003 construction/gold-label contracts. Formal scoring remains one-shot. No rescore of attempt 3. Runtime Skill is unchanged.

## Isolation

Parent has seen millinery, harpworks, Thornwick aerostat, and Greaveholt gold. Parent must not design cases. Isolated cloud designer + `git show` copy; never merge the designer branch.

## Domain denylist

All prior holdout domains plus Greaveholt cold-cathode neon/argon tube works and named attempt-3 entities. See `V33_ATTEMPT1_CASE_BRIEF.md`.

## Coverage

18 cases / 24 turns. IDs `V33-001`–`V33-018`. Only `V33-017` is non-manager. Question candidates `V33-004`–`V33-009`. Three-turn `V33-014`–`V33-016`. Image-only question prefers occluded Data A (`occluded_role: data_a`). Readable image `V33-018`.

## Formal scoring

One write-once `score_semantic_v3_3.py` invocation after gold, SUT, extraction, and matching freezes. Gold freeze must include ontology and the v3.3 scorer. Attempt 3 is not rescored.
