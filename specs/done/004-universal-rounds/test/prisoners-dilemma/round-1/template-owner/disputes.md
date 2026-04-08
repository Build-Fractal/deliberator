# Final Disputes: template-owner

**Agent**: template-owner
**Mode**: prisoners-dilemma
**Spec**: 004-universal-rounds
**Phase**: Disputes (final, pre-synthesis)

---

## Remaining Disputes

**Dispute: "Upstream producer" vs. "bilateral interface" framing for dispute headings**

Both sides withdrew their extreme framings -- I withdrew "source of truth" and engine-owner withdrew "bilateral contract (co-equal origination)." We converged on the directional reality: templates produce, engine consumes, changes are coordinated per SKILL.md line 683.

However, there is a residual disagreement on emphasis that matters for future change governance. Engine-owner's revised territory map (Revised Shared Interface Contract, item 1) places this under "Shared Interface" and describes the coordination as fully symmetric: "Neither side changes unilaterally." My revision agrees with that coordination rule but asserts that the upstream producer has first-mover standing: when a new mode's templates introduce new dispute headings (as spec 004 does for prisoners-dilemma with `## Disputed Boundaries` and `### [` sub-headings), the template creates the heading and the engine adds it to the Dispute-Parsing Subsystem. The flow is template-first, engine-follows -- the same directional dependency engine-owner acknowledged for Phase 6 heading values at SKILL.md line 594.

Engine-owner's revision does not explicitly concede this first-mover asymmetry for dispute headings the way it does for Phase 6 headings. The dispute: does the coordination protocol for dispute headings follow the same template-first pattern as Phase 6, or is it genuinely symmetric? I hold that it is template-first: new headings originate in template content, and the Dispute-Parsing Subsystem updates to consume them. The engine does not invent headings that templates must then produce.

**Dispute: Scope of "variable availability contract" -- who proposes new variables?**

Both sides agree that the variable availability contract is shared and that neither side unilaterally removes or renames variables (engine-owner's Claim 5 revision, my Claim 8). However, the revisions are silent on the direction of new variable proposals. In practice, new template requirements surface the need for new variables. When a template needs a datum the engine does not yet compute (e.g., a hypothetical `{COOPERATION_SCORE}` for prisoners-dilemma cross-round synthesis), who initiates?

Engine-owner's revision frames the variable set as "jointly maintained" with "neither side unilaterally expand[ing] or contract[ing]" it. My position: template-owner is the natural demand-side initiator for new variables, because templates are where the consumption requirement is discovered. The engine is the supply-side implementor. This is not unilateral expansion -- it is a request-fulfill pattern where templates identify the need and the engine decides feasibility. The dispute is whether new-variable proposals should be characterized as bilateral negotiation (engine-owner's framing) or demand-supply with template as requester (my framing).

---

## Convergence

The following boundaries are fully agreed by both sides and require no further negotiation:

### Engine-Owner Exclusive Territory (accepted without contest)

1. **All validation logic** (SKILL.md lines 170-195) -- templates have zero validation logic. Cleanest boundary in the system.
2. **Phase sequencing** (Phases 1-5 per round, SKILL.md lines 259-313) -- templates cannot alter phase order, round loop structure, or termination check sequence.
3. **Round loop mechanics** -- iteration loop nesting, termination check ordering, directory creation strategy, round transition mechanics.
4. **Variable computation** -- resolving paths, counting disputes, determining termination reasons, populating template variables. Templates never compute values.
5. **Output directory structure** -- flat-vs-round layout, lazy creation, retroactive Round 1 move. Templates write to `{OUTPUT_PATH}` and do not create directories.
6. **Agent dispatch mechanics** -- one agent per output file, all agents launched in one message, context isolation, no meta-agents, phase boundaries as hard barriers.
7. **Stagnation comparison logic** -- count >= prior = stagnation. Engine-only.
8. **Dispute-Parsing Subsystem implementation** -- parsing rules, marker-based and heading-based extraction, substring matching fallback logic.

### Template-Owner Exclusive Territory (accepted without contest)

1. **Mode-specific prompt engineering and game-theoretic framing** -- the scoring models, behavioral dynamics, identity prompts, and analytical frameworks that differentiate modes. The engine contains zero game-theoretic reasoning.
2. **Output content structure within phases** -- section ordering, sub-headings, tables, analysis frameworks, and content requirements. Engine validates heading presence, not content structure beneath headings.
3. **Agent behavioral constraints** -- scope limitations, citation requirements, neutrality mandates, length guidance, point-of-view rules. No engine mechanism to specify or override these.
4. **Cross-round narrative strategy** -- what analytical dimensions to track across rounds (cooperation/defection patterns, tit-for-tat emergence, boundary stability for PD; risk trajectories for red-blue; ranking stability for WTA). Narrative logic is template content; engine assembles the evidentiary record.

### Shared Interfaces (bilateral coordination required)

1. **Dispute headings**: Template-owner is the upstream producer; engine-owner is the downstream consumer via the Dispute-Parsing Subsystem. Neither side changes unilaterally. SKILL.md line 683 governs. (Residual dispute on first-mover asymmetry noted above.)
2. **Phase 6 heading validation**: Template-owner defines what the correct headings are. Engine-owner owns the validation mechanism (table existence, enforcement timing, severity, matching rules). SKILL.md line 594 governs the directional dependency: template-sourced values in an engine-owned mechanism.
3. **Structural markers** (`DISPUTES_BEGIN`/`DISPUTES_END`): Engine-owner owns the marker syntax specification (the `CONVERSUS:` namespace). Template-owner owns marker placement within template content. Both coordinate on changes per SKILL.md line 683.
4. **Template variable contract**: Engine-owner computes all values and documents the variable set. Template-owner decides consumption. Neither side unilaterally adds or removes variables. Engine-owner commits to deprecation cycles; template-owner commits to consuming only documented variables. (Residual dispute on new-variable proposal direction noted above.)

### Withdrawn Claims (mutual)

- **template-owner**: Withdrew "source of truth" (governance), "derived artifact" (Phase 6 table), blanket spec-deviation authority, and "the engine merely fills variables."
- **engine-owner**: Withdrew "bilateral contract" (co-equal origination) and "shared interface" (Phase 6 heading table).

### Cooperation Commitments (mutual)

- **template-owner**: Heading consistency audit, structural marker completion in cross-round templates, variable consumption documentation, support for stale comment cleanup.
- **engine-owner**: Variable documentation with type/source/edge cases, deterministic parsing behavior, termination reason transparency, stale comment cleanup.

---

## Final Position Statement

### Non-Negotiables

1. **Template-owner is the upstream producer of dispute headings.** The data flow is directional: templates produce headings, the engine consumes them. This is not "co-equal origination." The coordination protocol (SKILL.md line 683) is bilateral; the origination is not. When spec 004 adds prisoners-dilemma with `## Disputed Boundaries`, the template creates that heading and the Dispute-Parsing Subsystem adds it to its list. This directional reality must be reflected in any synthesized boundary map.

2. **Mode-specific prompt engineering is exclusively template territory.** The engine is mode-agnostic (confirmed by both sides). All game-theoretic reasoning, behavioral dynamics, scoring models, and narrative strategy live in templates. No engine component should ever contain mode-specific analytical logic.

3. **Cross-round narrative ownership is template-only, data assembly is engine-only.** The engine assembles the evidentiary record (computing variables, aggregating prior syntheses). The template defines what to do with that record (what dimensions to analyze, what patterns to identify). Both contributions are essential; neither is subordinate. I will not accept any framing that subordinates the narrative to the data or vice versa.

4. **Template-owner defines the correct Phase 6 heading values.** The directional dependency at SKILL.md line 594 is clear: when templates change, the engine's validation table updates. The validation mechanism is engine-owned; the heading values track template content.

### Flexibility

1. **Coordination protocol symmetry for dispute headings.** I hold that template-owner has first-mover standing for new headings, but I can accept a synthesis that describes the coordination as "bilateral with template-first origination pattern" rather than insisting on a pure demand-supply framing. The key requirement is that the directional flow (template produces, engine consumes) is explicitly stated in the final boundary map.

2. **New variable proposal process.** I can accept "bilateral negotiation" as the governance model for new variables, provided it acknowledges that template-owner is the typical demand-side initiator. I do not need exclusive proposal rights -- I need the pattern to reflect that consumption requirements drive variable creation, not the reverse.

3. **"Jointly maintained" variable contract.** I accept engine-owner's "jointly maintained" framing for the overall variable set, provided it does not imply that the engine can unilaterally decide which variables templates should consume. The stability guarantees (deprecation cycles, documented-only consumption) are sufficient safeguards.

4. **Structural marker syntax ownership.** I fully accept that engine-owner owns the `CONVERSUS:` namespace and marker format. I retain placement decisions. This split is clean and I have no residual dispute here.
