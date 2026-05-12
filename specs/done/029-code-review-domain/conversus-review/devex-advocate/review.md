# DevEx Advocate — Phase 1 Review: Code Review Domain (Spec 029)

## Executive Summary

The code review domain plugin delivers a solid foundation for quantifying code review as an optimization problem. The extractor-scorer-scaffold architecture is sound, and the 8 built-in extractors cover the major dimensions developers care about. However, several practical gaps would frustrate adoption in real workflows: extractors expect specific file paths as context attributes but provide no discovery mechanism; the scoring normalization functions use hard-coded magic numbers that will surprise developers; and the scaffold weight-to-score relationship is opaque enough that a developer cannot intuitively predict whether a change will improve their score.

The 5 scaffolds are a good starting set but have tuning issues: the healthcare scaffold's `minimum_coverage` threshold references `line_coverage` directly rather than through the dimension scoring system, creating a bypass of the normalization layer. The startup-mvp scaffold's documentation weight (0.2) is so low that a project could have zero docstrings and barely notice the score impact, which may be intentional but is never stated.

The test suite is thorough for extractors but thin for scoring edge cases. The recommendation engine produces useful output but lacks the specificity a developer needs to act — "fix 5 high vulns" is actionable but "reduce avg complexity (7.2)" gives no file or function targets.

---

## Extractor Practicality Assessment

### CoverageExtractor — GOOD

Reads Cobertura XML and lcov.info, the two dominant coverage formats. The auto-detection fallback (try XML parse, then check for `LF:` markers) is pragmatic. One gap: Istanbul (JavaScript) produces a different JSON format that is not handled. The extractor silently returns None for Istanbul JSON, which satisfies FR-003 but leaves JavaScript projects with no coverage data despite having a report.

### LintExtractor — GOOD WITH GAPS

Handles ruff flat-list and eslint file-object JSON correctly. The edge case where eslint produces a file object with an empty `messages` list counts as zero violations — correct. However, the eslint format detection relies on the presence of a `messages` key, which is fragile: some eslint formatters (sarif, stylish) produce different shapes. The extractor would silently count them as one violation each (falling into the ruff path), which is wrong. More critically, the `format_compliant` variable is derived entirely from lint violation count (`count == 0`), conflating two distinct concepts. A project can have zero lint violations but still fail `black --check`. The ConventionExtractor separately produces `format_compliant` from black output, but because extractors run sequentially and later extractors override earlier ones, the ConventionExtractor's `format_compliant` will overwrite LintExtractor's — but only if both have reports. If only lint_report is provided, `format_compliant` reflects lint, not formatting.

### ComplexityExtractor — GOOD

Parses radon's `{filename: [block_info]}` format correctly. Function length computation from lineno/endline is sound. One concern: the extractor reads `context.complexity_report` but radon produces complexity and raw metrics as separate commands (`radon cc --json` vs `radon raw --json`). The extractor only handles `cc` output, which is fine but should be documented — users expecting `radon raw` metrics will get None values.

### SecurityExtractor — ADEQUATE WITH CRITICAL GAP

Parses bandit JSON and gitleaks JSON. The severity mapping (HIGH severity + HIGH confidence = critical) is a reasonable heuristic but differs from bandit's own severity model, which has no "critical" level. This mapping is undocumented and could confuse developers who expect the numbers to match bandit's output. More importantly: **the extractor does not handle Semgrep, CodeQL, or Snyk** — three of the most widely used SAST tools. A team using Semgrep instead of bandit gets None for all vulnerability variables, meaning the security dimension scores 1.0 (perfect) due to the None-exclusion logic in `_score_dimension`. This is the opposite of safe: missing security data should degrade the score, not improve it.

### SpecComplianceExtractor — ADEQUATE

The FR/SC extraction regex (`\b(FR-\d{3})\b`) is correct for the conversus spec format. The test mapping JSON approach is workable but introduces a manual step: someone must create the mapping file. There is no tooling to generate this mapping from pytest markers or test names. For adoption, this extractor will be the hardest to use because it requires a file that does not exist in most workflows.

### DocumentationExtractor — GOOD

Handles both interrogate text and JSON badge formats. The changelog detection via filename matching is pragmatic. The mypy stats parser handles both percentage and fraction formats. One minor issue: `has_changelog_entry` is produced by both DocumentationExtractor and GitDiffExtractor, and the last-writer-wins behavior depends on extractor ordering in `get_extractors()`.

### ConventionExtractor — ADEQUATE

Reads black and isort text output. The `naming_consistency` variable requires a custom JSON report that no standard tool produces, making it effectively unusable without custom tooling. This should be documented as "requires custom analysis" or removed from the default dimension.

### GitDiffExtractor — GOOD

The `git diff --stat` summary line parser is correct. The `changed_files` override from context is a good design — it means the extractor works both with a pre-generated diff stat file and with a programmatic file list.

---

## Scaffold Tuning Assessment

### startup-mvp — REASONABLE

Security weight 5.0 with low everything else matches the "ship fast with guardrails" philosophy. The documentation weight (0.2) is so low that this dimension is effectively invisible in the score. This is probably intentional but creates a risk: teams adopt startup-mvp, grow, and never notice their documentation score because the weight suppresses it.

### healthcare — OVERTUNED

The `minimum_spec_compliance: 0.9` threshold is aggressive. The spec compliance dimension aggregates `fr_satisfaction_rate`, `sc_pass_rate`, and `has_spec`. If a spec has 19 FRs and 1 is unmet, `fr_satisfaction_rate` = 0.947, but if `sc_pass_rate` is 0.8 (4 of 5 SCs pass), the dimension average is ~0.88, which fails the 0.9 threshold. The threshold operates on the dimension average, not on individual variables, so a high FR rate can be dragged below threshold by a moderate SC rate. This interaction is non-obvious and will frustrate developers.

Additionally, the `minimum_coverage` threshold is handled as a special case in the scoring code rather than through the dimension system. The code at line 423 checks `variables.get("line_coverage")` directly against the threshold, bypassing the normalization and dimension averaging. This means `minimum_coverage: 0.85` checks raw `line_coverage`, not the `test_quality` dimension score. This inconsistency is a bug.

### enterprise — BALANCED

Weights are well-distributed. The `minimum_coverage: 0.8` has the same direct-variable-check issue as healthcare.

### api-service — REASONABLE

High security (5.0) and test quality (4.0) weights make sense for API services. The documentation weight (2.5) is higher than enterprise (2.0), which reflects the reality that API documentation is critical.

### open-source — GOOD

Highest documentation weight (4.0) and conventions weight (3.0) of all scaffolds, reflecting the open-source reality that readability and contribution friendliness matter most. No `minimum_coverage` or `minimum_spec_compliance` thresholds, which is correct — open-source projects have diverse maturity levels.

---

## Scoring Intuitiveness

### Normalization

The `_normalize_variable` function uses domain-specific normalization rules that are not configurable:

- **Complexity**: `score = 1.0 - (cc - 1.0) / 19.0` — this means CC=10 scores 0.526 and CC=5 scores 0.789. Developers familiar with cyclomatic complexity thresholds (CC > 10 is "high", CC > 20 is "very high") would expect a steeper penalty curve, not a linear one.
- **Function length**: `score = 1.0 - (length - 10.0) / 90.0` — a 50-line function scores 0.556, which feels harsh for many codebases where 50 lines is normal.
- **Violation counts**: `score = 1 / (1 + count)` — this curve is extremely steep at low counts (1 violation = 0.5, 2 = 0.33) but flattens at high counts (100 violations = 0.0099, 200 = 0.00498). This means the difference between 0 and 1 violation is the same magnitude as the difference between 1 and infinity violations. A developer fixing 50 violations down to 5 would see their score go from 0.02 to 0.167 — barely noticeable in the weighted composite.

### Score Predictability

A developer cannot currently predict their score before running the tool. The weighted composite formula is: `overall = sum(weight * dimension_score) / sum(weights)`, where each dimension score is the average of its normalized variables. This multi-level averaging means small changes to a single variable have unpredictable impact on the overall score. The recommendation engine partially compensates by ordering suggestions by impact, but the impact calculation (`weight * (1 - score)`) does not account for the variable's contribution to the dimension average.

---

## Recommendations

### Ordered by Impact

1. **[CRITICAL] SecurityExtractor None-exclusion creates false sense of security** — When no security tool output is available, all security variables are None, and `_score_dimension` excludes None values from the average. If all security variables are None, the dimension returns None and is excluded from the weighted composite. This means a project with no security scanning scores *higher* than one with scanning that found issues. Either default missing security data to a penalty score (e.g., 0.5) or apply a "missing data penalty" when a dimension has no values. This is the most important fix because it inverts the incentive: the easiest way to get a high security score is to not run a security scanner.

2. **[HIGH] `minimum_coverage` threshold bypasses dimension scoring** — The healthcare and enterprise scaffolds check `variables.get("line_coverage")` directly against `minimum_coverage`, bypassing the normalization and dimension averaging used for all other thresholds. Either route all threshold checks through the dimension system or document this as intentional behavior. Currently it creates a confusing inconsistency where `minimum_security: 0.95` checks the security dimension score but `minimum_coverage: 0.85` checks the raw `line_coverage` variable.

3. **[HIGH] Duplicate `format_compliant` and `has_changelog_entry` across extractors** — Both LintExtractor and ConventionExtractor produce `format_compliant`. Both DocumentationExtractor and GitDiffExtractor produce `has_changelog_entry`. The last-writer-wins behavior depends on extractor ordering. Either remove the duplicates (assign each variable to exactly one extractor) or implement explicit merge semantics.

4. **[MEDIUM] Violation count normalization curve too steep** — The `1 / (1 + count)` formula makes the score effectively binary: 0 violations = 1.0, anything else drops sharply. Consider a log-based curve like `1 / (1 + log(1 + count))` or a threshold-based approach where counts below a configurable threshold score linearly.

5. **[MEDIUM] SecurityExtractor should support Semgrep and CodeQL** — These are the two most popular SAST tools beyond bandit. At minimum, the Semgrep SARIF format and CodeQL SARIF format should be supported. Both use the standard SARIF schema, so a single SARIF parser would cover multiple tools.

6. **[LOW] Add scaffold documentation with score simulation examples** — Each scaffold should include example scenarios showing "if your project looks like X, your score will be Y." This helps developers choose the right scaffold and understand what the numbers mean.

7. **[LOW] SpecComplianceExtractor test mapping generation tooling** — Without tooling to generate the test mapping JSON, the spec compliance dimension is unusable in CI/CD. A pytest plugin that maps test names to FR/SC IDs would make this practical.

---

## Referenced Files

- `<HOME>/code/payer-index-mono/conversus/specs/029-code-review-domain/spec.md` — FR-001 through FR-019, SC-001 through SC-005
- `<HOME>/code/payer-index-mono/conversus/conversus/domains/code_review/domain.py` — scoring logic, lines 76-150 (normalization), 152-202 (hard blocks), 204-300 (recommendations), 315-465 (CodeReviewDomain)
- `<HOME>/code/payer-index-mono/conversus/conversus/domains/code_review/extractors.py` — all 8 extractors, lines 68-745
- `<HOME>/code/payer-index-mono/conversus/tests/test_code_review.py` — test coverage assessment
- `<HOME>/code/payer-index-mono/conversus/conversus/domains/code_review/scaffolds/*.yml` — all 5 scaffolds
