# Fair Division Review — Phase 1: Valuation Statement

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you state your valuations for the items or resources being divided. Your goal is to honestly declare what you value, how much, and why — establishing the basis for an envy-free division.

## What to Read

1. **Target files** (the items/resources to be divided — read ALL of these):
{TARGET_FILES}

2. **Your documentation** (your grounding material — read all of these thoroughly):
{AGENT_DOCS}

{PRIOR_FILES_SECTION}

{PRIOR_ROUND_SECTION}

{PRIOR_ARBITRATION_SECTION}

Read every file listed above before writing your valuation statement. Your valuations must be grounded in your actual documentation. Cite exact file paths and line numbers.

## What to Produce

Return your valuation statement as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
Your valuation statement must contain the following sections in this exact order:

---

### Valuation Table

For each item or resource to be divided:

| Item | Your Valuation | Justification | Priority Rank |
|------|---------------|---------------|---------------|
| [item] | [value/score] | [Why you value it this much] | [1=highest] |

Valuations must be consistent: if you value A more than B, your score for A must be higher. Contradictory valuations will be exposed in cross-review.

### Valuation Rationale

For each high-priority item (top 3), provide detailed justification:

- **[Item label]**: Why this item is particularly valuable to you. Reference your documentation: `[doc-file, L##-##]`.
  - **Use case**: How you would use this item.
  - **Substitutability**: Can anything else substitute for this item? If so, at what loss?
  - **Synergies**: Does this item's value increase when combined with other items?

### Fairness Criteria

State which fairness properties you consider essential for the division:

- **Envy-freeness**: Do you require that no party prefers another's bundle? (standard requirement)
- **Proportionality**: Do you require that each party receives at least 1/n of their total valuation?
- **Efficiency**: Do you require Pareto optimality (no reallocation can make someone better off without making another worse off)?
- **Other criteria**: Any domain-specific fairness requirements from your documentation.

### Indivisible Items

For items that cannot be split:

- **[Item label]**: Why this item is indivisible, and how you propose handling allocation (lottery, compensation, time-sharing).

---

## Rules

- **Honest valuations.** Misrepresenting your valuations undermines envy-freeness. Cross-review will test consistency.
- **Evidence over assertion.** Every valuation must reference your documentation.
- **Consistency is testable.** If you claim item A is more valuable than item B, your actions throughout the deliberation must reflect this.
- **Declare fairness criteria early.** The division protocol depends on agreed criteria.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate.
