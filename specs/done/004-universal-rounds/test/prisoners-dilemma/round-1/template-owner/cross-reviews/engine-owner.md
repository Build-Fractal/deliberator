# Cross-Review of engine-owner's Territory Declaration

**Reviewer**: template-owner
**Reviewed**: engine-owner
**Mode**: prisoners-dilemma
**Spec**: `004-universal-rounds`
**Date**: 2026-03-20

---

## Contested Territory

### 1. Dispute Headings: Who Is the Authority?

engine-owner (Claim 3 / Shared Interface 1) describes the dispute headings as a "bilateral contract" where "neither side changes them unilaterally." This framing is partially correct but obscures the directional dependency. The headings exist because templates produce them. The Dispute-Parsing Subsystem (SKILL.md lines 674-678) documents which headings to look for, but the headings originate in template content. If a template never produced `## Disputed Boundaries`, the parser would have nothing to match.

engine-owner's own Limitation 2 concedes this: "I need template-owner to maintain heading consistency as a discipline, because I cannot enforce it without becoming a content validator." This is an admission that template-owner is the upstream producer. The "bilateral contract" framing is accurate for change management (neither side should change unilaterally), but the power asymmetry is real: template-owner defines, engine-owner consumes. engine-owner's review calls this a "dependency, not shared ownership" (Claim 1 Boundary) when it suits their framing for validation rules, but switches to "bilateral" when it suits their framing for dispute headings. The relationship is structurally the same in both cases: template-owner is upstream.

**Resolution**: Accept the bilateral coordination protocol for changes (SKILL.md line 683 is correct), but acknowledge that template-owner is the authority on what the headings are. The engine's heading table is a derived index, not a co-equal definition.

### 2. Phase 6 Heading Table: "Engine-Tracked but Template-Sourced" vs. Template-Owned

engine-owner (Claim 4 / Shared Interface 2) calls the Phase 6 heading table a "shared interface" with a "template-leads, engine-follows relationship." This is close to correct, but the word "shared" overstates the engine's role. SKILL.md line 594 explicitly states: "if a template's heading instructions change, update this table." The engine's table is a cache of template-defined values. It is engine-maintained infrastructure that mirrors template authority.

engine-owner's review correctly identifies the directional flow (template defines, engine validates), which aligns with my own declaration. The disagreement is semantic: engine-owner calls it "shared," I call it "template-owned with engine-maintained validation." The practical difference matters because "shared" implies co-equal negotiation rights, while the actual relationship is that templates define the headings and the engine must follow.

**Resolution**: Accept engine-owner's coordination protocol (update table when templates change), but clarify that this is not shared ownership. The engine's heading table is an index that must stay synchronized with its source of truth (the templates). engine-owner maintains the index; template-owner maintains the authority.

### 3. Template Variable Population: Who Defines the Contract?

engine-owner (Claim 5) claims full ownership of "computation and substitution" of variables, and states that templates "decide which variables to reference and how to use them" but cannot compute them. My review states that template-owner defines the "semantic contract for how variables are consumed" -- which engine-owner does not contest.

The contested zone is the variable contract itself. engine-owner frames this as "I compute, you consume, end of story." But the actual relationship is richer: templates define which variables are necessary for each phase by using them, and the engine must provide those variables. If a template references `{REMAINING_DISPUTES}` and the engine fails to populate it, the template breaks. The engine's obligation to populate specific variables is driven by template consumption patterns.

engine-owner's Limitation 3 (cannot enforce variable consumption) concedes one direction of this asymmetry: the engine cannot know what templates ignore. But the reverse is also true: the engine cannot arbitrarily remove a variable without breaking templates that consume it. engine-owner's cooperation offer (point 2: "I never remove or rename an existing variable without a deprecation cycle") implicitly acknowledges template-owner's stake in the variable contract.

**Resolution**: Variable computation is engine territory. Variable availability (which variables exist and their documented semantics) is a shared interface. Template-owner depends on the engine providing documented variables; the engine depends on templates consuming only documented variables. Neither side unilaterally adds or removes from the contract.

---

## Overreach Assessment

### Claim 1 (All Validation Logic): No Overreach

engine-owner's claim to all validation logic is well-evidenced and correctly scoped. SKILL.md lines 170-195 are unambiguously engine territory. template-owner has zero validation logic and should not have any. The boundary statement ("I own the rules, not the content those rules reference") is honest and correctly drawn. FR-001 confirms these were engine-level edits.

**Verdict**: Legitimate claim. No overreach.

### Claim 2 (Round Loop Mechanics): No Overreach

The round loop (SKILL.md lines 294-313), directory creation strategy (lines 209-239), and termination check (lines 461-498) are pure engine infrastructure. template-owner deferred entirely to engine-owner on these topics, and engine-owner does not reach into template content decisions. The boundary ("I own mechanics of when rounds start/stop, not the content agents produce within each round") is correctly drawn.

**Verdict**: Legitimate claim. No overreach.

### Claim 3 (Stagnation Detection): Minor Overreach in Framing

The stagnation comparison logic (count >= prior = stagnation) is cleanly engine-owned. The Dispute-Parsing Subsystem is cleanly engine infrastructure. However, engine-owner's framing of dispute headings as a "bilateral contract" overstates the engine's positional authority, as discussed in Contested Territory 1 above. The headings are template-produced, engine-consumed. engine-owner does not overreach in capability (parsing and comparison are theirs), but overreaches slightly in framing the governance model of the shared interface.

**Verdict**: Capability claim is legitimate. Governance framing overstates engine-owner's positional authority.

### Claim 4 (Phase 6 Output Validation): No Overreach

engine-owner correctly claims the validation mechanism (check headings exist, emit warnings) and correctly identifies the heading values as template-sourced. The boundary is well-drawn. engine-owner explicitly cites SKILL.md line 594's directional dependency. This is the most honest boundary statement in the review.

**Verdict**: Legitimate claim. No overreach.

### Claim 5 (Template Variable Population): Minor Overreach in Scope

engine-owner claims "variable computation is engine-only" as a hard boundary. The computation is indeed engine-only. But by framing this as a hard boundary where "templates consume but never compute," engine-owner implicitly claims sole authority over the variable contract itself. As discussed in Contested Territory 3, the variable contract is shared: the engine provides, the templates require, and neither side can unilaterally change the interface. engine-owner's cooperation offer (deprecation cycles for variable removal) implicitly acknowledges this shared stake, but the hard boundary framing does not.

**Verdict**: Computation claim is legitimate. Framing the variable contract as engine-only overstates scope.

---

## Verified Claims

### 1. Validation Rule Ownership (Claim 1)

Fully verified. SKILL.md lines 170-195 are engine-only. FR-001's two removals were engine-level edits. template-owner has no validation logic and should not. No contest.

### 2. Round Loop Mechanics (Claim 2)

Fully verified. The outer round loop, directory creation, lazy creation, retroactive move, and termination check ordering are all engine infrastructure with no template involvement. template-owner deferred entirely on all of these in its own review.

### 3. Phase Sequencing (Hard Boundary 1)

Fully verified. Templates cannot and should not alter phase ordering. SKILL.md lines 259-313 define the non-negotiable execution model. template-owner agrees without reservation.

### 4. Output Directory Structure (Hard Boundary 4)

Fully verified. Templates write to `{OUTPUT_PATH}`; the engine determines what that path resolves to. Directory creation, flat-vs-round layout, and retroactive moves are engine decisions. template-owner agrees.

### 5. Agent Dispatch Mechanics

Fully verified. The non-negotiable multi-agent rules (SKILL.md lines 272-284) -- one agent per output file, all agents launched in one message, context isolation, no meta-agents, phase boundaries as hard barriers -- are engine infrastructure. template-owner is agnostic to dispatch mechanics.

### 6. Limitation Honesty

engine-owner's five stated limitations are honest and well-characterized:
- Cannot validate template quality (correct -- structure vs. content)
- Depends on templates for heading consistency (correct -- producer-consumer asymmetry)
- Cannot enforce variable consumption (correct -- unused variables are template's right)
- Cannot prevent spec-implementation drift (correct -- organizational concern)
- DISPUTES_BEGIN/END marker gap (correct -- requires template-owner action)

These limitations demonstrate self-awareness about the engine's scope boundaries. No hiding of weaknesses detected.

---

## Cooperation Opportunities

### 1. Dispute Heading Stabilization

engine-owner's Limitation 2 identifies heading inconsistencies (winner-take-all uses "Remaining Contested Positions" instead of "Remaining Disputes"; prisoners-dilemma uses "Remaining Disputed Boundaries" instead of "Disputed Boundaries"). The engine tolerates these via substring matching (SKILL.md line 681), but they are technical debt.

**Proposal**: template-owner audits all synthesis and cross-round-synthesis templates for heading consistency against the Dispute-Parsing Subsystem's documented headings (SKILL.md lines 674-678). Exact matches replace approximate matches. This reduces the engine's reliance on fuzzy substring matching and strengthens the stable interface contract. This is a template-owner action item that engine-owner benefits from.

### 2. DISPUTES_BEGIN/END Marker Completion

engine-owner's Limitation 5 identifies that cross-round synthesis templates omit structural markers. The engine falls back to heading-based parsing, which is functional but degraded.

**Proposal**: template-owner adds `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` markers to all cross-round-synthesis templates (red-blue, winner-take-all, prisoners-dilemma). This upgrades the engine from fallback parsing to primary parsing for cross-round outputs. This is a template-owner action item that directly improves engine reliability.

### 3. Variable Contract Documentation

engine-owner offers to document every variable with type, source, and edge cases (Cooperation Offer 1). template-owner should reciprocate by documenting which variables each template actually consumes.

**Proposal**: Each template file includes a comment block listing consumed variables. This makes the variable interface explicitly bilateral: engine-owner documents what is available, template-owner documents what is consumed. Unused variables become visible to both parties without runtime enforcement. This benefits future template authors who engine-owner (Limitation 3) correctly notes may not know a variable exists.

### 4. Stale Comment Cleanup

engine-owner commits to fixing the "cooperative mode only" comment on SKILL.md line 34 (Cooperation Offer 4). This is a low-cost, high-value coordination item. template-owner supports this and notes that any stale mode-gating language elsewhere in SKILL.md should be swept in the same pass.

---

## Updated Boundary Proposal

Based on this cross-review, the boundary map should be:

### Engine-Owner Territory (exclusive)

1. **Validation rules** -- all of SKILL.md lines 170-195. Undisputed.
2. **Phase sequencing and execution model** -- SKILL.md lines 259-313. Undisputed.
3. **Round loop mechanics** -- outer loop, termination checks, directory creation, lazy creation, retroactive moves. Undisputed.
4. **Stagnation comparison logic** -- count >= prior = stagnation. Undisputed.
5. **Dispute-Parsing Subsystem implementation** -- parsing rules, marker-based and heading-based extraction, substring matching. Undisputed.
6. **Variable computation** -- resolving paths, counting disputes, determining termination reasons, substituting into templates. Undisputed.
7. **Output directory structure** -- flat vs. round layout, path resolution, `{OUTPUT_PATH}` determination. Undisputed.
8. **Agent dispatch mechanics** -- parallelism rules, one-agent-per-file, context isolation. Undisputed.

### Template-Owner Territory (exclusive)

1. **Mode-specific prompt engineering** -- game-theoretic framing, scoring models, behavioral constraints, identity prompts. Undisputed.
2. **Output content structure** -- section ordering, sub-headings, tables, analysis frameworks within required sections. Undisputed.
3. **Agent behavioral constraints** -- third-person rules, length guidelines, do-not-introduce rules. Undisputed.
4. **Cross-round narrative strategy** -- how to frame multi-round evolution per mode. Undisputed.
5. **Dispute heading definitions** -- template-owner is the authority on what headings are produced. Engine-owner indexes these headings for parsing. template-owner is upstream.
6. **Phase 6 heading definitions** -- template-owner's arbitration templates define the required headings. Engine-owner's validation table (SKILL.md lines 586-593) is a derived index that must track template changes.

### Shared Interface (bilateral coordination required)

1. **Stable interface contract (SKILL.md line 683)** -- the dispute headings and structural markers. Template-owner produces them; engine-owner consumes them. Changes require bilateral coordination. template-owner is the upstream authority; engine-owner is the enforcement mechanism.
2. **Phase 6 heading table synchronization** -- template-owner defines headings in arbitration templates; engine-owner mirrors them in the validation table. Template changes trigger engine table updates in the same change. Flow is template-defines, engine-follows (SKILL.md line 594).
3. **Template variable contract** -- engine-owner defines and documents available variables; template-owner consumes documented variables. Neither side adds or removes variables without coordination. engine-owner provides deprecation cycles for removals; template-owner does not consume undocumented variables.

### Key Correction from engine-owner's Proposal

engine-owner's Hard Boundary 3 ("Variable computation is engine-only") is accepted for computation but rejected as a framing of the full variable relationship. Computation is engine-only. The variable contract (which variables exist, their semantics, their stability guarantees) is a shared interface. engine-owner's own cooperation offer (deprecation cycles, documentation commitments) implicitly recognizes this. The updated boundary makes it explicit.

engine-owner's Shared Interface framing of dispute headings as a "bilateral contract" is accepted for change management but amended to reflect the directional dependency: template-owner is the upstream producer and the authority on what headings are correct. The engine's parsing rules are derived from template content. "Bilateral" describes the coordination protocol, not the authority structure.

---

## Summary Assessment

engine-owner's review is thorough, well-evidenced, and largely honest. The territorial claims are narrow and defensible. The limitations section is genuinely self-aware -- particularly the admission that the engine cannot validate content quality, cannot prevent heading inconsistencies, and cannot enforce variable consumption. These are real architectural boundaries, not rhetorical concessions.

The two areas of overreach are both framing issues rather than capability grabs:
1. Describing dispute headings as a "bilateral contract" obscures template-owner's upstream authority.
2. Framing variable computation as a hard boundary implicitly extends to the variable contract itself, which is shared.

Neither overreach is severe. engine-owner does not claim template territory (prompt engineering, content structure, behavioral framing). engine-owner does not attempt to expand the engine's role into content validation. The review's cooperation offers are genuine and actionable.

The engine-template boundary in conversus is clean. This cross-review confirms that the boundary holds under scrutiny. The refinements proposed here are about precision of framing, not territorial disputes.
