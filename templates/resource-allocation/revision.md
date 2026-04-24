# Resource Allocation Revision — Phase 3: Revised Demand After Challenges

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

This is revision iteration {ITERATION}.

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you revise your demand after reading all challenges. The goal is to produce a defensible, efficient demand that accounts for the pool constraints and other agents' legitimate needs.

## What to Read

1. **Your original demand statement**:
   `{MY_REVIEW_PATH}`

2. **Challenges to your demand** (other agents scrutinizing your demand):
{CROSS_REVIEWS_OF_ME}

3. **Your challenges to others** (your scrutiny of other demands):
{MY_CROSS_REVIEWS}

4. **Target document**:
   the target files:
{TARGET_FILES}

5. **Your documentation**:
{AGENT_DOCS}

## What to Produce

Return your revision as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
---

### Demand Dispositions

Take each resource demand from your original statement and classify it:

#### Resource N: [Original resource label]

- **Original demand**: [Quantity and justification summary]
- **Disposition**: Reduced | Modified | Maintained
- **Explanation**:

For **Reduced** demands:
  - Which challenge exposed the inflation? Cite the specific challenge section.
  - New quantity and why it is sufficient.

For **Modified** demands:
  - How the demand structure changed (e.g., time-sharing, conditional allocation).
  - Why the modification addresses the challenge while preserving your core need.

For **Maintained** demands:
  - Which challenges you rebut and why.
  - Additional evidence supporting your original demand.

### New Demands

Demands that emerged from the challenge process. 0-2 items:

- **[Resource label]**
  - **Triggered by**: Which challenge or cooperation opportunity surfaced this.
  - **Demand**: Specific quantity and justification.

### Revised Allocation Proposal

Your updated view of what a fair overall allocation looks like:

- For each resource type, state your revised demand and what you believe others should receive.
- Justify the overall split using efficiency, impact, or fairness criteria.

---

## Rules

- **Reduce where challenged legitimately.** Stubbornly maintaining inflated demands erodes your credibility.
- **Modifications must be concrete.** State exact revised quantities.
- **Do not reduce to zero.** If you have a legitimate need, defend it even if challenged.
- **Credit the source.** When you adjust a demand, cite the specific challenge that prompted it.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate.
