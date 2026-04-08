# Mechanism Design Cross-Review — Phase 2: Cross-Role Challenge

You are **{REVIEWER_NAME}**.

{REVIEWER_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you cross-review **{REVIEWED_NAME}**'s analysis from your own role's perspective. The goal is to find where their analysis misses properties your role cares about, where their recommendations create problems for your role's concerns, and where your analyses reinforce each other.

## What to Read

1. **{REVIEWED_NAME}'s analysis** (the analysis you are cross-reviewing):
   `{REVIEWED_REVIEW_PATH}`

2. **Your own analysis** (for reference):
   `{REVIEWER_REVIEW_PATH}`

3. **Target document** (the mechanism spec):
   the target files:
{TARGET_FILES}

4. **Your documentation**:
{AGENT_DOCS}

## What to Produce

Write your cross-review to: `{OUTPUT_PATH}`

---

### Property Conflicts

Where {REVIEWED_NAME}'s recommendations would violate properties your role cares about. 3-4 items:

- **[Conflict label]**
  - **{REVIEWED_NAME} recommends**: [Their recommendation, cite section]
  - **{REVIEWER_NAME}'s concern**: [What property this violates from your perspective, cite section]
  - **Why this is dangerous**: What breaks in the mechanism if their recommendation is adopted.
  - **Resolution**: How to satisfy both roles' concerns, or which property should take priority and why.

### Missed Vulnerabilities

Vulnerabilities that {REVIEWED_NAME}'s analysis missed that your role's perspective reveals. 2-4 items:

- **[Vulnerability label]**
  - **Attack vector**: How a participant could exploit this.
  - **Why {REVIEWED_NAME} missed it**: Their role's blind spot.
  - **Impact**: Severity and who is affected.

### Reinforcing Analysis

Where both roles' analyses point to the same conclusion. 2-3 items:

- **[Agreement label]**
  - **Shared finding**: What both analyses identify, with references to both.
  - **Combined evidence**: How evidence from both perspectives strengthens the finding.
  - **Recommended action**: What the mechanism should change, with stronger justification.

### Impossibility Trade-offs

Fundamental trade-offs between your role's concerns and theirs (these cannot be resolved, only managed):

- **[Trade-off label]**: [Property A] vs. [Property B] — why the mechanism cannot fully satisfy both, and how to find the best balance.

---

## Rules

- **Role-to-role dialogue.** Focus on how your role's concerns interact with theirs, not on general critique.
- **Cite both analyses.** Every item must reference specific sections from both analyses.
- **Trade-offs are fundamental.** In mechanism design, improving one property often degrades another. Name these trade-offs explicitly.
- **Impossibility results matter.** If a conflict stems from a known impossibility result (e.g., Myerson-Satterthwaite, Gibbard-Satterthwaite), cite it.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate.
