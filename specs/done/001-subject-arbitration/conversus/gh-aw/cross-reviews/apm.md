# gh-aw Cross-Review of APM's Review

**Cross-Reviewer**: gh-aw (GitHub Agentic Workflows)
**Reviewing**: APM's review of Subject Arbitration (Phase 6)
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: Grounding document expansion weakens the integrity mechanism we both praise

APM recommends supporting `grounding` as a list of paths (P2-4) and argues the single-path constraint is too narrow. gh-aw separately recommended expanding FR-019 citation scope to include `arbiter.docs`. Both recommendations sound reasonable in isolation, but together they dissolve the spec's core integrity mechanism. The grounding document works precisely because it is singular -- it forces the arbiter to derive all rulings from one declared framework, making evasion hard. If `grounding` becomes a list, the arbiter can cherry-pick whichever document supports a predetermined conclusion. If `docs` also become citable as grounding, the distinction between "decision framework" and "reference material" collapses entirely. The spec's design is deliberate: one framework, one citation target, supplementary docs for context only. APM's recommendation and my own recommendation (P2-7) both erode this and should be withdrawn or at minimum guarded with a rule that the primary grounding document must be cited in every ruling, with supplementary docs cited only as corroboration.

### DC-2: Removing FR-004 without analyzing non-cooperative game dynamics is reckless

APM's P1-1 recommends removing the cooperative-only restriction and enabling all four modes at launch, arguing the templates are "already written and tested." gh-aw flagged the same template/constraint mismatch (P2-4) but recommended either removing the templates or relaxing the constraint -- not unconditionally enabling all modes. The critical issue APM's recommendation ignores: the spec's Constraints section explicitly states "Prisoner's Dilemma and Red-Blue extensions change game dynamics fundamentally and need separate analysis." That is not an arbitrary limitation. In Prisoner's Dilemma mode, Phase 5 already produces binding trust-scored responsibility maps. Adding a Phase 6 arbiter that can override those trust scores creates a mechanism for the subject to rehabilitate its reputation regardless of the game's revealed preferences -- it defeats the entire purpose of the PD mechanism. In Red-Blue mode, the adversarial dynamic means the "subject" may be the entity one team is trying to attack. Giving it binding arbitration authority over attack findings is a security anti-pattern. Templates existing is not the same as templates being safe to deploy. APM's recommendation to "enable all modes" without the separate game-dynamics analysis the spec calls for is the most dangerous recommendation in either review.

### DC-3: Schema versioning solves a problem that does not yet exist and creates one that does

APM recommends adding `schema: 1` or `version: 2` to `conversus.yml` (P2-5), citing APM's own `apm.yml` versioning as precedent. This contradicts the spec's backward-compatibility design (FR-005) which achieves compatibility through additive optional fields, not version negotiation. Introducing a version field means every existing `conversus.yml` is now implicitly "version 0" or "version 1," and future tooling must handle version detection, migration, and validation for each version. The conversus schema has exactly one extension point so far (`arbiter`), which is fully optional. APM's own experience with `apm.yml` versioning is relevant -- but the lesson is that versioning is worth its cost only when breaking changes are unavoidable. The `arbiter` field is not a breaking change. Adding versioning now creates tooling complexity for a migration that is not needed, and sets a precedent where every future optional field bumps the version number. The right time to add versioning is when an actual breaking change forces it.

---

## Tensions

### T-1: Structured metadata -- sidecar file vs. frontmatter vs. extraction pipeline

APM recommends a `resolution.summary.yml` sidecar (P3-9) alongside the markdown resolution. gh-aw recommends a `metadata.yml` in the arbitration output directory (P2-6). Both identify the same gap (no machine-readable output), but propose different artifacts with different scopes. APM's sidecar contains ruling-level data (dispute labels, citations, confidence). gh-aw's metadata contains run-level data (dispute counts, trigger type, arbiter name, timestamp). These are complementary, not conflicting, but shipping both creates two non-markdown files that must be maintained, versioned, and documented. The tension is whether structured output should live in one file or two, and whether the engine produces it or a post-processing step extracts it from the markdown.

### T-2: Trigger robustness -- structured signal vs. locked contract

Both reviews identify the fragile heading-based trigger parsing as a problem. APM recommends HTML comment markers (`<!-- CONVERSUS:DISPUTES_BEGIN -->`) in the synthesis template (P1-2). gh-aw recommends either an HTML comment, a sidecar metadata file, or at minimum a locked-contract comment in the template (P1-2). The tension: APM's marker approach embeds machine-readable signals inside human-readable prose, which works but makes the synthesis template a dual-purpose document. gh-aw's sidecar approach separates concerns cleanly but requires Phase 5 to produce two outputs instead of one, complicating the execution model. The locked-contract comment (gh-aw's option c) is the cheapest but weakest -- it is a convention, not an enforcement mechanism. Neither review fully addresses who is responsible for maintaining the contract: the template author, the Phase 5 agent, or the engine.

### T-3: Dry-run mode vs. hook-based post-arbitration validation

gh-aw recommends a `dry_run` / `staged: true` mode for previewing arbitration (P2-5). APM recommends `post-arbitration` hooks that can run validation scripts before output is accepted (P2-7). Both address the same underlying concern -- how do you trust a new Phase 6 before committing to its results? -- but from opposite directions. Dry-run mode says "run it but label the output as non-binding." Hooks say "run it for real but let a script reject the output." The tension: dry-run is safer for adoption (no binding output until explicitly promoted) but creates a "preview that never graduates" risk. Hooks are more flexible (arbitrary validation logic) but require the operator to write and maintain scripts. Both have merit; the question is which belongs in the spec and which is a future extension.

### T-4: Arbiter reuse across conversus runs -- packaging vs. runtime concern

APM recommends an arbiter extraction/reuse pattern (P3-8) where arbiter configs can be stored as standalone files and referenced across multiple `conversus.yml` files, potentially as APM-packaged artifacts. gh-aw's review does not address reuse at all -- from the CI/orchestration perspective, each conversus run is an independent pipeline invocation with its own config. The tension: APM sees the arbiter as a reusable artifact (like a package), while gh-aw treats it as a per-run configuration (like workflow inputs). In a monorepo with multiple conversus runs over different specs, APM's pattern avoids duplication. In a CI pipeline where reproducibility matters, gh-aw's implicit model (inline config, pinned to the run) avoids the indirection and version-skew risks that shared references introduce.

### T-5: The observation loophole -- gap or feature?

APM identifies a contradiction between FR-015.5 ("MUST NOT introduce new recommendations") and the template's instruction to "note it as an observation in the Confidence Assessment" (Off-Base #3, P1-3). APM frames this as a gap that should be reconciled by explicitly carving out an observation exception. gh-aw's review does not flag this tension. On reflection, the tension is real but the resolution is not obvious. If observations are formally exempted, a clever arbiter can launder new recommendations as "observations" and circumvent the scope constraint entirely. If observations are prohibited, the arbiter loses the ability to flag genuine insights that fall outside existing dispute boundaries. The spec's current ambiguity may be intentional -- the template softens the hard rule to allow professional judgment while the spec's formal requirements maintain the bright-line prohibition for accountability.

---

## Safe Agreements

### SA-1: Backward compatibility is correctly designed

Both reviews agree that the `arbiter` field's fully-optional nature (FR-005) and zero-behavioral-change guarantee when omitted (SC-004) is the right approach. APM calls it "the correct approach -- additive features should never break existing configurations." gh-aw calls it the "same additive-only principle gh-aw uses for new frontmatter fields." No disagreement. The spec got this right.

### SA-2: Template-per-mode extensibility is architecturally sound

Both reviews agree that placing `arbitration.md` in `templates/{mode}/` and using the same `{VARIABLE}` substitution system is the correct design. APM aligns it with convention-based file discovery in `.apm/` directories. gh-aw aligns it with the markdown + frontmatter compilation model. Both agree this preserves extensibility without code changes. The spec got this right.

### SA-3: The grounding document requirement is the key integrity mechanism

Both reviews identify the grounding-document-as-citation-source pattern as the strongest element of the spec. APM maps it to constitution injection in `apm compile`. gh-aw maps it to protected-files policy in safe-outputs. Both agree that requiring every ruling to cite a specific document is what makes interested-party arbitration legitimate rather than unconstrained. Where the reviews diverge (see DC-1) is on whether to weaken this mechanism by expanding what counts as grounding -- but both affirm the principle itself.

### SA-4: The template/constraint mismatch for non-cooperative modes must be resolved

Both reviews flag the contradiction between FR-004 (cooperative-only) and the existence of arbitration templates for all four modes. APM and gh-aw agree this is a consistency defect that creates dead code and user confusion. They disagree on the resolution (APM says enable all modes; gh-aw says pick one direction), but both agree the current state is unacceptable.
