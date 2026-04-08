# Cross-Review: dependency-auditor reviewing consistency-auditor

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: CSI-1 (scaffold extension mismatch) is real, but the root cause is not a dependency violation

The consistency-auditor elevates the scaffold `.json` vs `.yml` mismatch to P1, framing it as a "direct code-level contradiction" between specs 029 and 030. My audit verified that `CodeReviewDomain` imports only from `domains/base` — the override is architecturally permitted. The contradiction is not a dependency boundary violation; it is a contract mismatch within a legitimate inheritance hierarchy. This matters because the fix (search for multiple extensions) is a base class improvement, not a decoupling action. The consistency-auditor's framing as "cross-spec inconsistency" is correct, but the implication that the dependency architecture failed is misleading. The architecture correctly permits the override; the override's implementation is buggy.

### DC-2: CSI-3 (equilibrium score discontinuity) assumes an integration path that does not exist

The consistency-auditor connects spec 021's heuristic-vs-solver score discontinuity to spec 022's Kalman filter, arguing that future wiring of eq_scores will corrupt the filter. My audit confirms there is NO orchestration layer connecting these components today. The integration path (spec 022 Remediation 6) requires inter-plugin data flow, which in turn requires an orchestration mechanism that no synthesis has verified. The consistency-auditor's finding is correct in principle but describes a bug in code that does not yet exist and may require an architectural layer (my Missed Opportunity #2) that also does not exist. The actual risk is lower than P2.

### DC-3: R-10 dependency map overestimates the urgency of documentation vs. verified code

The consistency-auditor's R-10 lists 6 cross-spec dependencies as a P3 documentation task. My audit verified the actual dependency DAG against code and found it clean. The 6 dependencies in R-10 are a mix of verified code-level dependencies (e.g., spec 029 using `DomainPlugin` from spec 030) and aspirational design dependencies (e.g., spec 030 FR-015 depending on "the conversus engine gate runner injection"). Mixing verified and aspirational dependencies in a single matrix without distinguishing them would create a false sense of completeness.

---

## Tensions

### T-1: Import-level purity vs. behavioral contract analysis

My audit scope is import boundaries and architectural layering. The consistency-auditor's scope is behavioral contract consistency. The consistency-auditor found bugs (CSI-1, CSI-2) that are invisible to import analysis. This is a genuine complementarity, not a disagreement, but consumers must understand that my "all clean" verdict is scoped to import boundaries, not behavioral correctness.

### T-2: Severity of the `domains/__init__.py` docstring

I rate this P1 because inaccurate dependency claims prevent correct mental models. The consistency-auditor does not explicitly reference this finding but implicitly agrees that the architectural confusion between `domains` and `schemas`/`plugins.base` contributes to the problems they found. The tension is in prioritization: my P1 is documentation correctness; the consistency-auditor's P1s are code correctness. Both are valid.

### T-3: The optional-import convention recommendation

The consistency-auditor's R-5 recommends a shared optional-import convention document (P2). My audit verified that the `HAS_*` pattern is consistently used across specs 021, 022, and 023 but is independently implemented each time. I agree this should be formalized but note that it is a code quality improvement, not a dependency boundary fix. The pattern works correctly as-is; centralizing it reduces duplication but does not fix bugs.

---

## Safe Agreements

### SA-1: The architecture is sound at the boundary level

The consistency-auditor's findings (CSI-1 through CSI-4) are all bugs within legitimate architectural boundaries, not violations of those boundaries. My audit confirms the boundaries are clean. Both reviews agree the architecture is correct; the implementation within those boundaries has bugs.

### SA-2: The orchestration layer is a shared blind spot

Both reviews identify that the mechanism connecting plugins to the engine and domains to the gate system is unverified. The consistency-auditor tracks this in R-10; I track it in Missed Opportunity #2. Neither of us can fully validate our findings without understanding this layer.

### SA-3: Plugin isolation is genuine

The consistency-auditor confirms the optional-dependency pattern is consistent across solver specs. My audit confirms plugin-to-plugin isolation at the import level. These are complementary verifications of the same architectural property.
