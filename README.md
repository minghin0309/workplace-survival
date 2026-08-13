# Workplace Survival

Workplace Survival reviews and minimally revises work messages intended for a manager. It checks responsibility clarity and tone against user-provided background, asks focused follow-up questions, and can generate fill-in message templates.

## Runtime files

The installable skill is:

```text
.cursor/skills/workplace-survival/
├── SKILL.md
├── REFERENCE.md
├── FORMATS.md
└── EXAMPLES.md
```

Copy the complete `workplace-survival/` directory. Keep all four files together because `SKILL.md` links directly to the other three.

## Install as a project skill

Use a project installation when the skill should be available only inside one project or shared through that project's repository.

Target path:

```text
<your-project>/.cursor/skills/workplace-survival/
```

### From a GitHub clone

Clone this repository, then copy the skill directory into the target project.

PowerShell:

```powershell
git clone <repository-url> workplace-survival-source
New-Item -ItemType Directory -Force "<your-project>\.cursor\skills" | Out-Null
Copy-Item -Recurse -Force `
  "workplace-survival-source\.cursor\skills\workplace-survival" `
  "<your-project>\.cursor\skills\"
```

macOS or Linux:

```bash
git clone <repository-url> workplace-survival-source
mkdir -p "<your-project>/.cursor/skills"
cp -R \
  "workplace-survival-source/.cursor/skills/workplace-survival" \
  "<your-project>/.cursor/skills/"
```

If this repository is already the target project, no copy is required; the skill is already in the correct project path.

## Install as a personal skill

Use a personal installation to make the skill available across projects for the current user.

Target path:

```text
~/.cursor/skills/workplace-survival/
```

On Windows, `~` corresponds to `%USERPROFILE%`.

PowerShell:

```powershell
git clone <repository-url> workplace-survival-source
New-Item -ItemType Directory -Force "$HOME\.cursor\skills" | Out-Null
Copy-Item -Recurse -Force `
  "workplace-survival-source\.cursor\skills\workplace-survival" `
  "$HOME\.cursor\skills\"
```

macOS or Linux:

```bash
git clone <repository-url> workplace-survival-source
mkdir -p "$HOME/.cursor/skills"
cp -R \
  "workplace-survival-source/.cursor/skills/workplace-survival" \
  "$HOME/.cursor/skills/"
```

## Download without Git

1. Open the repository on GitHub.
2. Select **Code → Download ZIP**.
3. Extract the archive.
4. Copy `.cursor/skills/workplace-survival/` to either the project or personal target path above.
5. Restart Cursor or open a new chat if the skill is not discovered immediately.

## Do not use the built-in skills directory

Do not install this skill in:

```text
~/.cursor/skills-cursor/
```

That directory is reserved for Cursor-managed built-in skills and may be overwritten.

## Verify the installation

Confirm that this file exists at the selected target:

```text
workplace-survival/SKILL.md
```

Then test explicit invocation:

```text
Use the workplace-survival skill to review this message to my manager.
```

The skill also supports automatic invocation for requests that clearly ask to check, revise, rewrite, or draft a work message intended for a manager.

## Development documents

- `SPEC.md`: product intent, scope, and non-negotiable behavior.
- `ARCHITECTURE.md`: rule ownership and change flow.
- `TASK.md`: active work only.
- `CHANGELOG.md`: completed outcomes.
- `tests/TEST_CASES.md`: acceptance assertions and current coverage.

Avoid copying rules between these files. Update the owner identified in `ARCHITECTURE.md`.

## Validation status

The T13.12 evidence-complete acceptance run reports:

- 136 behavioral cases passed, 0 failed;
- 13 attached-image cases passed;
- 1 automated package check passed;
- 14 high-risk cases repeated three times with 0 material variations.

See `tests/FINAL_ACCEPTANCE_RESULTS.md` and `tests/evidence/t13-12-final.json`.

Automatic-trigger and final-configuration explicit-invocation cases were evaluated deterministically against the current frontmatter. A live probabilistic Cursor dispatcher was not available, so production routing variance is not claimed.

Targeted mutation testing killed 9 of 9 selected non-equivalent mutants. This confirms that the frozen tests detect those deliberate defects; it does not replace blind holdout or real-world accuracy testing. See `tests/mutation/MUTATION_RESULTS.md`.

The cloud-isolated 30-case blind holdout failed every preregistered accuracy threshold and recorded one critical recipient-scope violation. Gold disagreement and exact-token scoring also contributed substantial uncertainty. See `tests/blind/CLOUD_BLIND_RESULTS.md`; do not interpret the public regression pass rate as unseen-case accuracy.

Post-blind remediation fixed three confirmed generalized defects and added TC-112–TC-114. Evidence-complete remediation acceptance reports 139 behavioral cases passed plus one separate package check. Fifteen disputed benchmark/gold cases were deliberately not converted into product rules. The original blind score remains unchanged; no fresh hidden holdout has yet measured post-remediation accuracy.

Blind benchmark methodology v2 now separates SUT-visible Data A from oracle notes and uses semantic concept matching instead of exact topic/fact token equality. The methodology is validated but has not yet been used for a fresh hidden holdout. See `tests/benchmark/`.
