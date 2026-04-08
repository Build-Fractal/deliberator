# Fair Division Revision — Phase 3: Revised Valuations After Challenges

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

This is revision iteration {ITERATION}.

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you revise your valuations after reading all challenges. The goal is to produce honest, consistent valuations that can support an envy-free division — adjusting where challenges exposed real inconsistencies.

## What to Read

1. **Your original valuation statement**:
   `{MY_REVIEW_PATH}`

2. **Challenges to your valuations** (other agents testing your valuations):
{CROSS_REVIEWS_OF_ME}

3. **Your challenges to others** (your tests of their valuations):
{MY_CROSS_REVIEWS}

4. **Target document**:
   the target files:
{TARGET_FILES}

5. **Your documentation**:
{AGENT_DOCS}

## What to Produce

Write your revision to: `{OUTPUT_PATH}`

---

### Valuation Dispositions

Take each item from your original valuation table and classify:

#### Item N: [Item label]

- **Original valuation**: [Score/rank and justification summary]
- **Disposition**: Adjusted | Maintained
- **Explanation**:

For **Adjusted** valuations:
  - Which challenge exposed the inconsistency? Cite the specific challenge section.
  - New valuation and why it better reflects your true preferences.

For **Maintained** valuations:
  - Which challenges you rebut and why.
  - Additional evidence supporting your original valuation.

### Revised Valuation Table

| Item | Original Valuation | Revised Valuation | Change | Reason |
|------|-------------------|-------------------|--------|--------|
| [item] | [old] | [new] | [+/-/=] | [brief explanation] |

### Trade Acceptance

Respond to trade proposals from cross-reviews:

- **[Trade label]**: Accept / Reject / Counter-propose
  - **Reasoning**: Why this trade does or does not improve your outcome.
  - **Counter-proposal** (if applicable): What you would accept instead.

### Revised Fairness Position

Update your fairness criteria if cross-reviews revealed conflicts:

- Which criteria you maintain.
- Which criteria you modify and why.
- Whether a shared fairness framework is emerging.

---

## Rules

- **Adjust where caught.** If a challenge exposed a genuine inconsistency, fix it. Maintaining inconsistent valuations undermines the entire division.
- **Consistency is mandatory.** Your revised valuation table must be internally consistent.
- **Trades create value.** Accept trades that genuinely improve your outcome. Reject trades based on misrepresented valuations.
- **Credit the source.** When you adjust a valuation, cite the challenge that prompted it.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate.
