# Template-First Approach: Opening Argument

## Thesis

The template-first approach is the correct architecture for extending conversus to universal rounds because **mode-specific behavior IS prompt engineering**, and prompt engineering belongs in templates. Spec 004 proves this empirically: all four modes now support rounds, stagnation, and arbitration with exactly four lines changed in SKILL.md and six new template files created. The engine stayed mode-agnostic. The templates carry the mode intelligence. This is not a theoretical preference -- it is the architecture that shipped, and it shipped cleanly because templates are the right abstraction for this problem.

## Strengths

### 1. The Implementation Proves the Architecture

Spec 004's `work_done.md` documents the complete changeset (`<HOME>/code/payer-index-mono/conversus/specs/004-universal-rounds/work_done.md`). The SKILL.md changes were:

| Change | Scope |
|--------|-------|
| Remove arbiter mode restriction | Delete one validation rule |
| Remove rounds mode restriction | Delete one validation rule |
| Update Phase 6 forward-compat note | One sentence edit |
| Add mode-specific Phase 6 validation headings | One table addition |

That is it. Four edits to the engine. The remaining work -- the game-theory-informed prompt engineering that makes red-blue rounds track risk trajectories, winner-take-all rounds track ranking evolution, and prisoners-dilemma rounds track cooperation dynamics -- all lives in templates. The engine did not need to know anything about these mode-specific behaviors.

This is not an accident. The spec itself predicted this outcome at line 199-208 of `spec.md`:

> The conversus engine (SKILL.md orchestrator) already implements rounds, stagnation, and arbitration generically. The mode-specific behavior lives almost entirely in templates. The engine changes are:
> 1. Remove two validation `if` statements (FR-001).
> 2. Add mode-specific required headings to Phase 6 validation (FR-009).
> 3. Verify round-aware variables populate for all modes (FR-010).

The spec called it "Template-First Approach" (line 208) and the implementation confirmed it.

### 2. Templates Are the Right Abstraction for Mode Behavior

Consider what differs between cooperative and winner-take-all cross-round synthesis. It is not the orchestration mechanics -- both run through the same round loop (SKILL.md lines 296-313), both use the same termination conditions, both produce output at `{output}/summary/final.md`. What differs is the **analytical framework** the synthesizer applies:

- **Cooperative** (`templates/cooperative/cross-round-synthesis.md`): Tracks dispute trajectory, convergence progression, produces a final recommendation set with P1/P2/P3 priorities.
- **Winner-take-all** (`templates/winner-take-all/cross-round-synthesis.md`): Tracks ranking trajectory, proposal evolution, produces a winner declaration with runner-up assessment.
- **Red-blue** (`templates/red-blue/cross-round-synthesis.md`): Tracks risk trajectory, defense effectiveness progression, attack pattern shifts, produces a final risk register.
- **Prisoners-dilemma** (`templates/prisoners-dilemma/cross-round-synthesis.md`): Tracks cooperation dynamics, boundary trajectory, tit-for-tat emergence, produces a final boundary map.

These are not different algorithms. They are different lenses applied to the same structural process. Templates are precisely the right abstraction for "same structure, different content." A parameterized prompt with mode-specific analytical instructions is what template engines exist for.

### 3. Each Template Is Independently Reviewable and Testable

The constitution compliance review (`<HOME>/code/payer-index-mono/conversus/specs/004-universal-rounds/work_done_constitution_review/templates_review.md`) demonstrates this concretely. The reviewer examined each template against all nine constitutional principles independently. Findings were scoped to individual templates:

- Red-blue cross-round synthesis: 9/9 PASS
- Winner-take-all cross-round synthesis: 8/9 PASS, 1 VIOLATION (heading naming -- low severity, functional parser still works)
- Prisoners-dilemma cross-round synthesis: 8/9 PASS, 1 VIOLATION (heading naming -- low severity, functional parser still works)

If mode behavior lived in engine logic, you could not review it this way. Conditional branches in SKILL.md's orchestrator would interleave mode logic with framework logic, making independent review impossible. Templates give you clean boundaries: each file is one mode's behavior for one phase, reviewable in isolation.

### 4. The Engine Stays Simple

SKILL.md line 701 states the architectural principle explicitly:

> Templates contain the mode-specific prompt engineering. The skill just fills variables and orchestrates.

The engine's responsibilities are well-defined and mode-agnostic:
- Parse config and validate (Step 1)
- Create output directories (Step 2)
- Load templates by path `templates/{mode}/` (Step 3)
- Execute phases with variable substitution (Step 4)
- Report results (Step 5)

The engine knows `{mode}` exists as a path selector for templates and as a key for the Phase 6 validation heading table (SKILL.md lines 587-592). Beyond that, it does not interpret mode semantics. This is a clean separation of concerns.

### 5. Adding New Modes Requires Zero Engine Changes

If a fifth mode were added to conversus -- say, `auction` for multi-agent bidding deliberations -- the template-first architecture requires:

1. Create `templates/auction/review.md`, `cross-review.md`, `revision.md`, `disputes.md`, `synthesis.md`
2. Optionally create `templates/auction/arbitration.md` and `cross-round-synthesis.md`
3. Add `auction` to the mode validation enum in SKILL.md (one word in one line)
4. Add an `auction` row to the Phase 6 validation heading table (one table row)

No orchestration logic changes. No new conditional branches. No risk of breaking existing modes. The engine's round loop, stagnation detection, phase execution, and agent dispatch all work identically for the new mode because they work identically for all modes.

### 6. Constitutional Alignment Is Explicit

Constitution Principle VIII (`<HOME>/code/payer-index-mono/conversus/.specify/memory/constitution.md`, lines 121-139) is titled "Templating Engines Over Inference" and states:

> Prefer mechanical template-driven behavior over LLM inference and improvisation. When an outcome can be achieved by variable substitution, structured config, or deterministic rules, do NOT delegate it to agent reasoning.

And specifically:

> Mode-specific behavior is encoded in templates, not inferred by agents at runtime. The template dictates the output shape -- the agent provides the content within that shape.

This is not a general preference -- it is a constitutional mandate. The template-first approach is the only approach that satisfies this principle. An engine-level approach that encodes mode behavior in SKILL.md conditional logic would either (a) duplicate template-level instructions in engine logic, or (b) require the engine to emit mode-specific prompts dynamically, which is inference-over-templates.

## Honest Weaknesses

### W1: Templates Cannot Enforce Structural Invariants Across Phases

The engine-approach competitor will correctly note that templates are phase-scoped. A template for Phase 5 synthesis cannot enforce that Phase 4 dispute documents used the correct headings. The Dispute-Parsing Subsystem (SKILL.md lines 656-683) is engine-level logic that reaches across phases to parse template-produced output. This IS engine logic, and the template-first approach acknowledges it.

However, this is a narrow exception. The Dispute-Parsing Subsystem is a stable interface contract -- it defines what headings templates must produce, and templates comply. The engine parses; the templates produce. This is a well-understood pattern (like a compiler reading source files), not evidence that mode behavior should move into the engine.

### W2: The Phase 6 Validation Heading Table Is Engine Logic

The mode-specific validation heading table (SKILL.md lines 587-592) IS mode-aware engine logic. There is no way around it: the engine must know which headings to validate per mode. This is a small, bounded exception (four rows in one table) that exists because output validation is inherently a consumer responsibility, not a producer responsibility. The template says what to write; the engine checks that it was written.

### W3: Heading Naming Inconsistencies Emerged

The constitution review found two low-severity violations: the winner-take-all cross-round synthesis used `### Remaining Contested Positions` instead of `### Remaining Disputes`, and the prisoners-dilemma cross-round synthesis used `### Remaining Disputed Boundaries` instead of `## Disputed Boundaries`. These are heading renames that, while functionally harmless (the parser's substring matching still works), demonstrate that templates require discipline to maintain naming consistency across the template set. This is a governance challenge, not an architectural one.

### W4: Templates Are Opaque to Automated Testing

You cannot unit-test a markdown template the way you can test conditional engine logic. Template quality depends on prompt engineering review, not automated validation. The constitution review process (nine-principle manual audit per template) is the testing mechanism, and it is human-intensive.

## Competitor Gaps

### The Engine Approach Conflates Orchestration with Content

The engine-approach argument -- that mode behavior should be encoded in SKILL.md as conditional orchestration logic -- fundamentally misidentifies what varies across modes.

What varies is **content**: what the synthesizer analyzes (risks vs. rankings vs. boundaries), what headings it uses, what analytical framework it applies, what output sections it produces.

What does NOT vary is **orchestration**: the phase sequence (1-5, optionally 6), the round loop, the stagnation detection formula (dispute count comparison), the agent dispatch model (parallel within phase, sequential across phases), the output directory structure.

Encoding content variation in orchestration logic would mean SKILL.md contains prose prompt text for each mode -- effectively embedding templates inside the engine. This is strictly worse than having templates in template files because:
1. The engine file grows linearly with modes (four modes means four copies of every phase prompt)
2. Template changes require editing the engine file, increasing blast radius
3. Mode-specific prompt engineering is buried in orchestration logic, making it harder to review

### Stagnation Detection Is Not Evidence for Engine-Level Mode Logic

The engine-approach competitor will argue that stagnation detection is already engine logic (which it is), and therefore mode behavior belongs in the engine. This is a non sequitur. Stagnation detection is a mode-parameterized engine operation: it uses mode-specific headings (defined in the Dispute-Parsing Subsystem's stable interface table at SKILL.md lines 674-677) but applies the same algorithm (count comparison) for all modes. The mode-specific headings are data, not logic. They are a lookup table, not conditional branches.

The correct analog is a database query engine that uses different column names per table but applies the same comparison operators. You do not build a separate query engine per table -- you parameterize the column names. This is exactly what the Dispute-Parsing Subsystem does.

### Engine-Level Mode Awareness Creates Coupling That Prevents Extension

If mode behavior is encoded as conditional branches in SKILL.md, adding a fifth mode means:
1. Adding branches to every conditional in SKILL.md (stagnation detection, phase execution, output validation, template loading, variable population)
2. Testing every existing mode to ensure the new branches did not break them
3. Reviewing the entire SKILL.md file, not just the new mode's templates

The template-first approach localizes mode addition to a new `templates/{mode}/` directory. Existing templates and SKILL.md are untouched.

## Risk Profile

### R1: Template Sprawl

As modes multiply and each mode requires 7 template files, the template directory grows. With 4 modes, that is 28 template files. With 6 modes, 42. Each requires independent review and maintenance.

**Mitigation**: The cooperative templates serve as structural references. New mode templates follow the same pattern (Context, What to Read, What to Produce, Rules). A template linter could validate structural consistency.

### R2: Cross-Template Consistency Is Not Automatically Enforced

Templates can drift in heading names, section ordering, or variable usage. The constitution review caught two instances. Without automated validation, these accumulate.

**Mitigation**: Add template validation to the conversus test suite: verify all templates use the correct variables, produce the correct headings, and follow the structural pattern. This is a testing gap, not an architectural gap.

### R3: Templates Cannot Express Conditional Behavior

If a future mode requires fundamentally different phase structure (e.g., skipping Phase 3 for a "debate" mode where there are no revisions), templates alone cannot express this. The engine would need mode-specific phase gating.

**Mitigation**: This has not happened. All four modes use the same 6-phase structure. If it does happen, the correct response is to add a bounded exception to SKILL.md (like the Phase 6 validation heading table), not to move all mode behavior into the engine.

## Migration/Adoption Path

There is no migration needed. **This is the approach that was actually implemented.** Spec 004 shipped with the template-first architecture. The engine is mode-agnostic. The templates carry the mode intelligence. Every template has been written, reviewed against the constitution, and verified against the spec's functional requirements.

The engine-approach competitor would need to justify migrating away from a working architecture. The template-first approach asks only that the existing architecture be maintained and extended.

---

The template-first approach wins because it correctly identifies what varies across modes (content, not orchestration), puts that variation in the right abstraction layer (templates, not engine logic), and has been empirically validated by the spec 004 implementation. The engine stayed simple. The templates scaled. The constitution endorses this architecture. The implementation proves it works.
