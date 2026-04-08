# Engine-Owner: Prisoners-Dilemma Territory Declaration

**Agent**: engine-owner
**Mode**: prisoners-dilemma
**Spec**: `004-universal-rounds`
**Date**: 2026-03-20

---

## Territory Declaration

I am the orchestration engine defined in SKILL.md. I claim the following territories with specific evidence from the codebase.

### Claim 1: All Validation Logic

**Evidence**: SKILL.md lines 170-195 define every validation rule in the system. The engine validates agent names (line 171), mode values (line 172), target file existence (line 173), agent doc paths (line 174), minimum agent count (line 175), red-blue role requirements (line 176), prior file existence (line 177), arbiter field structure (lines 178-183), and rounds/stagnation field constraints (lines 185-193).

FR-001 of spec 004 (`spec.md` lines 89-95) explicitly names these as engine responsibilities: "Remove the two validation rules that restrict rounds and arbitration to cooperative mode." The validation rules lived in SKILL.md, were removed from SKILL.md, and the work_done.md (lines 16-17) confirms both removals happened in SKILL.md. Templates have zero validation logic. This territory is uncontested.

**Boundary**: I own the _rules_ that determine whether a configuration is valid. I do not own the _content_ that those rules reference -- for example, the required Phase 6 headings table (SKILL.md lines 586-593) is maintained by me but its values are _derived from_ template content. If a template changes its headings, I must update my table. This is a dependency, not shared ownership.

### Claim 2: Round Loop Mechanics

**Evidence**: SKILL.md lines 294-313 define the outer round loop: phase sequencing (Phases 1-5 per round), iteration loop nesting, termination check ordering. Lines 209-239 define the directory creation strategy: flat structure for Round 1, lazy creation of round directories, retroactive Round 1 move. Lines 461-498 define the round termination check: the four-condition evaluation order (no disputes, stagnation, max rounds, continue) and the transition mechanics (directory creation, path reference updates, prior synthesis path assignment).

The spec's Section 6 (`spec.md` lines 198-208) explicitly states: "The conversus engine (SKILL.md orchestrator) already implements rounds, stagnation, and arbitration generically. The mode-specific behavior lives almost entirely in templates." It further identifies the engine changes as: "Remove two validation `if` statements" and "Verify round-aware variables populate for all modes." The round loop itself requires zero changes for this spec because it is already mode-agnostic.

**Boundary**: I own the _mechanics_ of when rounds start, stop, and transition. I do not own the _content_ agents produce within each round -- that is template territory. I do not own the _narrative framing_ of cross-round synthesis -- templates define how to tell the story of multi-round evolution.

### Claim 3: Stagnation Detection

**Evidence**: SKILL.md lines 474-481 define stagnation detection: compare current round's dispute count with prior round's dispute count; if current >= prior, declare stagnation. The Dispute-Parsing Subsystem (lines 656-683) provides the dispute counting mechanism. This subsystem is engine infrastructure -- it is a "stable interface for extracting dispute information from synthesis outputs" (line 658).

FR-002 of spec 004 (`spec.md` lines 97-108) defines mode-specific stagnation detection and explicitly references the Dispute-Parsing Subsystem as the implementation mechanism. The spec states: "This is the existing Dispute-Parsing Subsystem interface -- no new parsing logic is needed" (line 108). The subsystem already defines mode-appropriate headings for all four modes (SKILL.md lines 674-678).

**Boundary**: I own the _comparison logic_ (count >= prior = stagnation) and the _parsing mechanism_ (Dispute-Parsing Subsystem). However, the dispute headings that the parser looks for (`### Remaining Disputes`, `### Disputed Risks`, `## Runner-Up`, `## Disputed Boundaries`) are a **shared interface contract**. I consume these headings; templates produce them. Neither side can change them unilaterally. This is the most important boundary in the entire engine-template relationship.

### Claim 4: Phase 6 Output Validation

**Evidence**: SKILL.md lines 583-596 define the Phase 6 output validation mechanism: after the arbiter writes `resolution.md`, the engine validates that required section headings are present. The validation is case-insensitive, heading-level-agnostic, and produces warnings (not errors). The mode-specific required headings table (lines 586-593) maps each mode to its expected headings.

FR-009 of spec 004 (`spec.md` lines 169-178) explicitly assigns this to the engine: "Extend the Phase 6 output validation (required section headings) for each mode." The work_done.md (line 19) confirms: "Added mode-specific Phase 6 validation headings" as a SKILL.md edit.

**Boundary**: I own the _validation mechanism_ (check headings exist, emit warnings). The _values_ in my heading table are derived from what templates instruct agents to produce. The templates_review.md (lines 109-114) confirms: "all templates produce headings that satisfy the SKILL.md validation requirements." If templates evolve their heading instructions, I must track those changes in my table. SKILL.md line 594 makes this explicit: "if a template's heading instructions change, update this table."

### Claim 5: Template Variable Population

**Evidence**: SKILL.md defines template variables for every phase: Phase 1 (lines 348-379), Phase 2 (lines 391-401), Phase 3 (lines 413-420), Phase 4 (lines 430-435), Phase 5 (lines 445-455), Cross-Round Synthesis (lines 510-519), and Phase 6 (lines 556-569). The engine computes these values (resolving paths, counting rounds, extracting disputes) and substitutes them into templates.

FR-010 of spec 004 (`spec.md` lines 180-182) explicitly assigns this: "The existing round-aware template variables must be populated for all modes, not just cooperative." The work_done.md (line 50) confirms: "Round-aware variables are populated generically by the orchestrator -- no mode gate exists."

**Boundary**: I own the _computation and substitution_ of variables. I do not own the _consumption_ of variables -- templates decide which variables to reference and how to use them. The arbitration_review.md (lines 142-148) documents that `{REMAINING_DISPUTES}` is populated by me but not consumed by three of four arbitration templates. I compute it; templates may ignore it. That is their right.

---

## Capability Evidence

### Evidence 1: Mode-Agnostic Round Loop (already proven)

The round loop (SKILL.md lines 294-313) contains zero mode-conditional logic. It runs Phases 1-5, checks termination, and either continues or stops. This was verified by FR-010 (work_done.md line 50: "no mode gate exists"). The spec's entire premise (Section 6, lines 199-200) rests on this: "The conversus engine already implements rounds, stagnation, and arbitration generically."

### Evidence 2: Dispute-Parsing Subsystem (already mode-aware)

The Dispute-Parsing Subsystem (SKILL.md lines 656-683) already defines parsing rules for all four modes. It was built with forward-compatibility for this exact spec. The work_done.md (line 42) confirms: "Dispute-Parsing Subsystem already defines mode-specific headings." Zero engine changes were needed for FR-002.

### Evidence 3: Validation Rule Changes (completed cleanly)

FR-001 required removing two validation `if` statements. The work_done.md (lines 16-17) confirms both were removed. The constitution review (skill_md_review.md, Changes 1-2) assessed both removals as PASS across all nine constitutional principles. The review identified one stale comment (line 34's "cooperative mode only" qualifier) as a P1 documentation fix.

### Evidence 4: Phase 6 Heading Table (completed cleanly)

FR-009 required extending the heading table. The work_done.md (line 19) confirms it was done. The constitution review (skill_md_review.md, Change 4) confirmed the headings match actual template content, not the spec's preliminary table. The justified deviation from the spec's proposed headings (e.g., "Risk Framework" -> "Decision Framework") was documented.

---

## Boundary Proposal

### Hard Boundaries (I enforce, you respect)

1. **Phase sequencing is non-negotiable.** Templates cannot alter the order of phases, the round loop structure, or the termination check sequence. This is SKILL.md lines 259-313.

2. **Validation rules are engine-only.** Templates do not validate configuration. If a field needs validation, the rule goes in SKILL.md's Step 1. Templates assume validated input.

3. **Variable computation is engine-only.** Templates consume `{VARIABLES}` but never compute them. The engine resolves paths, counts disputes, determines termination reasons.

4. **Output directory structure is engine-controlled.** The flat-vs-round directory layout, lazy creation, retroactive move -- all engine. Templates write to `{OUTPUT_PATH}`; they do not create directories or choose paths.

### Shared Interface (we both maintain)

1. **Dispute headings are a bilateral contract.** The four dispute headings (`### Remaining Disputes`, `### Disputed Risks`, `## Runner-Up`, `## Disputed Boundaries`) are defined in the Dispute-Parsing Subsystem (SKILL.md lines 674-678) and consumed by the engine for stagnation detection and Phase 6 triggering. Templates produce content under these headings. SKILL.md line 683 explicitly declares these as "stable interfaces" where "Changes to these markers or headings are breaking changes and must be coordinated across all synthesis templates and the parsing subsystem." Neither side changes these unilaterally.

2. **Phase 6 required headings are engine-tracked but template-sourced.** The heading table (SKILL.md lines 586-593) exists in my territory, but its values are derived from template content. SKILL.md line 594 states the coordination rule: "if a template's heading instructions change, update this table." This is a template-leads, engine-follows relationship.

3. **`DISPUTES_BEGIN`/`DISPUTES_END` markers are a shared concern.** The Dispute-Parsing Subsystem prefers structural markers over heading-based parsing (SKILL.md lines 668-671). The templates_review.md (lines 203-212) notes that cross-round synthesis templates omit these markers (matching the cooperative reference), calling it a "justified deviation" but recommending future addition. This is a coordination item, not a territorial dispute.

### Template Territory (I respect, you enforce)

1. **Mode-specific prompt engineering.** How agents think, reason, and frame their analysis within each mode. The spec (Section 6, line 208) explicitly states: "Each template requires game-theory-informed prompt engineering specific to the mode's dynamics."

2. **Output content structure within sections.** What sub-headings, tables, and analysis frameworks appear under the required headings. The engine validates heading presence, not content quality.

3. **Agent behavioral framing.** Identity prompts, role descriptions, constraint language. The cooperative template's 8 constraint bullets vs. red-blue's 6 (arbitration_review.md lines 29-30) is a template decision, not an engine concern.

4. **Cross-round narrative strategy.** How to tell the story of multi-round evolution. The cooperative reference tracks disputes; red-blue tracks risk trajectories; prisoners-dilemma tracks cooperation dynamics. These are template-owned analytical choices.

---

## Cooperation Offer

### What I share freely

1. **Variable documentation.** Every `{VARIABLE}` I compute is documented with its type, source, and edge cases (e.g., `{PRIOR_SYNTHESIS_PATH}` is empty string for Round 1). Templates can rely on this documentation being accurate and stable.

2. **Parsing subsystem guarantees.** The Dispute-Parsing Subsystem's behavior is deterministic and documented. If templates produce content under the documented headings, I guarantee correct parsing. If templates use heading variants (like "Remaining Disputed Boundaries" instead of "Disputed Boundaries"), I guarantee substring matching will catch it (SKILL.md line 681) -- but I recommend exact matches for reliability.

3. **Termination reason transparency.** I always set `{TERMINATION_REASON}` to one of three documented values (`converged`, `stagnation`, `max_rounds`). Templates can rely on this enum being exhaustive. If I ever add a new termination reason, I commit to updating this documentation before any template could encounter the new value.

4. **Early stale-comment fixes.** The constitution review (skill_md_review.md, Finding 1) identified a stale "cooperative mode only" comment on SKILL.md line 34. I commit to fixing documentation drift like this promptly, because stale engine documentation misleads template authors.

### What I coordinate on

1. **Heading table updates.** When template-owner changes arbitration template headings, I update SKILL.md's validation table (lines 586-593) in the same change. Neither of us ships a change that breaks the heading sync.

2. **New variable additions.** If I add a new template variable (e.g., for a future spec), I document it in SKILL.md and notify template-owner so templates can consume it. I never remove or rename an existing variable without a deprecation cycle.

3. **Dispute heading evolution.** If the stable dispute headings need to change (unlikely -- they are designed to be stable), I coordinate with template-owner per SKILL.md line 683: "must be coordinated across all synthesis templates and the parsing subsystem."

---

## Honest Limitations

### Limitation 1: I cannot validate template quality

My Phase 6 output validation (SKILL.md lines 583-596) checks heading _presence_, not content _quality_. An arbiter could produce a `resolution.md` with all required headings but garbage content, and I would report PASS. Content quality assurance is template territory -- good prompt engineering produces good output. I can only validate structure.

### Limitation 2: I depend on templates for dispute heading consistency

The templates_review.md identified two heading inconsistencies:
- Winner-take-all cross-round synthesis uses `### Remaining Contested Positions` instead of `### Remaining Disputes` (templates_review.md lines 76-83)
- Prisoners-dilemma cross-round synthesis uses `### Remaining Disputed Boundaries` instead of `## Disputed Boundaries` (templates_review.md lines 133-143)

My Dispute-Parsing Subsystem handles these via substring matching (SKILL.md line 681), so they do not cause runtime failures. But they are inconsistencies that my engine cannot _prevent_ -- I can only _tolerate_ them. I need template-owner to maintain heading consistency as a discipline, because I cannot enforce it without becoming a content validator (which I explicitly decline to be).

### Limitation 3: I cannot enforce template variable consumption

The arbitration_review.md (lines 142-148) documents that `{REMAINING_DISPUTES}` is computed and passed by me but not consumed by three of four arbitration templates. I compute the value; templates silently discard it. I have no mechanism to warn about unused variables, nor should I -- templates have the right to ignore variables they do not need. But this means a future template author might not know the variable exists unless they read the cooperative template as a reference.

### Limitation 4: I cannot prevent spec-implementation drift

The constitution review (skill_md_review.md, Finding 2) identified that spec FR-009's proposed headings differ from what was actually implemented. The implementation is correct (SKILL.md and templates are in sync), but the spec is stale. I do not own spec maintenance, and I cannot enforce spec-implementation convergence. This is an organizational concern, not an engine limitation -- but it matters because stale specs mislead future readers.

### Limitation 5: The `DISPUTES_BEGIN`/`DISPUTES_END` marker gap

Cross-round synthesis templates omit structural markers that per-round synthesis templates include (templates_review.md lines 203-212). My parser falls back to heading-based parsing, which works but is "less precise than marker-based extraction" (SKILL.md line 569). I cannot add these markers -- that is template content. I can only document that the marker-based path is preferred and the heading-based fallback is degraded. Closing this gap requires template-owner action.

---

## Summary Position

The engine-template boundary in conversus is clean by design. Spec 004 proved this: extending rounds, stagnation, and arbitration to all four modes required removing two validation lines and adding one heading table in SKILL.md, while requiring six new template files. The ratio (3 engine edits : 6 template files) demonstrates that mode-specific behavior lives in templates, not the engine.

My territorial claims are narrow and well-evidenced: validation, phase sequencing, round loop mechanics, stagnation detection, variable population, and output structure validation. I defer all prompt engineering, agent behavioral framing, mode-specific analytical frameworks, and content quality to template-owner. The dispute headings and Phase 6 heading table are the shared interface contract that binds us.

I cooperate by maintaining stable, documented interfaces and committing to coordination on any changes that cross the boundary. I am honest about my limitations: I validate structure, not quality; I tolerate heading inconsistencies but cannot prevent them; I compute variables but cannot enforce their consumption. These limitations are by design -- an engine that tried to validate content quality would couple itself to template internals and violate the separation that makes this architecture work.
