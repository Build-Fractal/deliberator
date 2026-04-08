# Cross-Review: game-theorist reviewing spec-compliance

**Spec**: 025-game-form-expansion
**Reviewer**: game-theorist
**Subject**: spec-compliance Phase 1 review

---

## Verified Claims

### 1. FR compliance matrix is accurate

The FR-by-FR assessment is thorough and well-evidenced. I verify:

- **FR-001 through FR-003**: PASS verdicts correct. YAML schemas exist, Pydantic models have validators, mode mapping updated.
- **FR-004**: PASS verdict correct (revised from the earlier conversus-output which had PARTIAL). The check functions are the diagnostic; the PotentialGame model is a result container.
- **FR-005 through FR-007**: PASS verdicts correct. The observation that FR-005 is exceeded (no scipy dependency despite FR-005 allowing it) is a good note.
- **FR-010**: The spec-compliance agent correctly identifies that integrality.yml and cardinality.yml exist in `schema/objective-functions/constraints/`. This was marked NOT ASSESSED in the prior round -- good catch.
- **FR-011 through FR-013**: PASS verdicts correct with accurate test counts.

### 2. SC-001 and SC-002 are correctly verified

SC-001 uses the exact test cases cited in the spec (coordination game = potential, matching pennies = non-potential). SC-002 uses a 3-player game with explicit grand coalition value check. Both are definitive.

### 3. SC-003 and SC-004 correctly deferred

Tier 2 solver integration is not in scope for this phase. The spec explicitly separates Tier 1 (pure Python + scipy) from Tier 2 (nashopt/AMPL). Deferring SC-003 and SC-004 is the correct call.

---

## Disagreements

### 1. SC-005: the 10-vs-9 analysis should be more decisive

The spec-compliance agent notes the discrepancy but frames it as "PARTIAL" without taking a clear position. From a mathematical standpoint, the count is unambiguous:

**Existing forms** (pre-spec-025): normal-form, gnep, parametric, stackelberg = 4
**New forms** (spec 025): coalitional, congestion, bayesian, repeated, mechanism-design = 5
**Total**: 9

The potential diagnostic is explicitly not a form (FR-004). No other form is described in spec section 2. The spec text `len(game_forms) >= 10` is a drafting error -- the section describes exactly 6 new items (5 forms + 1 diagnostic), which combined with 4 existing forms gives 9 forms + 1 diagnostic.

**My position**: SC-005 should be PASS with an annotation that the spec threshold should be amended to >= 9. The implementation correctly covers every form described in the spec.

### 2. FR-008/FR-009 should distinguish between "not assessed" and "not required yet"

The spec-compliance agent marks FR-008 and FR-009 as "NOT ASSESSED" and attributes them to spec 026. However, FR-008 is a requirement of spec 025 itself ("Each game form MUST have at least one objective template"). Whether spec 026 also addresses this is irrelevant -- the requirement exists in this spec.

Current state: `schema/objective-functions/` contains templates that apply to some new forms (e.g., `cooperative-consensus.yml` could serve coalitional games, `territory-claiming.yml` could serve congestion games). A more accurate verdict would be "PARTIAL -- some new forms are covered by existing templates, but no dedicated per-form templates exist."

---

## Additions

### Cross-cutting observation on `is_potential_game()` and FR-004 tension

FR-004 says the diagnostic is "a check applied to existing game forms." The implementation is a check applied to 2-player normal-form games only. This means:

- For NormalFormGame with 2 players: diagnostic works
- For NormalFormGame with 3+ players: diagnostic fails (no implementation)
- For GNEPGame: diagnostic inapplicable (no payoff matrix to check)
- For StackelbergGame: diagnostic inapplicable (leader-follower structure, not simultaneous)

The spec's language "existing game forms" is broader than what's implemented. This is my Finding #1 from the initial review, and I note that the spec-compliance agent does not flag it despite it being a compliance gap. The implementation satisfies FR-004 in spirit (the diagnostic is a function, not a form) but not in scope (it does not apply to all existing forms).
