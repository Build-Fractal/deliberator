# Cross-Review: devex-advocate reviews security-reviewer

## Context

The devex-advocate evaluates the security-reviewer's Phase 1 review from the perspective of developer experience and practical usability. The security-reviewer focuses on threat models, gaming vectors, and security control completeness. This cross-review identifies where security recommendations conflict with usability and where they reinforce each other.

---

### Dangerous Contradictions

- **Missing data penalty vs. developer onboarding friction**
  - **security-reviewer claims**: Missing dimension data should receive a penalty score (e.g., 0.5) rather than being excluded from the composite. This prevents gaming by omitting tool reports.
  - **devex-advocate claims**: Penalizing missing data creates a hostile onboarding experience. A developer trying the tool for the first time with only a coverage report would receive penalties on security, documentation, conventions, spec compliance, and code quality — 5 of 6 dimensions penalized. Their first score would be artificially low, creating a negative first impression. The current None-exclusion behavior lets developers adopt incrementally: start with coverage, add lint next sprint, add security scanning later.
  - **Why this is dangerous**: If the security-reviewer's recommendation is implemented without nuance, the tool becomes unusable for incremental adoption. Developers will not adopt a tool that punishes them for not running every possible analysis tool on day one. But if the devex-advocate's position prevails, the gaming vector remains open.
  - **Suggested resolution**: Implement a per-dimension "required" flag on scaffolds. Healthcare and enterprise scaffolds can mark security as `required: true`, which applies the penalty when security data is missing. Startup-mvp can leave all dimensions optional, allowing incremental adoption. This gives scaffold authors explicit control over the tradeoff rather than making it a system-wide policy.

- **Hard blocks on missing security data vs. FR-003**
  - **security-reviewer claims**: When `secrets_exposed` is None (no gitleaks report), the system should either block or treat None as "unknown, which is not clean."
  - **devex-advocate claims**: FR-003 explicitly states "missing tool output MUST default variables to None, with a warning." Changing None to a blocking condition violates FR-003. The spec intentionally chose the lenient behavior. Furthermore, blocking on missing data would make the tool unusable without gitleaks installed — which is a strong constraint for developers who use different secret scanners (trufflehog, detect-secrets) or who have not yet set up secret scanning.
  - **Why this is dangerous**: The security-reviewer's recommendation directly contradicts a functional requirement. Implementing it would break FR-003 compliance.
  - **Suggested resolution**: Add a `required_tools` scaffold field that lists which tool reports must be present. If a required tool's report is missing, the scaffold produces a "configuration error" verdict (distinct from block/pass/revise) with a message indicating which tools need to be run. This respects FR-003 (values still default to None) while giving scaffolds the ability to require specific tools.

---

### Tensions

- **Synthetic "critical" severity documentation**
  - **security-reviewer's position**: The bandit parser's mapping of HIGH severity + HIGH confidence to "critical" is undocumented and confusing. Developers will see different numbers than bandit reports.
  - **devex-advocate's position**: The synthetic severity is actually a good UX decision — it surfaces the highest-risk findings more prominently. The issue is not the mapping itself but the lack of documentation. The recommendation to document the mapping is correct and aligns with the devex perspective that scoring should be predictable.
  - **Nature of tension**: Agreement on the fix (document it) but different framing. The security-reviewer sees it as a security transparency issue; the devex-advocate sees it as a predictability issue.
  - **Coordination needed**: Document the mapping in both the SecurityExtractor docstring and in scaffold documentation. Both perspectives are served by the same fix.

- **Dependency vulnerability scanning priority**
  - **security-reviewer's position**: The absence of dependency scanning (pip-audit, npm-audit, Snyk) is a HIGH severity gap because dependency vulnerabilities are the most common attack vector.
  - **devex-advocate's position**: Adding more extractors increases the number of tools developers must run to get a complete score. Each new required tool is adoption friction. The priority should be supporting the tools teams already use (Semgrep SARIF is the most impactful addition) rather than adding new tool categories that require new CI/CD pipeline steps.
  - **Nature of tension**: The security-reviewer wants broader vulnerability coverage; the devex-advocate wants lower adoption friction. Both are valid concerns operating on different timescales.
  - **Coordination needed**: Implement SARIF format support (covers Semgrep, CodeQL, many others) as a single generic extractor rather than tool-specific extractors. This maximizes coverage while minimizing the number of extractors to maintain.

---

### Safe Agreements

- **`_INVERTED_BOOLEANS` should be a module-level constant**
  - **Shared position**: The hard-coded set inside `_normalize_variable` is a maintenance hazard. Both perspectives agree it should be elevated to module scope with documentation. The security-reviewer frames this as reducing the risk of synchronization bugs between normalization and hard block paths. The devex-advocate frames this as making the scoring rules more discoverable for developers who want to understand how their scores are computed.
  - **Confidence level**: High.

- **Operator parsing is acceptable for YAML-sourced scaffolds**
  - **Shared position**: The `_evaluate_hard_block` parser's string-splitting approach is adequate when scaffolds come from trusted YAML files on disk. The security-reviewer notes it would need hardening if user-defined scaffolds are accepted via API. The devex-advocate agrees that YAML scaffolds are the primary interface and the parser is good enough for this use case.
  - **Confidence level**: High.

- **SecurityExtractor handles bandit and gitleaks output correctly**
  - **Shared position**: The parsing logic for both tools is correct. Test fixtures confirm the expected counts match. The devex-advocate agrees the parser produces accurate results; the security-reviewer confirms the security semantics are sound.
  - **Confidence level**: High.

---
