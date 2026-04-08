# Revision -- integration-architect

## Recommendation Dispositions

### Rec 1: Add influence-aware heading alternatives to mode schema (originally P1)
**Disposition: Maintain at P1.**
Universal agreement across all three agents. functional-typing provides the Pydantic model design (`influence_headings: dict[InfluenceLevel, list[str]]`). game-engine-advocate endorses Option A (structured data) over Option B (skip validation). The YAML structure proposed in the original review is directly compatible with functional-typing's typed field. No changes needed.

### Rec 2: Wire {ARBITRATION_PATHS} into cross-round synthesis (originally P1)
**Disposition: Maintain at P1.**
Both co-reviewers adopted this in their revisions after not catching it in their original reviews. This validates the integration-architect's prioritization. The template is the last-mile consumer; without the reference, the entire schema-model-SKILL.md pipeline for this variable is dead infrastructure.

### Rec 3: Add {ARBITRATION_RULINGS} to cross-round synthesis template (originally P1)
**Disposition: Maintain at P1.**
Same reasoning as Rec 2. The variable is provisioned end-to-end but the template does not consume it.

### Rec 4: Document the linter's static-vs-runtime heading validation gap (originally P2)
**Disposition: Maintain at P2.**
functional-typing's cross-review notes a tension between "document the gap" vs. "build infrastructure to close the gap." Both are complementary: document the current boundary AND build the data model (Rec 1) that makes the boundary eventually closable. The documentation prevents a future contributor from attempting a misguided "fix" to the linter.

### Rec 5: Add PRIOR_ARBITRATION_SECTION field documentation (originally P2)
**Disposition: Maintain at P2.**
functional-typing's complementary recommendation (model_validator enforcing PATH when SECTION is non-empty) is additive. Both documentation and enforcement are warranted, but documentation comes first since the model_validator is a P3 item.

### Rec 6: Verify PRIOR_ARBITRATION_PATH is set during dispatch (originally P2)
**Disposition: Maintain at P2.**
No cross-review disagreement. game-engine-advocate's SA5 (path computation clarity for plugin developers) reinforces the need.

### Rec 7: Add influence_headings to ArbitrationConfig Pydantic model (originally P2)
**Disposition: Upgrade to P1, merge with Rec 1.**
This is a prerequisite for Rec 1. The YAML schema change (Rec 1) requires the Pydantic model to accept the new field (Rec 7). If the model does not have the `influence_headings` field, the YAML data will be rejected by `extra: "forbid"` validation. These two recommendations should be treated as a single atomic change.

### Rec 8: Add stagnation interaction documentation for influence levels (originally P3)
**Disposition: Maintain at P3.**
No cross-review disagreement. The stagnation-influence interaction is inferrable from reading order but should be explicit.

### Rec 9: Mark ARBITRATION_RULINGS as required:true when inter-round (originally P3)
**Disposition: Maintain at P3, note dependency on config_conditions evaluation.**
functional-typing correctly observes that marking a variable `required: true` with a config_conditions gate is meaningless if config_conditions are not evaluated. The practical effect depends on the resolution of functional-typing's Rec 5 (implement or document config_conditions evaluation). If config_conditions remain metadata-only, then `required: true` will be enforced unconditionally, which is wrong for this variable. The correct sequencing is: (1) document that config_conditions are metadata-only (functional-typing Rec 5 minimum), (2) then address required status when the evaluation mechanism exists.

## New Recommendations

### NEW-1: Use Phase enum in validate.py (Priority: P2)
**Source: functional-typing Rec 1, downgraded from P1 during cross-review.**
Adopting this recommendation at P2. The string comparisons work but violate Constitution Principle IX. The functional-typing agent accepted the P2 downgrade. This is code quality improvement, not a correctness fix.

### NEW-2: Type VariableDefinition.phases as list[Phase] (Priority: P2)
**Source: functional-typing Rec 4.**
Adopting this recommendation. Eliminates a manual validator by leveraging the type system directly. Consistent with the Phase enum adoption in NEW-1.

### NEW-3: Add structural markers for provisionally resolved disputes (Priority: P2)
**Source: Own Missed Opportunity 6, reinforced by game-engine-advocate cross-review.**
The dispute-parsing subsystem uses `DISPUTES_BEGIN`/`DISPUTES_END` markers. For `recommended` influence, provisionally-resolved disputes need distinct markers (e.g., `PROVISIONALLY_RESOLVED_BEGIN`/`PROVISIONALLY_RESOLVED_END`) so the dispute-parsing subsystem can accurately count remaining vs. provisionally-resolved disputes. Without these markers, the orchestrator relies on agent prose categorization, violating "templating over inference."

## Position Summary

After cross-reviews, the integration-architect position has strengthened on its core claims and adopted two functional-typing recommendations:

1. **P1 consolidation**: The three original P1 items (influence-aware headings, ARBITRATION_PATHS wiring, ARBITRATION_RULINGS wiring) are validated by all agents. Rec 7 (ArbitrationConfig model update) is upgraded to P1 and merged with Rec 1 as an atomic change.

2. **Type-system gaps adopted**: functional-typing's Phase enum usage (Rec 1, at P2) and VariableDefinition.phases typing (Rec 4) are adopted because they strengthen the codebase without conflicting with integration concerns.

3. **Structural markers elevated**: The provisionally-resolved dispute marker gap is elevated from a "missed opportunity" observation to a concrete NEW-3 recommendation at P2, reinforced by game-engine-advocate's convergence predictor use case.

The core integration-architect position: the template wiring gaps ({ARBITRATION_PATHS}, {ARBITRATION_RULINGS}) are the most important findings because they represent dead infrastructure -- fully provisioned pipelines with no last-mile connection. The influence-aware heading gap is universally agreed as P1. Type-system improvements are important but secondary to wiring correctness.
