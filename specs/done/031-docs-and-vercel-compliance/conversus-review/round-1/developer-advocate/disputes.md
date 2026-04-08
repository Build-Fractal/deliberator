# Developer Advocate — Final Disputes (Phase 4)

---

### Remaining Disputes

- **Dispute: End-to-end domain tutorial is P1, not deferrable**
  - **My claim**: The building-domains guide is the single largest documentation gap for the developer audience. It stops at class definition and never demonstrates the extract-score-persist-gate-serve lifecycle. A developer cannot ship a domain plugin from the current docs alone. This is P1 for the extensibility track and should not be sequenced behind onboarding fixes.
  - **Opposing position(s)**: user-advocate argues that onboarding fixes gate the audience for extensibility docs and should be sequenced first ("the onboarding path gates the audience for everything else" -- user-advocate revision, Position Summary). By implication, the domain tutorial can wait.
  - **Why I will not concede**: The two tracks serve different audiences with different entry points. A developer integrating conversus into a CI pipeline or a FastAPI service will never touch the quickstart -- they arrive via the SDK page or the building-domains guide directly. Sequencing the domain tutorial behind quickstart prerequisites assumes a single linear funnel that does not exist for the developer persona.
  - **Counter-argument to their position**: user-advocate's own revision (Recommendation 7, modified) concedes that "Next steps" should have two tracks -- "Explore conversus" for users and "Build with conversus" for developers. If the developer track is visible from the quickstart exit point, the domain tutorial must exist at the other end of that link. A signpost to an empty room is worse than no signpost.
  - **Proposed resolution path**: Both tracks execute in parallel. Acknowledge that neither blocks the other. The domain tutorial and the quickstart prerequisites are independent work items that can be assigned to different contributors simultaneously.

- **Dispute: API reference pages need structural class listings, not just prose**
  - **My claim**: The API reference pages (especially `api/domains/base.md`) must include explicit class listings with one-line descriptions and relationship notes, not just a plain-English introductory sentence. The `domains/base.md` page currently has no member filter at all -- it renders the entire module undifferentiated. A developer scanning for `DomainStore` or `VariableExtractor` gets no navigational aid.
  - **Opposing position(s)**: user-advocate's revision (Recommendation 6, modified) adopts my layered approach but emphasizes the "one plain-English sentence" layer as the priority for newcomers. The risk is that implementation stops at the sentence and never adds the structural layer, leaving the pages only marginally more useful for developers.
  - **Why I will not concede**: A one-sentence summary of a module is documentation for the table of contents, not the API reference. The API reference exists to answer "what classes are in this module, what do they do, and how do they relate to each other." Without the structural listing, a developer still cannot use the page as a reference -- they must read the source code.
  - **Counter-argument to their position**: user-advocate's concern about intimidating new users is valid for the quickstart and config reference, but the API reference is not a new-user page. No newcomer navigates to `api/domains/base.md` before reading the building-domains guide. The audience for this page has already committed to building a domain; serving them a single sentence is inadequate.
  - **Proposed resolution path**: Implement the full layered approach as agreed in revision: (1) one-sentence summary, (2) key class listing with relationships, (3) cross-link to developer guide. Treat all three layers as a single atomic deliverable, not three separate tasks that can be partially shipped.

- **Dispute: Plugin wiring documentation belongs in the building-plugins guide, not just config-reference**
  - **My claim**: The building-plugins guide must explain how to make a plugin importable -- that `package` is a Python dotted path, the module must be on `sys.path` (or installed via `pip install -e .`), and what happens when import fails (warning logged, plugin skipped). This is the developer's primary reference for plugin authorship.
  - **Opposing position(s)**: code-verifier's revision (New Recommendation B) and user-advocate's revision (New Recommendation B) both focus on adding the `plugins:` key to config-reference.md. While correct, this addresses config schema completeness, not the developer's operational question of "how do I make my plugin loadable."
  - **Why I will not concede**: Config-reference.md documents *what* the YAML schema accepts. The building-plugins guide documents *how* to author a plugin. The wiring question ("how does `package: my_plugins.scorer` become a running plugin?") is a *how* question. A developer who reads the config reference learns the field names; a developer who reads the building-plugins guide learns the full authorship lifecycle. The wiring gap is in the lifecycle documentation, not the schema documentation.
  - **Counter-argument to their position**: The building-plugins guide already has a "Dynamic loading" section (L162-170) that partially covers this, but it describes the engine's internal behavior (`importlib.import_module`) rather than the developer's setup steps. The developer needs: (1) make your module importable (`pip install -e .` or add to `PYTHONPATH`), (2) set `package` to the dotted path, (3) know the failure mode (warning + skip). Items 1 and 3 are missing from both the building-plugins guide and the config reference.
  - **Proposed resolution path**: Add the developer-facing wiring steps to the building-plugins guide's "Dynamic loading" section. Also add `plugins:` to config-reference.md as both other agents recommend. The two changes are complementary, not alternative.

### Convergence

- **Converged: `decide` command 4-mode restriction needs a clarifying note in cli.md**
  - **Shared position**: Add a one-line note under the `decide` command in cli.md: "For the remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design), use `conversus run` with a config file. See [Deliberation Modes](modes.md) for all 8."
  - **Agreeing agents**: code-verifier (Recommendation 1, surviving), user-advocate (Recommendation 10, modified), developer-advocate (New Recommendation C)
  - **Strength**: Unanimous
  - **Path to convergence**: code-verifier identified the Click constraint factually. user-advocate's original recommendation to list all 8 modes was retracted after seeing the code evidence. All three agents converged on the same documentation-only fix: keep cli.md accurate (4 modes), add a cross-link to modes.md (all 8).

- **Converged: Scaffolds endpoint must glob YAML files, not just JSON**
  - **Shared position**: Fix `api.py` L208 to glob `("*.yml", "*.yaml", "*.json")`. The documentation is correct (YAML-first); the code is the outlier. `load_scaffold()` already handles both formats.
  - **Agreeing agents**: code-verifier (Recommendation 2, modified), developer-advocate (New Recommendation A)
  - **Strength**: Bilateral (user-advocate did not engage with this finding)
  - **Path to convergence**: code-verifier originally presented "fix the code" and "fix the docs" as equal options. developer-advocate's cross-review argued the documentation is correct because every scaffold example uses YAML. code-verifier accepted this in revision and modified the recommendation to code-fix-only.

- **Converged: `plugins:` key must be added to config-reference.md**
  - **Shared position**: Add a `plugins:` section to config-reference.md documenting the `name`, `package`, and `config` sub-keys, with a note that plugins are optional and the section should be clearly labeled as advanced/extensibility.
  - **Agreeing agents**: developer-advocate (Recommendation 3, modified), code-verifier (New Recommendation B), user-advocate (New Recommendation B)
  - **Strength**: Unanimous
  - **Path to convergence**: developer-advocate identified the gap in Phase 1. code-verifier verified the schema against `load_plugins()` code. user-advocate raised the concern about intimidating new users, which led to the "Advanced / Extensibility" subsection placement that all agents accept.

- **Converged: `determine_verdict` example must be split into default behavior and custom override**
  - **Shared position**: Add a "Default behavior" paragraph explaining the base class logic (hard blocks then per-dimension thresholds), then relabel the existing example as "Customizing verdict logic" and enhance it to show `dimensions` and `variables` parameters.
  - **Agreeing agents**: developer-advocate (Recommendation 7, modified), code-verifier (Recommendation 8, modified)
  - **Strength**: Bilateral (user-advocate did not engage with this finding at the structural level)
  - **Path to convergence**: developer-advocate identified that the example teaches logic different from the base class default. code-verifier identified that the example omits available parameters. Both converged on a structural fix (split into two subsections) that addresses both concerns.

- **Converged: Provider precedence needs a note in cli.md**
  - **Shared position**: Add a brief note under the `run` command in cli.md stating that `--provider` defaults to `mock` and overrides the config file's `provider` field. Cross-reference config-reference.md rather than duplicating the full precedence rule.
  - **Agreeing agents**: code-verifier (Recommendation 3, modified), user-advocate (New Recommendation A), developer-advocate (New Recommendation B)
  - **Strength**: Unanimous
  - **Path to convergence**: code-verifier identified the mismatch between CLI default (`mock`) and config default (`anthropic`). developer-advocate's cross-review noted that config-reference.md L60 already documents the override. All three agents converged on a targeted one-line fix in cli.md with a cross-reference.

### Final Position Statement

**Non-Negotiables:**

1. **End-to-end domain tutorial must exist and must be treated as P1 for the developer track.** The building-domains guide currently stops at class definition. A developer cannot build, test, or deploy a domain plugin from the existing documentation. This is the largest gap in the developer-facing docs and it is independent of onboarding fixes.

2. **API reference pages must include structural class listings, not just prose summaries.** The `api/domains/base.md` page has no member filter and renders the entire module undifferentiated. The agreed layered approach (sentence + class listing + cross-link) must be implemented as a single atomic deliverable.

3. **Plugin wiring must be documented in the building-plugins guide, not only in config-reference.md.** The developer needs to know: make the module importable, set `package` to the dotted path, and understand the failure mode (warning + skip). The "Dynamic loading" section already exists but describes engine internals rather than developer setup steps.

**Flexibility:**

1. **Sequencing of onboarding vs. extensibility tracks.** I accept that both tracks run in parallel and neither blocks the other. I will not insist that extensibility work starts first, only that it is not deferred behind onboarding.

2. **SDK async-vs-sync presentation.** I accept user-advocate's modified position: keep async as the canonical form, add a prominent note about `asyncio.run()`, and use tabbed code blocks if the docs framework supports it. My original position that sync should be shown first was about the default-visible tab, not about demoting async.

3. **Quickstart length and troubleshooting placement.** I accept that the quickstart should stay lean and troubleshooting should live on a separate page. The 2-3 line prerequisites callout proposed by user-advocate is sufficient for the quickstart itself.
