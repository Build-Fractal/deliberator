# Conversus Run Handoff — specs/011-adoption-harness

## Run Configuration

```yaml
mode: cooperative
target: specs/011-adoption-harness/proposal.md
output: specs/011-adoption-harness/conversus/
iterations: 1
rounds: 1 (default)
arbiter: none
```

## Resolved Agents

| # | Name | Docs | Preset |
|---|------|------|--------|
| 1 | consumer-advocate | specs/999-decision-framework/spec.md | — |
| 2 | devex-advocate | specs/999-decision-framework/spec.md | — |
| 3 | architect | SKILL.md, specs/007-game-engine/spec.md | — |
| 4 | adoption-strategist | README.md, specs/999-decision-framework/spec.md | — |
| 5 | devils-advocate | (none) | presets/role/devils-advocate.yml |

### Agent Prompts

**consumer-advocate:**
```
You are the Consumer Advocate. You represent NON-TECHNICAL users who will
never open a terminal, never write YAML, and never understand what "game
theory mode" means. Your users are: a retiree picking stocks, a college
student choosing a major, a parent planning a family vacation, a small
business owner evaluating vendors, someone deciding which car to buy.

Your core concerns:
- Can my users get value in under 60 seconds with zero setup?
- Is the language jargon-free? ("Pick the best option" not "winner-take-all")
- Are results presented as clear recommendations, not academic analysis?
- Does the web app feel like a consumer product (Perplexity, ChatGPT) not a developer tool?
- What happens when users ask bad or vague questions? Does the system help them or fail?

You are skeptical of anything that requires installation, configuration,
or technical knowledge. If a feature only serves developers, challenge
whether it belongs in v1. Push hard for the "just ask" mode and web app
as the primary product, not an afterthought.
```

**devex-advocate:**
```
You are the Developer Experience Advocate. You represent AI-native engineers
who already use Claude Code, Cursor, Windsurf, VS Code, or similar tools daily.
Your users want conversus to plug into their existing workflow with minimal
friction — not replace it.

Your core concerns:
- Can I install and use this in under 5 minutes?
- Does it integrate as an MCP server, CLI tool, or SDK — not a separate app I have to context-switch to?
- Is the Python package well-designed? Clean API, good types, async support?
- Can I programmatically compose deliberations in my CI/CD pipeline?
- Does model agnosticism actually work, or will it be Claude-first with degraded experience on other models?
- Can I use my own presets, templates, and customizations without forking?

You are skeptical of the web app priority — developers don't want browser
apps for tools. Push for CLI + MCP + SDK as the primary distribution, with
the web app as a nice-to-have for demos and non-technical stakeholders.
```

**architect:**
```
You are the Systems Architect. You evaluate this proposal from the
perspective of engineering feasibility, maintainability, and complexity
management. You have built multi-platform tools before and know the
failure modes.

Your core concerns:
- Is the proposed build order correct? What dependencies are missing?
- The SKILL.md-to-Python extraction is the riskiest step — how do we preserve
  the battle-tested orchestration logic (parallel dispatch, phase barriers,
  context isolation) when moving to a different runtime?
- LiteLLM vs custom provider: what are the real trade-offs?
- How does multi-agent parallelism work outside Claude Code's Agent tool?
  asyncio + concurrent API calls is stated but not designed. This is hard.
- The web app adds massive complexity (auth, hosting, streaming, state
  management). Is it worth it in v1?
- How many of these distribution formats can actually share a single engine,
  and where do they diverge in practice?
- What is the minimum viable extraction? Can we ship a CLI that wraps
  SKILL.md's logic without rewriting it?

You are skeptical of scope. This proposal has 8 build phases. You want to
know: which 2-3 things actually matter, and can we defer the rest without
painting ourselves into a corner?
```

**adoption-strategist:**
```
You are the Adoption Strategist. You think about how tools go from zero
users to widespread adoption. You study how successful developer tools
and consumer products grew. You know that distribution > features.

Your core concerns:
- What is the single fastest path to getting 100 people using conversus?
  Not 100 features — 100 users. What is the atomic unit of value?
- Is MCP really the right bet for distribution, or is it too early/niche?
  How many developers actually use MCP-compatible tools today?
- The "just ask" mode is compelling but risks being "just another ChatGPT
  wrapper." What makes multi-agent deliberation visibly different from
  asking ChatGPT the same question? How do we communicate that difference?
- Build order should be driven by adoption milestones, not technical
  dependencies. What gets users fastest?
- Community presets could be a growth flywheel (like npm packages or
  Homebrew formulas). How do we seed the initial library?
- What's the competitive landscape? Are there other multi-agent deliberation
  tools? What's the moat?
- Open source strategy: what's open, what's proprietary? How does this
  affect adoption vs revenue?

You are skeptical of building in isolation. Push for the smallest thing
that can be shipped to real users and validated before building the next thing.
```

**devils-advocate:**
```
You are the Devil's Advocate. Your job is to challenge the positions
that appear most agreed-upon. When everyone converges on an approach,
find the strongest argument against it. You are not opposed to the
proposal -- you are opposed to unchallenged assumptions. If a position
survives your challenge, it is stronger. If it does not, it was not
ready.
```

## Absolute Paths

- **Target**: `/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/proposal.md`
- **Output base**: `/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/conversus`
- **Templates**: `/Users/brettkellgren/Sites/conversus/templates/cooperative/`

## Phase 1 Status: COMPLETE

All 5 reviews written:
- `specs/011-adoption-harness/conversus/consumer-advocate/review.md` (18793 bytes)
- `specs/011-adoption-harness/conversus/devex-advocate/review.md` (22553 bytes)
- `specs/011-adoption-harness/conversus/architect/review.md` (22293 bytes)
- `specs/011-adoption-harness/conversus/adoption-strategist/review.md` (20180 bytes)
- `specs/011-adoption-harness/conversus/devils-advocate/review.md` (21463 bytes)

---

## Phase 2: Cross-Reviews — 20 Agents

Template: `templates/cooperative/cross-review.md`

Each agent reviews every other agent's review. 5 agents × 4 others = 20 cross-review agents.

### All 20 Cross-Review Pairs

| # | Reviewer (A) | Reviewed (B) | A reads B's review | A reads own review | Output path |
|---|---|---|---|---|---|
| 1 | consumer-advocate | devex-advocate | `conversus/devex-advocate/review.md` | `conversus/consumer-advocate/review.md` | `conversus/consumer-advocate/cross-reviews/devex-advocate.md` |
| 2 | consumer-advocate | architect | `conversus/architect/review.md` | `conversus/consumer-advocate/review.md` | `conversus/consumer-advocate/cross-reviews/architect.md` |
| 3 | consumer-advocate | adoption-strategist | `conversus/adoption-strategist/review.md` | `conversus/consumer-advocate/review.md` | `conversus/consumer-advocate/cross-reviews/adoption-strategist.md` |
| 4 | consumer-advocate | devils-advocate | `conversus/devils-advocate/review.md` | `conversus/consumer-advocate/review.md` | `conversus/consumer-advocate/cross-reviews/devils-advocate.md` |
| 5 | devex-advocate | consumer-advocate | `conversus/consumer-advocate/review.md` | `conversus/devex-advocate/review.md` | `conversus/devex-advocate/cross-reviews/consumer-advocate.md` |
| 6 | devex-advocate | architect | `conversus/architect/review.md` | `conversus/devex-advocate/review.md` | `conversus/devex-advocate/cross-reviews/architect.md` |
| 7 | devex-advocate | adoption-strategist | `conversus/adoption-strategist/review.md` | `conversus/devex-advocate/review.md` | `conversus/devex-advocate/cross-reviews/adoption-strategist.md` |
| 8 | devex-advocate | devils-advocate | `conversus/devils-advocate/review.md` | `conversus/devex-advocate/review.md` | `conversus/devex-advocate/cross-reviews/devils-advocate.md` |
| 9 | architect | consumer-advocate | `conversus/consumer-advocate/review.md` | `conversus/architect/review.md` | `conversus/architect/cross-reviews/consumer-advocate.md` |
| 10 | architect | devex-advocate | `conversus/devex-advocate/review.md` | `conversus/architect/review.md` | `conversus/architect/cross-reviews/devex-advocate.md` |
| 11 | architect | adoption-strategist | `conversus/adoption-strategist/review.md` | `conversus/architect/review.md` | `conversus/architect/cross-reviews/adoption-strategist.md` |
| 12 | architect | devils-advocate | `conversus/devils-advocate/review.md` | `conversus/architect/review.md` | `conversus/architect/cross-reviews/devils-advocate.md` |
| 13 | adoption-strategist | consumer-advocate | `conversus/consumer-advocate/review.md` | `conversus/adoption-strategist/review.md` | `conversus/adoption-strategist/cross-reviews/consumer-advocate.md` |
| 14 | adoption-strategist | devex-advocate | `conversus/devex-advocate/review.md` | `conversus/adoption-strategist/review.md` | `conversus/adoption-strategist/cross-reviews/devex-advocate.md` |
| 15 | adoption-strategist | architect | `conversus/architect/review.md` | `conversus/adoption-strategist/review.md` | `conversus/adoption-strategist/cross-reviews/architect.md` |
| 16 | adoption-strategist | devils-advocate | `conversus/devils-advocate/review.md` | `conversus/adoption-strategist/review.md` | `conversus/adoption-strategist/cross-reviews/devils-advocate.md` |
| 17 | devils-advocate | consumer-advocate | `conversus/consumer-advocate/review.md` | `conversus/devils-advocate/review.md` | `conversus/devils-advocate/cross-reviews/consumer-advocate.md` |
| 18 | devils-advocate | devex-advocate | `conversus/devex-advocate/review.md` | `conversus/devils-advocate/review.md` | `conversus/devils-advocate/cross-reviews/devex-advocate.md` |
| 19 | devils-advocate | architect | `conversus/architect/review.md` | `conversus/devils-advocate/review.md` | `conversus/devils-advocate/cross-reviews/architect.md` |
| 20 | devils-advocate | adoption-strategist | `conversus/adoption-strategist/review.md` | `conversus/devils-advocate/review.md` | `conversus/devils-advocate/cross-reviews/adoption-strategist.md` |

All relative paths above are relative to `specs/011-adoption-harness/`. Prepend `/Users/brettkellgren/Sites/conversus/` for absolute paths.

### Template Variables for Phase 2

For each cross-review agent (A reviewing B):

| Variable | Value |
|---|---|
| `{REVIEWER_NAME}` | A's name |
| `{REVIEWER_PROMPT}` | A's prompt (see Agent Prompts above) |
| `{REVIEWED_NAME}` | B's name |
| `{AGENT_DOCS}` | A's doc paths (see Resolved Agents table) |
| `{REVIEWED_REVIEW_PATH}` | Absolute path to B's `review.md` |
| `{REVIEWER_REVIEW_PATH}` | Absolute path to A's `review.md` |
| `{TARGET_FILES}` | `/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/proposal.md` |
| `{OUTPUT_PATH}` | Absolute path to `A/cross-reviews/B.md` |
| `{MODE}` | `cooperative` |
| `{ROUND}` | `1` |
| `{MAX_ROUNDS}` | `1` |
| `{PRIOR_SYNTHESIS_PATH}` | (empty string) |
| `{PRIOR_ROUND_DIR}` | (empty string) |

---

## Phase 3: Revisions — 5 Agents

Template: `templates/cooperative/revision.md`

Each agent revises their review after reading cross-reviews.

### Template Variables for Phase 3

For each agent:

| Variable | Value |
|---|---|
| `{AGENT_NAME}` | agent name |
| `{AGENT_PROMPT}` | agent prompt |
| `{AGENT_DOCS}` | agent doc paths |
| `{MY_REVIEW_PATH}` | `{output_base}/{agent}/review.md` |
| `{CROSS_REVIEWS_OF_ME}` | All `{other}/cross-reviews/{agent}.md` paths (4 files per agent) |
| `{MY_CROSS_REVIEWS}` | All `{agent}/cross-reviews/{other}.md` paths (4 files per agent) |
| `{TARGET_FILES}` | `/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/proposal.md` |
| `{OUTPUT_PATH}` | `{output_base}/{agent}/revision.md` |
| `{ITERATION}` | `1` |
| `{MODE}` | `cooperative` |

### Cross-Reviews-Of-Me paths (for each agent)

**consumer-advocate** reads:
- `conversus/devex-advocate/cross-reviews/consumer-advocate.md`
- `conversus/architect/cross-reviews/consumer-advocate.md`
- `conversus/adoption-strategist/cross-reviews/consumer-advocate.md`
- `conversus/devils-advocate/cross-reviews/consumer-advocate.md`

**devex-advocate** reads:
- `conversus/consumer-advocate/cross-reviews/devex-advocate.md`
- `conversus/architect/cross-reviews/devex-advocate.md`
- `conversus/adoption-strategist/cross-reviews/devex-advocate.md`
- `conversus/devils-advocate/cross-reviews/devex-advocate.md`

**architect** reads:
- `conversus/consumer-advocate/cross-reviews/architect.md`
- `conversus/devex-advocate/cross-reviews/architect.md`
- `conversus/adoption-strategist/cross-reviews/architect.md`
- `conversus/devils-advocate/cross-reviews/architect.md`

**adoption-strategist** reads:
- `conversus/consumer-advocate/cross-reviews/adoption-strategist.md`
- `conversus/devex-advocate/cross-reviews/adoption-strategist.md`
- `conversus/architect/cross-reviews/adoption-strategist.md`
- `conversus/devils-advocate/cross-reviews/adoption-strategist.md`

**devils-advocate** reads:
- `conversus/consumer-advocate/cross-reviews/devils-advocate.md`
- `conversus/devex-advocate/cross-reviews/devils-advocate.md`
- `conversus/architect/cross-reviews/devils-advocate.md`
- `conversus/adoption-strategist/cross-reviews/devils-advocate.md`

---

## Phase 4: Disputes — 5 Agents

Template: `templates/cooperative/disputes.md`

### Template Variables for Phase 4

| Variable | Value |
|---|---|
| `{AGENT_NAME}` | agent name |
| `{AGENT_PROMPT}` | agent prompt |
| `{AGENT_DOCS}` | agent doc paths |
| `{ALL_REVISION_PATHS}` | All 5 `{agent}/revision.md` paths |
| `{MY_REVISION_PATH}` | `{output_base}/{agent}/revision.md` |
| `{TARGET_FILES}` | target path |
| `{OUTPUT_PATH}` | `{output_base}/{agent}/disputes.md` |

### All revision paths (for ALL_REVISION_PATHS variable)

```
/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/conversus/consumer-advocate/revision.md
/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/conversus/devex-advocate/revision.md
/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/conversus/architect/revision.md
/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/conversus/adoption-strategist/revision.md
/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/conversus/devils-advocate/revision.md
```

---

## Phase 5: Synthesis — 1 Agent

Template: `templates/cooperative/synthesis.md`

### Template Variables for Phase 5

| Variable | Value |
|---|---|
| `{MODE}` | `cooperative` |
| `{TARGET_PATH}` | `/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/proposal.md` |
| `{TARGET_FILES}` | same as TARGET_PATH |
| `{AGENT_NAMES}` | `consumer-advocate, devex-advocate, architect, adoption-strategist, devils-advocate` |
| `{ALL_REVIEWS}` | All 5 `{agent}/review.md` absolute paths |
| `{ALL_CROSS_REVIEWS}` | All 20 `{agent}/cross-reviews/{other}.md` absolute paths |
| `{ALL_REVISIONS}` | All 5 `{agent}/revision.md` absolute paths |
| `{ALL_DISPUTES}` | All 5 `{agent}/disputes.md` absolute paths |
| `{OUTPUT_PATH}` | `/Users/brettkellgren/Sites/conversus/specs/011-adoption-harness/conversus/summary/final.md` |

---

## How to Continue

In a fresh context window, run:

```
/conversus run specs/011-adoption-harness/conversus.yml
```

Then tell Claude:

> Phase 1 is already complete — all 5 review files are written to disk. Read the handoff at `specs/011-adoption-harness/conversus/HANDOFF.md` and continue from Phase 2. Use the pre-computed paths from the handoff. Launch all 20 Phase 2 cross-review agents in parallel.

### Recommended splits

- **Context 2**: Phase 2 (20 agents) — the heaviest phase
- **Context 3**: Phase 3 (5 agents) + Phase 4 (5 agents) — these are lighter
- **Context 4**: Phase 5 (1 synthesis agent) — needs full context of all artifacts, benefits from clean window

Or if you want fewer windows:
- **Context 2**: Phase 2 (20 agents) + Phase 3 (5 agents)
- **Context 3**: Phase 4 (5 agents) + Phase 5 (1 agent)

### Permission Note

In Phase 1, subagents were denied Write/Bash permissions and review content had to be extracted from transcripts. You may want to pre-approve write permissions for the `specs/011-adoption-harness/conversus/` directory to avoid this in subsequent phases.

---

## Final Report Template (after Phase 5)

```
Conversus complete.

Mode: cooperative
Target: specs/011-adoption-harness/proposal.md
Agents: consumer-advocate, devex-advocate, architect, adoption-strategist, devils-advocate
Agents launched: 36
Artifacts: 36
Arbitration: skipped (no arbiter configured)

Output: specs/011-adoption-harness/conversus/
├── summary/final.md          ← start here
├── {agent}/review.md
├── {agent}/revision.md
├── {agent}/disputes.md
├── {agent}/cross-reviews/
```

To apply changes: /speckit.specify --input specs/011-adoption-harness/conversus/summary/final.md
