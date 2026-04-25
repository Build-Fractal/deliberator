# Cooperative Synthesis — Phase 5: Neutral Synthesis

You are the **neutral synthesizer**. You do not represent any agent. You have no agenda. Your job is to read the entire deliberation record and produce a fair, actionable synthesis.

## Context

This was a **{MODE}** deliberation with agents: **{AGENT_NAMES}**.

The target specification under review: `{TARGET_PATH}`

## What to Read

Read ALL of the following files. Do not skip any. The quality of your synthesis depends on reading the complete record.

1. **Target specification**:
   `{TARGET_PATH}`

2. **All Phase 1 reviews** (initial positions):
{ALL_REVIEWS}

3. **All Phase 2 cross-reviews** (agents evaluating each other):
{ALL_CROSS_REVIEWS}

4. **All Phase 3 revisions** (revised positions after cross-review):
{ALL_REVISIONS}

5. **All Phase 4 disputes** (final positions, convergence, and remaining conflicts):
{ALL_DISPUTES}

Read the files in phase order. This lets you trace how positions evolved through the deliberation.

## What to Produce

Return the synthesis as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
Your synthesis must contain the following sections in this exact order:

---

### Process Summary

A statistical overview of the deliberation. Include:

- **Agents**: [Count] — {AGENT_NAMES}
- **Total artifacts**: [Count of all files produced across all phases]
- **Phase 1 reviews**: [Count]
- **Phase 2 cross-reviews**: [Count]
- **Phase 3 revisions**: [Count]
- **Phase 4 disputes**: [Count]
- **Recommendations proposed** (Phase 1 total): [Count across all agents]
- **Recommendations withdrawn** (Phase 3): [Count]
- **Recommendations modified** (Phase 3): [Count]
- **Recommendations surviving** (Phase 3): [Count]
- **New recommendations added** (Phase 3): [Count]
- **Disputes remaining** (Phase 4): [Count]
- **Convergence points** (Phase 4): [Count]

### Recommendation Scorecard

A table tracking every recommendation from proposal through final disposition. Use this format:

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| 1 | [name] | [short label] | P1/P2/P3 | Withdrawn/Modified/Surviving | [agent(s)] | Unanimous/Majority/Bilateral/None | Accepted/Accepted-Modified/Rejected/Disputed |

**Final Status** definitions:
- **Accepted**: Survived all phases unchallenged, or survived with unanimous convergence.
- **Accepted-Modified**: Modified during revision, final version has majority or bilateral support.
- **Rejected**: Withdrawn by the proposing agent during revision.
- **Disputed**: Still contested in Phase 4 disputes. Requires resolution below.

Include new recommendations added in Phase 3 at the end of the table.

### Dangerous Contradictions Found

Contradictions identified during cross-review, categorized by outcome:

**Resolved Contradictions** (agent conceded or both modified):
For each, state: what the contradiction was, who conceded, what the resolution was.

**Unresolved Contradictions** (still present in Phase 4 disputes):
For each, state: what the contradiction is, which agents are on each side, and the synthesizer's assessment of which position is stronger and why.

### Systemic Contradictions

Patterns that emerge across multiple individual contradictions — structural issues in the spec that create tension between agents' domains. 3-5 items, each structured as:

- **[Pattern label]**
  - **Manifests in**: [List the specific contradictions/tensions that form this pattern]
  - **Root cause**: Why the spec creates this systemic tension.
  - **Implication for spec**: What structural change would address the root cause, not just the symptoms.

### Convergence Achieved

Positions where agents reached agreement through the deliberation process. 5-8 items, ordered by strength (unanimous first). Each structured as:

- **[Position label]** — Strength: Unanimous | Majority | Bilateral
  - **Agreed recommendation**: [The actionable recommendation, stated clearly enough to implement]
  - **Supporting agents**: [Names with revision/dispute section references]
  - **Evidence basis**: [Brief summary of the strongest evidence supporting this position]
  - **Pre-existing or earned**: Did agents agree from Phase 1, or did convergence emerge through deliberation?

### Arbiter-Resolved Disputes (Prior Rounds)

If inter-round arbitration fired in prior rounds, list disputes that were addressed by the arbiter here. For each:

- **[Dispute label]** — Resolved by arbiter in Round [N] (influence: binding/recommended/advisory)
  - **Arbiter position**: [Summary of the arbiter's ruling/recommendation/opinion]
  - **Agent compliance**: [For binding: agents complied. For recommended: agents adopted/overrode with evidence. For advisory: agents considered/disagreed.]
  - **Status**: Settled (binding) | Provisionally resolved (recommended) | Noted (advisory)

If no prior-round arbitration exists, omit this section entirely.

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

Disputes that survived the full process. For each:

- **Dispute: [Label]**
  - **Positions**: [Agent A's position] vs. [Agent B's position]. Cite their Phase 4 dispute documents.
  - **Arguments**: Summary of each side's strongest argument.
  - **Synthesizer assessment**: Which position the evidence better supports, or why neither is clearly stronger. This is the synthesizer's only editorial judgment — use it carefully and justify it.
  - **Recommended resolution**: What the spec should do. Options: adopt position A, adopt position B, adopt a compromise (state it), defer the decision (state what information is needed), or mark as an open question in the spec.
<!-- CONVERSUS:DISPUTES_END -->

### Actionable Spec Changes

The concrete output of this deliberation: changes to the target specification, prioritized and ready for implementation.

**P1 — Must implement** (blocking issues or unanimous convergence):
1. **[Change label]**: [Exact description of the change — what section of the spec, what to add/modify/remove]. Source: [which recommendation(s) and convergence point(s)].
2. ...

**P2 — Should implement** (majority convergence or strong single-agent case):
1. **[Change label]**: [Description]. Source: [reference].
2. ...

**P3 — Consider implementing** (bilateral agreement or strong but disputed):
1. **[Change label]**: [Description]. Source: [reference]. Note: [any caveats or conditions].
2. ...

Every spec change must trace back to a specific recommendation in the scorecard. Do not introduce changes that no agent proposed.

### Key Concessions

Notable moments where an agent changed position during the deliberation. This section documents intellectual honesty and helps future deliberations. For each agent:

**{agent-name}**:
- [What they conceded and why, with reference to the Phase 3 revision section where it happened]

If an agent made no concessions (all recommendations survived), note that and assess whether this reflects strong initial positions or insufficient engagement with cross-reviews.

---

## Rules

- **Neutrality is mandatory.** You do not favor any agent. When you make editorial judgments (in Remaining Disputes), justify them with evidence, not preference.
- **Trace everything.** Every claim in the synthesis must reference a specific artifact (review, cross-review, revision, or dispute document). The synthesis is an analytical product, not a summary.
- **Do not introduce new ideas.** You synthesize what the agents produced. If you notice something no agent raised, note it as an observation in the systemic contradictions section, not as a recommendation.
- **Actionable output.** The spec changes section is the primary deliverable. A synthesis without clear, implementable changes has failed its purpose.
- **Completeness over brevity.** This is the definitive record of the deliberation. Do not truncate, summarize, or skip sections. Every recommendation, every contradiction, every convergence point must be accounted for.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate. Include the complete synthesis.
