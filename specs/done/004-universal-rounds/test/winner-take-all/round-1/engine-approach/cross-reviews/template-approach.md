# Engine-Approach Cross-Review of Template-Approach

## Weaknesses in Competitor's Proposal

### W1: The "Four Edits" Narrative Understates Engine Dependency

Template-approach's central rhetorical move is to count SKILL.md edits (four) versus template files (six) and declare victory by ratio. This framing obscures the architectural significance of those four edits.

The four SKILL.md changes were not minor housekeeping. They were *preconditions* without which the templates would be inert text:

1. **Removing the arbiter mode restriction**: Without this, any non-cooperative config with `arbiter:` would fail at validation. Templates cannot override validation rules.
2. **Removing the rounds mode restriction**: Without this, any non-cooperative config with `rounds > 1` would fail at validation. Templates cannot override validation rules.
3. **Adding the Phase 6 validation heading table**: This is mode-keyed engine logic -- the engine looks up required headings by mode and validates output. Templates cannot self-validate their own output.
4. **Updating the forward-compat note**: Explicitly acknowledges mode-awareness in the engine.

The template-approach argument amounts to: "the engine barely changed, so templates did all the work." The reality is: the engine already contained the mode-aware orchestration infrastructure (Dispute-Parsing Subsystem, round termination logic, Phase 6 trigger evaluation). It didn't need to change much because the engine-level mode awareness was already built. The templates were downstream consumers of engine guarantees that were already in place.

### W2: Template-Approach Cannot Account for the Dispute-Parsing Subsystem

Template-approach's review (Section "Strengths 2") claims that what differs across modes is the "analytical framework" -- different lenses on the same structural process. This is true for prompt engineering, but it ignores the Dispute-Parsing Subsystem entirely.

The Dispute-Parsing Subsystem (SKILL.md lines 656-683) is a 28-line engine component that:
- Uses mode-keyed lookup to select the correct heading (`### Remaining Disputes` vs. `### Disputed Risks` vs. `## Runner-Up` vs. `## Disputed Boundaries`)
- Uses mode-keyed lookup to select the correct entry pattern (`**Dispute:` vs. `**[RISK-ID]:` vs. presence check vs. `### [` sub-headings)
- Makes a termination decision (continue or stop the round loop)

Template-approach's review mentions this in "Honest Weakness W1" and calls it "a narrow exception." But this exception is the single most important cross-round behavior in the system. Stagnation detection is what prevents infinite loops. Phase 6 trigger evaluation is what decides whether arbitration runs. These are not narrow exceptions -- they are the control-flow backbone of multi-round execution.

Dismissing the Dispute-Parsing Subsystem as "a compiler reading source files" (template-approach's Section "Competitor Gaps", paragraph 2) is a misleading analogy. A compiler is general-purpose; it does not have a hardcoded lookup table mapping four specific languages to four specific parsing rules. The Dispute-Parsing Subsystem is mode-specific engine logic, and it contradicts the claim that the engine is "mode-agnostic."

### W3: The "Zero Engine Changes for New Modes" Claim Is Empirically Falsified

Template-approach's Strength 5 claims adding a fifth mode requires "zero orchestration logic changes" -- just templates plus one enum entry and one table row. But the spec 004 implementation itself disproves this:

- FR-001 required SKILL.md edits (validation rule removal).
- FR-009 required SKILL.md edits (Phase 6 validation heading table).
- The Dispute-Parsing Subsystem's mode-keyed heading table (SKILL.md lines 674-677) already listed all four modes *before* spec 004. Any fifth mode would need a new row here.
- Role enforcement rules (SKILL.md line 176: red-blue requires red+blue roles) are mode-specific engine invariants. A fifth mode with its own role requirements would need engine edits.

A fifth mode would actually require:
1. New row in the Dispute-Parsing Subsystem heading table
2. New row in the Phase 6 validation heading table
3. New entry in the mode validation enum
4. Potentially new role enforcement rules
5. Potentially new stagnation detection semantics if the mode's dispute structure is novel

That is at minimum three SKILL.md edits, not zero. The "just add templates" narrative is marketing, not architecture.

### W4: Template-Approach Conflates Two Kinds of Mode Behavior and Assigns Both to Templates

Template-approach's review identifies that mode differences are about "content, not orchestration" (Section "Competitor Gaps", paragraph 1). This is only half right. Mode differences are about:

1. **Content** (how agents are instructed to think): This is legitimately template territory. Red-blue agents think about attack surfaces; winner-take-all agents think about rankings.

2. **Orchestration semantics** (how the engine interprets output and makes control-flow decisions): This is engine territory. The stagnation formula may be the same algorithm (count comparison), but the *inputs* to that algorithm are mode-specific -- what heading to look for, what entry pattern to count, what constitutes a "dispute."

Template-approach collapses both into templates and then claims the engine is mode-agnostic. But the engine is NOT mode-agnostic. It has a mode-keyed dispatch table for dispute parsing and a mode-keyed dispatch table for output validation. These are engine data structures indexed by mode. The template-approach argument requires pretending these data structures don't exist.

### W5: The Constitution Is Misread

Template-approach cites Constitution Principle VIII ("Templating Engines Over Inference") to argue that templates should carry all mode behavior. But the full text of Principle VIII (constitution.md lines 121-139) says:

> "Orchestration decisions (phase ordering, trigger evaluation, termination checks) are rule-based, not inferred. SKILL.md specifies deterministic logic; agents execute it."

This explicitly places trigger evaluation and termination checks in SKILL.md. Stagnation detection is a termination check. Phase 6 trigger evaluation is a trigger evaluation. Principle VIII says these belong in SKILL.md as deterministic rules -- not in templates as prompt engineering. Template-approach reads Principle VIII as "all mode behavior in templates," but the principle actually says "orchestration in SKILL.md, content in templates." The engine-approach is the correct reading.

### W6: Templates Cannot Self-Enforce Consistency

Template-approach's "Honest Weakness W3" admits that heading naming inconsistencies emerged. The constitution review found two violations:
- Winner-take-all: `### Remaining Contested Positions` instead of `### Remaining Disputes`
- Prisoners-dilemma: `### Remaining Disputed Boundaries` instead of `## Disputed Boundaries`

Template-approach calls this "a governance challenge, not an architectural one." This is precisely wrong. A system where consistency depends on human reviewers catching naming drift across a growing matrix of templates has an *architectural* gap: there is no structural enforcement at the layer where the drift occurs. The engine-approach fills this gap by having the engine validate template output against its mode-keyed heading table. The drift becomes a validation failure rather than a review finding.

Calling this "governance, not architecture" is an attempt to re-categorize an architectural weakness as someone else's problem.

---

## Rebuttal of Competitor's Attacks on Me

### Attack: "The Engine Approach Conflates Orchestration with Content"

Template-approach claims that I want to put "prose prompt text for each mode" into SKILL.md. This is a straw man. The engine-approach explicitly states (review Section "Migration/Adoption Path", item 2):

> "Keep templates for prompt engineering. Templates continue to define how agents think. The engine-approach does not replace templates -- it separates the orchestration layer from the prompt layer."

I am not proposing to embed template content in SKILL.md. I am proposing that the engine explicitly owns mode-specific *orchestration semantics* (stagnation detection, dispute parsing, role enforcement, output validation) while templates continue to own *prompt engineering* (how agents analyze, what analytical framework they apply, what sections they write). Template-approach attacks a position I do not hold.

### Attack: "Stagnation Detection Is Not Evidence for Engine-Level Mode Logic"

Template-approach argues (Section "Competitor Gaps", paragraph 2) that the Dispute-Parsing Subsystem's mode-specific headings are "data, not logic" -- like a database using different column names per table. This analogy undermines their own argument.

A database query engine with per-table column names is *parameterized by table*. It is *table-aware*. If you told a database engineer that their query engine was "table-agnostic" because it uses the same comparison operators for all tables, they would disagree. The engine is table-aware precisely because it maintains a schema mapping per table.

The Dispute-Parsing Subsystem maintains a heading mapping per mode. The Phase 6 validation table maintains a required-headings mapping per mode. The role enforcement rules maintain a role-requirement mapping per mode. The conversus engine is mode-aware in exactly the same way a database engine is table-aware. Calling mode-keyed data "not logic" does not change the fact that the engine dispatches differently based on mode. That is mode awareness.

### Attack: "Engine-Level Mode Awareness Creates Coupling That Prevents Extension"

Template-approach claims (Section "Competitor Gaps", paragraph 3) that engine-level mode awareness means adding a fifth mode requires "adding branches to every conditional in SKILL.md" and "testing every existing mode."

This overstates the coupling. The engine's mode awareness is concentrated in three lookup tables:
1. Dispute-Parsing Subsystem heading table (4 rows)
2. Phase 6 validation heading table (4 rows)
3. Role enforcement rules (1 rule for red-blue)

Adding a fifth mode means adding one row to each table. These are additive, non-breaking changes -- they do not modify existing rows. The claim that existing modes must be "tested to ensure the new branches did not break them" applies equally to the template-approach: adding new templates could theoretically introduce heading conflicts or variable misuse that affects other templates. The coupling concern is symmetric.

### Attack: "This Is the Approach That Was Actually Implemented"

Template-approach's strongest rhetorical argument is incumbency: "this is what shipped." But what shipped is a hybrid. The implementation includes both templates (for prompt engineering) AND engine-level mode awareness (for orchestration semantics). Template-approach claims credit for the whole implementation while acknowledging the engine changes in footnotes.

Incumbency does not prove architectural correctness. It proves that the current architecture works. The engine-approach argument is not "tear it down and rebuild" -- it is "acknowledge the engine's mode awareness explicitly and formalize it, rather than maintaining the fiction that the engine is mode-agnostic while it contains three mode-keyed lookup tables."

---

## Conceded Points

### C1: Templates Are the Correct Home for Prompt Engineering

Template-approach is right that mode-specific analytical frameworks (risk trajectories, ranking evolution, cooperation dynamics, boundary maps) belong in templates. I do not dispute this. Prompt engineering is content; content belongs in templates. My opening argument may have underemphasized this concession.

### C2: The Implementation Works

The spec 004 implementation satisfies all FRs. The system runs. The templates produce correct output (modulo the heading drift). I do not argue that the current architecture is broken -- I argue that it mislabels itself. The engine IS mode-aware; calling it mode-agnostic is a naming error, not a functional one.

### C3: Templates Enable Independent Reviewability

Template-approach correctly notes (Strength 3) that each template can be reviewed against constitutional principles independently. This is a genuine benefit of the template architecture. Engine-level mode logic interleaved with orchestration logic would be harder to review in isolation. I concede this reviewability advantage.

### C4: The Engine Should Not Grow Unboundedly

Template-approach's concern about SKILL.md growing linearly with modes (Section "Competitor Gaps", paragraph 1) is valid. If every mode's prompt engineering were moved into SKILL.md, it would become unwieldy. But this is the straw man I already rebutted -- I propose keeping prompt engineering in templates while formalizing the engine's existing mode-aware orchestration.

---

## Updated Competitive Position

The cross-review sharpens the debate to a single question: **is the engine mode-agnostic or mode-aware?**

Template-approach says mode-agnostic. But the engine contains:
- A mode-keyed Dispute-Parsing Subsystem with four heading entries and four entry-pattern rules
- A mode-keyed Phase 6 validation table with four sets of required headings
- A mode-specific role enforcement rule for red-blue
- Mode-specific template path resolution (`templates/{mode}/`)

That is four mode-aware engine components. Calling this "mode-agnostic with bounded exceptions" is a definition stretched past its useful meaning.

The engine-approach does not propose replacing templates. It proposes:

1. **Acknowledge** that the engine is mode-aware -- stop claiming mode-agnosticism while maintaining three mode-keyed lookup tables.
2. **Formalize** the mode registry: one SKILL.md section that explicitly defines each mode's invariants (dispute heading, entry pattern, required Phase 6 headings, role requirements). This already exists in scattered form; consolidation improves readability.
3. **Add engine-level template validation**: when loading a template, verify it uses the correct stable interface headings for its mode. This catches the heading drift the constitution review found -- at load time, not review time.
4. **Keep templates for prompt engineering**: no change to what templates do. They continue to define analytical frameworks, output sections, and agent instructions.

The net result is a system where:
- Templates own content (what agents write) -- unchanged from current
- The engine owns orchestration semantics (stagnation, validation, enforcement) -- explicit rather than implicit
- Heading drift is caught by the engine, not by human reviewers

Template-approach's strongest argument is that the current system works. It does. The engine-approach's argument is that the current system works *because* the engine is mode-aware, and making that awareness explicit rather than pretending it doesn't exist produces a more honest, maintainable, and enforceable architecture.

The heading drift found by the constitution review is the decisive evidence. Under the template-approach, drift is caught by manual audit. Under the engine-approach, drift is caught by the engine. In a system that will grow to more modes and more templates, manual audit does not scale. Engine enforcement does.
