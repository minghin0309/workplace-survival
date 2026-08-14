# Benchmark v3.1 Holdout Archive

The v3.1 unseen holdout is permanently archived with status `SCORER_ERROR`.

- Formal scorer attempts: 1
- Formal scorer reruns: 0
- Error: `ValueError: manifest schema`
- Failed stage: v2 `validate_benchmark.validate_manifest`
- Formal metrics emitted: none
- Formal case results emitted: none
- Score report SHA-256: `3ce1834894dd1007e4929ad4da0f44c5592264c49358f89473c4882101e4e8c2`
- Evaluation snapshot SHA-256: `70ab4a3490a04ea68cd060502031712fe111479ce1ee8f5d6dad2e1526071f7d`
- Extraction snapshot SHA-256: `a406161c1fac10f9c8b1f86c402891ac7dc81ac616abc8df0ebf9eb545c8b46e`
- Gold manifest SHA-256: `2aea483242418bdf73a56b0fdb921a718d4ea54c66611a8eae8d7bf7cf8e0377`

The v3.1 gold freeze does not include an `ontology` role. The v3 scorer requires a v2 exact-key manifest. Those facts are historical. They must not be repaired in-place or used to claim a v3.1 pass/fail Skill result.

Any scorer-schema correction belongs to benchmark v3.2 and requires a fresh unseen holdout.
