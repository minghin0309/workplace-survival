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

## Coverage

- T9.1 input and mode routing: TC-01–TC-05.
- T9.2 normal ratings: TC-06–TC-10.
- T9.3 Grill me interaction: TC-11–TC-15.
- T9.4 revision policy: TC-16–TC-20.
- T9.5 image input: TC-21–TC-25.
- T9.6 state and case isolation: TC-26–TC-30.
- T9.7 short acknowledgements: TC-31–TC-32.
