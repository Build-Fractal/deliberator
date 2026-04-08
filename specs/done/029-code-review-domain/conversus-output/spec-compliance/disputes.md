# Phase 4 Disputes: spec-compliance

**Spec**: 029-code-review-domain

---

## Surviving Disputes

### DISPUTE 1: format_compliant variable collision (Medium)

**Status**: Surviving -- all three agents.

LintExtractor and ConventionExtractor both set `format_compliant` with different meanings. Needs renaming.

### DISPUTE 2: FR-012 developer profiles missing (Medium)

**Status**: Surviving -- devex-advocate and spec-compliance.

No author field in DomainRecord. No author-based aggregation in store.

### DISPUTE 3: FR-013 technical debt alerting NOT IMPLEMENTED (Medium)

**Status**: Surviving -- security-reviewer and spec-compliance.

Configured per-dimension alert thresholds are required but not implemented. Current alert is a hardcoded declining-trend binary.

### DISPUTE 4: FR-014 through FR-016 gate integration NOT IMPLEMENTED (High)

**Status**: Surviving -- all agents acknowledge.

The conversus gate integration is the differentiating feature of this domain plugin. Without it, the plugin is a standalone scorer without the multi-agent deliberation that the spec envisions. This is the highest-priority gap.

### DISPUTE 5: FR-019 Supabase backend DEFERRED (Low)

**Status**: Surviving -- architecture supports it, implementation pending.

## Withdrawn Disputes

- FR-013 reclassified from PARTIAL to NOT IMPLEMENTED (consensus)
- FR-019 reclassified from PARTIAL to DEFERRED (consensus)
