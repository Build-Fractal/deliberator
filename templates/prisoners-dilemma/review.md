# Phase 1: Capability Declaration — {AGENT_NAME}

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Mode: Prisoner's Dilemma

You are participating in a **Prisoner's Dilemma** deliberation. The scoring rules are:

- **Accuracy**: starts at 100%. You lose points for every capability you claim that cross-reviewers flag as overreach — and that survives rebuttal. Overreach means claiming you handle something better than another participant when the evidence says otherwise.
- **Value**: starts at 0. You gain points for every unique, confirmed capability you declare. If you sandbag (hide real capabilities to avoid scrutiny), reviewers will flag it and you lose potential value points.
- **Trust = Accuracy x Value**. The winning strategy is honest, well-evidenced advocacy. Overclaiming destroys accuracy. Underclaiming destroys value.

The Nash equilibrium is **not** to be the loudest or the most modest. It is to be the most precisely calibrated to your actual capabilities.

## Your Task

Read the target document and your documentation, then write a **Capability Declaration** — an honest, evidence-backed assessment of what you do, what you do best, where you overlap with others, and where you explicitly defer.

### Files to Read

**Target document:**
- the following target files:
{TARGET_FILES}

**Your documentation (read all of these for grounding — your claims must be traceable to evidence here):**
{AGENT_DOCS}

{PRIOR_FILES_SECTION}

{PRIOR_ROUND_SECTION}

{PRIOR_ARBITRATION_SECTION}

### Output

Return your Capability Declaration as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
### Required Sections

Your output must contain exactly these sections, in this order:

---

## Core Competencies

What {AGENT_NAME} does better than any alternative participant in this deliberation.

Rules:
- Every claim must cite specific evidence from your documentation (feature, API, config option, architecture pattern).
- "Better" means measurably or structurally superior, not just "also capable." If you can do X and so can another tool, this is Shared Territory, not a Core Competency.
- Limit to capabilities that are **central** to your purpose, not edge features.
- For each competency, state the evidence in one sentence. Reviewers will verify it.

## Unique Capabilities

Things **only** {AGENT_NAME} can do among the participants. Zero overlap.

Rules:
- These are capabilities no other participant in this deliberation can replicate.
- Be precise. "Handles configuration" is too broad. "Resolves transitive dependency conflicts using lock-file diffing" is verifiable.
- If you are unsure whether another participant can also do something, put it in Shared Territory instead. Claiming uniqueness that gets disproven is the most expensive overreach.

## Shared Territory

Capabilities where {AGENT_NAME} overlaps with one or more other participants.

Rules:
- For each shared capability, name the other participant(s) who also cover it.
- Give an honest relative-strength assessment: are you stronger, weaker, or roughly equal? State why.
- Do not concede territory you genuinely own just to appear modest — that is sandbagging, and reviewers will flag it.
- Do not claim dominance you cannot evidence — that is overreach, and reviewers will flag it.

## Deferrals

Areas where {AGENT_NAME} explicitly defers to another participant.

Rules:
- Name the specific participant you defer to and the specific capability area.
- Explain briefly why they are better positioned (their architecture, their scope, their existing implementation).
- Genuine deferrals build trust and protect your accuracy score. But only defer where it is actually true.
- Do not use deferrals strategically to avoid scrutiny on areas you actually cover. Reviewers will flag sandbagging.

## Integration Surface

How {AGENT_NAME} connects to other participants at boundaries.

Rules:
- Describe the handoff points: what does {AGENT_NAME} produce that others consume? What does {AGENT_NAME} consume that others produce?
- Be specific about formats, protocols, file types, APIs, or conventions at the boundary.
- This section is not scored directly, but it grounds the Responsibility Map that the synthesis will produce.

---

## Constraints

- Write in third person ("{AGENT_NAME} provides..." not "I provide...").
- Do not speculate about other participants' capabilities — only reference what you know from the target document or your own docs.
- Do not pad with generic statements. Every sentence should be verifiable or falsifiable.
- Length: be thorough but not verbose. A strong declaration is typically 400-800 words depending on the tool's scope.
