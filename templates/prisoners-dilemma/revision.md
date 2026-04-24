# Phase 3: Recalibration — {AGENT_NAME}

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

This is revision iteration {ITERATION}.

## Mode: Prisoner's Dilemma

You have submitted your Capability Declaration (Phase 1) and received audits from other participants (Phase 2). Now you must **recalibrate** — adjust your claims based on the evidence presented in those audits.

The scoring rules make this phase critical:
- **Accepting a valid overreach flag** and withdrawing the claim preserves your accuracy. Defending an indefensible claim costs more.
- **Accepting a valid sandbagging flag** and adding the capability increases your value score. Continuing to hide it leaves value on the table.
- **Rebutting an invalid flag** with counter-evidence is legitimate and expected. But the rebuttal must present new evidence or reasoning, not just reassert the original claim.

The goal is convergence toward an accurate capability map. Stubbornness without evidence is penalized. Capitulation without reason is also penalized (it suggests the original declaration was careless).

## Your Task

Read all audits written about you, your own audits of others, and your original declaration. Then write a **Recalibration** that addresses every flag and updates your capability boundaries.

### Files to Read

**Your original Capability Declaration:**
- `{MY_REVIEW_PATH}`

**Audits written about you (other participants reviewing your declaration):**
{CROSS_REVIEWS_OF_ME}

**Your audits of others (for context on positions you have already taken):**
{MY_CROSS_REVIEWS}

**Target document:**
- the target files:
{TARGET_FILES}

**Your documentation:**
{AGENT_DOCS}

### Output

Return your recalibration as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
### Required Sections

Your output must contain exactly these sections, in this order:

---

## Overreach Responses

Address **every** overreach flag raised against {AGENT_NAME} in the cross-reviews. No flag may be ignored.

For each flag, write one of:

### Accepted: [capability name]
- **Flagged by:** [reviewer name]
- **Original claim:** [what you claimed]
- **Acceptance reason:** [why the flag is valid — what evidence convinced you]
- **Updated position:** [where this capability now sits — deferred, shared territory, or withdrawn]

### Rebutted: [capability name]
- **Flagged by:** [reviewer name]
- **Original claim:** [what you claimed]
- **Rebuttal evidence:** [new evidence or reasoning not present in the original declaration — must be specific and verifiable]
- **Maintained position:** [your claim stands, with this additional grounding]

Rules:
- You must respond to every overreach flag. Silence on a flag is treated as implicit acceptance.
- Rebuttals must introduce evidence, not reassert the claim. "We still believe X" is not a rebuttal.
- Partial acceptance is allowed: "We accept that Y handles the common case better, but maintain our claim for the Z-specific scenario because..."

## Sandbagging Responses

Address **every** sandbagging flag raised against {AGENT_NAME} in the cross-reviews. No flag may be ignored.

For each flag, write one of:

### Accepted: [capability name]
- **Flagged by:** [reviewer name]
- **Omitted capability:** [what you failed to claim]
- **Acceptance reason:** [why the flag is valid — the capability is real and should have been declared]
- **Updated position:** [where this capability now sits — core competency, unique capability, or shared territory]

### Rebutted: [capability name]
- **Flagged by:** [reviewer name]
- **Alleged capability:** [what they say you have]
- **Rebuttal evidence:** [why this is not actually a capability you have, or why it is too minor/experimental to declare]

Rules:
- You must respond to every sandbagging flag.
- Accepting a sandbagging flag is not a weakness — it shows your declaration is becoming more accurate and complete.

## Updated Capability Boundaries

Restate your capability map with all adjustments applied. This replaces your Phase 1 declaration.

Subsections:
- **Core Competencies** (updated)
- **Unique Capabilities** (updated)
- **Shared Territory** (updated — include any changes to relative-strength assessments)
- **Deferrals** (updated — include any new deferrals from accepted overreach)
- **Integration Surface** (updated if boundary changes affect handoff points)

Rules:
- Changes from Phase 1 must be clearly marked. Use "(unchanged)", "(added — accepted sandbagging flag from [reviewer])", "(withdrawn — accepted overreach flag from [reviewer])", or "(modified — [brief reason])".
- The updated map must be internally consistent. If you accepted an overreach flag in Core Competencies, it should not reappear unchanged in the updated Core Competencies.

## Adjustment Summary

A concise table showing what changed and why:

| Claim | Original Position | Adjustment | Reason |
|-------|-------------------|------------|--------|
| ... | Core Competency | Withdrawn | Accepted overreach flag from [reviewer] |
| ... | Not declared | Added as Shared Territory | Accepted sandbagging flag from [reviewer] |
| ... | Shared Territory (stronger) | Shared Territory (equal) | Partial acceptance of [reviewer]'s dispute |

---

## Constraints

- Write in third person ("{AGENT_NAME} accepts..." not "I accept...").
- Every overreach and sandbagging flag must get a response. Count them. If you received 4 flags total, your document must contain 4 responses.
- Do not introduce entirely new claims that were not in your Phase 1 declaration or flagged as sandbagging. Recalibration adjusts existing claims; it does not expand scope.
- Length: proportional to the number of flags received. Typically 400-800 words.
