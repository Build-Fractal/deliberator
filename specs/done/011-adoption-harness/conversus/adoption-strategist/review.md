# Adoption Strategist Review: Conversus Adoption Harness (Spec 011)

---

### Executive Summary

The Adoption Harness proposal aims to transform conversus from a power-user tool requiring hand-crafted YAML and game theory knowledge into a general-purpose decision-making tool accessible to everyone. It proposes three user tiers (Just Ask, Guided, Power), five distribution formats (MCP Server, CLI, Web App, Claude Code Skill, Python SDK), model agnosticism via LiteLLM, and a build order that starts with engine extraction and ends with a consumer web app. The vision is sound: conversus today has a real adoption ceiling because configuration complexity gates access.

However, the proposal makes a critical strategic error: it sequences build order by technical dependency rather than by adoption velocity. The build order starts with Python engine extraction and LiteLLM integration — infrastructure work that produces zero new users. Meanwhile, the existing decision framework (spec 003, `999-decision-framework/spec.md`) already provides a guided workflow that dramatically lowers the barrier to entry, and it ships entirely within the current Claude Code runtime. The proposal treats spec 003 as step 6 of 8 instead of recognizing it as the single fastest path to initial adoption. Additionally, the proposal spreads thin across five distribution formats simultaneously without validating that any single channel produces engaged users.

My most important recommendation: ship "Just Ask" mode as a Claude Code skill within the existing runtime in two weeks, validate it with 100 real decisions, and let usage data — not architectural ambition — drive the subsequent build order.

---

### Alignment

- **Three-tier user model** (`L25-31`): The tiered approach (Just Ask / Guided / Power) correctly recognizes that different users need different entry points. This maps directly to the guided workflow spec 003 already defines (`999-decision-framework/spec.md, L12-17`), which transforms conversus from a "deliberation tool" into a "decision-making framework" via five progressive commands. The tier model is the right mental framework for adoption.

- **"Just Ask" mode as zero-config entry point** (`L33-45`): This is the single most important feature for adoption. The spec correctly identifies that the atomic unit of value is answering a question, not configuring a deliberation. The decision framework spec already lays groundwork for this with its `/conversus define` command that accepts natural language (`999-decision-framework/spec.md, L26-75`) and auto-classifies problem types.

- **Community preset library** (`L116`): Presets as a growth flywheel is strategically correct. Like npm packages or Homebrew formulas, presets turn users into contributors and create network effects. The decision framework's mode selection heuristics (`999-decision-framework/spec.md, L322-343`) provide the foundation — presets would encode proven agent configurations for common decision types.

- **MCP server as primary integration path** (`L74-86`): The tool surface design is well-structured. Mapping the five guided workflow commands (`define`, `interests`, `mode`, `converge`, `run`) to MCP tools creates a clean programmatic API. This aligns with the decision framework's command architecture (`999-decision-framework/spec.md, L449-458`).

- **Plain-language mode descriptions** (`L94`): Replacing game theory jargon ("winner-take-all") with user-facing language ("Pick the best option") directly addresses the decision framework's constraint that game theory knowledge must not be required (`999-decision-framework/spec.md, L521`).

---

### Missed Opportunities

- **No validation milestone before building infrastructure**: The proposal goes straight to Python engine extraction (step 1) without first validating that "Just Ask" mode produces decisions people actually trust. The decision framework spec already defines the complete guided workflow within the existing Claude Code runtime (`999-decision-framework/spec.md, L547-566`). Shipping spec 003 Phase A inside Claude Code costs nothing architecturally and produces real usage data. Impact: **high**.

- **No definition of the "100 users" milestone or adoption metrics**: The proposal describes five distribution formats but never defines what adoption success looks like. How many people need to use conversus before investing in the web app? What retention metric matters — do users come back for a second deliberation? Without these gates, the build order becomes a waterfall plan disconnected from market feedback. The decision framework's success criteria (`999-decision-framework/spec.md, L479-511`) define functional quality but not adoption quality. Impact: **high**.

- **No competitive positioning or differentiation strategy**: The proposal asks "What's the moat?" in the vision section but never answers it. The core differentiator is structured multi-agent deliberation with game-theoretic incentives — but this must be communicated in the first 30 seconds of a user's experience. The README (`README.md, L3-5`) describes this well: "competition dynamics change how agents argue." The "Just Ask" mode must visibly demonstrate this difference, not just produce a recommendation. Impact: **high**.

- **Missing "show your work" output mode**: The proposal's "Just Ask" mode returns "a plain-English synthesis" (`L41`), but this hides conversus's core differentiator. Users need to see agents disagreeing — the cross-review attacks, the rebuttals, the concessions. The decision framework already produces a rich artifact tree (`999-decision-framework/spec.md, L277-293`). "Just Ask" should produce a concise answer plus a collapsible "see the debate" section. Without this, conversus is indistinguishable from asking ChatGPT. Impact: **high**.

- **No seeding strategy for community presets**: The proposal mentions community presets (`L116`) but provides no plan for initial library seeding. The first 20 presets need to be built by the conversus team and cover high-value, high-frequency decisions: framework selection, architecture pattern choice, build-vs-buy, hiring decision structure. These presets also serve as marketing: "Here are 20 decisions conversus helps you make better." Impact: **medium**.

- **No referral or sharing mechanism in the architecture**: The web app mentions "share links" (`L97`), but sharing should be a first-class feature across all distribution formats. When someone gets a good decision from conversus, making it trivially easy to share that result (with the visible debate) is the highest-leverage growth mechanic. The decision framework's artifact chain (`999-decision-framework/spec.md, L259-300`) produces durable, shareable files — but nothing in the proposal makes sharing a deliberate growth channel. Impact: **medium**.

- **Build order delays the highest-signal distribution channel**: The CLI (`pip install conversus`) is step 3 and MCP server is step 5. But MCP server users (Claude Code, Cursor, Windsurf) are the most likely early adopters — they are already in AI-native workflows. The CLI is a utility; the MCP integration is distribution. The build order should prioritize the channel that puts conversus in front of users who are already making decisions with AI tools. Impact: **medium**.

- **No pricing or sustainability model mentioned**: The proposal includes a SaaS web app (`L99`) but never addresses whether conversus is open source, freemium, or paid. This affects every adoption decision: open-core drives adoption but requires a monetization wedge; fully open source needs community or sponsorship; SaaS needs pricing before launch. The README positions conversus as a framework (`README.md, L1`), which implies open source, but the web app implies SaaS. This tension must be resolved before investing in the web app. Impact: **medium**.

---

### Off-Base Assumptions

- **"MCP is the primary integration path"** (`L74`): The proposal assumes MCP is mature enough and widely adopted enough to be the primary integration strategy. This is premature. MCP adoption is growing rapidly but as of early 2026, the majority of developers using AI coding tools are not yet on MCP-compatible setups. Cursor supports MCP but many users do not configure custom servers. VS Code MCP support is recent. Building the MCP server is correct, but calling it the "primary" path overweights a channel that may reach only thousands of developers today. The primary path for the first 100 users should be the channel with the lowest friction — which is the existing Claude Code skill, where conversus already works. The MCP server should be built as the second distribution channel, validated by the first 100 users' requests for it.

- **"Python engine extraction is step 1"** (`L120`): The proposal assumes the engine must be extracted to Python before any adoption work can happen. This is an engineering-first assumption that delays all user-facing work by the duration of a significant rewrite. The decision framework spec (`999-decision-framework/spec.md, L547-559`) explicitly shows that Phase A (define / interests / mode) has zero dependencies on engine changes — it produces markdown artifacts via conversational commands. "Just Ask" mode could be built as a thin wrapper around the existing skill that auto-generates a `conversus.yml` and delegates to `/conversus run`. The engine extraction is valuable for long-term portability but is not a prerequisite for initial adoption.

- **"The web app is the path to non-technical users"** (`L89-99`): The proposal assumes non-technical users need a web app. In practice, the fastest path to non-technical users is not a custom web app — it is embedding conversus in tools non-technical users already use. A Slack bot, a ChatGPT plugin, or even a simple hosted API with a one-page form would reach non-technical users faster than a full Next.js application. The web app is a significant investment (Next.js + FastAPI + WebSocket + PostgreSQL) that should be validated by demand, not assumed.

---

### Actionable Recommendations

1. **Ship "Just Ask" as a Claude Code skill first** (Priority: P1)
   - **Current state**: "Just Ask" is listed as step 4 of 8, after Python extraction, LiteLLM, and CLI (`L123-124`).
   - **Proposed change**: Move "Just Ask" to step 1. Implement it as a new `/conversus decide` skill command within the existing SKILL.md runtime. It accepts a natural-language question, auto-generates a `conversus.yml` using the heuristics from spec 003 (`999-decision-framework/spec.md, L309-343`), runs `/conversus run`, and returns a plain-language synthesis. No Python extraction needed.
   - **Rationale**: The existing runtime already supports everything needed. The decision framework spec defines the mode selection logic and agent generation approach. This gets a usable product in front of real users in days, not months.
   - **Risk if ignored**: Months of infrastructure work before any user validation. The team builds a Python engine for a product that may need fundamentally different UX.

2. **Define adoption gates before committing to build order** (Priority: P1)
   - **Current state**: The build order (`L118-128`) is a linear sequence with no decision points or validation gates.
   - **Proposed change**: Add explicit gates: "After 50 'Just Ask' runs, review: Do users trust the output? Do they return? What decisions work best? Gate: proceed to CLI/MCP only if retention > X%." After CLI/MCP: "Gate: proceed to web app only if MCP adoption > Y users."
   - **Rationale**: Every successful developer tool (Homebrew, npm, Docker) grew by validating one channel before expanding. Conversus should not build five distribution formats speculatively.
   - **Risk if ignored**: Resources spread across five channels, none reaching critical mass. The "build it and they will come" anti-pattern.

3. **Add "see the debate" to Just Ask output** (Priority: P1)
   - **Current state**: Just Ask returns "a plain-English synthesis with the recommendation, supporting arguments, and dissenting views" (`L41`).
   - **Proposed change**: The output should have two layers: (1) a concise recommendation (2-3 sentences), and (2) a full "debate transcript" showing the agent positions, cross-review attacks, and how the synthesis resolved disagreements. The transcript is what makes conversus visibly different from ChatGPT.
   - **Rationale**: The README's core insight (`README.md, L3-5`) is that "competition dynamics change how agents argue." If users cannot see this dynamic, conversus is just another wrapper. The decision framework's artifact tree (`999-decision-framework/spec.md, L277-293`) already produces this — it just needs to be surfaced.
   - **Risk if ignored**: Users perceive no difference between conversus and asking a single LLM the same question. Zero word-of-mouth, zero organic growth.

4. **Reorder build sequence: MCP before CLI** (Priority: P2)
   - **Current state**: CLI is step 3, MCP server is step 5 (`L122-124`).
   - **Proposed change**: After validating "Just Ask" in Claude Code, build the MCP server next (step 2). The CLI can come later as a convenience wrapper. MCP puts conversus in front of users who are already in AI-assisted workflows — the highest-value early adopter segment.
   - **Rationale**: Distribution matters more than packaging. An MCP tool in Cursor/Windsurf/Claude Code reaches users at the moment of decision-making. A CLI requires users to context-switch.
   - **Risk if ignored**: The CLI ships to developers who must remember to invoke it. MCP integration puts conversus in the flow where decisions happen.

5. **Seed 20 community presets before launching the preset system** (Priority: P2)
   - **Current state**: Community presets are mentioned as "a growth flywheel" (`L116`) with no seeding plan.
   - **Proposed change**: Before launching the preset system, create 20 presets covering: framework selection (React vs Vue vs Svelte), database choice (Postgres vs MySQL vs Mongo), architecture pattern (monolith vs microservices), cloud provider (AWS vs GCP vs Azure), hiring decision structure, product prioritization, investment analysis, and 13 more high-frequency decision types. Each preset includes pre-written agent prompts, recommended documentation sources, and the optimal competition mode.
   - **Rationale**: Empty marketplaces do not grow. The initial presets demonstrate conversus's range and give new users immediate value. They also serve as templates for community contributions.
   - **Risk if ignored**: The preset system launches empty. Users must write everything from scratch. The flywheel never starts spinning.

6. **Resolve open-source strategy before web app investment** (Priority: P2)
   - **Current state**: Open question #3 asks "Should the web app be a SaaS product or self-hostable?" (`L133`). Open question #4 asks about preset governance (`L134`).
   - **Proposed change**: Decide now: the engine and CLI are open source (MIT/Apache 2.0). The web app, if built, is a hosted service with a free tier. Community presets are open. This follows the open-core model that worked for Supabase, PostHog, and similar developer tools.
   - **Rationale**: The open-source decision affects every subsequent investment. If the engine is proprietary, adoption is capped. If everything is open, revenue requires a services model. Deciding now prevents building the wrong thing.
   - **Risk if ignored**: The team builds a web app without knowing whether it is the product (SaaS) or a demo (open source). This leads to confused positioning and wasted effort.

7. **Build a sharing mechanism as a first-class feature** (Priority: P2)
   - **Current state**: Share links are mentioned only for the web app (`L97`).
   - **Proposed change**: Every deliberation output — regardless of distribution channel — should produce a shareable artifact. In Claude Code / MCP, this means a self-contained markdown file or HTML report that can be pasted into Slack, emailed, or linked. In the web app, this means a public URL. The share artifact should include the debate, not just the conclusion.
   - **Rationale**: Word-of-mouth is the primary growth channel for developer tools. A shareable deliberation that shows agents disagreeing and resolving is inherently interesting — it is the kind of output people forward to colleagues.
   - **Risk if ignored**: Users get value from conversus but have no natural way to show others. Growth is limited to direct marketing.

8. **Cut the web app from the initial roadmap** (Priority: P2)
   - **Current state**: Web app is step 7 of 8 (`L127`), with a full Next.js + FastAPI + WebSocket + PostgreSQL stack.
   - **Proposed change**: Remove the web app from this proposal entirely. If adoption via Claude Code skill, MCP, and CLI validates demand from non-technical users, revisit a web app as a separate spec. The tech stack is a significant investment that should be justified by demonstrated demand, not assumed need.
   - **Rationale**: The web app is the highest-cost, highest-risk item in the proposal. It requires frontend, backend, real-time infrastructure, and database — a different skill set than the deliberation engine. Building it before validating demand is the classic "build the product before finding the market" mistake.
   - **Risk if ignored**: Months of development on a web app that may attract zero non-technical users because the tool's value proposition has not been validated with any user segment.

9. **Answer "Why not just ask ChatGPT?" in the first user interaction** (Priority: P3)
   - **Current state**: The proposal does not address how conversus differentiates itself in the user experience.
   - **Proposed change**: The first output of any conversus interaction should include a brief note: "This recommendation was produced by N agents with [cooperative/adversarial] incentives. [X] arguments were challenged and [Y] survived cross-review. Expand to see the full debate." This makes the multi-agent process visible and differentiates from single-model responses.
   - **Rationale**: The README explains why multi-agent deliberation produces different results (`README.md, L1-5`), but this insight must be communicated to users at the point of value delivery, not in documentation they will never read.
   - **Risk if ignored**: Users try conversus once, see a recommendation that looks like any ChatGPT answer, and never return. The structural advantage of multi-agent deliberation remains invisible.

10. **Address the "MCP maturity" open question with a concrete fallback** (Priority: P3)
    - **Current state**: Open question #5 asks "Is MCP mature enough to be the primary integration strategy?" (`L135`).
    - **Proposed change**: Answer it: MCP is the right bet for the AI-native developer segment, but it is not yet universal. The fallback is the Claude Code skill (current) and the CLI. Build the MCP server, but do not depend on it for the first 100 users. Track MCP adoption metrics separately from overall adoption.
    - **Rationale**: Hedging keeps optionality without delaying the MCP investment. The decision framework's entry-point flexibility (`999-decision-framework/spec.md, L244-256`) already supports multiple paths — this is a distribution strategy question, not an architecture question.
    - **Risk if ignored**: The team either over-invests in MCP (building native plugins for every IDE as a hedge) or under-invests (delays the MCP server waiting for maturity that is already sufficient for early adopters).

---

### Referenced Documentation

- `specs/011-adoption-harness/proposal.md` — sections/lines cited: L25-31, L33-45, L41, L74-86, L89-99, L94, L97, L116, L118-128, L120, L122-124, L123-124, L127, L133, L134, L135
- `README.md` — sections/lines cited: L1-5, L3-5
- `specs/999-decision-framework/spec.md` — sections/lines cited: L12-17, L26-75, L244-256, L259-300, L277-293, L309-343, L322-343, L449-458, L479-511, L521, L547-559, L547-566
