# Workplace Survival Output Formats

Use the applicable format exactly in the listed section order. Keep the instructions in this file in English, but render user-facing headings and fixed status text in the user's current language. Keep the revised message in the language, script, and register of Data B unless the user requests otherwise.

## Intake format

Use this format when a review cannot start because Data A, Data B, A/B classification, a sendable-body boundary, or material image confirmation is required:

```markdown
## Information needed

- Missing: [Data A / Data B / A-B classification / sendable-body boundary / image confirmation]
- Next step: [the exact information or confirmation the user must provide]
```

Do not include ratings, inferred facts, or a revision in an intake response.

## Review format

Use this format for the first review and every follow-up review:

```markdown
## Mode

[Normal mode / Limited-background mode]

## Background understanding

- [Current confirmed Data A relevant to Data B, followed by any required Data B provenance entries]

## Ratings

### Responsibility clarity

- Rating: [Green / Yellow / Red / Gray]
- Evidence: [specific evidence from Data A or Data B, or the exact missing information]
- Communication risk: [specific risk, or "None found"]

### Tone

- Rating: [Green / Yellow / Red / Gray]
- Evidence: [specific evidence from Data B, or the exact missing information]
- Communication risk: [specific risk, or "None found"]

### Overall status

- Rating: [Green / Yellow / Red / Gray]
- Next action: [No revision needed / Minimal revision recommended / Revision required / More information required]

## Confirmation needed

1. Question: [neutral material question]
   - Affected dimension: [Responsibility clarity / Tone]
   - Why this matters: [how the answer can change the assessment or safe revision]
   - Neutral answer structure: [fill-in structure or balanced neutral options]

## Minimal revision

[revised message or fixed no-revision/unavailable text]
```

Apply these fixed values:

- If no material question remains, write `None` under `Confirmation needed`.
- If both dimensions are green, write `No revision needed` under `Minimal revision`.
- If missing information prevents any safe revision, write `Not provided — answer the questions above first`.
- If a partial revision is safe, use clear descriptive placeholders for unresolved required information.
- When Data B contains embedded content, add `Evaluated Data B: [verbatim new body]` and `Excluded from evaluation: [quoted / forwarded / reply-header / original-message / chat-preview content]` under `Background understanding`.
- Identify the excluded content type without reproducing it as Data A.
- When mixed text was safely auto-classified, add `Adopted Data A: [verbatim background payload]` and `Evaluated Data B: [verbatim new body after embedded-content exclusions]` under `Background understanding`.
- Semantic role labels identify boundaries but are not part of either payload unless the user explicitly includes them.
- If auto-classified Data B contains embedded content, use one `Evaluated Data B` entry for the new body and one `Excluded from evaluation` entry for the embedded content; do not add a second evaluated-draft entry.

## Normal review

Use the full review format with these required values:

- Set `Mode` to `Normal mode`.
- Under `Background understanding`, include confirmed Data A relevant to the current Data B. Required `Evaluated Data B` and `Excluded from evaluation` entries are provenance metadata, not Data A.

## Limited-background review

Use the full review format with these required values:

- Set `Mode` to `Limited-background mode`.
- Start `Background understanding` with `Data A was not provided; this review assesses Data B only`.
- Add `Manager-requirement alignment: Not assessed — Data A was not provided`.

## Message-template format

Use this format only in message-template mode:

```markdown
## Message template

[message containing clear descriptive placeholders for every unknown value]

## Information to fill

- [required missing value]
```

Do not include ratings, overall status, evidence, communication risk, or claims that the template satisfies the manager's requirements. If no case-specific background is available, keep the template generic and neutral.

## Image-based Data B

When Data B comes from an image and the draft is reliably identifiable, add this entry under `Background understanding`:

```markdown
- Recognized Data B:

  > [verbatim text of the unsent draft that was evaluated]
```

Include only the identifiable unsent draft. Do not include application interface text, notifications, or unrelated conversation. If the draft region or material wording is uncertain, use the intake format to request image confirmation instead of producing a review.

## Follow-up review

After the user provides background, answers a question, corrects Data A, or submits a revised Data B, reuse the complete review format in the same section order.

- Replace `Background understanding` with the latest confirmed case background.
- Display the latest rating for both dimensions, even when only one changed.
- Recalculate and display the overall status.
- Include only material questions that remain unresolved; write `None` when none remain.
- Update `Minimal revision` using the latest Data A and Data B.
- Do not retain superseded facts, stale ratings, resolved questions, or an older revision.
- If the user supplied a new Data B, review that message rather than the prior draft.

