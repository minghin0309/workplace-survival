# Blind Defect Remediation Triage

## Scope

The post-blind diagnostic labelled 18 cases as clear Skill/output defects. A second review found that the set mixed product defects with benchmark provenance and gold-contract problems.

No remediation rule is added solely to make disputed gold pass.

## Confirmed generalized product defects

| Root cause | Cases | Remediation |
|---|---|---|
| Qualified bad-faith inference overcalled as Tone Red | BH-018 | Keep explicitly qualified, non-severe intent inference Yellow; preserve observed facts and remove asserted intent |
| Low-value pronoun question outranked causal basis for accepting remediation ownership | BH-023 | Ask current causal basis/authority/scope before accepting fault; never re-ask prior facts already in Data A |
| Revision redirected from intended manager to source-email author | BH-028 | Preserve intended recipient independently from source authors, quoted speakers, and background participants |

## Benchmark/input-contract defects — no runtime fix

Cases: BH-002, BH-004, BH-008, BH-011, BH-012, BH-016, BH-017, BH-019, BH-020.

The gold treated `recipient_description` and `case_designer_notes` as Data A. Those fields were accessible to the SUT but are not part of the user-visible Workplace Survival input contract. Routing failures therefore do not justify changing the production Skill to ingest evaluator-only metadata.

Future blind cases must put every intended Data A fact inside the actual submitted input or a formally defined host context channel.

## Gold/question defects — no runtime fix

Cases: BH-007, BH-009, BH-010, BH-014.

The Skill used known facts from accessible case context, while gold required questions/placeholders for the same facts. Asking again would violate the existing effective-Data-A and no-repeat rules.

## Product-contract ambiguity — no runtime fix

Cases: BH-029, BH-030.

The images were background rather than identifiable unsent drafts. The user described intended content but did not supply exact Data B or explicitly request composition. Current Intake behavior follows the specification; gold instead rated a message that did not yet exist.

## Regression policy

- Add public regressions only for BH-018, BH-023, and BH-028 root causes.
- Preserve disputed blind evidence unchanged.
- Do not reuse cloud holdout gold as the remediation oracle.
- Re-run the complete public suite and mutation tests after generalized changes.
- Any new blind measurement must use unseen cases with an explicit Data A channel and semantic topic/fact ontology.
