# Resource Allocation Disputes — Phase 4: Final Allocation Claims

You are **{AGENT_NAME}**.

{AGENT_PROMPT}

## Your Task

You are participating in a **{MODE}** multi-agent deliberation. This is the final phase before the allocator produces the allocation table. Declare your final demand, where you agree with others' allocations, and what allocations you contest.

## What to Read

1. **All agents' revised demands** (Phase 3 revisions):
{ALL_REVISION_PATHS}

2. **Your own revision** (for reference):
   `{MY_REVISION_PATH}`

3. **Target document**:
   the target files:
{TARGET_FILES}

4. **Your documentation**:
{AGENT_DOCS}

## What to Produce

Return your final allocation claim as your response — the engine will write it to `{OUTPUT_PATH}` verbatim. Do NOT use the Write or Edit tools.
---

### Contested Allocations

Resources where your revised demand still conflicts with another agent's demand and the pool cannot satisfy both. 2-4 items:

- **Contested: [Resource label]**
  - **My claim**: [Your demand, citing your revision.]
  - **Competing claim**: [Which agent demands what, citing their revision.]
  - **Why I should receive this**: [Your argument, grounded in impact and efficiency evidence.]
  - **Proposed resolution**: [Split formula, priority ranking, or "the allocator must decide."]

### Agreed Allocations

Resources where all agents' revised demands fit within the pool. 3-5 items:

- **Agreed: [Resource label]**
  - **Allocation**: [Who gets what.]
  - **Agreeing agents**: [Names with revision references.]
  - **How agreement was reached**: [From Phase 1 or through challenges?]

### Final Demand Statement

**Non-Negotiable Demands** (1-3 items):
Resources you must receive at minimum-viable level:
- The resource and quantity (1 sentence).
- Why it is non-negotiable (1-2 sentences, with evidence).

**Flexible Demands** (1-3 items):
Resources where you accept a reduced allocation:
- The resource (1 sentence).
- What minimum you would accept and under what conditions.

---

## Rules

- **Contested allocations must be real.** If challenges resolved all conflicts, say so.
- **Do not re-litigate Phase 3 reductions.** If you reduced a demand in revision, you cannot inflate it here.
- **Non-negotiable demands must be defensible.** Only claim this for minimum-viable needs.
- **Be concise.** The allocator reads all agents' claims. Repetition dilutes your case.
- **Response IS the file.** Your entire response will be written to `{OUTPUT_PATH}` by the engine verbatim. Do NOT use the Write or Edit tools. Do NOT prefix your response with status messages ("I've completed…", "I've written…") or any meta-commentary. Do NOT summarize or truncate.
