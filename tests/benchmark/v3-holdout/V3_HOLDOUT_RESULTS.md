# Fresh Benchmark v3 Holdout Results

- Status: `INVALID_COVERAGE`
- Cases: 18
- Turns: 24
- Images: 2
- Required question concepts: 2
- Cases with required question concepts: 2
- Required revision concepts: 88
- Cases with required revision concepts: 17
- Accepted turns: 24
- Gold-uncertain turns: 0
- SUT execution authorized: no
- SUT contexts executed: 0
- Formal scorer invocations: 0

Coverage failure:

- v3 requires at least 3 required question concepts across at least 3 cases;
- adjudicated gold contains required questions only for V3-005 and V3-017;
- `required_question_concepts` and `required_question_cases` therefore fail.

The four material-information designs did not guarantee four required questions after independent gold review. V3-004 became a direct responsibility failure, V3-006 produced no two-of-three required revision or question majority, and V3-007 was adjudicated Green. Gold was not altered to fit the preregistered gate.

Isolation and provenance:

- the case designer produced new synthetic domains and wording from the case brief;
- three accepted gold labelers used Grok, Kimi, and GPT families;
- a Claude-family fourth adjudicator preserved all votes and reported coverage honestly;
- one incomplete Kimi attempt that read runtime Skill files was rejected;
- accepted contexts had no prohibited benchmark-content access;
- path and commit-subject metadata deviations are preserved in audit evidence.

Classification:

- Skill defect: none; the Skill was never executed;
- gold defect: none confirmed; independent labels were preserved;
- benchmark design/coverage defect: confirmed insufficient required-question coverage;
- scorer defect: none exercised; v3 scorer was not invoked;
- harness defect: none caused the stop; the v3 pre-SUT gate worked as designed.

Frozen evidence:

- canonical gold SHA-256: `cb98bad55e0d365d7781d0abc11d180c4548575c83c35df6a427ed39ddc387f9`
- coverage report SHA-256: `c05477a4d64cf29b273c73152c70b34308e89241be4ac4410d3b430900bf7b1d`
- invalid-coverage manifest SHA-256: `1e031dce4bb364e9f7cbf62b2f6c8dbdfc7065ec2c67ffb228c32a29e05e8dd9`

No SUT, extraction, matching, or scoring artifact may descend from this invalid holdout.
