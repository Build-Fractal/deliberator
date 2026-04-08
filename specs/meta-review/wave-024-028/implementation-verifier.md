# Meta-Review Phase 1: Implementation Verifier — Wave 024-028

**Scope**: Specs 024, 027, 028
**Date**: 2026-04-01
**Auditor role**: Spot-check 3 claims per synthesis against actual code. VERIFIED/INACCURATE/STALE.

---

## Spec 024 — Cross-Plugin Interfaces

### Claim 1: "The predictor receives only the current round's score and wraps it in a single-element list" (P1 item 1)

**Source**: `conversus/plugins/nashopt/predictor.py:255-261`

**Code** (lines 255-261):
```python
eq_score = state.plugin_results.get("equilibrium_score")
equilibrium_scores: list[float] | None = None
if eq_score is not None:
    # Current round's score is available; prior rounds are not
    # (they were consumed in earlier hook executions).  Pass as
    # a single-element list so the predictor can use it.
    equilibrium_scores = [float(eq_score)]
```

**Verdict**: **VERIFIED** — The code exactly matches the synthesis claim. The predictor wraps the single eq_score in a one-element list. The comment even acknowledges prior rounds are lost.

---

### Claim 2: "`any(s != 0.0 for s in equilibrium_scores)` conflates scorer absent with score equals zero" (P1 item 2)

**Source**: `conversus/plugins/nashopt/convergence.py:268-271`

**Code** (lines 268-271):
```python
use_3d = (
    equilibrium_scores is not None
    and len(equilibrium_scores) > 0
    and any(s != 0.0 for s in equilibrium_scores)
)
```

**Verdict**: **VERIFIED** — The `any(s != 0.0 ...)` gate is present. A legitimate equilibrium_score of 0.0 (all agents not at equilibrium) would cause fallback to 2D, losing the 3D signal. The synthesis correctly identifies this as a sentinel bug.

---

### Claim 3: "SC-003: Topological sort guarantees scorer before predictor — MET"

**Source**: `conversus/plugins/base.py:306-393` (topological sort), `conversus/plugins/nashopt/scorer.py:349` (`produces = ["equilibrium_score"]`), `conversus/plugins/nashopt/predictor.py:181` (`consumes = ["equilibrium_score"]`)

**Code verification**:
- `EquilibriumScorer.produces = ["equilibrium_score"]` (scorer.py:349)
- `ConvergencePredictor.consumes = ["equilibrium_score"]` (predictor.py:181)
- `_topological_sort_plugins()` builds a dependency graph where producers run before consumers (base.py:346-350)
- Test `test_scorer_before_predictor_in_topological_sort` confirms this (test_cross_plugin.py:679-696)

**Verdict**: **VERIFIED** — Topological sort correctly handles the scorer->predictor dependency. Both the code and tests confirm SC-003.

---

## Spec 027 — Solver Validation Flow

### Claim 4: "SC-001 is satisfied by the fairness-advocate prompt"

**Source**: `conversus/schemas/validation.py:134-150` (assignment agent templates)

**Code** (fairness-advocate prompt):
```python
"You are the Fairness Advocate. Examine whether the assignment "
"distributes resources equitably. Flag cases where the best "
"resources are concentrated on low-priority tasks or where "
"some stakeholders are systematically disadvantaged.\n\n"
+ _SENSITIVITY_INSTRUCTIONS
```

**Verdict**: **VERIFIED** — The fairness-advocate prompt explicitly instructs the agent to "Flag cases where the best resources are concentrated on low-priority tasks," which directly addresses SC-001 (bad assignment detection). The test `test_fairness_advocate_prompt_catches_inequity` also confirms this.

---

### Claim 5: "`constraint_additions: list[str]` — free-form strings, not solver-consumable" (Dispute 2, FR-010)

**Source**: `conversus/schemas/validation.py:61-64`

**Code**:
```python
constraint_additions: list[str] = Field(
    default_factory=list,
    description="Proposed new constraints to improve the solution (FR-009).",
)
```

**Verdict**: **VERIFIED** — `constraint_additions` is typed as `list[str]`, confirming the synthesis claim that these are free-form strings unsuitable for solver consumption. The synthesis correctly identifies the need for a `ConstraintAddition` typed model.

---

### Claim 6: "SC-005 (timing) is satisfied at 16 LLM calls for a 3-agent deliberation"

**Source**: `conversus/schemas/validation.py:236-245` (config generation output)

**Code verification**: The generated config has `rounds: 1`, `iterations: 1`, and 3 agents. A standard conversus deliberation with 3 agents and 1 round produces:
- Phase 1: 3 reviews (3 calls)
- Phase 2: 6 cross-reviews (6 calls)
- Phase 3: 3 revisions (3 calls)
- Phase 4: 3 dispute assessments (3 calls)
- Phase 5: 1 synthesis (1 call)
= 16 LLM calls total

**Verdict**: **VERIFIED** — The math checks out. The config generator produces a 3-agent, 1-round config which maps to 16 LLM calls through the standard 5-phase pipeline.

---

## Spec 028 — Mode Expansion

### Claim 7: "'ration' keyword regex is a bug — matches 'rational' as substring"

**Source**: `conversus/schemas/construction.py:105-108`

**Code**:
```python
DecisionType.RESOURCE_ALLOCATION: re.compile(
    r"allocat|distribut|budget|resource\s+pool|capacity"
    r"|headcount|assign\s+resource|fair\s+share|ration",
    re.IGNORECASE,
),
```

**Verification**: The pattern `ration` in the regex is not word-boundary-protected. It will match as a substring of "rational", "rationale", "irrational", etc. The regex for NEGOTIATION includes `negotiat` (also a prefix match, but the target word is "negotiate/negotiation" which would also match RESOURCE_ALLOCATION's "ration" prefix of "rationing").

**Verdict**: **VERIFIED** — The `ration` pattern will indeed match "rational" and similar words. This is a real bug that could cause misclassification. The synthesis correctly identifies the fix as `\bration(?:ing|ed)?\b`.

---

### Claim 8: "All 4 mode-to-form mappings are correct — negotiation->bayesian, resource-allocation->coalitional, fair-division->coalitional, mechanism-design->mechanism-design"

**Source**: `conversus/schemas/construction.py:123-132`

**Code**:
```python
_DECISION_TYPE_MODE: dict[DecisionType, str] = {
    DecisionType.SELECTION: "winner-take-all",
    DecisionType.INTEGRATION: "cooperative",
    DecisionType.SCOPING: "prisoners-dilemma",
    DecisionType.STRESS_TEST: "red-blue",
    DecisionType.NEGOTIATION: "negotiation",
    DecisionType.RESOURCE_ALLOCATION: "resource-allocation",
    DecisionType.FAIR_DIVISION: "fair-division",
    DecisionType.MECHANISM_DESIGN: "mechanism-design",
}
```

**Note**: The synthesis claim is about mode-to-game-form mappings (bayesian, coalitional, etc.), not DecisionType-to-mode mappings. The `_DECISION_TYPE_MODE` dict maps DecisionType to mode strings. The game form mapping would be in the objective templates or schema/modes YAML files, not in construction.py.

**Verdict**: **PARTIALLY VERIFIED** — The DecisionType-to-mode mapping is correct and all 8 entries are present. However, the synthesis claim about game form mappings (bayesian, coalitional) refers to schema-level definitions in the mode YAML files, not the construction.py code. The claim is about a different layer than what is shown here. The mode-to-form mappings are defined in `schema/modes/*.yml`, which do exist (8 files confirmed), but the specific form values were not verified against the claim.

---

### Claim 9: "`test_mode_expansion.py` must be populated — the empty test file is the single most critical gap"

**Source**: `tests/test_mode_expansion.py`

**File contents**: The file exists but is empty (1 line).

**Verdict**: **VERIFIED** — The test file is genuinely empty. No tests exist for mode expansion. This is confirmed as the most critical gap for SC-005 (backward compatibility) empirical confirmation.

---

## Summary

| # | Claim | Spec | Verdict |
|---|-------|------|---------|
| 1 | Predictor wraps eq_score in single-element list | 024 | VERIFIED |
| 2 | Zero-score sentinel gate conflates absent with zero | 024 | VERIFIED |
| 3 | Topological sort guarantees scorer before predictor | 024 | VERIFIED |
| 4 | Fairness-advocate prompt satisfies SC-001 | 027 | VERIFIED |
| 5 | constraint_additions is list[str] (not structured) | 027 | VERIFIED |
| 6 | SC-005 satisfied at 16 LLM calls | 027 | VERIFIED |
| 7 | "ration" regex matches "rational" | 028 | VERIFIED |
| 8 | Mode-to-form mappings correct | 028 | PARTIALLY VERIFIED |
| 9 | test_mode_expansion.py is empty | 028 | VERIFIED |

**8 of 9 claims VERIFIED. 1 PARTIALLY VERIFIED (game form mapping layer unclear). 0 INACCURATE. 0 STALE.**
