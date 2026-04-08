# Phase 1 Review: devex-advocate

**Spec**: 029-code-review-domain
**Agent**: devex-advocate
**Focus**: Extractor practicality, real tool output parsing, scaffold tuning

---

## Overall Assessment

The extractors are practical and well-designed. They read pre-existing tool output (never execute tools), handle missing reports gracefully (returning None), and parse the most common output formats for each tool class. The scaffolds provide good differentiation between use cases (startup-mvp vs healthcare). The scoring model is intuitive and the recommendation engine is useful.

**Verdict**: PASS with observations.

---

## Detailed Findings

### 1. CoverageExtractor -- PRACTICAL

Supports both Cobertura XML and lcov.info formats, which covers pytest-cov and istanbul (the two dominant Python/JS coverage tools). Auto-detection by file extension with fallback to content sniffing is robust. The XML parsing uses `xml.etree.ElementTree` which is stdlib -- no extra deps.

Test fixtures include both formats and edge cases (missing report, nonexistent file). Coverage is thorough.

### 2. LintExtractor -- PRACTICAL

Parses both ruff JSON format (flat list of violations) and eslint JSON format (file objects with messages lists). This covers the two most popular linters for Python and TypeScript.

**Observation**: The extractor does not handle ruff's SARIF output format, which is becoming more common in CI/CD pipelines. This is a minor gap -- JSON is still the default output format for both tools.

### 3. ComplexityExtractor -- PRACTICAL

Reads radon `cc --json` output correctly. Extracts cyclomatic complexity average/max and function length average/max from the radon block structure.

**Observation**: Does not support eslint's `complexity` rule output for TypeScript/JavaScript projects. A frontend project would need a separate complexity extractor. This is acceptable for the initial implementation (Python-focused) but should be noted.

### 4. SecurityExtractor -- THOROUGH

Handles two tool chains:
- **Bandit**: Parses JSON output, maps severity/confidence combinations to critical/high/medium categories. The `HIGH severity + HIGH confidence = critical_vulns` mapping is sensible.
- **Gitleaks**: Parses JSON findings for secrets detection. Simple and effective.

**Note on secrets_exposed inversion**: The `_normalize_variable` function in domain.py (line 86-88) correctly inverts `secrets_exposed` for scoring: `True -> 0.0` (bad), `False -> 1.0` (good). This inversion is sound -- secrets being exposed is the negative condition.

### 5. DocumentationExtractor -- PRACTICAL

Parses interrogate output (both text and JSON badge format) and mypy stats. The text parsing uses regex to find percentage patterns, with multiple fallback strategies. The changelog detection scans `changed_files` for common changelog filenames.

**Observation**: The changelog filename set (`changelog.md`, `changelog`, `changes.md`, `changes`, `history.md`) does not include `CHANGELOG.md` (uppercase). Python's `f.name.lower()` comparison (line 519) handles this correctly via case-insensitive matching. Good.

### 6. ConventionExtractor -- ADEQUATE

Parses black `--check` and isort `--check` output by looking for indicator strings. The naming consistency score is read from a custom JSON report, which is pragmatic (different projects have different naming conventions).

**Observation**: The `format_compliant` variable is set by both LintExtractor and ConventionExtractor, which could lead to inconsistent values depending on extractor ordering. The last extractor wins due to dict.update() semantics. This is acknowledged in the spec but could be confusing.

### 7. SpecComplianceExtractor -- CLEVER

Uses regex to extract FR-NNN and SC-NNN identifiers from spec.md text, then cross-references against a test mapping JSON file. This is a practical approach that doesn't require any special tooling -- just a spec file and a test results mapping.

**Observation**: The regex `r"\b({re.escape(prefix)}\d{{3}})\b"` matches exactly 3-digit IDs (FR-001, SC-005). If a spec has more than 999 requirements (unlikely but possible), this would miss them. Trivial to fix with `\d{3,}` but not urgent.

### 8. Scaffold Tuning

Reviewed scaffolds from the spec description and the scaffolds directory:
- **startup-mvp**: Low ceremony -- security weight 5x, test quality 1.5x, everything else low. Appropriate for fast iteration.
- **healthcare**: High ceremony -- spec compliance 5x, security 5x, documentation 3x. Appropriate for regulated environments.
- **enterprise**, **open-source**, **api-service**: Additional scaffolds with sensible weight distributions.

The scaffold system is well-designed for target audience differentiation.

---

## Concerns

| # | Severity | Item |
|---|----------|------|
| 1 | Low | No eslint complexity support (JavaScript/TypeScript projects) |
| 2 | Low | format_compliant variable set by two extractors (potential override) |
| 3 | Info | ruff SARIF format not supported |
| 4 | Info | FR/SC regex limited to 3-digit IDs |

---

## Recommendation

Accept. The extractors are practical, handle real tool output correctly, and degrade gracefully when tools are missing. The scaffolds are well-tuned for their target audiences.
