# DevEx Advocate — Phase 3 Revision

## Preamble

Revising based on cross-reviews from security-reviewer and spec-compliance. The security-reviewer challenged my None-exclusion fix and coverage threshold assessment. The spec-compliance auditor challenged my FR-006 assessment and my Istanbul format recommendation.

---

### Recommendation Dispositions

#### Recommendation 1: SecurityExtractor None-exclusion creates false sense of security

- **Original position**: CRITICAL. Default missing dimensions to 0.5 penalty score.
- **Disposition**: Modified
- **Explanation**: Both cross-reviewers converge on this being the top issue but challenge the fixed 0.5 penalty. The security-reviewer proposes a per-scaffold configurable penalty (healthcare = 0.0/block, startup-mvp = 0.5). The spec-compliance auditor correctly notes that a blanket penalty violates FR-003 ("missing tool output MUST default variables to None, not zero") and the "works without tools" constraint. I accept the spec-compliance framing: the fix must be at the scaffold level, not the engine level. **Modified recommendation**: Add an optional `missing_data_policy` field to scaffolds with values `exclude` (current behavior), `penalize: <float>`, or `require`. This preserves FR-003 while giving scaffold authors control. The startup-mvp scaffold uses `exclude` for onboarding; healthcare uses `require` for security dimensions.

#### Recommendation 2: `minimum_coverage` threshold bypasses dimension scoring

- **Original position**: HIGH. Route all threshold checks through the dimension system.
- **Disposition**: Modified
- **Explanation**: The security-reviewer makes a compelling defense-in-depth argument: the direct `line_coverage` check prevents dimension averaging from masking a low individual value. I concede that removing the direct check would weaken the threshold. However, the inconsistency is still confusing — `minimum_security: 0.95` checks a dimension average while `minimum_coverage: 0.85` checks a raw variable. **Modified recommendation**: Keep the direct variable check but document it explicitly in scaffold documentation. Add a naming convention: `minimum_<dimension>` checks the dimension score; `minimum_<variable>` checks the raw variable. Rename `minimum_coverage` to `minimum_line_coverage` to make the semantics clear.

#### Recommendation 3: Duplicate `format_compliant` and `has_changelog_entry` across extractors

- **Original position**: HIGH. Assign each variable to exactly one extractor.
- **Disposition**: Surviving
- **Explanation**: All three reviews converge on this being a real issue. No cross-review challenged the fix. The spec-compliance auditor notes the spec does not specify variable ownership, confirming this is an implementation improvement, not a compliance fix. Assign `format_compliant` to ConventionExtractor only (it reads black output, which is the authoritative source). Assign `has_changelog_entry` to GitDiffExtractor only (it reads the changed files list, which is the authoritative source). Remove these variables from LintExtractor and DocumentationExtractor respectively.

#### Recommendation 4: Violation count normalization curve too steep

- **Original position**: MEDIUM. Use a log-based curve for all counts.
- **Disposition**: Modified
- **Explanation**: The security-reviewer argues that the steep curve is correct for security counts (one HIGH vuln should dramatically reduce the score) but inappropriate for quality counts (5 lint violations should not score like 50). I accept this distinction. **Modified recommendation**: Use variable-category-specific curves. Security counts (`critical_vulns`, `high_vulns`, `medium_vulns`) keep `1 / (1 + count)`. Quality counts (`lint_violation_count`) use `1 / (1 + log2(1 + count))`. This makes 5 lint violations score ~0.28 instead of 0.167, and 50 violations score ~0.15 instead of 0.0196. The security curve remains punitive as intended.

#### Recommendation 5: SecurityExtractor should support Semgrep and CodeQL

- **Original position**: MEDIUM. Add SARIF format support.
- **Disposition**: Surviving
- **Explanation**: The security-reviewer agrees on SARIF but adds dependency scanning (pip-audit, npm-audit) as a higher priority. I accept that dependency scanning is important but maintain that a generic SARIF parser covers more tools with less code. **Combined recommendation**: Implement (1) a SARIF generic extractor that covers Semgrep, CodeQL, and any other SARIF-producing tool, plus (2) specific parsers for pip-audit and npm-audit JSON. The SARIF parser is the higher-leverage implementation.

#### Recommendation 6: Scaffold documentation with score simulation examples

- **Original position**: LOW.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this. It remains a documentation improvement.

#### Recommendation 7: SpecComplianceExtractor test mapping generation tooling

- **Original position**: LOW.
- **Disposition**: Surviving
- **Explanation**: All reviews agree the manual test mapping is a friction point. A pytest plugin that generates the mapping would make the spec compliance dimension practical.

---

### New Recommendations from Cross-Review

#### New Recommendation 8: DomainScore.variables bug fix

- **Position**: P1 (bug fix)
- **Source**: Identified by spec-compliance auditor, confirmed by security-reviewer
- **Explanation**: `CodeReviewDomain.score()` (domain.py line 448) does not pass `variables=variables` to the `DomainScore` constructor, unlike the base class implementation. This is a one-line bug fix that restores the audit trail for gate integration. Both cross-reviewers independently identified this.

#### New Recommendation 9: Spec amendment for `missing_data_policy`

- **Position**: P2 (spec change)
- **Source**: Derived from the three-way discussion between all reviewers about None handling
- **Explanation**: The current spec's FR-003 creates a tension with the security-reviewer's concerns about missing data. The resolution requires a spec amendment adding `missing_data_policy` to the scaffold schema. This should be filed as a spec update, not an implementation change, because it modifies the plugin's behavior contract.

---
