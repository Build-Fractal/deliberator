# Spec Compliance Auditor — Phase 3 Revision

## Preamble

Revising based on cross-reviews from devex-advocate and security-reviewer. The devex-advocate challenged my FR-006 and FR-015 ratings and questioned whether the NOT MET verdicts for FR-010 through FR-013 give the right impression. The security-reviewer challenged my FR-015 assessment scope and my framing of FR-010 as a feature gap rather than a security property.

---

### Recommendation Dispositions

#### FR-006 Rating: Recommendations ordered by impact

- **Original position**: PARTIALLY MET. The impact calculation operates at dimension granularity, not variable granularity.
- **Disposition**: Modified to MET
- **Explanation**: The devex-advocate's cross-review makes a persuasive argument: the spec says "the change that would most improve the overall score listed first," which is ambiguous about granularity. The implementation orders dimensions by impact and provides dimension-specific advice within each recommendation. The devex-advocate correctly argues that variable-level ordering would be confusing ("improve branch_coverage before fixing high_vulns" is mathematically optimal but misleading). I concede: the current dimension-level ordering satisfies the spec's intent. **FR-006 is MET.**

#### FR-015 Rating: Gate agents receive extracted variables and scaffold

- **Original position**: PARTIALLY MET. `CodeReviewDomain.score()` does not populate `DomainScore.variables`.
- **Disposition**: Surviving as PARTIALLY MET but reclassified as a bug
- **Explanation**: Both cross-reviewers confirm this is a bug, not a design gap. The devex-advocate calls it "a one-line fix that should be immediate." The security-reviewer frames it as a security issue (scores without backing variables are unverifiable claims). I accept both framings: this is a P1 bug fix. The PARTIALLY MET verdict remains because the requirement is not fully met until the fix lands, but the recommendation is elevated from P2 to P1.

#### FR-010 through FR-013: Persistence layer NOT MET

- **Original position**: NOT MET for all four (no ReviewStore implementation).
- **Disposition**: Surviving with added context
- **Explanation**: The devex-advocate requests distinguishing "not yet implemented" from "implemented incorrectly." The security-reviewer requests noting FR-010 as a security-critical FR (append-only = immutable audit trail). Both are valid additions. **Modified assessment**: FR-010 through FR-013 remain NOT MET but with annotations: "Phase 2 implementation scope. The extraction-scoring core (Phase 1) is complete. Persistence is the next layer." FR-010 additionally notes: "Append-only semantics are a security property. When implementing, enforce at the storage I/O layer (file mode='a', INSERT-only database permissions), not just as protocol convention."

#### Recommendation 1: Implement ReviewStore with JSONLReviewStore

- **Original position**: P1.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged the substance. The security-reviewer adds the append-only enforcement guidance, which I incorporate.

#### Recommendation 2: Add missing fields to DomainRecord

- **Original position**: P1.
- **Disposition**: Surviving
- **Explanation**: The `DomainRecord` model lacks `author`, `pr_id`, `commit_sha`, `branch`, `files_changed`, `lines_added`, `lines_removed` from the spec's `ReviewRecord`. No cross-review challenged this. Required for FR-012 (developer profiles).

#### Recommendation 3: Wire `_linear_slope()` into trend analysis

- **Original position**: P1.
- **Disposition**: Surviving
- **Explanation**: Required for FR-011 and SC-003. No cross-review challenged this.

#### Recommendation 4: Populate `DomainScore.variables` in CodeReviewDomain.score()

- **Original position**: P2.
- **Disposition**: Elevated to P1
- **Explanation**: All three reviews converge on this being a bug, not a feature gap. The security-reviewer frames the missing variables as breaking the audit trail. The devex-advocate frames it as a one-line fix. Both framings support P1 priority. The fix is adding `variables=variables` to the DomainScore constructor call at domain.py line 448.

#### Recommendation 5: Add missing spec variables to extractors

- **Original position**: P2.
- **Disposition**: Modified
- **Explanation**: The devex-advocate argues that some spec variables (`edge_case_coverage`, `coupling_score`) have no standard tool output and would produce permanent None values. The security-reviewer argues `edge_case_coverage` could be approximated by analyzing test names. I accept both points. **Modified recommendation**: Categorize spec variables as "auto-extractable" (have standard tools) and "heuristic/future" (require custom analysis). Implement extractors only for auto-extractable variables. For `edge_case_coverage`, accept the security-reviewer's heuristic approach as a P3 enhancement. For `duplication_rate`, implement a jscpd JSON parser. For `coupling_score` and `test_to_code_ratio`, defer as future/manual.

#### Recommendation 6: Implement conversus gate invocation

- **Original position**: P3.
- **Disposition**: Surviving
- **Explanation**: Depends on external spec (011 gate system). No cross-review challenged the priority.

#### Recommendation 7: Implement FastAPI API layer

- **Original position**: P3.
- **Disposition**: Surviving with security note
- **Explanation**: The security-reviewer adds path validation as a requirement for the API. When implementing, validate all file paths against a configured workspace root.

---

### New Recommendations from Cross-Review

#### New Recommendation 8: Spec amendment for `missing_data_policy`

- **Position**: P2
- **Source**: Three-way convergence across all reviews
- **Explanation**: FR-003's None-default behavior creates a tension with security requirements. All three reviews agree the resolution is a per-scaffold `missing_data_policy` field. This requires a spec amendment because it modifies the plugin's behavior contract. File as spec 029 amendment.

#### New Recommendation 9: Resolve spec inconsistency in FR-001 vs. parameter `derived_from`

- **Position**: P3
- **Source**: Security-reviewer and spec-compliance cross-review
- **Explanation**: FR-001 lists specific tool formats (pytest-cov XML, eslint JSON, ruff JSON, radon JSON) but parameter definitions reference "dependency scan" and "secret scanner" as derived_from sources without corresponding FR-001 format entries. Either add these formats to FR-001 or clarify that `derived_from` is informational, not normative.

---
