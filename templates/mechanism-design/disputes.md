# Mechanism Design Disputes — Phase 4: Final Property Claims and Trade-offs

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. This is the final phase before the mechanism spec is synthesized. Declare which mechanism properties you consider essential, where you agree with other roles, and which trade-offs remain unresolved.

## What to Read

1. **All roles' revised analyses** (Phase 3 revisions):
{ALL_REVISION_PATHS}

2. **Your own revision** (for reference):
   `{MY_REVISION_PATH}`

3. **Target document**:
   the target files:
{TARGET_FILES}

4. **Your documentation**:
{AGENT_DOCS}

## What to Produce

Write your final position to: `{OUTPUT_PATH}`

---

### Mechanism Vulnerabilities

Mechanism properties or recommendations where your role's analysis still conflicts with another role's and you believe the mechanism is at risk. 2-4 items:

- **Vulnerability: [Label]**
  - **My finding**: [Your property concern, citing your revision.]
  - **Opposing position**: [Which role disagrees and why, citing their revision.]
  - **Why this matters**: [What happens to the mechanism if this is not addressed.]
  - **Proposed resolution**: [How to balance both roles' concerns, or "the synthesizer must choose based on the deployment context."]

### Convergence

Properties where all roles agree after cross-review. 3-5 items:

- **Converged: [Property/Recommendation label]**
  - **Shared finding**: [What all roles agree on, stated as a mechanism requirement.]
  - **Agreeing roles**: [Names with revision references.]
  - **Strength**: Unanimous | Majority | Bilateral
  - **Path to convergence**: [Agreed from Phase 1 or emerged through cross-review?]

### Final Position Statement

**Non-Negotiable Properties** (1-3 items):
Properties the mechanism MUST satisfy from your role's perspective:
- [Property] (1 sentence).
- Why non-negotiable (1-2 sentences, with documentation reference).

**Acceptable Trade-offs** (1-3 items):
Properties where you accept a weaker guarantee if another property is strengthened:
- [Property] — what minimum guarantee you need and what you would trade for.

---

## Rules

- **Vulnerabilities must be real.** If cross-review resolved all conflicts, say so.
- **Do not re-litigate Phase 3 withdrawals.** If you withdrew a recommendation, it stays withdrawn.
- **Impossibility trade-offs are valid outcomes.** Some property conflicts cannot be resolved — they can only be managed with explicit trade-off documentation.
- **Be concise.** The synthesizer reads all roles' final positions.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate.
