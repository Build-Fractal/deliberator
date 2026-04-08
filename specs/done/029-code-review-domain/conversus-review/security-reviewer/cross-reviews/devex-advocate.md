# Cross-Review: security-reviewer reviews devex-advocate

## Context

The security-reviewer evaluates the devex-advocate's Phase 1 review, focusing on whether developer experience recommendations introduce security risks or correctly identify security-relevant issues.

---

### Dangerous Contradictions

- **None-exclusion framing: "false sense of security" vs. "fundamental design flaw"**
  - **devex-advocate claims**: The None-exclusion logic in `_score_dimension` means a project with no security scanning scores higher than one that scans and finds issues. The devex-advocate labels this as the #1 critical recommendation: "the easiest way to get a high security score is to not run a security scanner."
  - **security-reviewer claims**: The same issue is identified in my review as gaming vector #1 (selective report omission) and recommendation #1 (missing data must not improve scores). However, my framing goes further: the issue is not just about incentives but about the security model's integrity. The devex-advocate frames it as an incentive problem; I frame it as a safety bypass. The devex-advocate suggests defaulting missing dimensions to 0.5; I suggest a configurable penalty with a default of 0.5 and the option for healthcare scaffolds to set it to 0.0 (block).
  - **Why this is dangerous**: Both reviews independently identify the same critical issue — which strongly validates its priority. But the devex-advocate's fixed 0.5 penalty is insufficient for regulated environments where missing security data should be treated as a hard block. A healthcare scaffold that tolerates missing security data (scoring 0.5 instead of blocking) fails the regulatory intent.
  - **Suggested resolution**: Adopt the security-reviewer's configurable penalty approach. The per-scaffold `missing_data_penalty` field satisfies both perspectives: startup-mvp can use 0.5 (lenient), healthcare can use 0.0 (hard block on missing data). The devex-advocate's concern about onboarding friction is addressed by making the penalty scaffold-specific rather than global.

- **`minimum_coverage` threshold bypass: bug vs. feature**
  - **devex-advocate claims**: The `minimum_coverage` threshold checks `variables.get("line_coverage")` directly rather than going through the dimension scoring system. The devex-advocate calls this "a bug" and an "inconsistency."
  - **security-reviewer claims**: While not explicitly addressed in my review, this direct-variable check is actually a defense-in-depth pattern from a security perspective. The dimension scoring system averages `line_coverage` and `branch_coverage`, which can mask low line coverage. A direct variable check ensures that `line_coverage` itself meets the threshold regardless of how branch coverage compensates. However, the inconsistency is real: `minimum_security` checks the dimension score (which averages 4 variables), while `minimum_coverage` checks a single variable. The healthcare scaffold could have `minimum_security: 0.95` but a project with 0 critical vulns, 0 high vulns, 0 medium vulns, and `secrets_exposed = True` would have security dimension score of average(1.0, 1.0, 1.0, 0.0) = 0.75, which fails the 0.95 threshold. So the dimension-level check does catch this.
  - **Why this is dangerous**: If the devex-advocate's recommendation to "route all threshold checks through the dimension system" is implemented without security analysis, the direct `line_coverage` check is removed, and a project could pass the coverage threshold with high branch_coverage compensating for low line_coverage. The dimension average could be above threshold while line_coverage is below the intended minimum.
  - **Suggested resolution**: Keep the direct variable check as intentional but document it. Add similar direct-variable checks for other thresholds where dimension averaging could mask individual variable deficiencies (e.g., `minimum_secrets: false` alongside `minimum_security`).

---

### Tensions

- **SecurityExtractor missing tool support: practical vs. threat-model driven**
  - **devex-advocate's position**: The missing support for Semgrep, CodeQL, and Snyk is a gap. Recommends adding SARIF support as a generic parser.
  - **security-reviewer's position**: The missing dependency scanning (pip-audit, npm-audit, trivy) is the more critical gap because dependency vulnerabilities are the primary attack vector. SARIF support helps but does not cover dependency scanning tools that use their own formats.
  - **Nature of tension**: Both agree tools are missing. The devex-advocate optimizes for coverage breadth with minimal implementation effort (SARIF parser covers many tools). The security-reviewer optimizes for covering the highest-risk gap first (dependency scanning).
  - **Coordination needed**: Implement both: (1) SARIF generic parser for code-level SAST tools, and (2) specific parsers for pip-audit and npm-audit JSON for dependency scanning. The SARIF parser is a medium-effort generic solution; the dependency parsers are low-effort specific solutions.

- **Violation count normalization curve**
  - **devex-advocate's position**: The `1 / (1 + count)` curve is too steep, making the score effectively binary. Recommends a log-based alternative.
  - **security-reviewer's position**: From a security perspective, the steep curve for `critical_vulns` and `high_vulns` is correct. One HIGH vulnerability should dramatically reduce the security score. The curve being "effectively binary" for security counts is a feature, not a bug. However, for `lint_violation_count`, the steep curve is inappropriate — 5 lint violations should not score the same as 50.
  - **Nature of tension**: The devex-advocate wants a uniform curve change; the security-reviewer wants variable-specific curves. Security counts should remain steep; quality counts should be gentler.
  - **Coordination needed**: Use different normalization curves per variable category. Security counts keep `1 / (1 + count)`. Lint/quality counts use `1 / (1 + log2(1 + count))` or similar. This satisfies both perspectives.

---

### Safe Agreements

- **Duplicate variable production across extractors is a real problem**
  - **Shared position**: Both `format_compliant` and `has_changelog_entry` are produced by multiple extractors. The last-writer-wins semantics create non-obvious behavior. The security-reviewer notes this as a reliability concern (the "correct" value depends on extractor ordering); the devex-advocate notes it as a predictability concern (developers cannot determine which extractor's value wins).
  - **Confidence level**: High. The fix is straightforward: assign each variable to exactly one extractor.

- **Healthcare scaffold minimum_spec_compliance interaction is non-obvious**
  - **Shared position**: The devex-advocate's observation that the 0.9 spec_compliance threshold operates on the dimension average (which includes `fr_satisfaction_rate`, `sc_pass_rate`, and `has_spec`) is correct. A developer could have FR satisfaction at 0.95 but SC pass rate at 0.80, averaging to ~0.917 if `has_spec = True`, which barely passes. But if `has_spec = False`, the dimension is strongly affected. The security-reviewer agrees this interaction should be documented but notes it is not a security concern — it is a UX concern.
  - **Confidence level**: High.

- **SpecComplianceExtractor requires manual test mapping**
  - **Shared position**: Both reviews note that the test mapping JSON file is a manual step with no tooling. The devex-advocate recommends a pytest plugin; the security-reviewer has no objection as this is a UX issue, not a security concern. The agreement is that the extractor is functionally correct but practically difficult to use.
  - **Confidence level**: High.

---
