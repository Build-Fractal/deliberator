# Phase 4 Disputes: consistency-auditor

**Date**: 2026-04-01

---

## Remaining Disputes

### Dispute 1: Orchestration layer audit — P1 scoping (dependency-auditor) vs. P3 documentation (my original R-10)

The dependency-auditor upgraded their orchestration layer audit from P2 to P1 in their revision, arguing it "blocks verification" of 3 spec features. I originally tracked this as P3 documentation (R-10). The test-coverage-auditor does not explicitly rank it but identifies the same gap. The implementation-verifier notes the engine has zero plugin/domain/schema imports.

**My position**: I concede the upgrade to P1 for **investigation/scoping**, not for code changes. The dependency-auditor is correct that without understanding the orchestration mechanism, specs 030 (gate lifecycle), 022 (inter-plugin data flow), and 021 (plugin hooks) cannot be sequenced. However, I maintain that the output should be a structured dependency matrix (my R-10, as amended) paired with the dependency-auditor's import-linter configuration, not a code change. The P1 is an investigation, not an implementation.

### Dispute 2: SC-001/SC-002 (spec 021) vs. scaffold YAML test — which is more CRITICAL?

The test-coverage-auditor maintains SC-001/SC-002 as the primary CRITICAL item, while accepting my argument for a second CRITICAL category (cross-spec regression tests). I still believe the scaffold YAML test has higher *architectural* impact because it affects all future domains (spec 030's core promise), while SC-001/SC-002 affect only spec 021's acceptance.

**My position**: I accept the test-coverage-auditor's two-category CRITICAL system. Both are CRITICAL for different reasons. I withdraw my claim that one outranks the other. The sequencing should be: write both categories in parallel since they target different files and test different code paths.

---

## Convergence

### Full convergence on:

1. **R-1 (scaffold `.json` fix)**: All 4 reviews agree this is P1, confirmed in code, and must land before R-3. No remaining dispute.

2. **R-2 (`DomainScore.variables` fix)**: Unanimous across all 4 reviews. The most validated finding. No dispute.

3. **R-4 (`highspy` import guard)**: Unanimous. No dispute.

4. **R-11 (write failing tests before fixes)**: The test-coverage-auditor expanded this to all 4 CSIs. The implementation-verifier adopted test-first sequencing for all 5 immediate fixes. Full convergence on the principle of test-first development for P1 bugs.

5. **R-3 sequencing (R-1 -> tests -> R-3)**: Implementation-verifier identified the dependency. All accept it. No dispute.

6. **Spec 021 is the weakest link**: All 4 reviews identify spec 021 as having the most issues (cross-spec inconsistencies, mislocated findings, untested P1s, missing acceptance tests).

7. **Specs 025/026 are the healthiest**: All 4 reviews agree.

8. **Import-level verification is necessary but insufficient**: The dependency-auditor concedes this limitation. All agree behavioral verification (implementation-verifier) and test verification (test-coverage-auditor) are needed in addition to import verification.

9. **Docstring rewrite as coupling RULE**: All accept the implementation-verifier's reframing. The dependency-auditor's revision adopts it.

10. **R-8 file attribution**: All accept that solver provenance keys belong on `PluginResult` in plugin wrappers, not on `SolverResult` in pure function modules.

---

## Final Position

My 4 cross-spec inconsistencies (CSI-1 through CSI-4) survived the deliberation intact. All are confirmed as real findings. The severity adjustments are:

- **CSI-1 (scaffold extension)**: P1 confirmed, fix sequenced before R-3
- **CSI-2 (DomainScore.variables)**: P1 confirmed, most validated finding
- **CSI-3 (eq_score discontinuity)**: Downgraded P2 -> P3 (dormant), re-evaluate at Remediation 6
- **CSI-4 (solver provenance)**: P2 maintained, file attribution corrected to plugin wrappers

My 3 missed opportunities (MO-1 through MO-3) were refined:
- **MO-1 (game form / payoff matrix)**: Narrowed by the implementation-verifier — only congestion games map to payoff matrices
- **MO-2 (mode validation)**: Maintained — `mode-mapping.yml` should annotate solver type per mode
- **MO-3 (optional import pattern for plugin discovery)**: Maintained — R-5 formalization accepted

The deliberation's most significant contribution is the adoption of test-first development (R-11) as a prerequisite for all P1 code fixes. This was the test-coverage-auditor's strongest insight, and it closes the gap between architecturally correct findings and empirically validated findings.
