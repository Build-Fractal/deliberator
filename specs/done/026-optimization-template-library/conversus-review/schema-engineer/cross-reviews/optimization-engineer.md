# Cross-Review: schema-engineer reviewing optimization-engineer

**Spec**: 026-optimization-template-library

---

## Dangerous Contradictions

None. The optimization-engineer's mathematical review is authoritative on formulation correctness and does not conflict with schema-level findings.

---

## Tensions

### T1: Concern severity calibration (Low vs. Info)

- **optimization-engineer's position**: Rates PSD validation (OE-1) and supply_demand sum-to-zero (OE-2) as Info. Rates game_form cross-validation (OE-3) and mode_compatibility cross-validation (OE-4) as Low.
- **schema-engineer's position**: I agree with all four severity ratings. The distinction is correct: OE-1 and OE-2 are inherent limitations of the template abstraction layer (you cannot enforce numerical properties in a YAML schema), while OE-3 and OE-4 are test coverage gaps that *could* be fixed with additional parametric tests. The actionability criterion justifies the severity split.
- **Nature**: Agreement. No tension on substance.

### T2: Parameter reasonableness scope

- **optimization-engineer's position**: Assesses parameter reasonableness (ranges, defaults, types) from a mathematical perspective. Finds all parameters reasonable.
- **schema-engineer's position**: I assess parameter structure (correct type declarations, gap_question presence) from a schema perspective. Both perspectives are needed: a parameter could be structurally correct (right type, gap_question present) but mathematically unreasonable (range too wide, default nonsensical), or vice versa.
- **Nature**: Complementary, not competing. The two-lens approach provides stronger coverage than either alone.

---

## Safe Agreements

1. **All 15 formulations are mathematically correct**: I defer to the optimization-engineer on mathematical soundness. The formulations use standard notation and problem classifications consistent with the OR literature.

2. **Parameters are reasonable and well-typed**: The optimization-engineer's mathematical assessment and my schema assessment converge: parameters have appropriate types (`string` for encoded matrices, `integer` for counts, `float` for scalars), meaningful ranges, and sensible defaults.

3. **Examples produce feasible instances**: The optimization-engineer verified feasibility of all examples. From a schema perspective, the examples provide realistic parameter values that a construction pipeline would produce -- not toy values or edge cases.

4. **PSD and sum-to-zero are correctly deferred to solver**: Both agents agree that these are solver-time concerns, not template concerns. The template descriptions correctly document these requirements.

5. **game_form and mode_compatibility cross-validation is needed**: Both agents independently identified these gaps (OE-3/OE-4 and SE-2/SE-3). The convergence is strong evidence this is a real gap worth addressing.

---

## Additions from schema-engineer perspective

### A1: Template-to-constraint correspondence is both structural and semantic

The optimization-engineer notes that constraints referenced are "mathematically required" for each formulation. I can confirm from the schema side that this semantic correctness is also *verifiable* -- the test `TestTemplateConstraintReferences.test_constraint_refs_exist` already checks structural existence. A semantic test (does this problem class require these constraints?) would need domain knowledge encoded in the test, which is impractical. The current structural test plus the optimization-engineer's manual review provides sufficient coverage.

### A2: String encoding consistency

The optimization-engineer notes that string-encoded matrices require parsing (OE-3, Info). I want to highlight a positive aspect: the encoding convention is *consistent* across all templates. Vectors use comma-separation. Matrices use semicolon-separated rows of comma-separated values. Arc lists use semicolon-separated triples. This consistency means a single parser module can handle all templates, which reduces the implementation burden for the construction pipeline (spec 014).

### A3: game_form appropriateness

The optimization-engineer notes that `assignment-optimal` uses `gnep` while most others use `parametric`. From the schema perspective, I can confirm that `gnep` and `parametric` are both valid game_form values that reference existing game form YAML files. The choice of `gnep` for assignment is semantically interesting -- it models the assignment problem as a game where each agent's optimal strategy depends on other agents' assignments. The `parametric` form models optimization problems where agents operate on shared parameters rather than competing directly.
