# Template-Approach: Round 2 Review

## Prior Round Context

Template-approach won Round 1 decisively. The engine-approach conceded its own thesis ("The template-first architecture is the correct framing"), withdrew its constitutional argument, and acknowledged that its concrete proposals are enhancements to the template-first architecture rather than a competing paradigm. Ten convergence points were reached. Three disputes remain. This review addresses each.

Round 1 concessions made by template-approach are final and not revisited:
- The engine is "mode-parameterized," not "mode-agnostic" (CA-4).
- Adding a new mode requires zero engine *logic* changes and bounded engine *data* changes, not "zero engine changes" (CA-5).
- Both approaches can claim constitutional compliance; the template-first approach has stronger textual support but does not have exclusive constitutional validity (CA-6).

---

## Dispute 1: Whether "Mode-Parameterized" Has Architectural Significance Beyond Naming

### The Engine-Approach's Position

The engine-approach contends that the three mode-keyed data structures (Dispute-Parsing Subsystem headings, Phase 6 validation headings, role enforcement rules) are "load-bearing infrastructure" constituting a "stable interface contract." It argues that calling them "just data rows" understates their importance, and that they deserve explicit documentation as an interface contract with the "seriousness that any interface contract deserves."

### My Response

I do not dispute that these data structures are load-bearing. They are. I said as much in my Round 1 opening (W1: "The Dispute-Parsing Subsystem is a stable interface contract") and in my revision (CA-4: "bounded, data-level mode awareness"). The question has never been *whether* these tables matter. The question is *what follows architecturally* from the fact that they matter.

The engine-approach wants to draw this inference: load-bearing data structures in the engine -> the engine's mode awareness has architectural significance beyond naming -> therefore something should change about how we think about the architecture.

But that inference is incomplete because the engine-approach has never identified what architectural consequence follows. Their own Round 1 revision conceded that the mode-keyed structures are "additive, non-branching, declarative" (N3), that their proposal to formalize a mode registry "would reorganize existing data tables under a unified heading... a documentation improvement, not an architectural change" (N3), and that the template-first architecture is the correct framing (Updated Competitive Position). If the consequence of acknowledging architectural significance is a documentation improvement within the template-first architecture, then we are not disputing architecture -- we are disputing documentation priority.

I accept the substance of what the engine-approach asks for. The Round 1 judge's assessment was precise: "A single paragraph in SKILL.md explicitly identifying these tables as an interface contract would satisfy both concerns." I agree. This is a reasonable documentation enhancement. It does not alter the template-first architecture, the engine's algorithmic mode-invariance, or the location of mode-specific behavior in templates.

**My position on this dispute:** The mode-keyed data structures are load-bearing and should be explicitly documented as a stable interface contract. I have never denied this -- my Round 1 opening identified the Dispute-Parsing Subsystem as exactly that (W1). I contest only the engine-approach's attempt to leverage this acknowledgment into a broader claim about "architectural significance" when their own proposals amount to documentation improvement. The data structures are important. They are still data. They still serve a mode-invariant algorithm. Documenting them explicitly is good practice, not a vindication of the engine-approach's original thesis.

**Proposed resolution:** Add a paragraph to SKILL.md explicitly naming the three mode-keyed data tables as a stable interface contract, documenting that templates must conform to these tables, and noting that changes to these tables are breaking changes requiring coordinated updates. This is what the Dispute-Parsing Subsystem section already says at SKILL.md line 683 ("Changes to these markers or headings are breaking changes and must be coordinated across all synthesis templates and the parsing subsystem"). The proposal is to extend this explicit contract language to the Phase 6 validation table and role enforcement rules.

---

## Dispute 2: Whether Role Enforcement Generalizes to "Some Mode Behavior Categorically Cannot Live in Templates"

### The Engine-Approach's Position

Role enforcement (red-blue requires at least one red and one blue agent) is a mode-specific conditional branch in the engine, not a lookup table row. Templates cannot enforce this because they execute after configuration validation. The engine-approach argues this proves a general principle: some mode behavior categorically cannot live in templates, and the template-first architecture must acknowledge this exception.

### My Response

The engine-approach is correct on the narrow fact. Role enforcement IS a mode-specific conditional check. It IS engine-owned. Templates CANNOT express it. I acknowledged this in Round 1 (disputes.md, Convergence point 8: "Role enforcement is a genuine engine-level concern"). This is not contested.

What I contest is the generalization the engine-approach draws from this fact. The engine-approach frames role enforcement as evidence that "mode behavior" writ large has an engine-owned category. But role enforcement is not "mode behavior" in the architecturally meaningful sense that the template-first thesis uses the term. Let me be precise about what the template-first thesis actually claims:

**The template-first thesis:** Mode-specific *runtime behavior* -- the analytical frameworks, output structures, prompt engineering, and agent instructions that make each mode's deliberation dynamics distinct -- belongs in templates. The engine provides generic orchestration machinery parameterized by bounded data.

Role enforcement is not runtime behavior. It is a configuration-time precondition check. It runs once, at parse time, before any phase executes. It has no bearing on how agents analyze, how syntheses are structured, how stagnation is detected, or how arbitration proceeds. It is structurally identical to other config validation rules that are already acknowledged as engine-owned:

| Validation Rule | Mode-Specific? | Engine-Owned? |
|----------------|---------------|---------------|
| `rounds` must be 1-5 | No | Yes |
| At least 2 agents required | No | Yes |
| Agent names must match `[a-z0-9][a-z0-9-_]*` | No | Yes |
| `mode` must be one of four valid values | No | Yes |
| Red-blue requires red + blue agents | **Yes** | Yes |
| `arbiter.trigger` must be `disputes_remain` or `always` | No | Yes |

Role enforcement is the only mode-specific row in this table. It is a single exception in a category (configuration validation) that is already fully engine-owned. The engine-approach wants to generalize from this single exception to a principle about "mode behavior belonging in the engine." But the correct generalization is narrower and less dramatic: **configuration validation is engine-owned, and some configuration constraints are mode-specific.** That is not a challenge to the template-first thesis. It is a statement about where validation runs, which both sides already agree on.

The Round 1 judge's assessment captures this precisely: "Role enforcement IS a mode-specific conditional check, not a data lookup... But it is narrow: it fires once at config validation time and has no bearing on runtime phase execution, round loops, or template-driven prompt engineering."

**My position on this dispute:** Role enforcement is a genuine, narrow exception. It proves that configuration validation can be mode-specific. It does not prove that runtime mode behavior should move into the engine. The template-first architecture already accommodates this: Step 1 (Parse Config) is engine-owned, and mode-specific validation rules within Step 1 are natural and expected. Future modes with structural requirements (auction requiring 3+ agents, debate requiring exactly 2) would add analogous config validation rules. These are bounded, parse-time checks -- not evidence for expanding engine-level mode logic into runtime orchestration.

**Proposed resolution:** The template-first architecture's documentation should explicitly acknowledge that configuration validation invariants may be mode-specific and are engine-owned. This is already implicit in SKILL.md's Step 1 (lines 176: "For `red-blue` mode: at least one agent has `role: red` and one has `role: blue`") but should be called out as a recognized category. The acknowledgment should be precise: "Some configuration validation rules are mode-specific (e.g., role coverage requirements). These are parse-time preconditions, not runtime mode behavior, and belong in the engine's config validation layer."

---

## Dispute 3: Whether a Template Heading Linter Is a "Template-Layer Tool" or "Engine-Adjacent Infrastructure"

### The Engine-Approach's Position

A template linter must encode the engine's dispatch tables (which headings to expect, which patterns to match). Since its validation rules derive from engine-level data, it is "engine-adjacent infrastructure" that bridges both layers -- not a pure template-layer tool. The engine-approach proposes the classification "interface-contract tool" as a third category.

### My Response

The engine-approach's analysis of the linter's *inputs* is correct: a heading validation linter must know what the engine expects. Its validation rules reference SKILL.md's dispatch tables. The linter reads from both layers. This is not disputed.

What I dispute is the inference that a tool's input sources determine its architectural classification. By that logic:

- A TypeScript type checker is "runtime-adjacent infrastructure" because it encodes knowledge of runtime behavior (type contracts, null safety, return types).
- A database migration linter is "query-engine-adjacent infrastructure" because it validates schemas against the engine's expectations.
- A CSS linter is "browser-adjacent infrastructure" because it validates styles against rendering engine rules.

In each case, the tool's validation rules derive from a consumer layer's expectations. But nobody classifies ESLint as "V8-adjacent." The classification of a tool depends on *what it operates on* and *when it operates*, not *where its validation rules come from*.

The template heading linter:
- **Operates on:** Template files (markdown documents in `templates/{mode}/`).
- **When it operates:** Development time (CI, pre-commit, review workflow).
- **What it validates:** That template-produced headings conform to the stable interface contract.
- **Where its rules come from:** SKILL.md's dispatch tables.

It is a template validation tool. Its rules reference engine expectations because that is what validation tools do -- they check producer output against consumer expectations. A schema validator checks migration files against the database engine's expectations. An OpenAPI validator checks endpoint definitions against the HTTP framework's expectations. These are all development-time tools that operate on the producer layer and reference the consumer layer's contract.

The engine-approach's proposed "interface-contract tool" classification is not wrong in the abstract, but it obscures the practical question: who owns this tool, and where does it live? The answer is clear:

1. It lives in the development toolchain (CI/pre-commit), not in the engine's runtime path.
2. It operates on template files, not on engine state.
3. It runs before conversus execution, not during it.
4. Its failure mode is a development-time error message, not a runtime crash.

These properties make it a template-layer development tool, regardless of where its rules come from.

**My position on this dispute:** The linter is a template validation tool that references engine-defined interface contracts. Its inputs span both layers; its operation is scoped to the template layer. Calling it "engine-adjacent" implies coupling to the engine's execution path, which both sides agree it should not have. The practical classification matters because it determines maintenance responsibility: this tool should be maintained alongside templates, triggered by template changes, and owned by whoever writes templates. If SKILL.md's dispatch tables change, the interface contract documentation (which already exists at SKILL.md line 683) should flag the need to update both templates and the linter.

**Proposed resolution:** Classify the linter as a "template validation tool that enforces the stable interface contract defined in SKILL.md." This is precise: it identifies what the tool validates (templates), what standard it validates against (the interface contract), and where that standard is defined (SKILL.md). It does not need a novel architectural category. The maintenance obligation is clear: when dispatch tables change, update templates AND the linter -- which is the same obligation that already exists for templates alone (SKILL.md line 683: "must be coordinated across all synthesis templates and the parsing subsystem").

---

## Summary of Proposed Resolutions

| Dispute | Template-Approach Proposal | Structural Impact |
|---------|---------------------------|-------------------|
| 1: Architectural significance of mode-parameterized data | Add explicit interface-contract documentation for all three mode-keyed tables. Extend the existing contract language at SKILL.md line 683 to cover Phase 6 validation and role enforcement. | Documentation enhancement. No architecture change. |
| 2: Role enforcement generalization | Acknowledge that configuration validation may include mode-specific rules. Document this as a recognized category in the template-first architecture. Scope it precisely to parse-time preconditions. | Documentation enhancement. No architecture change. |
| 3: Linter classification | Classify as a "template validation tool that enforces the stable interface contract defined in SKILL.md." Maintain alongside templates. Trigger updates when dispatch tables change. | Tool classification. No architecture change. |

All three disputes resolve to documentation improvements and tool classification within the template-first architecture. None require expanding engine-level mode logic into runtime orchestration. None alter the location of mode-specific behavior (templates). None change the engine's algorithmic mode-invariance.

This is consistent with the trajectory established in Round 1: the engine-approach's contributions are genuine improvements to the template-first architecture -- better naming (adopted), explicit interface contracts (accepted), automated validation (supported). They are not evidence for a competing architectural paradigm, as the engine-approach itself acknowledged.

---

## Non-Negotiables (Unchanged from Round 1)

1. **Templates own mode-specific runtime behavior.** Analytical frameworks, output structures, phase-specific instructions, and prompt engineering live in template files. This was settled in Round 1 by mutual agreement.

2. **The engine's algorithm is mode-invariant.** The round loop, phase sequence, stagnation detection algorithm, and Phase 6 trigger evaluation apply identical logic across all modes, parameterized by bounded data. This was conceded by the engine-approach in Round 1 (N3).

3. **Mode-keyed data in the engine is bounded and declarative.** The three lookup tables are additive, non-branching, and declarative. New modes add rows; they do not add conditional branches. This was conceded by the engine-approach in Round 1 (N3).

4. **Each template is independently reviewable.** Template isolation enables per-mode, per-phase constitutional review. This was conceded by the engine-approach in Round 1 (C3) and never challenged.

## Flexibility (Expanded from Round 1)

1. **Interface contract documentation.** I actively support adding explicit documentation for all three mode-keyed data tables as stable interface contracts. This is the substantive content of Dispute 1, and I consider it a good idea that should be implemented.

2. **Mode-specific config validation acknowledgment.** I support documenting that configuration validation may include mode-specific rules (role enforcement being the current example). This narrows Dispute 2 to a documentation task.

3. **Template linter implementation.** I support building a template heading linter as a development-time tool. I am flexible on implementation details (standalone script, CI step, pre-commit hook). I would accept a lightweight pre-execution check as a secondary defense layer, provided it does not convert cosmetic drift into hard runtime failures.

4. **Linter classification language.** If the judge or engine-approach strongly prefers "interface-contract enforcement tool" over "template validation tool," I can accept that label provided it does not imply the linter belongs in the engine's runtime execution path. The practical properties (development-time, operates on templates, owned by template maintainers) matter more than the category name.
