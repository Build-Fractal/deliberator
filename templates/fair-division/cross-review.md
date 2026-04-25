# Fair Division Cross-Review — Phase 2: Valuation Challenge

You are **{REVIEWER_NAME}**.

{REVIEWER_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you challenge **{REVIEWED_NAME}**'s valuation statement. Your goal is to test whether their valuations are consistent, honest, and well-justified — and to identify where your valuations create opportunities for mutually beneficial trades.

## What to Read

1. **{REVIEWED_NAME}'s valuation statement** (the valuations you are challenging):
   `{REVIEWED_REVIEW_PATH}`

2. **Your own valuation statement** (for reference):
   `{REVIEWER_REVIEW_PATH}`

3. **Target document** (the items being divided):
   the target files:
{TARGET_FILES}

4. **Your documentation**:
{AGENT_DOCS}

## What to Produce

Return your valuation challenge as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
---

### Valuation Consistency Test

Test {REVIEWED_NAME}'s valuations for internal consistency:

- **Transitivity**: Do their rankings form a consistent ordering? (If A > B and B > C, do they rank A > C?)
- **Proportionality**: Are their valuations proportional to their stated justifications?
- **Documentation alignment**: Do their valuations match the priorities implied by their documentation?

For each inconsistency found:
- **[Inconsistency label]**: What is inconsistent and why it matters for the division.

### Strategic Misrepresentation Check

Assess whether {REVIEWED_NAME} may be misrepresenting valuations:

- **Inflated valuations**: Items they claim to value highly but their documentation suggests otherwise.
- **Deflated valuations**: Items they claim to value little but would clearly benefit from.
- **Evidence**: Specific documentation references that contradict their stated valuations.

### Trade Opportunities

Where your valuations and theirs create opportunities for mutually beneficial allocation:

- **[Trade label]**
  - **You value [item X] more**: Your valuation vs. theirs.
  - **They value [item Y] more**: Their valuation vs. yours.
  - **Proposed trade**: Give them Y, you get X. Both parties gain relative to proportional division.

### Fairness Criteria Alignment

Compare their stated fairness criteria to yours:

- **Shared criteria**: Where you agree on fairness requirements.
- **Conflicting criteria**: Where your fairness requirements conflict and how to resolve.

---

## Rules

- **Challenge valuations, not people.** Test consistency and honesty through evidence, not accusations.
- **Cite both valuations.** Every item must reference specific sections from both valuation statements.
- **Identify trades.** The most productive outcome of cross-review is discovering mutually beneficial trades.
- **Fairness criteria matter.** If you disagree on what "fair" means, flag it now.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate.
