# Workplace Survival — Product Specification

## 1. Purpose

Workplace Survival reviews a work message before the user sends it to a manager. It uses user-provided background to:

- assess responsibility clarity;
- assess tone;
- identify concrete communication or execution risks;
- ask focused, neutral follow-up questions;
- make only the minimum necessary revision.

The skill reviews communication against supplied information. It does not verify real-world facts or predict the manager's reaction.

## 2. Document authority

This file owns product intent, scope, and non-negotiable behavior. A behavior change starts here.

Runtime ownership is deliberately split to avoid repeating the same rule:

- `.cursor/skills/workplace-survival/SKILL.md` owns routing and workflow;
- `.cursor/skills/workplace-survival/REFERENCE.md` owns detailed semantics and rating boundaries;
- `.cursor/skills/workplace-survival/FORMATS.md` owns exact output structures and fixed text;
- `.cursor/skills/workplace-survival/EXAMPLES.md` contains non-normative examples only;
- `tests/TEST_CASES.md` owns acceptance assertions and recorded coverage boundaries.

Lower-level files may implement this contract but must not expand product scope. If they conflict with this file, stop and resolve the specification before changing behavior.

## 3. Inputs and modes

### Data A

Data A is case-scoped background and the verification basis for Data B. Known requirements include only facts explicitly supplied or confirmed by the user.

Assistant suggestions, workplace conventions, unstated context, inferred intent, and facts found only in Data B are not Data A.

### Data B

Data B is the identifiable message the user intends to send. It is content under review, not evidence that verifies itself.

Data B is required for a review. Plain text is preferred; a screenshot containing a clearly identifiable unsent draft is also accepted.

### Modes

- **Normal mode:** requires Data A and identifiable Data B.
- **Limited-background mode:** requires explicit user confirmation after the user cannot or will not provide Data A. It assesses Data B only and does not assess alignment with the manager's original requirements.
- **Message-template mode:** requires an explicit template request. It produces no ratings and uses placeholders for every unknown case value.

Do not rate while required input or a material input boundary is unresolved.

## 4. Product behavior

### Evidence and isolation

- Base every finding, question, and revision only on Data A, Data B, or explicit user confirmation.
- Never invent a date, person, owner, responsibility, progress value, commitment, or manager intent.
- Keep Data A scoped to one work matter and its Data B revisions.
- Do not carry background, answers, ratings, or commitments into a different case.
- Ask for classification when it is unclear whether new input is background, a revised draft, or a new case.

### Images

- Use clearly legible image content only in the role identified by the user or visible structure.
- Display the recognized text when Data B comes from an image.
- Ask for confirmation only when identity, key wording, conversation order, crop, or draft boundaries are materially ambiguous.
- Never reconstruct cropped or illegible content.

### Ratings

Rate responsibility clarity and tone independently:

- **Green:** no contradiction, material omission, concrete risk, or necessary revision is found.
- **Yellow:** a concrete ambiguity or tone problem may cause misunderstanding, but available evidence does not show major execution risk.
- **Red:** direct evidence shows a contradiction, incorrect commitment, material omission, or major risk that must be corrected.
- **Gray:** information required to assess that dimension is missing or materially ambiguous.

Derive overall status with fixed priority: `red > gray > yellow > green`. Overall status states the next action and never replaces either dimension rating.

Do not rate a message yellow merely because it could be more polished, formal, detailed, or polite. Do not rate missing information red unless Data A explicitly requires it or the omission itself creates major execution risk.

### Short acknowledgements

A short acknowledgement may confirm one identifiable reply target containing clear, non-conflicting instructions that require acknowledgement rather than a factual answer. It does not prove execution, completion, or external verification.

Do not use this rule when the instruction requests a specific owner, date, progress value, choice, explanation, or other informational answer, or when the acknowledgement changes or limits the instruction.

### Follow-up questions

- Ask only questions whose answers can materially change a rating or safe revision.
- Ask no more than three questions per response.
- Use neutral wording and placeholders or balanced options; never steer the user toward a preferred answer.
- Do not repeat resolved questions or force questions when both dimensions are green.
- User-supplied answers and corrections update Data A; assistant-generated answer structures do not.

### Revisions

- Revise only issues identified by the ratings and evidence.
- Preserve Data B's purpose, language, script, register, and voice unless the user requests otherwise.
- Use descriptive placeholders for required unknown values; never fill them by inference.
- When both dimensions are green, provide no alternative rewrite.
- An assistant revision becomes Data B only after the user adopts, modifies, or resubmits it.

## 5. Output contract

Every review shows:

1. mode;
2. current background understanding;
3. separate responsibility-clarity and tone ratings with evidence and concrete risk;
4. overall status;
5. up to three material confirmation questions;
6. a minimal revision or the applicable no-revision/unavailable result.

Exact section order, fixed values, intake output, limited-background output, image disclosure, and template output are defined only in `.cursor/skills/workplace-survival/FORMATS.md`.

## 6. Distribution and triggering

- Runtime path: `.cursor/skills/workplace-survival/`.
- Personal installation path: `~/.cursor/skills/workplace-survival/`.
- Never install into Cursor's managed `~/.cursor/skills-cursor/` directory.
- The slug and frontmatter name are `workplace-survival`.
- Automatic invocation is limited to requests to check, revise, rewrite, or draft a work message intended for a manager.

## 7. Acceptance

A release is acceptable only when:

- runtime files respect the ownership split above;
- functional, anti-hallucination, interaction-quality, explicit-invocation, and auto-trigger suites pass;
- every normative change has a corresponding acceptance case;
- no example or process document introduces behavior absent from this specification;
- installation instructions and the publication manifest match the runtime file set.
