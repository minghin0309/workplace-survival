# Workplace Survival Interaction Quality Cases

Run each case with the project skill explicitly loaded. Evaluate the response against every requirement.

## IQ-01 — Irrelevant uncertainty does not trigger a question

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked who owns the report. Alex is the confirmed owner. The lunch location for Friday has not been decided.
Data B: Alex owns the report.
```

**Required**

- Rate both dimensions and overall status green.
- Ask no question about the lunch location.
- State `No revision needed`.

## IQ-02 — Green message is not forcibly rewritten

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked for the deployment date. Tuesday is the confirmed deployment date.
Data B: The deployment is scheduled for Tuesday.
```

**Required**

- Ask no follow-up question.
- Provide no optional, stylistic, or more formal rewrite.
- Use `No revision needed`.

## IQ-03 — Suggested answers remain neutral

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked whether the deadline is confirmed. Data A does not establish the answer.
Data B: We are targeting Friday.
```

**Required**

- Ask whether Friday is confirmed only if the answer can change the rating or safe revision.
- Offer balanced options such as `confirmed / not confirmed / not yet confirmed`, or an equally neutral structure.
- Do not label an option as better, safer, more professional, or more likely to earn green.

## IQ-04 — Answered question is not repeated

**Initial input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked for the task owner. No owner has been confirmed.
Data B: The task is assigned.
```

**Follow-up input**

```text
Alex is the task owner.
```

**Final input**

```text
Data B: Alex owns the task.
```

**Required**

- Add the explicit answer to Data A.
- Do not ask for the owner again after the answer.
- Reassess the final Data B and return green without stale questions.

## IQ-05 — Risk description does not predict manager reaction

**Input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked for the confirmed owner. Jamie is the confirmed owner.
Data B: Alex owns it, and this is not my problem.
```

**Required**

- Identify the owner contradiction and responsibility-shifting wording.
- Describe concrete execution or communication risks.
- Do not claim that the manager will be angry, blame the user, criticize the user, or react in any definite way.

## IQ-06 — No repeated question under paraphrase

**Initial input**

```text
Use workplace-survival to review my reply.
Data A: My manager asked for the completion date. No date has been confirmed.
Data B: I will finish the task.
```

**Follow-up input**

```text
The confirmed completion date is 20 August.
```

**Final input**

```text
Please reassess the same draft.
```

**Required**

- Add 20 August to Data A.
- Do not ask `When will it be completed?`, `What is the deadline?`, or any paraphrase of the resolved date question.
- Use the confirmed date in a safe minimal revision if Data B still omits it.
