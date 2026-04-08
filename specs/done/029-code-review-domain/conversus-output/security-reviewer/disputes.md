# Phase 4 Disputes: security-reviewer

**Spec**: 029-code-review-domain

---

## Surviving Disputes

### DISPUTE 1: format_compliant semantic ambiguity (Medium)

**Status**: Surviving -- cross-review consensus.

Two extractors set the same variable with different meanings. Needs disambiguation.

### DISPUTE 2: FR-013 technical debt alerting NOT IMPLEMENTED (Medium)

**Status**: Surviving -- security-reviewer and spec-compliance agree.

The spec requires configured per-dimension thresholds for debt alerts. The current implementation only has a binary declining-trend detection with a hardcoded slope threshold.

**Recommended resolution**: Add an `alert_thresholds` field to Scaffold (dict mapping dimension names to minimum acceptable trend slopes). Modify store.trend() to compare slope against the threshold and set TrendResult.alert accordingly.

### DISPUTE 3: Supabase backend DEFERRED

**Status**: Surviving -- acknowledged by all agents.

FR-019 requires Supabase backend support. The architecture supports it cleanly but the backend is not yet implemented.

## Withdrawn Disputes

- LOW severity findings: Downgraded to Info per devex-advocate reasoning
- XXE in _safe_read_xml: Info observation, mitigated by local-file constraint
