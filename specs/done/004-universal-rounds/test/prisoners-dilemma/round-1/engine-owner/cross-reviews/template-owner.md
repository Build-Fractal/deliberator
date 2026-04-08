# Cross-Review: engine-owner evaluates template-owner

**Reviewer**: engine-owner
**Subject**: template-owner's Phase 1 capability declaration
**Mode**: prisoners-dilemma
**Spec**: 004-universal-rounds

---

## Contested Territory

### 1. Dispute Heading Ownership — Who Is "Source of Truth"?

template-owner claims (review.md, "Dispute heading conventions" section): "template-owner is the source of truth for what these markers are and where they appear."

engine-owner's position (review.md, Claim 3): The dispute headings are a "shared interface contract" where "neither side can change them unilaterally," citing SKILL.md line 683.

**Assessment**: SKILL.md line 683 is unambiguous: "Changes to these markers or headings are breaking changes and must be coordinated across all synthesis templates and the parsing subsystem." The word "coordinated" means bilateral. template-owner's claim of being "source of truth" overstates this. The headings exist in two places simultaneously: the synthesis templates produce them, and the Dispute-Parsing Subsystem (SKILL.md lines 674-678) defines the canonical list the engine parses against. Neither artifact is derived from the other — they must be kept in sync. This is a bilateral contract, not a template-leads relationship. template-owner's "source of truth" framing is overreach on this specific point.

**Proposed resolution**: Shared interface. Both sides have veto power over heading changes. The coordination requirement in SKILL.md line 683 is the governing rule.

### 2. Phase 6 Required Headings — "Derived Artifact" vs. "Engine-Owned Table"

template-owner claims (review.md, "Phase 6 required headings" section): The engine's validation table (SKILL.md lines 586-593) is "a derived artifact" where "template-owner is the authority on what headings are correct" and "the engine validation table follows."

engine-owner's position (review.md, Claim 4): "I own the validation mechanism. The values in my heading table are derived from what templates instruct agents to produce."

**Assessment**: Both reviews agree on the directional dependency (templates define headings, engine tracks them), and SKILL.md line 594 explicitly states: "if a template's heading instructions change, update this table." However, template-owner's characterization of the table as a "derived artifact" understates the engine's role. The engine owns the validation mechanism and decides what to validate, when to validate, and what severity to assign (warning, not error). The table values follow templates, but the table's existence and enforcement are engine decisions. Calling it "derived" implies the engine is a passive mirror; in reality, the engine chose to build this validation layer and could choose different enforcement strategies. template-owner defines what the correct headings are; engine-owner decides that heading validation exists at all and how it behaves.

**Proposed resolution**: Template-leads on heading content, engine-owns the validation mechanism. template-owner cannot claim the validation table itself as their artifact — only that the heading values within it must track their templates.

### 3. `DISPUTES_BEGIN`/`DISPUTES_END` Markers — Producer vs. Shared Concern

template-owner claims (review.md, "Dispute heading conventions" section): "The synthesis templates contain the `DISPUTES_BEGIN` and `DISPUTES_END` structural markers... template-owner is the source of truth for what these markers are and where they appear."

engine-owner's position (review.md, Shared Interface point 3): These markers are "a shared concern" noting that cross-round synthesis templates omit them.

**Assessment**: The markers appear in the per-round synthesis templates (confirmed: `templates/prisoners-dilemma/synthesis.md` lines 97, 117) but are absent from the cross-round synthesis template (`templates/prisoners-dilemma/cross-round-synthesis.md` — verified, no markers present). The marker syntax itself (`<!-- CONVERSUS:DISPUTES_BEGIN -->`) uses the `CONVERSUS:` namespace prefix, which is an engine-level convention, not a template convention. The Dispute-Parsing Subsystem (engine territory) defines the parsing rules that consume these markers (SKILL.md lines 668-671). template-owner places the markers; the engine defines their syntax and parsing semantics. This is genuinely shared — neither side fully owns it.

**Proposed resolution**: Engine-owner owns the marker syntax specification (what the markers look like). template-owner owns marker placement (where they appear in templates). Both coordinate on changes per SKILL.md line 683.

---

## Overreach Assessment

### Overreach 1: "No other component in the system defines what agents produce"

template-owner claims (review.md, Core Competencies, first paragraph): "No other component in the system defines what agents produce or how they frame their arguments."

**Verdict: Mild overreach.** The engine defines the variable population that shapes what agents have access to. The engine's choice of which variables to compute (SKILL.md lines 348-569) directly constrains what agents can produce. For example, `{PRIOR_ROUND_SECTION}` (engine-computed) determines whether agents receive cross-round context. `{REMAINING_DISPUTES}` (engine-computed) gives arbiters quantitative dispute data. The templates frame how agents use this information, but the engine determines what information is available in the first place. A more accurate claim would be: "No other component defines the narrative framing and analytical structure of agent outputs." The engine defines the informational substrate.

### Overreach 2: "Cross-round narrative logic is entirely template-owned"

template-owner claims (review.md, "Cross-round narrative framing" section): "The engine merely fills variables and dispatches agents; the cross-round narrative logic is entirely template-owned."

**Verdict: Accurate but misleadingly framed.** The claim is technically true — the narrative logic (cooperation dynamics tracking, boundary trajectory analysis, tit-for-tat assessment) is entirely template content. However, the phrase "the engine merely fills variables and dispatches agents" understates the engine's contribution. The engine computes `{TERMINATION_REASON}`, `{ROUNDS_COMPLETED}`, and `{ROUND_SYNTHESES}` (the ordered list of all prior syntheses). Without these computed values, the cross-round narrative would have no data to analyze. The engine does more than "merely fill variables" — it assembles the evidentiary record that makes cross-round synthesis possible. template-owner should acknowledge this dependency rather than minimizing it with "merely."

### Overreach 3: Spec-to-template authority claim

template-owner claims (review.md, "Spec-to-template feedback loop" section): "Where the spec's proposed headings (FR-009) diverged from the template implementation, the templates were treated as authoritative and the SKILL.md validation table was updated to match the templates rather than the spec."

**Verdict: Factually accurate but problematic as a general principle.** For spec 004, this is what happened — the work_done.md confirms it, and the SKILL.md heading table matches the actual template headings, not the spec's FR-009 table. But template-owner extrapolates this into a general rule: "the spec proposes, the template implements, and the engine validates what the template actually produces." This framing gives templates unilateral authority to deviate from specs. In practice, spec deviations should be documented and justified, not normalized as a template prerogative. The engine has a legitimate interest in spec fidelity because stale specs mislead future implementers (as engine-owner's Limitation 4 notes). template-owner should not claim blanket authority to deviate from specs without coordination.

---

## Verified Claims

### Verified 1: Mode-specific agent behavior definition

template-owner's claim that templates define mode-specific agent behavior is fully verified. The seven template files under `templates/prisoners-dilemma/` encode the PD-specific framing: trust scorecards (synthesis.md lines 42-72), cooperation/defection tracking (cross-round-synthesis.md lines 45-60), boundary dispute format (disputes.md), and subject arbitration with boundary rulings (arbitration.md lines 56-82). The engine is mode-agnostic — confirmed by work_done.md line 50: "no mode gate exists." This is template-owner's strongest and most legitimate claim.

### Verified 2: Output format definition

template-owner legitimately owns the output format within each phase. The synthesis template specifies exact section structure (Trust Scorecard, Responsibility Map, Disputed Boundaries, Recommended Assignments, Gaps and Risks). The arbitration template specifies exact section structure (Process Note, Decision Framework, Binding Decisions, Revised Responsibility Map, Confidence Assessment). These are template decisions, not engine decisions. The engine validates heading presence but does not define or constrain content structure beneath those headings.

### Verified 3: Game-theoretic prompt engineering

template-owner's claim to unique ownership of game-theoretic prompt engineering is verified. The PD-specific dynamics — Accuracy/Value/Trust scoring, tit-for-tat emergence analysis, cooperation equilibrium assessment, reputation effects — appear exclusively in template files. The engine contains zero game-theoretic reasoning. This is the cleanest territory boundary in the entire system.

### Verified 4: Agent constraint specification

Behavioral constraints (scope limitations, citation requirements, neutrality mandates, length guidance) are exclusively template content. Verified in `templates/prisoners-dilemma/arbitration.md` lines 107-114 and `templates/prisoners-dilemma/synthesis.md` lines 148-154. The engine has no mechanism to specify or override these constraints.

### Verified 5: Deferrals are honest

template-owner's deferrals (phase sequencing, config validation, agent dispatch, dispute count computation) are genuine. These are all clearly engine-only concerns with no template involvement. The deferrals demonstrate honest self-assessment — template-owner is not sandbagging on any of these; they are genuinely outside template scope.

### Verified 6: Template variable dependency acknowledgment

template-owner's Shared Territory section acknowledges: "engine-owner is stronger here because the engine defines the available variable set. template-owner can only use what the engine provides." This is accurate and honest. It is the most important concession in template-owner's review.

---

## Cooperation Opportunities

### 1. Closing the structural marker gap

Both reviews identify that cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` markers. template-owner produces the templates; engine-owner's parser benefits from the markers. This is a natural cooperation item: template-owner adds the markers in a future change, engine-owner's parser automatically benefits. No coordination complexity — just template-owner action with engine-owner gratitude.

### 2. Heading consistency discipline

engine-owner's Limitation 2 identifies heading inconsistencies (e.g., "Remaining Disputed Boundaries" vs. "Disputed Boundaries" in PD cross-round synthesis). The engine tolerates these via substring matching but prefers exact matches. template-owner can improve reliability by auditing heading consistency across templates. This is a low-cost, high-value cooperation: template-owner aligns headings, engine-owner's parser becomes more reliable.

### 3. Variable consumption documentation

engine-owner's Limitation 3 notes that `{REMAINING_DISPUTES}` is computed but unused by three of four arbitration templates. Rather than treating this as a problem, both sides can cooperate: engine-owner documents all available variables with usage examples, template-owner evaluates whether consuming additional variables would improve template quality. This is informational cooperation, not a territorial negotiation.

### 4. Spec-implementation convergence

Both reviews acknowledge the FR-009 heading drift (spec says "Boundary Framework, Binding Boundary Decisions, Cooperation Assessment"; implementation says "Decision Framework, Binding Decisions, Revised Responsibility Map"). Neither side owns spec maintenance, but both benefit from spec accuracy. Cooperation opportunity: after implementation stabilizes, one side files a spec update to align FR-009 with reality. This prevents the stale-spec problem both reviews flag.

---

## Updated Boundary Proposal

### Engine-Owner Hard Boundaries (unchanged from Phase 1)

1. **Phase sequencing, round loop, and termination mechanics** — engine-only.
2. **All validation logic** — engine-only.
3. **Variable computation and substitution** — engine-only.
4. **Output directory structure** — engine-only.

### Template-Owner Hard Boundaries (accepted from template-owner's review)

1. **Mode-specific prompt engineering and game-theoretic framing** — template-only.
2. **Output content structure within phases** (sections, sub-headings, tables, analysis frameworks) — template-only.
3. **Agent behavioral constraints** (scope, citation requirements, neutrality, length) — template-only.
4. **Cross-round narrative strategy** (what analytical dimensions to track across rounds) — template-only.

### Shared Interface Contract (revised from both Phase 1 proposals)

1. **Dispute headings**: Bilateral contract governed by SKILL.md line 683. Neither side is "source of truth" — both sides must coordinate on changes. The engine's Dispute-Parsing Subsystem (SKILL.md lines 674-678) and the synthesis templates are co-equal authorities that must stay in sync.

2. **Phase 6 required headings**: Template-leads on heading content (templates define what headings agents produce). Engine-owns the validation mechanism (the table at SKILL.md lines 586-593, the validation logic, the warning severity). The directional dependency at SKILL.md line 594 governs: template changes trigger engine table updates.

3. **Structural markers** (`DISPUTES_BEGIN`/`DISPUTES_END`): Engine-owns the marker syntax specification. Template-owner owns marker placement within templates. Both coordinate on any syntax changes.

4. **Template variables**: Engine-owns computation and the available variable set. Template-owner owns consumption decisions (which variables to use, where, and how). Engine commits to stable variable contracts; template-owner accepts that unused variables are not a defect.

### Rejected Claims

1. **template-owner as "source of truth" for dispute headings**: Rejected. The relationship is bilateral, not hierarchical. SKILL.md line 683 says "coordinated," not "template-defined."

2. **Engine validation table as "derived artifact"**: Rejected as framing. The heading values track templates, but the table's existence and enforcement behavior are engine-owned. "Template-sourced values in an engine-owned mechanism" is the accurate characterization.

3. **Blanket authority to deviate from specs**: Rejected as a general principle. Spec 004's implementation correctly followed templates over a stale spec table, but this should be treated as a justified exception requiring documentation, not a permanent template prerogative.
