# Benchmark v2 Case Brief

Create 18 novel synthetic manager-message cases with IDs `V2-001` through `V2-018`.

Exact case schema:

- `case_id`;
- `category`;
- `recipient_context`;
- `data_a`: every fact available to the Skill;
- `turns`: 1-based `turn_index`, `input_raw`, optional `image_path`;
- `image_spec`: null or a PNG specification.

Do not include `case_designer_notes`.

Write separate `oracle-notes.json` records containing only:

- `case_id`;
- `design_intent`;
- `difficulty_notes`.

Oracle notes must not contain factual background used for ratings.

Use novel domains, names, facts, and language not copied from repository tests or prior holdouts. All content is synthetic.
