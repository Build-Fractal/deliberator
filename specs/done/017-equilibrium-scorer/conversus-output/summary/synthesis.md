# Phase 5 Synthesis: Spec 017 — Equilibrium Scorer

**Spec**: 017-equilibrium-scorer
**Date**: 2026-03-24
**Agents**: game-theorist, plugin-engineer, spec-compliance

---

## Overall Assessment

The Equilibrium Scorer plugin is a well-structured, robust implementation that correctly models per-mode payoff functions and computes equilibrium quality scores. The Plugin ABC conformance is complete, error handling is thorough, and the output format is largely compliant. Three issues were identified: one critical (nashopt integration gap), one moderate (hook field value), and one disputed (filename format).

---

## Consensus Findings

### 1. FR-005 NOT MET — nashopt.check_equilibrium() never called (Critical)

**Unanimous**. The code imports `nashopt` to check availability and uses the result to set the `solver` field in output data, but never delegates computation to `nashopt.check_equilibrium()`. The heuristic payoff functions are always used. The `solver: "nashopt"` output is misleading when nashopt is installed but not used.

**Recommendation**: Either (a) implement actual nashopt delegation when the package is available, or (b) always report `solver: "heuristic"` and document nashopt integration as a future enhancement. Option (b) is simpler and more honest.

### 2. FR-007 PARTIALLY MET — hook field value incorrect (Medium)

**Unanimous**. `PluginResult.data["hook"]` is set to `"equilibrium-scorer"` (the plugin name) instead of the actual hook point (e.g., `"post_phase_5"`). The persisted JSON file from `execute_hooks()` contains the correct hook, but in-memory consumers see the wrong value.

**Recommendation**: Either pass the hook point as a parameter to `execute()` (requires ABC change) or document that the JSON output file is the authoritative source for hook identification.

### 3. Payoff Functions Mathematically Sound (Consensus)

All four mode payoffs (cooperative, WTA, PD, red-blue) are mathematically reasonable heuristics. game-theorist validated each formula against the spec's Section 2 definitions. The heuristic best-response estimates are upper bounds that produce correct equilibrium/non-equilibrium classifications for the test cases.

### 4. Error Handling Robust (Consensus)

FR-012 and FR-013 are fully MET. The two-tier feature extraction fallback (full extraction -> state-based), per-agent exception handling, and top-level computation failure catch provide defense-in-depth. No crash paths exist.

### 5. Plugin ABC Conformance Complete (Consensus)

Full conformance with the Plugin abstract base class. Correct `name`, `hooks`, `execute()` signature, and constructor behavior.

### 6. Red-Blue total_surface=0 Edge Case (Consensus)

When no attacks exist (`total_surface == 0`), red gets `payoff = severity_sum` while blue gets `payoff = 0.0`. This asymmetry is mathematically questionable. Both should return 0.0 when there is no attack surface.

### 7. WTA Magic Threshold (Consensus)

The hardcoded 2.0 score differential threshold in `winner_take_all_payoff` is undocumented and not configurable. Should be a named constant at minimum, ideally a config parameter.

### 8. Cooperative Docstring/Code Mismatch (Consensus)

The docstring claims concession_rate is factored as a cost, but the code only uses `surviving_count`. Documentation bug.

---

<!-- DISPUTES_BEGIN -->

## Unresolved Disputes

### Dispute: FR-008 Compliance Level

**game-theorist**: MET. The requirement says "MUST include the round number" -- it does. The example filename is illustrative. The base infrastructure's pattern is actually better.

**plugin-engineer**: PARTIALLY MET. The spec uses MUST with a specific format string, which is normative per RFC 2119. The code deviates from the stated format.

**spec-compliance**: PARTIALLY MET. Aligns with plugin-engineer. MUST + specific format = absolute requirement.

**Vote**: 2-1 for PARTIALLY MET.

**Synthesis ruling**: PARTIALLY MET. The intent (round-specific files) is satisfied, but the exact format deviates. **Recommended action**: Update spec 017 FR-008 to align with the base plugin infrastructure's naming convention `{plugin-name}-{hook}-round-{N}.json`, then mark as MET.

<!-- DISPUTES_END -->

---

## Compliance Summary

| Requirement | Status | Notes |
|-------------|--------|-------|
| FR-001 | MET | |
| FR-002 | MET | |
| FR-003 | MET | |
| FR-004 | MET | |
| FR-005 | **NOT MET** | nashopt never called |
| FR-006 | MET | |
| FR-007 | PARTIALLY MET | hook field value wrong |
| FR-008 | PARTIALLY MET (disputed) | Filename format deviation |
| FR-009 | MET | |
| FR-010 | MET | |
| FR-011 | MET | |
| FR-012 | MET | |
| FR-013 | MET | |
| SC-001 | MET | |
| SC-002 | MET | |
| SC-003 | MET | |
| SC-004 | NOT VERIFIED | No packaging config |
| SC-005 | MET | |

**MET**: 11/13 FR, 3/5 SC verified
**PARTIALLY MET**: 2 FR
**NOT MET**: 1 FR
**NOT VERIFIED**: 1 SC

---

## Recommended Actions

1. Fix FR-005: Either integrate nashopt.check_equilibrium() or always report solver as "heuristic".
2. Fix FR-007: Resolve hook field value in PluginResult.data.
3. Update spec FR-008: Align filename pattern with base infrastructure convention.
4. Fix Red-Blue edge case: Return (0.0, 0.0) when total_surface == 0.
5. Make WTA threshold configurable or document the 2.0 value.
6. Fix cooperative payoff docstring to remove concession_rate mention.
