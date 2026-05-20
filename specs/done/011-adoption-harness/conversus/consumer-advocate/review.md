# Consumer Advocate Review — Adoption Harness Proposal (011)

---

### Executive Summary

The Adoption Harness proposal (011) aims to transform conversus from a developer-only tool into a general-purpose decision-making product accessible to everyone. It proposes three user tiers (Just Ask, Guided, Power), five distribution formats (MCP Server, CLI, Web App, Claude Code Skill, Python SDK), model agnosticism via LiteLLM, and a "Just Ask" mode where users type a plain-language question and get a recommendation. The scope is ambitious and the vision is correct: conversus has real value for non-technical decision-makers, but only if they can actually reach it.

The proposal acknowledges consumer users explicitly -- retirees picking stocks, students choosing majors, parents planning vacations -- and places them in the "Just Ask" tier with zero configuration. The web app description (L89-98) reads like a consumer product brief: single text input, live deliberation view, plain-language mode descriptions, share links. The decision framework spec (003) that underpins the guided workflow already mandates jargon-free language and non-expert usability. These are strong foundations.

However, the proposal's build order (L119-127) buries the consumer-facing product at step 7 of 8. Every step before it serves developers. The "Just Ask" mode -- the single most important feature for non-technical users -- is step 4, but it is delivered as a CLI/SDK feature, not a web experience. The web app that would actually put this in front of consumers is nearly last. The proposal also underspecifies what happens when users ask bad, vague, or unanswerable questions, which is the most common consumer scenario. **My most important recommendation: move the web app and "Just Ask" mode into a single deliverable and prioritize it above the MCP server and CLI, because non-technical users are the largest addressable market and they will never use a terminal.**

### Alignment

- **Three-tier user model** (`L25-31`): The tiered approach correctly segments users by technical ability. The "Just Ask" tier with "Zero -- system infers everything" config effort directly matches what consumer users need. This mirrors the decision framework's constraint that the system "Must NOT require coding knowledge to use" [`spec.md, L518-519`].

- **Plain-language mode descriptions** (`L94`): The web app section explicitly calls out using "Pick the best option" instead of "winner-take-all." This aligns with the decision framework's constraint that mode names are "implementation labels" and the guided workflow uses plain-language descriptions [`spec.md, L521`].

- **Auto-generated agents** (`L37-42`): The "Just Ask" mode auto-generates 2-4 agents, picks the optimal competition mode, and returns a plain-English synthesis. This eliminates the three hardest steps for consumers: writing agent prompts, understanding game theory, and configuring YAML. The decision framework's heuristic detection system [`spec.md, L322-343`] provides the underlying capability for this.

- **Web app as consumer product** (`L89-98`): The web app description includes consumer-grade features: single text input landing page, live deliberation view, result page with clear recommendation, decision history, and share links. These are the right features for a consumer product.

- **Plain-English synthesis output** (`L41`): The "Just Ask" mode returns "a plain-English synthesis with the recommendation, supporting arguments, and dissenting views." This matches the decision framework's SC-8 requirement for plain-language output [`spec.md, L509-511`].

- **Lightweight deliberation default** (`L40`): The "2-3 agents, 1 round -- fast and cheap" default for "Just Ask" mode is correct for consumer use cases where speed matters more than exhaustiveness. A parent choosing a vacation destination does not need 5 agents and 3 rounds.

### Missed Opportunities

- **Vague question handling is unspecified**: The proposal's open question 7 (L137) asks "Does 'just ask' mode risk oversimplifying?" but never specifies what happens when a consumer asks a vague or malformed question like "help me decide" or "what should I do about my job." The decision framework already solves this with `[CLARIFY: ...]` tags and interactive clarifying questions [`spec.md, L40-44`], but the "Just Ask" mode description (L35-42) implies a single-shot flow with no clarification step. Consumer users ask bad questions constantly. The system must handle this gracefully or it will feel broken. Impact: **high**.

- **No example-driven onboarding**: The proposal describes a blank text input (L93) but does not mention example questions, templates, or categories that help consumers understand what conversus can do. The decision framework's worked example [`spec.md, L579-609`] demonstrates the power of concrete examples, but this is an appendix for spec reviewers, not a user-facing feature. Consumer products like ChatGPT and Perplexity show example prompts on the landing page. Without them, users stare at a blank box and leave. Impact: **high**.

- **No progressive disclosure of results**: The proposal says results include "recommendation, supporting arguments, and dissenting views" (L41) but does not describe how these are layered for consumers. The decision framework's output format [`spec.md, L185`] always dumps everything into `summary/final.md`. Consumer users need: (1) a one-sentence answer, (2) a one-paragraph explanation, (3) full analysis -- revealed progressively on click/scroll. Dumping the full synthesis on a non-technical user is overwhelming. Impact: **high**.

- **No confidence/certainty indicator**: When a consumer asks "should I buy Tesla stock," the system should communicate how confident the deliberation is in its recommendation. The decision framework's mode selection logic includes a "Confidence" column [`spec.md, L310-319`] for mode recommendations, but no equivalent exists for the final output. Consumers need to know "the agents strongly agreed" vs. "this was a close call with significant dissent." Impact: **medium**.

- **No mobile-first design consideration**: The web app description (L89-98) lists features but says nothing about mobile. Non-technical users are overwhelmingly mobile-first. A parent planning a vacation is on their phone, not at a desktop. The tech stack (L99) specifies Next.js, which supports responsive design, but the proposal never mentions mobile as a requirement. Impact: **medium**.

- **No decision categories or domains**: The "Just Ask" mode treats all questions the same (L35-42). Consumer users benefit from domain-specific handling: personal finance questions should auto-generate risk-aware agents, health decisions should include disclaimers, entertainment recommendations should be lighter and faster. The decision framework's problem type classification [`spec.md, L36, L54-55`] is a start, but it maps to game theory modes, not consumer domains. Impact: **medium**.

- **Share links lack context for recipients**: The proposal mentions "Share links: send a deliberation result to anyone" (L97) but does not describe the recipient experience. When a consumer shares a stock analysis with their spouse, the recipient needs a self-contained, readable page -- not a link into a tool they have never seen. The share page must work without login, without context, and without understanding what conversus is. Impact: **medium**.

- **No feedback loop for result quality**: The proposal has no mechanism for consumers to rate whether the recommendation was helpful. Without this, there is no way to improve "Just Ask" mode's question classification, agent generation, or synthesis quality over time. The decision framework does not address this either. Impact: **low**.

### Off-Base Assumptions

- **"Just Ask" as CLI-first feature** (`L123-124`, build order step 4): The proposal positions "Just Ask" mode as step 4 in the build order, delivered as part of the Python engine before the web app (step 7). This assumes "Just Ask" is primarily an API/CLI feature that the web app will later wrap. This is backwards. For consumers, "Just Ask" IS the web app. The mode, the interface, and the experience are inseparable. Building "Just Ask" as a headless engine and then bolting a web UI onto it will produce a developer tool with a web skin, not a consumer product. The correct approach is to design "Just Ask" as a web-native experience from the start, with the engine as its backend.

- **MCP Server as "Primary Integration Path"** (`L74`): The proposal labels the MCP server as the primary integration path. For developers working in Claude Code, Cursor, or VS Code, this is correct. But labeling it "primary" signals that the web app is secondary. For the non-technical users the proposal explicitly names (L18-20), the web app is the only integration path that exists. The MCP server is invisible to them. The proposal should clearly state that the web app is the primary path for consumers and the MCP server is the primary path for developers -- two equal primaries for two distinct audiences.

### Actionable Recommendations

1. **Elevate web-app priority** (Priority: P1)
   - **Current state**: Web app is build order step 7 of 8 (`L127`), after CLI, MCP server, and guided workflow.
   - **Proposed change**: Move web app to step 4 or 5, immediately after "Just Ask" engine work. Deliver "Just Ask" and web app as a single milestone, not separate steps.
   - **Rationale**: The decision framework's SC-1 (Non-Expert Usability) [`spec.md, L481-483`] defines success as a non-expert going from "I have a decision" to a completed deliberation. Non-experts will not use a CLI. The web app is the only path that satisfies SC-1 for the consumer tier.
   - **Risk if ignored**: The product ships as a developer tool with a web app bolted on months later. Consumer adoption is delayed, and the web app inherits CLI-shaped abstractions that feel wrong in a browser.

2. **Specify vague-question handling for Just Ask** (Priority: P1)
   - **Current state**: "Just Ask" mode description (`L35-42`) implies a clean input-to-output pipeline. Open question 7 (`L137`) raises oversimplification risk but provides no answer.
   - **Proposed change**: Add explicit behavior for vague, ambiguous, or unanswerable questions in "Just Ask" mode. The system should ask one clarifying question (not five), offer to reframe the question, or explain what kinds of questions work best. Model this on the decision framework's `[CLARIFY: ...]` behavior [`spec.md, L44`] but make it conversational, not tag-based.
   - **Rationale**: The decision framework already handles vagueness in the guided workflow [`spec.md, L40-44`]. "Just Ask" mode must handle it too, because consumer users are the most likely to ask vague questions and the least likely to know how to fix them.
   - **Risk if ignored**: Consumers type vague questions, get shallow or confused results, and conclude the tool is useless. First impressions are permanent.

3. **Add example questions to web app landing page** (Priority: P1)
   - **Current state**: Landing page is described as "single text input -- 'What decision are you facing?'" (`L93`).
   - **Proposed change**: Add 6-8 clickable example questions spanning consumer domains: "Should I lease or buy my next car?", "Which major should I choose: CS or economics?", "Where should my family vacation this summer -- beach, mountains, or Europe?", "Should I invest in index funds or individual stocks?" Clicking an example populates the input and runs the deliberation.
   - **Rationale**: The decision framework's worked example [`spec.md, L579-609`] demonstrates how concrete examples make the system tangible. Consumer products universally use example prompts to reduce blank-page anxiety.
   - **Risk if ignored**: Users do not understand what the tool does, type nothing, and leave. Bounce rate will be high.

4. **Design progressive result disclosure** (Priority: P1)
   - **Current state**: Results are described as "recommendation, supporting arguments, and dissenting views" (`L41`) delivered as a single output.
   - **Proposed change**: Structure results in three layers: (1) headline recommendation in one sentence, (2) summary paragraph with key trade-offs, (3) full agent arguments and dissent expandable on demand. The web app result page (`L95`) should default to showing layers 1 and 2, with layer 3 behind a "Show full analysis" toggle.
   - **Rationale**: The decision framework's output goes to `summary/final.md` [`spec.md, L185`], which is a single document. Consumers need the answer first and the reasoning second. This is how Perplexity and Google AI Overviews present results.
   - **Risk if ignored**: Non-technical users are overwhelmed by a wall of agent arguments. They cannot find the recommendation buried in the analysis.

5. **Add confidence indicator to results** (Priority: P2)
   - **Current state**: No mention of confidence or certainty in "Just Ask" mode output (`L41`).
   - **Proposed change**: Add a confidence signal to every result: "Strong recommendation" (agents converged), "Moderate recommendation" (majority agreement with notable dissent), or "Close call" (significant disagreement). Derive this from the dispute count and cross-review alignment in the deliberation output.
   - **Rationale**: The decision framework's mode selection logic includes confidence levels [`spec.md, L310-319`]. Extending this concept to the final output helps consumers calibrate how much to trust the recommendation.
   - **Risk if ignored**: Consumers treat a barely-consensus recommendation the same as a unanimous one, leading to poor decisions and eroded trust.

6. **Declare dual-primary integration paths** (Priority: P2)
   - **Current state**: MCP Server is labeled "Primary Integration Path" (`L74`). Web app is listed as one of five distribution formats (`L53`).
   - **Proposed change**: Replace "Primary Integration Path" with "Primary Developer Integration Path" for MCP. Add "Primary Consumer Integration Path" heading for the Web App section. Both are primary, for different audiences.
   - **Rationale**: The decision framework's backward compatibility table [`spec.md, L443-446`] already distinguishes non-expert and expert paths. The adoption harness should mirror this distinction in its distribution strategy.
   - **Risk if ignored**: Internal prioritization follows the "primary" label, and the web app remains an afterthought. Developer features ship first and shape the product's DNA.

7. **Add mobile-first requirement to web app** (Priority: P2)
   - **Current state**: Web app tech stack specifies Next.js, FastAPI, WebSocket, PostgreSQL (`L99`). No mention of mobile.
   - **Proposed change**: Add to web app requirements: "The web app must be fully functional on mobile browsers. The landing page, deliberation view, and result page must be designed mobile-first and scale up to desktop, not the reverse."
   - **Rationale**: The consumer users named in the proposal (L18-20) -- retirees, students, parents, small business owners -- are mobile-majority demographics. The decision framework does not address distribution format, so this is a gap the adoption harness must fill.
   - **Risk if ignored**: The web app ships as a desktop experience. Mobile users (the majority of consumer traffic) get a cramped, unusable interface.

8. **Specify self-contained share page experience** (Priority: P2)
   - **Current state**: "Share links: send a deliberation result to anyone" (`L97`) with no detail on the recipient experience.
   - **Proposed change**: Specify that shared links render a standalone result page that requires no login, no account, and no knowledge of conversus. The page should show: the question asked, the recommendation, the key arguments, and a CTA to "Ask your own question." The page must load fast and look professional.
   - **Rationale**: Share links are the primary viral growth mechanism for consumer products. If the shared page confuses the recipient, the viral loop breaks. The decision framework's output format [`spec.md, L283-293`] is designed for file-system consumption, not web sharing -- the adoption harness must bridge this gap.
   - **Risk if ignored**: Shared links lead to confusing pages. Recipients do not convert. Organic growth stalls.

9. **Add consumer domain routing** (Priority: P3)
   - **Current state**: "Just Ask" mode classifies questions by type (selection, integration, scoping, stress-test) per the decision framework's taxonomy (`L37`, [`spec.md, L54-55`]).
   - **Proposed change**: Add a secondary classification layer for consumer domains: personal finance, career, travel, shopping, health, entertainment. Use domain to adjust agent personas (a stock-picking deliberation should include a risk-averse agent; a vacation deliberation should include a budget-conscious agent), set appropriate disclaimers (finance and health), and tune output tone (entertainment recommendations can be casual; financial analysis should be formal).
   - **Rationale**: The decision framework's problem type classification [`spec.md, L322-343`] maps to game theory mechanics, not user domains. Consumer users think in domains, not problem types. Domain routing makes the auto-generated agents feel relevant rather than generic.
   - **Risk if ignored**: All consumer questions get the same generic agent treatment. A vacation recommendation feels as clinical as an architecture review.

10. **Add result quality feedback mechanism** (Priority: P3)
    - **Current state**: No feedback mechanism mentioned anywhere in the proposal.
    - **Proposed change**: Add a thumbs-up/thumbs-down on the result page, with optional free-text feedback. Store this alongside the decision in PostgreSQL (already in the tech stack, `L99`). Use aggregated feedback to improve question classification, agent generation templates, and synthesis prompts over time.
    - **Rationale**: The decision framework's SC-2 (Mode Recommendation Accuracy) [`spec.md, L486-487`] targets 80% accuracy on mode selection. Consumer feedback is the only way to measure and improve this in production.
    - **Risk if ignored**: No data on whether recommendations are helpful. Product improvement is guesswork.

### Referenced Documentation

- `specs/011-adoption-harness/proposal.md` -- sections/lines cited: L18-20, L25-31, L35-42, L37, L40, L41, L53, L74, L89-98, L93, L94, L95, L97, L99, L119-127, L123-124, L127, L137
- `specs/999-decision-framework/spec.md` -- sections/lines cited: L36, L40-44, L44, L54-55, L185, L283-293, L310-319, L322-343, L443-446, L481-483, L486-487, L509-511, L518-519, L521, L579-609
