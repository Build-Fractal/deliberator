# Template-First Approach: Revised Position

## Competitive Advantage Classification

### CA-1: "The Implementation Proves the Architecture" — Modified

**Original claim**: Four SKILL.md edits vs. six template files; the engine barely changed; templates did all the work.

**Engine-approach challenge**: The four edits were preconditions without which templates would be inert text. The Dispute-Parsing Subsystem, Phase 6 validation table, and role enforcement already existed as engine-level mode awareness. The engine did not need to change much because its mode-aware infrastructure was already built, not because the engine is mode-agnostic.

**Modified position**: I withdraw the rhetorical framing that minimizes the engine edits as "just four changes." The engine-approach is right that these edits were necessary preconditions, not housekeeping. However, the structural argument survives: the nature of those four edits was *removing restrictions* (FR-001: deleting two validation `if` statements) and *adding data rows* (FR-009: adding four rows to a heading table). These are configuration-level changes — removing gatekeeping rules and extending a lookup table — not algorithmic changes to orchestration logic. The engine's algorithm (parse synthesis, count disputes, compare counts, decide termination) did not change for any mode. What changed was which strings to look up. The implementation still proves that mode-specific *behavior* — the analytical frameworks, output structures, and prompt engineering that make each mode distinct — lives in templates. The engine provides generic machinery parameterized by bounded data.

---

### CA-2: "Templates Are the Right Abstraction for Mode Behavior" — Surviving

**Original claim**: What differs across modes is content (analytical frameworks, output sections), not orchestration (phase sequence, round loop, stagnation algorithm). Templates are the correct abstraction for content variation.

**Engine-approach challenge**: Two kinds of mode behavior exist — prompt engineering (templates) and orchestration semantics (engine). The engine's mode-keyed dispatch tables for dispute parsing and output validation are "orchestration semantics," not just data.

**Surviving position**: The engine-approach's taxonomy of "prompt engineering vs. orchestration semantics" is reasonable in the abstract but does not describe the actual system accurately. The "orchestration semantics" that differ per mode in SKILL.md are: (1) which heading string to search for, (2) which entry pattern string to count, and (3) which heading strings to validate in Phase 6 output. All three are string lookups from a four-row table. The algorithm applied to those strings — search, count, compare, decide — is identical across all modes. This is parameterized data for a generic algorithm, not mode-specific orchestration logic in any meaningful sense.

The database analogy from my opening argument holds: a query engine that uses different column names per table is table-parameterized, not table-specific. The engine-approach's rebuttal — "a database engineer would say their engine IS table-aware" — is true at the level of naming, but misses the architectural point. The database engine's *logic* does not change per table. Its *data* (schema metadata) changes per table. The conversus engine's *logic* does not change per mode. Its *data* (heading strings) changes per mode. This distinction between data-level parameterization and logic-level branching is architecturally significant. It is why adding a new mode requires adding data rows, not writing new conditional branches.

---

### CA-3: "Each Template Is Independently Reviewable and Testable" — Surviving

**Original claim**: Templates can be reviewed against constitutional principles independently. If mode behavior lived in engine logic, interleaved conditional branches would make independent review impossible.

**Engine-approach concession**: The engine-approach conceded this point explicitly in their cross-review (C3): "Template-approach correctly notes (Strength 3) that each template can be reviewed against constitutional principles independently. This is a genuine benefit of the template architecture."

**Surviving position**: This advantage is unchallenged. Each template file is a self-contained unit of mode behavior for one phase, reviewable in isolation against all nine constitutional principles. The constitution compliance review demonstrated this concretely. This reviewability property is a direct consequence of the template-first architecture and would degrade under any approach that distributes mode behavior across engine conditional branches.

---

### CA-4: "The Engine Stays Simple" — Modified

**Original claim**: The engine is mode-agnostic. It knows `{mode}` only as a path selector for templates and as a key for the Phase 6 validation heading table.

**Engine-approach challenge**: The engine contains three mode-keyed lookup tables (Dispute-Parsing Subsystem, Phase 6 validation, role enforcement) plus mode-specific template path resolution. Calling this "mode-agnostic" stretches the definition past usefulness.

**Modified position**: I withdraw the unqualified claim that the engine is "mode-agnostic." The engine is **mode-parameterized**: it maintains bounded, data-level mode awareness in the form of lookup tables, but its algorithmic logic is mode-invariant. The distinction matters. "Mode-agnostic" implies the engine has no knowledge of modes, which is false — SKILL.md lines 674-677 list four mode-specific headings. "Mode-parameterized" accurately describes an engine whose logic is generic but whose data includes per-mode configuration. This is the architecture that shipped, and it is the architecture I defend.

The engine-approach's claim that this parameterization proves mode behavior "belongs in the engine" does not follow. The parameterization is bounded (three lookup tables totaling ~12 rows of data) and serves as an interface contract between the engine and the templates. Templates produce headings; the engine validates them. This is a producer-consumer contract, not evidence that producer logic should move into the consumer.

---

### CA-5: "Adding New Modes Requires Zero Engine Changes" — Modified

**Original claim**: A fifth mode requires zero orchestration logic changes — just templates, one enum entry, and one table row.

**Engine-approach challenge**: Spec 004 itself required SKILL.md edits. A fifth mode would need at minimum three SKILL.md edits (Dispute-Parsing Subsystem row, Phase 6 validation row, mode enum entry), plus potentially role enforcement rules. "Zero engine changes" is empirically false.

**Modified position**: I withdraw the "zero engine changes" claim. It was imprecise. The accurate claim is: **adding a new mode requires zero engine *logic* changes and a bounded number of engine *data* changes.** Specifically:

1. One new row in the Dispute-Parsing Subsystem heading table (data)
2. One new row in the Phase 6 validation heading table (data)
3. One new entry in the mode validation enum (data)
4. Potentially one new role enforcement rule if the mode has role requirements (data)
5. New template files (content)

Items 1-4 are additive, non-breaking data additions. They do not modify existing rows or introduce conditional branches. They do not change the stagnation detection algorithm, the round loop, the phase execution sequence, or the agent dispatch model. The engine's *algorithm* is unchanged; its *configuration data* grows by a few rows.

This is categorically different from the engine-approach's implied alternative, where adding a mode would mean adding conditional branches to orchestration logic. The template-first architecture keeps mode addition in the data layer, which is precisely where it should be.

---

### CA-6: "Constitutional Alignment Is Explicit" — Modified

**Original claim**: Constitution Principle VIII mandates that mode-specific behavior is encoded in templates. The template-first approach is the only constitutionally compliant approach.

**Engine-approach challenge**: Principle VIII also says "Orchestration decisions (phase ordering, trigger evaluation, termination checks) are rule-based, not inferred. SKILL.md specifies deterministic logic." The engine-approach reads this as placing stagnation detection and Phase 6 trigger evaluation in SKILL.md as deterministic rules — which they already are. Principle VIII says "orchestration in SKILL.md, content in templates," not "all mode behavior in templates."

**Modified position**: The engine-approach's reading of Principle VIII is partially valid. Principle VIII does assign orchestration decisions to SKILL.md as deterministic rules. And stagnation detection and Phase 6 trigger evaluation ARE deterministic rules in SKILL.md — correctly so.

But the engine-approach overreaches when it uses this to argue for expanding the engine's mode awareness. The current system already satisfies Principle VIII on both sides:
- **Orchestration in SKILL.md**: Stagnation detection, trigger evaluation, termination checks — all rule-based, all in SKILL.md. Principle VIII is satisfied.
- **Mode-specific behavior in templates**: Analytical frameworks, output structures, prompt engineering — all in templates. Principle VIII is satisfied.

The question is whether the engine's existing mode-parameterized data (lookup tables) should be *expanded* into a formal mode registry with additional enforcement. Principle VIII does not speak to this. It says orchestration is rule-based (it is) and mode behavior is in templates (it is). The current architecture already satisfies both mandates. The engine-approach proposes additional formalization that goes beyond what Principle VIII requires, without constitutional basis for doing so.

I concede that my original claim — that template-first is "the only constitutionally compliant approach" — was too strong. Both approaches can be read as constitutionally compliant. The template-first approach satisfies Principle VIII as implemented; the engine-approach proposes a reorganization that Principle VIII neither mandates nor prohibits.

---

## New Arguments from Cross-Review

### NA-1: The Engine-Approach Is Not a Competing Architecture — It Is a Validation Enhancement to the Template-First Architecture

This is the strongest argument that emerged from the cross-review exchange, and I sharpen it here.

The engine-approach's concrete deliverables, as stated in their cross-review's "Updated Competitive Position," are:

1. **Acknowledge** that the engine is mode-aware — i.e., rename "mode-agnostic" to "mode-parameterized." (Naming change. I have now adopted this terminology in CA-4 above.)
2. **Formalize** the mode registry — consolidate the three existing lookup tables into one SKILL.md section. (Cosmetic reorganization. The tables already exist in named subsections.)
3. **Add engine-level template validation** — verify template headings against the stable interface contract at load time. (A testing/validation enhancement.)
4. **Keep templates for prompt engineering** — no change to what templates do. (Concession of the template-first architecture.)

Item 4 is an explicit concession that templates own mode-specific behavior. Items 1-3 are incremental improvements to the existing template-first system. None of them move mode behavior from templates to the engine. None introduce mode-specific conditional branches in orchestration logic. None change which layer is responsible for analytical frameworks, output structures, or agent instructions.

The engine-approach is the template-first architecture with better naming (which I accept) and a proposed validation layer (which I support as a future enhancement). It is not a competing architecture.

### NA-2: The Template Drift Finding Supports a Template Linter, Not Engine-Level Validation

The engine-approach's decisive evidence is the heading drift caught by the constitution review (winner-take-all used `### Remaining Contested Positions` instead of `### Remaining Disputes`; prisoners-dilemma used `### Remaining Disputed Boundaries` instead of `## Disputed Boundaries`).

The engine-approach proposes catching this at "load time" via engine validation. But consider the failure modes:

- **Under engine validation**: The conversus run starts, loads templates, checks headings, and fails with a validation error. The user must fix the template and re-run. The error is caught at runtime.
- **Under a template linter**: The heading mismatch is caught during development, before the template is committed. CI/review catches it. The user never encounters a runtime failure.

A template linter catches drift *earlier* (development time) and *cheaper* (no wasted runtime). Engine validation catches drift *later* (execution time) and *more expensively* (the user is waiting for results). The engine-approach proposes moving a development-time concern into the runtime path.

Furthermore, the specific drift instances were functionally harmless — the Dispute-Parsing Subsystem's heading matching is case-insensitive and uses substring matching (SKILL.md line 681). The heading `### Remaining Disputed Boundaries` would still match a check for `Disputed Boundaries`. Engine-level exact-string validation would convert this cosmetic deviation into a hard runtime failure — making the system more brittle, not more robust.

The correct solution is a template linter that validates headings against the stable interface contract at development time, integrated into the review workflow. This is fully compatible with the template-first architecture and does not require engine changes.

### NA-3: FR-001's Direction of Change Refutes the Engine-Approach Thesis

The engine-approach argues that spec 004's engine changes prove mode behavior belongs in the engine. But the direction of those changes tells the opposite story:

- FR-001 *removed* two mode-specific validation rules (`rounds > 1` restricted to cooperative; `arbiter` restricted to cooperative).
- Before spec 004, the engine was *more* mode-aware — it actively rejected non-cooperative modes from using rounds and arbitration.
- After spec 004, the engine is *less* mode-aware — it allows all modes to use rounds and arbitration without mode-specific gating.

The spec 004 implementation made the engine MORE mode-agnostic (or, in my revised terminology, more generically parameterized) by removing mode-specific conditional logic. The template-first approach's primary engine contribution was *deleting* mode-aware code, not adding it. The FR-009 validation heading table was an additive data change, not a new conditional branch.

If the engine-approach thesis were correct — that mode behavior should move into the engine — we would expect spec 004 to have added mode-specific conditional branches to SKILL.md. Instead, it removed them. The implementation moved in the template-first direction, not the engine-first direction.

---

## Updated Competitive Position

After reading the engine-approach's cross-review, I make three concessions and sharpen one claim:

**Concessions:**
1. The engine is not "mode-agnostic" — it is **mode-parameterized**. It maintains bounded lookup tables (heading strings, entry patterns, required validation headings) indexed by mode. I adopt this more precise terminology.
2. "Zero engine changes for new modes" was imprecise. New modes require **zero engine logic changes** and a **bounded number of engine data additions** (table rows).
3. My original constitutional argument was too absolute. Both approaches can claim constitutional compliance. Principle VIII is satisfied by the current system, not uniquely by either proposal.

**Sharpened claim:**

The engine-approach is not a competing architecture. When its four concrete deliverables are examined, three are incremental improvements to the existing template-first system (better naming, consolidation, validation), and the fourth is an explicit concession that templates own mode behavior. The engine-approach's argumentative framework — that mode behavior belongs in the engine — is not reflected in its own proposals, which keep mode behavior in templates and add a validation layer.

The template-first architecture is the architecture that shipped, that the spec called for (spec.md line 208: "Template-First Approach"), that the constitution endorses, and that the engine-approach's own proposals do not actually propose to replace. The debate reduces to: should we add a template linter (template-first enhancement) or engine-level heading validation (engine-approach enhancement)? Both are compatible with the template-first foundation. Neither moves mode behavior into the engine.

The template-first approach wins because the engine-approach, examined at the level of concrete proposals rather than rhetorical framing, is a variant of the template-first approach. The engine-approach's thesis — that mode behavior belongs in the engine — is contradicted by its own deliverables, which keep mode behavior in templates and propose adding validation. That is the template-first architecture with better tooling, and I support adding that tooling within the template-first framework.
