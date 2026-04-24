# Red-Blue Disputes — Phase 4: Final Position

You are **{AGENT_NAME}**, assigned to the **{AGENT_ROLE} team**.

{AGENT_PROMPT}

## Your Task

This is the final phase before synthesis. You have seen the full adversarial exchange: initial reviews, cross-reviews, and revised positions from all agents. Now produce your team's final position — the claims you stand behind after three rounds of challenge and response.

## What to Read

1. **Your revised position**:
   `{MY_REVISION_PATH}`

2. **All agents' revised positions** (to see how both teams adjusted):
{ALL_REVISION_PATHS}

3. **Target document** (the original proposal):
   the target files:
{TARGET_FILES}

4. **Your documentation**:
{AGENT_DOCS}

Read all revision documents to understand where the deliberation has landed. Your final position should reflect the full arc of the debate, not just your initial review.

## What to Produce

Return your final position as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
---

**If your role is RED (attacker), produce a Final Unmitigated Risks document:**

### Preamble

One paragraph summarizing the overall outcome of the adversarial process from the Red Team's perspective. How many original threats were withdrawn vs. sustained vs. escalated? What is the overall risk posture of the proposal?

### Final Risk Register

The definitive list of risks that remain unmitigated after the full deliberation. These are threats the Blue Team either conceded, failed to adequately defend, or where their proposed mitigations are insufficient.

Rank by severity (critical first), then by likelihood. For each:

- **[RISK-ID]: [Risk name]** (Severity: critical / high / medium / low | Likelihood: certain / likely / possible / unlikely)
  - **Description**: Precise statement of the risk.
  - **Deliberation history**: How this risk evolved through the phases — was it in the original attack, escalated, or newly discovered? Did Blue attempt to mitigate? Why did their mitigation fail?
  - **Evidence trail**: Key references across the deliberation documents that establish this risk.
  - **Required mitigation**: What must change in the proposal to address this risk. Be specific — name the component, the mechanism, and the expected behavior.
  - **Acceptance criteria**: How would you verify that the mitigation is sufficient?

### Attacks That Landed

A concise summary table of all risks, grouped by status:

| Risk ID | Name | Severity | Likelihood | Status |
|---------|------|----------|------------|--------|
| ... | ... | ... | ... | Unmitigated / Partially mitigated / Blue conceded |

### Closing Statement

2-3 paragraphs. The Red Team's final assessment: Is this proposal safe to proceed as-is? What is the minimum set of changes required before it should be approved? What risks should be explicitly accepted with documentation?

---

**If your role is BLUE (defender), produce a Final Defense Posture document:**

### Preamble

One paragraph summarizing the overall outcome from the Blue Team's perspective. How many attacks were neutralized vs. conceded? What is the proposal's residual risk profile?

### Successfully Defended

Attacks that the Blue Team fully neutralized during deliberation. For each:

- **[Attack reference]**: Brief description of the attack.
- **Defense**: The safeguard or evidence that neutralized it.
- **Confidence**: High / medium — how confident you are this defense holds in production.

### Conceded with Proposed Mitigations

Attacks the Blue Team acknowledges as valid, with concrete proposed fixes. For each:

- **[Attack reference]**: Brief description of the valid attack.
- **Concession**: Why this is a genuine vulnerability.
- **Proposed mitigation**: Specific, actionable change to the proposal. Include:
  - What to change (component, configuration, code, process)
  - Expected effort (trivial / moderate / significant)
  - Whether it blocks launch or can be addressed post-launch
- **Post-mitigation residual risk**: What risk remains even after the fix, if any.

### Remaining Disputes

Attacks where Red and Blue fundamentally disagree after the full deliberation. For each:

- **[Attack reference]**: The disputed threat.
- **Red's position**: Their final claim (cite their revision).
- **Blue's position**: Your rebuttal (cite your revision).
- **Core disagreement**: The specific factual or analytical point where you diverge.
- **Suggested resolution**: What evidence or testing would settle this dispute.

### Closing Statement

2-3 paragraphs. The Blue Team's final assessment: Is the proposal sound with the proposed mitigations applied? What is the residual risk the organization should accept? What monitoring or follow-up should be put in place?

---

## Rules

- **Final means final.** This is your last word. Make it count. Do not introduce entirely new attacks or defenses — this phase is for crystallizing positions established in earlier phases.
- **Acknowledge the full deliberation.** Your final position must reflect what happened in cross-review and revision, not just reiterate your opening position.
- **Be concrete about mitigations.** "This needs to be fixed" is not actionable. State what the fix is, how to verify it, and what effort it requires.
- **Rank by impact.** Spend the most space on the highest-severity items. Do not give equal weight to critical risks and minor quibbles.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate. Include the complete final position.
