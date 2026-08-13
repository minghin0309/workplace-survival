# Benchmark v2 Replacement Gold Protocol Audit

## Replacement labeler 2

- Context: `bc-ad97cf43-3536-51e5-8449-36f664077d45`
- Verdict: `PASS`
- Model family: `grok`
- Machine model ID: `unverified`
- Labels commit: `30bc76b0f569d57a373d91c25bbf4cf14ec176fb`
- Attestation commit: `575aecee61269fb450b81cb81c96560b99392e96`
- Labels SHA-256: `3d927fa748f90c6bc264b30d23354855968f70ee01b25f5c54d5f5dad2976eb8`

Transcript audit found only the five allowed inputs and the two authored output files. No directory listing, search, prior label, gold, adjudication, plan, methodology, scorer, validator, test, oracle note, runtime file, history, diff, PR, or SUT output was accessed.

## Replacement adjudicator

- Context: `bc-71c5d4ca-0585-5745-99ec-50491605c172`
- Verdict: `PASS`
- Model family: `gpt`
- Machine model ID: `unverified`
- Raw output commit: `5811293f638248d896dc3319ddcd5d0898aa0efb`
- Attestation commit: `e3a7236054bb2a787ceaaf67d5c7043ba601bb66`
- Raw gold SHA-256: `6aa1e952c725727919ac9c315a2f48b4f3d6ad1da975ceecb5330295cc7aff0a`
- Raw adjudication SHA-256: `a53fc6b3d07da8832d9b9a6f0614f8935f802ec341701a5376cf08645f153f67`

Transcript audit found only the twelve allowed inputs and three authored outputs. The invalidated labeler-2 artifact, prior gold/adjudication, plans, methodology, scorer, validator, tests, oracle notes, runtime files, manifests, PRs, and SUT outputs were not accessed.

## Results

- Cases: 18
- Turns: 24
- Gold-uncertain turns: 1 (4.17%)
- Gold/adjudication final-turn parity mismatches: 0
- Categorical vote distributions with totals other than three: 0

Both audits are transcript/tool-log based. They do not constitute an independent filesystem access log. Image tools opened both PNG paths; the allowlisted case document also contains rendered image text, so the audit proves file isolation but not pixel-only OCR.
