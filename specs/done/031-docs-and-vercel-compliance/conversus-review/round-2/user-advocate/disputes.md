# User-Advocate -- Final Disputes (Round 2, Phase 4)

**Reviewer role:** user-advocate (new user evaluating from a first-time user's perspective)
**Phase:** Final disputes and convergence before Round 2 synthesis

---

## Remaining Disputes

### 1. The provider default mismatch warrants P1 as a warning callout, not P2 as a documentation note

**My position**: Code-verifier's revision accepts the warning callout format (admonition box in config-reference.md) and accepts the three-way mismatch as "a behavioral trap, not an informational footnote" -- but then assigns P2 because "the user gets mock output instead of real API calls. No money is spent, no incorrect results are generated."

**Why I will not concede**: The safe-failure argument is backwards. A user who writes a config file with `provider: anthropic`, runs `conversus run config.yml` expecting real LLM output, and receives mock output has wasted their time debugging a problem that does not produce an error message. The failure is silent. Silent failures are worse than loud ones because the user does not know they need to debug anything -- they may conclude the tool produces low-quality output rather than that the CLI silently overrode their config. Code-verifier's own revision says "a broken example and an unexplained example are both user traps" (Recommendation 1 modification). A silent default override is a worse trap than either, because the user does not even know they are in one.

**What would resolve this**: Elevate to P1 specifically because of the silent-failure characteristic. The callout box text code-verifier proposed is excellent. The priority is the dispute, not the content.

### 2. The implementation plan must explicitly sequence onboarding fixes before or alongside extensibility content

**My position**: All three revisions now accept the "parallel tracks" framing. Developer-advocate's revision states the domain tutorial (DA-1) "should remain P1 for the extensibility track." Code-verifier's revision adds two new onboarding recommendations (New-1 at P1, New-2 at P2) without stating sequencing. My revision's New Recommendation 1 asks for explicit pairing of plugins changes as a single deliverable.

**Why I will not concede**: "Parallel tracks" is a planning abstraction that dissolves the moment a single implementer sits down to work. My Round 1 dispute on this point was resolved with the synthesizer's note that "onboarding changes have higher expected impact per hour due to audience breadth." Developer-advocate's revision explicitly quotes this note and concedes it. Yet no revision produces an ordered implementation plan. The synthesizer will produce the final plan. I am asking that the plan say: "Batch 1 ships independently: index page install fix, epilog + phase review docs, uv run note, slash command heading, provider warning callout. Batch 2 ships after or alongside Batch 1: domain tutorial, plugin wiring, error handling guidance, testing examples." This is not about devaluing extensibility work. It is about ensuring that the audience for Batch 2 exists by the time Batch 2 ships. Code-verifier's New-1 (the `pip install conversus` finding) is evidence for this: if the index page install command fails, no one reaches the domain tutorial.

**What would resolve this**: The synthesis includes explicit batch ordering with a statement that Batch 1 items can ship independently without waiting for Batch 2, and Batch 2 items should not ship before the install-path contradictions (index page, uv run note) are resolved.

### 3. SDK happy-path-only documentation should be treated as a single P2 deliverable with a stated principle, not individual instance fixes

**My position**: Code-verifier's revision absorbs Recommendation 10 into Recommendation 7 and now covers three source-verified instances (`cost_estimate`, `construct_objective`, `classify`). This is better than the original two-item split. But the revision explicitly rejects "a single sweeping audit" in favor of "instance-specific" fixes because "each nullable return or exception-raising function has different failure semantics."

**Why I will not concede**: I agree that the documentation annotations must be instance-specific. I am not asking for a generic "check for None" section. I am asking for a stated principle in the implementation plan: "Every SDK function shown in documentation whose return type includes `| None` or whose implementation raises exceptions must include an inline annotation describing the failure case." Code-verifier has already identified three instances. The principle prevents future documentation additions from repeating the happy-path-only pattern. Without the principle, the next person who documents a new SDK function will omit failure modes because there is no stated expectation to include them. Code-verifier's "copy-paste test" endorsement from my revision shows they accept documentation principles as durable guidance. This is the same kind of principle, applied to failure-mode documentation rather than example runnability.

**What would resolve this**: The synthesis includes both the three instance-specific fixes and a stated principle for future SDK documentation additions. The principle is one sentence. The cost is negligible. The benefit is preventing recurrence.

## Convergence

### 1. The `pip install conversus` vs. `uv sync` discrepancy is the highest-priority onboarding fix

All three revisions now agree. Code-verifier's New-1 calls it P1 and "potentially the most dangerous first-contact failure in the documentation." Developer-advocate's New Recommendation A calls it P1 and notes it "blocks all downstream documentation from being trustworthy." My Recommendation 2 originally identified it and both cross-reviews validated it without modification. This is the strongest three-way convergence on a new finding in Round 2. The fix must determine whether a PyPI package exists and align the index page with reality.

### 2. The epilog bug fix (Recommendation 1) and `--phase review` documentation (Recommendation 9) are a single P1 deliverable

Code-verifier's revision elevates Recommendation 9 to P1 and couples it with Recommendation 1. Developer-advocate's cross-review originally identified the compounding effect. My cross-review of code-verifier provided the "broken self-help loop" framing. All three revisions now treat these as inseparable. The user who sees `--phase synthesis` in the epilog, gets a Click error, tries `--phase review`, and cannot interpret the partial output -- that entire failure chain is addressed by this single deliverable. No further debate needed.

### 3. The `uv run` prefix note at the top of cli.md is accepted by all three agents with identical scope

Code-verifier's New-2 proposes it at P2. Developer-advocate's New Recommendation B proposes it at P2 with "option A only" (the single note, not the per-example rewrite). My Recommendation 4 proposed it at P1 but my revision accepted the single-note format per developer-advocate's feedback. The content is nearly identical across all three revisions: one sentence explaining that `uv sync` users should prefix with `uv run`. The only remaining difference is priority (I proposed P1, others propose P2). I accept P2 given that this is a one-sentence addition with low implementation risk that can ship in any batch.

### 4. The copy-paste test is accepted as a documentation principle

Code-verifier's revision explicitly endorses generalizing it beyond the SDK Quick Start: "user-advocate's copy-paste test framing is more precise... provides a durable principle." Developer-advocate's revision accepts it as compatible with the async-context note. My revision proposed extending it to all first-example blocks. All three agents agree the first code example on any documentation page should be self-contained and runnable without modification. This principle should appear in the implementation plan as standing guidance, not a one-off fix.

### 5. The slash command context-switch explanation needs both a heading and placement after the CLI path completes

My revision proposed the heading ("## Try the guided workflow (in your AI editor)"). Developer-advocate's revision accepted the heading format but insisted it appear after the CLI path is complete, not mid-flow. Code-verifier supported the heading without reservation. All three revisions now agree on both the mechanism (heading + 2-sentence explanation) and the placement (after "Try with a real provider," not mid-quickstart). This is fully converged.

## Final Position Statement

### Non-Negotiables

1. **The install path must be consistent across the index page and quickstart before any other documentation ships.** Code-verifier's New-1, developer-advocate's New Recommendation A, and my Recommendation 2 all agree this is P1. If `pip install conversus` fails and there is no PyPI package, the documentation's credibility is destroyed on first contact. This is the single item I would ship before everything else if forced to choose.

2. **The SDK documentation must annotate failure modes inline, and the implementation plan must state a principle preventing future happy-path-only additions.** The three specific instances (cost_estimate, construct_objective, classify) are agreed. The principle -- one sentence -- prevents recurrence. Instance fixes without the principle are whack-a-mole.

3. **The synthesis must produce an ordered implementation plan, not just a priority-tagged list.** Batching with explicit sequencing (onboarding fixes can ship independently; extensibility content should not ship before install-path contradictions are resolved) is the mechanism. This does not devalue extensibility work; it ensures the extensibility work has an audience.

### Flexibility

1. **Provider default mismatch priority.** I argued for P1 above, but I will accept P2 if the synthesis commits to the warning callout format (not inline prose) and places it prominently in config-reference.md. The presentation matters more than the priority number if implementation is batched correctly.

2. **Example output in the quickstart.** My original proposal was 10-15 lines. Developer-advocate and code-verifier both constrained it to 8-10 lines showing only phase markers and the final verdict. I accept the narrower scope. The abbreviated block still lets a user verify success.

3. **MkDocs as primary reading surface.** All three agents agree this should be stated. I am flexible on where the statement lives (index page, README, contributing guide) and on the exact wording, as long as it includes the `uv run mkdocs serve` instruction so a user can build the docs locally.

4. **The `conversus status` placement in the quickstart.** I proposed it between the API key export and the `decide` command. If there is a better placement that all agents agree on, I will not dispute it. The command belongs somewhere in the quickstart; the exact line number is not worth fighting over.
