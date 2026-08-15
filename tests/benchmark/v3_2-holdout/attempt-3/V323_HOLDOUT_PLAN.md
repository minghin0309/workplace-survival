# V3.2 holdout attempt 3 — T14.16

**Harness branch:** `cursor/blind-v323-holdout-17a0`  
**Skill runtime:** T14.15 @ `d37540b` (`cursor/s001-s002-remediation-17a0`)  
**Methodology:** v3.2 (`cursor/v32-recipient-contract-17a0` @ `2a7c7f5`)  
**Frozen attempt 2:** do not rescore. Gold SHA-256 `96c2ff593e42a0b909a5f4fd39a66835a5f12da4b95208d4464796cafa23a432`.

## Why a new attempt

Attempt 2 scored `SCORED` / `thresholds_passed: false`. Triage: S-001/S-002 Skill-fixed. H-001/H-002/H-003/G-001 not Skill-fixed. Formal scoring one-shot; no rescore of attempt 2.

## Isolation

Parent has seen millinery, harpworks, and Thornwick aerostat gold. Parent must not design cases. Isolated cloud designer + `git show` copy; never merge the designer branch.

## Domain denylist (attempt 2 + aerostat)

Attempt-2 denylist plus: aerostat, balloon, envelope hall, envelope, gondola, load tapes, helium, hydrogen, inflation, hangar, Thornwick Aerostat Works, Spindlefen Hangar, Envelope Hall, Saira Vennick, Bram Cotrell, Ivo Drellan, Mirelle Oatswell, Pell Oswaithe, Wardenmere Sightseeing, Pellwick Balloon Club, Brackfen Ripstop, RN-7602, RN-7609, RN-7741, TW-441, TW-508, TW-512, TW-519, TW-530, TW-547, TW-561, TW-574, TW-588.

## Coverage

18 cases / 24 turns. IDs `V323-001`–`V323-018`. Only `V323-017` is non-manager. Question candidates `V323-004`–`V323-009`. Three-turn `V323-014`–`V323-016`. Image-only question + readable image `V323-018`.

## Formal scoring

One write-once `score_semantic_v3_2.py` invocation: `SCORED`, `thresholds_passed: false`, `rerun_performed: false`. Report SHA-256 `4f9a30bc01f6e419a4cc173f3a1f49bb19feb5ce8206ef2bbeb852ddabe1c834`. Attempt 2 is not rescored.
