# Phase 4 Disputes: devex-advocate

**Spec**: 029-code-review-domain

---

## Surviving Disputes

### DISPUTE 1: format_compliant semantic ambiguity (Medium)

**Status**: Surviving -- all three agents agree.

The `format_compliant` variable is set by both LintExtractor and ConventionExtractor with different semantics. The last extractor wins. This creates confusion for scaffold authors.

**Recommended resolution**: Rename LintExtractor's `format_compliant` to `lint_clean` or remove it entirely (since `lint_violation_count == 0` captures the same concept).

### DISPUTE 2: Developer profile gap (Medium)

**Status**: Surviving -- devex-advocate and spec-compliance agree.

FR-012 requires developer profiles with per-author aggregation. DomainRecord has no author field, and store.aggregate() does not support grouping by author.

**Recommended resolution**: Add `author` to DomainRecord.context_summary in the create_record() method. Add "author" as a supported group_by value in store implementations.

## Withdrawn Disputes

- eslint complexity: Feature request, not compliance gap
- ruff SARIF: Info, not a dispute
