# Negotiation Disputes — Phase 4: Final Terms and Deal-Breakers

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. This is the final phase before the mediator synthesizes the deal. You have stated your position, exchanged counter-offers, and revised your terms. Now you declare your final position: what terms you insist on, where you have flexibility, and what breaks the deal.

## What to Read

1. **All parties' revised positions** (Phase 3 revisions):
{ALL_REVISION_PATHS}

2. **Your own revision** (for reference):
   `{MY_REVISION_PATH}`

3. **Target document**:
   the target files:
{TARGET_FILES}

4. **Your documentation**:
{AGENT_DOCS}

Read all revision documents before writing. Focus on where parties' revised positions still diverge.

## What to Produce

Return your final position as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
Your final position must contain the following sections in this exact order:

---

### Unresolved Terms

Terms where your revised position still conflicts with at least one other party and you are not willing to concede further. 2-4 items:

- **Term: [Label]**
  - **My position**: [Your term, as stated in your revision. Cite your revision section.]
  - **Their position**: [Which party disagrees and what they propose. Cite their revision.]
  - **Why I hold firm**: [Your argument, grounded in your interests and evidence.]
  - **Proposed resolution**: [A specific compromise, conditional acceptance, or "the mediator must decide."]

### Agreed Terms

Terms where all parties now converge. 3-6 items:

- **Agreed: [Term label]**
  - **Shared term**: [The exact term all parties accept. State it precisely.]
  - **Agreeing parties**: [Which parties agree, with revision references.]
  - **Strength**: Unanimous | Bilateral
  - **How agreement was reached**: [Was this agreed from Phase 1, or did it emerge through counter-offers?]

### Final Position Statement

**Deal-Breakers** (1-3 items):
Terms that are absolutely non-negotiable. For each:
- The term (1 sentence).
- Why it is a deal-breaker (1-2 sentences, with documentation reference).

**Flexibility** (1-3 items):
Terms where you are willing to accept an alternative formulation. For each:
- The term (1 sentence).
- What you are flexible on and what must be preserved.

**Walk-Away Point**: Under what specific conditions you would prefer no deal to a bad deal.

---

## Rules

- **Unresolved terms must be real.** If the counter-offer process resolved everything, say so. An empty unresolved section is a valid and positive outcome.
- **Do not re-litigate Phase 3 concessions.** If you conceded a term in revision, you cannot bring it back here.
- **Deal-breakers must be defensible.** Anything you declare a deal-breaker will receive extra scrutiny from the mediator. Only claim this status for terms backed by essential interests.
- **Be concise.** The mediator will read all parties' final positions. Repetition dilutes your strongest terms.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate. Include the complete final position.
