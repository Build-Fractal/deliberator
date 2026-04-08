# Cross-Review of Developer-Advocate's Round 2 Review

**Reviewer**: user-advocate
**Reviewing**: developer-advocate Round 2 review
**Round**: 2 of 3

---

## Dangerous Contradictions

### 1. The end-to-end domain tutorial (DA-1) is P1 for developers but unreachable without the front door fixes we both agree on

Developer-advocate's review places the end-to-end domain tutorial as "the single highest-impact change for the developer audience" (Actionable Recommendations #1) and correctly identifies that building-domains.md promises a 5-stage lifecycle but only delivers 2 stages. I agree the gap is real. However, developer-advocate's own Off-Base Assumptions #2 concedes that "if resources are serial, the synthesis's own note -- 'onboarding changes have higher expected impact per hour due to audience breadth' -- effectively makes onboarding first." My review identifies at least two front-door problems that Round 1 missed entirely: the `pip install conversus` vs. `uv sync` discrepancy on the index page (my Recommendation #2), and the `uv run` prefix inconsistency between the quickstart and the CLI reference (my Recommendation #4). These are not cosmetic -- they produce errors on first contact. A developer who arrives at building-domains.md via the quickstart will have already encountered failures that neither review's domain tutorial can recover from. The danger is not disagreement about whether the tutorial matters (we agree it does) but about whether shipping the tutorial without fixing the install path creates a documentation suite where the advanced content works but the entry point does not. We should explicitly state that the domain tutorial is P1 for the extensibility track but that the install-path contradictions must not be deprioritized below P1 on the onboarding track.

### 2. Plugin wiring steps (DA-2) describe a workflow that config-reference.md cannot yet support

Developer-advocate's Recommendation #2 proposes adding developer-facing wiring steps to building-plugins.md: set `package` to a dotted import path, ensure the module is importable, understand that failure is non-fatal. These steps assume the developer has already discovered the `plugins:` YAML key in their config file. Developer-advocate acknowledges this dependency ("This complements the `plugins:` config-reference addition (Convergence #3)") but then lists the wiring steps as an independent P1 item. My review does not challenge the content of the wiring steps -- they are correct and necessary. The contradiction is in the implementation ordering: if a developer reads building-plugins.md and follows the wiring steps before config-reference.md is updated to include the `plugins:` key, they will look for the `plugins:` field in the config reference, not find it, and lose confidence in the documentation's completeness. Both changes are converged; the danger is shipping one without the other. These should be explicitly paired in the implementation plan, not treated as independent deliverables.

### 3. The import namespace explanation (Recommendation #7) risks deepening the confusion it aims to resolve

Developer-advocate proposes adding a note to the SDK guide explaining that `engine` and `conversus` are "separate Python packages in the same repo." My review does not address this directly, but as a user-advocate I must flag the risk: telling a new user that two different import namespaces are "both correct" and come from "different packages" raises more questions than it answers. A user who has just completed the quickstart does not have a mental model that distinguishes packages within a monorepo. Developer-advocate's proposed text ("Both are installed by `uv sync`; they are separate Python packages in the same repo") assumes familiarity with Python packaging conventions that a first-time user may not have. The Round 1 synthesis tracked a related code change (CV-4, exporting `classify` from `engine/__init__`) that would partially reduce the surface area of this confusion by making `engine` the single entry point for commonly-used symbols. If CV-4 ships first, the namespace explanation becomes simpler because fewer cross-package imports are needed in practice. The contradiction is not in the content but in the sequencing: explaining the split before consolidating the API surface may normalize a confusing pattern that the codebase is already moving away from.

### 4. Error handling guidance (Recommendation #5) prescribes behaviors that no code example validates

Developer-advocate recommends adding error handling guidance for plugin and domain authors, including specific patterns: "Domain extractor exceptions should return empty dicts rather than raising" and "Recommend defensive patterns: `state.plugin_results.get('key', default_value)`." My review acknowledges this gap exists but does not propose specific patterns. The danger is that developer-advocate's recommendations prescribe defensive coding patterns without providing tested examples that prove those patterns work against the actual codebase. For instance, the claim that "plugin `execute()` exceptions are caught by the orchestrator, logged at WARNING, and the plugin is skipped" is stated as fact but was not verified by code-verifier in their Round 2 review. If the orchestrator's exception handling has changed or behaves differently for certain exception types (e.g., `KeyboardInterrupt`, `SystemExit`), the guidance becomes actively harmful. This should be flagged for code-verifier validation before shipping.

---

## Tensions

### 1. Scope of "developer audience" vs. "user audience" remains imprecise

Developer-advocate's Executive Summary frames the review around "three critical developer tasks" that remain impossible from documentation alone. My review frames around "a new user who has never encountered this tool." The Round 1 synthesis identified this as Systemic Contradiction #1 (audience segmentation without explicit scoping) but neither of our Round 2 reviews proposes a concrete mechanism to resolve it. Developer-advocate's Missed Opportunity #1 (domain-to-pipeline bridge) is invisible to my audience; my Missed Opportunity #1 (index page contradictions) is invisible to developer-advocate's audience. We are both correct within our respective frames, but the documentation itself still has no "who this page is for" markers. This tension will recur in Round 3 unless one of us proposes an audience-labeling scheme.

### 2. How much the quickstart should explain about slash commands

Developer-advocate's Recommendation #3 proposes "2-3 sentences" explaining the slash command context switch. My Recommendation #3 proposes a structural fix: a heading break ("## Try the guided workflow (in your AI editor)") plus a 2-sentence explanation. We agree on the problem and the content of the explanation. The tension is about the weight of the fix. Developer-advocate frames this as a minor clarification ("Unchallenged" from Round 1); I frame it as a broken quickstart that loses users at the moment of highest engagement. The resolution probably lies in developer-advocate's framing being right about the content (2-3 sentences is enough) and my framing being right about the presentation (a heading break is necessary to signal the context change). Both should be adopted.

### 3. The `uv run` prefix inconsistency is invisible from the developer-advocate's vantage point

My review identifies a systemic discrepancy: the quickstart uses `uv run conversus ...` but the CLI reference uses bare `conversus ...` (my Recommendation #4). Developer-advocate's review does not mention this, likely because the developer audience is assumed to understand Python packaging and would resolve the discrepancy themselves. This tension is productive: it illustrates exactly the audience segmentation gap. A note at the top of cli.md resolves it for users; leaving it out does not harm developers. The cost of adding the note is one sentence; the cost of omitting it is a class of user failures. I believe this should be added to the onboarding track as a low-effort, high-impact item.

### 4. Whether the "copy-paste test" or the "conceptual accuracy test" should govern first examples

Developer-advocate's Off-Base Assumptions #1 accepts the sync-first SDK ordering but adds a caveat: "a developer who learns the sync pattern first may structure their entire integration around `asyncio.run()` wrappers, missing the event subscription pattern entirely." My Off-Base Assumptions #2 argues the strongest justification for sync-first is the copy-paste test: the first code block should be runnable as `python script.py` without modification. These are different evaluation criteria for the same decision. Developer-advocate's concern is about long-term learning outcomes; mine is about first-contact success. Both are legitimate, and the Round 1 synthesis resolved this well: sync-first code block with an immediate note about async-native architecture. The residual tension is whether the note is strong enough to prevent the "asyncio.run() everywhere" anti-pattern developer-advocate fears. I believe it is, given that the existing Async Patterns section is the next thing a progressing developer will encounter.

### 5. Whether missing example output in the quickstart matters

My Recommendation #5 proposes adding abbreviated terminal output after the "What just happened" section so users can verify success. Developer-advocate's review does not mention this gap. From the developer-advocate's perspective, developers can interpret terminal output without a reference; from the user-advocate's perspective, a new user cannot distinguish between expected output and an error they should investigate. This is a low-stakes tension -- adding 10-15 lines of example output has minimal cost and addresses a real first-contact anxiety. I would welcome developer-advocate's perspective on whether the output would also help developers confirm they are running the correct version or configuration.

---

## Safe Agreements

### 1. The 7 Round 1 convergence items are correctly scoped and should ship as-is

Both reviews affirm all 7 convergence points from the Round 1 synthesis: the `decide` 4-mode note (Convergence #1), the scaffolds YAML fix (Convergence #2), the `plugins:` config-reference addition (Convergence #3), the API reference narrative prose (Convergence #4), the `determine_verdict` split (Convergence #5), the provider precedence note (Convergence #6), and the `estimate_cost_usd()` documentation (Convergence #7). Neither review challenges the scoping, wording, or priority of any of these items. This is a strong foundation: 7 items with unanimous or bilateral agreement, covering both code changes and documentation changes, ready for implementation.

### 2. The domain tutorial and plugin wiring gaps are real and must be addressed

Developer-advocate's Recommendations #1 and #2 (end-to-end domain tutorial, plugin wiring steps) identify gaps I also acknowledged in my review. My review describes the building-domains guide as promising "5-stage lifecycle, delivers 2 stages" and the building-plugins guide as "solid but missing wiring steps." We agree on the diagnosis. The only disagreement is about relative priority against onboarding fixes, which the Round 1 synthesis resolved via the parallel-tracks framing that both reviews now accept. The content of the domain tutorial (DomainContext construction, extract/score/persist/serve flow) and the plugin wiring steps (dotted import path, sys.path requirements, failure modes) should proceed without further deliberation on whether they are needed.

### 3. The parallel-tracks implementation framing is accepted by both sides

Developer-advocate's Off-Base Assumptions #2 explicitly accepts the parallel-tracks framing: "I accept this framing but note that the domain tutorial (DA-1) should not be deprioritized to P2 just because onboarding is broader." My Alignment section #8 states: "I accept the synthesizer's resolution that onboarding and extensibility are independent work streams." This dispute is resolved. Both tracks are P1 for their respective audiences. Neither blocks the other. If resources are serial, onboarding has higher expected impact per hour, but both reviews now frame this as a resource allocation observation, not a priority ranking.

### 4. The `conversus status` command belongs in the quickstart after API key setup

Developer-advocate's Recommendation #9 and my Recommendation #10 both endorse adding `conversus status` to the quickstart's "Try with a real provider" section. This was Round 1 P3 item #20, carried forward without challenge. It is the simplest verification step a user or developer can run to confirm their environment is correctly configured. No further deliberation needed.
