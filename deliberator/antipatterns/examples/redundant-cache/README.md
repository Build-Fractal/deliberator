# Antipattern Example: Redundant Cache

**Antipattern**: Convention Over Content
**Observed**: 2026-03-20, during spec 005-p2p3-backlog-hardening Phase 2-3 gate deliberations

## Summary

Agents created a manually-maintained status tracking artifact (STATUS.md taxonomy with custom labels) that duplicated information already tracked by speckit's task-checkbox convention. This spawned two additional specs (007, 008) just to maintain the cache, consuming multiple deliberation cycles on housekeeping instead of substantive work.

## Symptoms

1. Agents proposed new vocabulary ("Implementation-complete," "Feature-complete," "Not assessed") for states already expressible by counting task checkboxes
2. Deliberation cycles spent debating label names, transition criteria, and compound formats — all for a derived summary
3. Gate reviews discovered "drift" between STATUS.md and actual state, generating fix-it specs
4. Each fix-it spec triggered its own deliberation, compounding the overhead

## Root Cause

Agents were not instructed to check whether speckit already tracked the information they were documenting. The self-audit (spec 005) identified "no single status document" as a gap, but the actual gap was agent awareness of speckit conventions — not a missing artifact. Agents defaulted to creating a new document rather than deriving status from existing task checkboxes.

## Correction

Tell agents to derive status from speckit artifacts:
- **Implementation state** → count `[x]` vs `[ ]` in tasks.md
- **Acceptance state** → check spec.md acceptance scenarios against tasks.md completion
- **Gaps** → unchecked tasks with FR references
- **Dependencies** → declared in each spec.md

Do not create summary documents that cache computable information.

## When This Does NOT Apply

- When the information is genuinely not derivable (e.g., subjective risk assessments, effort estimates requiring human judgment)
- When a cross-cutting view is needed that no single artifact provides AND cannot be computed by reading multiple artifacts
- When external stakeholders need a format different from speckit's internal structure

## Artifacts

```
examples/redundant-cache/
├── README.md                              # This file
├── STATUS.md                              # The redundant cache artifact
├── specs/
│   ├── 007-status-taxonomy-updates/       # Fix-it spec #1 (Phase 2 gate)
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── checklists/
│   └── 008-status-enrichment-hardening/   # Fix-it spec #2 (Phase 3 gate)
│       ├── spec.md
│       └── checklists/
└── deliberations/
    ├── phase-2-gate-summary.md            # Deliberation that identified taxonomy gaps
    └── phase-3-gate-summary.md            # Deliberation that identified more drift
```

## Keywords

tracking, cache, artifact-creation, status, taxonomy, deliberation-drift, convention-over-content, speckit-duplication
