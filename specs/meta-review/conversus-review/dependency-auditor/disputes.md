# Phase 4 Disputes: dependency-auditor

**Date**: 2026-04-01

---

## Remaining Disputes

### Dispute 1: Docstring fix priority — P1 or P2?

The test-coverage-auditor's cross-review rates the `domains/__init__.py` docstring fix as P2 because "docstring inaccuracy does not cause test failures." The consistency-auditor originally did not rate it but now endorses rewriting it as a coupling RULE (their R-12). The implementation-verifier supports the RULE reframing.

**My position**: I maintain P1 for the rewritten docstring. The test-coverage-auditor's argument that docstrings do not cause test failures is true but misses the point: the docstring is the only documentation of the coupling rules for the domains package. An incorrect coupling rule has the same practical impact as no coupling rule — future contributors may introduce `plugins.base` imports into domains because the docstring says they can. The reframe from CLAIM to RULE makes this even more important: a wrong RULE actively invites violations.

**Concession path**: If the import-linter configuration (my P3-4, now recommending automated enforcement) lands, then the docstring becomes less critical because violations are caught automatically. In that case, I would accept P2. But until import-linter is configured, the docstring is the only coupling enforcement mechanism, and it must be correct.

### Dispute 2: Orchestration layer audit scope

The consistency-auditor concedes the upgrade to P1 for investigation but insists the output should be a dependency matrix + import-linter config, not code changes. The implementation-verifier's revision does not directly address the orchestration layer. The test-coverage-auditor's revision focuses on tests for existing code, not the orchestration gap.

**My position**: I agree with the consistency-auditor that the P1 is an investigation, not an implementation. However, the investigation scope should be broader than a dependency matrix. It should produce: (a) identification of the orchestration entry point(s), (b) a sequence diagram showing how plugins are loaded and invoked, (c) a determination of whether the dependency injection pattern proposed in spec 030 Dispute 1 is feasible, and (d) identification of what changes are needed to support inter-plugin data flow (spec 022 Remediation 6). The dependency matrix is one output; the architectural feasibility assessment is the more important output.

---

## Convergence

### Full convergence on:

1. **The dependency DAG is correct**: No reviewer found import boundary violations. The DAG is the authoritative representation of the codebase's structural health.

2. **Import-level verification is necessary but insufficient**: All 4 reviews now explicitly agree on this. The dependency-auditor's scope (imports) is complemented by the consistency-auditor (behavioral contracts), implementation-verifier (code-to-claim accuracy), and test-coverage-auditor (code-to-test alignment).

3. **The `domains/__init__.py` docstring should be rewritten as a coupling RULE**: All 4 reviews accept the implementation-verifier's reframing. The only remaining dispute is priority (P1 vs. P2), not content.

4. **Plugin-to-plugin isolation is the strongest architectural property**: All 4 reviews confirm this from their respective angles.

5. **schemas/ is a true leaf package**: Unanimously confirmed.

6. **VariableExtractor protocol conformance should be tested**: The implementation-verifier reframed this as an interface test. The test-coverage-auditor confirmed no test exists. The consistency-auditor did not object. I accept the reframing.

7. **The `@runtime_checkable` amendment**: My new recommendation to add `@runtime_checkable` to the VariableExtractor protocol was not explicitly addressed by other revisions, but it is consistent with all positions (enables testing without changing the structural typing design).

8. **1 of 6 cross-spec dependencies is verified in code**: The dependency matrix I produced in my revision shows that 5 of 6 cross-spec dependencies identified by the consistency-auditor are aspirational. All reviews agree this characterization is correct.

---

## Final Position

My central finding — that the dependency architecture is clean — is confirmed and unchallenged. The deliberation produced three important qualifications:

1. **Clean imports do not guarantee behavioral correctness**: The consistency-auditor's CSI-1 and CSI-2 are bugs within clean dependency boundaries. My audit correctly verified the boundaries but cannot detect these bugs. I accept this limitation.

2. **The docstring fix is more than documentation**: Rewriting it as a coupling RULE (not just correcting a factual error) has architectural significance. The priority depends on whether automated enforcement (import-linter) is available.

3. **The orchestration layer gap is the single largest shared blind spot**: All 4 reviews identify it from different angles. The investigation is P1 for scoping; the code changes will follow once the architecture is understood.

My confidence in the DAG is 100%. My confidence that the DAG is *sufficient* for dependency health dropped from implicit certainty to explicit acknowledgment that behavioral and test verification are also required.
