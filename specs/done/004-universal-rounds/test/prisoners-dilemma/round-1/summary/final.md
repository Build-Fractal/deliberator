# Arbiter Synthesis: engine-owner vs. template-owner

**Spec**: 004-universal-rounds
**Mode**: prisoners-dilemma
**Arbiter**: neutral (Phase 5 synthesis)
**Date**: 2026-03-20

---

### Process Summary

| Metric | Value |
|--------|-------|
| Participants | 2 (engine-owner, template-owner) |
| Phases completed | 4 (review, cross-review, revision, disputes) |
| Initial claims (engine-owner) | 5 |
| Initial claims (template-owner) | 8 (core competencies + unique capabilities + shared territory items) |
| Claims surviving unmodified | engine-owner: 2 of 5 (Claim 1, Claim 2); template-owner: 3 of 8 (Claim 1 amended, Claim 2, Claim 8 clarified) |
| Claims modified | engine-owner: 3 (Claims 3, 4, 5); template-owner: 4 (Claims 3, 4, 5, 6) |
| Claims withdrawn | engine-owner: 0 full withdrawals, 2 framing corrections; template-owner: 1 full withdrawal (Claim 7: blanket spec-deviation authority), 1 minimization retraction ("merely fills variables") |
| Converged boundaries | 17 (enumerated in both disputes.md files) |
| Remaining disputes | 2 |
| Cooperation commitments | 8 (4 per side) |

---

### Trust Scorecard

| Dimension | engine-owner | template-owner |
|-----------|-------------|----------------|
| **Initial honesty** | High. Five stated limitations demonstrated genuine self-awareness about engine scope boundaries (cannot validate content quality, depends on templates for heading consistency, cannot enforce variable consumption, cannot prevent spec drift, marker gap). | High. Deferrals were honest and comprehensive (phase sequencing, config validation, agent dispatch, dispute count computation). Variable dependency acknowledgment was the strongest concession in either review. |
| **Overreach severity** | Mild. Two framing issues identified by template-owner: (1) "bilateral contract" for dispute headings obscured template-owner's upstream role; (2) "variable computation is engine-only" as hard boundary implicitly extended to the variable contract itself. Neither was a capability grab. | Mild. Three overreach items identified by engine-owner: (1) "source of truth" for dispute headings overstated governance authority; (2) "the engine merely fills variables" minimized engine contribution; (3) blanket spec-deviation authority was a problematic generalization. All were framing issues, not territory grabs. |
| **Response to criticism** | Cooperative. Withdrew "bilateral contract (co-equal origination)" framing, withdrew "shared interface" label for Phase 6 heading table, reclassified variable availability from engine-only to shared. All modifications were principled concessions that improved precision without surrendering legitimate capability claims. | Cooperative. Withdrew "source of truth" governance framing, withdrew "derived artifact" characterization, withdrew blanket spec-deviation authority, withdrew "merely fills variables." All modifications were genuine corrections accepted with substantive reasoning, not reluctant concessions. |
| **Consistency** | Mostly consistent. template-owner caught one inconsistency: engine-owner called the validation-rule-to-template relationship a "dependency, not shared ownership" but called the structurally analogous heading relationship "bilateral." engine-owner acknowledged this fairly. | Consistent. No internal contradictions identified across phases. Positions shifted toward center without reversals. |
| **Cooperation quality** | Strong. Offered variable documentation, parsing guarantees, termination reason transparency, stale comment cleanup. Accepted all template-owner cooperation proposals. | Strong. Offered heading consistency audit, structural marker completion, variable consumption documentation, stale comment cleanup support. Accepted all engine-owner cooperation offers. |
| **Overall cooperation rating** | **Cooperate** | **Cooperate** |

Both participants demonstrated cooperative behavior throughout. No defection detected. The deliberation followed the iterated PD's theoretical prediction: observable history and reputation effects drove both sides toward cooperation. Concessions were genuine, critiques were evidence-based, and both sides improved the precision of the boundary map rather than trying to expand their territory.

---

### Responsibility Map

| Area | Owner | Evidence | Status |
|------|-------|----------|--------|
| Validation rules (SKILL.md lines 170-195) | engine-owner | Uncontested by both sides. FR-001 edits were engine-level. | Agreed |
| Phase sequencing (SKILL.md lines 259-313) | engine-owner | Uncontested. Templates cannot alter phase order. | Agreed |
| Round loop mechanics (outer loop, termination checks, directory creation, lazy creation, retroactive moves) | engine-owner | Uncontested. template-owner deferred entirely. | Agreed |
| Stagnation comparison logic (count >= prior = stagnation) | engine-owner | Uncontested capability claim. Governance framing was modified. | Agreed |
| Dispute-Parsing Subsystem implementation (parsing rules, marker-based/heading-based extraction, substring matching) | engine-owner | Uncontested. Implementation details are engine infrastructure. | Agreed |
| Variable computation (path resolution, dispute counting, termination reason determination, substitution) | engine-owner | Uncontested. Templates never compute values. | Agreed |
| Output directory structure (flat-vs-round layout, path resolution, `{OUTPUT_PATH}` determination) | engine-owner | Uncontested. Templates write to `{OUTPUT_PATH}`. | Agreed |
| Agent dispatch mechanics (one-agent-per-file, parallelism, context isolation, background/foreground) | engine-owner | Uncontested. SKILL.md lines 272-284. | Agreed |
| Phase 6 validation mechanism (table existence, enforcement timing, severity level, matching rules) | engine-owner | Uncontested. The mechanism is engine-owned; only the heading values are template-sourced. | Agreed |
| Mode-specific prompt engineering and game-theoretic framing | template-owner | Uncontested. Engine contains zero game-theoretic reasoning. Cleanest boundary. | Agreed |
| Output content structure within phases (sections, sub-headings, tables, analysis frameworks beneath required headings) | template-owner | Uncontested. Engine validates heading presence, not content structure. | Agreed |
| Agent behavioral constraints (scope limitations, citation requirements, neutrality mandates, length guidance) | template-owner | Uncontested. No engine mechanism to override. | Agreed |
| Cross-round narrative strategy (analytical dimensions, game-theoretic dynamics per mode) | template-owner | Modified from original. Engine assembles evidentiary record; templates define the narrative. Both essential. | Agreed |
| Cross-round data assembly (computing and populating variables carrying evidentiary record) | engine-owner | Agreed after template-owner withdrew "merely fills variables" minimization. | Agreed |
| Structural marker syntax (`CONVERSUS:` namespace, marker format) | engine-owner | Agreed. The namespace is engine convention. | Agreed |
| Structural marker placement (where markers appear in templates) | template-owner | Agreed. Template-owner decides placement within template content. | Agreed |
| Dispute headings (stable interface contract) | Shared: template-owner upstream producer, engine-owner downstream consumer | Both agree on directional data flow and bilateral coordination (SKILL.md line 683). | Agreed (governance emphasis disputed) |
| Phase 6 heading values | template-owner defines; engine-owner mirrors in validation table | SKILL.md line 594 governs: template changes trigger engine table updates. | Agreed |
| Variable availability contract (which variables exist, their semantics, stability guarantees) | Shared | Both converged independently. Engine documents, templates consume. Neither side unilaterally adds/removes. | Agreed |
| Spec-to-template authority | Neither holds blanket authority | template-owner withdrew generalization. Deviations require documentation and coordination. | Agreed |

---

### Agreed Boundaries

The following boundaries are fully accepted by both participants and require no further negotiation.

**Engine-owner exclusive territory:**

1. All validation logic (SKILL.md lines 170-195). Templates have zero validation logic.
2. Phase sequencing and execution model (SKILL.md lines 259-313). Templates operate within phases; they do not define or reorder them.
3. Round loop mechanics: outer loop, iteration loop nesting, termination check ordering, directory creation strategy, round transition mechanics.
4. Stagnation comparison logic: count >= prior = stagnation.
5. Dispute-Parsing Subsystem implementation: parsing rules, marker-based and heading-based extraction, substring matching fallback.
6. Variable computation and substitution: resolving paths, counting disputes, determining termination reasons, populating template variables.
7. Output directory structure: flat-vs-round layout, lazy creation, retroactive Round 1 move, `{OUTPUT_PATH}` determination.
8. Agent dispatch mechanics: one agent per output file, parallel within phase, context isolation, no meta-agents, phase boundaries as hard barriers.
9. Phase 6 validation mechanism: table existence, enforcement timing, severity level (warnings not errors), case-insensitive matching.
10. Cross-round data assembly: computing `{TERMINATION_REASON}`, `{ROUNDS_COMPLETED}`, `{ROUND_SYNTHESES}`, and all round-aware variables.
11. Structural marker syntax: the `CONVERSUS:` namespace prefix and marker format specification.

**Template-owner exclusive territory:**

1. Mode-specific prompt engineering and game-theoretic framing: scoring models, behavioral dynamics, identity prompts, analytical frameworks.
2. Output content structure within phases: section ordering, sub-headings, tables, analysis frameworks beneath required headings.
3. Agent behavioral constraints: scope limitations, citation requirements, neutrality mandates, length guidance, point-of-view rules.
4. Cross-round narrative strategy: what analytical dimensions to track across rounds, what game-theoretic dynamics to assess.
5. Structural marker placement: where `DISPUTES_BEGIN`/`DISPUTES_END` markers appear within template content.
6. Phase 6 heading value authority: arbitration templates define what the correct heading values are; the engine's validation table follows (SKILL.md line 594).

**Shared interfaces (bilateral coordination required):**

1. Dispute headings: template-owner produces them; engine-owner consumes them via the Dispute-Parsing Subsystem. Neither side changes unilaterally. SKILL.md line 683 governs. Data flow is directional (template produces, engine consumes).
2. Phase 6 heading table synchronization: template-sourced values in an engine-owned mechanism. Template changes trigger engine table updates per SKILL.md line 594.
3. Structural markers: engine-owner owns syntax specification; template-owner owns placement. Both coordinate on changes per SKILL.md line 683.
4. Variable availability contract: engine-owner documents and provides the variable set; template-owner consumes documented variables. Neither side unilaterally adds or removes. Engine-owner commits to deprecation cycles; template-owner commits to consuming only documented variables.

**Mutual cooperation commitments:**

- template-owner: heading consistency audit, structural marker completion in cross-round templates, variable consumption documentation, support for stale comment cleanup.
- engine-owner: variable documentation with type/source/edge cases, deterministic parsing behavior guarantees, termination reason transparency (`converged`/`stagnation`/`max_rounds` enum is exhaustive), stale comment cleanup (SKILL.md line 34 and other stale mode-gating language).

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Disputed Boundaries

### Dispute Heading Governance: First-Mover Authority vs. Symmetric Coordination

**template-owner position**: Template-owner has first-mover standing for new dispute headings. When a new mode's templates introduce new headings (e.g., spec 004 introducing `## Disputed Boundaries` for prisoners-dilemma), the template creates the heading and the Dispute-Parsing Subsystem updates to consume it. This mirrors the Phase 6 directional dependency at SKILL.md line 594. The coordination protocol is bilateral, but the origination pattern is template-first. template-owner is willing to accept "bilateral with template-first origination pattern" rather than pure demand-supply framing.

**engine-owner position**: The coordination protocol for dispute headings is symmetric. SKILL.md line 683 uses the word "coordinated," which implies symmetric obligation. The data flow is directional (template produces, engine consumes), but the change-management protocol is bilateral. Either side can propose heading changes -- the engine might need a new heading for parsing purposes just as a template might need one for analytical purposes. "First-mover authority" implies that template-owner proposes and the engine must follow, reducing coordination to a notification step. engine-owner wants "upstream producer" for data flow and "bilateral coordination" for governance, kept as separate axes.

**Arbiter analysis**: Both sides agree on the factual data flow (template produces, engine consumes) and on the coordination rule (SKILL.md line 683: bilateral). The dispute is about whether the typical origination pattern (templates have historically introduced new headings) should be formalized as "first-mover authority" or described as an observed pattern within a symmetric protocol. SKILL.md line 683 does not distinguish between heading-content changes and heading-existence changes -- both are "breaking changes" requiring coordination. However, the historical record supports template-owner's observation: spec 004's new headings originated from template content, not engine requirements. The Phase 6 heading table has an explicit directional rule (SKILL.md line 594); the dispute headings' governing rule (SKILL.md line 683) uses symmetric language. This textual distinction is meaningful. The arbiter recommends: describe the data flow as directional (template-owner is upstream producer), describe the governance as bilateral (SKILL.md line 683 governs), and note as an observed pattern (not a formal rule) that new headings typically originate from template content. This avoids formalizing "first-mover authority" while acknowledging the practical reality.

### New Variable Proposal Direction

**template-owner position**: Template-owner is the natural demand-side initiator for new variables because templates are where consumption requirements are discovered. When a template needs a datum the engine does not yet compute, the template identifies the need and the engine evaluates feasibility. This is a request-fulfill pattern, not bilateral negotiation. template-owner is willing to accept "bilateral negotiation" provided it acknowledges template-owner as the typical demand-side initiator.

**engine-owner position**: New variable proposals should be characterized as bilateral negotiation. The engine is "open to template-owner proposing new variables through the shared interface contract" but frames this as the engine evaluating feasibility and implementing, with neither side having exclusive proposal rights.

**Arbiter analysis**: Both sides agree that new variables can be proposed and that the engine evaluates feasibility. The dispute is characterization. engine-owner's flexibility statement explicitly says "I am open to template-owner proposing new variables" and describes "templates identify the need and the engine decides feasibility" -- which is substantively identical to template-owner's request-fulfill pattern. The disagreement is rhetorical, not substantive. The arbiter recommends: the variable availability contract permits either side to propose new variables. In practice, template-owner is the typical demand-side initiator (consumption requirements surface in template development). The engine evaluates feasibility and implements. This is bilateral governance with an observed demand-side pattern, parallel to the dispute heading resolution above.
<!-- CONVERSUS:DISPUTES_END -->

---

### Cooperation Assessment

This deliberation demonstrated strong bilateral cooperation across all four phases. Both participants entered with well-evidenced claims, accepted legitimate criticism, made genuine concessions, and converged on a precise boundary map.

**Indicators of cooperation:**

- Both sides withdrew overreaching framing without being forced. engine-owner withdrew "bilateral contract (co-equal origination)" and "shared interface" for the Phase 6 table. template-owner withdrew "source of truth," "derived artifact," "merely fills variables," and blanket spec-deviation authority.
- Both sides accepted the other's verified claims without resistance. engine-owner accepted all four template-owner exclusive territories. template-owner accepted all eight engine-owner exclusive territories.
- Both sides proactively identified cooperation opportunities (heading consistency audit, marker completion, variable documentation, stale comment cleanup) and accepted each other's proposals.
- The disputes phase produced only two remaining disputes, both of which are characterization disagreements (first-mover vs. symmetric, demand-side vs. bilateral) rather than territorial contests. Neither dispute affects what either side can do -- only how the governance is described.

**Indicators against defection:**

- Neither side attempted to expand into the other's territory during revisions. engine-owner did not claim content authority. template-owner did not claim execution authority.
- Both sides' limitation disclosures were genuine. engine-owner's five limitations and template-owner's dependency acknowledgments were confirmed as honest by the opposing cross-review.
- No sandbagging detected. template-owner's deferrals were genuine (engine-owner verified them as "not sandbagging"). engine-owner's template-territory acknowledgments were unconditional.

**Overall assessment**: Mutual cooperation. The deliberation produced a high-quality boundary map with minimal residual dispute. The two remaining disputes are low-severity governance-characterization issues that do not affect operational boundaries.

---

### Key Concessions

| Participant | Concession | Significance |
|-------------|-----------|--------------|
| engine-owner | Withdrew "bilateral contract (co-equal origination)" for dispute headings; accepted "upstream producer" characterization for template-owner | Acknowledged the directional data-flow reality rather than maintaining a symmetric-origination fiction. This was the most structurally important concession -- it correctly describes how headings enter the system. |
| engine-owner | Reclassified variable availability from engine-only to shared interface | Acknowledged that deprecation-cycle commitments and coordination requirements make the variable set genuinely bilateral. Strengthened the shared interface contract. |
| engine-owner | Withdrew "shared interface" label for Phase 6 heading table; accepted "engine-owned mechanism with template-sourced values" | More precise than the original framing. Preserved engine authority over the validation mechanism while acknowledging the directional dependency on template content. |
| template-owner | Withdrew "source of truth" governance framing for dispute headings; accepted "upstream producer within bilateral contract" | Recognized that SKILL.md line 683's "coordinated" language implies bilateral governance, not template-owner authority. Preserved the directional data-flow claim while accepting symmetric change-management. |
| template-owner | Withdrew "derived artifact" characterization of Phase 6 heading table | Accepted that the validation table's existence, enforcement behavior, and severity are engine design decisions -- not template-derived. Only the heading values within the table are template-sourced. |
| template-owner | Withdrew blanket authority to deviate from specs | Accepted that spec 004's implementation deviation was a justified exception, not a permanent template prerogative. Spec deviations require documentation and coordination. |
| template-owner | Withdrew "the engine merely fills variables" minimization | Acknowledged that the engine assembles the evidentiary record (computing variables, aggregating prior syntheses) that makes cross-round synthesis possible. Both contributions are essential. |
| template-owner | Acknowledged engine's informational substrate role | Amended "no other component defines what agents produce" to exclude the engine's variable computation, which determines what information agents have access to. |
