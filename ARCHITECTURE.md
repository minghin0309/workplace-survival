# Workplace Survival — Document Architecture

## Authority

```text
SPEC.md
  ├─ SKILL.md       routing, workflow, top-level safeguards
  ├─ REFERENCE.md   detailed semantics and rating boundaries
  └─ FORMATS.md     exact output structures and fixed text

EXAMPLES.md         non-normative runtime examples
TEST_CASES.md       exhaustive acceptance assertions
TASK.md             active work only
CHANGELOG.md        completed outcomes
```

`SPEC.md` owns product intent, scope, and non-negotiable behavior. Runtime files implement that contract using the ownership split above. Examples, tasks, changelog entries, and test results never create product behavior.

## Runtime directory

```text
.cursor/skills/workplace-survival/
├── SKILL.md
├── REFERENCE.md
├── FORMATS.md
└── EXAMPLES.md
```

Keep all four files together when installing the skill.

## Change rules

1. Start behavior changes in `SPEC.md`.
2. Change only the runtime owner of the affected detail.
3. Put exact output syntax only in `FORMATS.md`.
4. Put exhaustive scenarios only in `tests/TEST_CASES.md`; keep `EXAMPLES.md` representative.
5. Record active implementation work in `TASK.md`, then move its completed outcome to `CHANGELOG.md`.
6. If two normative files conflict, stop and resolve the ownership error before testing.

`SKILL.md` may link directly to the three runtime support files. Support files must not require deeper runtime dependencies.
