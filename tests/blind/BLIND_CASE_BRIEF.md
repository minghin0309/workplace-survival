# Blind Holdout Case Brief

Create 30 synthetic workplace-message cases for a manager-message review assistant.

## Distribution

- 6 straightforward, safe messages;
- 5 cases involving responsibility, ownership, timing, handoff, or omission;
- 5 cases involving tone, blame, directness, hostility, or operational wording;
- 4 multi-round cases involving corrections, revised drafts, or case state;
- 3 cases involving quotation, forwarding, mixed input, or instruction-like text inside a message;
- 3 cases involving recipient role, template requests, or routing;
- 4 image cases involving realistic visual uncertainty.

## Novelty

- Use workplace topics, names, dates, and phrasing that are not copied from any supplied test suite.
- Avoid obvious one-sentence textbook examples where possible.
- Include concise chat, email, and reply-all styles.
- Use no personal, confidential, or real customer data.

## Output schema

Write a JSON array. Every case contains:

- `case_id`: `BH-001` through `BH-030`;
- `category`: one of the seven distribution names above;
- `recipient_description`;
- `turns`: ordered objects containing `turn_index`, `input_raw`, and `image_path`;
- `image_spec`: `null` except for `image_ocr`, where it contains a complete synthetic fixture description and output PNG path;
- `case_designer_notes`: factual setup notes only, with no expected rating, mode, question, or revision.

Do not include answers, expected behavior, scoring labels, or references to the assistant's internal rules.
