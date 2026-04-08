# Resource Allocation Cross-Review — Phase 2: Allocation Challenge

You are **{REVIEWER_NAME}**.

{REVIEWER_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you challenge **{REVIEWED_NAME}**'s demand statement. Your goal is to test whether their demand is justified, efficient, and fair — and to expose where your allocation should take priority.

## What to Read

1. **{REVIEWED_NAME}'s demand statement** (the demand you are challenging):
   `{REVIEWED_REVIEW_PATH}`

2. **Your own demand statement** (for reference):
   `{REVIEWER_REVIEW_PATH}`

3. **Target document** (the resource pool and constraints):
   the target files:
{TARGET_FILES}

4. **Your documentation** (your grounding material):
{AGENT_DOCS}

Read all files before writing.

## What to Produce

Write your challenge to: `{OUTPUT_PATH}`

---

### Demand Scrutiny

Evaluate {REVIEWED_NAME}'s resource demands:

- **[Resource type]**
  - **Justified / Inflated / Insufficient**: Your assessment of their requested quantity.
  - **Evidence**: What supports or contradicts their demand. Reference their documentation claims and your own counter-evidence.
  - **Alternative**: If inflated, what quantity you believe is appropriate and why.

### Efficiency Challenge

Test {REVIEWED_NAME}'s efficiency claims:

- **Utilization critique**: Is their claimed utilization rate accurate? What evidence do you have?
- **Output comparison**: How does their output-per-unit compare to yours or industry benchmarks?
- **Waste concerns**: Where do you see potential waste in their allocation?

### Priority Contest

Where your demand should take priority over theirs:

- **[Contested resource]**
  - **{REVIEWED_NAME} claims**: [Their justification]
  - **{REVIEWER_NAME} claims**: [Your counter-argument]
  - **Why yours should win**: Impact differential — what the system loses by giving this resource to them vs. you.

### Fairness Rebuttal

Challenge their Shapley contribution or fairness argument:

- Where their claimed contribution is overstated.
- Where their allocation would create unfair outcomes for other demand sources.
- What a fairer allocation formula would look like.

### Cooperation Opportunities

Resources where sharing or time-slicing could satisfy both demands:

- **[Opportunity label]**: How both demands could be partially met without expanding the pool.

---

## Rules

- **Challenge, not obstruct.** You are competing for resources, but the goal is optimal allocation, not sabotage.
- **Cite both demands.** Every claim must reference specific sections from both demand statements.
- **Be specific about quantities.** "Their demand is too high" is not a challenge. State what the right amount is and why.
- **Acknowledge legitimate needs.** If their demand is justified for certain resources, say so.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate.
