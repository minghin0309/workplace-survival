# Workplace Survival Auto-Trigger Cases

Submit each prompt without naming or explicitly invoking `workplace-survival`.

## Should trigger

### AT-01 — Review a message to a manager

```text
Please check this work message before I send it to my manager.
Background: My manager asked for the report owner. Alex is the confirmed owner.
Message: Alex owns the report.
```

Expected: Trigger the skill and use its review intake or review workflow.

### AT-02 — Rewrite a risky reply to a manager

```text
Can you minimally rewrite my reply to my manager and check the responsibility and tone?
Background: Jamie is the confirmed deployment owner.
Message: Alex owns it, and this is not my problem.
```

Expected: Trigger the skill and evaluate responsibility clarity and tone separately.

### AT-03 — Draft a manager-message template

```text
Draft a work update template for my manager. It needs placeholders for the owner, progress, and completion date.
```

Expected: Trigger the skill and enter Message-template mode without ratings.

### AT-04 — Traditional Chinese manager-message review

```text
幫我檢查準備發俾上司嘅工作訊息，睇吓責任同語氣有冇問題。
背景：阿明係已確認嘅負責人。
訊息：阿明會負責呢項工作。
```

Expected: Trigger the skill, preserve the user's language, and use the review workflow.

## Should not trigger

### AT-05 — General writing request

```text
Rewrite this paragraph to make it more vivid for a short story.
```

Expected: Do not trigger the skill.

### AT-06 — Casual conversation

```text
What are some good lunch ideas for tomorrow?
```

Expected: Do not trigger the skill.

### AT-07 — Message to a colleague

```text
Make this casual message to my friend sound warmer: See you at seven.
```

Expected: Do not trigger the skill.

### AT-08 — Technical review

```text
Review this Python function for bugs and performance problems.
```

Expected: Do not trigger the skill.

### AT-09 — Work message not intended for a manager

```text
Polish this work announcement for all conference attendees.
```

Expected: Do not trigger the skill.

## Explicit invocation regression

### AT-10 — Explicit slug remains available

```text
Use the workplace-survival skill.
Data A: My manager asked for the owner. Alex is the confirmed owner.
Data B: Alex owns the task.
```

Expected: Explicit invocation still loads the skill and produces a green Normal-mode review.
