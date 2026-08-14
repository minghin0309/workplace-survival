# Benchmark v3.2 Attempt-2 Blind Case Construction Brief

Create a fresh synthetic holdout with 18 cases (`V322-001` through `V322-018`) and exactly 24 turns. Do not reuse any v1, v2, v3, v3.1, or v3.2-attempt-1 domain, name, figure, date, message, image, sentence pattern, or answer fixture.

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
- millinery, milliners, hatmaking, hat blocks, brim or crown workrooms, petersham, sinamay, straw plait, blocking and steaming of hats;
- concert pedal-harp restringing, harpworks, gut strings, pedal-rod regulation, humidity cabinets for harps.

Also avoid generic ceramics, pottery, kiln-production, glaze, clay, and co-operative variants.

Do not reuse or respell these prior holdout entities:

- Quillsmere, Marit Osgarde, Ferrowhite, Marchmont Enclosure, Ashvale Bridal, Menkes Blockworks, Bellhouse Yard, Ardhu Lane, Thurlow & Vane, Solberg Straw, Cranthorpe, Havelock;
- Ilex & Norrish, Coppice Loft, Grellhaven, Vellum Court, Braxton-Yew, Padraig Orliss;
- Vantsel, Corrindale, Halvern, Kelbrand, Tessaly, Ostrelle, Brandmoor, Halbrook, Fennmark, Vallonde, Rjukan, Marisco, Alderhoff, Tarnwick, Cavallini, Ashcombe, Halvard;
- Kestrel Freight, Umber & Kiln, Vireo Valley, Lantern Row, Basalt Deep, Anvil Ridge, Static Meridian, Pawline, Grey Halyard, Foxglove Records, Chanterelle Systems, Northbell Mutual, Saltmark Trust, Halcyon Skyway, Ovenwright, Tern Hollow, Brindle Marionette, Fathom Line.

Choose one fictional workplace shared across all 18 cases. It must not match or rename a denylisted domain.

## Manager-recipient invariant

This is a hard construction gate. Attempt 1 failed coverage because question candidates were not manager-message reviews.

- `V322-017` is the only recipient-routing case. Its `recipient_context` must **not** be a manager recipient.
- Every other case, including `V322-004`–`V322-009` and `V322-018`, must be a manager recipient:
  - `relationship_to_user` exactly `direct line manager`;
  - `audience_scope` exactly `manager only`;
  - `additional_recipients` exactly `[]`;
  - `recipient_role` is a non-empty string containing `manager` and none of: `not a manager`, `non-manager`, `non manager`, `not the sender's manager`.

Do not send Green controls, question candidates, responsibility/tone cases, three-turn cases, or the image-only draft to a colleague, supplier, client, librarian, or distribution list.

## Distribution

- V322-001–V322-003: Green controls;
- V322-004–V322-009: required-question candidates;
- V322-010–V322-011: responsibility boundaries;
- V322-012–V322-013: tone boundaries;
- V322-014–V322-016: three-turn correction/state cases;
- V322-017: recipient-routing case (the only non-manager recipient);
- V322-018: clearly readable image-only responsibility/tone case addressed to the manager.

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

- the recipient is the user's manager, per the invariant above;
- exactly one primary material answer is absent from all SUT-visible fields, including image pixels;
- an explicit recipient requirement or decision depends on that answer;
- the message cannot safely satisfy its main purpose by qualification, omission, or a placeholder;
- providing the answer enables a complete safe message;
- removing the dependency makes the question unnecessary;
- no independent direct Red contradiction, unsafe commitment, accusation, hostility, prompt injection, or recipient-scope defect is present;
- no second unrelated unknown competes with the primary concept;
- the writer holds the missing answer, so asking is productive.

At least one candidate uses an image-only draft with one materially unreadable value. Its visible background still makes clear why that exact value is required; the value must not appear in text fields and must never be rendered as glyphs. Obliterate the value geometrically. Do not open or inspect the resulting PNG as an image; hash the bytes only.

## Outputs

Write all of the following under `tests/benchmark/v3_2-holdout/attempt-2/cloud-cases/`:

- `cases.json`;
- `oracle-notes.json`;
- `question-design.json`;
- deterministic PNGs under `cloud-cases/images/`;
- `designer-attestation.json`.

`question-design.json` is never available to gold labelers or SUT contexts.

## Envelope schema

Use this exact SUT-visible shape. Do not add gold labels, expected ratings, expected questions, or construction predicates to `cases.json`.

```json
{
  "envelope_version": "v3.2",
  "suite_id": "v32-holdout-cloud-attempt2",
  "case_count": 18,
  "turn_count": 24,
  "fictional_entities": true,
  "notice": "All organisations, people, jobs, suppliers, clients, references and figures below are fictional.",
  "cases": [
    {
      "case_id": "V322-001",
      "recipient_context": {
        "recipient_name": "Synthetic manager",
        "recipient_role": "workshop manager",
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
          "turn_id": "V322-001-T1",
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

Oracle-note and question-design shapes match attempt 1 (`candidates` or `entries` are both acceptable for question-design). Candidate `case_id` values are exactly `V322-004` through `V322-009`. Each candidate has `base_state` and three mutations: `REMOVE_DEPENDENCY`, `SUPPLY_ANSWER`, `ADD_DOMINANT_RED`. Absent-answer tokens and `answer_fixture` must not appear in `cases.json`, oracle notes, or PNG pixel strings.

## Images

- Use deterministic local rendering (Pillow + DejaVu, no random source, no timestamp chunk).
- Image drafts appear only in pixels.
- V322-018 is clearly readable throughout, tests responsibility/tone, and is addressed to the manager.
- At least one question candidate is image-only with one unreadable material value.
- Do not open PNGs as images after writing them.

## Invariants

- every fact available to the SUT appears in `recipient_context`, `data_a`, a user turn, or a visible image;
- oracle notes add no factual answer;
- turns are one-based and contiguous;
- exactly three cases have three turns; every other case has one turn;
- all people and organizations are fictional;
- Green controls contain no missing material answer and no independent Red/Yellow trap.

The designer attestation records cloud context, model metadata when available, branch, commit, exact files read, image hashes, the chosen domain and why it is not denylisted, an explicit statement that V322-017 is the only non-manager recipient, and that no other repository content was accessed.
