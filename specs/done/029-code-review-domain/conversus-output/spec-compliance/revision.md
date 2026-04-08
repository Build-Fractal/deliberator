# Phase 3 Revision: spec-compliance

**Spec**: 029-code-review-domain

---

## Position Changes After Cross-Review

### Modified: FR-013 -- RECLASSIFIED from PARTIAL to NOT IMPLEMENTED

The security-reviewer's argument is correct. The spec requires "configured threshold" for technical debt alerts. The current implementation only has a hardcoded declining-trend detection (slope < -0.01). No per-dimension threshold configuration exists, and no alerting mechanism fires on threshold crossing. This is NOT IMPLEMENTED.

### Modified: FR-019 -- RECLASSIFIED from PARTIAL to DEFERRED

The devex-advocate correctly distinguishes between "partially implemented" and "not yet implemented with clean architecture for addition." The JSONL and SQLite backends demonstrate the store protocol. A Supabase backend can be added without code changes to existing modules. This is DEFERRED, not PARTIAL.

### New: format_compliant semantic ambiguity (Medium)

Cross-review consensus: `format_compliant` is set by two extractors with different semantics. The security-reviewer and devex-advocate both flag this. Needs variable renaming.

### Surviving: FR-012 (author aggregation) PARTIAL

The DomainRecord does not include an author field. The store's aggregate method does not support grouping by author. Developer profile functionality is missing.

### Surviving: FR-014 through FR-016 NOT IMPLEMENTED (gate integration)

No change. Gate integration depends on the conversus engine's gate mechanism, which is a separate work stream.
