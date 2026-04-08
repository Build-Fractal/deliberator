# Cross-Review of user-advocate's Review

**Cross-reviewer:** developer-advocate
**Reviewing:** user-advocate's Phase 1 review
**Date:** 2026-04-02

---

### Dangerous Contradictions

- **SDK async-vs-sync first example priority**
  - **user-advocate claims**: "The sync pattern should be the first example, with async as the 'advanced' pattern below" (Missed Opportunities, SDK doc item). The rationale is that most Python developers will paste the first example into a plain script and hit a `SyntaxError` from bare `await`.
  - **developer-advocate claims**: The SDK documentation's async-first approach is listed as an Alignment item: "The SDK provides working async patterns and the event subscription model is well-documented" (Executive Summary). The developer-advocate review does not flag async-first as a problem and instead focuses on the dual import namespace (`engine.*` vs `conversus.*`) as the SDK's primary confusion risk (Recommendation #9).
  - **Why this is dangerous**: If both positions are implemented naively, the SDK page would either flip to sync-first (losing the async patterns that pipeline/CI developers need front-and-center) or stay async-first (continuing to break first-time script users). The deeper issue is audience segmentation: user-advocate optimizes for the script-writing newcomer; developer-advocate optimizes for the integration developer building pipelines. Both are valid primary audiences for the SDK page.
  - **Suggested resolution**: Lead with a two-tab code block (a pattern common in modern docs frameworks like MkDocs Material): one tab labeled "Script (sync)" showing `asyncio.run()`, one tab labeled "Async" showing bare `await`. The sync tab is default-selected. This satisfies user-advocate's "first thing you see must work in a plain script" requirement without demoting the async pattern that developer-advocate considers well-documented and appropriate for the SDK's primary audience.

- **API reference stubs: prose-first vs. autodoc-first**
  - **user-advocate claims**: "There should be at minimum a prose summary of what each module does and its key classes, even if the auto-generated API docs supplement it" (Missed Opportunities, API reference item; Recommendation #6). The rationale is that GitHub is the primary discovery surface and mkdocstrings directives render as blank on GitHub.
  - **developer-advocate claims**: The API stubs should have "a brief narrative section (3-5 sentences) before each autodoc directive" AND specifically for `api/domains/base.md`, the full member list should be added to match the level of detail in `api/plugins/base.md` (Recommendation #4). Additionally, the developer-advocate flags a deeper problem: the stubs are not just cosmetically empty on GitHub -- they fail to document the *relationships* between the listed members, which autodoc alone cannot convey even when rendered.
  - **Why this is dangerous**: If only user-advocate's recommendation is applied (add prose summary), developers still lack the structural relationships (e.g., how `Plugin` relates to `HookPoint` and `execute_hooks`). If only developer-advocate's recommendation is applied (add narrative + member list + "See also" links), the prose might be written in developer jargon that new users cannot parse. The two reviews agree on the symptom but diverge on the depth of the fix.
  - **Suggested resolution**: Apply developer-advocate's fuller recommendation (narrative + member list + cross-links to developer guides) but write the opening sentence of each narrative section at user-advocate's accessibility level -- one plain-English sentence saying what the module is for, followed by developer-oriented structural detail. This layers the audiences rather than forcing a choice.

- **Mode count inconsistency: index.md fix scope**
  - **user-advocate claims**: The index.md "4 competition modes" claim is a factual error and should be fixed to "8 deliberation modes" with all 8 listed or summarized (Off-Base Assumptions; Recommendation #3, rated P1). The CLI `decide` command also lists only 4 modes and should be updated (Recommendation #10, rated P3).
  - **developer-advocate claims**: The developer-advocate review does not flag the index.md mode count at all -- it treats the modes page and config reference (which correctly list 8) as the authoritative sources and focuses instead on the CLI's `--mode` flag listing only 4 as a secondary concern. The developer-advocate's framing implicitly accepts that the CLI only exposes 4 modes for ad-hoc `decide` usage, which may be intentional (the other 4 modes may require config-file setup with agent roles/resources).
  - **Why this is dangerous**: If user-advocate's fix is applied to the index page but not the CLI, users will see "8 modes" on the landing page, try `conversus decide --mode negotiation`, and get an error. If the CLI genuinely only supports 4 modes for ad-hoc use, then the index page should say "8 modes (4 via CLI, all 8 via config)" rather than a flat "8." Applying the user-advocate fix without checking the CLI's actual mode validation could create a new inconsistency.
  - **Suggested resolution**: First verify whether `conversus decide --mode negotiation` actually works. If the CLI restricts ad-hoc mode to 4, the index page fix should say "8 deliberation modes" with a note that ad-hoc CLI supports 4 and config-based runs support all 8. If the CLI supports all 8, both the index and CLI docs should list all 8. The developer-advocate's silence on the index.md issue should not be read as disagreement -- it is a gap in the developer-advocate review, which was scoped to developer-facing docs.

- **Quickstart prerequisites: `uv` dependency**
  - **user-advocate claims**: The quickstart's reliance on `uv` without explanation or `pip` fallback is a P1 issue (Missed Opportunities; Off-Base Assumptions; Recommendation #1). "A user on a corporate laptop without `uv` installed will fail on the very first command."
  - **developer-advocate claims**: The developer-advocate review does not flag `uv` as a problem. The mock provider alignment item (Alignment, first bullet) implicitly accepts the `uv run conversus decide` command as the correct quickstart entry point. The developer-advocate's Recommendation #10 even suggests adding `conversus status` to the quickstart flow, using `uv run` without comment.
  - **Why this is dangerous**: These positions are not in direct conflict, but the developer-advocate's silence on `uv` combined with active endorsement of `uv run`-based commands means that if only the developer-advocate review is consulted, the `uv` accessibility problem is never addressed. Corporate environments, Docker containers with minimal tooling, and CI/CD pipelines that use `pip` would all hit this wall.
  - **Suggested resolution**: The user-advocate is correct that the quickstart needs a `pip` path. The developer-advocate's `uv run`-based recommendations should stand but with a note showing the `pip`/`python -m` equivalents. The quickstart should show both installation paths (as `index.md` already does) and then use `conversus` directly (which works after `pip install -e .`) rather than `uv run conversus`.

### Tensions

- **Scope of "developer" vs. "user" documentation**
  - user-advocate explicitly states that the developer guide pages (architecture, building-plugins, building-domains) had "no issues found from user perspective" (Referenced Documentation). developer-advocate's heaviest criticism targets exactly those pages -- the domain guide's missing end-to-end tutorial, the plugin wiring gap, the error handling silence, and the missing testing guidance. This is not a contradiction but a tension: user-advocate's review gives a clean bill of health to pages that developer-advocate considers significantly deficient. If a prioritization exercise weights user-advocate findings higher because they are P1-rated, the developer guide deficiencies could be deprioritized despite being equally blocking for their audience.

- **Config reference: completeness vs. approachability**
  - user-advocate wants a "starter template" at the top of the config reference (Recommendation #9, P3) to reduce cognitive load for first-time config authors. developer-advocate wants the `plugins:` key added to the config reference (Recommendation #3, P1) because it is the single source of truth and omitting a top-level key is a factual gap. Both are valid, but applying the starter template without including `plugins:` would reinforce the idea that plugins are an afterthought. Applying `plugins:` without the starter template keeps the page intimidating. These should be coordinated: the starter template goes at the top (simple, no plugins), then the full schema (including `plugins:`), then common configs.

- **Guided workflow: explanation depth**
  - user-advocate wants a 2-3 sentence explanation of slash commands before the guided workflow (Recommendation #2, P1) and a "Before you start" note on the complete example (Recommendation #8, P3). developer-advocate does not address the guided workflow at all -- it falls outside the developer-advocate's scope. The tension is that both reviews' recommendations would modify the same page (`guided-workflow.md`) but from different angles. user-advocate's edits are about user comprehension; any future developer-advocate edits (e.g., linking the guided workflow to the SDK for programmatic alternatives) would need to coordinate with the new prerequisite section.

- **Troubleshooting: where to put it**
  - user-advocate wants a troubleshooting section in the quickstart (Recommendation #5, P2). developer-advocate wants error handling guidance in the plugin and domain guides (Recommendation #5, P2). Neither addresses a centralized troubleshooting page. If both are implemented independently, troubleshooting content will be scattered across three pages with no cross-linking. A lightweight coordination step -- adding a "Troubleshooting" entry to the docs nav that links to page-specific sections -- would prevent fragmentation.

- **"Next steps" navigation vs. developer onboarding path**
  - user-advocate wants a "Next steps" section at the end of the quickstart pointing to modes, guided workflow, SDK, and MCP setup (Recommendation #7, P2). developer-advocate's recommendations imply a different next-steps path for developers: quickstart -> SDK -> building-plugins -> building-domains. If the quickstart's "Next steps" only lists user-advocate's suggestions, the developer path (which is the more complex and more documentation-deficient one) remains invisible from the primary entry point.

### Safe Agreements

- **Mock provider as the correct default onboarding pattern**
  - Both reviews cite the same quickstart lines (L19-22) and agree that `--provider mock` removing the credential barrier is the single most important onboarding decision. user-advocate calls it "removes the single biggest friction point in LLM tool onboarding" (Alignment, first item). developer-advocate calls it "the correct onboarding pattern" (Alignment, first item). No coordination needed -- both endorse the status quo.

- **Cost estimation transparency is well-documented**
  - Both reviews cite the CLI `validate` command (L63-91) and the SDK `cost_estimate` property as well-documented and critical for user trust. user-advocate highlights the worked example (3 agents = 16 launches). developer-advocate highlights the per-phase breakdown. The documentation succeeds here from both perspectives.

- **API reference stubs need prose content**
  - Both reviews independently identify the mkdocstrings-only API reference pages as a problem. user-advocate frames it as "blank pages on GitHub" (Missed Opportunities; Recommendation #6). developer-advocate frames it as "no narrative context, no usage examples, and no explanation of relationships" (Missed Opportunities; Recommendation #4). The diagnosis converges; the resolution depth differs (addressed in Dangerous Contradictions above), but the agreement that these pages need work is unambiguous.

- **The modes documentation is a highlight**
  - user-advocate praises the imperative mode descriptions and "When to use" heuristics as allowing a user to "scan all 8 modes in under 2 minutes" (Alignment, second item). developer-advocate does not flag any issues with the modes page. Both reviews treat `modes.md` as one of the strongest pages in the documentation suite.
