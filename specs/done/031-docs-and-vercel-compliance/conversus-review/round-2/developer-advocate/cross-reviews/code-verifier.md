# Developer-Advocate Cross-Review of Code-Verifier -- Round 2

## Dangerous Contradictions

### 1. The three-way provider default mismatch obscures the real developer trap

Code-verifier's new finding (Missed Opportunities #5) identifies a three-way default split: config file defaults to `"anthropic"`, CLI defaults to `"mock"`, SDK defaults to `"mock"`. Code-verifier frames this as a documentation refinement extending the converged CV-3 recommendation. I agree the finding is accurate and important, but the proposed fix -- adding a clarifying sentence to config-reference.md -- underestimates the damage to developers building integrations.

Consider the developer who writes a config file, omits `provider:` (trusting the documented default of `"anthropic"`), and then runs `conversus run config.yml`. They get mock output. They add `provider: anthropic` to their config. They still get mock output, because the CLI flag default silently wins. This is not a documentation gap -- it is a behavioral trap that no amount of prose in config-reference.md will prevent, because the developer's mental model ("config files configure behavior") is contradicted by the implementation.

My review (DA, Actionable Recommendation #7) proposes a namespace explanation in the SDK guide, which partially addresses the SDK default. But neither of us has proposed the fix that would actually prevent the trap: making the import path between config-reference.md and cli.md bidirectional and prominent, with a warning callout (not just a cross-reference) at the point where a developer sets `provider:` in YAML. The danger is that code-verifier's precise technical description ("When `provider` is omitted from the config, it defaults to `anthropic`. However, the CLI `--provider` flag has its own default (`mock`) that takes full precedence") reads as informational rather than alarming. A developer scanning config-reference.md will not internalize a parenthetical about CLI behavior. This needs a visually distinct warning box, not a sentence.

**Cited**: Code-verifier Missed Opportunities #5, Actionable #4. Developer-advocate Actionable #7. Round 1 synthesis Convergence #6.

### 2. The `--phase synthesis` epilog bug is real but the proposed fix is incomplete

Code-verifier's strongest new Round 2 finding (Missed Opportunities #1) identifies that the CLI's own `--help` output shows `--phase synthesis` as an example, but Click constrains `--phase` to `["all", "review"]`. This is a genuine code bug that I missed entirely. However, code-verifier's proposed fix (Actionable #1: change the epilog from `--phase synthesis` to `--phase review`) addresses the immediate error while leaving the deeper problem untouched.

Code-verifier's own Missed Opportunities #2 notes that the docs say nothing about what `--phase review` actually produces. If we change the epilog to advertise `--phase review` without documenting its behavior, we replace a broken example with a confusing one. A developer who sees `--phase review` in the help text and tries it will get Phase 1 output only -- agent reviews with no cross-review, revision, disputes, or synthesis -- and will not know whether this is expected or a failure. The epilog fix and the `--phase` documentation (code-verifier Actionable #9) must ship together or not at all. Shipping the epilog fix alone creates a new documentation gap in the CLI's own help text.

**Cited**: Code-verifier Missed Opportunities #1, #2. Code-verifier Actionable #1, #9.

### 3. `cost_estimate` nullability is symptomatic of a broader happy-path-only pattern

Code-verifier identifies that `Deliberation.cost_estimate` can return `None` but the SDK docs show it without the nullable annotation (Missed Opportunities, Off-Base #2, Actionable #7). This is a correct finding. But code-verifier treats this as an isolated documentation omission worth a P2 fix. From the developer-advocate perspective, this is part of a pattern that code-verifier's own review documents but does not connect: `construct_objective()` raises `ValueError`/`RuntimeError` on bad input (Off-Base #1), `cost_estimate` returns `None` on unparseable config (Off-Base #2), and the `AgentCompleted.response_text` field is optional but documented as required (Missed Opportunities #3).

My review (DA, Missed Opportunities #2) flags the absence of error handling guidance for plugin/domain authors as a distinct gap. Code-verifier's three findings in this round strengthen my case: the SDK documentation systematically presents happy paths without failure modes. The contradiction is that code-verifier proposes individual fixes for each instance (P2 for `cost_estimate`, P3 for `construct_objective`) rather than a systemic fix. A developer building a production integration needs to know, in one place, which SDK calls can fail and how. Individual nullable annotations scattered across pages do not build the mental model that "this SDK's error contract is: check return values, catch ValueError/RuntimeError, and expect None from property accessors."

**Cited**: Code-verifier Off-Base #1, #2, Missed Opportunities #3, Actionable #7, #10. Developer-advocate Missed Opportunities #2, Actionable #5.

### 4. The `CallbackEmitter` callable protocol gap affects every custom integration

Code-verifier's Missed Opportunities #4 identifies that `CallbackEmitter` takes a `Callable[[EngineEvent], None]` but the CLI instantiates it with `RichProgressHandler`, which must implement `__call__`. Code-verifier notes this is "an implementation detail that developers building custom emitters need to understand and is not documented." I agree completely -- and I think code-verifier underrates its severity by not including it in the Actionable Recommendations.

From a developer-advocate perspective, the event system is the primary extensibility mechanism for SDK integrations. A developer building a custom progress display, a logging pipeline, or a webhook forwarder must understand that their handler needs to be callable. The architecture.md event system table (L107) describes `CallbackEmitter` as using "Sync callback" transport but does not show the protocol. My review (DA, Missed Opportunities #1) flags the missing domain-to-pipeline bridge in architecture.md. Code-verifier's finding here reveals a parallel gap: the event-to-developer bridge is also missing. Both findings point to the same systemic issue -- architecture.md describes internal wiring without explaining the developer extension points.

**Cited**: Code-verifier Missed Opportunities #4. Developer-advocate Missed Opportunities #1, Actionable #4.

## Tensions

### 1. Granular code-line citations vs. developer-actionable guidance

Code-verifier's review excels at pinpointing exact lines where code diverges from documentation (e.g., `engine/cli/__init__.py` L95, `engine/config.py` L77, `engine/sdk.py` L182-205). This precision is invaluable for implementers. However, code-verifier's Actionable Recommendations often translate these findings into narrow documentation patches ("add a note," "add a nullable annotation") rather than structural changes that would prevent the class of problem. My review tends toward structural fixes (end-to-end tutorials, error handling subsections, testing patterns) that address multiple findings at once but are harder to scope.

The tension is productive: code-verifier's line-level findings are the evidence base that justifies my structural proposals. Without CV's precision, my "add error handling guidance" recommendation (DA Actionable #5) would be abstract advice. With CV's three specific failure mode findings from this round, it becomes a concrete deliverable with known coverage targets. The risk is that implementers cherry-pick CV's individual fixes and declare the problem solved, leaving the structural gap for the next review cycle.

**Cited**: Code-verifier Actionable #1, #4, #7, #9, #10. Developer-advocate Actionable #1, #2, #5.

### 2. P1 code bugs vs. P1 documentation architecture

Code-verifier promotes the `--phase synthesis` epilog bug to P1 (Actionable #1). This is a legitimate code bug that causes incorrect CLI help output. My P1 items (DA Actionable #1-3) are documentation structural changes: end-to-end domain tutorial, plugin wiring docs, slash command explanation. Both are correct P1 assignments for their respective audiences -- a developer running `conversus run --help` deserves accurate output; a developer building a domain plugin deserves a complete tutorial.

The tension is resource allocation. If the implementation team treats P1 as a single queue, the epilog one-line fix will naturally be prioritized over the multi-page domain tutorial because it is smaller. The Round 1 synthesis resolved the analogous onboarding-vs-extensibility dispute by declaring them "parallel independent tracks." Code-verifier's new P1 code bug should be assigned to the code track (alongside CV-2 scaffolds fix), not inserted into the documentation track's P1 queue. Otherwise it will displace structural documentation work that has higher cumulative impact.

**Cited**: Code-verifier Actionable #1, #2, #3. Developer-advocate Actionable #1, #2, #3. Round 1 synthesis "parallel independent tracks" resolution.

### 3. The `classify` export question remains unresolved in both reviews

Code-verifier's Missed Opportunities #6 confirms that `classify` is not exported from `engine/__init__.py`, referencing the Round 1 actionable item #16. My review (DA Actionable #7) proposes an import namespace explanation that would document both `engine.*` and `conversus.*` namespaces. We agree the gap exists but propose different remediation strategies: code-verifier wants a code change (add `classify` to the export list); I want a documentation change (explain the dual-namespace pattern).

The tension is that both are needed but neither review explicitly says so. If only the code change ships, developers still will not understand why some imports come from `engine` and others from `conversus`. If only the documentation change ships, developers who read `from engine import classify` in the SDK docs will get an `ImportError`. The Round 1 synthesis (item #16) recommended both changes. Neither of our Round 2 reviews challenges that recommendation, but neither explicitly reaffirms the "both" framing either, creating a risk that the dual fix gets silently reduced to one or the other during implementation.

**Cited**: Code-verifier Missed Opportunities #6. Developer-advocate Actionable #7. Round 1 synthesis Actionable #16.

### 4. Code-verifier's `domains/base.md` member list is necessary but insufficient for GitHub readers

Code-verifier (Actionable #6) provides a specific `members:` list for `domains/base.md`: `DomainPlugin`, `DomainContext`, `DomainScore`, `DomainRecord`, `TrendResult`, `Scaffold`, `VariableExtractor`, `load_scaffold`, plus `DomainStore`, `JSONLStore`, `SQLiteStore`. This fixes the inconsistency with sibling API reference pages and ensures correct MkDocs rendering. The Round 1 synthesis (Convergence #4) agreed on adding narrative prose above the autodoc directives.

The tension from my perspective: both of these fixes assume MkDocs as the rendering target. For a developer reading on GitHub (which my review and the Round 1 synthesis identify as a primary consumption surface), the `members:` list is a YAML directive option that renders as nothing. The narrative prose is visible on GitHub, but without the rendered autodoc output beneath it, the page becomes an introductory paragraph followed by an opaque `:::` block. Code-verifier's fix is correct for MkDocs; the narrative prose convergence is correct for GitHub; but neither review has proposed a solution that works well on both surfaces simultaneously. A possible bridge: include a plain-text summary of the key classes and their relationships in the narrative prose itself, so GitHub readers get a useful class listing even without autodoc rendering.

**Cited**: Code-verifier Actionable #6. Developer-advocate Referenced Documentation table (Domain API row). Round 1 synthesis Convergence #4, Systemic Contradiction #3.

### 5. New findings vs. carried-forward findings: scope creep risk

Code-verifier introduces 6 new findings in Round 2 (Missed Opportunities #1-6), of which 4 are genuinely new (the `--phase synthesis` epilog, `--phase review` behavior, `CallbackEmitter` protocol, three-way provider defaults). My Round 2 review introduces 5 missed opportunities, of which 3 are genuinely new (domain-to-pipeline bridge, error handling patterns, scaffold `score()` call convention). Combined, that is 7 new findings across two reviews in Round 2 alone.

The tension is between thoroughness and convergence. Each new finding is individually valid and well-sourced. But the Round 2 process is meant to cross-review Round 1 conclusions and refine priorities, not to open new investigation lines. If Round 3 introduces another 7 findings, the actionable item list will grow unboundedly. Code-verifier acknowledges this implicitly by placing most new findings at P2-P3, but the cumulative effect on the implementation plan is still significant. We should agree that Round 3 will not introduce new findings unless they contradict an existing convergence point.

**Cited**: Code-verifier Missed Opportunities #1-6. Developer-advocate Missed Opportunities #1-5.

## Safe Agreements

### 1. The Round 1 convergence points are confirmed and stable

Both reviews explicitly reaffirm all 7 Round 1 convergence items without reversal. Code-verifier's Alignment section systematically re-verifies each one against source code. My Alignment section confirms each from the developer workflow perspective. The converged items -- `decide` 4-mode note, scaffolds YAML fix, `plugins:` config key, API reference prose, `determine_verdict` split, provider precedence note, `estimate_cost_usd` documentation -- form a stable foundation for implementation. Neither review challenges the Round 1 synthesis's dispositions on the resolved disputes (sync-first SDK ordering, parallel implementation tracks, micro-hint troubleshooting).

**Cited**: Code-verifier Alignment (all 7 items). Developer-advocate Alignment (all 7 items). Round 1 synthesis Convergence #1-7.

### 2. The epilog bug is a genuine code defect that both perspectives can validate

Code-verifier's discovery of the `--phase synthesis` epilog bug (Missed Opportunities #1) is the strongest new finding in either Round 2 review. It is a concrete, verifiable code defect: the Click definition constrains `--phase` to `["all", "review"]` while the help text advertises `--phase synthesis`. From the developer-advocate perspective, this is exactly the kind of finding that justifies having a code-verifier in the review process -- it is invisible from documentation alone and would cause a confusing Click error for any developer who follows the CLI's own guidance. I missed this entirely. The fix is unambiguous (change the epilog string) even though, as noted in Dangerous Contradictions #2 above, I believe it should ship alongside `--phase` behavior documentation.

**Cited**: Code-verifier Missed Opportunities #1, Actionable #1.

### 3. Plugin and domain error handling is an acknowledged gap across both reviews

Code-verifier's Round 2 findings on `cost_estimate` nullability (Off-Base #2), `construct_objective` failure modes (Off-Base #1), and `AgentCompleted.response_text` optionality (Missed Opportunities #3) all point to the same gap that my review identifies at the structural level (DA Missed Opportunities #2, Actionable #5): developers have no guidance on what fails and how to handle it. Code-verifier approaches this from individual API contracts; I approach it from developer workflow patterns. Both perspectives agree the gap exists and must be addressed. The implementation should combine both approaches: individual nullable/exception annotations on the specific APIs (code-verifier's approach) plus a consolidated error handling subsection in the developer guides (my approach).

**Cited**: Code-verifier Off-Base #1, #2, Missed Opportunities #3. Developer-advocate Missed Opportunities #2, Actionable #5. Round 1 synthesis Actionable #12.

### 4. The carried-forward Round 1 items need no further deliberation

Both reviews carry forward their respective Round 1 recommendations without modification: code-verifier carries CV-1, CV-2, CV-3/CV-B, CV-A, CV-7, CV-8 (Actionable #2, #3, #5, #6, #8). I carry DA-1, DA-2, DA-5, DA-6, DA-8, DA-9, DA-10 (Actionable #1-9). Neither review challenges the other's carried-forward items. The Round 1 synthesis's priority assignments and disposition language for these items should be preserved unchanged into the final implementation plan.

**Cited**: Code-verifier Actionable #2, #3, #5, #6, #8. Developer-advocate Actionable #1-9. Round 1 synthesis Actionable Spec Changes #1-23.
