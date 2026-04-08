# Engine-Approach Revision

## Advantage Classification

### Advantage 1: Stagnation Detection Is Engine Logic, Not Template Logic
**Classification: Modified**

The template-approach cross-review correctly identifies that the Dispute-Parsing Subsystem uses a single algorithm (count comparison) parameterized by mode-keyed data (which heading, which entry pattern). I concede that calling this "mode-specific orchestration logic" overreaches if "logic" is defined narrowly as conditional branching. The algorithm does not branch per mode; it dispatches by data lookup.

However, I do not withdraw the core claim. The template-approach's reframing -- "data, not logic" -- is a semantic maneuver that obscures a meaningful architectural fact. The engine makes a termination decision (continue or stop the round loop) based on mode-specific inputs. Whether you call the dispatch table "data" or "logic," the engine must understand mode-specific output structure to function. A mode whose synthesis uses a heading not listed in the dispatch table will fail silently (disputes always return 0, or the default `true` fires unnecessarily). This is engine-level mode dependency regardless of whether it is implemented as a lookup table or a conditional branch.

**Modified position**: The Dispute-Parsing Subsystem is a mode-parameterized engine operation, not mode-specific conditional logic. But "parameterized by mode" IS a form of mode awareness that contradicts the label "mode-agnostic." The template-approach's own framing -- "the engine needs to know the interface contract to validate template output" -- is an acknowledgment that the engine is mode-aware. The disagreement is about degree, not kind.

### Advantage 2: Phase 6 Validation Is Already Mode-Aware in the Engine
**Classification: Modified**

The template-approach cross-review calls this a "lookup table, not logic" and analogizes it to a routing table that dispatches to handlers. I accept the analogy -- but note that a routing table is definitionally part of the engine, not part of the handlers. If the Phase 6 validation table is like a routing table, then it is engine infrastructure that knows about modes. The template-approach agrees it is engine-level mode awareness (their Weakness W2: "the Phase 6 validation heading table IS mode-aware engine logic"). The only dispute is whether this awareness is "bounded" or "fundamental."

**Modified position**: The Phase 6 validation table is bounded mode awareness in the engine. I withdraw the claim that its existence alone proves mode behavior belongs in the engine. But I maintain that the table's existence disproves the claim that the engine is "mode-agnostic." The engine is mode-aware-by-data, which is a weaker form of mode awareness than mode-aware-by-branching, but is still mode awareness.

### Advantage 3: Role Enforcement Is an Engine Invariant Templates Cannot Guarantee
**Classification: Surviving**

The template-approach cross-review did not directly rebut this advantage. Role enforcement (red-blue requires at least one `role: red` and one `role: blue`) is a precondition that runs before any template is loaded. Templates cannot express or enforce this invariant. If a `conversus.yml` is misconfigured with three red agents and zero blue agents, only the engine catches it.

This advantage survives because it is a concrete example of mode behavior that CANNOT live in templates. It is not data parameterization; it is a mode-specific validation rule. A fifth mode with its own structural requirements (e.g., "auction mode requires at least three competing agents") would need an analogous engine-level rule. Templates can instruct agents about their roles, but they cannot prevent misconfiguration.

### Advantage 4: Constitution Principle VI Explicitly Favors Executable Config
**Classification: Withdrawn**

The template-approach cross-review's reading of Principle VIII is stronger than my reading of Principle VI. The relevant constitutional text is unambiguous:

> "Mode-specific behavior is encoded in templates, not inferred by agents at runtime." (constitution.md, line 130-131)

I initially argued that Principle VI ("Scripts Over Markdown") and the "orchestration decisions" clause of Principle VIII placed mode behavior in the engine. But re-reading Principle VIII in full, it makes a clear two-part allocation:
1. Mode-specific behavior goes in templates.
2. Orchestration decisions (phase ordering, trigger evaluation, termination checks) are rule-based and belong in SKILL.md.

My original argument tried to classify stagnation detection and dispute parsing as "mode-specific behavior" that belongs in the engine. But the constitution's taxonomy puts these in different categories: the mode-specific analytical frameworks (how agents think about risks vs. rankings vs. boundaries) are template behavior; the orchestration mechanics (when to terminate, when to trigger Phase 6) are engine behavior that happens to be parameterized by mode data. Principle VIII supports the template-approach's architecture more directly than mine.

I withdraw the constitutional argument. The constitution favors templates for mode-specific behavior and the engine for mode-agnostic orchestration parameterized by mode data. This is the template-first position.

### Advantage 5: The Spec's Game-Theory Analysis Proves Modes Are Structurally Different
**Classification: Modified**

The game-theory differences across modes are real: asymmetric roles in red-blue, single-verdict output in winner-take-all, trust scores in prisoners-dilemma. But the template-approach correctly notes that these differences manifest in content (what agents analyze and produce), not in orchestration (the phase sequence, round loop, and termination mechanics). All four modes use the same 6-phase structure. All four use the same round loop. All four use the same stagnation detection algorithm.

**Modified position**: The structural game-theory differences between modes are significant and real, but they are content differences that templates correctly capture. The orchestration layer treats all modes uniformly (with data parameterization for dispute parsing and output validation). This is evidence FOR the template-first approach, not against it. I originally overstated the architectural implications of game-theory differences.

### Advantage 6: Cross-Round Synthesis Templates Reveal Template-Approach Limitations
**Classification: Modified**

The template-approach cross-review makes two strong counter-arguments:

First, the heading drift was caught by review (earlier in the development cycle), whereas engine-level runtime validation would catch it during execution (later, when a user is waiting). Earlier detection is better.

Second, exact-match engine validation would convert cosmetic naming inconsistencies into hard runtime failures -- making the system more fragile, not less.

I concede both points as stated. However, I note that the template-approach itself concedes the gap (their Weakness W3 and Concession 3) and proposes a template linter as the fix. A linter is not a template. It is a validation tool that encodes knowledge of the stable interface contract -- which is engine-adjacent infrastructure. Whether that validation runs as a linter, a pre-execution check, or a CI step, it embodies the same principle I argued for: structural enforcement of the interface contract, rather than relying on human reviewers.

**Modified position**: The heading drift is real and should be addressed by automated validation. I withdraw the claim that this validation must be runtime/engine-level. A development-time linter or pre-execution check is a better fit. Both approaches agree on the need for automated enforcement; the disagreement is only about where that enforcement runs.

## New Arguments from Cross-Review

### N1: The Engine-Approach Is the Template-First Approach Plus Validation

The template-approach cross-review's sharpest observation is that the engine-approach, when reduced to concrete deliverables, amounts to:
1. Keeping templates for prompt engineering (concedes template-first).
2. Formalizing existing lookup tables (cosmetic reorganization).
3. Adding engine-level template validation (a testing enhancement).

I must address this honestly. On reflection, this characterization is largely accurate. My original argument framed these as a paradigm shift ("the engine IS mode-aware, stop pretending otherwise"), but the concrete changes I proposed do not constitute a different architecture. They constitute an enhancement to the existing architecture.

Where I maintain a genuine disagreement: the template-approach's self-description as "mode-agnostic engine" is misleading. The engine contains three mode-keyed data structures. Calling it "mode-agnostic with bounded exceptions" is a label I find inaccurate, even if the architecture is sound. But accurate labeling is a documentation concern, not an architectural one.

### N2: The Scalability Rebuttal Has Force

The template-approach cross-review dissects the "every non-cooperative mode extension REQUIRED engine changes" claim effectively:

- FR-001 REMOVED engine mode-awareness (deleting validation restrictions). This moved the engine toward mode-agnosticism, the opposite of my thesis.
- FR-009 added four rows of data, not conditional logic.
- The Dispute-Parsing Subsystem predates spec 004 entirely.

Adding a fifth mode would require adding one row to the Dispute-Parsing table, one row to the Phase 6 validation table, and one enum value. These are additive, non-breaking, one-line data additions. This IS meaningfully different from "add conditional branching to orchestration logic." My original claim that "just add templates" was "aspirational marketing" overstated the case. The more honest description is "add templates plus two one-line data rows," which is a lightweight, scalable pattern.

### N3: The "Data vs. Logic" Distinction Matters More Than I Acknowledged

The template-approach cross-review repeatedly insists that the engine's mode awareness is data (lookup tables), not logic (conditional branches). Initially I dismissed this as semantic hair-splitting. After re-reading the Dispute-Parsing Subsystem and Phase 6 validation table, I acknowledge the distinction has architectural substance.

A lookup table is:
- Additive (new rows don't affect existing rows).
- Non-branching (no if/else paths to test).
- Declarative (states what to look for, not how to behave).

Conditional branching is:
- Potentially interfering (new branches can affect control flow of existing branches).
- Requires exhaustive testing of all paths.
- Imperative (specifies different behavior per mode).

The engine's mode awareness is genuinely the former. My proposal to "formalize the mode registry" would not change this -- it would reorganize existing data tables under a unified heading. This is a documentation improvement, not an architectural change.

## Updated Competitive Position

After reading the cross-reviews and re-examining the source materials, I revise my position substantially.

**What I was right about:**
- The engine IS mode-aware. Three mode-keyed data structures exist in SKILL.md. The label "mode-agnostic" is misleading.
- Role enforcement is a genuine engine-level mode invariant that templates cannot express.
- Heading drift is a real risk that requires automated enforcement (both sides agree on this).

**What I was wrong about:**
- The constitutional argument. Principle VIII explicitly places mode-specific behavior in templates. My reading was selective.
- Characterizing data tables as "engine logic." The Dispute-Parsing Subsystem and Phase 6 validation table are parameterized data for a uniform algorithm, not conditional logic.
- The scalability claim. "Just add templates" is approximately true -- the engine data additions for a new mode are bounded, one-line, and non-breaking.
- Framing my proposal as a competing architecture. My concrete deliverables (formalize existing tables, add validation) are an enhancement to the template-first architecture, not a replacement for it.

**Where I maintain ground:**
- The engine should not be described as "mode-agnostic." It is mode-aware-by-data, which is a specific and defensible architectural pattern, but it is not mode-agnostic. Accurate self-description matters for maintainability.
- Role enforcement and any future structural preconditions are genuinely engine territory, not template territory. Templates assume invariants; the engine establishes them.
- Automated heading validation (whether as a linter or pre-execution check) should be implemented. Both sides agree, but neither the template-approach nor the engine-approach has shipped it yet.

**Revised verdict:** The template-first architecture is the correct framing. The engine-approach's original thesis -- that mode behavior belongs in the engine -- overstated what is actually a narrow, data-level mode awareness in the engine that supports (rather than replaces) the template-first architecture. My strongest surviving arguments (role enforcement, heading validation) are compatible with the template-first architecture and do not require an alternative paradigm.

The honest summary: I argued for a paradigm shift but was actually proposing an incremental enhancement to the existing architecture. The template-approach's cross-review correctly identified this. The enhancement (formalized mode registry, automated heading validation) has merit and should be adopted, but it should be adopted as an improvement to the template-first architecture, not as a replacement for it.
