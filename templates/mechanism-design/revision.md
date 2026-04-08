# Mechanism Design Revision — Phase 3: Revised Analysis After Cross-Review

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

This is revision iteration {ITERATION}.

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you revise your analysis after reading cross-reviews from other roles. The goal is to integrate insights from other perspectives while maintaining your role's core concerns.

## What to Read

1. **Your original analysis**:
   `{MY_REVIEW_PATH}`

2. **Cross-reviews of your analysis** (other roles challenging your findings):
{CROSS_REVIEWS_OF_ME}

3. **Your cross-reviews of others** (your challenges to other roles):
{MY_CROSS_REVIEWS}

4. **Target document**:
   the target files:
{TARGET_FILES}

5. **Your documentation**:
{AGENT_DOCS}

## What to Produce

Write your revision to: `{OUTPUT_PATH}`

---

### Recommendation Dispositions

Take each recommendation from your original analysis and classify it:

#### Recommendation N: [Original label]

- **Original recommendation**: [1-sentence summary]
- **Disposition**: Withdrawn | Modified | Surviving
- **Explanation**:

For **Withdrawn**:
  - Which cross-review showed this recommendation violates a critical property? Cite the section.
  - Why you agree the trade-off is not worth it.

For **Modified**:
  - Which cross-review prompted the modification? Cite sections.
  - How the modification preserves your role's concern while respecting the other role's property.
  - The new recommendation, stated precisely.

For **Surviving**:
  - Which cross-reviews challenged this? Cite sections.
  - Why the trade-off is still worth it despite the other role's concern.

### New Recommendations

Recommendations from cross-review insights. 0-3 items:

- **[Label]** (Priority: P1/P2/P3)
  - **Triggered by**: Which cross-review finding.
  - **Recommendation**: The specific mechanism change.
  - **Trade-off acknowledged**: What this costs in other properties.

### Updated Property Assessment

Revise your incentive/vulnerability/efficiency assessment based on cross-review findings:

- Which properties did you initially assess incorrectly?
- Which new vulnerabilities did other roles reveal?
- How does the overall mechanism assessment change?

### Position Summary

2-3 paragraphs:
1. Recommendations withdrawn, modified, and maintained.
2. The most significant insight from cross-review.
3. Your remaining highest-priority recommendation.

---

## Rules

- **Integrate, do not ignore.** If another role identified a genuine property violation, address it.
- **Trade-offs are not defeats.** Modifying a recommendation to respect another property is good mechanism design, not weakness.
- **Maintain role discipline.** Even after revision, your analysis should reflect your role's primary concern.
- **Credit sources.** Cite the cross-review that prompted each change.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate.
