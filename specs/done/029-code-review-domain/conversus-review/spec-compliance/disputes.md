# Spec Compliance Auditor — Final Disputes and Convergence

---

### Remaining Disputes

- **Dispute: FR-003 scope — does "default to None" prohibit downstream penalties?**
  - **My claim**: FR-003 states "Missing tool output MUST default variables to None (not zero), with a warning." This constrains the extraction layer: extractors must produce None for missing data. It does not constrain the scoring layer: how the scorer handles None dimensions is a separate concern. The `missing_data_policy` scaffold field operates in the scoring layer, not the extraction layer, so it is compatible with FR-003.
  - **Opposing position(s)**: A strict reading of FR-003 combined with the constraint "The plugin MUST work without any code analysis tools installed (all variables default to None)" could be interpreted as requiring that None-only inputs produce a valid pass/block/revise verdict without penalties. The `missing_data_policy: require` option would produce an "incomplete" verdict when all data is missing, which could be seen as violating "MUST work without tools installed."
  - **Why I will not concede**: "Works without tools installed" means "does not crash and produces a meaningful result." An "incomplete" verdict IS a meaningful result — it tells the user they need to run tools before the scaffold can score their code. This is more useful than a meaningless "pass" verdict based on no data. The constraint's intent is crash-prevention and zero-dependency operation, not guarantee-of-positive-verdict.
  - **Counter-argument to their position**: If "works without tools" means "produces pass/block/revise," then the current behavior already fails this test in some cases: healthcare scaffold blocks when `has_spec == false`, and if no spec is provided, `has_spec` defaults to `False` (not None — see SpecComplianceExtractor line 701), triggering a BLOCK verdict with no tools installed. The constraint is already not universally satisfied. Adding "incomplete" as a verdict is no more restrictive than the current BLOCK-on-no-spec behavior.
  - **Proposed resolution path**: Clarify in the spec that "works without tools" means "does not crash or require tool installation." Scaffold-specific verdicts (including "incomplete") are the scaffold's responsibility. Add "incomplete" as a fourth verdict option in the spec.

- **Dispute: Are spec variables normative or informational?**
  - **My claim**: The spec's Section 2 parameter list defines 18 variables. The implementation extracts a different set (adding `medium_vulns`, `cyclomatic_complexity_max`, `function_length_avg`, `function_length_max`, `import_order_correct`, `has_spec`, `files_changed`, `lines_added`, `lines_removed` not in the spec; omitting `edge_case_coverage`, `test_to_code_ratio`, `duplication_rate`, `coupling_score` from the spec). The spec's variable list should be treated as normative (all must be implemented) or informational (implementation can diverge).
  - **Opposing position(s)**: The devex-advocate argues variables without standard tools should be categorized as "future." The security-reviewer argues `edge_case_coverage` should be approximated by heuristic.
  - **Why I will not concede**: A spec compliance audit must take a position on whether the parameter list is normative. If it is normative, the implementation is non-compliant for omitting 4 variables and adding 9 unlisted ones. If it is informational, the audit cannot use it as a compliance baseline. The spec uses MUST language for FRs but does not qualify the parameter list with MUST/SHOULD/MAY. This ambiguity should be resolved.
  - **Counter-argument to their position**: Both the devex-advocate and security-reviewer propose practical solutions (categorize, heuristic) but do not address the fundamental question: is the parameter list a requirement or a suggestion? Without resolving this, the compliance audit cannot definitively rate extraction completeness.
  - **Proposed resolution path**: Amend the spec to explicitly classify each parameter as MUST (required extractor), SHOULD (expected but optional), or MAY (future/manual). This would make the compliance audit unambiguous.

---

### Convergence

- **Converged: DomainScore.variables is a P1 bug fix**
  - **Shared position**: Unanimous. Add `variables=variables` to the DomainScore constructor in `CodeReviewDomain.score()`.
  - **Agreeing agents**: spec-compliance, devex-advocate, security-reviewer
  - **Strength**: Unanimous
  - **Path to convergence**: Independent discovery.

- **Converged: FR-001 through FR-003 are MET**
  - **Shared position**: The extraction core satisfies all three extraction FRs. Standard tool output parsing works (FR-001). Extractors are pluggable via Protocol (FR-002). Missing data defaults to None with warnings (FR-003). Tests provide strong evidence.
  - **Agreeing agents**: spec-compliance, devex-advocate, security-reviewer
  - **Strength**: Unanimous
  - **Path to convergence**: All Phase 1 reviews independently confirmed.

- **Converged: FR-005 is MET — hard blocks override composite scores**
  - **Shared position**: The `if triggered_blocks: verdict = "block"` check at line 408 is the first verdict evaluation, ensuring hard blocks always produce BLOCK. SC-002 test confirms universal blocking on `secrets_exposed`.
  - **Agreeing agents**: spec-compliance, devex-advocate, security-reviewer
  - **Strength**: Unanimous
  - **Path to convergence**: Structural code analysis confirmed by all reviews.

- **Converged: FR-006 is MET (revised from PARTIALLY MET)**
  - **Shared position**: The dimension-level impact ordering satisfies the spec's intent. Devex-advocate's argument that variable-level ordering would be confusing was accepted in Phase 3 revision.
  - **Agreeing agents**: spec-compliance (revised), devex-advocate
  - **Strength**: Bilateral
  - **Path to convergence**: Devex-advocate challenged in Phase 2 cross-review. Spec-compliance conceded in Phase 3.

- **Converged: `missing_data_policy` scaffold field resolves None-handling tension**
  - **Shared position**: All three reviews agree on the mechanism. Requires spec amendment.
  - **Agreeing agents**: spec-compliance, devex-advocate, security-reviewer
  - **Strength**: Unanimous
  - **Path to convergence**: Three-way negotiation across Phases 1-3.

- **Converged: Persistence layer (FR-010 through FR-013) is Phase 2 scope**
  - **Shared position**: NOT MET verdicts are factually correct. The implementation follows a layer-by-layer build strategy. NOT MET should include phasing context.
  - **Agreeing agents**: spec-compliance, devex-advocate
  - **Strength**: Bilateral
  - **Path to convergence**: Devex-advocate requested context in Phase 2. Spec-compliance accepted.

---
