# Benchmark v3.3 Attempt-1 Blind Case Construction Brief

Create a fresh synthetic holdout with 18 cases (`V33-001` through `V33-018`) and exactly 24 turns. Do not reuse any v1, v2, v3, v3.1, v3.2-attempt-1, v3.2-attempt-2, or v3.2-attempt-3 domain, name, figure, date, message, image, sentence pattern, or answer fixture.

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
- concert pedal-harp restringing, harpworks, gut strings, pedal-rod regulation, humidity cabinets for harps;
- hot-air balloons, aerostats, envelope halls, gore cutting, load tapes, rip panels, hangar-card tensioning, mouth-tape restitch, certificated cubic-foot envelopes;
- cold-cathode neon/argon tube works, bombard stations, electrode splicing, mercury dosing, pumping manifolds, ribbon burners, rare-gas fill logs.

Also avoid generic ceramics, pottery, kiln-production, glaze, clay, and co-operative variants.

Do not reuse or respell these prior holdout entities:

- Quillsmere, Marit Osgarde, Ferrowhite, Marchmont Enclosure, Ashvale Bridal, Menkes Blockworks, Bellhouse Yard, Ardhu Lane, Thurlow & Vane, Solberg Straw, Cranthorpe, Havelock;
- Ilex & Norrish, Coppice Loft, Grellhaven, Vellum Court, Braxton-Yew, Padraig Orliss;
- Vantsel, Corrindale, Halvern, Kelbrand, Tessaly, Ostrelle, Brandmoor, Halbrook, Fennmark, Vallonde, Rjukan, Marisco, Alderhoff, Tarnwick, Cavallini, Ashcombe, Halvard;
- Kestrel Freight, Umber & Kiln, Vireo Valley, Lantern Row, Basalt Deep, Anvil Ridge, Static Meridian, Pawline, Grey Halyard, Foxglove Records, Chanterelle Systems, Northbell Mutual, Saltmark Trust, Halcyon Skyway, Ovenwright, Tern Hollow, Brindle Marionette, Fathom Line;
- Thornwick Aerostat Works, Spindlefen Hangar, Envelope Hall, Saira Vennick, Bram Cotrell, Ivo Drellan, Mirelle Oatswell, Pell Oswaithe, Wardenmere Sightseeing, Pellwick Balloon Club, Brackfen Ripstop, lots RN-7602 RN-7609 RN-7741, envelopes TW-441 TW-508 TW-512 TW-519 TW-530 TW-547 TW-561 TW-574 TW-588;
- Greaveholt Cold-Cathode Works, Nine-Rib Bench, Yarrowbridge, Orrin Medwick, Lise Cardenoy, Niall Peveril, Tamsin Quelch, Kerr Adelune, Sablewick Tea Rooms, Parquet Room bookshop, Duskletter Outfitters, Wintle Chemists, Coppervine Cycles, jobs CC-3304 through CC-3432, packing note PN-19.

Choose one fictional workplace shared across all 18 cases. It must not match or rename a denylisted domain.

## Manager-recipient invariant

This is a hard construction gate.

- `V33-017` is the only recipient-routing case. Its `recipient_context` must **not** be a manager recipient.
- Every other case, including `V33-004`–`V33-009` and `V33-018`, must be a manager recipient:
  - `relationship_to_user` exactly `direct line manager`;
  - `audience_scope` exactly `manager only`;
  - `additional_recipients` exactly `[]`;
  - `recipient_role` is a non-empty string containing `manager` and none of: `not a manager`, `non-manager`, `non manager`, `not the sender's manager`.

Do not send Green controls, question candidates, responsibility/tone cases, three-turn cases, or the image-only draft to a colleague, supplier, client, librarian, or distribution list.

## Distribution

- V33-001–V33-003: Green controls;
- V33-004–V33-009: required-question candidates;
- V33-010–V33-011: responsibility boundaries;
- V33-012–V33-013: tone boundaries;
- V33-014–V33-016: three-turn correction/state cases;
- V33-017: recipient-routing case (the only non-manager recipient);
- V33-018: clearly readable image-only responsibility/tone case addressed to the manager.

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
- the draft **omits** that answer; do not invent a Data B-only token that pretends to supply it;
- set `"data_b_contains_unconfirmed_token": false`;
- an explicit recipient requirement or decision depends on that answer;
- the message cannot safely satisfy its main purpose by qualification, omission, or a placeholder;
- providing the answer enables a complete safe message;
- removing the dependency makes the question unnecessary;
- no independent direct Red contradiction, unsafe commitment, accusation, hostility, prompt injection, or recipient-scope defect is present;
- no second unrelated unknown competes with the primary concept;
- the writer holds the missing answer, so asking is productive.

At least one candidate uses an image-only draft. Prefer geometrically obliterating a **Data A / background** token (`"occluded_role": "data_a"`) so the sendable draft region stays readable. Do not obliterate a Data B sendable-body token unless you set `"occluded_role": "data_b"` (that case gold-routes Intake and is not a Normal-mode review). Image-only candidates must set `occluded_role` to exactly `data_a`, `data_b`, or `none`. Non-image candidates omit `occluded_role` or set `none`.

The occluded value must not appear in text fields and must never be rendered as glyphs. Obliterate it geometrically. Do not open or inspect the resulting PNG as an image; hash the bytes only.

## Outputs

Write all of the following under `tests/benchmark/v3_3-holdout/cloud-cases/`:

- `cases.json`;
- `oracle-notes.json`;
- `question-design.json`;
- `construction-mutations.json`;
- deterministic PNGs under `cloud-cases/images/`;
- `designer-attestation.json`.

`question-design.json` is never available to gold labelers or SUT contexts.

## Envelope schema

Use this exact SUT-visible shape. Do not add gold labels, expected ratings, expected questions, or construction predicates to `cases.json`.

```json
{
  "envelope_version": "v3.3",
  "suite_id": "v33-holdout-cloud-attempt1",
  "case_count": 18,
  "turn_count": 24,
  "fictional_entities": true,
  "notice": "All organisations, people, jobs, suppliers, clients, references and figures below are fictional.",
  "cases": [
    {
      "case_id": "V33-001",
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
          "turn_id": "V33-001-T1",
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

Oracle-note and question-design shapes match attempt 3 (`candidates` are required). Candidate `case_id` values are exactly `V33-004` through `V33-009`. Each candidate has `base_state` and three mutations: `REMOVE_DEPENDENCY`, `SUPPLY_ANSWER`, `ADD_DOMINANT_RED`. The image-only candidate must set `"image_only": true` and `"occluded_role"`. Absent-answer tokens and `answer_fixture` must not appear in `cases.json`, oracle notes, or PNG pixel strings.

`construction-mutations.json` is a flattened mutation table with exactly 18 rows, three per question candidate, `schema_version` `v3.3`, `artifact` `construction-mutations`, `suite_id` `v33-holdout-cloud-attempt1`. Each row has `case_id`, `mutation_type`, `before_state`, and `after_state`. `before_state` copies that candidate's `base_state`. `after_state` copies that mutation's `resulting_state`.

## Images

- Use deterministic local rendering (Pillow + DejaVu, no random source, no timestamp chunk).
- Image drafts appear only in pixels.
- V33-018 is clearly readable throughout, tests responsibility/tone, and is addressed to the manager.
- At least one question candidate is image-only as specified above.
- Do not open PNGs as images after writing them.

## Invariants

- every fact available to the SUT appears in `recipient_context`, `data_a`, a user turn, or a visible image;
- oracle notes add no factual answer;
- turns are one-based and contiguous;
- exactly three cases have three turns; every other case has one turn;
- all people and organizations are fictional;
- Green controls contain no missing material answer and no independent Red/Yellow trap.

The designer attestation records cloud context, model metadata when available, branch, commit, exact files read, image hashes, the chosen domain and why it is not denylisted, an explicit statement that V33-017 is the only non-manager recipient, `occluded_role` for any image-only question candidate, and that no other repository content was accessed.

Do not push `cursor/blind-v33-holdout-17a0`. If you name a branch, use `cursor/v33-attempt1-cases-<shortid>-17a0`.
Open a draft PR with base `cursor/blind-v33-holdout-17a0`. Do not put cursor.com agent URLs in the PR body. Do not merge this branch.
