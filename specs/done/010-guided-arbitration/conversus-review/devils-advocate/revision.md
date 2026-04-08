# Cooperative Revision — Phase 3

**Agent**: devils-advocate
**Round**: 1 of 2
**Mode**: cooperative
**Iteration**: 1

---

### Recommendation Dispositions

#### Recommendation 1: Add dispute preview before arbitration commitment
- **Original position**: Extract and display one-line dispute summaries before the user configures an arbiter.
- **Disposition**: Modified
- **Explanation**: Integration-architect's cross-review (cross-reviews/devils-advocate.md, Dangerous Contradictions, "Dispute preview scope") correctly identifies that this requires extending the Dispute-Parsing Subsystem to extract content, not just count. The current subsystem returns boolean/count (SKILL.md L756-758). I accept that this is a larger change than originally scoped.
- **Modified recommendation**: In Step 1, after reporting the dispute count, extract dispute labels from the synthesis by parsing `**Dispute:` entries under the Remaining Disputes heading. Display each label as a one-liner. This uses heading-based parsing that already exists in the subsystem (SKILL.md L768) — it's an extension of the existing count logic to also capture labels, not a new subsystem capability. If label extraction fails, display only the count (current behavior as fallback).

#### Recommendation 2: Change default influence from binding to recommended
- **Original position**: Default to `recommended` instead of `binding` for users without a preference.
- **Disposition**: Surviving
- **Explanation**: Integration-architect's cross-review (cross-reviews/devils-advocate.md, Dangerous Contradictions) argues that changing the default in the handler while the Run engine defaults to `binding` creates inconsistency. Functional-typing's cross-review (cross-reviews/devils-advocate.md, Dangerous Contradictions) notes the spec explicitly says "Default to `binding`" (L44) and a change requires a spec modification. Both arguments have merit on consistency grounds, but they miss the point: the guided handler serves a different user population than manual configuration. Users who hand-write `conversus.yml` understand the implications; users who go through the guided flow may not. The handler's default should serve its users, not mirror the engine's default. I maintain this position with the caveat that both the spec and engine defaults should be updated together.

#### Recommendation 3: Add grounding document quality warning
- **Original position**: After generating grounding.md, count concrete decision criteria. Warn if fewer than 3.
- **Disposition**: Modified
- **Explanation**: Functional-typing's cross-review (cross-reviews/devils-advocate.md, Dangerous Contradictions, "Grounding document validation") proposes combining content validation (emptiness check) with qualitative warning (thinness check). I accept this combined approach — it's stronger than either alone.
- **Modified recommendation**: After generating `grounding.md`: (1) Validate that Constraints and Success Criteria each contain at least one non-empty entry — if either is empty, block execution (do not generate a grounding document with no constraints). (2) If both sections have content but fewer than 3 total decision-relevant criteria, warn: "The generated grounding document contains limited decision criteria ({count} found). Arbiter rulings will be stronger with domain-specific criteria. Consider reviewing and adding criteria before proceeding." This combines functional-typing's emptiness check with the qualitative warning.

#### Recommendation 4: Add "generate config only" mode
- **Original position**: Add a "save only" option that generates config but does not execute.
- **Disposition**: Surviving
- **Explanation**: Integration-architect's cross-review (Tensions, "Save only mode and execution flow") acknowledges the implementation impact is minor (conditional skip of Steps 5-6) but asks for explicit flow branching in the spec. No cross-review argued against the feature itself. I maintain this — separating config generation from execution gives users a review point.

#### Recommendation 5: Add first-time arbitration guidance
- **Original position**: If no `arbitration/` directory exists, suggest starting with `recommended` influence.
- **Disposition**: Modified
- **Explanation**: This recommendation was partially about the default influence level (covered by Recommendation 2). The guidance aspect stands independently. The modification separates the guidance from the default question.
- **Modified recommendation**: If no `arbitration/` directory exists in the output path, add a brief note after Step 1's dispute report: "Tip: If this is your first arbitration, consider starting with 'recommended' influence. This lets you evaluate the arbiter's reasoning before committing to binding rulings. You can always re-run with 'final authority' later." This is informational guidance, not a default change.

#### Recommendation 6: Validate arbiter name does not collide with agent names
- **Original position**: Check arbiter name against agent names; append `-arbiter` on collision.
- **Disposition**: Surviving
- **Explanation**: Integration-architect's cross-review (Dangerous Contradictions, "Step 5 validation scope") adopted this as a cross-reference check in their modified Recommendation 1. Functional-typing did not challenge it. This is now a convergent position across multiple agents.

#### Recommendation 7: Strengthen the generated grounding document template
- **Original position**: Replace generic principles with domain-specific decision criteria extracted from problem.md.
- **Disposition**: Modified
- **Explanation**: The strengthened template should complement, not replace, functional-typing's content validation. The template improvement and the validation are independent mechanisms.
- **Modified recommendation**: Replace the Principles section in the generated grounding document template with: "## Decision Criteria\n- [Rephrase each constraint from problem.md as a decision criterion: 'When evaluating proposals, {constraint} takes priority because {rationale}']\n- When constraints conflict, prefer the constraint most directly tied to the success criteria above.\n\nNote: Review and refine these criteria before running arbitration. Generic criteria produce generic rulings." The explicit "Note" sets expectations about document quality.

#### Recommendation 8: Document undo path for arbiter config
- **Original position**: Add documentation about removing the arbiter block.
- **Disposition**: Surviving
- **Explanation**: Functional-typing's cross-review (Safe Agreements) confirms convergence on config backup. The undo documentation complements the backup recommendation. No cross-review challenged this.

### New Recommendations

No new recommendations. The cross-review process did not surface issues outside the scope of my original review.

### Position Summary

I withdrew 0 recommendations, modified 4 (Recommendations 1, 3, 5, and 7), and maintained 4 (Recommendations 2, 4, 6, and 8).

The most significant change was on grounding document quality (Recommendation 3). Functional-typing's content validation approach and my quality warning approach are complementary — combining them produces a stronger solution than either alone. The emptiness check catches the worst case (no content); the qualitative warning addresses the common case (thin content that technically passes validation).

My highest-priority remaining recommendation is the default influence level change (Recommendation 2). This is the position I defended most vigorously because it addresses a fundamental user-safety concern: inexperienced users who don't understand binding authority should not default into it. The consistency argument (both spec and engine default to binding) is valid but secondary to user safety for a guided flow.
