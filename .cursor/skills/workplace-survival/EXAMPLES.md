# Workplace Survival Examples

These examples are non-normative. They demonstrate `SKILL.md`, `REFERENCE.md`, and `FORMATS.md` without adding rules. Expected ratings show `Responsibility clarity / Tone / Overall status`.

## Input and mode routing

### Example 1 — Data B is missing

**Input**

- Data A: `The manager asked for the deployment owner and completion date.`
- Data B: Not provided.
- Request: `Please review my reply.`

**Expected mode:** No review mode; intake is required.

**Expected ratings:** None.

**Expected behavior:** Request Data B only. Do not rate, infer a reply, or provide a revision.

### Example 2 — Data A is missing

**Input**

- Data A: Not provided.
- Data B: `Alex will send the report tomorrow.`
- Request: `Check this before I send it to my manager.`

**Expected mode:** No review mode; intake is required.

**Expected ratings:** None.

**Expected behavior:** Request Data A and stop the assessment. Do not enter limited-background mode automatically.

### Example 3 — User refuses Data A

**Input**

- Data A: Not provided.
- Data B: `Alex will send the report tomorrow.`
- Follow-up: `I cannot provide the background.`

**Expected mode:** Awaiting limited-background confirmation.

**Expected ratings:** None.

**Expected behavior:** Ask whether the user wants to continue in limited-background mode. Do not rate until the user confirms.

### Example 4 — User confirms limited-background mode

**Input**

- Data A: Not provided.
- Data B: `Alex will send the report tomorrow.`
- Follow-up: `Yes, use limited-background mode.`

**Expected mode:** Limited-background mode.

**Expected ratings:** Green / Green / Green.

**Expected behavior:** Assess Data B only, mark manager-requirement alignment as not assessed, ask no questions, and state `No revision needed`. Do not claim that the message satisfies the manager's requirements.

### Example 5 — Explicit template request without Data B

**Input**

- Data A: `The manager wants an owner, current progress, and expected completion date.`
- Data B: Not provided.
- Request: `Give me a message template to fill in.`

**Expected mode:** Message-template mode.

**Expected ratings:** None.

**Expected behavior:** Provide a template using `[owner]`, `[current progress]`, and `[completion date]`, followed by the information-to-fill list. Do not include review ratings or claim compliance.

## Normal-mode ratings

### Example 6 — Data A and Data B fully align

**Input**

- Data A: `The manager asked who owns the report and when it will be delivered. The confirmed owner is Alex and the confirmed delivery date is Friday.`
- Data B: `Alex owns the report and will deliver it on Friday.`

**Expected mode:** Normal mode.

**Expected ratings:** Green / Green / Green.

**Expected behavior:** Cite the matching owner and date, ask no questions, and state `No revision needed`. Do not offer an optional rewrite.

### Example 7 — Data B supplies a requested name

**Input**

- Data A: `The manager asked for the name of the person responsible for the report.`
- Data B: `Alex is responsible for the report.`

**Expected mode:** Normal mode.

**Expected ratings:** Green / Green / Green.

**Expected behavior:** Treat the request as answered, describe Alex as the person stated in Data B, and do not demand external verification solely because the name first appears in Data B.

### Example 8 — Data B contradicts a known owner and date

**Input**

- Data A: `Jamie is the confirmed owner and the confirmed deadline is 15 August.`
- Data B: `Alex will complete it by 18 August.`

**Expected mode:** Normal mode.

**Expected ratings:** Red / Green / Red.

**Expected behavior:** Identify both direct contradictions and require correction. A safe minimal revision may use the confirmed owner and date from Data A.

### Example 9 — Non-critical ownership ambiguity

**Input**

- Data A: `Sam prepares the draft, then Lee performs the final check.`
- Data B: `We will review it and send it tomorrow.`

**Expected mode:** Normal mode.

**Expected ratings:** Yellow / Green / Yellow.

**Expected behavior:** Explain that `we` leaves the handoff or sender unclear, ask a neutral ownership question only if needed for a safe revision, and change only the ambiguous wording.

### Example 10 — Materially ambiguous Data A

**Input**

- Data A: `One note says Morgan owns the task. A later visible note says Taylor owns it, but the user has not identified which instruction governs.`
- Data B: `Morgan will complete the task.`

**Expected mode:** Normal mode.

**Expected ratings:** Gray / Green / Gray.

**Expected behavior:** Identify the conflicting Data A statements and ask which owner governs. Do not resolve the conflict using Data B or probability, and do not provide an unsafe revision.

## Questions and follow-up answers

### Example 11 — Data B omits required unknown values

**Input**

- Data A: `The manager explicitly requested the owner, deadline, current progress, and blocker. None of those values is available in Data A.`
- Data B: `Here is the project update.`

**Expected mode:** Normal mode.

**Expected ratings:** Red / Green / Red.

**Expected behavior:** Ask no more than three highest-impact neutral questions in this response. Suggested answer structures must use placeholders or balanced options and must not supply unknown facts. Defer the fourth uncertainty unless it remains material later.

### Example 12 — User answers become Data A

**Input**

- Existing case: Example 11.
- User answer: `Alex is the owner, the deadline is Friday, and progress is 80%.`

**Expected mode:** Normal-mode follow-up.

**Expected ratings:** Reassess responsibility clarity; display both current dimension ratings and the updated overall status.

**Expected behavior:** Add only the three explicit facts to Data A, do not add implications, do not repeat those questions, and ask about the blocker only if it remains material.

## Revision behavior

### Example 13 — Yellow issue receives a minimal same-language revision

**Input**

- Data A: `阿明負責整理資料；用家負責提交。`
- Data B: `我哋搞掂之後會交。`

**Expected mode:** Normal mode.

**Expected ratings:** Yellow / Green / Yellow.

**Expected behavior:** Revise only the unclear ownership, preserve Cantonese and the original register, and do not add a date or commitment. An acceptable minimal revision is `阿明搞掂啲資料之後，我會交。`; do not convert it to formal written Chinese such as `整理好資料之後，我會提交。`

### Example 14 — Red contradiction is corrected from Data A

**Input**

- Data A: `The confirmed deadline is Tuesday.`
- Data B: `I will finish this on Thursday.`

**Expected mode:** Normal mode.

**Expected ratings:** Red / Green / Red.

**Expected behavior:** Identify the deadline contradiction and minimally replace Thursday with Tuesday. Do not alter unrelated wording.

### Example 15 — Required value is unknown

**Input**

- Data A: `The manager requires an expected completion date, but no date has been confirmed.`
- Data B: `I am handling the task and will update you when it is complete.`

**Expected mode:** Normal mode.

**Expected ratings:** Red / Green / Red.

**Expected behavior:** Ask for the expected completion date. If showing a partial safe revision, use `[expected completion date]`; never invent a date. Do not treat a draft containing the placeholder as complete.

## Image input

### Example 16 — Clear image-based Data B

**Input**

- Data A: `The manager asked for the deployment owner. The confirmed owner is Priya.`
- Data B image: One clearly identifiable unsent draft reads `Priya owns the deployment.` The image also shows application controls, a battery notification, and older unrelated messages.

**Expected mode:** Normal mode.

**Expected ratings:** Green / Green / Green.

**Expected behavior:** Show only the recognized unsent draft verbatim under background understanding, ignore interface and unrelated text, ask no immaterial visual questions, and infer nothing outside the image.

### Example 17 — Multiple possible draft regions

**Input**

- Data A: Available.
- Data B image: Two different unsent text boxes are visible, and the request does not identify which one should be reviewed.

**Expected mode:** No review mode; image confirmation is required.

**Expected ratings:** None.

**Expected behavior:** Ask the user to identify the intended draft and stop. Do not choose one or rate either message.

### Example 18 — Unclear identity affects responsibility

**Input**

- Data A image: A conversation contains a clear instruction that `the sender` owns the handoff, but the sender's identity or role cannot be determined reliably from the visible content.
- Data B: `Jordan will handle the handoff.`

**Expected mode:** Normal mode with a partial assessment.

**Expected ratings:** Gray / Green / Gray.

**Expected behavior:** Ask for the material identity or role confirmation, keep responsibility clarity gray, and continue the unaffected tone assessment. Do not infer identity from avatar position or interface styling.

## Case state and isolation

### Example 19 — Revision in the same case

**Input**

- Existing Data A: `Alex owns the report; Friday is the confirmed deadline.`
- Previous Data B: `We will send it soon.`
- New Data B: `Alex will send the report on Friday.`

**Expected mode:** Normal-mode follow-up in the same case.

**Expected ratings:** Green / Green / Green.

**Expected behavior:** Reuse the existing case's Data A, replace the previous Data B, reassess both dimensions, and state `No revision needed`.

### Example 20 — Clearly different work matter

**Input**

- Existing case Data A concerns a Friday report owned by Alex.
- New Data B: `The customer database migration is complete.`

**Expected mode:** New case; intake is required because relevant Data A is missing.

**Expected ratings:** None.

**Expected behavior:** Do not reuse the report owner, deadline, ratings, or answers. Request Data A for the migration message.

### Example 21 — Case relationship is unclear

**Input**

- Existing case concerns a weekly report.
- New Data B: `The revised file will be ready tomorrow.`
- The message does not identify whether `the revised file` is the same report or a different matter.

**Expected mode:** Awaiting case classification.

**Expected ratings:** None until classification.

**Expected behavior:** Ask whether this is a revision in the existing case or a new work matter before reusing Data A.

### Example 22 — User adopts an incomplete revision

**Input**

- Assistant revision: `Alex will complete the task by [completion date].`
- User response: `Use that version.`
- The completion date remains unknown.

**Expected mode:** Normal-mode follow-up.

**Expected ratings:** The affected dimension remains gray or red as supported by the case; the overall status remains non-green.

**Expected behavior:** Treat the adopted revision as new Data B, reassess it, list the unresolved placeholder, and do not treat the case as complete.

### Example 23 — User refuses remaining required information

**Input**

- Current responsibility-clarity rating is gray because the governing owner cannot be determined.
- User response: `I will not provide anything else. Stop here.`

**Expected mode:** Review termination with unresolved information.

**Expected ratings:** Gray / current tone rating / Gray, unless another dimension is red.

**Expected behavior:** Preserve the gray assessment, briefly state the unresolved information, stop asking questions, and end without inventing an answer.

## Short acknowledgements

### Example 24 — Clear instructions receive a short acknowledgement

**Input**

- Data A: `The manager instructed the user to take photos from multiple angles now, not open the vacuum-packed boxes, pack tomorrow morning, and depart at 13:30.`
- Data B: `okok`

**Expected mode:** Normal mode.

**Expected ratings:** Green / Green / Green.

**Expected behavior:** Treat `okok` as acknowledging all directly preceding clear instructions. Do not require the instructions to be restated, claim that any task is complete, or expand the reply into a task list or new commitment.

### Example 25 — A short acknowledgement does not supply requested facts

**Input**

- Data A: `The manager explicitly requested the task owner and deadline. Neither value is known.`
- Data B: `okok`

**Expected mode:** Normal mode.

**Expected ratings:** Red / Green / Red.

**Expected behavior:** Do not treat `okok` as supplying the requested owner or deadline. Ask neutral questions using placeholders and do not invent either value.
