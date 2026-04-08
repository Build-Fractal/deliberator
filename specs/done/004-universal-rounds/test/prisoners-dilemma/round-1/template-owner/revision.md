# Territory Revision: template-owner

**Agent**: template-owner
**Mode**: prisoners-dilemma
**Spec**: 004-universal-rounds
**Phase**: Revision (post cross-review)

---

## Claim-by-Claim Disposition

### Claim 1: Mode-specific agent behavior definition

**Status: Surviving**

engine-owner verified this as "template-owner's strongest and most legitimate claim" (cross-review, Verified 1). The seven template files under `templates/prisoners-dilemma/` encode PD-specific framing -- trust scorecards, cooperation/defection tracking, boundary dispute format, subject arbitration with boundary rulings. The engine is mode-agnostic (confirmed by work_done.md line 50: "no mode gate exists"). No contest from either side.

engine-owner flagged (Overreach 1) my statement that "No other component in the system defines what agents produce or how they frame their arguments" as mild overreach, noting that the engine's variable computation (e.g., `{PRIOR_ROUND_SECTION}`, `{REMAINING_DISPUTES}`) determines what information agents have access to. This is a fair correction. The claim survives with the following amendment: **No other component defines the narrative framing, analytical structure, or game-theoretic dynamics of agent outputs. The engine determines the informational substrate available to agents; the templates determine how that substrate is shaped into analysis.**

### Claim 2: Output format definition

**Status: Surviving**

engine-owner verified this without contest (cross-review, Verified 2): "template-owner legitimately owns the output format within each phase... The engine validates heading presence but does not define or constrain content structure beneath those headings." No boundary adjustment needed.

### Claim 3: Dispute heading conventions -- "source of truth" framing

**Status: Modified**

This is the most significant contested claim. My Phase 1 review stated: "template-owner is the source of truth for what these markers are and where they appear."

engine-owner's cross-review (Contested Territory 1) argues this is overreach, citing SKILL.md line 683: "Changes to these markers or headings are breaking changes and must be coordinated across all synthesis templates and the parsing subsystem." The word "coordinated" implies bilateral governance. engine-owner further notes that the Dispute-Parsing Subsystem (SKILL.md lines 674-678) defines a canonical list of headings the engine parses against, and that list is not derived from the templates -- both artifacts must be kept in sync.

My own cross-review of engine-owner (Contested Territory 1) argued that template-owner is the upstream producer and therefore the authority on what headings are. I cited engine-owner's Limitation 2 admission that the engine "cannot enforce heading consistency without becoming a content validator" as evidence of the producer-consumer asymmetry.

**Revised position**: I withdraw the "source of truth" framing as applied to governance. The headings are a bilateral interface governed by SKILL.md line 683. However, the directional dependency remains real: templates produce the headings, the engine consumes them. Template-owner is the upstream producer, which gives it first-mover authority on heading content -- but not unilateral authority. Changes to headings require coordination with engine-owner because the Dispute-Parsing Subsystem must be updated in lockstep.

**Revised boundary**: Dispute headings are a shared interface with bilateral coordination requirements. Template-owner is the upstream producer (defines what headings exist in template content). Engine-owner is the downstream consumer (parses and indexes those headings). Neither side changes unilaterally. The "stable interface contract" at SKILL.md line 683 is the governing rule.

### Claim 4: Cross-round narrative framing

**Status: Modified**

engine-owner's cross-review (Overreach 2) flagged my statement that "the engine merely fills variables and dispatches agents" as "accurate but misleadingly framed." engine-owner correctly notes that the engine computes `{TERMINATION_REASON}`, `{ROUNDS_COMPLETED}`, and `{ROUND_SYNTHESES}` -- the evidentiary record that makes cross-round synthesis possible. The engine does more than "merely fill variables."

**Revised position**: The cross-round narrative logic (cooperation dynamics tracking, boundary trajectory analysis, tit-for-tat assessment) is exclusively template-owned content. The engine assembles the evidentiary record that feeds that narrative. Both contributions are essential -- the narrative is meaningless without the data, and the data is unstructured without the narrative. I withdraw the "merely" minimization.

**Revised boundary**: Cross-round narrative strategy (what analytical dimensions to track, what game-theoretic dynamics to assess) is template-owner territory. Cross-round data assembly (computing and populating the variables that carry the evidentiary record) is engine-owner territory. Both are necessary; neither is subordinate.

### Claim 5: Phase 6 required headings -- "derived artifact" framing

**Status: Modified**

My Phase 1 review characterized the engine's validation table (SKILL.md lines 586-593) as "a derived artifact" where "template-owner is the authority on what headings are correct" and "the engine validation table follows."

engine-owner's cross-review (Contested Territory 2) accepts the directional dependency (templates define, engine tracks) and cites SKILL.md line 594 in agreement. However, engine-owner correctly argues that calling the table a "derived artifact" understates the engine's role: "The engine owns the validation mechanism and decides what to validate, when to validate, and what severity to assign (warning, not error). The table values follow templates, but the table's existence and enforcement are engine decisions."

**Revised position**: I withdraw the "derived artifact" characterization. The heading values in the table are template-sourced -- they must track what templates instruct agents to produce (per SKILL.md line 594). But the validation table itself, its enforcement behavior, and its severity model are engine decisions. "Template-sourced values in an engine-owned mechanism" (engine-owner's formulation) is more accurate than "derived artifact."

**Revised boundary**: Template-owner defines what the correct headings are (via arbitration template content). Engine-owner owns the validation mechanism (the table's existence, enforcement timing, severity level, matching rules). The directional dependency at SKILL.md line 594 governs the heading values: when templates change, the table updates. But the table is not a template artifact -- it is an engine artifact whose values are sourced from templates.

### Claim 6: `DISPUTES_BEGIN`/`DISPUTES_END` structural markers

**Status: Modified**

engine-owner's cross-review (Contested Territory 3) makes a fair point: the marker syntax (`<!-- CONVERSUS:DISPUTES_BEGIN -->`) uses the `CONVERSUS:` namespace prefix, which is an engine-level convention. The parsing rules that consume these markers (SKILL.md lines 668-671) are engine infrastructure. My claim to be "source of truth" for the markers conflated marker placement (where they appear in templates) with marker definition (what they look like and how they are parsed).

**Revised position**: Engine-owner owns the marker syntax specification (the `CONVERSUS:` namespace and the marker format). Template-owner owns marker placement (where markers appear within template content). Both sides coordinate on changes per SKILL.md line 683.

### Claim 7: Spec-to-template authority

**Status: Withdrawn**

My Phase 1 review extrapolated from spec 004's implementation experience into a general principle: "the spec proposes, the template implements, and the engine validates what the template actually produces."

engine-owner's cross-review (Overreach 3) correctly identifies this as problematic: "This framing gives templates unilateral authority to deviate from specs... spec deviations should be documented and justified, not normalized as a template prerogative."

**Revised position**: For spec 004, the templates correctly implemented headings that diverged from FR-009's proposed table, and SKILL.md was updated to match the templates. This was a justified implementation decision. But I withdraw the generalization. Templates do not have blanket authority to deviate from specs. Spec deviations should be documented and coordinated, not treated as a template prerogative. The engine has a legitimate interest in spec fidelity because stale specs mislead future implementers.

### Claim 8: Template variable contracts -- semantic consumption ownership

**Status: Surviving (with clarification)**

My Phase 1 review stated that template-owner defines the "semantic contract for how variables are consumed." engine-owner did not contest this specific point. My cross-review of engine-owner (Contested Territory 3) further established that the variable contract is shared: the engine cannot arbitrarily remove a variable without breaking templates that consume it, and engine-owner's own cooperation offer (deprecation cycles) implicitly recognizes this.

**Revised position**: Variable computation is engine territory (undisputed). Variable availability -- which variables exist, their documented semantics, and their stability guarantees -- is a shared interface. Template-owner depends on the engine providing documented variables; the engine depends on templates consuming only documented variables. Neither side unilaterally adds or removes from the contract.

---

## Cooperation Commitments

Based on both cross-reviews, template-owner commits to the following cooperation items:

1. **Heading consistency audit**: Audit all synthesis and cross-round-synthesis templates for heading consistency against the Dispute-Parsing Subsystem's documented headings (SKILL.md lines 674-678). Replace approximate matches with exact matches. This reduces engine reliance on substring matching.

2. **Structural marker completion**: Add `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` markers to all cross-round-synthesis templates (red-blue, winner-take-all, prisoners-dilemma). This upgrades the engine from fallback parsing to primary parsing for cross-round outputs.

3. **Variable consumption documentation**: Add comment blocks to template files listing consumed variables. This makes the variable interface explicitly bilateral.

4. **Support stale comment cleanup**: Support engine-owner's effort to fix the "cooperative mode only" comment on SKILL.md line 34 and any other stale mode-gating language.

---

## Revised Territory Map

### Template-Owner Exclusive Territory

1. **Mode-specific prompt engineering and game-theoretic framing** -- the scoring models, behavioral dynamics, identity prompts, and analytical frameworks that differentiate modes. No other component contains game-theoretic reasoning. *Undisputed.*

2. **Output content structure within phases** -- section ordering, sub-headings, tables, analysis frameworks, and content requirements that define each phase's output format. The engine validates heading presence; templates define everything beneath those headings. *Undisputed.*

3. **Agent behavioral constraints** -- scope limitations, citation requirements, neutrality mandates, length guidance, point-of-view rules. These are exclusively template content with no engine mechanism to specify or override them. *Undisputed.*

4. **Cross-round narrative strategy** -- what analytical dimensions to track across rounds, what game-theoretic dynamics to assess (cooperation/defection patterns, tit-for-tat emergence, boundary stability). The narrative logic is template content; the engine assembles the evidentiary record that feeds it. *Modified: acknowledge engine's data assembly contribution without conceding narrative ownership.*

### Engine-Owner Exclusive Territory (accepted without contest)

1. **Phase sequencing, round loop, and termination mechanics** -- the execution model, outer loop, directory creation, retroactive moves, termination checks.
2. **All validation logic** -- SKILL.md lines 170-195, preset resolution, target resolution, error formatting.
3. **Variable computation and substitution** -- resolving paths, counting disputes, determining termination reasons, populating template variables.
4. **Output directory structure** -- flat vs. round layout, path resolution, `{OUTPUT_PATH}` determination.
5. **Agent dispatch mechanics** -- parallelism rules, one-agent-per-file, context isolation, background/foreground decisions.
6. **Stagnation comparison logic** -- count >= prior = stagnation.
7. **Dispute-Parsing Subsystem implementation** -- parsing rules, marker-based and heading-based extraction, substring matching logic.

### Shared Interfaces (bilateral coordination required)

1. **Dispute headings (stable interface contract, SKILL.md line 683)**: Template-owner is the upstream producer (defines what headings exist in template content). Engine-owner is the downstream consumer (parses and indexes those headings via the Dispute-Parsing Subsystem). Neither side changes unilaterally. The "coordinated" requirement at line 683 governs. *Modified from "source of truth" to "upstream producer within bilateral contract."*

2. **Phase 6 heading validation**: Template-owner defines what the correct headings are via arbitration template content. Engine-owner owns the validation mechanism (the table at SKILL.md lines 586-593, enforcement timing, severity model, matching rules). The directional dependency at SKILL.md line 594 governs: template changes trigger engine table updates. The heading values are template-sourced; the table itself is engine-owned infrastructure. *Modified from "derived artifact" to "template-sourced values in engine-owned mechanism."*

3. **Structural markers (`DISPUTES_BEGIN`/`DISPUTES_END`)**: Engine-owner owns the marker syntax specification (the `CONVERSUS:` namespace, marker format, parsing semantics). Template-owner owns marker placement (where markers appear in templates). Both coordinate on changes per SKILL.md line 683. *Modified from template "source of truth" to split ownership by concern.*

4. **Template variable contract**: Engine-owner owns computation and defines the available variable set. Template-owner owns consumption decisions (which variables to use, where, how). The variable availability contract is shared -- neither side unilaterally adds or removes variables. Engine-owner commits to deprecation cycles for removals; template-owner commits to consuming only documented variables. *Clarified from Phase 1.*

### Withdrawn Claims

1. **"Source of truth" for dispute headings**: Withdrawn as governance framing. Replaced with "upstream producer within bilateral contract." The coordination requirement at SKILL.md line 683 is the governing rule, not template-owner authority.

2. **Engine validation table as "derived artifact"**: Withdrawn. The heading values track templates (per SKILL.md line 594), but the table's existence and enforcement behavior are engine-owned decisions. "Template-sourced values in an engine-owned mechanism" is the accurate characterization.

3. **Blanket authority to deviate from specs**: Withdrawn as a general principle. Spec 004's implementation correctly followed templates over a stale FR-009 table, but this was a justified exception, not a permanent template prerogative. Spec deviations require documentation and coordination.

4. **"The engine merely fills variables"**: Withdrawn as minimizing framing. The engine assembles the evidentiary record that makes cross-round synthesis possible. Both contributions are essential.
