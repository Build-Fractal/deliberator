# Engine-Approach: Round 2 Review

**Context**: Round 2 of 3 in a winner-take-all deliberation on spec 004 (Universal Rounds, Stagnation Detection, and Arbitration). I lost Round 1; the judge acknowledged role enforcement as my strongest surviving point. This review addresses the 3 remaining disputes from Round 1 and proposes that my enhancements be adopted within the template-first framework, which I conceded is the correct architecture.

**Standing concessions (not reversed)**: The template-first architecture is the correct framing. My proposals are enhancements, not a competing paradigm. The constitutional argument (Principle VI) is withdrawn. The game-theory argument supports template-first. The data-vs-logic distinction is architecturally substantive. The engine's mode awareness is lookup tables, not conditional branches. FR-001's direction of change supports template-first. "Just add templates plus bounded data rows" is approximately accurate.

---

## Dispute 1: Whether "Mode-Parameterized" Has Architectural Significance Beyond Naming

### Round 1 Summary

The judge assessed that "both sides are partially right" -- the mode-keyed data structures ARE load-bearing but ARE bounded data rather than conditional logic. The judge proposed "a single paragraph in SKILL.md explicitly identifying these tables as an interface contract would satisfy both concerns."

### My Round 2 Position

I accept the judge's assessment and propose the concrete resolution it implies.

The template-approach's concern is that elevating "mode-parameterized" to architectural significance creates a wedge for future engine expansion. I understand this concern and withdraw any framing that treats the relabeling as an architectural discovery. It is a naming correction that reflects a real structural property.

But the template-approach's counter-position -- that the relabeling is "just documentation" -- understates the operational consequence. Consider what happens when a new mode is added. The spec's own Section 6 ("Implementation Notes") lists the engine changes: remove validation if-statements, add Phase 6 heading rows, verify variable population. This is accurate for spec 004 because the three existing modes already had Dispute-Parsing Subsystem entries. A genuinely new fifth mode would also require a new Dispute-Parsing row. Today, that requirement is implicit -- scattered across three separate subsections of SKILL.md. A contributor adding a new mode must discover each table independently. If they miss one, the system fails silently: stagnation detection returns the default `true` (as specified in SKILL.md line 679: "Return `true` (has disputes) as a safety measure"), Phase 6 validation misses required sections, or role constraints go unenforced.

The fix is exactly what the judge proposed: a single paragraph (or short section) in SKILL.md that explicitly names the three mode-keyed tables as a stable interface contract and states that any new mode must add entries to all three. This is not engine expansion. It is documentation of what already exists. It does not add conditional branches. It does not move mode behavior into the engine. It makes explicit what is currently implicit, reducing the risk of silent failure when the system scales.

**Concrete proposal**: Add to SKILL.md's "Important Notes" section a subsection titled "Mode Interface Contract" containing:

1. A list of the three mode-keyed tables (Dispute-Parsing Subsystem headings, Phase 6 validation headings, role enforcement rules).
2. A statement that these tables constitute the stable interface between the engine and templates.
3. A checklist: when adding a new mode, add entries to all three tables and create the mode's template directory.

This is a documentation change. It preserves the template-first architecture. It adds zero conditional branches. It costs one paragraph. The template-approach should find nothing objectionable here because it formalizes what both sides already agree is true.

**Resolution I propose**: Dispute 1 is resolved by the judge's own recommendation. The terminology "mode-parameterized" is adopted (already agreed). The architectural significance question is answered pragmatically: the mode-keyed tables are important enough to document as an interface contract, not important enough to restructure the architecture around. Both sides should accept this.

---

## Dispute 2: Whether Role Enforcement Generalizes to "Some Mode Behavior Categorically Cannot Live in Templates"

### Round 1 Summary

The judge assessed that I have "the stronger argument on the specific fact (role enforcement IS a mode-specific conditional check, not a data lookup)" but the template-approach has "the stronger argument on scope (this is a config-parse-time validation concern, not evidence that analytical frameworks or output structures should move into the engine)." The judge concluded: "The template-first architecture should acknowledge this exception explicitly without treating it as a wedge for expanding engine-level mode logic."

### My Round 2 Position

I accept the judge's scoping and withdraw the generalization. Let me be precise about what I am and am not claiming.

**What I am claiming**: Role enforcement is a mode-specific conditional check in the engine. It is not a lookup table row -- it is an `if mode == red-blue, then validate(agents have red and blue roles)` branch. This is the one place in the engine where the algorithm genuinely varies by mode, rather than merely being parameterized by mode data. Future modes with structural preconditions (e.g., an auction mode requiring a minimum bidder count) would need analogous checks. This category of engine-owned mode behavior exists and should be acknowledged.

**What I am NOT claiming**: I am not using role enforcement as a wedge to argue that analytical frameworks, output structures, or prompt engineering should move into the engine. The judge correctly identified this overreach in my Round 1 position, and I withdraw it. Role enforcement is a config-parse-time concern. It fires once, before any template loads, and has no bearing on runtime phase execution. It does not generalize to "mode behavior belongs in the engine."

**What I propose**: The template-first architecture's description of itself should include an explicit acknowledgment that configuration validation invariants are engine-owned. This is not a concession from the template-approach -- they already agreed in their Round 1 disputes (Convergence point 8: "Role enforcement is a genuine engine-level concern"). It is a request that this acknowledgment appear in the system's self-documentation rather than remaining an informal consensus.

Specifically, the "Mode Interface Contract" section I proposed for Dispute 1 should include a fourth item: mode-specific configuration validation rules (currently: red-blue role coverage). This keeps the acknowledgment bounded and explicit. It does not open the door to engine-level mode logic because configuration validation is, by both sides' agreement, a separate architectural layer from runtime orchestration.

**The template-approach's analogy to `rounds` validation**: The template-approach argued that role enforcement is "structurally identical to validating that `rounds` is a positive integer." I dispute this analogy while accepting the template-approach's architectural conclusion. Validating that `rounds` is a positive integer is mode-invariant -- the same check applies regardless of mode. Role enforcement is mode-specific -- it applies only to red-blue mode. This makes role enforcement categorically different from generic config validation, even though both execute at config-parse time. The category difference is factual, but I agree with the template-approach (and the judge) that it does not carry architectural weight beyond documentation.

**Resolution I propose**: Dispute 2 is resolved by adopting the judge's scoping. Role enforcement is a genuine, narrow, engine-owned mode-specific concern. It does not generalize to analytical frameworks or output structures. The template-first architecture explicitly acknowledges this exception in its self-documentation. Both sides already agree on the facts; the dispute is about documentation framing, which is exactly what a "Mode Interface Contract" section resolves.

---

## Dispute 3: Whether a Template Heading Linter Is a "Template-Layer Tool" or "Engine-Adjacent Infrastructure"

### Round 1 Summary

The judge assessed that "the engine-approach's classification is more precise" -- a linter that validates template headings against SKILL.md's dispatch tables "necessarily encodes knowledge from both layers." However, the judge also noted "this classification has no practical impact on where the linter runs (development time, both sides agree) or how it is implemented. This is a categorization question, not an architectural one."

### My Round 2 Position

I accept the judge's assessment that this is a categorization question with no practical impact. Given this, I propose we resolve it pragmatically rather than continuing to debate the taxonomy.

**The operational concern**: Whether we call the linter a "template tool," an "engine-adjacent tool," or an "interface-contract tool," the maintenance obligation is the same. When SKILL.md's Dispute-Parsing Subsystem headings change, the linter's validation rules must update. When a template's output headings change, the linter must verify they still match. The linter has dependencies in both directions. This is the factual basis for my Round 1 classification as "interface-contract enforcement," and the judge agreed it is "more precise."

**Why precision matters even without practical impact**: The template-approach argues the linter is a "development tool, like a schema validator or a type checker." I agree with this analogy -- but note that schema validators are classified by what they validate, not by when they run. A JSON Schema validator is not a "JSON tool" or an "application tool" -- it is a schema-contract enforcement tool. Similarly, a template heading linter is an interface-contract enforcement tool. Calling it a "template tool" implies its validation rules are self-contained within the template layer. They are not. Its rules derive from SKILL.md's dispatch tables. This matters for one practical reason: maintenance discoverability. When a maintainer updates the Dispute-Parsing Subsystem headings in SKILL.md, they need to know that the linter's rules must also update. If the linter is classified as a "template tool," a maintainer working in SKILL.md has no reason to look for it.

**Concrete proposal**: Rather than debating taxonomy, I propose we define the linter's specification in terms that make the dual dependency explicit, regardless of where it is classified:

1. **Validation source**: The linter reads its expected headings from SKILL.md's mode-keyed tables (Dispute-Parsing Subsystem headings and Phase 6 validation headings).
2. **Validation target**: The linter checks template output sections against those expected headings.
3. **Change coupling**: The linter's specification should state that changes to either SKILL.md's dispatch tables or template output sections require re-running the linter. This makes the bidirectional dependency explicit.

Whether this linter lives in a `tools/` directory, a `templates/lint/` directory, or a CI pipeline is a project-structure decision that neither the engine-approach nor the template-approach needs to resolve now. The architectural question -- where the linter's validation rules come from -- is answered: they come from the interface contract between engine and templates.

**Resolution I propose**: Dispute 3 is resolved by agreeing on the linter's specification rather than its categorization. The judge already ruled that categorization has no practical impact. Both sides agree the linter is needed. Both sides agree it runs at development time. The bidirectional dependency (linter reads from SKILL.md dispatch tables, validates against template outputs) should be explicit in the linter's specification. Whether we call it a "template tool" or an "interface-contract tool" is a labeling preference that each side can hold without further deliberation cost.

---

## Summary: Three Enhancements to the Template-First Architecture

All three disputes resolve into concrete enhancements that strengthen the template-first architecture without altering it:

| Dispute | Proposed Resolution | Type of Change |
|---------|---------------------|----------------|
| 1. "Mode-parameterized" significance | Add "Mode Interface Contract" section to SKILL.md documenting the three mode-keyed tables | Documentation |
| 2. Role enforcement generalization | Acknowledge config-validation invariants as engine-owned in the interface contract section; do not generalize to runtime mode behavior | Documentation |
| 3. Linter classification | Define the linter's spec with explicit bidirectional dependency on SKILL.md dispatch tables and template outputs; defer categorization | Specification |

None of these proposals add conditional branches to the engine. None move analytical frameworks or prompt engineering out of templates. None contradict the template-first architecture. They are maintenance-quality improvements that make implicit contracts explicit, reducing the risk of silent failure as the system scales to new modes.

The template-first architecture is correct. These enhancements make it more robust.

---

## Competitive Position

I am not arguing that the template-approach is wrong. I am arguing that the template-first architecture, as documented today, has three documentation gaps that create silent-failure risks:

1. The mode-keyed tables are not identified as an interface contract.
2. The engine's config-validation exceptions are not acknowledged in the architecture's self-description.
3. The heading linter's bidirectional dependency is not specified.

These gaps are not hypothetical. The heading drift caught during Round 1's constitutional review (two templates using `### Remaining Contested Positions` instead of `### Remaining Disputes`) is exactly the kind of silent failure that explicit interface-contract documentation prevents.

If the template-approach accepts these three documentation enhancements, the remaining disputes are fully resolved and the deliberation can converge. If the template-approach rejects them, I ask the judge to evaluate whether the rejection is substantive (the enhancements are harmful) or territorial (acknowledging engine-layer obligations feels like conceding ground). The enhancements are compatible with every position the template-approach holds. They are, in fact, the natural completion of the template-first architecture's own self-documentation.
