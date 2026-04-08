# Cross-Review of Engine-Approach — by Template-Approach

## Weaknesses in Competitor's Proposal

### 1. The Engine-Approach Mischaracterizes Data Tables as "Mode Logic"

The engine-approach's strongest exhibits -- the Dispute-Parsing Subsystem headings table (SKILL.md lines 674-677) and the Phase 6 validation heading table (SKILL.md lines 587-592) -- are not conditional logic. They are lookup tables. Data, not behavior.

The Dispute-Parsing Subsystem does not contain four different algorithms for parsing disputes. It contains ONE algorithm (search for heading, count entries beneath it) parameterized by four rows of data (which heading, which entry pattern). This is the template-first architecture applied to the engine: the engine is mode-agnostic in its *logic* and mode-aware only in its *data*. The engine-approach calls this "engine-level mode awareness" as though it proves that mode behavior belongs in the engine. It does not. It proves that the engine needs a small, bounded lookup table to interface with mode-specific template output -- exactly the pattern the template-first approach describes and defends.

If four rows of heading data constitute "engine-level mode logic," then a web server's routing table constitutes "application-level business logic." The analogy breaks down because a routing table dispatches to handlers (templates); it does not contain the handler logic itself. That is exactly the relationship between SKILL.md's heading tables and the templates that produce the headings.

### 2. The "Stagnation Detection Is Engine Logic" Argument Proves the Template-First Case

The engine-approach's Strength 1 argues that stagnation detection is "entirely engine-level" and that "templates cannot do this." We agree. We said so in our opening argument (Weakness W1). The engine parses template output to make termination decisions. This is consumer-side interpretation -- a well-understood pattern, not a revelation.

But the engine-approach then overreaches: "The template-first approach has no answer for this." We do have an answer, and we stated it explicitly: stagnation detection is a mode-parameterized engine operation that uses mode-specific headings as data inputs (lookup table) but applies the same algorithm (count comparison) for all modes. The engine-approach agrees that the algorithm is the same for all modes (count >= prior => stagnation). What differs is which heading to look under -- and that is a single string lookup, not conditional logic.

The engine-approach's proposal to "formalize the engine's mode registry" (Migration Step 1) would formalize what is already a four-row lookup table into an explicit registry. This adds ceremony without adding capability. The data is already organized in one place (the Dispute-Parsing Subsystem). Making it "more formal" does not make it more correct.

### 3. The Template Drift Argument Is Self-Defeating

The engine-approach's Strength 6 argues that heading drift in templates (e.g., `### Remaining Contested Positions` instead of `### Remaining Disputes`) proves templates are insufficiently constrained and that the engine should validate template output. This argument undermines the engine-approach's own position in two ways:

**First**, the heading drift was caught by the existing review process (constitution compliance review). The engine-approach proposes runtime validation as a replacement for review-time detection. But runtime validation catches errors LATER (during execution, when a user is waiting for results), while review-time detection catches errors EARLIER (before merge). Earlier detection is strictly better. The engine-approach is proposing a slower feedback loop as an improvement.

**Second**, the engine-approach concedes that the heading drift was "functionally harmless" -- the parser's substring matching still works. The drift created a naming inconsistency, not a functional failure. The fix is a one-word rename in a template file. If the engine were validating exact heading strings, that same one-word deviation would have caused a hard failure at runtime -- converting a cosmetic issue into a user-facing error. The engine-approach would make the system MORE fragile, not less.

### 4. The "Templates Cannot Enforce Cross-Template Consistency" Gap Is Real but the Proposed Solution Is Worse Than the Problem

The engine-approach identifies a real governance challenge: cross-template consistency is not automatically enforced. Their solution is to move enforcement into the engine. But this creates a new problem: the engine becomes the gatekeeper for template content, which means template authors cannot iterate on templates without coordinating with engine changes.

The template-first solution is a template linter -- a separate validation tool that checks templates against the stable interface contract without baking the contract into the engine's execution path. This keeps the engine simple (Principle IX: "If the implementation is hard to explain, it's a bad idea") and keeps template validation in the development workflow, not the runtime path.

### 5. The Migration Path Is a No-Op Dressed Up as a Plan

The engine-approach's "Migration/Adoption Path" (three steps) amounts to:

1. "Formalize the engine's mode registry" -- the engine already has the tables. "Formalizing" them means what? Adding a section heading? The tables are already organized in named subsections.
2. "Keep templates for prompt engineering" -- this IS the template-first approach. The engine-approach concedes that templates own prompt engineering.
3. "Add engine-level template validation" -- this is the only concrete proposal, and it amounts to string-matching validation of template headings at load time. This is a testing concern being shoehorned into the runtime engine.

When the engine-approach concedes that templates own prompt engineering and that the engine should "keep templates," it is conceding the template-first architecture and proposing to add a validation layer. That is not a competing architecture -- it is an incremental enhancement to the existing template-first architecture.

### 6. Constitution Principle VIII Is Misread

The engine-approach quotes Principle VIII to argue that orchestration logic belongs in SKILL.md. We agree -- and that is exactly where orchestration logic already lives. But Principle VIII also says:

> "Mode-specific behavior is encoded in templates, not inferred by agents at runtime."

This is the sentence the engine-approach conspicuously does not address head-on. The constitution explicitly places mode-specific behavior in templates. The engine-approach argues that mode-specific behavior belongs in the engine. The constitution disagrees.

The engine-approach tries to split "mode behavior" into "prompt engineering" (templates) and "orchestration semantics" (engine). But Principle VIII does not make this split -- it says mode-specific behavior goes in templates, full stop. The orchestration that Principle VIII assigns to SKILL.md is *mode-agnostic* orchestration: "phase ordering, trigger evaluation, termination checks are rule-based." These ARE rule-based in the current implementation -- a single stagnation algorithm parameterized by a heading lookup. The engine-approach wants to add mode-specific *branching* to what is currently mode-parameterized *data*, which is a step away from rule-based orchestration, not toward it.

### 7. The "New Modes Require Engine Changes Is a Feature" Argument Is Circular

The engine-approach's Honest Weakness 2 admits that new modes require engine changes, then claims this is a feature because "a mode that the engine doesn't know about can't have validated stagnation detection." This is circular: the engine-approach proposes putting mode knowledge in the engine, then argues that modes need engine knowledge. Under the template-first architecture, a new mode requires only: (a) a new heading row in the Dispute-Parsing Subsystem table, (b) a new row in the Phase 6 validation table, and (c) new templates. Items (a) and (b) are one-line data additions, not logic changes. The template-first approach already handles this.

## Rebuttal of Competitor's Attacks on Me

### Attack: "The Template-First Approach Cannot Enforce Cross-Template Consistency"

**Rebuttal**: Cross-template consistency is a governance problem, not an architecture problem. The constitution compliance review process caught both heading deviations. A template linter (which I proposed in Risk R2's mitigation) would automate this. The engine-approach proposes baking validation into the runtime engine, which is heavier than needed and couples template content to engine internals. Consistency enforcement belongs in the development pipeline (lint, review), not the execution path.

### Attack: "The Template-First Approach Conflates Two Kinds of Mode Behavior"

**Rebuttal**: The engine-approach proposes a clean-sounding taxonomy: "prompt engineering" (templates) vs. "orchestration semantics" (engine). But in practice, the "orchestration semantics" that differ per mode in the current implementation are: (1) which heading to parse for disputes (a string lookup), (2) which headings to validate in Phase 6 output (a string lookup), and (3) which roles to validate in config (a string lookup). Three lookup tables. These are not "orchestration semantics" in any meaningful sense -- they are parameterized data for a mode-agnostic orchestration engine. The template-first approach does not "collapse" these into templates; it correctly identifies them as bounded, data-level mode awareness that is already cleanly implemented as lookup tables.

### Attack: "The Template-First Approach's Scalability Story Is False"

**Rebuttal**: The engine-approach claims that "every non-cooperative mode extension REQUIRED engine changes." Let us examine what those changes were:

1. FR-001: Delete two `if` statements. This was *removing* engine mode-awareness, not adding it. Before spec 004, the engine was MORE mode-aware (it rejected non-cooperative modes). After spec 004, the engine is LESS mode-aware. The template-first approach made the engine more mode-agnostic. The engine-approach claims credit for a change that moved in the opposite direction of their thesis.

2. FR-009: Add four rows to a heading validation table. This is one-line-per-mode data. Not conditional logic. Not orchestration branches. Data.

3. The Dispute-Parsing Subsystem "already contained all four modes' parsing rules" -- yes, and those rules are four rows of (heading, pattern) data that predate spec 004 entirely. They were not written as part of the template-first approach; they were baseline infrastructure.

The scalability story is: adding a new mode requires new templates plus one-line data additions to two tables. The engine's logic does not change. The engine-approach's claim that "just add templates" is false is itself false -- it is "add templates plus add two one-line data rows," which is categorically different from "add conditional branching to orchestration logic."

### Attack: "The Engine IS Mode-Aware, and the Template-First Approach Pretends Otherwise"

**Rebuttal**: We never claimed the engine has zero mode awareness. Our opening argument explicitly acknowledged the Dispute-Parsing Subsystem (W1), the Phase 6 validation table (W2), and the role enforcement check as engine-level mode awareness. What we claimed -- and what remains true -- is that this awareness is bounded, data-level, and amounts to lookup tables, not orchestration logic. The engine-approach's narrative that the template-first camp "pretends" the engine is mode-agnostic is a straw man. Our thesis was: "mode-specific behavior IS prompt engineering, and prompt engineering belongs in templates." The small set of per-mode data in the engine (heading names, required output sections) is the interface contract between the engine and the templates -- not evidence that mode behavior should migrate into the engine.

## Conceded Points

### 1. The Engine Does Contain Mode-Aware Data (Already Acknowledged)

The Dispute-Parsing Subsystem, Phase 6 validation heading table, and role enforcement check ARE mode-aware engine elements. This was acknowledged in our opening argument (W1 and W2). The engine-approach correctly identifies these as mode-keyed lookup tables. We disagree only on the interpretation: lookup tables are data, not logic, and their presence supports the template-first architecture (the engine needs to know the interface contract to validate template output) rather than undermining it.

### 2. Engine-Level Template Validation Would Catch Drift Earlier Than Runtime

The engine-approach's proposal to validate template headings at load time is a reasonable enhancement. If implemented as a lightweight pre-execution check (not as embedded conditional logic), it would catch heading drift before templates produce output. This is compatible with the template-first architecture -- it is an engine-side validation of the template contract, not an engine-side replacement for templates.

### 3. The Heading Drift Finding Is Legitimate

The two heading naming inconsistencies are real. They were caught by review, but automated detection would be better. We concede this is a gap in the current template-first implementation that should be addressed via a template linter or a pre-execution validation step.

## Updated Competitive Position

The engine-approach's review is well-argued but fundamentally misidentifies what it is proposing. When stripped to its concrete deliverables, the engine-approach amounts to:

1. Keeping templates for prompt engineering (concedes template-first architecture).
2. Formalizing existing lookup tables into a named "mode registry" (cosmetic reorganization of already-organized data).
3. Adding engine-level template heading validation (a testing/validation enhancement, not an architectural change).

None of these deliverables constitute moving mode behavior into the engine. They constitute adding a validation layer to the existing template-first architecture. The engine-approach is not a competing architecture -- it is the template-first architecture plus a linting step, described in language that makes it sound like a paradigm shift.

The template-first approach remains the correct architecture because:

- **It shipped.** The spec 004 implementation is complete under this architecture. The engine-approach is a proposal; the template-first approach is a working system.
- **It is constitutionally mandated.** Principle VIII explicitly places mode-specific behavior in templates. The engine-approach has no constitutional basis for moving mode behavior into the engine -- it can only argue that its lookup tables constitute "orchestration semantics," which is a rebranding of data as logic.
- **It scales by addition.** New modes require new template files and one-line data additions to two tables. The engine's algorithm does not change.
- **The engine-approach's strongest evidence supports the template-first case.** The Dispute-Parsing Subsystem is a mode-parameterized, algorithmically-uniform operation -- exactly the pattern where templates provide the mode specialization and the engine provides the generic machinery.

Where we incorporate the engine-approach's feedback: we support adding a pre-execution template validation step that checks template headings against the stable interface contract. This is additive to the template-first architecture and addresses the heading drift risk without moving mode behavior into the engine. This enhancement can be specced as a future improvement (a template linter or contract validator), fully compatible with the template-first foundation.
