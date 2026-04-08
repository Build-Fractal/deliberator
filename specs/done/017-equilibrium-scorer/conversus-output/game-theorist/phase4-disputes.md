# Phase 4 Disputes: game-theorist

**Spec**: 017-equilibrium-scorer
**Reviewer**: game-theorist
**Date**: 2026-03-24
**Phase**: 4 (Dispute Declaration)

---

## Active Disputes

### Dispute 1: FR-008 Compliance Level

**My position**: MET (intent satisfied -- round number is included)
**Opposing position**: PARTIALLY MET (spec-compliance, plugin-engineer -- exact filename format differs)

**Argument**: The spec says "the output filename MUST include the round number: `equilibrium-score-round-{N}.json`." The colon followed by a specific example reads as illustrative, not normative. The requirement sentence is "the output filename MUST include the round number" -- which IS satisfied. The example filename is one way to satisfy it. The base infrastructure's pattern `{name}-{hook}-round-{N}.json` is actually superior because it supports multiple plugins at the same hook without collision. Enforcing the spec's literal filename would require the scorer to bypass `execute_hooks()` and write its own file, breaking the plugin infrastructure's consistency guarantee.

**Proposed resolution**: Update the spec to align with the base infrastructure pattern. Mark FR-008 as MET in the review.

---

## Resolved Disagreements

All other issues reached consensus across the three reviewers:

1. **FR-005 NOT MET**: Unanimous. nashopt is imported but never called.
2. **FR-007 PARTIALLY MET**: Unanimous. hook field value is wrong in PluginResult.data.
3. **Red-Blue edge case**: All agree this is a correctness concern (not compliance).
4. **WTA magic threshold**: All agree this should be configurable.

---

## Concessions

I concede to plugin-engineer on the Red-Blue `total_surface=0` edge case. My original review assessed Red-Blue payoffs as "sound." After plugin-engineer's observation about the asymmetric fallback (red gets severity_sum, blue gets 0.0), I acknowledge this is a mathematical concern. Both should return 0.0 when there is no attack surface.
