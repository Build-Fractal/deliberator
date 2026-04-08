# Engine-Approach — Opening Argument

## Thesis

The spec 004 implementation demonstrates that mode-specific behavior *cannot* live entirely in templates. The engine (SKILL.md) already contains mode-aware logic for stagnation detection, dispute parsing, Phase 6 validation, and role enforcement -- and this engine-level mode awareness is what actually makes multi-round non-cooperative modes work. The template-first narrative is a convenient fiction: the real architectural decision was to encode mode semantics in the engine while pretending templates do all the work.

## Strengths

### 1. Stagnation Detection Is Engine Logic, Not Template Logic

The most important cross-round behavior -- deciding whether to *stop* -- is entirely engine-level. The Dispute-Parsing Subsystem at SKILL.md lines 656-683 defines mode-specific parsing rules that the orchestrator executes:

| Mode | Heading | Entry Pattern |
|------|---------|---------------|
| cooperative | `### Remaining Disputes` | `**Dispute:` entries |
| red-blue | `### Disputed Risks` | `**[RISK-ID]:` entries |
| winner-take-all | `## Runner-Up` | presence check |
| prisoners-dilemma | `## Disputed Boundaries` | `### [` sub-headings |

This is a mode-keyed lookup table *in the engine*. The orchestrator reads synthesis output, applies mode-specific parsing rules, counts disputes, and makes termination decisions (SKILL.md lines 461-498). Templates cannot do this. Templates produce output; the engine *interprets* that output to make orchestration decisions. The template-first approach would require the synthesizer agent to self-report whether stagnation occurred -- delegating a control-flow decision to inference, which directly violates Constitution Principle VIII ("Templating Engines Over Inference", lines 121-139 of constitution.md):

> "Orchestration decisions (phase ordering, trigger evaluation, termination checks) are rule-based, not inferred."

Stagnation detection is a termination check. It is rule-based. It is engine logic. The template-first approach has no answer for this.

### 2. Phase 6 Validation Is Already Mode-Aware in the Engine

SKILL.md lines 585-593 contain a mode-keyed validation table:

| Mode | Required Headings |
|------|-------------------|
| cooperative | Process Note, Decision Framework, Binding Decisions, Summary of Changes Required |
| red-blue | Process Note, Decision Framework, Binding Decisions, Updated Risk Register |
| winner-take-all | Process Note, Decision Framework, Verdict Review, Binding Decision |
| prisoners-dilemma | Process Note, Decision Framework, Binding Decisions, Revised Responsibility Map |

This is *engine-level mode awareness*. The orchestrator reads the current mode, looks up the required headings, and validates Phase 6 output against them. The template-first approach claims the engine is "mode-agnostic" -- but the engine already has a mode-keyed lookup table for output validation. The spec 004 implementation *added this table* (per FR-009 and the work_done.md Change 4). The template-first camp wrote mode-specific engine logic while claiming they didn't.

### 3. Role Enforcement Is an Engine Invariant Templates Cannot Guarantee

Red-blue mode requires at least one `role: red` and one `role: blue` agent. This is enforced by SKILL.md validation at line 176:

> "For `red-blue` mode: at least one agent has `role: red` and one has `role: blue`"

This is a mode invariant. It guarantees structural correctness before any template is loaded. A template can instruct agents about their roles, but it cannot prevent a misconfigured `conversus.yml` from running 3 red agents and 0 blue agents. Only the engine can catch this at validation time.

The engine-approach generalizes this pattern: each mode's invariants (role balance for red-blue, minimum 2 competitors for winner-take-all, etc.) are engine-level preconditions. Templates assume these invariants hold -- but the engine is what *establishes* them. Templates are downstream consumers of engine guarantees.

### 4. Constitution Principle VI Explicitly Favors Executable Config Over Prompts

Constitution Principle VI ("Scripts Over Markdown", constitution.md lines 91-104) states:

> "Prefer executable scripts over static markdown when the artifact drives behavior. If a document is consumed by automation or agents to make decisions, it SHOULD be a script, config, or structured data -- not prose that must be parsed ambiguously."

And specifically:

> "Orchestration logic belongs in SKILL.md (executable spec) and templates (parameterized prompts), not in freeform documentation."

This principle explicitly names SKILL.md as the home for orchestration logic. Mode-specific round behavior (stagnation thresholds, termination conditions, dispute counting rules) IS orchestration logic. Encoding it in SKILL.md is constitutionally correct. The template-first approach pushes behavior into "parameterized prompts" -- but a template cannot make control-flow decisions. When cross-round behavior *differs fundamentally* across modes (and it does -- risk counting vs. ranking stability vs. boundary movement vs. dispute counting), the orchestration logic that interprets these differences belongs in the engine.

### 5. The Spec's Own Game-Theory Analysis Proves Modes Are Structurally Different

Section 3 of spec.md (lines 59-84) provides game-theory analysis showing that each mode has fundamentally different cross-round dynamics:

- **Red-blue**: Attack-defense iteration. Stagnation = "attack surface exhausted." The metaphor is *penetration testing rounds*.
- **Winner-take-all**: Elimination tournament. Stagnation = "rankings stabilize." The metaphor is *competitive refinement*.
- **Prisoners-dilemma**: Iterated PD with reputation. Stagnation = "boundary disputes stop moving." The metaphor is *strategy equilibrium*.

These are not cosmetic differences that templates paper over. They represent structurally different game dynamics:

- Red-blue has *asymmetric roles* (attacker/defender). No other mode has this. The engine must understand this asymmetry.
- Winner-take-all has a *single verdict output* rather than per-dispute resolutions. Phase 6 for winner-take-all makes ONE decision; Phase 6 for other modes makes N decisions.
- Prisoners-dilemma has *trust scores and reputation effects* that evolve across rounds. No other mode tracks per-agent trust.

Templates can describe these differences in prose. The engine can enforce them structurally. The engine-approach is stronger because enforcement prevents errors that description merely hopes to avoid.

### 6. Cross-Round Synthesis Templates Already Reveal Template-Approach Limitations

The constitution compliance review (`work_done_constitution_review/templates_review.md`, lines 69-83) found that the winner-take-all cross-round synthesis template uses `### Remaining Contested Positions` instead of the stable interface heading `### Remaining Disputes`. The prisoners-dilemma template uses `### Remaining Disputed Boundaries` instead of `## Disputed Boundaries`.

These are not random errors. They are *symptoms of templates not being constrained by the engine*. When mode behavior lives only in templates, there is no structural enforcement that templates use the correct headings. The template author drifted from the stable interface because nothing stopped them. The constitution review caught it, but the engine-approach prevents it: if the engine knows which heading each mode requires (as it already does in the Dispute-Parsing Subsystem), it can validate template output against that expectation.

The template-first approach relies on human reviewers catching heading mismatches across a growing matrix of modes x phases x templates. The engine-approach automates this enforcement.

## Honest Weaknesses

### 1. Higher SKILL.md Complexity

Moving more mode logic into SKILL.md increases its size and conditional complexity. SKILL.md is already 720 lines. Adding mode-specific orchestration branches could make it harder to read.

**Mitigation**: The complexity already exists -- the Dispute-Parsing Subsystem, Phase 6 validation table, and role enforcement rules ARE mode-specific engine logic. Making the pattern explicit and consistent is better than having it scattered implicitly. The complexity is inherent in the problem; the question is whether it's organized or ad hoc.

### 2. New Modes Require Engine Changes

Under the template-first approach, adding a new mode requires only new templates. Under the engine-approach, it also requires SKILL.md changes.

**Mitigation**: This is actually a *feature*, not a bug. A new mode SHOULD require engine awareness. A mode that the engine doesn't know about can't have validated stagnation detection, role enforcement, or dispute parsing. Under the template-first approach, a new mode with broken stagnation detection would silently run without catching stagnation -- a failure mode that the engine-approach prevents.

### 3. Templates Are Proven to Work

The spec 004 implementation was completed using the template-first approach. All FRs are done. The system works.

**Counter-argument**: It works because the engine ALSO changed. The work_done.md documents 4 SKILL.md edits and 6 template changes. The template-first narrative says "the bulk is template creation" (spec.md line 208), but the engine changes were *necessary* -- they enabled the templates to function. Without the validation rule removals and the Phase 6 heading table, the templates would be inert text. The engine-approach acknowledges this reality; the template-first approach obscures it.

## Competitor Gaps

### The Template-First Approach Cannot Enforce Cross-Template Consistency

The three new cross-round synthesis templates were created independently. Each one had heading drift from stable interfaces (documented in the templates_review.md). Under the template-first approach, the only defense against this drift is manual constitution compliance review.

The engine-approach would express mode-specific heading requirements as engine-level data (like the Phase 6 validation table), making drift detectable at execution time rather than review time.

### The Template-First Approach Conflates Two Kinds of "Mode Behavior"

There are two categories of mode-specific behavior:

1. **Prompt engineering** -- how agents are instructed to think (attack surfaces vs. competing proposals vs. boundary claims). This is legitimately template territory.
2. **Orchestration semantics** -- how the engine interprets agent output, makes control-flow decisions, and enforces invariants. This is engine territory.

The template-first approach collapses both into templates, which means orchestration semantics (stagnation detection, trigger evaluation, output validation) either get forced into templates (violating Principle VIII) or end up in the engine anyway (contradicting the template-first claim).

The engine-approach cleanly separates these concerns: templates own prompt engineering, the engine owns orchestration semantics. Each layer does what it's good at.

### The Template-First Approach's Scalability Story Is False

The template-first camp argues that "new modes can be added without touching SKILL.md." But the spec 004 implementation proves this is false:

- FR-001 required SKILL.md edits (validation rule removal)
- FR-009 required SKILL.md edits (Phase 6 validation table)
- The Dispute-Parsing Subsystem already contained all four modes' parsing rules before spec 004 was written

Every non-cooperative mode extension REQUIRED engine changes. The templates were necessary but not sufficient. The template-first scalability claim -- "just add templates" -- is aspirational marketing, not demonstrated reality.

## Migration/Adoption Path

The engine-approach does not require a rewrite. It requires acknowledging what has already happened: the engine IS mode-aware, and it should be explicitly so rather than pretending otherwise. The concrete steps:

1. **Formalize the engine's mode registry.** The Dispute-Parsing Subsystem, Phase 6 validation table, and role enforcement rules are already a de facto mode registry. Make it explicit: one SKILL.md section that defines each mode's invariants, stagnation semantics, and validation rules.

2. **Keep templates for prompt engineering.** Templates continue to define how agents think. The engine-approach does not replace templates -- it separates the orchestration layer from the prompt layer.

3. **Add engine-level template validation.** When loading a template, the engine can verify that it uses the correct stable interface headings for its mode. This catches the heading drift that the constitution review found -- at load time, not review time.

## Risk Profile

### Risk 1: Over-engineering for four modes

If conversus never adds a fifth mode, the engine-approach's formalization is unnecessary overhead.

**Mitigation**: The formalization also improves the existing four modes by catching template drift and making stagnation semantics explicit. The value is not just future-proofing; it's present-day correctness.

### Risk 2: SKILL.md becomes a monolith

Adding more engine logic could make SKILL.md unwieldy.

**Mitigation**: SKILL.md is already organized into subsections (Dispute-Parsing Subsystem, Important Notes, etc.). A formal mode registry would add one section, not scatter logic throughout the file. The alternative -- scattered implicit mode awareness -- is worse for readability than explicit, centralized mode definitions.

### Risk 3: Template authors lose autonomy

If the engine validates template headings, template authors can't freely rename sections.

**Mitigation**: This is the point. Freely renaming sections is how the heading drift happened in the first place. Constraints on template headings are not a bug -- they're the enforcement mechanism that stable interfaces require.
