# Developer Advocate -- Round 2 Disputes

## Remaining Disputes

### Dispute 1: The domain tutorial (DA-1) must not be gated behind install-path resolution

Both code-verifier (New-1, New-2) and user-advocate (Recommendation 2, New Recommendation A) have elevated the install-path consistency issue (`pip install conversus` vs. `uv sync`) to P1 and framed it as a blocker for downstream documentation trustworthiness. I agree the install-path issue is P1. I disagree that it blocks the domain tutorial.

My Recommendation #1 revision already accepts an explicit dependency: "the tutorial cannot land effectively if the install path remains contradictory." That was a sequencing note for the implementation plan, not a gating condition. Code-verifier's New Recommendation A now frames the install-path fix as something that must "be resolved first or simultaneously" with all developer guide work. User-advocate's New Recommendation 1 says the plugin and config-reference changes "must be explicitly paired as a single deliverable."

The risk of this framing is scope creep that delays substantive content. The domain tutorial touches `building-domains.md`. The install-path fix touches `index.md`, `quickstart.md`, and `cli.md`. These are different files, different audiences, and different review cycles. A developer who has already cloned the repo and run `uv sync` does not need the install path to be resolved on the index page before they can benefit from a complete domain lifecycle tutorial. Coupling these as a single deliverable creates exactly the kind of "all or nothing" release that the parallel-tracks resolution in Round 1 was designed to prevent.

My position: the install-path fix and the domain tutorial should ship in parallel, not in sequence. The tutorial should include its own self-contained setup preamble (`git clone` + `uv sync` + `uv run python`) that does not depend on the index page being consistent. If the install-path fix ships first, great. If the tutorial ships first with a correct local preamble, also fine. Neither blocks the other.

### Dispute 2: Error handling documentation should prescribe defensive patterns, not just describe framework behavior

Code-verifier's correction to my Recommendation #5 was factually right: the framework catches extractor exceptions at `domains/base.py` L697-708, so advising developers to swallow exceptions was wrong. I accepted this and revised the guidance to describe the actual catch-and-skip behavior. But in my revision I also wrote: "downstream consumers should use `.get()` with defaults." Code-verifier did not challenge this, but user-advocate's New Recommendation 2 flags the entire error handling section for "code-verifier validation before shipping" and treats the prescriptive patterns as unverified claims.

User-advocate is being overcautious here. The `.get()` pattern is not a claim about framework behavior -- it is a standard Python defensive programming recommendation. If a plugin declares `consumes = ["equilibrium_score"]` and the producing plugin fails, the consuming plugin receives a `state.plugin_results` dict without that key. Telling developers to use `.get("equilibrium_score", default_value)` is not a framework behavior claim that needs source verification; it is a Python dict access pattern that is correct regardless of what the framework does.

The deeper disagreement: code-verifier's revision says "the fix should still be instance-specific" (each function's failure semantics are different). I agree for the SDK documentation, where each function has different return types and exception classes. But for plugin and domain authoring, the guidance should be prescriptive. A developer writing their first plugin needs a pattern to follow, not a catalog of every possible exception type the framework might throw. "Raise freely, use `.get()` with defaults for consumed data, check logs for warnings" is a three-line recipe that covers 90% of cases. The remaining 10% (custom exception types, retry logic, circuit breakers) belongs in an advanced guide, not the introductory building-plugins page.

My position: the error handling subsection should include both descriptive content (what the framework does) and prescriptive content (what the developer should do). The prescriptive patterns (`.get()` with defaults, checking logs for plugin skip warnings) do not require source-code verification because they are defensive programming patterns, not claims about framework internals.

### Dispute 3: The "copy-paste test" principle must not become a maintenance trap for example output

User-advocate's copy-paste test principle (Recommendation 8) has now been endorsed by code-verifier, who proposes generalizing it to "every first code example on a page should be self-contained and runnable without modification." I support this principle for code examples. I dispute its application to output examples.

User-advocate's Recommendation 5 (add example output to the quickstart "What just happened" section) was narrowed in revision to "8-10 lines, abbreviated, phase markers and final verdict only." Code-verifier accepted this with the fragility caveat. But the copy-paste test principle, if applied consistently, would also demand that the output example be accurate -- a user who runs the command and sees different output will lose confidence, which is the exact failure mode the principle is designed to prevent.

Mock provider output is not stable across versions. Phase marker formatting, agent names, timing information, and verdict wording can all change without a breaking change being declared. An output block in the quickstart becomes a de facto integration test that must be updated with every release. The quickstart is the highest-traffic page in the documentation; a stale output example on this page is worse than no output example at all, because it signals "these docs are not maintained."

My position: the copy-paste test applies to input (code the user types or pastes). It should not be extended to output (text the tool produces). The quickstart should describe what output to expect in prose ("You will see five phase headings followed by a final verdict"), not show a literal output block. This is more durable and does not create a maintenance obligation that will inevitably be violated.

## Convergence

### 1. The epilog fix and `--phase review` documentation are a single deliverable (P1)

Code-verifier elevated Recommendation 9 to P1 and coupled it with Recommendation 1 (the `--phase synthesis` epilog bug). User-advocate independently identified the "broken self-help loop" where a user tries the invalid `--phase synthesis`, falls back to `--phase review`, and cannot interpret the output. My revision already endorsed this coupling. All three agents now agree: fixing the epilog without documenting `--phase review` behavior creates a new trap. This is the strongest three-way convergence to emerge in Round 2.

### 2. The install-path inconsistency is P1 and the most dangerous first-contact failure

All three agents now agree that `pip install conversus` on the index page contradicting `git clone` + `uv sync` in the quickstart is the single most dangerous onboarding defect. Code-verifier confirmed the structural evidence (pyproject.toml local entry points, no published PyPI package). User-advocate discovered it. I escalated it by connecting it to the import namespace confusion (`engine` vs. `conversus`). The fix must determine whether a PyPI package exists and unify the install instruction across index page, quickstart, and CLI reference.

### 3. Plugin wiring steps and `plugins:` config-reference addition ship together

My Recommendation #2 (plugin wiring steps) and the Round 1 converged item (add `plugins:` to config-reference.md) are explicitly paired by all three agents. User-advocate's New Recommendation 1 formalizes this as a process requirement. Code-verifier's Recommendation 5 disposition confirms the config-reference side. I accept the pairing without reservation.

### 4. MkDocs is the primary reading surface, with GitHub as a best-effort fallback

All three agents converged on declaring MkDocs as the primary documentation surface. Code-verifier's modified Recommendation 6 adds a plain-text class catalog to API reference pages so GitHub readers get a useful listing. User-advocate's Recommendation 7 proposes stating this explicitly with build instructions. My New Recommendation C endorses the same. The resolution: declare MkDocs primary, add `uv run mkdocs serve` instructions, and include plain-text summaries above `:::` directives for GitHub readers. No agent disputes this.

### 5. SDK happy-path-only documentation is a systemic issue requiring inline annotations

Code-verifier's modified Recommendation 7 absorbs the individual `cost_estimate` nullability note and `construct_objective` failure modes into a single item covering all SDK functions with `| None` returns or exception-raising implementations. My revision accepted the pattern identification. User-advocate endorsed it. The resolution is inline annotations at each documented call site (not a single "error handling" section), targeting the three source-verified instances: `cost_estimate`, `construct_objective`, `classify`. This is the right granularity.

## Final Position Statement

### Non-Negotiables

**The domain tutorial (DA-1) is P1 and must not be subordinated to onboarding fixes.** The parallel-tracks resolution from Round 1 established that onboarding and extensibility serve different audiences and touch different files. The install-path fix is also P1, but for the onboarding track. Coupling them as a single deliverable or establishing a hard sequencing dependency undermines the parallel-tracks agreement that all three agents accepted. A developer who has already installed the tool needs the domain tutorial regardless of whether the index page says `pip install` or `uv sync`.

**Error handling documentation must be prescriptive, not merely descriptive.** Describing framework catch-and-skip behavior is necessary but insufficient. A developer writing their first plugin needs actionable patterns: use `.get()` with defaults, raise exceptions freely, check logs for skip warnings. These patterns are standard defensive programming and do not require source-code verification to be valid.

**Output examples in the quickstart should be prose descriptions, not literal blocks.** The copy-paste test is an excellent principle for input code. Extending it to output creates a maintenance burden that will degrade the highest-traffic page in the docs. Describe expected output in durable prose; do not commit to a literal output block that becomes stale with every release.

### Flexibility

I am flexible on the scope of the `uv run` note in cli.md. User-advocate's option (a) -- a single note at the top -- is the minimum viable fix. If the install-path resolution establishes `pip install -e .` as a documented alternative, the note can mention both invocation styles. I accept either formulation.

I am flexible on whether the domain tutorial includes the API router mounting step inline or cross-references the existing documentation. My original Recommendation #1 listed it as step 6 with "(already documented, cross-reference it)." If the implementation team prefers a full inline example over a cross-reference, I support that. If they prefer a link, I support that too. The critical path is stages 1-5 (construct, extract, score, record, persist); stage 6 (serve) can be handled either way.

I am flexible on the exact placement of the slash command heading in the quickstart. My revision and user-advocate's revision both agree it should appear after the CLI path completes. Whether it falls before or after the "Try with a real provider" section is a layout decision I defer to whoever implements it, as long as it does not interrupt the CLI flow.
