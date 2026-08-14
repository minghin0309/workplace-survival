# Fresh v3.2 Holdout Status

- Status: `CONSTRUCTION_VALID`
- Methodology: v3.2
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`
- Holdout branch: `cursor/blind-v32-holdout-17a0`
- Cases: 18 (`V32-001`–`V32-018`)
- Turns: 24
- Formal scorer invocations: 0

Construction:

- isolated designer: `bc-9996f210-fde7-527c-898e-bc114613975e`;
- source branch `cursor/isolated-v32-case-design-975e` @ `466fd70` copied with `git show`; not merged;
- domain: concert pedal-harp restringing/regulation (not denylisted);
- six question candidates; V32-008 image-only occluded measurement; V32-018 readable image-only;
- `validate_holdout.py` passed (18 mutations, denylist, PNG headers);
- question-design key is `candidates`; harness accepts that alias without rewriting the blob.

Gold, SUT, extraction, matching, and scoring have not started.

v3.1 remains archived as `SCORER_ERROR` and will not be rescored.
