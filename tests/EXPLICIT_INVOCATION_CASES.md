# Workplace Survival Explicit Invocation Cases

Each case explicitly invokes the skill by its `workplace-survival` slug while `disable-model-invocation: true` remains enabled.

## EI-01 — Normal mode

**Input**

```text
Use the workplace-survival skill.
Data A: My manager asked for the report owner and delivery date. Alex is the confirmed owner and Friday is the confirmed date.
Data B: Alex will deliver the report on Friday.
```

**Expected**

- Loads and follows the workplace-survival review workflow.
- Enters Normal mode.
- Rates responsibility clarity, tone, and overall status green.
- Uses the fixed review format.
- Asks no questions and states `No revision needed`.

## EI-02 — Limited-background mode

**Round 1**

```text
Use the workplace-survival skill to review this message.
Data B: Alex will deliver the report on Friday.
I cannot provide Data A.
```

**Expected Round 1**

- Does not rate immediately.
- Asks whether to continue in Limited-background mode.

**Round 2**

```text
Yes, continue in Limited-background mode.
```

**Expected Round 2**

- Enters Limited-background mode.
- States that Data A was not provided.
- Marks manager-requirement alignment as not assessed.
- Rates only Data B's internal responsibility clarity and tone.
- Does not claim compliance with the manager's requirements.

## EI-03 — Message-template mode

**Input**

```text
Use the workplace-survival skill to draft a message template.
Data A: My manager requested the task owner, current progress, and completion date.
I have not written Data B.
```

**Expected**

- Enters Message-template mode.
- Uses the fixed template format.
- Includes descriptive placeholders for all three requested values.
- Produces no review ratings.
- Does not treat the template as Data B.
