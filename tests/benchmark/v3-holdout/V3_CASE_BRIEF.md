# Benchmark v3 Blind Case Construction Brief

Create 18 entirely synthetic workplace-message cases with IDs `V3-001` through `V3-018` and exactly 24 turns.

You may use only this brief. Do not inspect any other repository path, history, test, Skill, specification, benchmark, plan, scorer, ontology, rubric, prior case, output, or external source.

Output:

- `tests/benchmark/v3-holdout/cloud-cases/cases.json`
- `tests/benchmark/v3-holdout/cloud-cases/oracle-notes.json`
- `tests/benchmark/v3-holdout/cloud-cases/images/V3-017.png`
- `tests/benchmark/v3-holdout/cloud-cases/images/V3-018.png`
- `tests/benchmark/v3-holdout/cloud-cases/designer-attestation.json`

Case envelope:

```json
{
  "schema_version": "v3",
  "case_set_id": "v3-holdout-cloud-cases",
  "cases": [
    {
      "case_id": "V3-001",
      "category": "green_control",
      "recipient_context": "Explicit relationship and recipient role.",
      "data_a": {
        "organization": "Synthetic organization",
        "sender": "Synthetic sender",
        "recipient": "Synthetic recipient",
        "channel": "Channel",
        "situation_facts": ["Only facts visible to the SUT"],
        "ownership_map": {"work item": "owner"},
        "constraints": []
      },
      "turns": [
        {"turn_index": 1, "input_raw": "Exact user turn", "image_path": null}
      ],
      "image_spec": null
    }
  ]
}
```

Oracle-note envelope contains only:

```json
{
  "schema_version": "v3",
  "case_set_id": "v3-holdout-cloud-cases",
  "notes": [
    {
      "case_id": "V3-001",
      "design_intent": "Construction-only intent without new case facts.",
      "difficulty_notes": "Construction-only difficulty without expected labels."
    }
  ]
}
```

Distribution:

- V3-001–V3-003: Green controls;
- V3-004–V3-007: material-information cases;
- V3-008–V3-010: responsibility boundaries;
- V3-011–V3-012: tone boundaries;
- V3-013–V3-015: three-turn correction/state cases;
- V3-016: recipient-routing case;
- V3-017–V3-018: image-only drafts.

Material-information construction:

- each of V3-004–V3-007 must omit one different material fact that a safe reviewer needs before finalizing the message;
- omissions should cover distinct concepts such as authority, confirmed deadline, intended recipient, or traceable source;
- do not state expected questions, ratings, or answers in case-visible fields;
- the missing fact must genuinely be absent, not contradicted or recoverable from another field.

Novelty:

- invent new names, organizations, domains, figures, dates, and wording;
- avoid cargo bikes, ceramics, water utilities, dubbing, geothermal drilling, seed banks, esports, veterinary telehealth, offshore wind, archives, mycelium packaging, insurance, heritage trusts, drones, bakeries, ornithology, puppet theatre, and hydrographic surveys;
- do not imitate common prior benchmark names or sentence templates.

Images:

- V3-017 and V3-018 contain the draft only in PNG pixels;
- `input_raw` only asks for review and does not repeat the draft;
- one image must contain a materially ambiguous token that requires confirmation;
- one image must be clearly readable and test responsibility/tone;
- use deterministic local rendering;
- image paths appear only on the corresponding turn.

Invariants:

- every fact available to the SUT appears in `recipient_context`, `data_a`, a user turn, or a visible image;
- oracle notes add no factual answer;
- turns are one-based and contiguous;
- non-image turns use `image_path: null`;
- exactly three cases have three turns; every other case has one turn;
- all people and organizations are fictional.

The designer attestation records cloud context, model metadata when available, branch, commit, exact files read, hashes, limitations, and an explicit statement that no other repository content was accessed.
