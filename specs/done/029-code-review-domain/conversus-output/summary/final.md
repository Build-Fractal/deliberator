# Conversus Final Synthesis: 029-code-review-domain

**Agents**: devex-advocate, security-reviewer, spec-compliance
**Phases completed**: P1 (review) -> P2 (cross-review) -> P3 (revision) -> P4 (dispute) -> P5 (synthesis)

---

## Verdict: PASS with caveats

The core domain plugin (extract -> score -> persist -> API) is fully functional, well-tested, and production-quality. Extractors handle real tool output correctly and degrade gracefully. Scaffolds are well-tuned for target audiences. The scoring model is intuitive with correct inversion logic for security variables and impact-ordered recommendations.

Gate integration (FR-014 through FR-016) is the primary unimplemented feature. Developer profiles (FR-012) and configurable debt alerting (FR-013) are secondary gaps.

---

## Consensus Points

1. **Extractors are practical and robust**: All 8 extractors handle real tool output formats (Cobertura XML, lcov, ruff JSON, eslint JSON, radon JSON, bandit JSON, gitleaks JSON). Missing output yields None with warnings. No code execution.
2. **secrets_exposed inversion is correct**: True -> 0.0 (bad), False -> 1.0 (good). The _INVERTED_BOOLEANS set is extensible.
3. **Hard block evaluation is sound**: Supports truthy checks, comparison operators (==, !=, >=, <=, >, <), and type coercion. No injection risk (no eval).
4. **Scaffolds are well-differentiated**: startup-mvp (fast, low ceremony) vs healthcare (strict, audit-trail) with sensible weight distributions.
5. **Append-only persistence is correctly enforced**: No delete/update methods in stores. File locking via fcntl.
6. **API is optional**: Domain works as a library without the FastAPI server.
7. **"MUST NOT execute code" constraint is upheld**: All extractors read files only.

---

## DISPUTES_BEGIN

### DISPUTE 1: format_compliant variable collision
- **Severity**: Medium
- **Agents**: All three (consensus)
- **Description**: Both LintExtractor and ConventionExtractor set the `format_compliant` variable with different semantics. LintExtractor sets it based on zero lint violations; ConventionExtractor sets it based on black --check output. The last extractor wins via dict.update(), making the final value depend on ordering.
- **Recommendation**: Rename LintExtractor's `format_compliant` to `lint_clean` or remove it. Keep ConventionExtractor's `format_compliant` as the canonical formatter compliance variable.
- **Disposition**: SURVIVING

### DISPUTE 2: FR-012 developer profiles missing
- **Severity**: Medium
- **Agents**: devex-advocate, spec-compliance
- **Description**: FR-012 requires developer profiles with per-author score aggregation. DomainRecord has no author field. The store's aggregate() method does not support grouping by author.
- **Recommendation**: Add `author` to DomainRecord.context_summary during create_record(). Add "author" as a supported group_by value in JSONLStore and SQLiteStore.
- **Disposition**: SURVIVING

### DISPUTE 3: FR-013 technical debt alerting not implemented
- **Severity**: Medium
- **Agents**: security-reviewer, spec-compliance
- **Description**: The spec requires configured per-dimension thresholds for technical debt alerts. The current implementation only has a hardcoded declining-trend detection (slope < -0.01). No per-dimension threshold configuration exists.
- **Recommendation**: Add `alert_thresholds` field to Scaffold. Modify trend computation to compare slope against configurable thresholds per dimension.
- **Disposition**: SURVIVING

### DISPUTE 4: FR-014 through FR-016 gate integration not implemented
- **Severity**: High
- **Agents**: All three (consensus)
- **Description**: The conversus gate integration (multi-agent deliberation on review scores) is the differentiating feature. DomainPlugin.gate() returns None by default and CodeReviewDomain does not override it. Gate agents, equilibrium scoring, and POST_DELIBERATION hooks are not implemented.
- **Recommendation**: Implement gate() override in CodeReviewDomain that invokes the conversus engine's gate mechanism with extracted variables and scaffold as context. Depends on gate infrastructure from spec 011.
- **Disposition**: SURVIVING

### DISPUTE 5: FR-019 Supabase backend deferred
- **Severity**: Low
- **Agents**: All three (consensus)
- **Description**: The spec requires Supabase backend support via configuration. JSONL and SQLite backends are implemented. The store protocol cleanly supports adding new backends. Supabase implementation is pending.
- **Recommendation**: Implement SupabaseStore as a third backend. No architectural changes needed.
- **Disposition**: SURVIVING

## DISPUTES_END

---

## Action Items

| Priority | Action | Owner |
|----------|--------|-------|
| High | Implement gate() in CodeReviewDomain (FR-014-016) | depends on spec 011 |
| Medium | Rename LintExtractor format_compliant to lint_clean | devex-advocate |
| Medium | Add author field to DomainRecord and store aggregation (FR-012) | devex-advocate |
| Medium | Add configurable alert_thresholds to Scaffold (FR-013) | security-reviewer |
| Low | Implement SupabaseStore backend (FR-019) | architect |

---

## Compliance Summary

| Category | Total | Pass | Partial | Not Implemented | Deferred |
|----------|-------|------|---------|-----------------|----------|
| Functional Requirements | 19 | 12 | 1 (FR-012) | 4 (FR-013, FR-014-016) | 1 (FR-019) |
| Success Criteria | 5 | 2 | 0 | 1 (SC-004) | 2 (SC-003, SC-005) |
