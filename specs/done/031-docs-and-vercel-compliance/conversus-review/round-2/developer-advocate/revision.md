# Developer Advocate Revision -- Round 2, Iteration 1

## Recommendation Dispositions

### From my Round 2 review

**Recommendation #1 (P1): End-to-end domain tutorial in building-domains.md -- MODIFIED.**
Both cross-reviewers affirm this as the highest-impact developer-facing change. Code-verifier raises a legitimate type accuracy issue: my proposed example passes `changed_files=["src/app.py"]` (strings) when `DomainContext.changed_files` is typed as `list[Path]` at `base.py` L44. Pydantic v2 would coerce these, but the documentation should teach the correct type. I accept code-verifier's correction and modify the recommendation: all constructor calls in the tutorial must match source type annotations, and the `changed_files` example should use `[Path("src/app.py")]`. I also accept user-advocate's point that this tutorial cannot land effectively if the install path (index page `pip install conversus` vs. quickstart `uv sync`) remains contradictory -- a developer who enters through the wrong install path will not have the packages needed to follow the tutorial. The tutorial itself is unchanged in scope (5-stage lifecycle as a connected flow); the modification is the type-accuracy constraint and the explicit dependency on install-path consistency being resolved first or simultaneously. Credit: code-verifier Tension #1, user-advocate Dangerous Contradiction #1.

**Recommendation #2 (P1): Practical plugin wiring steps in building-plugins.md -- MODIFIED.**
Code-verifier's Tension #2 corrects my characterization of the plugin loader. I wrote "the loader finds the first `Plugin` subclass in the module -- name your module accordingly." Code-verifier points out that `dir()` returns names in alphabetical order, not declaration order, so `APlugin` always loads before `BPlugin` regardless of where they appear in the file. "Name your module accordingly" is vague to the point of being misleading. I accept code-verifier's proposed wording: "The loader finds the first `Plugin` subclass in the module (by alphabetical attribute name). Define exactly one `Plugin` subclass per module to avoid ambiguity." I also accept user-advocate's Dangerous Contradiction #2 that the wiring steps and the `plugins:` config-reference addition (Convergence #3) must ship together -- a developer reading wiring instructions who then cannot find the `plugins:` key in config-reference.md will lose trust. The modification is: sharpen the loader description per code-verifier, and explicitly pair this with the config-reference `plugins:` addition as a single deliverable. Credit: code-verifier Tension #2, user-advocate Dangerous Contradiction #2.

**Recommendation #3 (P1): Explain slash commands before guided workflow in quickstart.md -- MODIFIED.**
User-advocate's Tension #2 proposes that the heading break is as important as the explanatory sentences. I initially described this as "2-3 sentences" (content only). User-advocate proposes a heading ("## Try the guided workflow (in your AI editor)") plus the explanation. I accept the structural fix: the heading signals a context change that inline sentences alone cannot. However, per my cross-review of user-advocate (Dangerous Contradiction #3), I maintain that the guided workflow section should not be promoted to co-equal status with the CLI path within the quickstart. The heading is the right mechanism but should be positioned after the CLI path completes (after "Try with a real provider"), not mid-page. The modification is: adopt user-advocate's heading format, place it at the end of the quickstart as an optional next step rather than mid-flow. Credit: user-advocate Tension #2. My cross-review Dangerous Contradiction #3.

**Recommendation #4 (P2): Domain-engine integration subsection in architecture.md -- SURVIVING.**
Neither cross-reviewer challenged this. The gap remains: architecture.md's pipeline diagram does not show where domains are invoked relative to the deliberation phases. A developer reading the architecture cannot determine the trigger mechanism for their domain plugin. No modification needed. Surviving as stated.

**Recommendation #5 (P2): Error handling guidance for plugin and domain authors -- MODIFIED.**
Code-verifier's Dangerous Contradiction #2 delivers a direct correction. I wrote "Domain extractor exceptions should return empty dicts rather than raising, to allow partial scoring." Code-verifier shows that `domains/base.py` L697-708 already catches extractor exceptions with a try/except that logs a warning and skips the failed extractor. Telling authors to swallow exceptions would mask failures that the framework was designed to surface in logs. This is a factual error in my recommendation, and I withdraw the specific guidance about returning empty dicts. The corrected guidance should say: "Raise freely -- the framework catches and logs. A failed extractor's variables are simply absent from the merged dict. A failed plugin's results are absent from `state.plugin_results` -- downstream consumers should use `.get()` with defaults." The structural recommendation (add an error handling subsection to both building-plugins.md and building-domains.md) survives, but the content must document the framework's actual catch-and-skip behavior rather than prescribing a new convention. User-advocate's Dangerous Contradiction #4 reinforces this by noting that my original patterns were "prescribed without tested examples." Fair point. Credit: code-verifier Dangerous Contradiction #2, user-advocate Dangerous Contradiction #4.

**Recommendation #6 (P2): Testing examples for plugins and domains -- SURVIVING.**
Neither cross-reviewer challenged the substance. User-advocate acknowledged the gap. The recommendation to add `DeliberationState` and `DomainContext` construction examples in test contexts stands. These examples must use correct types (per the type-accuracy principle established in Recommendation #1's modification). No modification needed.

**Recommendation #7 (P2): Import namespace explanation in SDK guide -- MODIFIED.**
Code-verifier's Tension #3 argues I coupled the documentation note with the `classify` re-export code change, creating an unnecessary dependency. This is correct -- the namespace explanation can ship independently of the code change, and should. User-advocate's Dangerous Contradiction #3 raises a valid concern that explaining two namespaces to a new user may deepen confusion, especially if the codebase is moving toward consolidation via re-exports (CV-4). I accept both critiques. The modification: decouple the documentation note from the code change. Ship a minimal note ("The SDK spans two packages: `engine` for the deliberation runtime and `conversus` for schemas and plugins. Both are installed together.") without elaborating on the monorepo packaging model. If CV-4 ships first and consolidates imports under `engine`, simplify the note further. The user-advocate's sequencing concern is well-taken -- normalize before explaining the abnormal. Credit: code-verifier Tension #3, user-advocate Dangerous Contradiction #3.

**Recommendation #8 (P2): Sync-first SDK Quick Start -- SURVIVING.**
Code-verifier's Tension #4 notes that my added condition ("Event subscriptions require async context") was not part of the Round 1 resolution but accepts it as factually accurate. User-advocate's Tension #4 frames this as the "copy-paste test" vs. "architectural truth" and agrees both the sync wrapper and the async note should be present. No one challenges the recommendation as stated. Surviving with the note about event subscriptions intact. Credit: code-verifier Tension #4, user-advocate Tension #4.

**Recommendation #9 (P3): `conversus status` in quickstart -- SURVIVING.**
Both cross-reviewers independently endorse this. No modification needed. Credit: user-advocate Safe Agreement #4, code-verifier (no mention, unchallenged).

**Recommendation #10 (P3): Minimal starter config callout in config-reference.md -- SURVIVING.**
Neither cross-reviewer challenged this. The recommendation to add a 6-line minimal example at the top of config-reference.md stands as stated. No modification needed.

### From my Missed Opportunities

**Missed Opportunity #1 (domain-to-pipeline bridge in architecture.md) -- SURVIVING as Recommendation #4.**
Already addressed above. Carried forward without modification.

**Missed Opportunity #2 (error handling guidance) -- MODIFIED into Recommendation #5.**
Already addressed above. The specific guidance content was corrected per code-verifier.

**Missed Opportunity #3 (testing patterns) -- SURVIVING as Recommendation #6.**
Already addressed above.

**Missed Opportunity #4 (import namespace ambiguity) -- MODIFIED into Recommendation #7.**
Already addressed above. Decoupled from code change per code-verifier.

**Missed Opportunity #5 (`score()` call convention) -- MODIFIED.**
Code-verifier's Dangerous Contradiction #1 corrects my framing. I characterized the `score()` interface as ambiguous or undiscoverable. Code-verifier shows that `domains/base.py` L711-714 has explicit type annotations (`scaffold: str | Scaffold`) and a docstring explaining that a string argument is resolved as a scaffold name. The gap is real -- the documentation does not show this call -- but the contract is not unclear. The fix is a documentation coverage problem (add the call to the tutorial), not a contract discovery problem (restructure the guide). I accept this reframing. The `score()` call example should be included in the end-to-end tutorial (Recommendation #1) with `domain.score(variables, "default")`, matching the actual signature. No separate recommendation needed. Credit: code-verifier Dangerous Contradiction #1.

### From my Off-Base Assumptions

**Off-Base #1 (sync-first SDK ordering concession) -- SURVIVING.**
My concession with the event-context caveat note stands. Accepted by both cross-reviewers.

**Off-Base #2 (parallel tracks framing acceptance) -- SURVIVING.**
My acceptance of the parallel tracks framing with the note that DA-1 should remain P1 for the extensibility track stands. User-advocate's Safe Agreement #3 confirms this is resolved.

---

## New Recommendations

### New Recommendation A: Pair the install path with the import namespace as a single consistency fix

User-advocate's Dangerous Contradiction #1 identifies that the index page shows `pip install conversus` while the quickstart shows `git clone` + `uv sync`. My cross-review of user-advocate (Dangerous Contradiction #1) escalated this further: a developer who installs via `pip install conversus` and then encounters `from engine import Deliberation` in the SDK guide will hit an `ImportError` with no diagnostic path.

The fix must address three surfaces simultaneously: (1) the index page install command must match reality (either confirm `pip install conversus` works and installs both packages, or change it to the `uv sync` path), (2) the SDK guide imports must be reachable from whatever install method is documented, and (3) the quickstart must not contradict either. This is not three separate fixes -- it is one consistency pass across the install-to-first-import pipeline.

Priority: P1 for the onboarding track. This blocks all downstream documentation from being trustworthy. Credit: user-advocate Missed Opportunity #2, my cross-review Dangerous Contradiction #1.

### New Recommendation B: Add a `uv run` note to the top of cli.md (option A only)

User-advocate's Missed Opportunity #3 identifies the `uv run` prefix inconsistency between quickstart and CLI reference. My cross-review (Dangerous Contradiction #2) endorsed option (a) -- a single note at the top of cli.md -- and explicitly flagged options (b) and (c) as dangerous because they would embed a `uv`-specific assumption that contradicts the `pip install` path.

The note should read something like: "Examples below use bare `conversus` commands. If you installed via `uv sync` (as in the quickstart), prefix with `uv run`." This is install-method-agnostic and costs one line. Priority: P2 for the onboarding track. Credit: user-advocate Missed Opportunity #3, my cross-review Dangerous Contradiction #2.

### New Recommendation C: State MkDocs as the primary reading surface

User-advocate's Off-Base Assumption #3 proposes declaring MkDocs as the primary documentation surface with instructions for local building. My cross-review (Tension #5) endorsed this. The API reference pages (construction.md, base.md for plugins and domains) render as blank `:::` blocks on GitHub but are fully functional under MkDocs. Stating the primary surface explicitly unblocks the API reference work (Convergence #4, code-verifier Recommendation #6 member lists) and prevents future review cycles from re-litigating whether GitHub rendering is a blocking concern.

One sentence at the top of the docs README or index page: "These docs are built with MkDocs Material. For the full experience including API reference, run `uv run mkdocs serve`. GitHub renders most content correctly but API reference pages require MkDocs." Priority: P2. Credit: user-advocate Off-Base Assumption #3, my cross-review Tension #5.

---

## Position Summary

This revision corrects three factual errors in my Round 2 review while strengthening the structural recommendations that both cross-reviewers affirmed. The most important correction comes from code-verifier on error handling: the framework already catches and logs exceptions from extractors and plugins, so my original guidance to "return empty dicts rather than raising" would have actively worked against the framework's design. The corrected recommendation documents the actual catch-and-skip behavior, which is both simpler and more useful for developers. The second correction, also from code-verifier, fixes a type error in my proposed domain tutorial example (`list[str]` vs. `list[Path]` for `changed_files`). The third corrects my characterization of the `score()` interface as ambiguous -- it is typed and docstringed, just not demonstrated in the guide.

The core developer-advocate position is unchanged: the two highest-impact gaps for developers building on this system are the incomplete domain lifecycle tutorial (Recommendation #1) and the missing practical plugin wiring steps (Recommendation #2). Both cross-reviewers agree these gaps are real. The modifications sharpen accuracy and add explicit implementation dependencies (type-check examples against source, pair wiring steps with config-reference update, resolve install-path consistency first). The three new recommendations all come from cross-review insights: the install-path consistency fix (from user-advocate), the `uv run` note (from user-advocate), and the MkDocs surface declaration (from user-advocate). These are onboarding-track items that unblock the developer-track work by ensuring the foundation is solid. I am persuaded by user-advocate's argument that the extensibility content cannot land effectively if the entry path is broken, even though the two tracks are technically independent.

The review process is converging well. Of my 10 original recommendations, 5 survive without modification, 5 are modified (all for the better -- sharper accuracy, clearer dependencies, decoupled implementation). None are withdrawn entirely. The 3 new recommendations fill gaps I missed by focusing too narrowly on the developer guides without examining the entry-point pages. Round 3 should focus on finalizing the implementation plan rather than opening new investigation lines -- the combined findings from all three reviewers now cover the documentation suite comprehensively.
