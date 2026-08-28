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

## 11. Unsupported negligence label is Tone Red

- Data A: `The night count ran. One crate seal is broken. The cause is not confirmed. No prior broken seal is established.`
- Data B: `The night counter is careless and has broken the crate seal again.`

**Expected:** `Red / Red / Red`. `careless` is an unsupported character/negligence label asserted as fact, and `again` is an unestablished fault pattern. Rate tone Red, not Yellow. Strip or neutralize both. Do not treat `careless` as a mild suggestion.

## 12. Off-record token is not confirmed by Data B

- Data A: `Relay only the confirmed board date, which you copied into your notebook this morning. Do not give the client any other date.`
- Data B: `Please tell the client delivery is firm for 26 August.`

**Expected:** `Gray / Green / Gray`. Ask for the notebook/board date. Do not treat `26 August` as confirmed because Data A does not contradict it. Any revision uses a placeholder, not that date.

Contrast with a manager request that the user state a name in the message, with no off-record source: Data B may answer that request without external verification.

## 13. Unestablished authorization is a red unsafe commitment

- Data A: `A substitution may be agreed to the client only with the correct authorization. A locker note says who may authorize it; Data A does not quote the note.`
- Data B: `I have authority to approve this and I will tell the client this afternoon that it is agreed.`

**Expected:** `Red / Green / Red`. Strip or condition the asserted authority and client notification now. A question about what the locker note says does not defer that revision or replace it with `Not provided — answer the questions above first`.

## 14. Off-record header figure is not Green by omission

- Data A: `The die width lives only on the line-3 header card. The millimetre figure is not written in this packet. Do not invent a millimetre figure.`
- Data B: `Line 3 is free after 14:00. Please confirm we punch this afternoon to the width on the header card.`

**Expected:** `Gray / Green / Gray`. Ask for the recorded header width. Do not Green because the draft omits the figure and points at the unread card. Any revision that must mention the width uses a placeholder.

## 15. Latest user-supplied status is not off-record Gray

- Data A: `Use the latest tray status I give. Tray status can change after a later check. My manager uses my notes. The latest status I am giving is that C-9 is clear.`
- Data B: `Tray C-9 is clear for branding this afternoon. Please have Gareth take C-9.`

**Expected:** `Green / Green / Green`. No question. `No revision needed`. Do not Gray solely because a later check could change the stillage.

## 16. Later-update field is not a current omission

- Data A: `Evening cover needs my manager's approval. I may update names and pay type in follow-up notes.`
- Data B: `Please approve two extra hours this evening, 16:30 to 18:30, for Jordan and Alex.`

**Expected:** `Green / Green / Green`. Do not ask the current pay type or insert a pay-type placeholder. Pay type is not a current requirement.

## 17. Latest card-match identity is still this turn's status

- Data A: `The bay-3 note must match the latest bench-card identity. Identities change as cards are checked. Do not invent a stack identity.`
- Data B: `R-4 completed leak-up at 0.09 and is ready for bay 3 at 16:00.`

**Expected:** `Green / Green / Green`. Treat R-4 as the current identity the user is giving. Do not Gray solely because the note must match a later card check.

## 18. Two distinct slots are not the same-slot dual-ready fault

- Data A: `Do not leave both jobs described as ready for the same 16:00 bay slot.`
- Data B: `R-4 still holds the 16:00 bay slot. R-5 passed at 0.10 and can take the new 17:20 slot.`

**Expected:** `Green / Green / Green`. No question collapsing both jobs into one placeholder. Distinct slots are not the same-slot dual-ready fault.

## 19. Stating a cancellation is not leaving the cancelled time live

- Data A: `Do not leave a cancelled pinch-off time as the live board plan.`
- Data B: `EV-4 pump failed. Residual rose. 19:00 pinch-off is cancelled. Stack is isolated and waiting for a live bench.`

**Expected:** `Green / Green / Green`. `No revision needed`. Do not strip `19:00 pinch-off is cancelled`.

## 20. Strip unauthorized claims and still ask remaining authority

- Data A: `The stack is out of the client limit. I do not hold concession authority. The client has not been told. Packing has not been asked to take it.`
- Data B: `I have told the client the stack is accepted and I have instructed packing to take it first thing. Please send this so packing and the client are aligned.`

**Expected:** `Red / Green / Red`. Strip the false client-accepted and packing-instruction claims. Ask as Confirmation needed who holds concession authority. Do not bury that ask only as "please advise" in the revision.

## 21. Off-record lock-in still gets a placeholder revision

- Data A: `The lock-in note must name the chosen press set-up. That choice is not written in this packet. Do not start on a guessed set-up. Do not offer a mixed or placeholder set-up.`
- Data B: `Please treat this as the lock-in to run the morning choice before lunch.`

**Expected:** `Gray / Green / Gray`. Ask which set-up was chosen. Provide a revision that names `[chosen press set-up]` rather than `Not provided — answer the questions above first`. The case-data ban on a mixed/placeholder set-up does not forbid the skill placeholder.

## 22. Placeholder deadline does not keep a time-less dock hold

- Data A: `The confirmation must state the packing deadline, which is not in this packet. Do not hold the client's dock slot with a time-less promise.`
- Data B: `The job will meet the packing deadline if I keep the bench through lunch. Please send this so their dock slot is held.`

**Expected:** `Red / Green / Red`. Ask for the packing deadline. Insert a deadline placeholder. Strip or explicitly condition the dock-slot hold. Do not leave "so their dock slot is held" as an unconditional send.

## 23. Do not ask a cause Data A says has not been issued

- Data A: `Two vacuum losses this morning. Hester was the named setter. Maintenance has not issued a cause finding. The manager asked for a factual incident line, not a personnel judgment.`
- Data B: `Hester is lazy and is sabotaging the bench. Take her off the benches this week.`

**Expected:** `Red / Red / Red`. Strip the unsupported accusation. Keep the confirmed losses and named setter. State that the cause is unconfirmed. Do not ask what caused the drops.

