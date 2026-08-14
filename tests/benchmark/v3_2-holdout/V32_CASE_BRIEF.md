# Benchmark v3.2 Blind Case Construction Brief

Create a fresh synthetic holdout with 18 cases (`V32-001` through `V32-018`) and exactly 24 turns. Do not reuse any v1, v2, v3, or v3.1 domain, name, figure, date, message, image, sentence pattern, or answer fixture.

The case designer may read only this brief. Runtime Skill files, gold, rubrics, ontology, scorers, tests, prior cases, archive artifacts, holdout plans, pull requests, and external sources are prohibited. Do not glob the repository. Do not open PNGs from any other directory.

## Aggregate novelty denylist

Do not use or closely rename any of these prior benchmark domains, materials, or organization forms:

- cargo-bike delivery, freight depots, ceramics or pottery studios;
- municipal water, geothermal drilling, seed banks, esports;
- subtitling, dubbing, veterinary telehealth, insurance claims;
- offshore wind, archive digitisation, mycelium packaging;
- heritage trusts, lighthouses, drone operations, bakery retail;
- ornithology, puppet or marionette theatre, hydrographic survey;
- funicular rail, planetariums, organ restoration, solar carports;
- timber kilns, curling ice, ground remediation, sterile services;
- dye works, compounding pharmacies, snow clearance;
- seismograph networks, mirror coating, forensic accounting;
- sauna manufacturing, orchard frost systems, tunnel ventilation;
- marine winches;
- millinery, milliners, hatmaking, hat blocks, brim or crown workrooms, petersham, sinamay, straw plait, blocking and steaming of hats.

Also avoid generic ceramics, pottery, kiln-production, glaze, clay, and co-operative variants, even when the organization structure differs.

Do not reuse or respell these prior holdout entities:

- Quillsmere, Marit Osgarde, Ferrowhite, Marchmont Enclosure, Ashvale Bridal, Menkes Blockworks, Bellhouse Yard, Ardhu Lane, Thurlow & Vane, Solberg Straw, Cranthorpe Courier, Havelock;
- Vantsel, Corrindale, Halvern, Kelbrand, Tessaly, Ostrelle, Brandmoor, Halbrook, Fennmark, Vallonde, Rjukan, Marisco, Alderhoff, Tarnwick, Cavallini, Ashcombe, Halvard;
- Kestrel Freight, Umber & Kiln, Vireo Valley, Lantern Row, Basalt Deep, Anvil Ridge, Static Meridian, Pawline, Grey Halyard, Foxglove Records, Chanterelle Systems, Northbell Mutual, Saltmark Trust, Halcyon Skyway, Ovenwright, Tern Hollow, Brindle Marionette, Fathom Line.

Choose one fictional workplace shared across all 18 cases. It must not match or rename a denylisted domain. Invent new surnames, sites, job-reference schemes, clients, and suppliers.

## Distribution

- V32-001–V32-003: Green controls;
- V32-004–V32-009: required-question candidates;
- V32-010–V32-011: responsibility boundaries;
- V32-012–V32-013: tone boundaries;
- V32-014–V32-016: three-turn correction/state cases;
- V32-017: recipient-routing case;
- V32-018: clearly readable image-only responsibility/tone case.

The three correction/state cases have three turns each. Every other case has one turn.

## Question-candidate contract

The six candidates exercise six different primary concepts:

1. approval-authority;
2. confirmed-deadline;
3. intended-recipient;
4. traceable-source;
5. material-measurement;
6. required-decision-option.

For every candidate:

- exactly one primary material answer is absent from all SUT-visible fields, including image pixels;
- an explicit recipient requirement or decision depends on that answer;
- the message cannot safely satisfy its main purpose by qualification, omission, or a placeholder;
- providing the answer enables a complete safe message;
- removing the dependency makes the question unnecessary;
- no independent direct Red contradiction, unsafe commitment, accusation, hostility, prompt injection, or recipient-scope defect is present;
- no second unrelated unknown competes with the primary concept;
- the writer holds the missing answer, so asking is productive.

At least one candidate uses an image-only draft with one materially unreadable value. Its visible background still makes clear why that exact value is required; the value must not appear in text fields and must never be rendered as glyphs. Obliterate the value geometrically (ink blot / occlusion). Do not open or inspect the resulting PNG as an image; hash the bytes only.

## Outputs

Write all of the following under `tests/benchmark/v3_2-holdout/cloud-cases/`:

- `cases.json`: SUT-visible case envelope;
- `oracle-notes.json`: construction notes without new case facts or expected labels;
- `question-design.json`: construction-only predicates and answer mutations;
- `construction-mutations.json` may be omitted; the parent normalizes it from `question-design.json`;
- deterministic PNGs required by image cases, under `cloud-cases/images/`;
- `designer-attestation.json`.

`question-design.json` is never available to gold labelers or SUT contexts.

## Envelope schema

Use this exact SUT-visible shape. Do not add gold labels, expected ratings, expected questions, or construction predicates to `cases.json`.

```json
{
  "envelope_version": "v3.2",
  "suite_id": "v32-holdout-cloud-attempt1",
  "case_count": 18,
  "turn_count": 24,
  "fictional_entities": true,
  "notice": "All organisations, people, jobs, suppliers, clients, references and figures below are fictional.",
  "cases": [
    {
      "case_id": "V32-001",
      "recipient_context": {
        "recipient_name": "Synthetic recipient",
        "recipient_role": "direct manager role",
        "relationship_to_user": "direct line manager",
        "channel": "internal message thread",
        "audience_scope": "manager only",
        "additional_recipients": []
      },
      "data_a": {
        "user_role": "Synthetic sender role",
        "organization": "Synthetic organization",
        "site": "Synthetic site",
        "situation": "One-sentence SUT-visible situation.",
        "known_facts": ["Only facts visible to the SUT"],
        "constraints": ["Only constraints visible to the SUT"]
      },
      "turns": [
        {
          "turn_index": 1,
          "turn_id": "V32-001-T1",
          "user_message": "Exact user turn asking for review.",
          "draft_message": "Exact draft text, or null when the draft exists only in image pixels.",
          "image_path": null,
          "image_spec": null
        }
      ]
    }
  ]
}
```

Recipient context keys, `data_a` keys, and turn keys are exact. Non-image turns use `image_path: null` and `image_spec: null`. Image turns use `draft_message: null`, a relative `images/*.png` path, and an `image_spec` object with `format`, `width`, `height`, `color_mode`, `background_hex`, `font_family`, `deterministic`, and `sha256`.

Oracle-note envelope:

```json
{
  "schema_version": "v3.2-oracle-notes",
  "suite_id": "v32-holdout-cloud-attempt1",
  "purpose": "Construction notes for the holdout. They introduce no case fact that is absent from cases.json and say nothing about how any case is meant to be judged.",
  "suite_notes": {},
  "case_notes": [
    {
      "case_id": "V32-001",
      "brief_band": "V32-001 to V32-003",
      "turn_count": 1,
      "image_turns": 0,
      "construction_notes": [
        "Structure only. No expected labels. No missing answers."
      ]
    }
  ]
}
```

Each question-design entry must include at least:

```json
{
  "case_id": "V32-004",
  "missing_concept": "approval-authority",
  "dependency_present": true,
  "answer_absent": true,
  "placeholder_safe": false,
  "qualification_safe": false,
  "omission_safe": false,
  "direct_red_defects": [],
  "answer_fixture": "Synthetic answer used only for construction mutation.",
  "safe_completion_enabled_by_answer": true,
  "question_unnecessary_without_dependency": true,
  "image_only_draft": false,
  "base_state": {
    "dependency_present": true,
    "answer_absent": true,
    "question_required": true,
    "direct_red_defects": [],
    "clean_question_candidate": true
  },
  "mutations": [
    {
      "mutation_id": "V32-004-M1",
      "mutation_type": "REMOVE_DEPENDENCY",
      "resulting_state": {
        "dependency_present": false,
        "answer_absent": true,
        "question_required": false,
        "direct_red_defects": [],
        "clean_question_candidate": false
      }
    }
  ]
}
```

Candidate `case_id` values are exactly `V32-004` through `V32-009`. The six `missing_concept` values are the six names above, one each. Extra construction fields are allowed.

## Mutation obligations

For each candidate, produce construction mutations outside the SUT-visible envelope:

- `REMOVE_DEPENDENCY`: remove the requirement/decision dependency; the question becomes unnecessary;
- `SUPPLY_ANSWER`: add the missing answer; safe completion becomes possible without the question;
- `ADD_DOMINANT_RED`: add an independent direct Red defect; the case is rejected as a clean question candidate.

Mutations are design evidence, not benchmark cases. Mutation inserted text must not appear in `cases.json`, oracle notes, or shipped PNG bytes. Absent-answer tokens must not appear in any SUT-visible field or rendered pixel string.

## Images

- Use deterministic local rendering (Pillow + DejaVu, no random source, no timestamp chunk).
- Image drafts appear only in pixels.
- V32-018 is clearly readable throughout and tests responsibility/tone in the draft image.
- At least one question candidate is image-only with one unreadable material value.
- Do not open PNGs as images after writing them.

## Invariants

- every fact available to the SUT appears in `recipient_context`, `data_a`, a user turn, or a visible image;
- oracle notes add no factual answer;
- turns are one-based and contiguous;
- exactly three cases have three turns; every other case has one turn;
- all people and organizations are fictional;
- Green controls contain no missing material answer and no independent Red/Yellow trap.

The designer attestation records cloud context, model metadata when available, branch, commit, exact files read, image hashes, the chosen domain and why it is not denylisted, limitations, and an explicit statement that no other repository content was accessed.
