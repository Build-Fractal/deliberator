# Fair Division Disputes — Phase 4: Final Valuations and Division Claims

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. This is the final phase before the divider produces the allocation. Declare your final valuations, where you agree on allocation, and what valuations or allocations you dispute.

## What to Read

1. **All agents' revised valuations** (Phase 3 revisions):
{ALL_REVISION_PATHS}

2. **Your own revision** (for reference):
   `{MY_REVISION_PATH}`

3. **Target document**:
   the target files:
{TARGET_FILES}

4. **Your documentation**:
{AGENT_DOCS}

## What to Produce

Return your final valuation claim as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
---

### Disputed Valuations

Items where your valuation still conflicts with another agent's in ways that affect the division outcome. 2-4 items:

- **Disputed: [Item label]**
  - **My valuation**: [Your value/rank, citing your revision.]
  - **Their valuation**: [Which agent disagrees and their value, citing their revision.]
  - **Why it matters**: [How this disagreement affects the division outcome.]
  - **Proposed resolution**: [How to resolve — accept their valuation, use average, use external benchmark, or "the divider must decide."]

### Agreed Allocations

Items where all agents agree on who should receive them. 3-5 items:

- **Agreed: [Item label]**
  - **Allocation**: [Who receives this item.]
  - **Agreeing agents**: [Names with revision references.]
  - **Basis**: [Which trade or convergence produced this agreement.]

### Accepted Trades

Trades from cross-reviews that all involved parties accepted:

- **Trade: [Label]**
  - **[Agent A] receives**: [items]
  - **[Agent B] receives**: [items]
  - **Both accept because**: [Why this trade is mutually beneficial.]

### Final Fairness Statement

**Essential Properties** (properties the division MUST satisfy):
- [Envy-freeness / proportionality / other] — why this is essential.

**Desirable Properties** (properties you prefer but can compromise on):
- [Property] — what you would accept instead.

**Items you must receive** (1-3):
- [Item] — why receiving this item is essential to your participation.

---

## Rules

- **Disputed valuations must be real.** If all valuations converged, say so.
- **Do not reverse Phase 3 adjustments.** If you adjusted a valuation in revision, it stays adjusted.
- **Accepted trades are binding.** If you accept a trade here, you cannot reject it later.
- **Fairness claims must be grounded.** State which fairness property and why it matters for your domain.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate.
