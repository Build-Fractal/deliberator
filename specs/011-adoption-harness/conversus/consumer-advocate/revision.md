# Consumer Advocate Revision — Adoption Harness Proposal (011)

---

### Recommendation Dispositions

#### Recommendation 1: Elevate web-app priority

- **Original position**: Move the web app from build order step 7 to step 4-5, delivered as a single milestone with "Just Ask" engine work.
- **Disposition**: Modified
- **Explanation**:

Four out of four cross-reviews challenged this recommendation. The architect argued the web app should be removed from v1 scope entirely because it "adds 5+ new technology layers" and "creates scope pressure that will force shortcuts in the engine layer" (architect cross-review, Dangerous Contradictions, "Web app priority vs. engine foundation"). The adoption-strategist argued it should be "cut from the initial roadmap" as "the highest-cost, highest-risk item" (adoption-strategist cross-review, Dangerous Contradictions, "Web App Priority vs. Validation-First Sequencing"). The devil's advocate argued it should be "separated into its own spec" because it "introduces authentication, hosting, state management, real-time streaming, and database design" (devil's advocate cross-review, Dangerous Contradictions, "Web app priority vs. web app readiness"). The devex-advocate proposed a compromise sequence where the MCP server ships at step 3 and the web app at step 4-5, conceding that neither should be step 7 (devex-advocate cross-review, Dangerous Contradictions, "Build order inversion").

The architect and adoption-strategist are right that the full web app described in the proposal (Next.js + FastAPI + WebSocket + PostgreSQL + auth + history) is too large to be a step 4-5 deliverable. The devil's advocate is right that the design surface is underspecified. I was wrong to advocate for the full web app at step 4-5 without acknowledging the engineering cost. However, every cross-review also acknowledges that consumers need a non-terminal entry point, and the adoption-strategist explicitly concedes the risk that validating only through developer channels produces "a self-fulfilling prophecy created by the channel selection, not by actual market disinterest" (adoption-strategist cross-review, Dangerous Contradictions).

**Modified recommendation**: The engine API must be designed with web-app consumption as a first-class requirement from step 1 (streaming events, structured output with progressive-disclosure-compatible fields, clarification flow support). A minimal web artifact -- a single-page "Just Ask" interface with no auth, no history, no PostgreSQL -- ships as the step immediately after "Just Ask" engine work. The full-featured web app (history, sharing, accounts) is scoped as a follow-on milestone. This addresses the architect's scope concern, the adoption-strategist's validation concern, and preserves the core consumer requirement: non-technical users must have a non-terminal path to conversus within the initial release cycle.

#### Recommendation 2: Specify vague-question handling for Just Ask

- **Original position**: Add explicit behavior for vague, ambiguous, or unanswerable questions, including conversational clarification (one question, not five).
- **Disposition**: Surviving
- **Explanation**:

No cross-review challenged this recommendation. All four reinforced it. The devex-advocate agreed on the gap and proposed a shared sufficiency-check layer with mode-dependent responses: interactive mode triggers clarification, non-interactive mode triggers structured error (devex-advocate cross-review, Tensions, "Clarification flow: Conversational vs. non-interactive"). The adoption-strategist identified it as a "Critical Gap" safe agreement and endorsed "the consumer-advocate's one-question conversational pattern as the design constraint" (adoption-strategist cross-review, Safe Agreements, "Vague Question Handling Is a Critical Gap"). The devil's advocate agreed and added a cost concern: clarification adds API calls, so it should use a cheap model (devil's advocate cross-review, Tensions, "Vague question handling vs. cost implications"). The architect's review did not address vague question handling at all, which the architect cross-review notes is itself significant: "Architect's silence on this topic does not mean disagreement -- it means the architect does not view input quality as an architectural concern" (my cross-review of architect, Tensions, "Vague question handling: system concern vs. consumer concern").

I accept the devex-advocate's addition of a mode-dependent response (clarification for interactive, structured error for non-interactive) and the devil's advocate's addition that the clarification step must be cost-controlled (cheap model, single lightweight call). These improve the recommendation without changing its core: the "Just Ask" pipeline must handle vague input gracefully, not silently produce shallow output.

#### Recommendation 3: Add example questions to web app landing page

- **Original position**: Add 6-8 clickable example questions spanning consumer domains to the landing page to reduce blank-page anxiety.
- **Disposition**: Modified
- **Explanation**:

The devil's advocate challenged this with an important sequencing argument: "Example questions set expectations. If the examples promise consumer-grade answers... but the underlying deliberation engine has not been validated to produce meaningfully better answers than ChatGPT for those exact questions, the examples become a demonstration of the product's weakness rather than its strength" (devil's advocate cross-review, Tensions, "Example-driven onboarding vs. expectation management"). The adoption-strategist proposed a complementary approach: "Seed 20 community presets before launching the preset system" and suggested that the consumer examples and developer presets should be drawn from the same unified list (adoption-strategist cross-review, Tensions, "Example-Driven Onboarding vs. Speed-to-Ship").

The devil's advocate makes a valid point I did not consider. Example questions are a promise about output quality. Shipping examples before validating that conversus produces meaningfully different output for those exact questions is dangerous -- the examples would highlight the product's weakness, not its strength.

**Modified recommendation**: Example questions should be curated after competitive differentiation testing, not before. Each example must have a validated comparison showing that conversus's multi-agent output is measurably different from a single-model response for that specific question. The example set should be drawn from the same pool as the adoption-strategist's community presets, with consumer-facing language as the web app rendering. Examples should not ship until the quality bar (devil's advocate's Recommendation 1 -- deliberation quality criteria) is met for each example question.

#### Recommendation 4: Design progressive result disclosure

- **Original position**: Structure results in three layers: (1) headline recommendation, (2) summary paragraph, (3) full analysis behind a toggle.
- **Disposition**: Modified
- **Explanation**:

The devex-advocate proposed that the engine should produce structured data (JSON/dataclass) and the progressive disclosure should be a presentation-layer rendering of that structure (devex-advocate cross-review, Dangerous Contradictions, "Just Ask output format"). The architect required that "Just Ask" output follow the same mode-specific template structure so it can participate in the conversus ecosystem (prior: context, dispute parsing) (architect cross-review, Dangerous Contradictions, "Just Ask output format: structured vs. progressive"). The devil's advocate added that the headline layer must not conflict with quality criteria that require acknowledging trade-offs: "A headline that says 'Choose Postgres for your caching layer' satisfies consumer-advocate's UX goal but violates the quality criterion that trade-offs must be acknowledged" (devil's advocate cross-review, Tensions, "Progressive disclosure vs. quality criteria").

I accept the devex-advocate's and architect's position that progressive disclosure is a presentation concern, not an engine concern. The engine should produce structured, ecosystem-compatible output; the web app and CLI render it progressively. I also accept the devil's advocate's constraint that the quality criteria should specify which layer must contain each required element rather than requiring all elements in every layer.

**Modified recommendation**: The engine produces structured output compatible with the conversus ecosystem (parseable by dispute parsing, usable as `prior:` context). This structured output includes machine-extractable fields: a `headline` (one-sentence recommendation that may note the decision is close), a `summary` (key trade-offs), and `full_analysis` (agent arguments and dissent). The web app renders these fields as progressive disclosure layers. The headline may include a brief trade-off qualifier when the quality criteria require it (e.g., "Postgres is recommended, though Redis has advantages for write-heavy workloads"). Layer 2 and 3 carry the full disagreement and evidence requirements. Neither the structured format nor the progressive rendering is derived from the other -- both are renderings of the deliberation result.

#### Recommendation 5: Add confidence indicator to results

- **Original position**: Add "Strong recommendation," "Moderate recommendation," or "Close call" labels derived from dispute counts and cross-review alignment.
- **Disposition**: Modified
- **Explanation**:

The devex-advocate proposed that confidence should be a float (0-1) in structured output, with documented bucket boundaries mapping to consumer-facing labels (devex-advocate cross-review, Tensions, "Confidence indicators: Consumer-facing vs. machine-readable"). This is a reasonable coordination: the float serves developers, the labels serve consumers, and documented thresholds keep them consistent.

No cross-review challenged the recommendation itself; the only tension was format. The adoption-strategist endorsed the concept as part of the differentiation strategy (adoption-strategist cross-review, Safe Agreements, "Conversus must visibly differentiate from single-LLM answers").

**Modified recommendation**: Confidence is a float (0.0-1.0) in the engine output, derived from deliberation dynamics (dispute convergence, cross-review agreement). Documented, configurable bucket boundaries map the float to consumer labels: 0.0-0.4 = "Close call," 0.4-0.7 = "Moderate recommendation," 0.7-1.0 = "Strong recommendation." The web app and prose renderer display the label; the SDK and MCP return both the float and the label. Threshold values are configurable for developer use cases.

#### Recommendation 6: Declare dual-primary integration paths

- **Original position**: Replace "Primary Integration Path" with audience-qualified labels: "Primary Developer Integration Path" for MCP, "Primary Consumer Integration Path" for Web App.
- **Disposition**: Surviving
- **Explanation**:

The devil's advocate challenged this indirectly by arguing that the web app should be deferred entirely, which would make "Primary Consumer Integration Path" a label with no near-term deliverable behind it (devil's advocate cross-review, Dangerous Contradictions, "Build order: consumer-first vs. developer-first"). The architect's review implicitly endorsed MCP-as-primary without qualification (my cross-review of architect, Dangerous Contradictions, "MCP server as primary integration path"). The adoption-strategist proposed sequential validation -- prove one channel first, then expand -- rather than declaring dual primaries upfront (adoption-strategist cross-review, Dangerous Contradictions, "Dual-Primary Integration Paths vs. Single Validated Channel").

The devil's advocate acknowledged the resolution: "The spec should state: 'The web app is the primary consumer distribution path and represents the largest adoption opportunity. It is built after the engine, CLI, and MCP server are stable.'" This is essentially my recommendation with sequencing clarity. The adoption-strategist's sequential approach is compatible: validate developer channels first, then validate the consumer channel, but commit to both as primaries with a timeline. The label matters because it shapes internal prioritization. The devex-advocate agreed the dual-primary framing is correct (devex-advocate cross-review, Safe Agreements, "MCP 'Primary Integration Path' label needs qualification").

I maintain this recommendation. The label is low-cost and high-signal. It prevents the consumer path from being permanently deprioritized. The build sequence can still be developer-first without the label implying that the consumer path is secondary in importance.

#### Recommendation 7: Add mobile-first requirement to web app

- **Original position**: The web app must be designed mobile-first, scaling up to desktop.
- **Disposition**: Modified
- **Explanation**:

The adoption-strategist challenged this as premature, arguing it "increases the perceived scope and cost of the web app, which reinforces my argument that it should be deferred" (adoption-strategist cross-review, Tensions, "Mobile-First Design vs. Channel Validation"). Their proposed resolution: if a minimal web form is the compromise, it should be responsive by default (modern CSS frameworks) but not mobile-optimized with custom mobile UX. The full mobile-first investment happens only if the minimal form demonstrates consumer traction.

This is a fair point. Mandating full mobile-first design for a validation-stage minimal web artifact is scope creep. But responsive-by-default is not the same as mobile-first, and consumer users are overwhelmingly mobile. The question is timing.

**Modified recommendation**: The minimal web artifact (per Modified Recommendation 1) must be responsive and usable on mobile browsers -- this is a baseline requirement, not a mobile-first design mandate. The full mobile-first design investment (custom mobile UX, touch interactions, mobile-optimized layouts) is recorded as a design constraint for the full web app milestone and is not required for the initial validation artifact.

#### Recommendation 8: Specify self-contained share page experience

- **Original position**: Shared links must render standalone pages with no login, no account, no knowledge of conversus required, including a CTA.
- **Disposition**: Modified
- **Explanation**:

The devex-advocate did not mention share links, reflecting a different growth model for developer adoption (devex-advocate cross-review, Tensions, "Share links: Viral growth mechanism vs. API endpoint"). The adoption-strategist agreed that sharing is critical growth infrastructure and proposed it should be cross-channel, not web-app-only (adoption-strategist cross-review, Safe Agreements, "Sharing as Growth Mechanism"). The adoption-strategist also proposed that if the web app is scoped down, the share page must be included in the minimal scope (my cross-review of adoption-strategist, Tensions, "Sharing mechanism priority").

The adoption-strategist's framing is stronger than my original: sharing should be a property of every deliberation output, not just a web-app feature. A developer who runs conversus from CLI should also get a shareable artifact.

**Modified recommendation**: Every deliberation output -- regardless of distribution channel -- should produce a shareable artifact. For CLI/SDK/MCP, this is a self-contained HTML or markdown report. For the web app, this is a standalone URL that renders without login, shows the question, recommendation, key arguments, and includes a CTA ("Ask your own question"). The share page is in-scope for the minimal web artifact (per Modified Recommendation 1), not deferred to the full web app. Share functionality is a cross-channel feature, not a web-only feature.

#### Recommendation 9: Add consumer domain routing

- **Original position**: Add a secondary classification layer for consumer domains (personal finance, career, travel, health, entertainment) that adjusts agent personas, disclaimers, and output tone.
- **Disposition**: Modified
- **Explanation**:

The adoption-strategist argued this should be data-driven: "Ship 'Just Ask' without domain routing first. Track what categories of questions users actually ask. After 200-500 real questions, build domain routing for the top 3-5 observed categories" (adoption-strategist cross-review, Tensions, "Consumer Domain Routing vs. Adoption Simplicity"). The devil's advocate added that domain routing could mask quality problems: "Domain routing could become a substitute for real deliberation quality -- if the agents are well-named and domain-appropriate but do not actually produce adversarial pressure, the output looks good but is not better than ChatGPT" (devil's advocate cross-review, Tensions, "Domain routing vs. competitive differentiation"). The devex-advocate proposed implementing domain awareness as a preset layer, not core engine logic: "A 'personal-finance' preset would include risk-averse agent templates, disclaimer text, and formal output tone -- without requiring the engine to know about finance" (devex-advocate cross-review, Tensions, "Scope of 'Just Ask' auto-generation").

All three challenges have merit. The adoption-strategist is right that pre-building domain routing for hypothesized categories is premature. The devil's advocate is right that domain polish can mask deliberation quality problems. The devex-advocate's preset-based implementation is architecturally cleaner than baking domains into the engine.

**Modified recommendation**: Do not build domain routing for v1. Ship "Just Ask" with domain-agnostic classification. Track what categories of questions users actually ask. After sufficient usage data (200-500 real questions), build domain-specific presets for the top 3-5 observed categories. Domain awareness is implemented as a preset layer (per devex-advocate's architecture), not as core engine logic. Each domain preset must meet the devil's advocate's quality criteria (minimum one substantive disagreement, evidence-grounded positions) and be tested against the single-model baseline before shipping.

#### Recommendation 10: Add result quality feedback mechanism

- **Original position**: Add thumbs-up/thumbs-down on the result page with optional free-text feedback, stored in PostgreSQL.
- **Disposition**: Surviving
- **Explanation**:

No cross-review directly challenged this recommendation. The devil's advocate's quality criteria (Actionable Recommendations, item 1) and the adoption-strategist's validation gates (Actionable Recommendations, item 2) both depend on measuring output quality, which requires user feedback as the ultimate signal. The adoption-strategist's emphasis on data-driven decisions throughout their review implicitly supports a feedback mechanism.

The only modification needed is that the feedback mechanism should not depend on PostgreSQL (which is part of the full web app stack, not the minimal artifact). For the initial minimal web artifact, feedback can be stored in a lightweight backend (serverless function + simple storage). For CLI/SDK, feedback can be an optional CLI flag or SDK method. The recommendation stands: without feedback, product improvement is guesswork.

### New Recommendations

- **Adopt deliberation quality criteria for "Just Ask" mode** (Priority: P1)
  - **Triggered by**: Devil's advocate cross-review, Dangerous Contradictions, "Lightweight deliberation: sufficient vs. structurally degraded." The devil's advocate argued that "a 2-agent, 1-round deliberation is structurally identical to asking two models the same question and having a third summarize -- which is not what makes conversus valuable." My original review endorsed the lightweight default as "correct for consumer use cases" without examining whether it preserves conversus's value proposition.
  - **Proposed change**: Define minimum quality criteria for "Just Ask" output before shipping. At minimum: (1) the synthesis must surface at least one substantive disagreement between agents, (2) each agent must reference specific evidence or reasoning, not just assert positions, and (3) the recommendation must acknowledge trade-offs. If the 2-agent, 1-round configuration cannot meet these criteria, design a "mini-cross-review" (agents respond to each other in a single combined prompt) that preserves adversarial pressure while keeping latency and cost within consumer tolerance. Validate that "Just Ask" output is measurably different from a single-model response for each example question before launch.
  - **Rationale**: The devil's advocate exposed a blind spot in my original review. I endorsed the lightweight default because it serves consumer speed requirements, but I did not ask whether it produces output worth showing. If "Just Ask" delivers results indistinguishable from ChatGPT, the consumer experience fails regardless of how polished the UI is. Quality and accessibility are joint requirements, not trade-offs.

- **Design the engine API with web-app consumption as a first-class input** (Priority: P1)
  - **Triggered by**: Architect cross-review, Dangerous Contradictions, "Web app priority vs. engine foundation," and devex-advocate cross-review, Dangerous Contradictions, "'Just Ask' as CLI-first vs. web-native." The architect proposed that the engine's "async dispatch engine and streaming output contract must be designed with web consumption in mind from phase 1, even if the web UI ships last." The devex-advocate proposed that the engine's "streaming events, clarification flow, and result structure should be co-designed with the web app wireframes, even if the engine ships before the web app."
  - **Proposed change**: The engine extraction (step 1) must include explicit requirements derived from web-app and consumer UX needs: streaming partial results (not just final output), a `NEEDS_CLARIFICATION` state in the execution flow (per the architect's cross-review), structured output with progressive-disclosure-compatible fields (`headline`, `summary`, `full_analysis`, `confidence`), and a clarification flow that supports both interactive and non-interactive modes. These requirements are defined as part of the engine API contract, not deferred to the web app implementation.
  - **Rationale**: My original review argued for "web-native from the start" as a design approach. Multiple cross-reviews correctly pointed out that this risks coupling the engine to HTTP/WebSocket semantics. The right position is: the engine is headless (devex-advocate's position), but the engine's API contract is shaped by consumer UX requirements as first-class inputs (not as afterthoughts when the web app ships). This is the compromise that all four cross-reviews converge toward.

### Position Summary

Of my original 10 recommendations, I withdrew 0, modified 7, and maintained 3.

The most significant change in my thinking was prompted by the devil's advocate's challenge to my endorsement of the lightweight deliberation default. My original review treated consumer speed and the 2-agent, 1-round configuration as correct without examining whether it produces output that justifies the product's existence. The devil's advocate's argument -- that a 2-agent, 1-round deliberation without cross-review is "structurally identical to asking two models the same question and having a third summarize" -- exposed a genuine blind spot. I was optimizing for consumer UX (fast, cheap, simple) without ensuring the underlying output is worth presenting. This led to the new P1 recommendation on deliberation quality criteria, which I now consider inseparable from the consumer experience: a beautifully designed web app showing results no better than ChatGPT is a beautifully designed failure.

My remaining highest-priority recommendation is the specification of vague-question handling for "Just Ask" mode (original Recommendation 2, surviving). This earned unanimous agreement across all four cross-reviews and additional design constraints from each (mode-dependent responses from devex-advocate, cost control from devil's advocate, architectural hook point from architect). Vague question handling is where consumer adoption succeeds or fails: non-technical users are the most likely to provide unclear input and the least equipped to know what the system needs. The decision framework already has the `[CLARIFY: ...]` mechanism; the adoption harness must adapt it into a conversational, cost-controlled, mode-aware clarification step that works across all distribution channels. If "Just Ask" cannot handle "help me decide," every other consumer feature is irrelevant.
