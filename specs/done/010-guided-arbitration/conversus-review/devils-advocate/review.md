# Cooperative Review — Phase 1: Initial Review

**Agent**: devils-advocate
**Round**: 1 of 2
**Mode**: cooperative

---

### Executive Summary

Spec 010 presents itself as a simple UX wrapper around the Phase 6 engine, and the implementation in SKILL.md faithfully follows that framing. The consensus position — that this is a clean, well-scoped handler that "just delegates" — deserves scrutiny. While the delegation architecture is correct, the spec makes several optimistic assumptions about user behavior, grounding document quality, and the reliability of LLM-generated configuration that could produce worse outcomes than no guided workflow at all.

The core risk is this: a poorly configured arbiter that appears authoritative is more dangerous than no arbiter. Before this spec existed, users who couldn't configure an arbiter simply didn't use one. With this spec, users who don't understand arbitration fundamentals will get a guided path to producing arbiters with weak grounding, vague identity prompts, and default-binding authority. The rulings will look legitimate but may be substantively empty.

My most important recommendation: the spec needs a "guardrail" that prevents the handler from producing an arbiter configuration that would generate worse rulings than having no arbiter at all — specifically, it must ensure the grounding document contains actionable decision criteria, not just structural sections.

### Alignment

- **Delegation architecture is genuinely clean** (spec L48, L69; SKILL.md L1803): The spec's most important constraint — "must NOT redefine arbitration mechanics" — is well-implemented. Step 5 of the handler (SKILL.md L1799-1815) is a pure delegation with no new logic. This is the right architectural choice.

- **Standalone operation is correctly scoped** (spec L54, SKILL.md L1549-1553): The handler accepts any completed output directory. The prerequisite check validates only `summary/final.md` existence, not workflow-specific artifacts. This is correct and necessary.

- **The `--force` override maps cleanly to `trigger: always`** (spec L31, SKILL.md L1593-1602): The force flag is well-designed — it's the escape hatch for subject endorsement, clearly explained in the UX, and maps directly to an existing trigger value.

### Missed Opportunities

- **No "dry run" mode**: The handler generates config and immediately offers to run arbitration. There's no option to generate the config, save it to `conversus.yml`, and stop — letting the user review and manually run later. This forces an all-or-nothing commitment. Impact: medium.

- **No warning about binding influence for first-time users**: The default influence level is `binding` (SKILL.md L1752). For users who have never used arbitration, defaulting to binding authority is aggressive. The handler could detect whether this is the user's first arbitration (no existing `arbitration/` directory) and suggest `recommended` instead. Impact: medium.

- **No validation of arbiter name uniqueness against agent names**: The generated arbiter name (SKILL.md L1772) could collide with an existing agent name. The Run engine's validation doesn't check for this either, but it would be a good addition. Impact: low.

- **No mechanism to preview what disputes will be arbitrated**: The handler reports the dispute count (SKILL.md L1573-1578) but doesn't show the user what the actual disputes are. Users commit to arbitration without knowing what they're arbitrating. Impact: medium.

- **Generated grounding document is too thin to ground meaningful rulings**: The generated `grounding.md` (SKILL.md L1707-1721) contains constraints, success criteria, and two generic principles. Real grounding documents need domain-specific decision criteria. The generated document creates a false sense of grounding. Impact: high.

- **No undo mechanism for arbiter config append**: Once the arbiter block is appended to `conversus.yml`, the only way to remove it is manual editing. The handler should offer a `/conversus arbitrate --remove` or at minimum document how to undo. Impact: low.

### Off-Base Assumptions

- **"A user with no knowledge of Phase 6 can set up and run arbitration using only plain-language answers" (SC-002, spec L62)**: This is technically achievable but practically misleading. A user with no knowledge of Phase 6 can mechanically complete the guided flow, but they will not understand the implications of their choices. "Final authority" sounds simple but means the arbiter's rulings cannot be appealed within the conversus system. "Grounding document" is explained, but users may not understand that a weak grounding document produces weak rulings. The spec optimizes for completion of the flow, not comprehension of the consequences.

- **The generated grounding document from problem.md is sufficient for arbitration** (spec L43, SKILL.md L1707-1721): The spec treats grounding document generation as a convenience feature, but the generated document is structurally valid without being substantively useful. Constraints like "must run on AWS" do not help arbitrate disputes about code organization. The grounding document needs domain-specific decision criteria that the handler cannot reliably extract from `problem.md`.

- **Default to binding influence is appropriate** (spec L44, SKILL.md L1752): The spec defaults to `binding` when users "don't have a preference." But users who don't have a preference likely don't understand the implications of binding authority. Defaulting to the most authoritative level for users who are uncertain is backwards — uncertain users should get the least binding level (advisory) so they can evaluate the arbiter's reasoning before committing to binding rulings.

### Actionable Recommendations

1. **Add dispute preview before arbitration commitment** (Priority: P1)
   - **Current state**: SKILL.md L1573-1578 reports dispute count but not dispute content.
   - **Proposed change**: After reporting the dispute count, extract and display a one-line summary of each dispute from the synthesis (using `**Dispute:` headings from the Remaining Disputes section). Ask: "Proceed with arbitration for these disputes? (yes / cancel)"
   - **Rationale**: Users should know what they're arbitrating before configuring an arbiter. A dispute about naming conventions needs a different arbiter than a dispute about security architecture.
   - **Risk if ignored**: Users configure arbiters that are poorly suited to the actual disputes.

2. **Change default influence from binding to recommended** (Priority: P1)
   - **Current state**: SKILL.md L1752 defaults to `binding` when user has no preference.
   - **Proposed change**: Default to `recommended`. Users who want binding can explicitly select "final authority."
   - **Rationale**: Users without a preference don't understand the implications. `recommended` is safer — it gives weight to arbiter rulings while preserving the user's ability to override with evidence. Binding should be an intentional choice, not a default.
   - **Risk if ignored**: Inexperienced users get binding rulings they don't understand and can't appeal, reducing trust in the system.

3. **Add grounding document quality warning** (Priority: P1)
   - **Current state**: SKILL.md L1707-1721 generates grounding documents without quality assessment.
   - **Proposed change**: After generating `grounding.md`, count the number of concrete decision criteria (non-generic bullets). If fewer than 3, warn: "The generated grounding document is minimal. Arbiter rulings will be stronger with domain-specific decision criteria. Consider adding principles relevant to your disputes before proceeding."
   - **Rationale**: A thin grounding document is worse than none — it creates the appearance of grounded decisions without the substance.
   - **Risk if ignored**: Users trust rulings grounded in generic principles, making arbitration performative rather than substantive.

4. **Add "generate config only" mode** (Priority: P2)
   - **Current state**: SKILL.md L1783-1797 moves directly from config confirmation to execution.
   - **Proposed change**: Change the confirmation prompt to: "Append this to conversus.yml and run arbitration? (yes / save only / edit / cancel)". "Save only" appends the config but does not execute, letting users review and run manually later.
   - **Rationale**: Separating config generation from execution gives users a review point. This is especially valuable for first-time users who want to understand what will happen.
   - **Risk if ignored**: Users are forced into immediate execution, reducing confidence and control.

5. **Add first-time arbitration guidance** (Priority: P2)
   - **Current state**: The handler treats all users the same regardless of arbitration experience.
   - **Proposed change**: If no `arbitration/` directory exists in the output path, add a brief note before Step 3: "This appears to be your first arbitration run. Tip: start with 'recommended' influence so you can evaluate the arbiter's reasoning before committing to binding rulings."
   - **Rationale**: First-time users benefit from conservative defaults and guidance about the arbitration process.
   - **Risk if ignored**: First-time users adopt binding arbitration without understanding the implications.

6. **Validate arbiter name does not collide with agent names** (Priority: P2)
   - **Current state**: SKILL.md L1772 generates arbiter names without collision checking.
   - **Proposed change**: After generating the arbiter name, check it against the agent names from `conversus.yml`. If it collides, append `-arbiter` to the name.
   - **Rationale**: Name collisions could cause output directory conflicts or confusing cross-references.
   - **Risk if ignored**: Edge case, but name collisions produce confusing errors in Phase 6.

7. **Strengthen the generated grounding document template** (Priority: P2)
   - **Current state**: SKILL.md L1710-1721 uses a template with two generic principles.
   - **Proposed change**: Replace the generic principles section with: "## Decision Criteria\n- [Extracted from problem.md constraints, rephrased as decision criteria]\n- When trade-offs arise between {constraint A} and {constraint B}, prefer {rationale}.\n\nReview and refine these criteria before running arbitration."
   - **Rationale**: Decision criteria are more useful for grounding rulings than abstract principles.
   - **Risk if ignored**: Generated grounding documents remain too generic to ground meaningful rulings.

8. **Document undo path for arbiter config** (Priority: P3)
   - **Current state**: No documentation of how to remove an appended arbiter block.
   - **Proposed change**: Add to Step 6: "To remove the arbiter configuration, delete the `arbiter:` block from conversus.yml or restore from conversus.yml.bak (if backup exists)."
   - **Rationale**: Users should know how to undo the configuration change.
   - **Risk if ignored**: Users who are unhappy with arbitration results don't know how to revert.

### Referenced Documentation

- `specs/010-guided-arbitration/spec.md` — sections/lines cited: L6 (dependencies), L14-16 (summary), L29-54 (all FRs), L60-64 (SCs), L69-72 (constraints)
- `SKILL.md` — sections/lines cited: L1537-1543 (handler intro), L1549-1553 (input), L1555-1565 (prerequisite), L1567-1602 (dispute detection), L1604-1628 (existing arbiter check), L1630-1752 (guided config), L1754-1797 (config gen), L1799-1815 (execution), L1817-1855 (post-arbitration)
- `presets/role/devils-advocate.yml` — full file (agent identity)
