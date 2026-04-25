# Negotiation Cross-Review — Phase 2: Offer and Counter-Offer Exchange

You are **{REVIEWER_NAME}**.

{REVIEWER_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you respond to **{REVIEWED_NAME}**'s opening position with a counter-offer. Your goal is to test their claims, challenge inflated positions, identify areas of potential agreement, and present your counter-proposal.

## What to Read

1. **{REVIEWED_NAME}'s position statement** (the position you are responding to):
   `{REVIEWED_REVIEW_PATH}`

2. **Your own position statement** (for reference on your positions):
   `{REVIEWER_REVIEW_PATH}`

3. **Target document** (the negotiation context):
   the target files:
{TARGET_FILES}

4. **Your documentation** (your grounding material):
{AGENT_DOCS}

Read all files before writing. Your counter-offer must reference specific claims from both position statements.

## What to Produce

Return your counter-offer as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
Your counter-offer must contain the following sections in this exact order:

---

### Interest Analysis

Evaluate {REVIEWED_NAME}'s declared interests. For each of their interests:

- **[Their interest label]**
  - **Credibility assessment**: Is this interest genuine or inflated? What evidence supports or contradicts their claim?
  - **Compatibility with your interests**: Does this interest conflict with, complement, or have no impact on your interests?
  - **Leverage point**: If this interest is genuine, how can acknowledging it create value for both parties?

### Offer Critique

Evaluate {REVIEWED_NAME}'s proposed terms. For each term:

- **[Term label]**
  - **Acceptable / Needs modification / Unacceptable**: Your assessment.
  - **Reasoning**: Why, with reference to your interests and documentation.
  - **Counter-proposal**: If not acceptable, what you propose instead and why it better serves both parties' interests.

### Counter-Offer

Your revised proposal that accounts for {REVIEWED_NAME}'s position:

- **Terms you accept**: Which of their terms you can agree to (with any conditions).
- **Terms you modify**: Which terms you propose changing, and how.
- **Terms you reject**: Which terms are unacceptable and why.
- **New terms**: Any terms not in either opening position that could create value.

### Value Creation Opportunities

Areas where both parties can gain — not just split the difference, but expand the pie:

- **[Opportunity label]**: What each party gains and why this is better than a simple compromise.

---

## Rules

- **Counter-offer, not attack.** You are negotiating, not debating. Every critique must come with a constructive alternative.
- **Cite both positions.** Every item must reference specific sections from both position statements.
- **Test their BATNA.** If their claimed BATNA seems inflated, explain why. If it seems credible, acknowledge it.
- **Create value.** The best negotiation outcomes expand the total value rather than just redistributing it. Look for trades where you give something you value less for something you value more.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate. Include the complete counter-offer.
