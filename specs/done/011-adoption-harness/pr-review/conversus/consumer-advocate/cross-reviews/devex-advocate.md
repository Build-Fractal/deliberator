# Cross-Review of devex-advocate — by consumer-advocate

---

## Dangerous Contradictions

### DC-1: async-only SDK (G30) priority — P2 vs P3, but for incompatible reasons

devex-advocate argues G30 should be promoted from P3 to P2 because "most Python scripts, CI/CD pipelines, Jupyter notebooks, and synchronous web frameworks (Django, Flask) cannot call `await` without wrapping in `asyncio.run()`" (devex-advocate review, Off-Base Assumptions #1). This framing treats async-only as a developer ergonomics issue solved by a `run_sync()` wrapper.

From the consumer perspective, the async-only SDK is irrelevant to consumer adoption. No consumer will ever call `Deliberation.run()`. The consumer channel is the web form (M005), which already uses `AsyncQueueEmitter` to bridge sync engine to async SSE (M005 review, "Architecture Assessment"). Promoting G30 to P2 on developer ergonomics grounds is fine, but it must not compete for priority with consumer-facing P1/P2 issues (G3, G5, G17, G11) that actually block the web channel. If the team has limited bandwidth and must choose between `run_sync()` and fixing the BYOK race condition (G3), the consumer channel -- the only publicly accessible surface -- must win. The devex-advocate review does not acknowledge this tradeoff.

### DC-2: per_agent_outputs (G31) as P2 vs consumer feedback mechanisms as P2

devex-advocate promotes G31 (no per_agent_outputs in SDK Result) from P3 to P2, arguing it "gates the SDK's usefulness as a building block" for "training data extraction, feature engineering, custom rendering" (devex-advocate review, Missed Opportunities #4). The consumer-advocate review promotes qualitative feedback (free-text field alongside thumbs up/down) to P2 because SC-005 requires 25+ non-technical users and binary feedback from 25 data points is statistically meaningless (consumer-advocate review, Recommendations #5).

These compete for the same priority tier but serve opposite audiences. per_agent_outputs serves developers building downstream pipelines. Free-text feedback serves the team trying to understand why consumers are dissatisfied. Both cannot be P2 at the same time without acknowledging that one serves spec validation (SC-005) and the other serves SDK completeness (FR-015). The synthesis should separate "P2 for launch validation" from "P2 for API completeness" -- these are different urgency timelines. Consumer feedback is needed before the 25-user test; per_agent_outputs is needed before third-party SDK adoption.

### DC-3: "getting started" friction analysis vs consumer onboarding -- same gap, different users

devex-advocate flags a missed opportunity: "Can a developer go from `pip install conversus` to a working deliberation in under 5 minutes?" (devex-advocate review, Missed Opportunities #1). The consumer-advocate review independently flags a parallel gap: no example questions on the landing page, no input guidance, blank-page bounce risk (consumer-advocate review, Recommendations #7).

The danger is that these are diagnosed as the same problem and given a single fix. They are not the same problem. The developer zero-to-working path is blocked by `conversus decide` requiring a provider, OAuth being broken (G10), and no `conversus quickstart` command. The consumer zero-to-working path is blocked by BYOK key requirement, blank form with no examples, and no visible character guidance. A `conversus quickstart` command does nothing for web consumers. Example questions on the landing page do nothing for CLI developers. If the team treats "onboarding friction" as one issue, one audience will be neglected. The synthesis must maintain separate onboarding assessments per channel.

### DC-4: Error handling -- developer diagnostics vs consumer comprehension

devex-advocate recommends preserving `ProviderError.category` through `dispatch_agent` (recommendation #6) so SDK consumers can handle errors programmatically -- "retrying on rate_limit but aborting on auth_error" (devex-advocate review, Recommendations #6). The consumer-advocate review recommends designing consumer-facing error messages for every failure mode with plain-language copy and recovery actions (consumer-advocate review, Recommendations #9).

These are not contradictory in isolation, but they become dangerous if the error architecture serves only one audience. If `ProviderError.category` is preserved for programmatic handling but the web frontend still receives raw category strings like `rate_limit` or `auth_error`, consumers see developer jargon. If the frontend maps categories to friendly messages but the SDK wraps errors in a simplified format, developers lose the programmatic taxonomy. The architecture must serve both: structured categories for SDK consumers, human-readable messages for web consumers, derived from the same error objects. Neither review proposes this unified design.

---

## Tensions

### T-1: `decide` command extraction -- service layer vs consumer API surface

devex-advocate recommends extracting `decide` orchestration into a service function so "the SDK, MCP tool, and CLI all call" it (devex-advocate review, Recommendations #8). This is architecturally sound. However, the consumer web form's `/api/deliberate` endpoint is another caller of the same pipeline. The devex-advocate review frames the extraction as unblocking `--dry-run` and `--budget` -- developer features. From the consumer perspective, the extraction should also unblock consumer-specific behaviors: input guidance injection, consumer-tuned error messages, and the potential demo/trial mode (consumer-advocate review, Recommendations #10). The service function's interface should be designed for all four callers (CLI, SDK, MCP, web), not just the three developer channels.

### T-2: Priority of G17 (FRONTEND_URL) -- "one-line fix" vs systemic deployment gap

The consumer-advocate review rates G17 as P1 because broken share links destroy the primary viral growth mechanism (consumer-advocate review, Recommendations #2). devex-advocate does not mention G17 at all. This is not a contradiction -- devex-advocate's scope is developer experience, and share links are consumer-facing. But the tension is that the synthesis rates G17 as P2 (global-synthesis.md, P2 table), and the devex-advocate review's silence on it could be read as tacit agreement with P2. From the consumer perspective, share links are the sole mechanism by which one consumer brings another consumer to the product. A broken share link in production is not "should fix" -- it is "the product does not function for its intended viral use case." The devex-advocate's omission risks this being deprioritized.

### T-3: Test culture praise -- count vs contributor ergonomics

devex-advocate challenges the synthesis's unqualified praise of 1,318+ tests, noting the `try/except ImportError` pattern across all test files and missing `conftest.py` (devex-advocate review, Off-Base Assumptions #2). The consumer-advocate review does not examine test ergonomics because consumers never interact with the test suite. However, both reviews share a dependency: if the test suite is hard to contribute to, consumer-facing bugs are slower to fix. The tension is real but the devex-advocate's recommendation (#10, P3: add conftest.py) is correctly prioritized below consumer-facing issues. The consumer-advocate agrees with the priority but notes that test contributor friction has a downstream consumer impact that neither review quantifies.

### T-4: 30-second target validation -- devex-advocate silent, consumer-advocate P2

The consumer-advocate review flags that SC-001 (60-second zero-to-recommendation) and US-4 Scenario 1 (30-second target) are never validated with real API providers (consumer-advocate review, Recommendations #8). devex-advocate does not mention latency at all. For developers using the SDK or CLI, latency is controllable -- they can choose providers, adjust parameters, or accept longer waits. For consumers on the web form, latency is the product experience. A 90-second deliberation through Anthropic's API with no progress feedback other than SSE streaming could feel broken. The devex-advocate's silence here is understandable (developers tolerate latency) but creates a gap where the synthesis might deprioritize latency validation because only one advocate raised it.

### T-5: BYOK viability -- existential consumer risk vs non-issue for developers

The consumer-advocate review's strongest finding is that BYOK structurally prevents consumer validation: "can you recruit 25 non-technical users who already have an AI provider API key?" (consumer-advocate review, Recommendations #10). devex-advocate mentions the broken OAuth flow (G10) and empty client_id as developer-facing issues but never questions whether BYOK itself is the right model. For developers, BYOK is natural -- they already have API keys. For consumers, BYOK is an unprecedented barrier. This tension is not resolvable within the PR review -- it is a product strategy question -- but the synthesis must at least surface it rather than treating BYOK as an implementation detail both advocates accept.

---

## Safe Agreements

### SA-1: G4 (--phase broken choices) is correctly P1

Both reviews agree G4 is correctly rated P1. devex-advocate calls it "the single most damaging first-impression bug" because "the CLI actively misleads the developer" (devex-advocate review, Alignment #1). The consumer-advocate review does not discuss G4 because consumers do not use the CLI, but implicitly agrees by not contesting its P1 rating. The fix is a 1-line change to the Choice list. No consumer impact, clear developer impact, universal agreement.

### SA-2: G2 (OAuth state not validated) is a P1 security fix regardless of audience

devex-advocate rates G2 as P1 and provides the exact fix: "add `assert state_returned == state_local` before token exchange" (devex-advocate review, Recommendations #2). The consumer-advocate review focuses on M005 security issues (G3, G5) rather than OAuth because the web form uses BYOK, not OAuth. Both reviews agree that security issues must be fixed before merge -- devex-advocate on the OAuth path, consumer-advocate on the BYOK path. The synthesis correctly lists G2 as P1.

### SA-3: Pure function extraction is the right architecture

devex-advocate identifies pure function extraction as "the strongest finding across all milestone reviews" (devex-advocate review, Executive Summary). The consumer-advocate review implicitly benefits from this architecture: the M005 web backend calls the same engine functions as CLI and SDK, ensuring consumer output quality matches developer output quality (M005 review, "Separation of Concerns"). Both reviews trust the architecture to deliver consistent behavior across channels, which is the foundation for treating consumer and developer paths as equal.

### SA-4: The synthesis underweights consumer readiness as a distinct dimension

devex-advocate notes "the synthesis treats CLI and SDK as separate surfaces" without recognizing the CLI-to-SDK graduation path (devex-advocate review, Off-Base Assumptions #4). The consumer-advocate review notes "the synthesis does not distinguish 'consumer ready' from 'developer ready'" (consumer-advocate review, Off-Base Assumptions #3). Both independently identify the same structural gap in the synthesis: it evaluates issues by technical severity without assessing channel-specific readiness. The synthesis should include separate readiness verdicts for each integration path (CLI, SDK, MCP, web form) rather than a single merged priority list.

---

## Referenced Documentation

| Document | Key Citations |
|----------|--------------|
| devex-advocate review | Executive Summary (compound friction), Alignment #1 (G4), Missed Opportunities #1 (getting started), #4 (per_agent_outputs), Off-Base Assumptions #1 (G30 async), #2 (test culture), #4 (CLI-to-SDK gap), Recommendations #2 (G2 fix), #3 (run_sync), #6 (ProviderError.category), #8 (decide extraction) |
| consumer-advocate review | Executive Summary (BYOK viability), Missed Opportunities #1 (BYOK as sole gate), #3 (error UX), #4 (30-second target), Off-Base Assumptions #1 (M005 bugs as consumer-trust issues), #3 (consumer readiness), Recommendations #2 (G17), #5 (free-text feedback), #7 (example questions), #8 (latency validation), #9 (error messages), #10 (BYOK viability) |
| global-synthesis.md | G2, G3, G4, G5, G10, G11, G17, G30, G31; P1/P2/P3 priority assignments; cross-cutting patterns |
| M001 review | Pure function extraction, test dual-import pattern, conftest.py absence, QualityIndicators |
| M005 review | BYOK race condition, RLS/user_id mismatch, FRONTEND_URL gap, AsyncQueueEmitter, error mapping, share page SSR |
