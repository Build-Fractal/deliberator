# Neutral Synthesis — Code Review Domain (Spec 029)

## Process Summary

- **Agents**: 3 -- devex-advocate, security-reviewer, spec-compliance
- **Total artifacts**: 16 (of expected 16 for a full cooperative run)
- **Phase 1 reviews**: 3
- **Phase 2 cross-reviews**: 6
- **Phase 3 revisions**: 3
- **Phase 4 disputes**: 3
- **Recommendations proposed** (Phase 1 total): 21 (devex-advocate: 7, security-reviewer: 7, spec-compliance: 7)
- **Recommendations withdrawn** (Phase 3): 1 (security-reviewer #2: hard block on None)
- **Recommendations modified** (Phase 3): 7 (devex-advocate: #1, #2, #4, #5; security-reviewer: #1; spec-compliance: FR-006, #5)
- **Recommendations surviving** (Phase 3): 13
- **New recommendations added** (Phase 3): 5
- **Disputes remaining** (Phase 4): 4
- **Convergence points** (Phase 4): 7 unanimous, 3 bilateral

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 2 Reception | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|-------------------|---------------|-------------|--------------|
| 1 | devex-advocate | None-exclusion creates false sense of security → add `missing_data_policy` scaffold field | CRITICAL | Universally endorsed on substance; spec-compliance challenged FR-003 compatibility; security-reviewer proposed configurable penalty | spec-compliance (FR-003 conflict) | Unanimous on mechanism | **Accepted-Modified** (per-scaffold policy, not blanket penalty) |
| 2 | devex-advocate | `minimum_coverage` bypasses dimension scoring → rename to `minimum_line_coverage` | HIGH | Security-reviewer defends direct check as defense-in-depth | security-reviewer (keep direct check) | Bilateral on keeping check | **Disputed** (naming convention unresolved) |
| 3 | devex-advocate | Duplicate `format_compliant` and `has_changelog_entry` → assign to single extractor | HIGH | Universally endorsed | None | Unanimous | **Accepted** |
| 4 | devex-advocate | Violation count curve too steep → variable-category-specific curves | MEDIUM | Security-reviewer agrees for lint, disagrees for security counts | security-reviewer (keep steep for security) | Bilateral | **Accepted-Modified** (category-specific curves) |
| 5 | devex-advocate | SecurityExtractor needs Semgrep/CodeQL → SARIF parser | MEDIUM | Security-reviewer adds dependency scanning | security-reviewer (add pip-audit/npm-audit) | Bilateral | **Accepted-Modified** (SARIF + dependency parsers) |
| 6 | devex-advocate | Scaffold documentation with score simulations | LOW | No challenge | None | Unanimous | **Accepted** |
| 7 | devex-advocate | SpecComplianceExtractor test mapping tooling | LOW | No challenge | None | Unanimous | **Accepted** |
| 8 | security-reviewer | Missing data must not improve scores | CRITICAL | Merged with devex-advocate #1 | spec-compliance (FR-003 conflict) | N/A | **Accepted** (merged with #1) |
| 9 | security-reviewer | Hard blocks on missing security data | CRITICAL | spec-compliance: violates FR-003 and "works without tools" | spec-compliance, devex-advocate | N/A | **Withdrawn** (replaced by `missing_data_policy`) |
| 10 | security-reviewer | Add dependency vulnerability scanning | HIGH | devex-advocate adds SARIF parser | None | Bilateral | **Accepted** (merged with #5) |
| 11 | security-reviewer | Elevate `_INVERTED_BOOLEANS` to module level | HIGH | devex-advocate agrees (discoverability); spec-compliance notes not a compliance item | None | Bilateral | **Accepted** |
| 12 | security-reviewer | Add `high_vulns > 0` hard block to healthcare/enterprise | MEDIUM | No direct challenge; spec-compliance notes scaffold content is tuning | None | Unilateral | **Disputed** (scaffold tuning vs. security requirement) |
| 13 | security-reviewer | Document synthetic "critical" severity mapping | MEDIUM | Universally endorsed | None | Unanimous | **Accepted** |
| 14 | security-reviewer | Path validation for API inputs | LOW | spec-compliance confirms API not yet built | None | Unanimous | **Accepted** (future requirement) |
| 15 | spec-compliance | Implement JSONLReviewStore (FR-010 through FR-013) | P1 | No challenge on substance; devex-advocate adds phasing context | None | Unanimous | **Accepted** |
| 16 | spec-compliance | Add missing fields to DomainRecord | P1 | No challenge | None | Unanimous | **Accepted** |
| 17 | spec-compliance | Wire `_linear_slope()` into trend analysis | P1 | No challenge | None | Unanimous | **Accepted** |
| 18 | spec-compliance | DomainScore.variables bug fix | P2→P1 | Universally endorsed as P1 bug fix | None | Unanimous | **Accepted** (elevated to P1) |
| 19 | spec-compliance | Add missing spec variables | P2 | devex-advocate: categorize as auto/heuristic/future; security-reviewer: heuristic for edge_case_coverage | devex-advocate (scope), security-reviewer (approach) | Bilateral | **Accepted-Modified** (categorized approach) |
| 20 | spec-compliance | Implement conversus gate invocation | P3 | No challenge; depends on external spec 011 | None | Unanimous | **Accepted** |
| 21 | spec-compliance | Implement FastAPI API layer | P3 | security-reviewer adds path validation requirement | None | Unanimous | **Accepted** (with security notes) |

**Deduplication note**: After removing duplicates (security-reviewer #8 merged with #1, #9 withdrawn, #10 merged with #5), there are **18 unique recommendations** from the 21 total proposals.

---

## Dangerous Contradictions Found

### Resolved Contradictions

1. **None-handling: penalty vs. FR-003 compliance** (all three agents)
   - The security-reviewer recommended penalizing missing data. The spec-compliance auditor demonstrated this violates FR-003 and the "works without tools" constraint. The devex-advocate identified the onboarding friction concern.
   - **Resolution**: All three agents converged on `missing_data_policy` as a per-scaffold field that preserves FR-003 while enabling security requirements. The security-reviewer withdrew recommendation #2 (hard block on None).

2. **FR-006 rating: PARTIALLY MET vs. MET** (spec-compliance vs. devex-advocate)
   - The spec-compliance auditor initially rated FR-006 PARTIALLY MET (dimension-level not variable-level). The devex-advocate argued dimension-level ordering is the correct UX and satisfies the spec's intent.
   - **Resolution**: Spec-compliance conceded in Phase 3 revision. FR-006 is MET.

3. **FR-015 framing: missing feature vs. bug** (all three agents)
   - The spec-compliance auditor identified `DomainScore.variables` not being populated as an FR-015 compliance gap. The devex-advocate and security-reviewer both reframed it as a one-line bug fix.
   - **Resolution**: All agree it is a P1 bug fix. FR-015 remains PARTIALLY MET until the fix lands.

### Unresolved Contradictions

1. **`minimum_coverage` naming convention** — The devex-advocate wants to rename `minimum_coverage` to `minimum_line_coverage` for naming consistency. The security-reviewer supports keeping the direct variable check but did not address the naming. No formal resolution.

2. **`high_vulns > 0` as hard block** — The security-reviewer argues healthcare/enterprise scaffolds should hard-block on HIGH severity vulnerabilities. The spec-compliance auditor frames this as scaffold tuning, not a compliance issue. No reviewer directly opposed but no explicit endorsement either.

3. **FR-003 scope: extraction layer only vs. full pipeline** — The spec-compliance auditor argues FR-003 constrains only the extraction layer (variables default to None), not the scoring layer (how None affects scores). A strict reading might extend FR-003 to the full pipeline. Unresolved.

4. **Spec variable list: normative vs. informational** — The spec-compliance auditor disputes whether the Section 2 parameter list is a requirement or a suggestion. The spec does not qualify parameters with MUST/SHOULD/MAY. Requires spec amendment.

---

## Compliance Summary (Post-Deliberation)

### Functional Requirements

| Requirement | Verdict | Notes |
|---|---|---|
| FR-001 | **MET** | Extractors parse pytest-cov XML, eslint JSON, ruff JSON, radon JSON |
| FR-002 | **MET** | Protocol-based pluggable extractors |
| FR-003 | **MET** | Missing data → None with warnings |
| FR-004 | **MET** | Weighted composite from scaffold YAML |
| FR-005 | **MET** | Hard blocks override composite → BLOCK |
| FR-006 | **MET** | Recommendations ordered by dimension impact (revised from PARTIALLY MET) |
| FR-007 | **MET** | 5 scaffolds: startup-mvp, enterprise, open-source, healthcare, api-service |
| FR-008 | **MET** | Copy-and-modify custom scaffolds supported |
| FR-009 | **MET** | Pydantic validation via Scaffold model |
| FR-010 | **NOT MET** | No ReviewStore implementation (Phase 2 scope) |
| FR-011 | **NOT MET** | No trend analysis wired (infrastructure exists) |
| FR-012 | **NOT MET** | No developer profiles (DomainRecord lacks author field) |
| FR-013 | **NOT MET** | No debt alerts |
| FR-014 | **PARTIALLY MET** | Data model supports gate; no invocation code |
| FR-015 | **PARTIALLY MET** | DomainScore.variables not populated (P1 bug) |
| FR-016 | **PARTIALLY MET** | Data model supports equilibrium; no scoring code |
| FR-017 | **NOT MET** | No API layer |
| FR-018 | **MET** | Core works standalone without API |
| FR-019 | **NOT MET** | No backend implementations |

**Summary**: 11 MET, 3 PARTIALLY MET, 5 NOT MET. The 5 NOT MET are all outer-layer features (persistence, API) that represent Phase 2 scope.

### Success Criteria

| Criterion | Verdict |
|---|---|
| SC-001 | **MET** — Good PR with healthcare scores > 0.85 (tested) |
| SC-002 | **MET** — Secrets exposed blocks all scaffolds (tested across all 5) |
| SC-003 | **NOT MET** — No persistence or trend analysis operational |
| SC-004 | **PARTIALLY MET** — Data model supports gate; no invocation |
| SC-005 | **PARTIALLY MET** — Extract + score runs in milliseconds; full pipeline untestable |

---

## Priority Action Items

### P1 — Immediate

1. **Bug fix: Add `variables=variables` to DomainScore constructor** in `CodeReviewDomain.score()` (domain.py line 448). One-line fix. Unanimous agreement.

2. **Resolve duplicate variable ownership**: Remove `format_compliant` from LintExtractor. Remove `has_changelog_entry` from DocumentationExtractor. Unanimous agreement.

3. **Elevate `_INVERTED_BOOLEANS` to module-level constant** with docstring explaining inversion semantics. Bilateral agreement.

### P2 — Next Sprint

4. **Spec amendment: Add `missing_data_policy` scaffold field** with options `exclude`, `penalize: <float>`, `require`. Per-dimension control. Unanimous agreement on mechanism.

5. **Implement JSONLReviewStore** with append-only enforcement at I/O layer. Add `author`, `pr_id`, `commit_sha`, `branch` fields to DomainRecord. Unblocks FR-010 through FR-013.

6. **Add SARIF generic extractor** for Semgrep/CodeQL/other SAST tools. Add pip-audit and npm-audit parsers for dependency scanning. Bilateral agreement.

7. **Variable-category-specific normalization curves**: Keep `1/(1+count)` for security counts. Use `1/(1+log2(1+count))` for quality counts (lint violations). Bilateral agreement.

8. **Document synthetic "critical" severity mapping** in SecurityExtractor docstring and scaffold documentation. Unanimous agreement.

### P3 — Backlog

9. **Wire `_linear_slope()` into ReviewStore trend queries**. Implement `TrendResult` production.

10. **Implement heuristic `EdgeCaseExtractor`** scanning test names for boundary/error keywords. Disputed but security-reviewer makes a strong case.

11. **Rename `minimum_coverage` to `minimum_line_coverage`** in scaffolds. Disputed but devex-advocate's naming argument is persuasive.

12. **Add `high_vulns > 0` hard block to healthcare scaffold**. Disputed but security argument is valid for regulated environments.

13. **Spec clarification**: Classify Section 2 parameters as MUST/SHOULD/MAY. Resolve FR-001 inconsistency with parameter `derived_from` fields.

14. **Implement FastAPI API layer** (FR-017, FR-019) with path validation. Depends on ReviewStore.

15. **Implement conversus gate invocation** (FR-014 through FR-016). Depends on spec 011 gate system.

16. **SpecComplianceExtractor test mapping pytest plugin**. Enables practical use of spec compliance dimension.

17. **Scaffold documentation with score simulation examples**. Helps developers choose scaffolds and predict scores.

---

## Remaining Disputes (Phase 4)

| Dispute | Agents | Core Tension | Resolution Path |
|---|---|---|---|
| `minimum_coverage` naming | devex-advocate vs. implicit status quo | UX consistency vs. defense-in-depth naming | Rename to `minimum_line_coverage` in scaffolds |
| `high_vulns > 0` hard block | security-reviewer vs. scaffold-tuning framing | Security strictness vs. scaffold author autonomy | Add to healthcare scaffold specifically |
| FR-003 scope | spec-compliance internal | Extraction-layer only vs. full-pipeline scope | Spec amendment clarifying FR-003 applies to extraction layer |
| Spec variable list normative status | spec-compliance internal | Normative (must implement all) vs. informational (can diverge) | Spec amendment with MUST/SHOULD/MAY per parameter |

---

## Referenced Files

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/029-code-review-domain/spec.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/code_review/domain.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/code_review/extractors.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/base.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_code_review.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/code_review/scaffolds/*.yml`
