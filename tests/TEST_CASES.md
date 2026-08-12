# Workplace Survival Test Cases

These cases verify the normative behavior in `.cursor/skills/workplace-survival/`. Run each case in a fresh chat unless its `State` explicitly identifies a multi-round or existing-case test.

## Execution rules

- Invoke `workplace-survival` explicitly because model invocation is disabled during development.
- Submit the input exactly as written.
- Judge semantic behavior, not exact prose, except where a fixed value from `FORMATS.md` is required.
- A case passes only when every assertion under `Expected` is true and every item under `Forbidden` is absent.
- Record actual results separately during Phase 10. Do not modify expected results to match an incorrect actual response.
- For image cases, create or attach an image containing exactly the elements described under `Visual fixture`; the described layout and legibility are part of the test input.

## T9.1 — Input and mode routing

### TC-01 — Missing Data B

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked me to provide the deployment owner and completion date.
```

**Expected**

- Uses the intake format.
- Identifies only Data B as missing.
- Requests the message intended for the manager.
- Produces no mode rating, dimension rating, overall status, or revision.

**Forbidden**

- Inventing Data B.
- Entering message-template mode without an explicit template request.
- Requesting Data A again.

### TC-02 — Missing Data A

**State:** New case.

**Input**

```text
Use workplace-survival to review this message to my manager.
Data B: Alex will send the report tomorrow.
```

**Expected**

- Uses the intake format.
- Identifies Data A as missing.
- Requests relevant background and stops the assessment.
- Produces no rating or revision.

**Forbidden**

- Entering limited-background mode automatically.
- Inferring manager requirements from Data B.

### TC-03 — User refuses Data A

**State:** Continue TC-02 after the intake response.

**Input**

```text
I cannot provide Data A.
```

**Expected**

- Asks whether the user wants to continue in limited-background mode.
- Produces no rating before confirmation.

**Forbidden**

- Treating refusal as confirmation.
- Claiming that Data B meets the manager's requirements.

### TC-04 — User confirms limited-background mode

**State:** Continue TC-03 after the confirmation question.

**Input**

```text
Yes, continue in limited-background mode.
```

**Expected**

- Sets the mode to limited-background mode.
- States that Data A was not provided.
- Marks manager-requirement alignment as not assessed.
- Rates Data B's internal responsibility clarity green.
- Rates tone green.
- Sets overall status to green.
- States `No revision needed`.

**Forbidden**

- Marking either dimension gray solely because Data A is absent.
- Claiming compliance with the manager's original requirements.

### TC-05 — Explicit template request without Data B

**State:** New case.

**Input**

```text
Use workplace-survival to give me a message template.
Data A: My manager asked for the task owner, current progress, and expected completion date.
I have not written Data B.
```

**Expected**

- Enters message-template mode.
- Provides placeholders for owner, current progress, and completion date.
- Lists the information the user must fill in.
- Produces no ratings.

**Forbidden**

- Inventing any case value.
- Claiming that the unfilled template satisfies the manager's requirements.
- Treating the generated template as Data B.

## T9.2 — Normal-mode ratings

### TC-06 — Full alignment is green

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked who owns the report and when it will be delivered. Alex is the confirmed owner and Friday is the confirmed delivery date.
Data B: Alex owns the report and will deliver it on Friday.
```

**Expected**

- Uses normal mode.
- Rates responsibility clarity green.
- Rates tone green.
- Sets overall status to green.
- Asks no questions.
- States `No revision needed`.

**Forbidden**

- Providing an optional rewrite.
- Adding requirements not present in Data A.

### TC-07 — Requested owner supplied by Data B

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked for the name of the person responsible for the report.
Data B: Alex is responsible for the report.
```

**Expected**

- Uses normal mode.
- Treats the manager's request as answered.
- Rates both dimensions and overall status green.
- Describes Alex only as the owner stated in Data B.
- Does not ask for external verification solely because the name first appears in Data B.

**Forbidden**

- Adding Alex to Data A.
- Claiming that Alex's role was independently verified.

### TC-08 — Known owner and date contradiction is red

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Jamie is the confirmed owner. The confirmed deadline is 15 August.
Data B: Alex will complete it by 18 August.
```

**Expected**

- Uses normal mode.
- Rates responsibility clarity red.
- Rates tone green.
- Sets overall status to red.
- Cites both the owner and date contradictions.
- Requires correction before sending.

**Forbidden**

- Downgrading the direct contradictions to yellow.
- Treating either Data B value as verified Data A.

### TC-09 — Non-critical ambiguity is yellow

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Sam prepares the draft, then Lee performs the final check.
Data B: We will review it and send it tomorrow.
```

**Expected**

- Uses normal mode.
- Rates responsibility clarity yellow.
- Rates tone green.
- Sets overall status to yellow.
- Identifies `we` as the concrete ownership or handoff ambiguity.
- Recommends only a minimal wording change.

**Forbidden**

- Assigning red without evidence of major execution risk.
- Rewriting unrelated content.

### TC-10 — Missing governing information is gray

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: One manager note says Morgan owns the task. Another manager note says Taylor owns it. I do not know which instruction is current.
Data B: Morgan will complete the task.
```

**Expected**

- Uses normal mode.
- Rates responsibility clarity gray.
- Rates tone green.
- Sets overall status to gray.
- Identifies the conflicting Data A statements.
- Asks which owner governs the current case.

**Forbidden**

- Resolving the conflict using Data B, ordering, probability, or workplace convention.
- Presenting either owner as confirmed.

## T9.3 — Grill me interaction

### TC-11 — Material omission triggers a neutral question

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager explicitly requested the task owner. No owner has been confirmed.
Data B: Here is the project update.
```

**Expected**

- Rates responsibility clarity red, tone green, and overall status red because the sole explicit owner request is unanswered.
- Asks who the task owner is.
- Identifies responsibility clarity as the affected dimension.
- Explains that the answer affects whether the explicit request is answered.
- Provides a neutral fill-in structure such as `[owner]`.

**Forbidden**

- Suggesting a specific person.
- Implying which answer would produce a better rating.

### TC-12 — Maximum three questions per response

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager explicitly requested the owner, deadline, current progress, blocker, and next action. None of these values has been confirmed.
Data B: Here is the update.
```

**Expected**

- Rates responsibility clarity red, tone green, and overall status red because Data B supplies none of the explicitly requested substantive answers.
- Asks no more than three questions.
- Prioritizes questions that most affect the rating or safe revision.
- Defers lower-impact uncertainties.

**Forbidden**

- Asking four or five questions in the same response.
- Combining multiple independent questions into one numbered question to evade the limit.

### TC-13 — Suggested answers contain no unknown facts

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked for the owner and deadline. Neither value is known.
Data B: The task is in progress.
```

**Expected**

- Rates responsibility clarity red, tone green, and overall status red because neither explicitly requested value is answered.
- Uses placeholders or balanced neutral options.
- Keeps both owner and deadline unknown in the answer structures.

**Forbidden**

- Supplying a name, date, progress value, or commitment.
- Presenting an assistant example as known background.

### TC-14 — User answer is added to Data A

**State:** First run TC-11, then continue the same case.

**Input**

```text
Alex is the task owner.
```

**Expected**

- Adds only `Alex is the task owner` to the case's Data A.
- Reassesses the affected judgment.
- Displays the latest ratings for both dimensions and the latest overall status.
- Does not request confirmation of the same fact.

**Forbidden**

- Adding inferred duties, dates, progress, or commitments for Alex.
- Treating the answer as a replacement Data B.

### TC-15 — Resolved question is not repeated

**State:** Continue TC-14 in the same case.

**Input**

```text
Data B: Alex owns the task.
```

**Expected**

- Treats the message as new Data B.
- Reassesses both dimensions.
- Does not ask who owns the task again.

**Forbidden**

- Repeating the resolved owner question with different wording.
- Retaining stale ratings from the prior Data B.

## T9.4 — Revision policy

### TC-16 — Yellow receives only a minimal revision

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Sam prepares the draft. Lee performs the final check.
Data B: We will review it and send it tomorrow.
```

**Expected**

- Changes only the ambiguous ownership or handoff wording.
- Preserves `tomorrow` and the original message purpose.
- Does not alter the underlying work arrangement.

**Forbidden**

- Rewriting the entire message for style.
- Adding new owners, dates, progress, or commitments.

### TC-17 — Red contradiction uses confirmed correction

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Tuesday is the confirmed deadline.
Data B: I will finish this on Thursday.
```

**Expected**

- Rates responsibility clarity red.
- Identifies the direct deadline contradiction.
- Minimally revises Thursday to Tuesday.

**Forbidden**

- Preserving the known-wrong deadline.
- Changing unrelated wording.

### TC-18 — Unknown required value uses a placeholder

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager requires an expected completion date, but no date has been confirmed.
Data B: I am handling the task and will update you when it is complete.
```

**Expected**

- Rates responsibility clarity red, tone green, and overall status red because the sole required completion date is unanswered.
- Asks for the expected completion date.
- Uses `[expected completion date]` or an equally descriptive placeholder if a partial revision is safe.
- Does not treat the placeholder-bearing revision as complete.

**Forbidden**

- Inventing a date.
- Hiding or removing the unresolved requirement.

### TC-19 — Green produces no alternative draft

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked for the owner. Alex is the confirmed owner.
Data B: Alex owns the task.
```

**Expected**

- Rates both dimensions and overall status green.
- Writes `No revision needed` under minimal revision.
- Asks no follow-up questions.

**Forbidden**

- Providing an optional, polished, or more formal alternative.

### TC-20 — Language and register are preserved

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: 阿明負責整理資料，我負責提交。
Data B: 我哋搞掂之後會交。
```

**Expected**

- Keeps the revision in Cantonese written Chinese.
- Preserves the informal register.
- Clarifies only who prepares and who submits.

**Forbidden**

- Translating the revision into English.
- Converting it into formal written Chinese without a user request.
- Adding a date or new commitment.

## T9.5 — Image input

### TC-21 — Clear image draft is displayed and rated

**State:** New case.

**Visual fixture**

- One clearly identifiable unsent draft box contains `Priya owns the deployment.`
- The text is fully legible.
- Application controls, a battery notification, and older unrelated messages are also visible.

**Accompanying input**

```text
Use workplace-survival to review the unsent draft in this image.
Data A: My manager asked for the deployment owner. Priya is the confirmed owner.
```

**Expected**

- Uses normal mode.
- Shows `Priya owns the deployment.` verbatim as recognized Data B.
- Rates responsibility clarity, tone, and overall status green.
- Ignores interface text and unrelated conversation.

**Forbidden**

- Silently correcting the recognized draft during extraction.
- Including application controls or unrelated messages as Data B.

### TC-22 — Multiple possible drafts require confirmation

**State:** New case.

**Visual fixture**

- Two separate unsent draft boxes are visible.
- Draft one reads `Alex will send it Friday.`
- Draft two reads `Jamie will send it Monday.`
- Neither draft is visually or verbally identified as the target.

**Accompanying input**

```text
Use workplace-survival to review my draft in this image.
Data A: The manager asked for the owner and date.
```

**Expected**

- Uses the intake format.
- Requests confirmation of which draft should be reviewed.
- Produces no ratings or revision.

**Forbidden**

- Choosing either draft.
- Combining both drafts.

### TC-23 — Materially unclear identity requires confirmation

**State:** New case.

**Visual fixture**

- A background conversation clearly says `You own the handoff.`
- The visible participants are labelled only `Person 1` and `Person 2`.
- The conversation direction, avatars, and styling do not reliably establish who `You` identifies.

**Accompanying input**

```text
Use workplace-survival to review this message.
Data B: Jordan will handle the handoff.
The image is Data A.
```

**Expected**

- Keeps responsibility clarity gray.
- Asks for the identity or role needed to interpret `You`.
- Continues the unaffected tone assessment.

**Forbidden**

- Inferring identity from avatar, side of screen, color, or interface position.
- Using Data B to resolve the Data A ambiguity.

### TC-24 — Immaterial interface ambiguity causes no question

**State:** New case.

**Visual fixture**

- One clearly identifiable draft reads `Priya owns the deployment.`
- A partially cropped battery notification is illegible.
- The notification is visually separate from the draft and conversation.

**Accompanying input**

```text
Use workplace-survival to review the unsent draft.
Data A: Priya is the confirmed deployment owner.
```

**Expected**

- Reviews the draft without asking about the notification.
- Excludes the notification from Data A and Data B.

**Forbidden**

- Requesting confirmation of immaterial interface text.
- Delaying the review because of the notification.

### TC-25 — Cropped content is not reconstructed

**State:** New case.

**Visual fixture**

- A clearly identifiable draft reads `Alex owns the report.`
- The image ends immediately below the draft.
- No deadline appears anywhere in the image.

**Accompanying input**

```text
Use workplace-survival to review the unsent draft.
Data A: My manager asked only for the report owner.
```

**Expected**

- Evaluates only the visible draft and supplied Data A.
- Rates both dimensions and overall status green.
- Does not ask for or infer content outside the crop because it is immaterial to the known requirement.

**Forbidden**

- Reconstructing a deadline or additional sentence.
- Assuming that cropped content exists.

## T9.6 — State and case isolation

### TC-26 — Same-case revision reuses Data A

**State:** Existing case.

**Existing context**

```text
Data A: Alex owns the report. Friday is the confirmed deadline.
Current Data B: We will send it soon.
```

**Input**

```text
Here is my revised message: Alex will send the report on Friday.
```

**Expected**

- Treats the input as replacement Data B in the same case.
- Reuses the existing Data A.
- Reassesses both dimensions.
- Rates both dimensions and overall status green.

**Forbidden**

- Requesting the same Data A again.
- Retaining the previous Data B's stale ratings.

### TC-27 — New work matter does not reuse old Data A

**State:** Existing report case from TC-26.

**Input**

```text
Review this separate message about a new matter:
Data B: The customer database migration is complete.
```

**Expected**

- Starts a new case.
- Requests Data A for the database migration.
- Produces no review rating until new-case Data A is supplied.

**Forbidden**

- Reusing Alex, Friday, report requirements, prior answers, or prior ratings.

### TC-28 — Unclear case relationship requires classification

**State:** Existing case about a weekly report.

**Input**

```text
Review this: The revised file will be ready tomorrow.
```

**Expected**

- Asks whether the message is a revision in the existing case or a new work matter.
- Does not reuse Data A before classification.

**Forbidden**

- Assuming either same-case or new-case status.
- Rating against the existing case's Data A.

### TC-29 — Adopted draft with placeholder remains incomplete

**State:** Existing case in which the completion date is required but unknown. The assistant previously proposed `Alex will complete the task by [completion date].`

**Input**

```text
Use that version.
```

**Expected**

- Treats the adopted revision as new Data B.
- Reassesses the message.
- Lists `[completion date]` as unresolved.
- Keeps the affected dimension and overall status non-green.
- Does not treat the case as complete.

**Forbidden**

- Removing or filling the placeholder without user input.
- Ending as a successful completed review.

### TC-30 — Refusal preserves gray and stops questions

**State:** Existing case with responsibility clarity gray because the governing owner cannot be determined; the current tone rating is green.

**Input**

```text
I will not provide any more information. Stop here.
```

**Expected**

- Preserves the gray responsibility-clarity rating.
- Displays the green tone rating.
- Keeps overall status gray.
- Briefly identifies the unresolved owner information.
- Stops asking questions and ends the review.

**Forbidden**

- Inventing or selecting an owner.
- Continuing the Grill me loop after the explicit stop.

## T9.7 — Short acknowledgements

### TC-31 — Clear grouped instructions accept a short acknowledgement

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager instructed me to take photos from multiple angles now, not open the vacuum-packed boxes, pack tomorrow morning, and depart at 13:30.
Data B: okok
```

**Expected**

- Uses normal mode.
- Treats `okok` as acknowledging all directly preceding clear instructions.
- Rates responsibility clarity green.
- Rates tone green.
- Sets overall status to green.
- Asks no questions.
- States `No revision needed`.

**Forbidden**

- Requiring every instruction to be restated.
- Claiming that any task has already been completed.
- Adding `send the photos`, `we`, or any other unsupported action, owner, or commitment.
- Providing an expanded alternative message.

### TC-32 — Short acknowledgement does not answer a specific question

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager explicitly asked me to provide the task owner and deadline. Neither value is known.
Data B: okok
```

**Expected**

- Uses normal mode.
- Does not treat `okok` as supplying the owner or deadline.
- Rates responsibility clarity red because the reply fails to answer the explicit purpose.
- Rates tone green.
- Sets overall status to red.
- Asks neutral questions using placeholders for the owner and deadline.
- Uses placeholders rather than invented values in any partial revision.

**Forbidden**

- Rating responsibility clarity green based only on acknowledgement.
- Treating an acknowledgement as a specific informational answer.
- Inventing an owner or deadline.
- Claiming that either requested value has been externally verified.

## T13.1 — Quoted, forwarded, and nested content

### TC-33 — Markdown blockquote is excluded from the new body

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Alex is the confirmed report owner.
Data B:
Alex owns the report.

> Jamie owns the report and it is already late.
```

**Expected**

- Evaluates only `Alex owns the report.` as the new body.
- Identifies the blockquote as excluded content.
- Shows `Evaluated Data B: Alex owns the report.` and an `Excluded from evaluation` blockquote entry under background understanding.
- Rates responsibility clarity, tone, and overall status green.
- Leaves the blockquote unchanged if reproducing the complete message.

**Forbidden**

- Adding Jamie or lateness to Data A.
- Rating the blockquote as the user's responsibility wording or tone.
- Revising the blockquote.

### TC-34 — Email reply header and original message are excluded

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Friday is the confirmed report deadline.
Data B:
I will send the report on Friday.

On Monday, Pat wrote:
From: Pat
Sent: Monday
To: Me
Subject: Report
Send it on Thursday.
```

**Expected**

- Evaluates only `I will send the report on Friday.` as the new body.
- Identifies the reply introduction, header block, and original message as excluded content.
- Rates responsibility clarity, tone, and overall status green.

**Forbidden**

- Adding Thursday to Data A.
- Reporting a Friday/Thursday contradiction.
- Revising the original email.

### TC-35 — Forwarded content does not control tone or background

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked me only to acknowledge receipt of the information.
Data B:
Received.

-----Original Message-----
From: Customer
You people are useless.
```

**Expected**

- Evaluates only `Received.` as the new body.
- Identifies the original message as excluded content.
- Rates responsibility clarity, tone, and overall status green.
- Leaves the forwarded content unchanged if reproducing the complete message.

**Forbidden**

- Rating the user's tone red because of the customer's words.
- Treating the customer's words as manager requirements or Data A.
- Revising the forwarded content.

### TC-36 — Chat quote preview is excluded

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: I am the confirmed owner of the handoff.
Data B:
[Replying to Manager: "Jamie will handle the handoff."]
I will handle the handoff.
```

**Expected**

- Evaluates only `I will handle the handoff.` as the new body.
- Identifies the chat quote preview as excluded content.
- Rates responsibility clarity, tone, and overall status green.

**Forbidden**

- Treating Jamie as a confirmed or competing owner.
- Reporting a contradiction caused by the quote preview.
- Revising the quote preview.

### TC-37 — Ambiguous quote boundary stops assessment

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Alex is the confirmed owner.
Data B:
Alex owns it.
[Quoted message from Jamie
Taylor owns it.
I will send this part.
```

**Expected**

- Uses the intake format.
- Identifies the sendable-body boundary as missing.
- Requests the exact new body or explicit quote boundaries.
- Produces no ratings or revision.

**Forbidden**

- Guessing which lines are quoted.
- Combining all lines into the user's body and rating them.
- Adding Jamie or Taylor to Data A.

### TC-38 — Embedded content without a new body counts as missing Data B

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Alex is the confirmed report owner.
Data B:
> Alex owns the report.
```

**Expected**

- Uses the intake format.
- Identifies Data B as missing after excluding the blockquote.
- Requests the new body the user intends to send.
- Produces no ratings or revision.

**Forbidden**

- Rating the quoted sentence as the user's message.
- Treating the blockquote as Data A without separate user designation.
- Producing a revision from the blockquote.

### TC-39 — Limited-background mode excludes embedded content

**State:** Existing case after the user explicitly confirmed limited-background mode; no Data A is available.

**Input**

```text
Data B:
I will send the report on Friday.

> You people are useless.
```

**Expected**

- Uses limited-background mode.
- Starts background understanding with `Data A was not provided; this review assesses Data B only`.
- Shows `Evaluated Data B: I will send the report on Friday.` and an `Excluded from evaluation` blockquote entry.
- Marks manager-requirement alignment as not assessed.
- Rates responsibility clarity, tone, and overall status green based only on the new body.

**Forbidden**

- Rating the quoted insult as the user's tone.
- Adding the blockquote to Data A.
- Claiming the body matches the manager's original requirements.

### TC-40 — Inline quotation remains part of the new body

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Alex is the confirmed report owner and Friday is the confirmed deadline.
Data B: I told Sam, "Alex owns the report," and I will send it Friday.
```

**Expected**

- Evaluates the complete Data B, including the inline quotation, as the new body.
- Rates responsibility clarity, tone, and overall status green.
- Does not add an `Excluded from evaluation` entry.

**Forbidden**

- Removing or excluding `"Alex owns the report"` solely because it uses quotation marks or reported speech.
- Treating the inline quotation as separate Data A.
- Asking the user to identify a quote boundary.

### TC-41 — Revision changes only the new body

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Tuesday is the confirmed deadline.
Data B:
I will finish this on Thursday.

> Please keep this exact quoted line.
```

**Expected**

- Shows `Evaluated Data B: I will finish this on Thursday.` and an `Excluded from evaluation` blockquote entry.
- Rates responsibility clarity red, tone green, and overall status red.
- Minimally changes Thursday to Tuesday in the new body.
- Leaves `> Please keep this exact quoted line.` unchanged if reproducing the complete message.

**Forbidden**

- Revising, removing, or paraphrasing the blockquote.
- Treating the blockquote as Data A.
- Changing wording unrelated to the deadline contradiction.

### TC-42 — Nested content inside a forwarded block remains excluded

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Alex is the confirmed report owner.
Data B:
Alex owns the report.

-----Original Message-----
From: Pat
> Jamie owns the report.
```

**Expected**

- Evaluates only `Alex owns the report.` as the new body.
- Treats the complete original-message region, including its nested blockquote, as excluded content.
- Rates responsibility clarity, tone, and overall status green.

**Forbidden**

- Treating Jamie as a competing owner.
- Splitting the nested blockquote out as user-authored wording.
- Revising any part of the original-message region.

### TC-43 — Separately designated embedded content may be Data A

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Treat the clearly marked quoted original message inside Data B as Data A as well as embedded content.
Data B:
I will finish this on Thursday.

> Manager: Tuesday is the confirmed deadline.
```

**Expected**

- Evaluates only `I will finish this on Thursday.` as the new body.
- Uses the separately designated quoted statement as Data A.
- Rates responsibility clarity red, tone green, and overall status red because Thursday contradicts confirmed Tuesday.
- Minimally changes Thursday to Tuesday while leaving the blockquote unchanged if reproducing the complete message.

**Forbidden**

- Refusing to use the blockquote as Data A despite the explicit designation.
- Rating the manager's quoted tone as the user's tone.
- Revising the blockquote.

## T13.2 — Mixed input classification

### TC-44 — Explicit semantic boundaries allow auto-classification

**State:** New case.

**Input**

```text
Use workplace-survival to review this.
My manager wrote: Alex is the confirmed deployment owner.
I plan to send: Alex owns the deployment.
```

**Expected**

- Auto-classifies `Alex is the confirmed deployment owner.` as Data A.
- Auto-classifies `Alex owns the deployment.` as Data B.
- Shows `Adopted Data A: Alex is the confirmed deployment owner.` and `Evaluated Data B: Alex owns the deployment.` under background understanding.
- Excludes the semantic role labels from both payloads.
- Rates responsibility clarity, tone, and overall status green.

**Forbidden**

- Asking for A/B labels despite the unambiguous semantic boundaries.
- Treating both sentences as Data B.
- Including `My manager wrote:` or `I plan to send:` in the classified payloads.
- Omitting the provenance display.

### TC-45 — Unlabelled paragraphs require explicit classification

**State:** New case.

**Input**

```text
Use workplace-survival to review this.
The report belongs to Alex and Friday was mentioned.
Alex will send the report Friday.
```

**Expected**

- Uses the intake format.
- Identifies A-B classification as missing.
- Requests explicit Data A and exact Data B.
- Produces no ratings or revision.

**Forbidden**

- Assuming the first paragraph is Data A from its position or wording.
- Assuming the second paragraph is Data B from its position or wording.
- Using either paragraph to verify the other.

### TC-46 — Unclear multi-person roles stop classification

**State:** New case.

**Input**

```text
Use workplace-survival to review my manager message.
Pat: Morgan owns the release.
Lee: Taylor owns the release.
Morgan: I will send it tonight.
```

**Expected**

- Uses the intake format.
- Identifies A-B classification as missing.
- Requests identification of the manager, user, background, and exact message to send.
- Produces no ratings or revision.

**Forbidden**

- Inferring roles from speaker order, names, or sentence content.
- Selecting an owner or draft.
- Treating every line as Data A or every line as Data B.

### TC-47 — Multiple candidate drafts require selection

**State:** New case.

**Input**

```text
Use workplace-survival to review this.
Background: Alex is the confirmed owner and Friday is the confirmed deadline.
Possible wording 1: Alex will send it Friday.
Possible wording 2: I can probably get it out next week.
```

**Expected**

- Recognizes that the background boundary is clear but Data B is not uniquely selected.
- Uses the intake format.
- Requests which candidate is the actual Data B.
- Produces no ratings or revision.

**Forbidden**

- Choosing the first or second candidate.
- Combining both candidates.
- Rating either candidate before selection.

### TC-48 — Explicit Data B label prevents phrase-based reclassification

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Alex is the confirmed report owner and Friday is the confirmed deadline.
Data B: I wrote "my manager wrote about Alex" in my notes, and I will send the report Friday.
```

**Expected**

- Respects the explicit Data B label.
- Evaluates the complete Data B payload, including `my manager wrote about Alex`.
- Rates responsibility clarity, tone, and overall status green.
- Does not show `Adopted Data A` provenance for any phrase extracted from Data B.

**Forbidden**

- Reclassifying the quoted phrase as Data A.
- Splitting Data B at `my manager wrote`.
- Asking for A/B classification.

### TC-49 — Auto-classified draft still applies embedded-content boundaries

**State:** New case.

**Input**

```text
Use workplace-survival to review this.
My manager wrote: Friday is the confirmed report deadline.
I plan to send:
I will send the report Friday.

> My manager wrote: Send it Monday.
```

**Expected**

- Auto-classifies `Friday is the confirmed report deadline.` as Data A.
- Treats the complete region after `I plan to send:` as the outer Data B payload without recursively reclassifying its phrase.
- Evaluates only `I will send the report Friday.` as the new body.
- Shows one `Adopted Data A`, one `Evaluated Data B`, and one `Excluded from evaluation` entry.
- Rates responsibility clarity, tone, and overall status green.

**Forbidden**

- Adding Monday or the nested `My manager wrote:` blockquote to Data A.
- Showing a second `Evaluated Data B` entry containing the blockquote.
- Reporting a Friday/Monday contradiction.
- Revising the blockquote.

## T13.3 — Effective Data A replacement

### TC-50 — Withdrawn deadline no longer creates an omission

**State:** Existing case. Data A says the manager requires an owner and deadline; Alex is the confirmed owner, the deadline is unknown, and current Data B is `Alex owns the task.` The prior responsibility rating is red, tone is green, overall is red, and a deadline question and placeholder are unresolved.

**Input**

```text
Correction: the manager withdrew the deadline requirement. Only the owner is required now.
```

**Expected**

- Removes the deadline requirement from effective Data A.
- Rebuilds background understanding with only the current owner requirement and confirmed owner.
- Rates responsibility clarity, tone, and overall status green.
- Removes the deadline question and placeholder.
- States `No revision needed`.

**Forbidden**

- Retaining the old deadline requirement as an active conflict.
- Keeping a deadline question, placeholder, red rating, or gray rating.
- Treating the correction as replacement Data B.

### TC-51 — Corrected owner replaces the old owner

**State:** Existing case. Data A says Alex is the confirmed owner. Current Data B is `Jamie owns the task.`, producing responsibility red, tone green, overall red, and an Alex-based revision.

**Input**

```text
I need to correct the background: Alex is not the owner; Jamie is the confirmed owner.
```

**Expected**

- Replaces Alex with Jamie in effective Data A.
- Rebuilds background understanding with Jamie only.
- Reassesses current Data B as responsibility green, tone green, and overall green.
- Removes the stale Alex-based revision and states `No revision needed`.

**Forbidden**

- Keeping Alex and Jamie as conflicting active owners.
- Retaining the previous red rating or Alex-based revision.
- Treating the correction as replacement Data B.

### TC-52 — Cancelled requirement no longer produces stale output

**State:** Existing case. Data A says the manager requires owner and progress; progress is confirmed as 80%, owner is unknown, and current Data B is `Progress is 80%.` The prior review is red and asks for the owner.

**Input**

```text
The manager cancelled the owner request. The progress update is the only requirement now.
```

**Expected**

- Removes the owner request from effective Data A.
- Preserves the progress requirement and confirmed 80% value.
- Rates responsibility clarity, tone, and overall status green.
- Removes the owner question and any owner placeholder.
- States `No revision needed`.

**Forbidden**

- Treating the cancelled owner request as active.
- Retaining a non-green rating caused solely by the owner request.
- Removing the still-active progress requirement.

### TC-53 — Unmarked conflicting statement does not silently replace Data A

**State:** Existing case. Data A says Alex is the confirmed task owner. Current Data B is `Alex owns the task.` and no owner question is pending.

**Input**

```text
Background update: Jamie is the task owner.
```

**Expected**

- Treats Alex and Jamie as conflicting Data A statements rather than silently replacing Alex.
- Rates responsibility clarity gray and tone green, with overall gray.
- Asks neutrally which owner governs the current case.
- Keeps current Data B unchanged pending clarification.

**Forbidden**

- Assuming the new statement is a correction without explicit correction or governing wording.
- Selecting either owner using recency.
- Replacing Data B with the new statement.

### TC-54 — Targeted correction preserves unrelated Data A

**State:** Existing case. Data A says Alex is the confirmed owner and Friday is the confirmed deadline. Current Data B is `Jamie will finish it Monday.`, producing responsibility red and tone green.

**Input**

```text
Correction: Jamie, not Alex, is the confirmed owner.
```

**Expected**

- Replaces only the owner, making Jamie the effective owner.
- Preserves Friday as the effective deadline.
- Keeps responsibility red solely because current Data B says Monday instead of Friday; tone remains green and overall remains red.
- Revises Monday to Friday without changing Jamie.

**Forbidden**

- Removing or replacing the unrelated Friday deadline.
- Continuing to report an owner contradiction.
- Replacing current Data B with the correction statement.

### TC-55 — Unclear correction target requires clarification

**State:** Existing case. Data A says Alex owns the report and Taylor owns the deployment. Current Data B is `Jamie owns it.`, with responsibility gray and tone green because `it` is unclear.

**Input**

```text
Correction: Jamie is the owner.
```

**Expected**

- Does not replace either existing owner before the target is identified.
- Keeps responsibility clarity gray, tone green, and overall gray.
- Asks whether the correction concerns the report, deployment, or another work item.
- Preserves both existing owner facts pending clarification.

**Forbidden**

- Replacing Alex, Taylor, or both without clarification.
- Selecting a target from recency or Data B.
- Treating the correction statement as replacement Data B.

### TC-56 — Retracted fact no longer creates a contradiction

**State:** Existing case. Data A says vendor approval is a confirmed blocker. Current Data B is `Vendor approval is no longer a blocker.`, producing responsibility red and tone green.

**Input**

```text
Correction: retract the old blocker fact. Vendor approval is no longer a blocker.
```

**Expected**

- Removes the old `vendor approval is a blocker` fact from effective Data A.
- Uses the explicit current fact that vendor approval is no longer a blocker.
- Reassesses current Data B as responsibility green, tone green, and overall green.
- Removes the stale blocker contradiction and states `No revision needed`.

**Forbidden**

- Retaining both blocker states as an unresolved active conflict.
- Keeping the prior red rating or blocker-based revision.
- Treating the correction as replacement Data B.

### TC-57 — Withdrawn commitment no longer governs the case

**State:** Existing case. Data A says the user made a confirmed commitment to send the draft Friday. Current Data B is `I am no longer committing to a Friday draft.`, producing responsibility red and tone green.

**Input**

```text
Background correction: I withdraw my Friday draft commitment; that commitment no longer applies.
```

**Expected**

- Removes the Friday draft commitment from effective Data A.
- Reassesses current Data B as responsibility green, tone green, and overall green.
- Removes the stale commitment contradiction, question, or revision.
- States `No revision needed`.

**Forbidden**

- Keeping the withdrawn Friday commitment active.
- Retaining a non-green rating caused solely by the withdrawn commitment.
- Treating the withdrawal as replacement Data B.

## T13.4 — Tone boundaries

### TC-58 — Neutral direct request is Green

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My draft is complete. My manager's approval is required before I can send the report.
Data B: Please approve the report so I can send it today.
```

**Expected**

- Rates responsibility clarity green, tone green, and overall green.
- Treats the direct request as a clear handoff without a concrete tone risk.
- States `No revision needed`.

**Forbidden**

- Rating tone yellow merely because the message directly asks the manager to act.
- Rewriting the message to make it more formal or verbose.

### TC-59 — Dismissive responsibility shifting is Yellow

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My draft is complete. My manager's approval is required before I can send the report.
Data B: You need to approve it first. I've already done my part.
```

**Expected**

- Rates responsibility clarity green, tone yellow, and overall yellow.
- Identifies `I've already done my part` as dismissive responsibility-shifting wording.
- Describes the concrete risk without predicting the manager's reaction.
- Minimally revises the wording while preserving the approval handoff.

**Forbidden**

- Rating tone red without insult, hostility, threat, or unsupported accusation.
- Changing who must approve or who sends the report.

### TC-60 — Unsupported explicit accusation is Red

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The report is delayed. The cause is not confirmed. My manager asked for the current status.
Data B: The report is delayed. You caused this by ignoring my messages.
```

**Expected**

- Rates responsibility clarity red, tone red, and overall red.
- Identifies the definitive causal claim as conflicting with Data A's unconfirmed cause in the responsibility dimension.
- Identifies `You caused this by ignoring my messages` as an explicit accusation unsupported by Data A.
- Requires removal or neutralization of the accusation before sending.
- Does not claim that the accusation is false; states only that it is unsupported.

**Forbidden**

- Downgrading the explicit unsupported accusation to yellow.
- Using the tone rating as the reason for the responsibility rating instead of the separate Data A conflict.
- Predicting a definite manager reaction.

### TC-61 — Supported personalized blame is Yellow

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The report is delayed because the manager's required approval was not completed. My manager asked for the current status.
Data B: The report is delayed because you failed to approve it.
```

**Expected**

- Rates responsibility clarity green, tone yellow, and overall yellow.
- Recognizes that Data A supports the approval fact, so the wording is not an unsupported accusation.
- Identifies `you failed` as personalized blame that creates a concrete communication risk.
- Minimally changes the blame-focused wording to a neutral process statement.

**Forbidden**

- Rating tone red solely because the supported statement uses `you`.
- Removing or changing the confirmed cause of delay.

### TC-62 — Neutral process accountability is Green

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The report is delayed because the required approval was not completed. My manager asked for the current status.
Data B: The report is delayed because approval was not completed.
```

**Expected**

- Rates responsibility clarity green, tone green, and overall green.
- Treats the confirmed negative fact as neutral process accountability.
- States `No revision needed`.

**Forbidden**

- Rating tone yellow or red merely because the message identifies an operational failure.
- Adding personalized blame.

### TC-63 — Explicit insult is Red

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The report is delayed. My manager asked for the current status.
Data B: The report is delayed. Your work is useless.
```

**Expected**

- Rates responsibility clarity green, tone red, and overall red.
- Identifies `Your work is useless` as an explicit insult or degrading characterization.
- Requires removal of the insult.

**Forbidden**

- Rating the insult yellow as mere directness.
- Predicting how the manager will react.

### TC-64 — Targeted threat is Red

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The report is ready and requires my manager's approval before sending.
Data B: Approve this now or I'll make sure you're blamed for the delay.
```

**Expected**

- Rates responsibility clarity green, tone red, and overall red.
- Identifies `I'll make sure you're blamed` as a targeted threat or intimidation.
- Requires removal of the threat while preserving the approval request.

**Forbidden**

- Treating the threat as a neutral consequence.
- Changing the approval requirement.

### TC-65 — Neutral operational consequence is Green

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: Approval is required before the report can be sent. Without approval today, the report will be sent tomorrow.
Data B: If approval is not received today, the report will be sent tomorrow.
```

**Expected**

- Rates responsibility clarity green, tone green, and overall green.
- Treats the delayed send as a confirmed operational consequence, not a threat.
- States `No revision needed`.

**Forbidden**

- Rating tone red because the sentence uses an `if` condition.
- Rewriting a clear factual consequence.

### TC-66 — Explicit hostility is Red

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The report is ready. My manager asked for the current status.
Data B: The report is ready. I'm sick of dealing with you.
```

**Expected**

- Rates responsibility clarity green, tone red, and overall red.
- Identifies `I'm sick of dealing with you` as explicit hostility.
- Requires removal of the hostile sentence.

**Forbidden**

- Rating the hostility yellow as mere informality.
- Altering the accurate report status.

### TC-67 — Dismissive ambiguous stance is Yellow

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The report is ready. My manager asked for the current status.
Data B: The report is ready. Whatever.
```

**Expected**

- Rates responsibility clarity green, tone yellow, and overall yellow.
- Identifies `Whatever` as dismissive wording that leaves the sender's cooperative stance unclear.
- Minimally removes or neutralizes only the dismissive wording.

**Forbidden**

- Rating tone red without insult, threat, hostility, or unsupported accusation.
- Changing the report status.

### TC-68 — Qualified unsupported fault suggestion is Yellow

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The report is delayed. The cause is not confirmed. My manager asked for the current status.
Data B: The report is delayed. It seems you may have missed the approval.
```

**Expected**

- Rates responsibility clarity green, tone yellow, and overall yellow.
- Recognizes that `It seems` and `may have` present a qualified possibility rather than a major accusation asserted as fact.
- Identifies the personalized unsupported fault suggestion as a concrete non-major tone risk.
- Minimally changes it to a neutral statement that the cause is not confirmed.

**Forbidden**

- Rating tone red as though the qualified suggestion were a serious accusation asserted as fact.
- Presenting the possible missed approval as confirmed.
- Changing the accurate delayed status.

### TC-69 — Global degradation of a work product is Red

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The draft is incomplete. My manager asked for the current status.
Data B: The draft is incomplete. This draft is useless.
```

**Expected**

- Rates responsibility clarity green, tone red, and overall red.
- Identifies `This draft is useless` as a global degrading characterization rather than a specific operational defect.
- Requires removal or replacement of the degrading label.

**Forbidden**

- Rating the degradation yellow as ordinary task frustration.
- Altering the accurate incomplete status.

### TC-70 — Specific supported defect is Green

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The draft cannot be used yet because the required owner is missing. My manager asked for the current status.
Data B: The draft cannot be used yet because the required owner is missing.
```

**Expected**

- Rates responsibility clarity green, tone green, and overall green.
- Treats the supported, specific defect as a neutral operational fact.
- States `No revision needed`.

**Forbidden**

- Rating tone non-green merely because the draft cannot currently be used.
- Replacing the specific defect with vague or personalized blame.

### TC-71 — Task-directed dismissive frustration is Yellow

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: The draft is incomplete. My manager asked for the current status.
Data B: The draft is incomplete. I'm done dealing with this draft.
```

**Expected**

- Rates responsibility clarity green, tone yellow, and overall yellow.
- Treats `I'm done dealing with this draft` as task-directed dismissiveness rather than person-directed hostility.
- Minimally removes or neutralizes the dismissive sentence.

**Forbidden**

- Rating tone red without a degrading label, person-directed hostility, threat, or major unsupported accusation.
- Altering the accurate incomplete status.

## T13.5 — Responsibility Red and Gray boundaries

### TC-72 — Sole explicit requirement omitted is Red

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager explicitly requested only the confirmed task owner. No owner is known.
Data B: The project remains on schedule.
```

**Expected**

- Rates responsibility clarity red, tone green, and overall red.
- Identifies the unanswered sole owner request as defeating the reply's main purpose.
- Asks neutrally for the owner using a placeholder.

**Forbidden**

- Rating responsibility gray merely because the owner value is unknown.
- Inventing or suggesting an owner.

### TC-73 — Optional suggestion omitted is Green

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager requested the current status and said I may include the owner if useful, but the owner is not required. The confirmed status is on schedule.
Data B: The project remains on schedule.
```

**Expected**

- Rates responsibility clarity green, tone green, and overall green.
- Treats the omitted owner as a clearly optional suggestion.
- Asks no owner question and states `No revision needed`.

**Forbidden**

- Rating the optional omission yellow, red, or gray.
- Adding an owner placeholder.

### TC-74 — Ambiguous requirement applicability is Gray

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager requires the owner only if this is the final report. It is unknown whether the current report is final. The confirmed status is on schedule.
Data B: The project remains on schedule.
```

**Expected**

- Rates responsibility clarity gray, tone green, and overall gray.
- Identifies whether the current report is final as the governing missing information.
- Asks neutrally whether the final-report condition applies.

**Forbidden**

- Assuming that the owner requirement applies or does not apply.
- Rating the uncertain applicability as a known omission.

### TC-75 — Secondary requested detail omitted is Yellow

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager explicitly requested current progress as the main purpose and blocker status as a secondary detail. Progress is confirmed as 80%; blocker status is unknown.
Data B: Current progress is 80%.
```

**Expected**

- Rates responsibility clarity yellow, tone green, and overall yellow.
- Recognizes that Data B fulfills the stated main purpose but omits the secondary blocker detail.
- Asks neutrally for blocker status and uses a placeholder if revising.

**Forbidden**

- Rating the secondary omission red without evidence that it blocks execution.
- Rating it gray merely because blocker status is unknown.
- Inventing a blocker.

### TC-76 — Execution-gating omission is Red

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager requires the deployment owner before approval can proceed. No owner is known.
Data B: Please approve the deployment.
```

**Expected**

- Rates responsibility clarity red, tone green, and overall red.
- Identifies the missing owner as an explicit gate that prevents the requested approval.
- Asks neutrally for the owner and uses a placeholder in any partial revision.

**Forbidden**

- Rating the execution-gating omission yellow or gray.
- Inventing an owner.

### TC-77 — Conflicting governing deadline is Gray

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: One current-looking manager note says Tuesday is the deadline. Another says Thursday. The user cannot determine which note governs.
Data B: I will finish on Tuesday.
```

**Expected**

- Rates responsibility clarity gray, tone green, and overall gray.
- Identifies the governing deadline as materially conflicting Data A.
- Asks which deadline governs.

**Forbidden**

- Selecting Tuesday because Data B uses it.
- Selecting either deadline by order, probability, or convention.
- Rating the unresolved conflict red as though Tuesday were known wrong.

### TC-78 — Multiple explicit requirements answered is Green

**State:** New case.

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager requested the confirmed owner and deadline. Alex is the confirmed owner and Friday is the confirmed deadline.
Data B: Alex owns the task and will complete it Friday.
```

**Expected**

- Rates responsibility clarity green, tone green, and overall green.
- Recognizes that both explicit requirements are answered consistently.
- Asks no questions and states `No revision needed`.

**Forbidden**

- Requiring additional responsibility details not present in Data A.
- Asking for external verification of the confirmed values.

## Coverage

- T9.1 input and mode routing: TC-01–TC-05.
- T9.2 normal ratings: TC-06–TC-10.
- T9.3 Grill me interaction: TC-11–TC-15.
- T9.4 revision policy: TC-16–TC-20.
- T9.5 image input: TC-21–TC-25.
- T9.6 state and case isolation: TC-26–TC-30.
- T9.7 short acknowledgements: TC-31–TC-32.
- T13.1 quoted, forwarded, and nested content: TC-33–TC-43.
- T13.2 mixed input classification: TC-44–TC-49.
- T13.3 effective Data A replacement: TC-50–TC-57.
- T13.4 tone boundaries: TC-58–TC-71.
- T13.5 responsibility Red and Gray boundaries: TC-72–TC-78.
