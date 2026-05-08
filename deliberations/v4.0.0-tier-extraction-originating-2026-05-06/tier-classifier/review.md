### Executive Summary

The proposed tier extraction attempts to split 26 active constitutional principles across three hierarchical tiers based on scope of applicability. The classification correctly identifies most universal software engineering principles (I, II, III, IX, XI, XIV, XXVIII) and conversus-specific deliberation infrastructure (V, XIX, XX, XXI). However, several principles are misclassified due to scope misalignment. Most critically, Principle VIII (Templating Engines) is classified as Universal despite being specific to LLM-driven systems, while Principle XII (No Dead Infrastructure) is relegated to Suite tier despite being a fundamental software engineering principle. The classification framework itself is sound, but 4-5 principles require reclassification to accurately reflect their true scope of applicability. **Recommendation: Reclassify Principles VIII and IV to Suite tier, and XII to Universal tier before proceeding to spec drafting.**

### Alignment

- **Universal core principles** (CONSTITUTION.md L158-183, L248-273, L310-335): Principles I (Spec-Driven), II (Stable Interfaces), III (Backward-Compatible Extension) correctly identified as Universal. These establish fundamental software engineering disciplines that apply to any product line.

- **Conversus-specific deliberation infrastructure** (CONSTITUTION.md L1713-1748, L1755-1788): Principles XVII-XXI correctly classified as Component tier. These govern conversus-oss internal structure (content classification, progressive disclosure, non-extractable core, decomposition mechanisms).

- **Multi-agent system constraints** (CONSTITUTION.md L401-425, L1290-1349): Principles V (Observable Deliberation) and XXIV (Safety-Critical Defense-in-Depth) appropriately placed at Suite tier. These apply to any deliberation engine but not to general software products.

- **Functional programming discipline** (CONSTITUTION.md L474-584): Principle IX correctly classified Universal. The explicit typing requirements and functional patterns apply across all Build Fractal products.

- **Plugin monetization boundary** (CONSTITUTION.md L1055-1106): Principle XV (Plugin Isolation) correctly placed at Suite tier. This defines the conversus-family monetization seam but wouldn't apply to non-plugin product lines.

- **Provider abstraction requirements** (CONSTITUTION.md L1490-1520, L1521-1568): Principles XXIII (Provider Robustness) and XXV (Live Test Cost) appropriately classified Suite tier. These apply to any conversus repo using LLM providers but not to general software products.

### Missed Opportunities

- **Template-specific scope recognition**: Principle VIII (Templating Engines, L448-473) addresses "mechanical template-driven behavior over LLM inference" - inherently specific to AI systems that generate prompts or content, not universal to all software. The classification misses that most Build Fractal products may not have templating surfaces at all.

- **Documentation scope refinement**: Principle IV (Documentation Is the Product, L336-351) explicitly states "In a prompt-orchestrated system, specification text IS the implementation" - the prompt-orchestration framing is conversus-specific, not universal to all documentation practices.

- **Dead infrastructure universality**: Principle XII (No Dead Infrastructure, L836-865) states a fundamental software engineering principle about unused capabilities, but examples are conversus-specific. The core principle applies universally while implementation details are domain-specific.

- **Enum completeness generalization**: Principle XIII (Enum Completeness, L866-883) addresses exhaustive enum usage - a general programming discipline that applies beyond conversus to any codebase using typed enumerations.

- **Meta-testing pattern scope**: Principle XXVI (Meta-Testing, L1655-1675) describes testing parametrized capability sets - applicable to any system with parametrized features, not just conversus-oss internal testing.

- **Mathematical transparency boundaries**: Principle XVI (Mathematical Transparency, L1107-1289) addresses optimization parameter pinning - could apply to any Build Fractal product with mathematical surfaces, not just conversus-family repos.

### Off-Base Assumptions

- **Universal templating assumption**: The classification assumes all Build Fractal products will have template engines for content generation (Principle VIII at Universal tier). Many software products have no templating surface or LLM inference trade-offs to manage.

- **Documentation uniformity assumption**: Classifying Principle IV (Documentation Is the Product) as Universal assumes all Build Fractal products are "prompt-orchestrated systems" where specs are executable. This framing is conversus-specific.

- **Suite-limited infrastructure management**: Placing Principle XII (No Dead Infrastructure) at Suite tier assumes only conversus-family repos need dead code discipline. This is a universal software engineering concern.

### Actionable Recommendations

1. **Reclassify Templating Engines** (Priority: P1)
   - **Current state**: Principle VIII classified as Universal tier (L448-473).
   - **Proposed change**: Move to Suite tier. The principle addresses "mechanical template-driven behavior over LLM inference" which is specific to AI/LLM systems.
   - **Rationale**: Non-AI Build Fractal products may have no templating engines or inference trade-offs to manage.
   - **Risk if ignored**: Non-AI products inherit irrelevant LLM-specific constraints.

2. **Reclassify Documentation Is Product** (Priority: P1)  
   - **Current state**: Principle IV classified as Universal tier (L336-351).
   - **Proposed change**: Move to Suite tier. The principle explicitly states "In a prompt-orchestrated system, specification text IS the implementation."
   - **Rationale**: Prompt-orchestration is conversus-specific; not all Build Fractal products are prompt-orchestrated systems.
   - **Risk if ignored**: Non-prompt-orchestrated products inherit inappropriate documentation constraints.

3. **Reclassify Dead Infrastructure Management** (Priority: P2)
   - **Current state**: Principle XII classified as Suite tier (L836-865).
   - **Proposed change**: Move to Universal tier. Core principle is "Every provisioned capability MUST have at least one consumer."
   - **Rationale**: Dead code elimination is a universal software engineering discipline; implementation details can be domain-specific.
   - **Risk if ignored**: Non-conversus Build Fractal products lack fundamental code hygiene requirements.

4. **Reclassify Enum Completeness** (Priority: P2)
   - **Current state**: Principle XIII classified as Suite tier (L866-883).
   - **Proposed change**: Move to Universal tier. Core principle is exhaustive enum usage in typed languages.
   - **Rationale**: Enum completeness is a general programming discipline applicable to any typed codebase.
   - **Risk if ignored**: Non-conversus repos lack typed enumeration discipline.

5. **Reclassify Meta-Testing Pattern** (Priority: P3)
   - **Current state**: Principle XXVI classified as Component tier (L1655-1675).
   - **Proposed change**: Move to Suite tier. Principle addresses testing parametrized capability sets.
   - **Rationale**: Any system with parametrized capabilities benefits from meta-testing to prevent coverage drift.
   - **Risk if ignored**: Only conversus-oss gets parametrized capability testing discipline.

6. **Evaluate Mathematical Transparency Scope** (Priority: P3)
   - **Current state**: Principle XVI classified as Suite tier (L1107-1289).
   - **Proposed change**: Consider Universal tier if other Build Fractal products will have mathematical optimization surfaces.
   - **Rationale**: Parameter pinning and mathematical transparency could apply beyond conversus if other products have optimization components.
   - **Risk if ignored**: Mathematical discipline confined unnecessarily to conversus suite.

7. **Document Tier Assignment Criteria** (Priority: P2)
   - **Current state**: Classification rationale implicit in tier placement.
   - **Proposed change**: Add explicit criteria for Universal vs Suite vs Component determination to GOVERNANCE.md.
   - **Rationale**: Future tier assignments need consistent evaluation framework.
   - **Risk if ignored**: Ad-hoc tier assignments create inconsistent hierarchical boundaries.

8. **Cross-Reference Principle Dependencies** (Priority: P3)
   - **Current state**: No explicit mapping of cross-principle dependencies across tiers.
   - **Proposed change**: Document which Suite/Component principles depend on Universal principles.
   - **Rationale**: Tier inheritance relationships need explicit dependency tracking.
   - **Risk if ignored**: Principle amendments at higher tiers may unknowingly break lower-tier principles.

### Referenced Documentation

- `conversus-oss/CONSTITUTION.md` — sections/lines cited: L158-183, L248-273, L310-335, L336-351, L401-425, L448-473, L474-584, L836-865, L866-883, L1055-1106, L1107-1289, L1290-1349, L1490-1520, L1521-1568, L1655-1675, L1713-1748, L1755-1788
- `build-fractal/CONSTITUTION.md` — sections/lines cited: Universal principle enumeration table
- `build-fractal/conversus/CONSTITUTION.md` — sections/lines cited: Suite principle enumeration table  
- `conversus-oss/deliberations/v4.0.0-tier-extraction-originating-2026-05-06/QUESTION.md` — sections/lines cited: Proposed classification table, tier definitions