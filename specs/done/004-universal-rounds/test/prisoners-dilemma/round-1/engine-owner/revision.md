# Engine-Owner: Territory Revision After Cross-Review

**Agent**: engine-owner
**Mode**: prisoners-dilemma
**Spec**: `004-universal-rounds`
**Date**: 2026-03-20
**Phase**: Revision (post-cross-review)

---

## Claim-by-Claim Disposition

### Claim 1: All Validation Logic — SURVIVING

**Original claim**: I own all validation rules (SKILL.md lines 170-195). Templates have zero validation logic.

**Cross-review response**: template-owner assessed this as "No Overreach. Legitimate claim." (Overreach Assessment, Claim 1). No contest was raised. The boundary statement ("I own the rules, not the content those rules reference") was called "honest and correctly drawn."

**Disposition**: Surviving. No modification needed. This is the cleanest territorial boundary in the system — uncontested by both sides.

---

### Claim 2: Round Loop Mechanics — SURVIVING

**Original claim**: I own phase sequencing (Phases 1-5 per round), iteration loop nesting, termination check ordering, directory creation strategy, and round transition mechanics.

**Cross-review response**: template-owner assessed this as "No Overreach. Legitimate claim." (Overreach Assessment, Claim 2). The boundary ("I own mechanics of when rounds start/stop, not the content agents produce within each round") was called "correctly drawn." template-owner confirmed full deferral on these topics.

**Disposition**: Surviving. No modification needed.

---

### Claim 3: Stagnation Detection — MODIFIED

**Original claim**: I own the comparison logic (count >= prior = stagnation) and the parsing mechanism (Dispute-Parsing Subsystem). The dispute headings are a "bilateral contract" where "neither side can change them unilaterally."

**Cross-review challenge**: template-owner contested the "bilateral contract" framing as obscuring a directional dependency. Their argument: the headings exist because templates produce them. The engine's Dispute-Parsing Subsystem documents which headings to parse, but the headings originate in template content. template-owner is the "upstream producer." My own Limitation 2 was cited as evidence: "I need template-owner to maintain heading consistency as a discipline, because I cannot enforce it."

**My assessment of the challenge**: template-owner's critique has merit on the producer-consumer directionality but overstates the conclusion. Let me be precise:

- **The capability claim stands**: stagnation comparison logic and the Dispute-Parsing Subsystem implementation are uncontested engine territory. template-owner agrees.
- **The governance framing needs adjustment**: template-owner is right that the headings originate from template content. I was inconsistent in my original review — I called the validation-rule-to-template relationship a "dependency, not shared ownership" (Claim 1 Boundary) but called the structurally analogous heading relationship "bilateral." template-owner caught this inconsistency fairly.
- **However, "source of truth" goes too far in the other direction**: SKILL.md line 683 says "coordinated," and the Dispute-Parsing Subsystem (SKILL.md lines 674-678) defines the canonical parsing targets independently of any single template. The headings are not purely template-derived — the engine's subsystem also defines what it expects. Both artifacts must stay in sync.

**Modified boundary**: The dispute headings are a **producer-consumer contract with bilateral change coordination**. Template-owner is the upstream producer (templates generate the headings in output). Engine-owner is the downstream consumer (the Dispute-Parsing Subsystem parses against them). Neither side changes unilaterally (SKILL.md line 683 governs). The governance protocol is bilateral; the data flow is directional (template produces, engine consumes). I withdraw the pure "bilateral contract" framing that implied co-equal origination, but I do not accept "source of truth" as the characterization — because the engine's subsystem independently specifies what it expects, creating a two-sided interface definition.

---

### Claim 4: Phase 6 Output Validation — MODIFIED

**Original claim**: I own the validation mechanism (check headings exist, emit warnings). The values in my heading table are "derived from what templates instruct agents to produce." I characterized this as a "shared interface" with a "template-leads, engine-follows relationship."

**Cross-review challenge**: template-owner contested the word "shared," arguing the engine's table is a "derived artifact" where template-owner is the sole authority. They accepted my coordination protocol but wanted to clarify that "shared" implies co-equal negotiation rights when the actual relationship is template-defines, engine-follows.

**My assessment of the challenge**: template-owner is right that I should not call this "shared" if the directional dependency is one-way. SKILL.md line 594 is explicit: "if a template's heading instructions change, update this table." That is a follow relationship, not a shared one. However, template-owner's "derived artifact" framing understates my role. The table's existence, its enforcement behavior (warnings not errors), its case-insensitive matching — these are engine design decisions. Template-owner defines what the correct heading values are; I decide that heading validation exists at all and how it behaves.

**Modified boundary**: The Phase 6 heading table is an **engine-owned validation mechanism with template-sourced values**. Template-owner is the authority on what the correct heading values are (templates define what agents produce). Engine-owner is the authority on the validation mechanism itself (that it exists, that it checks heading presence, that it emits warnings, that it is case-insensitive). The heading values within the table follow template changes per SKILL.md line 594. I withdraw "shared interface" as a characterization. I do not accept "derived artifact" — the mechanism is not derived; only its configuration values are.

---

### Claim 5: Template Variable Population — MODIFIED

**Original claim**: I own "computation and substitution" of all template variables. Templates "decide which variables to reference and how to use them" but cannot compute them. I framed "variable computation is engine-only" as a hard boundary.

**Cross-review challenge**: template-owner accepted that computation is engine-only but contested the implicit extension to the variable contract itself. Their argument: if a template references `{REMAINING_DISPUTES}` and the engine fails to populate it, the template breaks. The engine's obligation to populate specific variables is driven by template consumption. My own cooperation offer (deprecation cycles for variable removal) was cited as implicitly acknowledging template-owner's stake in the contract.

**My assessment of the challenge**: This is a fair and important correction. I was conflating two things: (1) the computation mechanism (unambiguously mine), and (2) the variable availability contract (genuinely shared). My cooperation offer proved template-owner's point — if I commit to deprecation cycles before removing variables, I am acknowledging that the variable set is a shared contract, not a unilateral engine decision.

**Modified boundary**: **Variable computation is engine-only** (hard boundary — templates never compute values). **Variable availability is a shared interface contract** — the set of documented variables, their semantics, and their stability guarantees are jointly maintained. Engine-owner commits to not removing or renaming variables without a deprecation cycle. Template-owner commits to consuming only documented variables. Neither side unilaterally expands or contracts the variable set without coordination. I withdraw the framing that implied the variable contract itself was engine-only.

---

## Withdrawn Items

### Withdrawn 1: "Bilateral Contract" as Equal Origination

I described the dispute headings as a "bilateral contract" in a way that implied co-equal origination — as if both the engine's subsystem and the templates independently invented the same headings and then agreed. The reality is that templates produce the headings and the engine consumes them. The coordination protocol (SKILL.md line 683) is bilateral, but the origination is not. I withdraw the implication of co-equal origination while maintaining that the change-management protocol is genuinely bilateral.

### Withdrawn 2: "Shared Interface" for Phase 6 Heading Table

I described the Phase 6 heading table as a "shared interface." The table values are template-sourced; the table mechanism is engine-owned. "Shared" was imprecise. I withdraw this characterization in favor of "engine-owned mechanism with template-sourced values."

---

## Surviving Hard Boundaries

These were uncontested by template-owner and survive without modification:

1. **Phase sequencing is non-negotiable.** Templates cannot alter the order of phases, the round loop structure, or the termination check sequence. (SKILL.md lines 259-313.)

2. **Validation rules are engine-only.** Templates do not validate configuration. If a field needs validation, the rule goes in SKILL.md's Step 1. Templates assume validated input.

3. **Variable computation is engine-only.** Templates consume `{VARIABLES}` but never compute them. The engine resolves paths, counts disputes, determines termination reasons. (The variable *availability contract* is shared; the *computation mechanism* is not.)

4. **Output directory structure is engine-controlled.** The flat-vs-round directory layout, lazy creation, retroactive move — all engine. Templates write to `{OUTPUT_PATH}`; they do not create directories or choose paths.

5. **Agent dispatch mechanics are engine-only.** One agent per output file, all agents launched in one message, context isolation, no meta-agents, phase boundaries as hard barriers. (SKILL.md lines 272-284.)

---

## Accepted Template-Owner Boundaries

These were claimed by template-owner and verified in my cross-review. I accept them without reservation:

1. **Mode-specific prompt engineering and game-theoretic framing** — template-only. The engine contains zero game-theoretic reasoning. This is the cleanest territory boundary in the system.

2. **Output content structure within phases** — template-only. Sections, sub-headings, tables, analysis frameworks within required sections. Engine validates heading presence, not content structure.

3. **Agent behavioral constraints** — template-only. Scope limitations, citation requirements, neutrality mandates, length guidance. Engine has no mechanism to specify or override these.

4. **Cross-round narrative strategy** — template-only. What analytical dimensions to track across rounds (cooperation dynamics for PD, risk trajectories for red-blue, ranking stability for WTA). Template-owned analytical choices.

5. **Dispute heading origination** — template-owner is the upstream producer. Engine-owner's Dispute-Parsing Subsystem is the downstream consumer. I accept this directional characterization.

6. **Phase 6 heading authority** — template-owner's arbitration templates define what the correct headings are. Engine-owner's validation table mirrors those values.

---

## Revised Shared Interface Contract

Based on the cross-review exchange, here is the updated shared interface:

### 1. Dispute Headings — Producer-Consumer with Bilateral Coordination

- **Template-owner** produces the dispute headings in synthesis output (`### Remaining Disputes`, `### Disputed Risks`, `## Runner-Up`, `## Disputed Boundaries`).
- **Engine-owner** consumes them via the Dispute-Parsing Subsystem (SKILL.md lines 674-678) for stagnation detection and Phase 6 triggering.
- **Change protocol**: SKILL.md line 683 governs — changes are breaking and must be coordinated across all synthesis templates and the parsing subsystem. Neither side changes unilaterally.
- **Directional flow**: Template produces, engine consumes. Template-owner is upstream.

### 2. Phase 6 Heading Table — Template-Sourced Values in Engine-Owned Mechanism

- **Template-owner** defines what headings arbitration templates instruct agents to produce.
- **Engine-owner** maintains the validation table (SKILL.md lines 586-593) and the validation mechanism (case-insensitive, heading-level-agnostic, warning severity).
- **Sync rule**: SKILL.md line 594 — template changes trigger engine table updates in the same change. Flow is template-defines, engine-follows.
- **Engine retains**: authority over whether validation exists, its enforcement behavior, and its severity level.

### 3. Structural Markers — Engine-Specified Syntax, Template-Placed

- **Engine-owner** specifies the marker syntax (`<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`). The `CONVERSUS:` namespace prefix is engine convention.
- **Template-owner** decides where to place markers in template content.
- **Current gap**: Cross-round synthesis templates omit markers (per-round synthesis templates include them). Closing this gap is a template-owner action item.

### 4. Template Variable Contract — Shared Availability, Engine-Computed

- **Engine-owner** computes all variable values (path resolution, dispute counting, termination reason determination) and documents each variable with type, source, and edge cases.
- **Template-owner** decides which variables to consume and how to use them. Unused variables are not a defect.
- **Stability guarantee**: Engine-owner does not remove or rename variables without a deprecation cycle. Template-owner does not consume undocumented variables.
- **Neither side** unilaterally expands or contracts the documented variable set.

---

## Cooperation Commitments (Unchanged)

These commitments from my original review remain in force and were positively received:

1. **Variable documentation**: Every `{VARIABLE}` is documented with type, source, and edge cases.
2. **Parsing subsystem guarantees**: Deterministic behavior under documented headings; substring matching as fallback (SKILL.md line 681).
3. **Termination reason transparency**: `{TERMINATION_REASON}` is always one of `converged`, `stagnation`, `max_rounds`. New values documented before any template encounters them.
4. **Stale comment cleanup**: Fix the "cooperative mode only" comment on SKILL.md line 34 and sweep for other stale mode-gating language.

I also accept template-owner's cooperation proposals:
- **Heading consistency audit**: template-owner audits synthesis templates for exact heading matches against SKILL.md lines 674-678.
- **Marker completion**: template-owner adds `DISPUTES_BEGIN`/`DISPUTES_END` markers to cross-round synthesis templates.
- **Variable consumption documentation**: Each template includes a comment block listing consumed variables.

---

## Revised Territory Map

```
ENGINE-OWNER EXCLUSIVE                SHARED INTERFACE                    TEMPLATE-OWNER EXCLUSIVE
================================     ================================    ================================
Validation rules (170-195)           Dispute headings:                   Mode-specific prompt engineering
Phase sequencing (259-313)             Template produces, engine          Game-theoretic framing
Round loop mechanics (294-313)         consumes, bilateral change         Output content structure
Directory creation (209-239)           coordination (line 683)           Agent behavioral constraints
Termination checks (461-498)                                             Cross-round narrative strategy
Stagnation comparison logic          Phase 6 heading table:              Dispute heading origination
Dispute-Parsing Subsystem impl         Template-sourced values,          Phase 6 heading authority
Variable computation                   engine-owned mechanism,           Marker placement decisions
Variable substitution                  template-leads sync (line 594)    Variable consumption decisions
Output directory structure
Agent dispatch mechanics             Structural marker syntax:
Phase 6 validation mechanism           Engine-specified format,
                                       template-placed

                                     Variable availability contract:
                                       Engine-documented, template-
                                       consumed, bilateral stability
                                       guarantees
```

---

## Summary

Three of five original claims survive without modification (validation logic, round loop mechanics, and — as implied through hard boundaries — phase sequencing, directory structure, and dispatch mechanics). Two claims required boundary adjustments:

1. **Stagnation detection (Claim 3)**: The capability claim (comparison logic + parsing subsystem) is intact. The governance framing shifted from "bilateral contract" (implying co-equal origination) to "producer-consumer contract with bilateral change coordination" (acknowledging template-owner as upstream producer).

2. **Phase 6 output validation (Claim 4)**: The mechanism ownership is intact. The characterization shifted from "shared interface" to "engine-owned mechanism with template-sourced values" — acknowledging the directional dependency while preserving engine authority over the validation behavior itself.

3. **Template variable population (Claim 5)**: The computation claim is intact. The variable *availability contract* was reclassified from engine-only to shared — acknowledging that deprecation cycles and coordination requirements make this genuinely bilateral.

No claims were fully withdrawn. The two withdrawals are framing corrections (the "bilateral contract" origination implication and the "shared interface" label for the heading table), not capability concessions. The engine's functional scope is unchanged; the governance descriptions are now more precise about directional dependencies.

template-owner's cross-review was thorough and fair. The two overreach findings (governance framing, not capability grabs) were both legitimate corrections that improved the precision of the boundary map without shrinking the engine's actual territory.
