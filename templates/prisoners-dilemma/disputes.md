# Phase 4: Boundary Proposals — {AGENT_NAME}

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Mode: Prisoner's Dilemma

You have declared capabilities (Phase 1), been audited (Phase 2), and recalibrated (Phase 3). Now you must propose **final responsibility boundaries** with supporting evidence. These proposals feed directly into the Responsibility Map that the synthesis will produce.

This is your last opportunity to advocate. After this phase, a neutral arbiter reads everything and decides. Make your case with evidence, not volume.

## Your Task

Read all participants' revised capability maps (Phase 3 revisions), then write your **Boundary Proposals** — a final statement of what you own, what you share, and what remains disputed.

### Files to Read

**Your revision (Phase 3):**
- `{MY_REVISION_PATH}`

**All participants' revisions (read all of these to understand the current state of every boundary):**
{ALL_REVISION_PATHS}

**Target document:**
- the target files:
{TARGET_FILES}

**Your documentation:**
{AGENT_DOCS}

### Output

Return your boundary proposals as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
### Required Sections

Your output must contain exactly these sections, in this order:

---

## Accepted Boundaries

Responsibility boundaries that {AGENT_NAME} considers settled after the recalibration phase.

For each accepted boundary:
- **Area:** [capability or responsibility area]
- **Owner:** [which participant owns it, or "shared" with named participants]
- **Basis:** [one-sentence summary of why this boundary is settled — mutual agreement, accepted flag, uncontested claim]

Rules:
- Include boundaries from your own deferrals, verified unique capabilities, and any boundary agreements confirmed in Phase 2.
- Include boundaries where you accepted overreach flags in Phase 3 — these are now settled in the other participant's favor.
- Be thorough. The more boundaries you can mark as accepted, the less the arbiter must decide.

## Disputed Boundaries

Responsibility boundaries that remain contested after recalibration.

For each disputed boundary:

### [Capability/Area Name]

- **{AGENT_NAME}'s position:** [what you claim and why — reference your Phase 3 revision]
- **Counter-position:** [what the other participant claims — reference their Phase 3 revision]
- **Evidence for {AGENT_NAME}:** [specific evidence supporting your position — docs, features, architecture, the target document's requirements]
- **Evidence against:** [honestly acknowledge the strongest point in the other participant's case]
- **Proposed resolution:** [one of the following]
  - **Assign to {AGENT_NAME}** because [reason]
  - **Assign to [other participant]** because [reason] (concession with rationale)
  - **Split responsibility**: {AGENT_NAME} handles [specific aspect], [other participant] handles [specific aspect], boundary at [precise handoff point]
  - **Needs arbiter decision** because [reason both sides have legitimate claims]

Rules:
- Every rebutted overreach flag from Phase 3 where the other participant has not conceded must appear here as a dispute. Do not silently drop contested claims.
- Every boundary dispute from Phase 2 that was not fully resolved in Phase 3 must appear here.
- Proposed resolutions must be specific enough that the arbiter can act on them. "We should discuss further" is not a resolution.
- Acknowledge the other side's strongest argument. One-sided disputes signal bias and reduce the arbiter's trust in your position.

## Proposed Responsibility Summary

A concise mapping of {AGENT_NAME}'s final proposed responsibilities:

| Responsibility Area | Proposed Owner | Status | Confidence |
|---------------------|----------------|--------|------------|
| [area] | {AGENT_NAME} | Accepted | High |
| [area] | [other participant] | Accepted (deferred) | High |
| [area] | {AGENT_NAME} + [other] | Shared — accepted | Medium |
| [area] | Disputed | Pending arbiter | Low |

Confidence levels:
- **High**: both sides agree, or claim is verified and uncontested
- **Medium**: agreed in principle but boundary details are approximate
- **Low**: actively disputed, awaiting arbiter decision

---

## Constraints

- Write in third person ("{AGENT_NAME} proposes..." not "I propose...").
- Do not introduce new capability claims. This phase is about boundaries, not new arguments.
- Every disputed boundary must include a proposed resolution. The arbiter will use your proposals as starting points.
- Be honest about the strength of counter-arguments. The arbiter reads everyone's documents — one-sided framing will be visible and will reduce trust in your position.
- Length: proportional to the number of boundaries. Typically 400-700 words.
