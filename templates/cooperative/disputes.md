# Cooperative Disputes — Phase 4: Final Disputes and Convergence

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. This is the final phase before synthesis. You have reviewed the spec, been cross-reviewed, and revised your position. Now you read all agents' revised positions and produce your final statement: what you still dispute, where you converge, and what your non-negotiables are.

This is your last chance to speak before the neutral synthesizer reads everything. Make it count.

## What to Read

1. **All agents' revised positions** (Phase 3 revisions):
{ALL_REVISION_PATHS}

2. **Your own revision** (for reference):
   `{MY_REVISION_PATH}`

3. **Target specification**:
   the target files:
{TARGET_FILES}

4. **Your documentation**:
{AGENT_DOCS}

Read all revision documents before writing. Focus on where agents' revised positions still conflict after the concessions made in Phase 3.

## What to Produce

Write your disputes document to: `{OUTPUT_PATH}`

Your disputes document must contain the following sections in this exact order:

---

### Remaining Disputes

Issues where your revised position still conflicts with at least one other agent's revised position and you are not willing to concede. 2-4 items, each structured as:

- **Dispute: [Label]**
  - **My claim**: [Your position, as stated in your revision. Cite your revision section.]
  - **Opposing position(s)**: [Which agent(s) disagree and what their revised position states. Cite their revision sections.]
  - **Why I will not concede**: [Your argument, grounded in evidence. Reference your documentation or the target spec.]
  - **Counter-argument to their position**: [Why their reasoning is flawed or incomplete. Be specific — attack the argument, not the agent.]
  - **Proposed resolution path**: [How this could be resolved — compromise wording, conditional adoption, scope limitation, or "the synthesizer must choose."]

Only list disputes that survived the revision process. If a cross-review identified a contradiction and you already conceded in Phase 3, do not re-litigate it here.

If fewer than 2 genuine disputes remain, list what exists and state "The revision process resolved the remaining conflicts."

### Convergence

Positions where you and at least one other agent now agree after the revision process. 3-5 items, each structured as:

- **Converged: [Label]**
  - **Shared position**: [What the converged recommendation is. State it in actionable terms.]
  - **Agreeing agents**: [Which agents share this position, with revision section references.]
  - **Strength**: Unanimous (all agents) | Majority (most agents) | Bilateral (two agents)
  - **Path to convergence**: [Was this agreed from Phase 1, or did it emerge through cross-review and revision? Brief narrative.]

Convergence is the most valuable signal for the synthesizer. Be thorough here.

### Final Position Statement

A structured closing statement with two subsections:

**Non-Negotiables** (1-3 items):
Recommendations from your surviving or modified set that you consider essential. For each:
- The recommendation (1 sentence).
- Why it is non-negotiable (1-2 sentences, with doc reference).

**Flexibility** (1-3 items):
Recommendations where you are willing to accept an alternative formulation if it preserves the core intent. For each:
- The recommendation (1 sentence).
- What you are flexible on and what must be preserved.

---

## Rules

- **Disputes must be real.** If the revision process resolved everything, say so. An empty disputes section is a valid and positive outcome in cooperative mode.
- **Do not re-litigate Phase 3 concessions.** If you withdrew or modified a recommendation in your revision, you cannot bring it back here. That would undermine the entire deliberation process.
- **Convergence is not capitulation.** Listing a converged position means you genuinely agree, not that you gave up. If you are listing convergence on something you still have reservations about, it belongs in Disputes instead.
- **Non-negotiables must be defensible.** Anything you declare non-negotiable will receive extra scrutiny in the synthesis. Only claim this status for positions with strong evidentiary support.
- **Be concise.** The synthesizer will read all agents' disputes. Repetition and padding dilute your strongest arguments.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate. Write the complete disputes document.
