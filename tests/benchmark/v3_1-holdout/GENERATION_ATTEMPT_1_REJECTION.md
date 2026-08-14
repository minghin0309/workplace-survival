# v3.1 Generation Attempt 1 — Rejected

- Context: `bc-1780d218-aac3-5a93-9f1a-9eb48452d679`
- Branch: `cursor/v31-unseen-holdout-d679`
- Status: `REJECTED_NOVELTY`
- Artifacts integrated: no

Reason:

- The generated holdout used a ceramics co-operative as its shared domain.
- Benchmark v2 already used a production ceramics studio.
- This violates the v3.1 requirement not to reuse prior benchmark domains.

The designer correctly disclosed that it could not compare against prior corpora because those files were prohibited. The brief therefore contained an unverifiable requirement: avoid prior domains without providing a safe aggregate denylist.

Remediation:

- add a construction-only aggregate domain denylist to the brief;
- preserve the rejected attempt outside the accepted artifact chain;
- generate a new holdout in a fresh cloud context;
- do not reuse any case, image, answer fixture, wording, or construction artifact from attempt 1.
