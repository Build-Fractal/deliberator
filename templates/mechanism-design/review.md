# Mechanism Design Review — Phase 1: Role-Based Analysis

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. In this phase, you analyze the proposed mechanism from your specialized role's perspective. The goal is to evaluate the mechanism's incentive properties, efficiency, and vulnerability to gaming.

Mechanism design mode is unique: you are not advocating for a party's interests, you are analyzing the rules themselves. Your roles are: incentive analyst (truthfulness), efficiency advocate (social welfare), and gaming adversary (exploitation red-team).

## What to Read

1. **Target files** (the mechanism specification under review — read ALL of these):
{TARGET_FILES}

2. **Your documentation** (your grounding material — read all of these thoroughly):
{AGENT_DOCS}

{PRIOR_FILES_SECTION}

{PRIOR_ROUND_SECTION}

{PRIOR_ARBITRATION_SECTION}

Read every file listed above before writing your analysis. Ground every claim in your documentation. Cite exact file paths and line numbers.

## What to Produce

Write your analysis to: `{OUTPUT_PATH}`

Your analysis must contain the following sections in this exact order:

---

### Mechanism Overview

Summarize the mechanism under review in 2-3 paragraphs:
- What the mechanism does (input, process, output).
- Who the participants are and what they can control.
- What the mechanism is trying to achieve (social welfare objective).

### Incentive Analysis

Evaluate the mechanism's incentive properties from your role's perspective. 5-8 items:

- **[Property label]** (e.g., Truthfulness, Individual Rationality, Budget Balance)
  - **Status**: Satisfied / Violated / Conditionally satisfied
  - **Evidence**: Why, with reference to the mechanism spec and your documentation `[doc-file, L##-##]`.
  - **Impact**: What happens if this property is violated. Severity: critical / significant / minor.

### Vulnerability Assessment

Identify ways participants could game or exploit the mechanism. 3-6 items:

- **[Vulnerability label]**
  - **Attack vector**: How a rational participant would exploit this.
  - **Prerequisites**: What the attacker needs to know or control.
  - **Impact**: What they gain and what the system loses.
  - **Mitigation**: How to fix or reduce this vulnerability.

### Efficiency Evaluation

Assess the mechanism's efficiency properties:

- **Social welfare**: Does the mechanism maximize total value? Evidence and analysis.
- **Allocative efficiency**: Are resources allocated to those who value them most?
- **Computational complexity**: Is the mechanism tractable for the expected participant count?
- **Communication complexity**: How much information must participants reveal?

### Recommendations

5-8 concrete changes to improve the mechanism:

1. **[Verb-noun label]** (Priority: P1/P2/P3)
   - **Current state**: What the mechanism spec says now (cite line).
   - **Proposed change**: Exact change to the mechanism rules.
   - **Rationale**: Why, grounded in your documentation `[doc-ref]`.
   - **Trade-off**: What this change costs (every mechanism improvement has a trade-off).

---

## Rules

- **Role discipline.** Stay in your assigned role. Incentive analysts focus on truthfulness, efficiency advocates on welfare, gaming adversaries on exploitation.
- **Evidence over intuition.** Every claim must reference the mechanism spec or your documentation.
- **Trade-offs are mandatory.** Every recommendation must acknowledge what it costs. There is no free lunch in mechanism design.
- **Formal properties matter.** Use the language of mechanism design: incentive compatibility, individual rationality, budget balance, strategyproofness.
- **Write the file.** Your entire output must be written to `{OUTPUT_PATH}`. Do not summarize or truncate.
