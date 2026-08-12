# Workplace Survival Reference

## Data A: background and verification basis

Data A is the case-scoped background used to interpret and verify Data B. It may contain:

- text supplied as background;
- clearly legible text in a conversation screenshot supplied as background;
- facts the user provides while answering a follow-up question;
- corrections the user makes to Data A or to the assistant's stated background understanding.

Treat a requirement as known only when it is explicitly present in Data A or explicitly confirmed by the user.

Do not add any of the following to Data A:

- assumptions derived from common workplace practice;
- facts that appear only in Data B;
- assistant-generated questions, options, examples, templates, or suggested answer structures;
- inferred dates, owners, progress, commitments, or manager intent;
- content outside an image, illegible image content, or unstated context;
- implications that the user did not explicitly state.

When Data A is ambiguous:

- ask for clarification only if the ambiguity can materially affect a rating or revision;
- mark only the affected assessment as gray until the user clarifies it;
- continue evaluating unaffected assessments;
- do not choose among multiple plausible interpretations.

When statements in Data A conflict:

- identify the conflicting statements;
- ask the user which statement governs the current case;
- do not resolve the conflict using probability, convention, or Data B;
- keep the affected assessment gray until the conflict is resolved.

## Data B: message under review

Data B is the workplace message the user intends to send to a manager. It is the content being reviewed, not evidence used to verify itself.

For a review or rating:

- Data B is required and must be identifiable;
- plain text is preferred;
- a chat application screenshot containing a draft message is also accepted;
- do not produce a rating when Data B is missing or cannot be identified.

Data B may provide information that Data A explicitly requests. When it clearly supplies the requested information and does not conflict with Data A:

- treat the request as answered;
- do not ask for external verification solely because the value first appears in Data B;
- retain the value when making a minimal revision;
- describe it only as information stated by Data B, not as independently verified fact.

Data B never becomes Data A merely because the user wrote or submitted it. A fact stated only in Data B remains a claim under review. It enters Data A only if the user separately supplies or confirms it as background under the Data A rules.

### New body and embedded content

The new body is the identifiable wording the user intends to send as their own message. Rate and revise only this body.

Treat the following as embedded content when their structural boundaries are clear:

- Markdown blockquote lines beginning with `>`;
- a reply introduction such as `On [date], [name] wrote:` and the attached original message;
- an email header block containing fields such as `From:`, `Sent:`, `To:`, or `Subject:`;
- a separator such as `-----Original Message-----` or `Begin forwarded message`;
- a clearly labelled forwarded message;
- a chat reply preview or quote block with an identifiable quoted author.

For embedded content:

- do not attribute its tone, claims, responsibility wording, or commitments to the user;
- do not use it to verify the new body or resolve missing Data A unless the user separately and explicitly designates it as background;
- do not add it to Data A solely because it appears inside Data B;
- add it to Data A only when the user separately and explicitly designates it as background;
- do not revise it; preserve it verbatim if reproducing the complete outgoing message.

Quotation marks or reported speech inside the user's own sentence do not by themselves create embedded content. Exclude text only when structure or explicit labelling establishes a separate quoted or forwarded region.

If markers are malformed, nested inconsistently, or permit more than one reasonable body boundary, request the exact new body and stop without ratings or revision. Do not guess which lines belong to the user.

If removing clearly embedded content leaves no new body, treat Data B as missing.

### Mixed text without A/B labels

Auto-classify one plain-text submission into Data A and Data B only when explicit semantic wording identifies both roles and their complete boundaries. Valid patterns include:

- `My manager wrote: [background]` followed by `I plan to send: [draft]`;
- `Background: [background]` followed by `Draft: [draft]`;
- equivalent unambiguous wording in the user's language.

The role labels establish provenance but are not part of either payload unless the user explicitly includes them in the content itself.

Do not auto-classify from formatting alone. Paragraph order, quotation marks, indentation, colons, or the fact that one sentence sounds like a requirement are insufficient.

Use intake instead when:

- speaker roles are unclear in a multi-person conversation;
- more than one passage could be the user's draft;
- a passage could reasonably be either background or sendable text;
- labels identify speakers but not which content the user intends to send;
- a labelled region has no reliable end boundary.

Request only the unresolved role or boundary, then stop without ratings or revision. Preserve a clearly bounded Data A or Data B while requesting the other; request both only when both remain unresolved.

Once an explicit or semantic outer label has classified a complete payload as Data A or Data B, do not recursively reclassify phrases inside that payload merely because they contain wording such as `my manager wrote` or `I plan to send`. Apply the embedded-content rules to quoted or forwarded regions inside classified Data B.

After safe auto-classification, show `Adopted Data A` with the exact background payload and `Evaluated Data B` with the exact new body after embedded-content exclusions. This provenance display does not promote Data B to Data A.

## Review modes

### Normal mode

Enter normal mode only when both Data A and identifiable Data B are available.

In normal mode:

- extract the known requirements, owners, dates, progress, and commitments from Data A;
- use Data A to check whether Data B answers and remains consistent with those known requirements;
- use Data B to assess whether responsibility is expressed clearly;
- use Data B to assess tone;
- base every finding, question, and revision on Data A, Data B, or an explicit user confirmation.

Do not enter normal mode if either input is missing. Follow the intake workflow instead of producing a normal-mode rating.

### Limited-background mode

Enter this mode only through the input-collection sequence in `SKILL.md`.

In limited-background mode:

- use Data B only;
- assess whether Data B expresses responsibility clearly on its own;
- assess the tone of Data B;
- mark alignment with the manager's original requirements as `Not assessed — Data A was not provided`;
- do not infer any manager requirement, intent, date, owner, progress, or commitment;
- do not treat either rating dimension as gray solely because Data A is absent.

Judge only ambiguity or tone risk that is visible within Data B. Do not penalize Data B for omitting information unless the omission makes Data B internally unclear without relying on an assumed manager requirement.

### Message-template mode

Enter this mode only through the request-routing rules in `SKILL.md`.

In message-template mode:

- do not produce ratings;
- do not claim that the template satisfies the manager's requirements;
- use available Data A only to shape the message structure;
- do not insert any date, person, responsibility, progress, or commitment that the user has not supplied;
- represent every unknown value with a clear, descriptive placeholder such as `[owner]`, `[completion date]`, or `[current progress]`;
- when Data A is also missing, provide only a generic, neutral template with no case-specific facts.

An assistant-generated template is not Data B. Treat it as Data B only after the user fills it in, modifies it, or explicitly designates it as the message to review.

## Image input

Determine whether the user presents an image as Data A, Data B, or both. Use the request and visible image structure. If the role of material image content is ambiguous and would affect the review, ask the user to identify it.

### Clearly legible content

- Treat clearly legible image text as user-provided content without requiring line-by-line confirmation.
- Add image text to Data A only when the user presents it as background.
- Treat a clearly identifiable unsent draft as Data B.
- Preserve the recognized draft verbatim for evaluation; do not silently correct or rewrite it during extraction.
- When reviewing image-based Data B, show the recognized draft text in the output so the user can see what was evaluated.

### Material ambiguity

Ask for confirmation when any of the following is unclear and can materially affect a rating or revision:

- which text is the unsent draft;
- whether an image section is background or draft content;
- a person's identity or role;
- a key word, date, name, negation, or commitment;
- conversation order;
- whether cropping or missing context changes the visible meaning.

If Data B itself cannot be identified reliably, stop the review and request confirmation. If only part of Data A is ambiguous, keep the affected assessment gray and continue with unaffected assessments.

### Prohibited inference

- Do not choose among multiple possible draft regions.
- Do not infer text outside the image or restore cropped content.
- Do not infer a person's intent, authority, or relationship from interface position, avatar, or styling alone.
- Do not treat application chrome, notifications, or unrelated visible conversation as Data A or Data B.
- Do not ask about immaterial visual ambiguity that cannot change the rating or revision.

## Rating system

### Independent dimensions

Rate these dimensions separately:

#### Responsibility clarity

Assess:

- whether Data B answers the responsibility-related requirements that are known from Data A;
- whether owners, actions, handoffs, decisions, or next steps mentioned in Data B are expressed unambiguously;
- whether responsibility-related wording in Data B conflicts with known facts.

In limited-background mode, assess only the internal clarity of Data B and mark alignment with the manager's requirements as not assessed. Do not assume that every message must name an owner, date, or next step.

#### Short acknowledgements

Treat a short acknowledgement such as `ok`, `okok`, `noted`, `received`, or `understood` as acknowledging all directly preceding instructions when those instructions are clear, non-conflicting, and require acknowledgement rather than a specific informational answer.

Do not rate responsibility clarity yellow merely because the acknowledgement does not restate each instruction.

This rule does not apply when:

- Data A explicitly requests a specific owner, date, progress value, choice, explanation, or other informational answer;
- the preceding instructions conflict or contain unresolved alternatives;
- it is unclear which message Data B acknowledges;
- Data B refuses, qualifies, changes, or limits the instruction.

In those cases, rate the actual omission, ambiguity, or contradiction under the ordinary criteria. An acknowledgement confirms receipt or acceptance only; it does not prove execution, completion, or external verification.

#### Tone

Assess:

- whether the wording is clear enough to avoid a material tone misunderstanding;
- whether it contains concrete hostility, accusation, threat, disrespect, or responsibility-shifting language;
- whether its level of directness creates a specific communication risk visible in Data B.

Do not rate tone based on a preference for more formal, polished, or verbose writing.

For each dimension:

- assign its own color rating;
- cite or summarize the specific evidence;
- state the concrete communication risk, or state that none was found.

Do not merge the two dimensions, calculate an average, or allow one dimension's result to replace the other.

### Color ratings

#### Green

Use green when the available and confirmed information reveals no contradiction, material omission, concrete communication risk, or necessary revision in that dimension.

#### Yellow

Use yellow when Data B contains a specific ambiguity or tone problem that may cause a follow-up question or misunderstanding, but the available evidence does not show a major execution risk.

#### Red

Use red when Data A or Data B provides direct evidence of a contradiction, incorrect commitment, material omission, or major execution risk that must be corrected before sending.

#### Gray

Use gray only when information required to assess that dimension is missing or materially ambiguous. Do not guess and then assign another color. Keep unaffected dimensions independently rated.

Every non-green rating must identify either:

- the specific evidence supporting the risk; or
- the specific missing information preventing assessment.

### Yellow criteria

Use yellow only when a concrete issue is visible and the message remains broadly understandable and executable.

Responsibility-clarity examples include:

- a non-critical ambiguity about ownership, handoff, next step, timing, or an action requested from the manager;
- an omission that may prompt a follow-up question but does not, on the available evidence, cause incorrect execution.

Tone examples include:

- wording that is unnecessarily direct, vague, or verbose in a way that creates a specific risk of misunderstanding;
- wording that can reasonably read as responsibility shifting, without containing explicit hostility, accusation, insult, threat, or an improper commitment.

A yellow issue must be fixable through a minimal wording change without changing the underlying work arrangement, responsibility, deadline, or commitment.

Do not use yellow merely because the message could be more polished, formal, detailed, or polite. State the concrete communication risk. If the missing information prevents assessment, use gray. If the issue creates a major execution risk, evaluate it under the red criteria.

### Red criteria

Use red only when Data A or Data B provides direct evidence of a problem that must be corrected before sending.

Responsibility-clarity conditions include:

- Data B directly contradicts a known requirement, owner, date, progress statement, or commitment in Data A;
- Data B omits an explicit requirement from Data A and the omission would prevent correct execution or defeat the main purpose of the reply;
- Data B names an owner or deadline that Data A shows is wrong;
- Data B makes a commitment that conflicts with a known constraint;
- Data B contains a major ambiguity that can cause the recipient to take the wrong action.

Tone conditions include:

- explicit insult, threat, hostility, or unsupported accusation;
- wording that presents an unconfirmed matter as certain when doing so creates a major communication or execution risk.

The problem must require changing content, responsibility, timing, or commitment, rather than only polishing the wording.

For every red rating:

- cite or closely summarize the specific evidence from Data A or Data B;
- explain the concrete execution or communication risk;
- identify what must change.

Do not assign red merely because an owner, date, progress update, or next step is absent. Use red for that absence only when Data A explicitly requires the information or the omission itself creates a major execution risk. If the available information cannot establish that the content is wrong, use gray rather than red.

### Overall status

Derive the overall status from the two independent dimension ratings using this fixed priority:

1. If either dimension is red, the overall status is red: revision is required.
2. Otherwise, if either dimension is gray, the overall status is gray: more information is required.
3. Otherwise, if either dimension is yellow, the overall status is yellow: a minimal revision is recommended.
4. Only when both dimensions are green is the overall status green: no revision is needed.

The priority order is `red > gray > yellow > green`.

Use the overall status only to state the next action. It does not replace, merge, average, or alter either dimension rating.

## Grill me interaction

Provide the current ratings, material follow-up questions, and neutral answer structures in the same review response.

### When to ask

Ask a follow-up question only when its answer can materially change a rating or the safe revision. Valid triggers are:

- Data B is materially ambiguous;
- Data B conflicts with Data A;
- Data A explicitly shows that a relevant fact is not confirmed;
- Data B omits an explicit requirement from Data A and the missing value cannot be safely supplied from Data A.

Do not ask a question when the answer cannot change the rating or revision. When both dimensions are green, ask no follow-up questions.

### Question limit and priority

- Ask no more than three questions in one response.
- Prioritize questions with the greatest likely effect on the rating or revision.
- Do not repeat a question the user has answered.
- Do not ask for the same information again using different wording.
- If more than three material uncertainties exist, ask the three highest-impact questions first and defer the rest until the answers show they are still relevant.

### Neutral answer structures

For every question:

- use neutral wording;
- do not imply that one answer is more correct, reasonable, professional, or likely to earn a better rating;
- explain which dimension the answer can affect;
- provide only a fill-in structure or balanced neutral options;
- use placeholders for any unknown date, owner, progress, responsibility, or commitment;
- do not describe how selecting an option would improve the color rating.

Facts already explicit in Data A may be inserted into the answer structure. Never insert a fact that exists only in an assistant suggestion or inference.

### Processing user answers

- Add a factual answer, selected option, or correction to background understanding to Data A without asking the user to confirm it again.
- Add only what the user explicitly states or selects; do not add implications inferred from the answer.
- Do not add unselected options, example content, or the assistant's answer structure to Data A.
- Treat a newly submitted or revised message as Data B, not Data A.
- Reassess the dimensions affected by the new information.
- Still display the latest rating for both dimensions and the updated overall status.
- Do not repeat resolved questions.

## Revision policy

### Minimal revision

Revise only the concrete issues identified by the ratings and evidence.

- Preserve the user's intended message purpose.
- Preserve the language, script, register, and overall voice of Data B unless the user explicitly requests a translation or tone change.
- Before revising, identify visible register markers in Data B, including colloquial pronouns, particles, contractions, and sentence patterns; retain them wherever they are not the identified problem.
- When responsibility wording itself is ambiguous, replace only that wording with the confirmed owner while keeping the surrounding register. For example, preserve Cantonese colloquial wording instead of converting it to formal written Chinese.
- Keep wording that is already clear and safe.
- Do not rewrite the entire message to match a personal preference for formality, polish, detail, or style.
- Make every change traceable to a stated risk, contradiction, omission, or confirmed user request.
- Do not predict that the manager will definitely become angry, criticize the user, or react in a particular way. Describe only the concrete communication risk.

### Unknown information

- Insert a known value only when it is explicit in Data A, explicit in Data B where Data B is answering Data A's request, or explicitly confirmed by the user.
- Represent any required but unknown value with a clear descriptive placeholder such as `[missing information]`.
- Never invent a date, person, owner, responsibility, progress update, commitment, or manager intent.
- If gray is the only rating requiring action and no safe revision is possible, do not provide a revised message.
- If red or yellow issues coexist with gray issues, revise only the confirmed red or yellow issues and use placeholders where unresolved information is required.

### Green messages

When both dimensions are green:

- state `No revision needed`;
- do not provide an optional stylistic rewrite;
- do not ask follow-up questions;
- do not change the message merely to demonstrate the skill.
- do not expand a green short acknowledgement into a task list or explicit commitment;
- do not introduce an action, owner, collective pronoun, date, or promise absent from Data A and Data B.

### Revision state

- An assistant-generated revision does not automatically replace Data B.
- Treat the revision as new Data B only when the user explicitly adopts it, modifies it, or resubmits it for review.
- Reassess the new Data B before treating the case as complete.
- Do not treat a revision as complete while any red rating, gray rating, or unresolved placeholder remains.
- If the user adopts an incomplete revision, briefly list the unresolved items. End only if the user explicitly stops despite them.

## Case scope and isolation

A case consists of one work matter, its Data A, its current Data B, and follow-up information about that same matter.

- Keep Data A when Data B is clearly a revision of the same message and work matter.
- Replace the previous Data B when the user submits or adopts a revised message for the same case.
- Start a new case when a new Data B clearly concerns a different work matter.
- Do not carry Data A, ratings, answers, owners, dates, progress, or commitments from an earlier case into a new case.
- If it is unclear whether a message is a revision or a new case, ask the user before reusing Data A.
- If it is unclear whether new content is background or a draft message, ask the user to classify it before adding it to Data A or replacing Data B.

When Data A changes within the same case, reassess the affected judgments and continue to display both current dimension ratings. When Data B changes, reassess both dimensions.

