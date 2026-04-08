# Cross-Review of code-verifier's Review

**Cross-reviewer:** developer-advocate
**Reviewing:** code-verifier's Phase 1 review of Conversus Documentation Suite (Spec 031)

---

## Dangerous Contradictions

- **Scaffolds endpoint: fix the code vs. fix the docs**
  - **code-verifier claims**: The `/scaffolds` API endpoint only globs `*.json` files, so either the code must be updated to also glob `.yml`/`.yaml`, or the documentation should note that scaffolds must be JSON for API listing (Actionable Recommendations, item 2; Off-Base Assumptions, scaffolds endpoint). code-verifier frames both options as equally valid and prioritizes this as P1.
  - **developer-advocate claims**: The building-domains guide shows scaffold examples exclusively in YAML format (`building-domains.md`, L74-91, L225-236), and the `DomainPlugin` ABC documentation states `scaffold_dir` contains "scaffold YAML/JSON files" (`building-domains.md`, L31). The entire developer-facing contract is YAML-first. My review does not flag this endpoint bug because I evaluated from the documentation surface, but the YAML-first framing is what a developer will follow.
  - **Why this is dangerous**: If the resolution is "update docs to say scaffolds must be JSON," it contradicts every example in the developer guide and forces developers to rewrite their scaffolds. If the resolution is "update code to accept YAML," the documentation is already correct. These two resolutions are mutually exclusive, and code-verifier lists both without a recommendation for which direction to take. A developer following the current docs will create YAML scaffolds (as every example shows), hit the endpoint bug, and blame the docs.
  - **Suggested resolution**: Fix the code to glob `*.yml`, `*.yaml`, and `*.json` in the `/scaffolds` endpoint. The documentation is correct; the code is the outlier. `load_scaffold()` already handles both formats, so the endpoint is the only gap.

- **Provider precedence: "confusing inconsistency" vs. documented behavior**
  - **code-verifier claims**: The config `provider` field defaults to `"anthropic"` in code but CLI `--provider` defaults to `"mock"`, and the docs do not make this precedence clear (Off-Base Assumptions, config provider default; Actionable Recommendations, item 3). code-verifier calls this "confusing" and says "Users set `provider: anthropic` in their config, run without `--provider`, and get mock responses with no warning."
  - **developer-advocate claims**: The CLI docs (`cli.md`, L27) correctly show `--provider` defaulting to `mock`, and `config-reference.md` L58-60 states `provider: anthropic` with the note "CLI --provider flag overrides this." My review does not flag provider precedence as an issue because the config reference already documents the override relationship.
  - **Why this is dangerous**: code-verifier's recommendation to add explicit precedence documentation is reasonable on its own, but the framing overstates the severity. The config reference already says "CLI --provider flag overrides this" at L60. If both positions are implemented naively, one team adds a redundant explanation to `cli.md` while another team assumes the config reference note is sufficient, creating drift between two pages that say the same thing in different ways.
  - **Suggested resolution**: Accept code-verifier's recommendation to clarify precedence in `cli.md`, but frame it as a cross-reference ("See [Config Reference](config-reference.md) for how config-file `provider` interacts with `--provider`") rather than duplicating the precedence rule in two places.

- **`decide` mode restriction: documentation gap vs. code limitation**
  - **code-verifier claims**: The `decide` command accepts only 4 modes via `click.Choice`, and the docs should either explicitly state this restriction or the code should be updated to accept all 8 (Actionable Recommendations, item 1). code-verifier calls this P1.
  - **developer-advocate claims**: My review does not flag the 4-mode restriction on `decide` as an issue, because `cli.md` L57 already lists exactly 4 modes for the `decide` command and `modes.md` describes all 8 modes as a system capability, not a `decide` capability. A developer reading the CLI reference would see the correct 4 choices.
  - **Why this is dangerous**: code-verifier is correct that the juxtaposition between `modes.md` (8 modes) and `cli.md` (4 modes for `decide`) creates a reasonable expectation mismatch. However, my position that the docs are already technically correct means we disagree on whether this is a documentation error or a usability gap. If treated as a P1 doc fix, it may lead to unnecessary code changes (expanding Click to 8 modes) when the real solution is a one-line explanatory note.
  - **Suggested resolution**: Add a brief note to `cli.md` under the `decide` command: "For the remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design), use `conversus run` with a config file." This is the documentation-only fix code-verifier proposes as option A, and it does not require code changes.

### Tensions

- **API reference stubs: narrative docs vs. autodoc directives**
  - **code-verifier** notes the API reference pages use mkdocstrings directives and flags `DomainStore` as missing from `api/domains/base.md` (Missed Opportunities, DomainStore protocol), recommending adding it as a P2 fix.
  - **developer-advocate** flags all three API reference pages as "autodoc stubs" that are "effectively empty" when viewed outside a built mkdocs site (Missed Opportunities, API reference pages are autodoc stubs; Actionable Recommendations, item 4), recommending narrative sections before each directive.
  - **Tension**: We agree the pages are insufficient but disagree on the remedy's scope. code-verifier wants to add missing members to the existing autodoc approach. developer-advocate wants to replace the approach with narrative documentation. If both are implemented independently, you get narrative wrappers around expanded autodoc directives, which could be verbose. The tension is whether autodoc is a valid documentation strategy at all for this project, given that the docs may be read on GitHub without `mkdocs serve`.

- **`determine_verdict` example: incomplete vs. misleading**
  - **code-verifier** notes the example "ignores `dimensions` and `variables` parameters" and recommends updating it to "demonstrate using at least one of the ignored parameters" (Actionable Recommendations, item 8, P3).
  - **developer-advocate** flags the same example as showing "logic that is *not* the default" because the base class's default behavior checks per-dimension thresholds rather than `minimum_overall` (Off-Base Assumptions, domain guide `determine_verdict` signature mismatch; Actionable Recommendations, item 7, P2).
  - **Tension**: code-verifier treats this as an incomplete example (show more parameters); developer-advocate treats it as a misleading example (it teaches the wrong mental model of the default). The fix for "incomplete" is to add parameter usage. The fix for "misleading" is to separate default-behavior documentation from override-example documentation. These are different fixes that could conflict if applied independently.

- **`classify` re-export: consistency fix vs. dual-namespace documentation**
  - **code-verifier** recommends adding `classify` to `engine/__init__.py` exports so both import patterns work (Actionable Recommendations, item 4, P2).
  - **developer-advocate** recommends documenting the dual package structure (`engine.*` vs `conversus.*`) explicitly in the SDK page (Actionable Recommendations, item 9, P3), treating the two namespaces as an architectural fact to explain rather than an inconsistency to fix.
  - **Tension**: code-verifier's fix is a one-line code change. developer-advocate's fix is a documentation addition. They are not contradictory, but if only the code change is made, the broader confusion about dual namespaces remains. If only the documentation is added, the import inconsistency remains. Both should be applied.

- **Missing plugin configuration in config-reference.md**
  - **code-verifier** does not flag the absence of the `plugins:` key from `config-reference.md`, though it documents plugin config syntax in the building-plugins alignment section.
  - **developer-advocate** flags this as a P1 gap (Actionable Recommendations, item 3), arguing that the config reference is the "single source of truth for the YAML schema" and omitting `plugins:` means developers will not discover plugins exist when reading it.
  - **Tension**: code-verifier's silence on this issue implies it is not a verification concern (the plugin config syntax is documented in the plugin guide). developer-advocate's P1 rating reflects a developer-experience concern (discoverability). If only code-verifier's recommendations are implemented, the config reference remains incomplete as a schema document.

### Safe Agreements

- **8 modes match `VALID_MODES` exactly**
  - code-verifier confirms the 8 modes in `modes.md` and `config-reference.md` match `VALID_MODES` in `conversus/schemas/modes.py` L9-18 (Alignment, first item). developer-advocate confirms all 8 mode descriptions are complete with use-case guidance and YAML examples (Alignment, first item implicitly via modes.md coverage). The mode taxonomy is accurate and well-documented.

- **Plugin ABC and hook lifecycle are faithfully documented**
  - code-verifier verifies the `Plugin` class attributes, `execute()` signature, `__init_subclass__` validation, and `HookPoint` enum all match source code (Alignment, items 3-4). developer-advocate confirms the plugin guide is complete enough that "a developer could build a plugin from the guide alone" (Alignment, produces/consumes plugin data flow). The building-plugins guide is the strongest developer-facing document in the suite.

- **Cost formula is accurate and well-documented**
  - code-verifier verifies the cost formula matches `engine/cost.py` L70-103 exactly (Alignment, cost formula). developer-advocate confirms both CLI and SDK cost estimation are documented and that pre-execution cost visibility is "critical for developer trust" (Alignment, cost estimation before execution). Both reviews agree the cost documentation is a strength.

- **`estimate_cost_usd()` should be documented**
  - code-verifier identifies the undocumented `estimate_cost_usd()` function in `engine/cost.py` L106-158 as a missed opportunity (Missed Opportunities, no documentation of `estimate_cost_usd()`). developer-advocate does not flag this function specifically but notes the cost estimation is only documented in launch-count terms (`sdk.md`, L67-73), not USD terms. Both reviews converge on the position that USD cost estimation is a valuable undocumented capability that production users need.
