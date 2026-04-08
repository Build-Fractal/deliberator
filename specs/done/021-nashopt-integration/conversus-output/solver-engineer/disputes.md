# Phase 4 Disputes: solver-engineer

**Agent**: solver-engineer
**Spec**: 021-nashopt-integration
**Date**: 2026-04-01
**Phase**: 4 (Post-revision disputes)

---

## Remaining Disputes

### Dispute 1: Timeout implementation -- solver.py internal vs. scorer.py wrapper

**Disputed with**: None (consensus reached)

All three agents agree that the timeout should be implemented inside `check_equilibrium_nashopt()` as a `timeout_seconds` parameter with `concurrent.futures.ThreadPoolExecutor`. solver-engineer accepted plugin-engineer's argument. spec-compliance upgraded FR-007 to PARTIALLY MET based on existing test evidence.

**Status**: RESOLVED. No remaining dispute.

---

### Dispute 2: Distance normalization -- clamp vs. normalize

**Disputed with**: None (consensus reached)

All three agents agree that the spec should be amended to say "clamped to [0.0, 1.0]" rather than "normalized by maximum possible distance." The current implementation is correct under the amended spec.

**Status**: RESOLVED. Spec amendment recommended.

---

## Withdrawn Disputes

### Red-blue aggregation

solver-engineer withdrew the P2-2 recommendation after plugin-engineer and spec-compliance demonstrated that aggregation matches the spec's "red_agents_combined" design.

---

## No Active Disputes

All disagreements were resolved during Phase 2 (cross-review) and Phase 3 (revision). The three agents converge on:
1. Timeout belongs in solver.py.
2. Spec should say "clamped" not "normalized."
3. scorer.py must be included in future review artifacts.
4. WTA matrix shape compatibility must be verified.
