# Engine-Approach: Final Statement (Winner-Take-All)

## Remaining Disputes

**Dispute: The term "mode-parameterized" understates the architectural significance of engine-level mode awareness.**

The template-approach proposes "mode-parameterized" as the replacement for "mode-agnostic," and I adopted this terminology in my revision. But the template-approach then uses "parameterized" to minimize the significance: parameterization is "just data," data is "just configuration," therefore the engine's mode awareness is trivially bounded and architecturally insignificant.

This framing elides a real concern. Three mode-keyed data structures (Dispute-Parsing Subsystem, Phase 6 validation headings, role enforcement rules) constitute a stable interface contract between engine and templates. If a template violates this contract -- produces headings the engine does not recognize -- the system fails silently (stagnation detection returns 0 disputes, Phase 6 validation misses required sections). The engine's mode awareness is not cosmetic. It is load-bearing infrastructure that determines whether the system produces correct results. Calling it "just data" risks treating it as incidental rather than essential.

The template-approach's database analogy -- "a query engine parameterized by schema metadata" -- actually supports my concern. Schema metadata in a database is rigorously validated, version-controlled, and enforced at both definition time and query time. Nobody dismisses schema metadata as "just data rows." The mode-keyed tables in SKILL.md deserve the same treatment: explicit documentation as a stable interface contract, not casual minimization as bounded configuration.

I am not disputing the label "mode-parameterized." I am disputing the inference the template-approach draws from it: that data-level mode awareness is architecturally negligible. It is not negligible. It is the mechanism by which the engine validates template output, and it should be documented and maintained with the seriousness that any interface contract deserves.

---

**Dispute: Role enforcement proves that some mode behavior categorically cannot live in templates.**

The template-approach revision did not rebut this point. Role enforcement -- requiring that a red-blue session includes at least one `role: red` agent and one `role: blue` agent -- is a mode-specific validation rule that executes before any template is loaded. Templates cannot express or enforce this invariant. A misconfigured `conversus.yml` with all-red agents and no blue agents would produce a structurally broken deliberation that no template could recover from.

This is not a "bounded data addition." It is a mode-specific behavioral rule in the engine: "if mode is red-blue, then the agent list must satisfy a role-coverage constraint." This is a conditional branch, not a lookup table row. It is engine logic that varies by mode.

The template-approach's thesis -- that mode behavior lives in templates and the engine provides generic machinery -- has a categorical exception here. Some mode invariants are preconditions that must be enforced before templates execute. Any future mode with structural requirements (e.g., an auction mode requiring a minimum number of competing bidders) would need analogous engine-level enforcement. The template-first architecture must acknowledge this category of engine-owned mode behavior rather than treating the engine as a passive executor of template instructions.

---

**Dispute: A template linter is engine-adjacent infrastructure, not a pure template-layer concern.**

The template-approach proposes a development-time template linter as the solution to heading drift. I agree a linter is better than runtime validation (earlier detection, cheaper failure). But I dispute the framing that a linter is a "template-first enhancement" that keeps validation in the template layer.

A template linter must encode the stable interface contract: which headings the engine expects, which entry patterns the Dispute-Parsing Subsystem matches, which required sections Phase 6 validation checks. This knowledge lives in SKILL.md today. A linter that validates templates against SKILL.md's dispatch tables is, by definition, encoding engine-level expectations into a validation tool. It is engine-adjacent infrastructure regardless of when it runs.

The template-approach and I agree that automated enforcement is needed. But calling the linter a "template-layer" tool obscures where its validation rules come from: the engine's mode-keyed dispatch tables. The linter is a bridge between the engine layer and the template layer. Classifying it as belonging to either layer alone is imprecise.

This dispute is narrow and practical, not architectural. Both sides want the same thing (automated heading validation). The disagreement is only about honest classification: is this a template tool, an engine tool, or an interface-contract tool? I argue the third.

---

## Convergence

The following positions are agreed between both approaches:

1. **The template-first architecture is the correct framing.** I concede this explicitly. My revision states: "The template-first architecture is the correct framing. The engine-approach's original thesis -- that mode behavior belongs in the engine -- overstated what is actually a narrow, data-level mode awareness in the engine that supports (rather than replaces) the template-first architecture." The template-approach's cross-review correctly identified that my concrete deliverables amount to enhancements within the template-first paradigm, not a competing architecture.

2. **The engine is mode-parameterized, not mode-agnostic.** Both sides now use this terminology. The template-approach withdrew "mode-agnostic" in their CA-4 revision. The engine maintains bounded, data-level mode awareness through lookup tables whose algorithm is mode-invariant. This is a precise and defensible description.

3. **Mode-specific behavior (analytical frameworks, output structures, prompt engineering) belongs in templates.** The constitutional basis is clear: Principle VIII explicitly places mode-specific behavior in templates. I withdrew my constitutional counter-argument in Advantage 4 of my revision. Templates are the correct abstraction for content variation across modes.

4. **Orchestration logic (phase sequence, round loop, stagnation algorithm, termination checks) belongs in SKILL.md as deterministic rules.** Both sides agree the engine owns orchestration. The dispute was about whether the engine's mode-keyed data tables constitute "mode-specific behavior" (template territory) or "orchestration parameterization" (engine territory). Both sides now agree it is the latter: orchestration parameterized by mode data.

5. **Adding a new mode requires zero engine logic changes and bounded engine data additions.** The template-approach revised their "zero engine changes" claim to this more precise formulation. I conceded in N2 of my revision that the data additions (one dispatch-table row, one validation-table row, one enum entry) are lightweight, additive, and non-breaking. This IS meaningfully different from adding conditional branches.

6. **Each template is independently reviewable and testable against constitutional principles.** I conceded this in my original cross-review (C3) and maintain the concession. This is a genuine structural benefit of the template architecture.

7. **FR-001's direction of change moved the engine toward less mode-awareness, not more.** The spec removed two mode-specific validation gates (cooperative-only restrictions on rounds and arbiter). The implementation deleted conditional branches rather than adding them. This moved in the template-first direction.

8. **The data-vs-logic distinction has architectural substance.** I conceded in N3 of my revision that lookup tables (additive, non-branching, declarative) are categorically different from conditional branches (potentially interfering, requiring exhaustive path testing, imperative). The engine's mode awareness is genuinely the former.

9. **Automated heading validation is needed.** Both approaches identified the heading drift in cross-round synthesis templates as a real risk. Both propose automated enforcement. The template-approach favors a development-time linter; I originally proposed runtime engine validation but conceded in Advantage 6 of my revision that a linter catches drift earlier and cheaper.

10. **The Dispute-Parsing Subsystem uses a single algorithm parameterized by mode-keyed data, not mode-specific conditional logic.** I conceded this in Advantage 1 of my revision. The algorithm (count disputes by heading, compare to prior count, decide stagnation) is uniform across modes. Only the heading string and entry pattern vary.

---

## Final Position Statement

### Non-Negotiables

1. **The engine's mode-parameterized data structures constitute a stable interface contract that must be explicitly documented and maintained as such.** These are not incidental configuration. They are the mechanism by which the engine validates template output, detects stagnation, and enforces structural preconditions. Any documentation or architecture description that minimizes them as "just data rows" risks treating essential infrastructure as incidental detail. The spec and SKILL.md should contain an explicit "Interface Contract" section that names these tables, their purpose, and the obligation on templates to conform to them.

2. **Role enforcement is engine-owned mode behavior that templates cannot replicate.** This is a categorical fact, not a matter of framing. Some mode invariants are preconditions that must hold before templates execute. The template-first architecture should acknowledge this category explicitly rather than implying that all mode behavior lives in templates without exception.

3. **Automated heading validation -- however implemented -- must encode knowledge from both the engine layer (dispatch tables) and the template layer (output headings).** Classifying this validation as belonging purely to the template layer is imprecise. It is interface-contract enforcement, bridging both layers. This matters for maintenance: when SKILL.md's dispatch tables change, the validation tool must update in lockstep, and vice versa.

### Flexibility

1. **I concede the template-first architecture as the correct overall framing.** My concrete proposals (formalize mode registry, add validation) are enhancements to the template-first architecture, not a competing paradigm. I withdraw any framing that positions the engine-approach as an alternative architecture.

2. **I am flexible on where automated heading validation runs.** A development-time linter, a CI check, or a pre-execution validation step are all acceptable. I withdraw the claim that it must be runtime engine-level validation. Earlier detection is better.

3. **I am flexible on the exact documentation structure for the mode registry.** Whether the three existing lookup tables are consolidated into one "Mode Registry" section or remain in their current named subsections is a documentation choice. The substance -- that these tables are explicitly identified as a stable interface contract -- matters more than the formatting.

4. **I accept that the "data vs. logic" distinction accurately describes the engine's current mode awareness.** The engine's mode-keyed structures are additive, non-branching, and declarative. They are data parameterization for a generic algorithm, not conditional logic. My original framing overstated their architectural significance as "mode-specific orchestration logic."

5. **I support the template-approach's proposal to use the term "mode-parameterized" throughout.** This is accurate and defensible. I withdraw "mode-aware" as potentially overstating the degree of engine-level mode coupling.
