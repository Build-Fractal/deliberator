# Security Reviewer — Phase 3 Revision

## Preamble

Revising based on cross-reviews from devex-advocate and spec-compliance. The devex-advocate challenged my missing data penalty and hard block on None recommendations. The spec-compliance auditor directly contradicted my recommendation #2 as violating FR-003 and the "works without tools" constraint. Both cross-reviews converge on the point that my recommendations, while security-motivated, would break existing spec requirements if implemented as stated.

---

### Recommendation Dispositions

#### Recommendation 1: Missing data must not improve scores

- **Original position**: CRITICAL. Apply a configurable penalty when a dimension has no data.
- **Disposition**: Modified
- **Explanation**: The spec-compliance auditor's cross-review is correct: a blanket penalty on missing data would violate FR-003 ("MUST default to None, not zero") and the "works without tools" constraint. The devex-advocate's cross-review adds that penalizing missing data creates hostile onboarding. I concede that my original framing was too aggressive.

  However, I do not concede the substance: the gaming vector is real. The resolution is to make the penalty scaffold-specific rather than system-wide. **Modified recommendation**: Add `missing_data_policy` to the scaffold schema with per-dimension control. Example:
  ```yaml
  missing_data_policy:
    security: require    # No security reports → "incomplete" verdict
    test_quality: penalize: 0.5  # No coverage → treat as 50%
    documentation: exclude  # Missing docs tools → skip dimension
  ```
  Startup-mvp can use `exclude` for all dimensions (current behavior). Healthcare can use `require` for security. This satisfies FR-003 (variables still default to None) and the "works without tools" constraint (scaffolds without `missing_data_policy` work as today).

#### Recommendation 2: Hard blocks must trigger on missing security data

- **Original position**: CRITICAL. When `secrets_exposed` is None, the system should block.
- **Disposition**: Withdrawn
- **Explanation**: The spec-compliance auditor is right: this directly contradicts FR-003 and the "works without tools" constraint. If None triggers hard blocks, the plugin blocks when tools are not installed, violating two spec requirements. The gaming vector (bypass hard blocks by omitting reports) is real but must be addressed through the `missing_data_policy` scaffold mechanism (Recommendation 1), not by changing the hard block evaluation engine.

  I withdraw this recommendation and defer to the `missing_data_policy: require` mechanism. When a scaffold lists `security: require` in `missing_data_policy`, missing security reports produce an "incomplete" verdict — which is distinct from "block" (something is wrong) and "pass" (everything is fine). This preserves FR-003 while closing the bypass.

#### Recommendation 3: Add dependency vulnerability scanning

- **Original position**: HIGH.
- **Disposition**: Surviving
- **Explanation**: Both cross-reviewers agree dependency scanning is missing. The devex-advocate proposes a SARIF generic parser; I proposed tool-specific parsers. The combined approach (SARIF + pip-audit + npm-audit) covers both code-level SAST and dependency scanning. The spec-compliance auditor correctly notes that FR-001's format list does not include dependency scanning formats but the parameter `derived_from` fields mention "dependency scan" — a spec inconsistency that should be resolved.

#### Recommendation 4: Elevate `_INVERTED_BOOLEANS` to module-level constant

- **Original position**: HIGH.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this. The devex-advocate agrees it improves discoverability. The spec-compliance auditor notes it is not a compliance item, which is correct — it is a code quality improvement.

#### Recommendation 5: Add `high_vulns > 0` hard block to healthcare and enterprise scaffolds

- **Original position**: MEDIUM.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this. The devex-advocate's review did not address scaffold hard block coverage. The spec-compliance auditor's review confirms scaffold hard blocks are scaffold-specific (not engine-level), meaning this change is a scaffold tuning decision, not an engine change.

#### Recommendation 6: Document the synthetic "critical" severity mapping

- **Original position**: MEDIUM.
- **Disposition**: Surviving
- **Explanation**: The devex-advocate agrees documentation is needed (framing it as a predictability issue). The spec-compliance auditor confirms the spec does not mandate a mapping, so the implementation's choice is valid but should be documented.

#### Recommendation 7: Add path validation for API inputs

- **Original position**: LOW.
- **Disposition**: Surviving
- **Explanation**: The spec-compliance auditor confirms FR-017 is NOT MET (no API exists), making this a future implementation concern. When the API is built, path validation should be a requirement. No cross-review challenged this.

---

### New Recommendations from Cross-Review

#### New Recommendation 8: DomainScore.variables bug fix

- **Position**: P1
- **Source**: Identified by spec-compliance auditor, endorsed by devex-advocate
- **Explanation**: `CodeReviewDomain.score()` does not populate `DomainScore.variables`. This breaks the audit trail that makes scores verifiable. From a security perspective, a score without its backing variables is an unsigned claim — it cannot be independently verified. One-line fix.

#### New Recommendation 9: Variable-category-specific normalization curves

- **Position**: P2
- **Source**: Emerged from cross-review tension with devex-advocate
- **Explanation**: The devex-advocate correctly identifies the `1 / (1 + count)` curve as too steep for lint violations but I maintain it is correct for security counts. The resolution is variable-category-specific curves: keep the steep curve for security counts, use a log-based curve for quality counts. This satisfies both perspectives.

---
