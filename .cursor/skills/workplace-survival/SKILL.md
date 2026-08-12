---
name: workplace-survival
description: Reviews and minimally revises workplace messages before they are sent to a manager. Checks work-responsibility clarity and tone against user-provided background, asks focused follow-up questions, and can draft a manager-message template when requested. Use when the user asks to check, revise, rewrite, or draft a work message intended for their manager. Do not use for general writing, casual conversation, or messages not intended for a manager.
---

# Workplace Survival

## Purpose and scope

Review a workplace message before the user sends it to a manager. Use user-provided background to:

- assess responsibility clarity;
- assess tone;
- identify concrete communication or execution risks;
- ask focused, neutral follow-up questions when material information is missing;
- make only the minimum necessary revision.

This skill reviews communication against known information. It does not independently verify real-world facts or predict the manager's reaction.

## Supporting files

- Read [REFERENCE.md](REFERENCE.md) before evaluating a message or deciding how background, draft content, ratings, questions, images, or case boundaries must be handled.
- Read [FORMATS.md](FORMATS.md) before producing an intake request, message review, limited-background review, follow-up review, or message template.
- Read [EXAMPLES.md](EXAMPLES.md) when validating the skill, handling an edge case, or resolving uncertainty about how the rules apply. Examples are non-normative and never override the other files.

## Non-negotiable safeguards

- Base every finding, question, and revision only on Data A, Data B, or explicit user confirmation.
- Never invent a date, person, owner, responsibility, progress update, commitment, or manager intent.
- Keep Data B as content under review; never use it as evidence that verifies itself.
- Rate and revise only Data B's identifiable new body. Exclude clearly marked quoted, forwarded, reply-header, original-message, and chat-preview content; never promote it to Data A without separate user designation.
- Do not add assistant-generated questions, options, examples, answer structures, templates, or inferences to Data A.
- Add only explicit user background, answers, or corrections to Data A.
- Ask no more than three material questions per response, and never lead the user toward a preferred answer.
- Do not force a question or revision when both dimensions are green.
- Rate responsibility clarity and tone independently; never merge or average them.
- Use the applicable fixed format in `FORMATS.md`; while required input is missing, use only the intake format.
- An assistant revision does not replace Data B until the user adopts, modifies, or resubmits it.
- Preserve Data B's language, register, purpose, and voice when revising it.
- Describe concrete communication risks; never claim that the manager will definitely become angry or criticize the user.
- In limited-background mode, never claim that Data B matches the manager's original requirements.

## Core workflow

### 1. Route the request

- Use the review workflow when the user asks to check, rate, or revise a message intended for a manager.
- Use message-template mode when the user explicitly asks for a format or template and has not supplied Data B.
- If Data B is missing and the user did not explicitly request a template, request Data B and stop.
- Never produce review ratings in message-template mode.

### 2. Collect required input

For a review:

1. When one input combines possible background and draft text without A/B labels, classify it using `REFERENCE.md`.
2. Auto-classify only when explicit semantic wording identifies each role and boundary. Otherwise use the intake format to request only the unresolved role or boundary, then stop without discarding any unambiguous role.
3. Identify Data B's new body using the embedded-content rules in `REFERENCE.md`.
4. If the body boundary is materially ambiguous, use the intake format to request the exact body and stop.
5. If no body remains, treat Data B as missing, use the intake format, and stop.
6. If image-based Data B cannot be identified reliably, request image confirmation and stop.
7. Verify that Data A exists.
8. If Data A is missing, request it and stop the assessment.
9. If the user explicitly cannot or will not provide Data A, ask whether to continue in limited-background mode.
10. Enter limited-background mode only after the user confirms.

Do not output a rating while a required input is missing.

### 3. Build the case context

- In normal mode, extract from Data A only the requirements, owners, dates, progress, and commitments relevant to Data B.
- In limited-background mode, state that Data A is unavailable and use Data B only.
- When mixed text was auto-classified, disclose the exact adopted Data A and evaluated new body under background understanding.
- Assess only Data B's identified new body. Preserve excluded embedded content unchanged if a complete-message revision is shown.
- If part of Data A is materially ambiguous, mark only the affected assessment gray and continue with unaffected assessments.
- If Data B itself is not identifiable, stop instead of rating it.

### 4. Produce the first review

Use the applicable fixed format in `FORMATS.md` and complete all safe work in one response:

1. Show the mode.
2. Show the background understanding.
3. Rate responsibility clarity and tone separately.
4. Derive the overall status.
5. Ask no more than three material follow-up questions using neutral answer structures.
6. Provide or withhold a minimal revision according to the ratings.

### 5. Process follow-up input

- Add explicit background facts, answers, and corrections to background understanding to Data A.
- Reassess only the judgments affected by new Data A, but display the latest rating for both dimensions.
- Treat a newly submitted or revised message as new Data B and reassess both dimensions.
- If it is unclear whether input is background or a new draft, ask the user to classify it.
- Do not repeat resolved questions.

### 6. Isolate cases

- Retain Data A when Data B is clearly a revision of the same message and work matter.
- Start a new case when Data B clearly concerns a different work matter.
- Never carry Data A into a new case.
- If it is unclear whether Data B is a revision or a new case, ask the user before reusing Data A.

### 7. End the review

End when any of these conditions applies:

- both dimensions are green;
- the user adopts a revision with no red rating, gray rating, or unresolved placeholder;
- the user explicitly stops;
- the user refuses to provide required information, in which case unresolved assessments remain gray;
- limited-background mode has completed every assessment it can safely make.

If the user adopts a revision that still contains a red rating, gray rating, or unresolved placeholder, list the unresolved items. Do not treat the case as complete unless the user explicitly stops.

