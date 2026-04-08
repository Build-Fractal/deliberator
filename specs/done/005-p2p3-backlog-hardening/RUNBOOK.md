# Runbook: 005-p2p3-backlog-hardening

Manual execution sequence. Implement all tasks in a phase, then run the phase-level consensus gate to validate before proceeding.

## Phase 1: Verification (T001-T005)

Phase 1 tasks are read-only verification — confirm pre-existing FRs are intact.

```bash
# Implement all verification tasks (parallel — different file sections)
/speckit.implement T001   # Draft markers on templates (FR-001)
/speckit.implement T002   # SKILL.md Step 3 draft check (FR-002, FR-003)
/speckit.implement T003   # Phase 6 output validation (FR-004, FR-005, FR-006)
/speckit.implement T004   # Dispute-Parsing Subsystem (FR-010, FR-011 partial)
/speckit.implement T005   # Baseline Features (FR-018)

# Phase 1 consensus gate
/conversus conversus/specs/005-p2p3-backlog-hardening/gates/phase-1/conversus.yml
```

**Checkpoint**: All 10 pre-existing FRs verified, FR-011 partial confirmed. Proceed to Phase 2.

---

## Phase 2: Two-Tier Convention (T006-T007)

```bash
# Implement
/speckit.implement T006   # Add two-tier taxonomy to STATUS.md (FR-012)
/speckit.implement T007   # Apply acceptance labels to all specs (FR-013, FR-009)

# Phase 2 consensus gate (prior: Phase 1 synthesis)
/conversus conversus/specs/005-p2p3-backlog-hardening/gates/phase-2/conversus.yml
```

**Checkpoint**: Two-tier convention defined and applied. STATUS.md taxonomy is authoritative.

---

## Phase 3: STATUS.md Enrichment (T008-T012a)

Sequential — all edit the same file.

```bash
# Implement
/speckit.implement T008   # Shared Subsystems + maintenance note (FR-008a)
/speckit.implement T009   # Cross-Spec Dependencies (FR-008)
/speckit.implement T010   # Risk-of-Gap (FR-016)
/speckit.implement T011   # Effort estimates (FR-017)
/speckit.implement T012   # SKILL.md Structure Plan (FR-019)
/speckit.implement T012a  # Spec 005 self-tracking (FR-008, SC-003)

# Phase 3 consensus gate (prior: Phase 2 synthesis)
/conversus conversus/specs/005-p2p3-backlog-hardening/gates/phase-3/conversus.yml
```

**Checkpoint**: STATUS.md is the complete cross-spec reference.

---

## Phase 4: SKILL.md Documentation (T019, T019a, T013-T015)

Sequential — all edit the same file. T019 first (edits flow downward).

**Note**: Phase 4 depends on Phase 1 only — can run in parallel with Phases 2-3.

```bash
# Implement
/speckit.implement T019   # Round Termination cross-reference (FR-011a)
/speckit.implement T019a  # Trigger Evaluation cross-reference (FR-011b)
/speckit.implement T013   # Heading match semantics (FR-007)
/speckit.implement T014   # Phase 4 missing doc edge case (FR-014)
/speckit.implement T015   # Phase 6 overwrite semantics (FR-015)

# Phase 4 consensus gate (prior: Phase 1 synthesis)
/conversus conversus/specs/005-p2p3-backlog-hardening/gates/phase-4/conversus.yml
```

**Checkpoint**: SKILL.md Phase 6 section complete with all edge cases, match semantics, and overwrite behavior.

---

## Phase 5: Polish (T016-T018)

Depends on Phases 3 AND 4 both complete.

```bash
# Implement
/speckit.implement T016   # Verify all 19 FRs
/speckit.implement T017   # Update STATUS.md timestamp + verify maintenance note
/speckit.implement T018   # Run quickstart verification

# Phase 5 consensus gate (prior: Phase 3 + Phase 4 syntheses)
/conversus conversus/specs/005-p2p3-backlog-hardening/gates/phase-5/conversus.yml
```

**Done.**

---

## Execution Order

```
Phase 1 (verify)
    ├── Phase 2 (taxonomy) → Phase 3 (STATUS.md) ──┐
    └── Phase 4 (SKILL.md) ────────────────────────┤
                                                    └── Phase 5 (polish)
```

Phases 3 and 4 can run in parallel (different files). Phase 5 waits for both.

## Feed-Forward Chain

Each gate's synthesis feeds into the next gate as `prior:` context:

| Gate | Prior Context |
|------|--------------|
| Phase 1 | none |
| Phase 2 | Phase 1 synthesis |
| Phase 3 | Phase 2 synthesis |
| Phase 4 | Phase 1 synthesis |
| Phase 5 | Phase 3 + Phase 4 syntheses |

## Gate Agent Summary

| Phase | Agents | Focus |
|-------|--------|-------|
| 1 | compliance-auditor, scope-boundary | FR verification, no-change enforcement |
| 2 | taxonomy-reviewer, consistency-checker | Definition clarity, label correctness |
| 3 | completeness-checker, quality-reviewer | Section coverage, content quality |
| 4 | spec-compliance, integration-checker | FR match, SKILL.md coherence |
| 5 | fr-auditor, cross-phase-integrator | All 19 FRs, cross-phase consistency |

Each gate launches 7 agents (2 reviews + 2 cross-reviews + 2 revisions + 2 disputes + 1 synthesis = 9... N=2: N²+N+1 = 7).
