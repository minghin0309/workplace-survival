# Workplace Survival Explicit Invocation Results

## Summary

- Slug used: `workplace-survival`.
- Test-stage configuration: `disable-model-invocation: true` was present during T11.2.
- Core modes tested: 3.
- Cases passed: 3.
- Cases failed: 0.

## Results

- EI-01: PASS — Explicit invocation entered Normal mode, used the fixed review format, returned green/green/green, asked no questions, and required no revision.
- EI-02: PASS — Explicit invocation requested confirmation before entering Limited-background mode, then assessed Data B only and left manager-requirement alignment unassessed.
- EI-03: PASS — Explicit invocation entered Message-template mode, used descriptive placeholders, emitted no ratings, and did not treat the generated template as Data B.

## T11.2 conclusion

Explicit invocation by the `workplace-survival` slug works with model invocation disabled. Normal mode, Limited-background mode, and Message-template mode all pass their expected behavior checks.

## Final-configuration regression

The final published frontmatter omits `disable-model-invocation` to enable automatic invocation, so the original EI configuration is historical and is not expected to remain present. After the post-T11.5 changes, AT-10 passed again and confirmed that explicit `workplace-survival` invocation still loads the skill under the final automatic-invocation configuration.
