# Phase 3 Revision: dependency-auditor

**Date**: 2026-04-01

---

## Cross-Reviews Received From

- **consistency-auditor**: 3 DCs, 4 Ts, 3 SAs
- **implementation-verifier**: 3 DCs, 4 Ts, 3 SAs
- **test-coverage-auditor**: 3 DCs, 3 Ts, 3 SAs

---

## Recommendation Dispositions

### P1-1: Fix `domains/__init__.py` docstring
**Status**: MAINTAINED WITH AMENDMENT — The consistency-auditor (DC-2) agrees the docstring matters but frames the issue as an unresolved architectural decision, not just documentation. The implementation-verifier (DC-2) argues the docstring should be rewritten as a coupling RULE, not a dependency CLAIM. I accept this reframing. **Amended**: rewrite the docstring to follow the `code_review/__init__.py` pattern: "Domain plugins MUST NOT import from engine/, linter/, web/, mcp_server. They MAY import from domains/base, pydantic, stdlib." This is more durable than claiming specific current imports.

### P2-2: Audit the orchestration layer
**Status**: MAINTAINED — all three reviewers confirm this gap. The consistency-auditor identifies 6 cross-spec dependencies requiring orchestration (R-10). The implementation-verifier confirms the engine has zero imports from plugins/domains/schemas. The test-coverage-auditor confirms zero cross-spec integration tests. The convergence is strong: the orchestration layer is a shared blind spot across all four reviews.

**Adjustment**: Upgrade from P2 to P1 for scoping/investigation. While no code fix is needed immediately, the gap blocks verification of spec 030's gate lifecycle (Dispute 1), spec 022's inter-plugin data flow (Remediation 6), and spec 021's plugin hook execution. Without understanding the orchestration mechanism, these cannot be sequenced.

### P2-3: Verify VariableExtractor protocol conformance at test time
**Status**: MAINTAINED — the consistency-auditor does not directly address this. The implementation-verifier (DC-3) reframes this as "interface verification, not dependency verification" — I accept this reframing. The test-coverage-auditor (DC-2) confirms no test exists. **Amended**: the recommendation is now framed as an interface contract test, not a dependency audit item. The test should live in `test_code_review.py` (closer to the implementation) and use `@runtime_checkable Protocol` with `isinstance`.

### P3-4: Map the full dependency DAG with import-linter
**Status**: MAINTAINED — the test-coverage-auditor (T-1) argues tests should be prioritized over documentation. I accept that automated enforcement (via import-linter) is more valuable than a static diagram. **Amended**: the recommendation now specifies import-linter configuration as the deliverable, not a diagram. This provides automated enforcement that catches future violations.

### P3-5: Reconcile `code_review/domain.py` MAY-import-schemas permission with reality
**Status**: DOWNGRADED TO INFORMATIONAL — the consistency-auditor (T-1) notes this permission reflects an unresolved architectural decision. The implementation-verifier (T-1) suggests the docstring fix (my P1-1) should make this explicit. Since the amended P1-1 now uses a "MUST NOT / MAY" pattern, the schemas permission is handled there. This item is subsumed by the amended P1-1.

---

## New Recommendations

### P1-NEW: Distinguish verified vs. aspirational dependencies in cross-spec tracking

Accept the consistency-auditor's R-10 cross-spec dependency map, with the implementation-verifier's amendment to distinguish verified (code-level) from aspirational (synthesis-described) dependencies, and the test-coverage-auditor's amendment to pair each dependency with an integration test status. This should be a structured artifact, not prose.

The 6 dependencies identified by the consistency-auditor, classified:

| Dependency | Type | Status | Integration Test |
|---|---|---|---|
| Spec 026 SC-005 -> spec 023 AMPL solvability | Aspirational | Not implemented | None |
| Spec 026 FR-004 -> spec 014 classifier routing | Aspirational | Not implemented | None |
| Spec 029 FR-014/FR-016 -> spec 011 gate system | Aspirational | Not implemented | None |
| Spec 029 SC-004 -> spec 030 domain plugin base | **Verified** | Working | `pytest.skip` guard |
| Spec 022 Rem-6 -> spec 021 eq_score source | Aspirational | Not implemented (eq_score=0.0) | None |
| Spec 030 FR-015 -> conversus engine gate runner | Aspirational | Not implemented | None |

Only 1 of 6 is verified in code. This confirms that the cross-spec surface is largely aspirational.

### P2-NEW: Add `@runtime_checkable` to VariableExtractor protocol

The current Protocol in `domains/base.py` uses structural typing. Making it `@runtime_checkable` enables `isinstance` checks in tests without requiring extractors to import the protocol. This is a one-line change to `domains/base.py` that enables the interface contract tests recommended in P2-3.

---

## Position Summary

The cross-reviews confirmed my central finding: **the dependency architecture is clean at the import level**. No reviewer challenged the verified DAG or found boundary violations I missed. The disagreements were productive:

1. **Scope expansion**: The consistency-auditor's DC-1 correctly identifies that import-level cleanliness does not prevent behavioral contract bugs. I accept this limitation of my audit scope. Import boundaries are necessary but not sufficient for dependency health.

2. **Framing adjustment**: The implementation-verifier's DC-2 reframes my docstring fix as a coupling RULE rather than a dependency CLAIM. This is a better design that I adopt.

3. **Testing gap**: The test-coverage-auditor's DC-1 correctly identifies that my "verified" claims rest on untested code. My import-level verification confirms the code is correctly structured; it does not confirm the code works. Both are needed.

My confidence in the DAG itself is unchanged (no reviewer found a violation). My confidence in the behavioral health of the codebase is lower after seeing the test-coverage-auditor's data. The amended recommendations reflect this: the docstring fix is reframed, the orchestration audit is upgraded, and the protocol conformance test is reframed as an interface test.
