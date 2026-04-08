# Negotiation Review — Phase 1: Opening Position Statement

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you state your party's opening position. Your goal is to clearly articulate your interests, priorities, and constraints — not to compromise yet, but to establish what you value and why.

## What to Read

1. **Target files** (the documents defining the negotiation context — read ALL of these):
{TARGET_FILES}

2. **Your documentation** (your grounding material — read all of these thoroughly):
{AGENT_DOCS}

{PRIOR_FILES_SECTION}

{PRIOR_ROUND_SECTION}

{PRIOR_ARBITRATION_SECTION}

Read every file listed above before writing your position statement. Your claims must be grounded in your actual documentation, not general knowledge. Cite exact file paths and line numbers when referencing your docs.

## What to Produce

Write your position statement to: `{OUTPUT_PATH}`

Your position statement must contain the following sections in this exact order:

---

### Interests Declaration

State your party's core interests — not positions, but the underlying needs and motivations. 4-6 items, each structured as:

- **[Interest label]**: What you need and why, with documentation reference `[doc-file, L##-##]`. Classify as: essential (cannot accept any deal without this) | important (strongly preferred) | desirable (nice-to-have).

Be honest about priorities. Misrepresenting essential interests as desirable (or vice versa) will undermine your credibility in cross-review.

### Opening Offer

Your initial proposal for how the negotiation should resolve. Structure as:

- **Proposed terms**: 5-8 specific, concrete terms you propose. Each must be measurable or verifiable.
- **Rationale**: For each term, explain why this is reasonable given both parties' likely interests. Reference the target document and your documentation.

### Zone of Possible Agreement (ZOPA) Assessment

Your honest assessment of where a deal is possible:

- **Your BATNA** (Best Alternative to Negotiated Agreement): What happens if no deal is reached. Be specific — vague BATNAs are weak BATNAs.
- **Your reservation point**: The minimum terms you would accept (be strategic but honest — cross-review will test this).
- **Estimated overlap**: Where you believe the other party's interests and yours might align.

### Risk Factors

2-4 risks that could derail the negotiation or make any agreement unstable:

- **[Risk label]**: What could go wrong, how likely it is, and what safeguards you propose.

---

## Rules

- **Interests over positions.** State what you need and why, not just what you demand. Positional bargaining without interest disclosure leads to impasse.
- **Evidence over assertion.** Every claim must reference either the target document or your documentation. Ungrounded claims will be dismantled in cross-review.
- **Strategic honesty.** You may emphasize certain interests over others, but do not fabricate interests or misrepresent your BATNA. The cross-review phase will expose inconsistencies.
- **No premature concessions.** This is your opening position. Do not compromise in Phase 1 — that happens in revision.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate. Write the complete position statement.
