# Feature Specification: Mode Expansion

**Feature ID**: `028-mode-expansion`
**Created**: 2026-03-27
**Status**: Draft
**Depends On**: `025-game-form-expansion` (new game forms), `008-interests-mode` (mode selection)
**Origin**: Gap analysis — current 4 modes don't cover negotiation, resource allocation, or fair division

---

## 1. Feature Summary

Expand from 4 deliberation modes to 8, covering the most common real-world multi-agent decision scenarios. Each new mode maps to specific game forms and has its own template set.

---

## 2. New Modes

### 2.1 Negotiation Mode

**When**: Two or more parties have conflicting interests and must reach a mutually acceptable agreement.

**Game forms**: Bayesian (hidden preferences)

**Template set**: New `templates/negotiation/` directory

**Key difference from cooperative**: Cooperative assumes all agents want the same outcome. Negotiation assumes agents want different outcomes and must find a zone of possible agreement (ZOPA).

**Agents**: Each party + a mediator. Cross-reviews are offer/counter-offer exchanges.

**Synthesis**: Maps the ZOPA, identifies best alternative to negotiated agreement (BATNA) per party, recommends the Pareto-optimal deal.

### 2.2 Resource Allocation Mode

**When**: A fixed pool of resources must be distributed among competing demands.

**Game forms**: Mechanism design (VCG) + cooperative (Shapley for fair allocation)

**Template set**: New `templates/resource-allocation/` directory

**Key difference from selection**: Selection picks one winner. Resource allocation distributes among all.

**Agents**: Each demand source (team, project, department). Cross-reviews challenge allocation fairness.

**Synthesis**: Produces allocation table + Shapley-based fairness score + VCG truthfulness guarantee.

### 2.3 Fair Division Mode

**When**: Something must be divided among parties who have different valuations.

**Game forms**: Cooperative (Shapley, core, nucleolus)

**Template set**: New `templates/fair-division/` directory

**Key difference from resource allocation**: Fair division focuses on subjective valuations (each party values items differently), not objective quantities.

**Agents**: Each party's valuation perspective. Cross-reviews challenge valuation claims.

**Synthesis**: Produces envy-free (or approximately envy-free) allocation with fairness guarantees.

### 2.4 Mechanism Design Mode

**When**: You need to design the rules of a system so participants can't game it.

**Game forms**: Mechanism design (VCG, auction forms)

**Template set**: New `templates/mechanism-design/` directory

**Key difference from all others**: Other modes use fixed rules. This mode designs the rules themselves.

**Agents**: Incentive analyst, efficiency advocate, participation advocate, gaming adversary (red-team for mechanism exploitation).

**Synthesis**: Produces mechanism specification + incentive compatibility proof + gaming vulnerability report.

---

## 3. Functional Requirements

### Mode Infrastructure
- **FR-001**: Each new mode MUST have a complete template set (review, cross-review, revision, disputes, synthesis, arbitration).
- **FR-002**: The mode-mapping (`schema/game-forms/mode-mapping.yml`) MUST be updated.
- **FR-003**: `VALID_MODES` in `engine/config.py` and `conversus/schemas/objectives.py` MUST be updated.
- **FR-004**: The decision type classifier (spec 014) MUST route new problem types to new modes.

### Mode Selection
- **FR-005**: `/conversus mode` MUST include new modes in its recommendation matrix.
- **FR-006**: New decision types MUST be added: `negotiation`, `resource_allocation`, `fair_division`, `mechanism_design`.
- **FR-007**: Heuristic mode detection MUST recognize keywords for each new type.

### Templates
- **FR-008**: Each mode's synthesis template MUST define mode-specific dispute headings for the Dispute-Parsing Subsystem.
- **FR-009**: Each mode's arbitration template MUST define mode-specific required headings.
- **FR-010**: The linter (`linter/validate.py`) MUST validate templates for new modes.

### Backward Compatibility
- **FR-011**: Existing 4 modes MUST work identically.
- **FR-012**: Existing configs with the original 4 modes MUST NOT be affected.

---

## 4. Success Criteria

- **SC-001**: `/conversus mode` recommends `negotiation` for "We need to negotiate a contract with our vendor."
- **SC-002**: A resource allocation deliberation produces an allocation table with Shapley fairness scores.
- **SC-003**: A mechanism design deliberation produces a rule set with an incentive compatibility analysis.
- **SC-004**: `len(VALID_MODES) >= 8` after implementation.
- **SC-005**: All existing tests pass unchanged (backward compatibility).

---

## 5. Constraints

- New modes MUST NOT require new solver dependencies.
- Each mode MUST work with the heuristic fallback (no solver installed).
- Templates are markdown prompt engineering — no code changes to the engine for template-level changes.
- The Dispute-Parsing Subsystem MUST be extended (new heading patterns) but not restructured.
