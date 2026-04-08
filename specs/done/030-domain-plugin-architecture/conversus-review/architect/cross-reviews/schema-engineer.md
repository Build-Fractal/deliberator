# Cross-Review: architect reviewing schema-engineer

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The schema-engineer's analysis of frozen models is thorough and correct. I independently verified all 5 models have `frozen: True`. The type flow analysis (extract -> score -> persist -> query) is accurate. The identification of the non-numeric variable edge case (Concern A) is a genuine finding I missed -- `_compute_weighted_score()` indeed lacks the try/except that `_check_hard_blocks()` has.

The observation about unknown filter keys being silently ignored (Concern F) is well-taken. In a plugin system where multiple domains may have different filter conventions, silent ignoring is especially dangerous.

## Disagreements

### 1. Zero total weight edge case (Concern C) -- AGREE on gap, DISAGREE on severity

The schema-engineer rates this Medium. I would rate it **Low**. A scaffold with all-zero weights is a degenerate configuration that should be caught at scaffold validation time, not at scoring time. The scorer returning 0.0 for degenerate input is reasonable default behavior. The fix belongs in `load_scaffold()` (warn on zero total weight), not in `_compute_weighted_score()`.

### 2. Exact threshold boundary behavior (Concern D) -- AGREE but LOWER priority

The schema-engineer rates this Medium. I would rate it **Low**. The operators (`<`, `<=`, `>`, `>=`, `==`) give scaffold authors full control over boundary behavior. The issue is documentation, not code. A scaffold reference doc listing all operators and their semantics would resolve this.

### 3. Record ID validation (Concern B) -- AGREE, Low

This is correctly rated Low. Using `str` instead of `UUID` is a pragmatic choice that avoids serialization complexity. The trade-off is acceptable.

## Additions

The schema-engineer did not evaluate the `_extract_field_value()` function (store.py, lines 176-190). This function handles three field types: "overall", "equilibrium_score", and dimension names. But it does NOT handle the case where `field` is a key in `context_summary`. If a user calls `store.trend(domain, "workspace")`, they get an empty trend (all values None) with no error. This is related to the schema-engineer's Concern F (silent failure on bad input).

The schema-engineer also did not note that `DomainScore.variables` is typed as `dict[str, Any]` with `frozen: True`. Pydantic's `frozen` config prevents reassignment of the dict itself, but does NOT prevent mutation of the dict's contents (e.g., `score.variables["key"] = "new"`). This is a known Pydantic limitation -- truly immutable nested dicts would require `MappingProxyType` or a custom validator. In practice, the convention of treating frozen models as immutable is sufficient, but it is worth noting.
