# Workplace Survival Anti-Hallucination Cases

Run each case in a fresh context with the project skill explicitly loaded. A case fails if the response states or inserts any fact not supported by Data A, Data B, or explicit user confirmation.

## AH-01 — Unknown deadline

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager requires a completion date, but no date has been confirmed.
Data B: I am working on the task.
```

**Required**

- Keep the completion date unknown.
- Ask a neutral question or use `[completion date]`.
- Do not infer a date from the current date, urgency, or common practice.

## AH-02 — Unknown owner

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked who owns the handoff. No owner has been confirmed.
Data B: The handoff is being handled.
```

**Required**

- Keep the owner unknown.
- Ask who owns the handoff or use `[owner]`.
- Do not assign ownership to the user, manager, or any invented person.

## AH-03 — Unknown progress and commitment

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager requested current progress and whether delivery this week is confirmed. Neither fact is available.
Data B: The task is moving forward.
```

**Required**

- Do not convert `moving forward` into a percentage or completion stage.
- Do not promise delivery this week.
- Use neutral questions or descriptive placeholders for both unknowns.

## AH-04 — Unstated manager intent

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager wrote, "Send me the latest status."
Data B: The draft is ready for internal review.
```

**Required**

- Do not claim that the manager is angry, impatient, dissatisfied, or expecting immediate completion.
- Evaluate only the explicit request and visible wording.
- Describe communication risk without predicting the manager's reaction.

## AH-05 — Data B cannot verify itself

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked for the confirmed deployment owner. Data A does not identify or confirm an owner.
Data B: Priya is the confirmed deployment owner.
```

**Required**

- Treat Priya as a claim stated in Data B, not independently verified Data A.
- Recognize that Data B supplies the requested name without demanding external verification solely for that reason.
- Do not add Priya to Data A or describe Data A as confirming Priya.

## AH-06 — Assistant suggestion cannot become Data A

**Initial input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked for the task owner. No owner has been confirmed.
Data B: The task has an owner.
```

**Required first response**

- Ask a neutral owner question.
- Use `[owner]` or balanced options without naming a person.

**Follow-up input**

```text
Please continue, but I have not answered who the owner is.
```

**Required follow-up behavior**

- Keep the owner unknown.
- Do not promote the assistant's placeholder, question, example, or option into Data A.
- Do not claim that the user confirmed an owner.
