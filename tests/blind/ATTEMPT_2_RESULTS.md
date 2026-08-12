# Blind Holdout Attempt 2

## Outcome

Status: `INVALID — FROZEN-IMAGE MUTATION`

No Skill accuracy metric or pass/fail conclusion is reported.

## Frozen-image mutation

The final holdout freeze recorded retry `BH-028.png` as:

```text
3accd5925880ab0225f26faca91bb8063f46247e940f42290d310ea9088af02c
```

Before output normalization, the same path hashed to:

```text
0586fdaef36cb6ca8d6143c30f610f67b0bf91807095975660a8edc2809ae009
```

The deterministic normalizer rejected the run with `image changed after holdout freeze`. No re-freeze or post-unblinding correction was performed.

## Additional harness incidents

- One adjudicator ignored absolute-path restrictions, switched Git branches, committed to the wrong branch, and wrote to attempt-1 paths. The retry branch was restored before continuing.
- Five SUT contexts committed raw outputs into the retry branch. Their outputs were copied to the temporary evidence area, and normal revert commits removed the misplaced files.
- Multiple SUT contexts ignored the requested raw JSON envelope. Original files and the mechanical normalization log are preserved.

## Integrity statement

- No score was calculated.
- No gold was changed after Skill output generation.
- No frozen image was accepted after its hash changed.
- No raw Skill output was altered.
- The retry holdout is retired and will not be reused.

## Required next condition

A valid blind test now requires stronger artifact immutability and preferably cases supplied from an environment that cannot access prior holdouts, such as:

- user-provided hidden cases;
- a separately authorized cloud environment containing only the case brief;
- an independent human case designer.

Further prompt-only local retries would not provide credible blindness.
