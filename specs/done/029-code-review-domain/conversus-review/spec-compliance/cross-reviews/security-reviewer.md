# Cross-Review: spec-compliance reviews security-reviewer

## Context

The spec-compliance auditor evaluates the security-reviewer's Phase 1 review against the formal requirements, checking whether security concerns map to actual spec violations and whether proposed fixes would conflict with existing FRs.

---

### Dangerous Contradictions

- **Hard blocks on missing security data conflicts with FR-003**
  - **security-reviewer claims**: Recommendation #2 states that when `secrets_exposed` is None, the system should block or treat None as "unknown, which is not clean." This applies to all scaffolds that list `secrets_exposed` in hard_blocks.
  - **spec-compliance claims**: FR-003 is explicit: "Missing tool output MUST default variables to None (not zero), with a warning." The hard block evaluation function correctly returns `False` when a variable is None (domain.py line 197-198). Changing this to return `True` (trigger block) on None would violate FR-003's intent. Furthermore, the spec's Constraints section (Section 6) states: "The plugin MUST work without any code analysis tools installed (all variables default to None)." If None triggers hard blocks, the plugin cannot work without tools installed — every scaffold with `secrets_exposed` in hard_blocks would immediately BLOCK.
  - **Why this is dangerous**: The security-reviewer's recommendation, if implemented literally, would break two spec requirements (FR-003 and the "works without tools" constraint). A project with no tools installed would receive BLOCK verdicts on all scaffolds, making the tool unusable for evaluation or onboarding.
  - **Suggested resolution**: The correct fix is at the scaffold level, not the engine level. Add an optional `required_reports` field to scaffolds listing which tool reports must be present for the scaffold to produce a valid verdict. If a required report is missing, the scaffold returns a new verdict: "incomplete" (distinct from pass/block/revise). This preserves FR-003 (None defaults), preserves the "works without tools" constraint (scaffolds without `required_reports` work normally), and addresses the security concern (healthcare scaffolds can require security reports).

- **Gaming vector #4 (hard block bypass via missing reports) overstated**
  - **security-reviewer claims**: "A project with active security vulnerabilities and exposed secrets can score 'pass' on all scaffolds simply by not running security scanners."
  - **spec-compliance claims**: This statement is true but misleading. A project that does not run security scanners has *unknown* security posture, not "active vulnerabilities." The tool cannot detect what it cannot see. The spec's design choice (None = missing, not None = bad) is philosophically correct for a tool that reads existing output. The gaming vector exists, but it is inherent to any system that reads optional tool output. The mitigation is organizational (require security scanning in CI/CD), not architectural (change how the scorer handles None).
  - **Why this is dangerous**: If the implementation team accepts the "hard block bypass" framing, they may implement changes that violate FR-003 and the constraints. The correct framing is "the domain cannot assess what it cannot see" — which is a limitation, not a vulnerability.
  - **Suggested resolution**: Acknowledge the limitation in documentation. Recommend that CI/CD pipelines ensure all required tool reports are generated before invoking the domain. The domain's responsibility is scoring provided data, not ensuring data completeness.

---

### Tensions

- **`_INVERTED_BOOLEANS` location: module-level constant vs. configuration**
  - **security-reviewer's position**: Elevate `_INVERTED_BOOLEANS` to module-level constant for maintainability.
  - **spec-compliance's position**: The spec does not address normalization implementation details. The `_INVERTED_BOOLEANS` set is an implementation artifact, not a spec concept. Moving it to module level is a code quality improvement, not a compliance fix. No FR or SC addresses where normalization constants are defined.
  - **Nature of tension**: The security-reviewer frames this as a security maintenance risk. The spec-compliance auditor frames it as out of scope for compliance review. Both are right within their domains.
  - **Coordination needed**: Accept the recommendation as a code quality improvement. Do not track it as a spec compliance item.

- **Dependency vulnerability scanning: spec gap or implementation gap?**
  - **security-reviewer's position**: The absence of dependency scanning (pip-audit, npm-audit) is a HIGH severity gap.
  - **spec-compliance's position**: FR-001 lists "pytest-cov XML, eslint JSON, ruff JSON, radon JSON" as the required formats. The spec's Section 2 parameters list includes `critical_vulns` and `high_vulns` derived from "SAST/dependency scan" — note "dependency scan" is mentioned. FR-001's format list does not include pip-audit or npm-audit formats, but the parameter definitions reference dependency scanning as a data source. This is a spec inconsistency: the parameters imply dependency scanning support but FR-001's format list does not include dependency scanning formats.
  - **Nature of tension**: The security-reviewer sees a missing implementation. The spec-compliance auditor sees a spec inconsistency — the parameter definitions promise more than FR-001 requires.
  - **Coordination needed**: File a spec clarification: either add pip-audit/npm-audit JSON to FR-001's required format list, or remove "dependency scan" from the parameter derived_from fields. The current spec is internally inconsistent.

---

### Safe Agreements

- **secrets_exposed inversion logic is correct**
  - **Shared position**: The security-reviewer's detailed analysis of the normalization path (`_INVERTED_BOOLEANS`) and the hard block path (truthy check) confirms both are correct. The spec-compliance auditor confirms the hard block test `test_secrets_exposed_blocks_all_scaffolds_sc002` passes on all scaffolds. Both reviews agree the inversion is implemented correctly.
  - **Confidence level**: High.

- **Bandit severity mapping is undocumented but functionally correct**
  - **Shared position**: The security-reviewer correctly identifies that "critical" is a synthetic severity combining HIGH + HIGH confidence. The spec (Section 2) defines `critical_vulns` as a parameter derived from "SAST/dependency scan" without specifying the mapping from tool output to the variable. The implementation's mapping is a reasonable design choice. The spec-compliance auditor agrees this is not a spec violation (the spec does not mandate a mapping) but should be documented.
  - **Confidence level**: High.

- **API path traversal risk is a valid future concern**
  - **Shared position**: The security-reviewer's observation about potential path traversal in POST /api/review is valid for the API layer (FR-017). The spec-compliance auditor confirms FR-017 is NOT MET (no API exists), so this is a design recommendation for future implementation, not a current gap. Both agree it should be documented as a security requirement for the API layer.
  - **Confidence level**: High.

---
