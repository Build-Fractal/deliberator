# Cross-Review: spec-compliance reviews devex-advocate

## Context

The spec-compliance auditor evaluates the devex-advocate's Phase 1 review against the formal requirements. The devex-advocate focuses on practical usability; this cross-review checks whether the usability observations map to spec gaps.

---

### Dangerous Contradictions

- **SecurityExtractor None-exclusion: different scope than FR-003**
  - **devex-advocate claims**: The None-exclusion logic creates a perverse incentive where not running security scanners improves your score. Rates this as the #1 CRITICAL recommendation.
  - **spec-compliance claims**: This observation is accurate but misframes the relationship with the spec. FR-003 requires "missing tool output MUST default variables to None (not zero), with a warning." The implementation correctly follows FR-003. The incentive problem is a spec design issue, not an implementation bug. The spec chose to treat missing data as missing (None) rather than as bad (zero). The devex-advocate's recommendation to penalize missing dimensions would require a spec amendment — it cannot be implemented without contradicting FR-003's "not zero" language.
  - **Why this is dangerous**: If the implementation team treats this as a bug fix, they would change the None behavior, violating FR-003. It needs to be recognized as a spec limitation that requires a formal spec update before implementation.
  - **Suggested resolution**: File a spec amendment proposing a `missing_data_policy` scaffold field with options: `exclude` (current behavior, FR-003 compliant), `penalize` (configurable penalty score), or `block` (missing required tool output triggers block). The spec amendment preserves FR-003 for the `exclude` policy while enabling stricter policies.

- **Istanbul JSON format support: not in the spec**
  - **devex-advocate claims**: The CoverageExtractor does not handle Istanbul (JavaScript) JSON coverage format, leaving JavaScript projects with no coverage data.
  - **spec-compliance claims**: FR-001 specifies "pytest-cov XML, eslint JSON, ruff JSON, radon JSON" as the required standard formats. Istanbul JSON is not in the required list. The CoverageExtractor's support for Cobertura XML and lcov already exceeds the spec's requirements (lcov is not mentioned in FR-001). Supporting Istanbul JSON would be a nice-to-have but is not a spec compliance gap.
  - **Why this is dangerous**: If the Istanbul format is added as a "bug fix" based on the devex-advocate's recommendation, it sets a precedent where any format not supported is treated as a bug. The spec's format list is intentionally finite.
  - **Suggested resolution**: Track Istanbul support as an enhancement request, not a compliance fix. The spec should be updated if JavaScript coverage is important enough to be a requirement.

---

### Tensions

- **Normalization magic numbers vs. spec configurability**
  - **devex-advocate's position**: The hard-coded normalization formulas (complexity: `1.0 - (cc - 1.0) / 19.0`, function length: `1.0 - (length - 10.0) / 90.0`) use magic numbers that produce non-intuitive scores.
  - **spec-compliance's position**: The spec does not specify normalization formulas. Section 2 defines parameter ranges (`cyclomatic_complexity_avg range: {min: 1.0, max: 100.0}`) but does not prescribe how to normalize within those ranges. The implementation's normalization is a design decision, not a spec compliance issue. The spec's ranges suggest a normalization window of [1, 100] for complexity, but the implementation uses [1, 20], meaning CC=50 (within spec range) normalizes to 0.0 (fully bad). This is a tighter standard than the spec implies but does not violate any FR.
  - **Nature of tension**: The devex-advocate wants normalization to be configurable or at least documented. The spec is silent on normalization, leaving it as an implementation decision. Neither position is wrong, but they address different concerns.
  - **Coordination needed**: Document the normalization formulas in the scaffold or domain documentation so developers understand how raw values map to scores. This is a documentation improvement, not a compliance fix.

- **Recommendation specificity**
  - **devex-advocate's position**: Recommendations lack specificity — "reduce avg complexity (7.2)" gives no file or function targets.
  - **spec-compliance's position**: FR-006 says "the change that would most improve the overall score listed first." It does not require file-level or function-level targeting. The current implementation satisfies FR-006's ordering requirement. Adding file-level targeting would require extractors to track per-file metrics, which the current architecture does not support (extractors produce aggregate variables, not per-file breakdowns).
  - **Nature of tension**: The devex-advocate wants more actionable recommendations; the spec requires only ordering by impact. The gap is a UX enhancement, not a compliance issue.
  - **Coordination needed**: Note this as a future enhancement. Per-file recommendations require an architectural change (extractors produce per-file data, scorer aggregates) that is out of scope for the current spec.

---

### Safe Agreements

- **Duplicate `format_compliant` and `has_changelog_entry` across extractors is a real issue**
  - **Shared position**: Both reviews identify the duplicate variable production. The spec-compliance auditor confirms this is not addressed by any FR — the spec does not specify which extractor owns which variable. The devex-advocate correctly identifies the last-writer-wins behavior as problematic. Both agree the fix is to assign each variable to exactly one extractor.
  - **Confidence level**: High.

- **The 5 scaffolds satisfy FR-007**
  - **Shared position**: Both reviews confirm 5 scaffolds exist with the required names. The devex-advocate evaluates their tuning quality; the spec-compliance auditor confirms they validate against Pydantic. Both perspectives are satisfied that FR-007 is met.
  - **Confidence level**: High.

- **Test coverage for extractors is thorough**
  - **Shared position**: The devex-advocate's per-extractor assessment and the spec-compliance auditor's FR-003 evidence both rely on the test suite. Tests cover: correct parsing (with fixtures), missing reports (None behavior), edge cases (empty files, unknown formats). The test suite is the strongest evidence for FR-001 and FR-003 compliance.
  - **Confidence level**: High.

---
