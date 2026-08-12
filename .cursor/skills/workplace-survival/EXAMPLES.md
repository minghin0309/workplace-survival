# Workplace Survival Examples

These examples are non-normative. They illustrate edge cases without adding rules. `SKILL.md`, `REFERENCE.md`, and `FORMATS.md` govern behavior.

Ratings are shown as `Responsibility clarity / Tone / Overall`.

## 1. Missing background

- Data B: `Alex will send the report tomorrow.`
- Data A: Not provided.

**Expected:** Use intake output and request Data A. Do not enter limited-background mode or rate the message automatically.

If the user says Data A cannot be provided, ask whether to use limited-background mode. After explicit confirmation, assess Data B itself, mark manager-requirement alignment as not assessed, and do not infer missing requirements.

## 2. Direct contradiction

- Data A: `Jamie is the confirmed owner; the deadline is 15 August.`
- Data B: `Alex will complete it by 18 August.`

**Expected:** `Red / Green / Red`. Identify both contradictions and minimally replace only the incorrect owner and date with confirmed values.

## 3. Non-critical ownership ambiguity

- Data A: `Sam prepares the draft; Lee performs the final check.`
- Data B: `We will review it and send it tomorrow.`

**Expected:** `Yellow / Green / Yellow`. Explain that `we` leaves ownership or handoff unclear. Preserve `tomorrow` and change only the ambiguous responsibility wording.

## 4. Required value is unknown

- Data A: `The manager requires an expected completion date, but none is confirmed.`
- Data B: `I am handling the task and will update you when it is complete.`

**Expected:** `Red / Green / Red`. Ask neutrally for the date. A partial revision may use `[expected completion date]`; never invent a value or treat the placeholder as complete.

## 5. Preserve language and register

- Data A: `阿明負責整理資料；用家負責提交。`
- Data B: `我哋搞掂之後會交。`

**Expected:** `Yellow / Green / Yellow`. Clarify only the ownership. `阿明搞掂啲資料之後，我會交。` is an acceptable minimal revision. Do not convert the message into formal written Chinese.

## 6. Material image ambiguity

- An image contains two unsent draft boxes.
- Neither the request nor visible structure identifies the target.

**Expected:** Use intake output and ask which draft to review. Do not select, combine, or rate either draft.

If one draft is clearly identifiable, show its recognized text verbatim and ignore unrelated interface text.

## 7. Case isolation

- Existing case: Alex owns a Friday report.
- New message: `The customer database migration is complete.`

**Expected:** Treat the migration as a new matter and request its Data A. Do not reuse Alex, Friday, prior answers, or prior ratings.

If the relationship between a new message and the current case is unclear, ask before reusing Data A.

## 8. Short acknowledgement

- Data A: `Take photos now, do not open the boxes, pack tomorrow morning, and depart at 13:30.`
- Data B: `okok`

**Expected:** `Green / Green / Green` when this is one identifiable reply target containing clear, non-conflicting instructions that require acknowledgement. Do not expand the acknowledgement or claim completion.

Contrast:

- Data A: `Provide the task owner and deadline; neither is known.`
- Data B: `okok`

**Expected:** `Red / Green / Red`. The acknowledgement does not supply either requested fact; ask neutral questions using placeholders.

## 9. Template without background

- Request: `Give me a message template for a manager update.`
- Data A: Not provided.
- Data B: Not provided.

**Expected:** Enter message-template mode, provide a generic neutral structure with descriptive placeholders, and produce no ratings or claim of requirement alignment.

## 10. Explicit hostile tone

- Data A: `The report is confirmed delayed; the manager asked for its status.`
- Data B: `The report is delayed. This is your fault and your work is useless.`

**Expected:** `Green / Red / Red`. Treat the status statement separately from the unsupported accusation and insult. The tone requires revision; do not soften the responsibility rating merely because tone is red.
