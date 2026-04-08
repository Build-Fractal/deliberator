# Engine-Owner: Final Disputes

**Agent**: engine-owner
**Mode**: prisoners-dilemma
**Spec**: 004-universal-rounds
**Phase**: Disputes (final position before synthesis)

---

## Remaining Disputes

### **Dispute: Dispute Heading Governance — "First-Mover Authority" Ambiguity**

Both sides have converged significantly on this boundary. We agree on the producer-consumer directionality (template produces, engine consumes) and on bilateral change coordination (SKILL.md line 683). However, template-owner's revised position introduces the phrase "first-mover authority on heading content" (Claim 3, revised position). This phrase is imprecise and potentially overreaching.

"First-mover authority" implies that template-owner can propose heading changes and the engine must follow, with coordination being essentially a notification step. That is not what SKILL.md line 683 says. Line 683 says changes "must be coordinated across all synthesis templates and the parsing subsystem" — this is symmetric coordination language, not first-mover/follower language. The producer-consumer directionality describes data flow (templates emit headings, engine reads them), not governance priority (who initiates changes).

**Engine-owner position**: The dispute headings are a bilateral interface. Template-owner is the upstream producer (data flow). The change-management protocol is symmetric (governance). Neither side has "first-mover authority." A heading change can originate from either side — the engine might need a new heading for parsing purposes just as a template might need a new heading for analytical purposes. The coordination requirement applies equally regardless of who initiates.

**What I need from synthesis**: Drop "first-mover authority" from the final boundary description. Use "upstream producer" for the data-flow relationship and "bilateral coordination" for the governance relationship. These are two different axes and must not be conflated.

---

### **Dispute: Phase 6 Heading Table — Scope of "Template-Sourced"**

We agree on the formulation "template-sourced values in an engine-owned mechanism." The dispute is about the scope of what "template-sourced" means in practice.

Template-owner's revision (Claim 5) states that "Template-owner defines what the correct headings are via arbitration template content." This is true for the heading text values. But the set of headings that get validated — the fact that there are exactly four required headings per mode — is an engine design decision. If the engine decided that Phase 6 should validate six headings instead of four, that would be an engine change, not a template change. The template would then need to instruct agents to produce six sections, but the decision to require six is engine-originated.

The current spec (FR-009) proposes four headings per mode. Those heading values come from templates. But the cardinality and the decision to validate at all are engine decisions.

**Engine-owner position**: "Template-sourced" applies to the heading text values (what the headings say). It does not apply to the validation schema (how many headings are required, that headings are required at all, that validation is case-insensitive). Template-owner should not interpret "template-sourced values" as meaning the validation schema itself is template-governed.

**What I need from synthesis**: Clarify that "template-sourced" modifies the values, not the schema. The engine decides what to validate and how; the templates inform what values to check for.

---

## Convergence

The following boundaries are fully agreed and require no further deliberation:

1. **Validation rules are engine-only** (SKILL.md lines 170-195). Uncontested by both sides. The cleanest boundary in the system.

2. **Phase sequencing, round loop, and termination mechanics are engine-only** (SKILL.md lines 259-313). Uncontested. Templates cannot alter execution order.

3. **Mode-specific prompt engineering and game-theoretic framing are template-only**. Uncontested. The engine contains zero game-theoretic reasoning.

4. **Output content structure within phases is template-only**. Uncontested. Engine validates heading presence; templates own everything beneath those headings.

5. **Agent behavioral constraints are template-only**. Uncontested. The engine has no mechanism to specify or override scope limitations, citation requirements, or neutrality mandates.

6. **Variable computation is engine-only**. Both sides agree. Templates never compute variable values. The engine resolves paths, counts disputes, and determines termination reasons.

7. **Variable availability is a shared interface contract**. Both sides converged to this independently. The engine documents and provides variables; templates consume documented variables only. Neither side unilaterally adds or removes variables. Engine-owner commits to deprecation cycles for removals.

8. **Output directory structure is engine-controlled**. Uncontested. Flat-vs-round layout, lazy creation, retroactive Round 1 move — all engine territory. Templates write to `{OUTPUT_PATH}`.

9. **Agent dispatch mechanics are engine-only**. Uncontested. One agent per file, parallel within phase, context isolation, background/foreground decisions.

10. **Structural marker syntax is engine-specified; marker placement is template-owned**. Both sides agreed to split this by concern. The `CONVERSUS:` namespace and marker format are engine conventions. Where markers appear in template content is a template decision.

11. **Cross-round narrative strategy is template-owned; cross-round data assembly is engine-owned**. Both sides agreed after template-owner withdrew the "merely fills variables" minimization. The narrative logic (what analytical dimensions to track) is template content. The evidentiary record (computing and populating the variables) is engine infrastructure. Neither is subordinate.

12. **Dispute heading data flow is directional** (template produces, engine consumes). Both sides agree. Template-owner is the upstream producer. Engine-owner's Dispute-Parsing Subsystem is the downstream consumer.

13. **SKILL.md line 683 governs heading changes**. Both sides agree this is the authoritative rule. Changes to dispute headings or structural markers are breaking changes requiring coordination.

14. **SKILL.md line 594 governs Phase 6 heading table sync**. Both sides agree the heading values in the engine's table follow template changes. The sync direction is template-defines, engine-updates.

15. **Spec-to-template authority is not a blanket template prerogative**. Template-owner withdrew the generalization that templates have inherent authority to deviate from specs. Spec deviations require documentation and coordination.

16. **Stagnation comparison logic and Dispute-Parsing Subsystem implementation are engine-only**. Uncontested. The count-based comparison (count >= prior = stagnation) and the parsing rules are engine infrastructure.

17. **Cooperation commitments are accepted bilaterally**. Template-owner will audit heading consistency, complete structural markers in cross-round templates, and document variable consumption. Engine-owner will document all variables with type/source/edge-cases, maintain parsing subsystem guarantees, provide termination reason transparency, and clean up stale comments.

---

## Final Position Statement

### Non-Negotiables

1. **The engine's validation schema is not template-governed.** The engine decides that Phase 6 validation exists, how many headings to require, what severity to assign, and what matching rules to use. Templates inform the heading values; they do not control the validation design. This is the distinction between "template-sourced values" (accepted) and "template-governed mechanism" (rejected).

2. **Heading governance is symmetric, not first-mover/follower.** SKILL.md line 683 uses the word "coordinated," which implies symmetric obligation. The data flow is directional (template produces, engine consumes), but the change-management protocol is bilateral. Either side can propose heading changes; both sides must agree before implementation. No "first-mover authority" exists.

3. **Variable computation is engine-exclusive.** Templates consume `{VARIABLES}` but never compute them. This is the foundational separation between the engine's execution role and the templates' content role.

4. **Phase sequencing is inviolable.** The five-phase (or six-phase) execution order, the round loop structure, and the termination check sequence are engine decisions that templates cannot influence. Templates operate within phases; they do not define or reorder them.

5. **The Dispute-Parsing Subsystem is engine infrastructure.** Its implementation (parsing rules, marker detection, heading-based fallback, substring matching, default behavior) is engine-owned. Templates produce the content it parses; they do not configure its behavior.

### Flexibility

1. **I accept "upstream producer" for template-owner's heading role.** The data-flow characterization is accurate and I have no interest in contesting it. Templates generate the headings; the engine reads them. This is a factual description of the system's information flow.

2. **I accept that the variable availability contract is shared.** My original framing implied the variable set was engine-only. It is not — templates have a legitimate stake in variable stability, and my own deprecation-cycle commitment proves it. The computation is mine; the contract is ours.

3. **I accept template-owner's authority over Phase 6 heading text values.** When templates change what headings agents should produce, the engine's validation table follows (per SKILL.md line 594). I do not contest this directional dependency on the values.

4. **I am flexible on the precise language used to describe shared interfaces**, as long as the language does not imply governance asymmetry where SKILL.md specifies symmetric coordination. "Bilateral coordination," "stable interface contract," "producer-consumer with bilateral change management" — any of these formulations work, provided they do not smuggle in first-mover privilege.

5. **I am open to template-owner proposing new variables** through the shared interface contract. The engine evaluates feasibility and implements; the template motivates the need. This is a natural extension of the bilateral variable contract that neither side has yet formalized.
