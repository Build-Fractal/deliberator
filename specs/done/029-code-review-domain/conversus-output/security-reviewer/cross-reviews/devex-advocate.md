# Cross-Review: security-reviewer reviewing devex-advocate

**Spec**: 029-code-review-domain

---

## Agreement

The devex-advocate's review is practical and well-grounded. I agree with:

- CoverageExtractor auto-detection is robust
- LintExtractor handles the dominant formats
- SpecComplianceExtractor is a clever approach to requirement tracing
- Scaffold tuning is appropriate for each audience

## Disagreements

### Concern #2 (format_compliant override) -- should be Medium, not Low

The devex-advocate notes that `format_compliant` is set by both LintExtractor and ConventionExtractor. From a security perspective, this is a **Medium** concern because:

- The ConventionExtractor's `format_compliant` comes from `black --check` output (formatting only)
- The LintExtractor's `format_compliant` comes from `count == 0` (no lint violations)
- These are semantically different: formatting compliance vs. lint violation count

If both extractors run, ConventionExtractor runs last (it appears after LintExtractor in get_extractors()) and overwrites the LintExtractor's value. This means the `format_compliant` variable in the final variables dict reflects black compliance, not lint compliance. But the variable name doesn't clarify this.

**Recommendation**: Rename one of the variables to disambiguate:
- LintExtractor: `lint_clean` (zero violations)
- ConventionExtractor: `format_compliant` (formatter check passes)

### Agreement: eslint complexity gap is Low

I agree with the devex-advocate that lacking eslint complexity support is Low severity. The extractor architecture is pluggable, so a future `ESLintComplexityExtractor` can be added without modifying existing code.

## Additions

The devex-advocate did not assess the security implications of `_safe_read_xml()`. The function uses `ET.parse(path)` which is vulnerable to XML entity expansion attacks (XXE) if the XML file is attacker-controlled. The comment `# noqa: S314 -- trusted local file` acknowledges this. Since the extractors only read local files (constraint: "MUST NOT execute code"), this is acceptable. However, if the tool ever reads XML from network sources, this should be revisited with `defusedxml`.
