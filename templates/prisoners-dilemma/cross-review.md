# Phase 2: Capability Audit — {REVIEWER_NAME} reviews {REVIEWED_NAME}

You are **{REVIEWER_NAME}**.

{REVIEWER_PROMPT}

## Mode: Prisoner's Dilemma

You are auditing another participant's Capability Declaration. Your job is to verify their claims and flag problems. This is not adversarial — the goal is calibration, not destruction. But you must be rigorous.

The scoring system rewards honest auditing:
- **Overreach flags** that hold up reduce the reviewed agent's accuracy score. But frivolous flags that get rebutted in Phase 3 reflect poorly on your own judgment.
- **Sandbagging flags** that hold up increase the reviewed agent's potential value (they should have claimed it). Missing real sandbagging means the final Responsibility Map will have gaps.
- **Verified claims** confirm the reviewed agent's value score. Do not withhold verification to suppress a competitor — your accuracy depends on honest auditing too.

## Your Task

Read the reviewed agent's Capability Declaration and your own declaration, then write an **Audit** that verifies, challenges, or supplements their claims.

### Files to Read

**{REVIEWED_NAME}'s Capability Declaration (the document you are auditing):**
- `{REVIEWED_REVIEW_PATH}`

**Your own Capability Declaration (for context on where your capabilities overlap):**
- `{REVIEWER_REVIEW_PATH}`

**Target document (for shared context):**
- the target files:
{TARGET_FILES}

**Your documentation:**
{AGENT_DOCS}

### Output

Write your audit to: `{OUTPUT_PATH}`

### Required Sections

Your output must contain exactly these sections, in this order:

---

## Verified Claims

Claims from {REVIEWED_NAME}'s declaration that {REVIEWER_NAME} confirms as accurate.

Rules:
- List each verified claim with a brief note on why you consider it accurate (your own experience with the boundary, documentation you can corroborate, or structural reasons it must be true).
- Do not skip this section or give it token treatment. Verifying legitimate claims is as important as flagging problems.
- If a claim is in their Core Competencies or Unique Capabilities and you agree, say so explicitly. This directly supports their value score.

## Overreach

Capabilities {REVIEWED_NAME} claimed that are better handled by {REVIEWER_NAME} or another participant.

Rules:
- For each overreach flag, state: (1) what they claimed, (2) why it is overreach, and (3) who actually handles it better and why.
- Provide specific counter-evidence. "I think we do this better" is not sufficient. Cite features, architecture, documentation, or structural advantages.
- Only flag genuine overreach. Frivolous flags that get rebutted in Phase 3 weaken the audit's credibility.
- If there is no overreach, say "None identified" — do not manufacture flags.

## Sandbagging

Capabilities {REVIEWED_NAME} has but did not claim — possibly to avoid scrutiny or reduce attack surface.

Rules:
- For each sandbagging flag, state: (1) the capability they omitted, (2) evidence that they actually have it (from their docs, the target document, or your knowledge of their architecture), and (3) why it matters for the Responsibility Map.
- Sandbagging is harder to detect than overreach. Look for: capabilities mentioned in their docs but absent from their declaration; features implied by their architecture that they did not list; areas they deferred on where they actually have meaningful capability.
- If you find no sandbagging, say "None identified."

## Boundary Agreement

Areas where {REVIEWER_NAME} agrees with {REVIEWED_NAME}'s proposed responsibility boundaries.

Rules:
- Reference specific items from their Shared Territory, Deferrals, or Integration Surface sections.
- For each agreement, briefly state why the proposed boundary makes sense.
- Explicit agreement stabilizes the boundary for the final Responsibility Map.

## Boundary Dispute

Areas where {REVIEWER_NAME} disagrees with {REVIEWED_NAME}'s proposed boundaries.

Rules:
- For each dispute, state: (1) what boundary they proposed, (2) what you believe the boundary should be, and (3) counter-evidence supporting your position.
- Disputes can arise from Shared Territory assessments (they said they are stronger, you disagree), Deferrals (they deferred something they should own), or Integration Surface (the handoff point is in the wrong place).
- Be specific. Vague disputes cannot be resolved in later phases.
- If you have no disputes, say "None identified."

---

## Constraints

- Write in third person ("{REVIEWER_NAME} finds that..." not "I find that...").
- Base all flags on evidence, not opinion. Cite documentation, features, or architectural facts.
- Be balanced. A good audit has verified claims, not just flags. An audit that only attacks signals bias, not rigor.
- Length: match the scope of the declaration you are reviewing. A thorough audit is typically 300-600 words.
