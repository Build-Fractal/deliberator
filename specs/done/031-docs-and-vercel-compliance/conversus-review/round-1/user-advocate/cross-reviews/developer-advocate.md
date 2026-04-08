# Cross-Review of developer-advocate's Review

**Cross-reviewer:** user-advocate
**Reviewing:** developer-advocate's Phase 1 review
**Date:** 2026-04-02

---

## Dangerous Contradictions

- **Priority inversion on who the docs serve first**
  - **developer-advocate claims**: The single most important recommendation is "add a complete end-to-end walkthrough for building and running a domain plugin" (Executive Summary, final paragraph). Their P1 items are: end-to-end domain tutorial, plugin wiring/discoverability docs, and adding `plugins:` to the config reference (Recommendations #1-#3).
  - **user-advocate claims**: The single most important recommendation is "add a Prerequisites and Concepts section before the guided workflow that explains what Claude Code slash commands are, what `uv` is, and what MCP means" (Executive Summary, final paragraph). My P1 items are: quickstart prerequisites, slash command explanation, and fixing the "4 modes" factual error (Recommendations #1-#3).
  - **Why this is dangerous**: If the team adopts developer-advocate's P1 priorities, they will invest their documentation sprint on domain plugin tutorials and plugin wiring -- pages that matter only to developers already committed to extending conversus. Meanwhile, the quickstart remains broken for anyone who does not already have `uv` installed, the guided workflow is unusable for anyone unfamiliar with Claude Code, and the landing page contradicts the modes page on how many modes exist. New users never get past the front door, so the domain plugin tutorial has no audience. Conversely, if only my priorities are adopted, experienced developers who want to build plugins or domains are left reading source code. Both P1 lists need to be addressed; the danger is treating either set as deferrable.
  - **Suggested resolution**: Treat the two P1 sets as two tracks: "onboarding track" (my #1-#3) and "extensibility track" (developer-advocate's #1-#3). Both are P1 but for different audiences. If forced to sequence, onboarding comes first because it gates the audience for everything else.

- **Scope of the "4 modes" inconsistency**
  - **developer-advocate claims**: The CLI `decide` command's `--mode` flag lists only 4 of the 8 modes (not flagged in developer-advocate's review -- they do not mention this at all). Their review does not identify the index.md "4 competition modes" claim or the CLI's 4-mode list as issues.
  - **user-advocate claims**: The index page says "4 competition modes" (Off-Base Assumptions, third bullet) and the CLI `--mode` description lists only 4 modes (Recommendation #10). Both contradict the modes page and config reference, which document 8.
  - **Why this is dangerous**: Developer-advocate's silence on this issue could be read as implicit agreement that the current state is acceptable. But a factual inconsistency between the landing page, CLI reference, and modes page will confuse every user -- new and experienced alike. A developer reading the CLI reference and building tooling around it would assume only 4 modes are available for programmatic use.
  - **Suggested resolution**: Acknowledge this as a documentation bug regardless of audience. Update index.md, cli.md, and any other page that enumerates fewer than 8 modes. This is a low-effort, high-trust fix.

- **API reference stubs: narrative prose vs. autodoc enhancement**
  - **developer-advocate claims**: "Add a brief narrative section (3-5 sentences) before each autodoc directive explaining what the module does, its key classes, and how they relate. For `api/domains/base.md`, add the full member list" (Recommendation #4, Priority P2). The framing is about adding context to assist developers who have the source code but need orientation.
  - **user-advocate claims**: "Add 3-5 sentences above each `:::` directive describing what the module does, its key classes, and a one-line usage example. This ensures GitHub readers get value even without a built MkDocs site" (Recommendation #6, Priority P2). The framing is about making the pages useful to evaluators reading raw Markdown on GitHub.
  - **Why this is dangerous**: The recommendations sound similar but serve different audiences with different needs. Developer-advocate wants navigation context ("how these classes relate"); I want standalone comprehensibility ("what this module does and a usage snippet"). If both are implemented without coordination, the API reference pages could end up with redundant or conflicting prose sections -- one oriented toward experienced developers, one toward newcomers.
  - **Suggested resolution**: Write a single prose section per API page that serves both needs: open with what the module does (new user), then list key classes with one-line descriptions and relationships (developer), then link to the relevant developer guide page (both). One section, not two.

- **Where plugin config documentation belongs**
  - **developer-advocate claims**: The `plugins:` key is missing from config-reference.md and should be added as a dedicated section (Recommendation #3, Priority P1). The config reference is "the single source of truth for the YAML schema."
  - **user-advocate claims**: The config reference lacks a "copy this and modify it" starter template (Recommendation #9, Priority P3), but I did not flag the missing `plugins:` key specifically -- my review focused on the config reference as overwhelming for new users rather than incomplete for plugin developers.
  - **Why this is dangerous**: If the `plugins:` key is added to the config reference without also adding it to a minimal starter template or clearly marking it as optional/advanced, new users will see it in the "full schema" section and assume they need to configure plugins to use conversus. This would increase the intimidation factor I already flagged. On the other hand, omitting it from the config reference means the reference is factually incomplete.
  - **Suggested resolution**: Add the `plugins:` key to the config reference as developer-advocate recommends, but place it in a clearly labeled "Advanced" or "Extensibility" subsection below the core fields. The minimal starter template (if adopted from my review) should explicitly exclude it.

---

## Tensions

- **Async-first SDK vs. new user accessibility**
  - **developer-advocate** does not flag the SDK's async-first presentation as a problem. Their review praises the event subscription model (Alignment, fifth bullet) and the async patterns, treating them as well-documented features for developers who will integrate conversus into pipelines.
  - **user-advocate** flags the async-first quick start as a missed opportunity (Missed Opportunities, fifth bullet; Recommendation #4, Priority P2): most Python developers will paste the first example into a script and get a `SyntaxError`.
  - **Tension**: Developer-advocate's audience is comfortable with async Python. Mine is not. Moving the sync example to the top (my recommendation) could make the SDK page feel less "production-grade" to developer-advocate's audience. The resolution is straightforward (sync first, async second, both on the same page) but requires agreement that the SDK page serves onboarding, not just reference.

- **Error handling documentation: who needs it and why**
  - **developer-advocate** flags missing error handling guidance as a medium-impact missed opportunity (Missed Opportunities, third bullet) and recommends documenting the skip-on-error behavior so plugin authors know to return empty data rather than raising (Recommendation #5).
  - **user-advocate** did not flag this because error handling in plugin development is outside the new-user scope.
  - **Tension**: This is a real gap that I missed because of my lens. Developer-advocate is right that a plugin author who does not know about silent skip behavior will write broken plugins. The tension is only about prioritization -- adding error handling docs is clearly valuable but competes with onboarding fixes for documentation sprint time.

- **Testing guidance for plugins and domains**
  - **developer-advocate** flags the absence of testing examples as a medium-impact missed opportunity (Missed Opportunities, fourth bullet; Recommendation #6, Priority P2), noting that frozen Pydantic models require explicit construction.
  - **user-advocate** did not raise this, as testing guidance is beyond first-contact user concerns.
  - **Tension**: Similar to error handling -- this is a legitimate gap that my review's scope excluded. If the documentation sprint is time-boxed, this competes with onboarding improvements. The tension is about which audience's gaps are addressed first, not whether the gaps exist.

- **`determine_verdict` documentation accuracy**
  - **developer-advocate** identifies a concrete code-documentation mismatch: the `determine_verdict` example in building-domains.md checks `minimum_overall`, but the base class default does not implement this check (Off-Base Assumptions, first bullet; Recommendation #7).
  - **user-advocate** did not flag this because new users are unlikely to read the domain plugin guide closely enough to notice the mismatch.
  - **Tension**: This is a correctness issue that could cause real bugs for domain authors. It should be fixed regardless of audience prioritization, but its priority relative to onboarding fixes is where the tension lies. Developer-advocate rates it P2; I would defer it to after onboarding fixes are in, but I agree it needs fixing.

- **Quickstart troubleshooting vs. quickstart brevity**
  - **developer-advocate** praises the quickstart as functional (Executive Summary: "the quickstart gets a developer from zero to a working deliberation in under a minute") and does not recommend adding a troubleshooting section.
  - **user-advocate** recommends adding a troubleshooting section (Recommendation #5, Priority P2) covering `uv` not found, Python version errors, and missing API keys.
  - **Tension**: Adding troubleshooting makes the quickstart longer, potentially undermining the "under a minute" quality developer-advocate praises. The resolution is to add troubleshooting as a collapsible section or a linked page rather than inline content, preserving the quickstart's brevity while giving stuck users somewhere to go.

---

## Safe Agreements

- **Mock provider for zero-cost exploration is correctly implemented**
  - Both reviews independently identify the `--provider mock` default in the quickstart as a strong onboarding decision. Developer-advocate calls it "the correct onboarding pattern" that "removes the highest friction point" (Alignment, first bullet). I call it the removal of "the single biggest friction point in LLM tool onboarding" (Alignment, first bullet). No disagreement on this point.

- **Cost estimation documentation is strong and important**
  - Developer-advocate praises cost estimation in both CLI and SDK as "critical for developer trust" (Alignment, second bullet). I praise the same feature, noting the formula table and worked example make it concrete (Alignment, third bullet). Both reviews agree this is well-documented and important to preserve.

- **API reference pages are unusable in raw Markdown form**
  - Developer-advocate flags the autodoc stubs as giving "nothing" to "a developer without the source code installed" (Missed Opportunities, fifth bullet; Recommendation #4). I flag the same pages as "effectively blank" for "anyone reading the docs on GitHub" (Missed Opportunities, sixth bullet; Recommendation #6). Both reviews agree that narrative prose is needed above the `:::` directives. The implementation details differ slightly (see Dangerous Contradictions above) but the diagnosis is shared.

- **Architecture documentation does not explain domain integration**
  - Developer-advocate flags that the architecture page "does not explain where domain plugins fit into the execution flow" (Missed Opportunities, eighth bullet; Recommendation #8). While I did not flag this explicitly (architecture was outside my new-user lens), I agree that the three-layer diagram in architecture.md mentions domains without explaining how data flows between the engine and domain layers. This gap would confuse any user who reads the architecture page expecting a complete picture of the system.
