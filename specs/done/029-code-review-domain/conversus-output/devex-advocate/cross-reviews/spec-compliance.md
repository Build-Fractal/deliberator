# Cross-Review: devex-advocate reviewing spec-compliance

**Spec**: 029-code-review-domain

---

## Agreement

The compliance matrix is thorough. I agree with:

- All PASS verdicts for FR-001 through FR-009
- The PARTIAL verdicts for FR-012 (missing author aggregation) and FR-013 (no configurable threshold)
- The NOT IMPLEMENTED verdicts for FR-014 through FR-016 (gate integration)
- SC-001 and SC-002 PASS

## Disagreements

### FR-012 severity -- Medium, not just PARTIAL

The spec-compliance agent marks FR-012 as PARTIAL. I think the absence of developer profiles is a **Medium** gap from a devex perspective. Developer profiles are the most user-facing feature in the persistence layer -- they answer "how am I doing over time?" which is a key motivator for code quality improvement. The current store.aggregate() supports grouping by verdict/convergence/scaffold_name but not by author.

The fix is straightforward: add `author` as a field in DomainRecord's `context_summary` and add "author" as a supported `group_by` value in the store implementations.

### FR-019 (Supabase backend) -- should be DEFERRED, not PARTIAL

The spec says "API MUST support both JSONL and Supabase backends via configuration." The implementation has JSONL and SQLite backends. I would classify this as DEFERRED rather than PARTIAL because:
1. The store protocol is defined and both backends conform to it
2. A Supabase backend can be added without changing any existing code
3. The configuration pattern (choosing backend via config) is established

It's not a partial implementation -- it's a not-yet-implemented backend. The architecture supports it cleanly.

## Additions

The spec-compliance agent did not assess the quality of error messages from extractors. From a devex perspective, the logger.warning messages are informative:
- `"CoverageExtractor: no coverage_report path in context"` -- tells the user exactly what's missing
- `"Could not read JSON from %s: %s"` -- includes path and error

This is good practice. Users who see None values in their scores can check logs to understand which tool output is missing.
