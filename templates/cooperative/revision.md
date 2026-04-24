# Cooperative Revision — Phase 3: Revise Position After Cross-Reviews

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

This is revision iteration {ITERATION}.

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you revise your original review after reading all cross-reviews — both what others said about your review and what you said about theirs. The goal is intellectual honesty: withdraw what was wrong, modify what was partially right, and defend what survives scrutiny.

## What to Read

1. **Your original review**:
   `{MY_REVIEW_PATH}`

2. **Cross-reviews written about your review** (other agents evaluating your positions):
{CROSS_REVIEWS_OF_ME}

3. **Cross-reviews you wrote** (your evaluation of other agents — for consistency):
{MY_CROSS_REVIEWS}

4. **Target specification**:
   the target files:
{TARGET_FILES}

5. **Your documentation**:
{AGENT_DOCS}

Read all files before writing. Pay close attention to contradictions and tensions flagged in the cross-reviews of your work.

## What to Produce

Return your revision as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
Your revision must contain the following sections in this exact order:

---

### Recommendation Dispositions

Take each numbered recommendation from your original review (the Actionable Recommendations section) and classify it. Use this exact format for every recommendation:

#### Recommendation N: [Original verb-noun label]

- **Original position**: [1-sentence summary of what you recommended]
- **Disposition**: Withdrawn | Modified | Surviving
- **Explanation**:

For **Withdrawn** recommendations:
  - Which cross-review(s) challenged this, and what was the argument? Cite the specific cross-review section.
  - Why you now agree the recommendation was wrong or unnecessary. Be honest — do not frame withdrawal as strategic retreat.

For **Modified** recommendations:
  - Which cross-review(s) prompted the modification? Cite sections.
  - What the original recommendation was and what it becomes. State the new version clearly enough that the synthesis can use it directly.
  - Why the modification addresses the concern while preserving the core value.

For **Surviving** recommendations:
  - Which cross-review(s) challenged this (if any)? Cite sections.
  - Why the challenges do not change your position. Provide additional evidence or reasoning if needed.
  - If no one challenged this recommendation, state that and briefly reaffirm why it matters.

Process every recommendation. Do not skip any. If your original review had 8 recommendations, this section has 8 subsections.

### New Recommendations

Recommendations that emerged from the cross-review process — things you did not see in Phase 1 but now recognize. 0-3 items, each structured as:

- **[Verb-noun label]** (Priority: P1/P2/P3)
  - **Triggered by**: Which cross-review or tension surfaced this. Cite the specific cross-review section.
  - **Proposed change**: What you now recommend.
  - **Rationale**: Why this matters, grounded in your documentation or the cross-review evidence.

If no new recommendations emerge, write "No new recommendations. The cross-review process did not surface issues outside the scope of my original review."

### Position Summary

2-3 paragraphs summarizing your revised position. State:
1. How many recommendations you withdrew, modified, and maintained.
2. The most significant change in your thinking and what caused it.
3. Your remaining highest-priority recommendation and why it should survive into the final synthesis.

---

## Rules

- **Honesty over consistency.** If a cross-review exposed a genuine flaw in your reasoning, withdraw the recommendation. Stubbornly defending weak positions erodes your credibility in the synthesis.
- **Modifications must be concrete.** "I modified my recommendation to be more nuanced" is not a modification. State the new recommendation in actionable terms.
- **Do not withdraw everything.** If cross-reviews challenged all your positions, some of those challenges were likely wrong. Defend what deserves defending with evidence.
- **Do not add recommendations just to pad.** New recommendations should only appear if the cross-review process genuinely surfaced something you missed.
- **Acknowledge the source.** When you change your position, credit the specific cross-review that prompted it. This creates the audit trail the synthesis needs.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate. Include the complete revision.
