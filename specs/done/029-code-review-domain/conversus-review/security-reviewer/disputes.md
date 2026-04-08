# Security Reviewer — Final Disputes and Convergence

---

### Remaining Disputes

- **Dispute: Should `high_vulns > 0` be a hard block on healthcare and enterprise scaffolds?**
  - **My claim**: HIGH severity vulnerabilities in regulated (healthcare) and production (enterprise) environments should be hard blocks, not just score penalties. A single HIGH severity vulnerability currently passes the startup-mvp scaffold through dimension scoring (security dimension averages to ~0.875, above the 0.8 threshold).
  - **Opposing position(s)**: No reviewer explicitly challenged this recommendation, but the spec-compliance auditor's framework treats scaffold content as a tuning decision, not a compliance issue. The spec (Section 2, scaffolds) defines the healthcare hard blocks as `secrets_exposed`, `critical_vulns > 0`, `has_spec == false`, and `has_changelog_entry == false`. Adding `high_vulns > 0` would change the spec's defined scaffold.
  - **Why I will not concede**: The spec defines "critical_vulns" as a synthetic severity (HIGH + HIGH confidence) that excludes HIGH-severity/MEDIUM-confidence findings. A B602 (subprocess shell injection) flagged as HIGH severity but MEDIUM confidence is classified as `high_vulns`, not `critical_vulns`. In a healthcare context, a shell injection vulnerability should be a hard block regardless of confidence level. The current scaffolds allow genuine security vulnerabilities to pass through dimension averaging.
  - **Counter-argument to their position**: Scaffold tuning is a design decision, but the healthcare scaffold claims to enforce "regulated environment" standards. A regulated environment that permits HIGH severity vulnerabilities through dimension averaging is not living up to its description. Either the scaffold description should be weakened or the hard blocks should be strengthened.
  - **Proposed resolution path**: Add `high_vulns > 0` to the healthcare scaffold's hard blocks. For enterprise, add it as a configurable option that defaults to enabled. For startup-mvp and open-source, leave it as a score penalty only.

- **Dispute: Edge case coverage heuristic extractor**
  - **My claim**: `edge_case_coverage` from the spec (Section 2) should be approximated by analyzing test names and docstrings for keywords like "edge", "boundary", "error", "invalid", "empty", "null", "overflow". Even a rough heuristic is better than permanent None.
  - **Opposing position(s)**: The devex-advocate argues that spec variables without standard tool output should be categorized as "future/manual" and not extracted. The spec-compliance auditor suggests categorizing variables as "auto-extractable" vs. "heuristic/future."
  - **Why I will not concede**: Edge case coverage is the most security-relevant variable in the spec. Error paths and boundary conditions are the primary surface for injection attacks, buffer overflows, and denial-of-service. A heuristic that analyzes test names for security-relevant keywords is imperfect but provides signal where None provides nothing. The heuristic's false positive rate (tests named "test_edge_layout" falsely counted as edge case tests) is acceptable because the variable is one of multiple inputs to the test_quality dimension.
  - **Counter-argument to their position**: The devex-advocate's position that "adding extractors for uncomputable variables produces permanent None values" is correct for truly uncomputable variables (coupling_score). But edge_case_coverage IS computable by heuristic. The distinction between "no standard tool" and "uncomputable" is important. A heuristic extractor that scans test names is a 50-line implementation with real value.
  - **Proposed resolution path**: Implement a heuristic `EdgeCaseExtractor` that scans test file names and docstrings for security-relevant patterns. Mark it as "heuristic" in its docstring and variable declaration. Include it in the default extractor list but document its approximate nature.

---

### Convergence

- **Converged: DomainScore.variables is a P1 bug fix**
  - **Shared position**: Unanimous across all three reviews. The missing `variables=variables` in the DomainScore constructor is a bug that breaks the audit trail for gate integration and score verification.
  - **Agreeing agents**: security-reviewer, devex-advocate, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Independent discovery in Phase 1.

- **Converged: `missing_data_policy` resolves the None-handling tension**
  - **Shared position**: My original recommendation to block on missing security data was correctly identified by the spec-compliance auditor as violating FR-003. The per-scaffold `missing_data_policy` field resolves the tension: healthcare can require security reports, startup-mvp can exclude missing data, all while preserving FR-003.
  - **Agreeing agents**: security-reviewer, devex-advocate, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Security-reviewer proposed configurable penalty in Phase 1. Spec-compliance challenged FR-003 violation in Phase 2. Three-way convergence on `missing_data_policy` in Phase 3. Security-reviewer withdrew recommendation #2 (hard block on None).

- **Converged: Duplicate variable ownership must be resolved**
  - **Shared position**: Same as devex-advocate's convergence statement. `format_compliant` → ConventionExtractor, `has_changelog_entry` → GitDiffExtractor.
  - **Agreeing agents**: security-reviewer, devex-advocate, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Identified by devex-advocate, confirmed by both cross-reviewers.

- **Converged: The core extraction-scoring pipeline is solid**
  - **Shared position**: FR-001 through FR-009 are substantially met. Extractors parse real tool output correctly. Scaffolds validate against Pydantic. Hard blocks override composite scores. The inner layers of the architecture are production-quality.
  - **Agreeing agents**: security-reviewer, devex-advocate, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: All three Phase 1 reviews independently confirmed the core pipeline works correctly.

- **Converged: `_INVERTED_BOOLEANS` should be a module-level constant**
  - **Shared position**: Both security-reviewer and devex-advocate identified this independently. The spec-compliance auditor acknowledges it as a code quality improvement (not a compliance item).
  - **Agreeing agents**: security-reviewer, devex-advocate
  - **Strength**: Bilateral
  - **Path to convergence**: Independent identification in Phase 1 reviews.

---
