# DevEx Advocate — Final Disputes and Convergence

---

### Remaining Disputes

- **Dispute: `minimum_coverage` threshold semantics — keep direct check or route through dimensions**
  - **My claim**: The `minimum_coverage` threshold should be renamed to `minimum_line_coverage` and documented as a direct variable check, distinct from dimension-level thresholds. The inconsistency where `minimum_security` checks a dimension average but `minimum_coverage` checks a raw variable is confusing for developers.
  - **Opposing position(s)**: The security-reviewer argues the direct check is a defense-in-depth feature that prevents dimension averaging from masking a low individual value. Removing or renaming it could weaken the threshold.
  - **Why I will not concede**: The defense-in-depth argument is valid but the naming inconsistency is a real UX problem. A developer reading `minimum_coverage: 0.85` alongside `minimum_security: 0.95` will assume both operate at the same level of abstraction. When they discover one checks a raw variable and the other checks a dimension average, trust in the scoring system erodes. Renaming to `minimum_line_coverage` makes the semantics explicit without removing the direct check. This is not about removing the feature — it is about honest naming.
  - **Counter-argument to their position**: Defense-in-depth does not require misleading names. The security benefit of the direct check is preserved if it is named correctly. `minimum_line_coverage: 0.85` is just as effective as `minimum_coverage: 0.85` at catching low coverage, but it does not mislead developers about what is being checked.
  - **Proposed resolution path**: Rename `minimum_coverage` to `minimum_line_coverage` in all scaffolds. Add both `minimum_<dimension>` and `minimum_<variable>` as supported threshold types with clear documentation distinguishing them.

- **Dispute: Normalization curves should be configurable vs. hard-coded**
  - **My claim**: The normalization formulas (complexity linear scale, function length linear scale, violation count inverse) should be configurable per-scaffold or at least documented prominently. The current hard-coded magic numbers create an opaque scoring system.
  - **Opposing position(s)**: The spec-compliance auditor notes the spec is silent on normalization, making it an implementation decision. Configurability adds complexity without a spec mandate.
  - **Why I will not concede**: Developer trust depends on score predictability. A developer who reduces cyclomatic complexity from 15 to 10 and sees their score go from 0.26 to 0.53 will wonder why the change is not proportional to their effort. The linear formula `1 - (cc - 1) / 19` is not intuitive and cannot be discovered from the scaffold YAML. At minimum, the normalization rules should be documented. Ideally, scaffolds should support overriding them.
  - **Counter-argument to their position**: "The spec is silent" does not mean "the implementation is fine." The spec defines parameter ranges (Section 2) that imply a normalization window. The implementation's choice of [1, 20] for complexity (vs. the spec's [1, 100]) is a design decision that affects scores. Design decisions should be transparent.
  - **Proposed resolution path**: Document normalization rules in a table accessible to developers. As a future enhancement, allow scaffolds to override normalization parameters per variable.

---

### Convergence

- **Converged: DomainScore.variables is a P1 bug fix**
  - **Shared position**: All three reviews independently identified that `CodeReviewDomain.score()` does not populate `DomainScore.variables`. This is a one-line bug fix (add `variables=variables` to the constructor). The devex-advocate frames it as a data completeness issue, the security-reviewer as an audit trail issue, the spec-compliance auditor as an FR-015 compliance issue. All agree on P1 priority.
  - **Agreeing agents**: devex-advocate, security-reviewer, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Independent discovery in Phase 1. No challenge in Phase 2.

- **Converged: Duplicate variable ownership must be resolved**
  - **Shared position**: `format_compliant` (LintExtractor + ConventionExtractor) and `has_changelog_entry` (DocumentationExtractor + GitDiffExtractor) have last-writer-wins semantics. Assign each variable to exactly one extractor: `format_compliant` → ConventionExtractor, `has_changelog_entry` → GitDiffExtractor.
  - **Agreeing agents**: devex-advocate, security-reviewer, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Identified by devex-advocate in Phase 1. Confirmed by both cross-reviewers.

- **Converged: `missing_data_policy` scaffold field is the right solution for None handling**
  - **Shared position**: The None-exclusion gaming vector is real (security-reviewer, devex-advocate). FR-003 must be preserved (spec-compliance). The resolution is a per-scaffold `missing_data_policy` field that gives scaffold authors explicit control over how missing data affects scoring. This requires a spec amendment.
  - **Agreeing agents**: devex-advocate, security-reviewer, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Three-way negotiation across Phases 1-3. Security-reviewer proposed the configurable penalty. Devex-advocate accepted with scaffold-level granularity. Spec-compliance auditor confirmed FR-003 compatibility.

- **Converged: Persistence layer is NOT MET but on a planned path**
  - **Shared position**: FR-010 through FR-013 are factually not implemented. The extraction-scoring core is the Phase 1 delivery. Persistence is Phase 2. The NOT MET verdicts are correct but should include phasing context.
  - **Agreeing agents**: devex-advocate, spec-compliance
  - **Strength**: Bilateral (security-reviewer focused on append-only enforcement, not phasing)
  - **Path to convergence**: Devex-advocate requested phasing context in Phase 2 cross-review. Spec-compliance accepted.

- **Converged: SARIF generic parser + dependency-specific parsers**
  - **Shared position**: The SecurityExtractor needs broader tool support. A SARIF generic parser covers Semgrep, CodeQL, and other SAST tools. Specific pip-audit and npm-audit parsers cover dependency scanning. Both are needed.
  - **Agreeing agents**: devex-advocate, security-reviewer
  - **Strength**: Bilateral
  - **Path to convergence**: Devex-advocate proposed SARIF in Phase 1. Security-reviewer proposed dependency parsers. Combined in Phase 3.

---
