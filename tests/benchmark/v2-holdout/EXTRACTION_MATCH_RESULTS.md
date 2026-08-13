# Benchmark v2 Extraction and Semantic Match Results

- Status: `EVALUATIONS_FROZEN`
- Gold-blind extractors: 2
- Extractor model families: Claude and Kimi
- Extraction adjudicator family: GPT
- Cases: 18
- Turns: 24
- Extracted claims: 89
- Unresolved claim disagreements: 0
- Unsupported semantic claims: 7
- Extraction snapshot SHA-256: `cc5dd4dd8dd80fd8ea6477c52941206c55d213067cfed2f5a2b3d1cdf424d419`
- Canonical evaluations SHA-256: `61c5aa0791ab3138fa597f13d59330668f4ecc3d24bc651115e728a468189764`
- Canonical matches SHA-256: `b487fa6a62d99915ba60cc1a5000e643cefbd012d19877039df756720e48e19b`
- Evaluation manifest SHA-256: `89c73ffb919541e8fbba0d55cc12e5c20b83af526a97bb216d35cbf4d1a40e16`

Validation:

- Both extractors operated without gold, adjudication, ontology, rubric, scorer, oracle, or expected-answer access.
- Every claim has a unique ID and a non-empty evidence span copied exactly from the frozen raw Skill output.
- All 18 cases and 24 turns were reviewed by both extractor contexts.
- A third gold-blind context resolved claim-granularity differences and recorded zero unresolved disagreements.
- Extraction artifacts were frozen before semantic matching.
- The first matcher attempt was rejected after non-allowlisted path attempts.
- The accepted matcher read exactly the frozen extraction snapshot, canonical evaluations, raw outputs, canonical gold, and ontology.
- Every one of the 89 extracted claims has exactly one match decision.
- Non-null concept IDs are restricted to the matching turn and claim domain's allowed gold concepts.
- Semantic decisions use confidence at least 0.8; unsupported claims retain null concept IDs.
- Frozen scorer and validator bytes were restored after an intermediate gate detected accidental post-freeze modification.
- The recursive gold-to-output evaluation manifest passed validation and additionally freezes the extraction snapshot.
- No score report was generated.
- Runtime Skill files were not modified.
