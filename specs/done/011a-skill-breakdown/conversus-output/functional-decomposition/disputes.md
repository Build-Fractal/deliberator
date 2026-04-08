# Functional Decomposition — Disputes (Phase 4)

## Remaining Disputes

### Dispute 1: Run engine placement — reference file versus SKILL.md core

**My claim:** The run engine core should remain in SKILL.md. Extracting it to `references/handler-run.md` creates a two-hop loading dependency (dispatch → handler-run → subsystem) that is fragile. Every execution path requiring the engine — including `/conversus converge` and `/conversus gate` — must either follow a two-hop chain or find the engine missing at execution time. This is not a theoretical risk: the agentskills best practices warn explicitly that "the agent may not recognize the trigger" for content in reference files, and the run engine is not a conditional subsystem — it is the execution substrate for the majority of conversus invocations.

**Opposing position:** integration-specialist and agentskills-specialist both revised toward extracting the engine to `references/handler-run.md`. integration-specialist argues that internal cohesion can be preserved in a reference file just as well as in root, and that the root SKILL.md need only carry a phase-level summary (~300-350 lines). agentskills-specialist initially proposed this, then reversed — but integration-specialist maintained it and built the revised architecture around a ~300-350 line root with a ~450-550 line `handler-run.md`. apm-specialist did not take a position on engine placement after conceding the primary sub-skill strategy.

**Why I will not concede:** The extraction-to-reference-file position assumes that the agent reliably follows a dispatch-table reference chain to `handler-run.md` and that, from there, it further loads subsystem files on condition. This is a two-hop chain with compounded failure modes. agentskills-specialist's own revision (Recommendation 1) reversed course and concluded the engine is "not extractable" precisely because converge and gate compose the engine rather than call it as a peer handler. I reached the same conclusion in my revision (Recommendation 7) by analyzing the cascade: if multi-round cannot cleanly extract (Recommendation 4), the retained engine core is ~625 lines, which is too large for a reference file that is always loaded by three different dispatch paths. The comparison point is not "root SKILL.md versus handler-run.md as storage locations" — it is whether the agent at `/conversus converge` can safely execute without the engine in its always-loaded context. If the engine is missing from SKILL.md and the agent fails to follow the two-hop chain, it attempts multi-phase orchestration with a one-paragraph summary, which is a silent degradation failure.

**Counter-argument I must acknowledge:** integration-specialist's revised position is architecturally cleaner than my formulation on one dimension: it produces a smaller root SKILL.md (~300-350 lines vs. my ~700 lines), which benefits all non-engine subcommand invocations (`/conversus define`, `/conversus interests`, `/conversus mode`). My position penalizes every invocation to protect the engine invocations. integration-specialist correctly identifies this asymmetry.

**Proposed resolution path:** Empirical validation gates (New Recommendation B in my revision) should settle this. Implement the gate handler extraction first (Recommendation 1 — universally agreed). Then, for the second phase, test two configurations side-by-side: (a) engine in SKILL.md with guided handlers in references, and (b) engine in `references/handler-run.md` with a phase-summary in SKILL.md. Execute `/conversus converge` in both configurations and compare execution fidelity. The configuration where `/conversus converge` reliably produces correct multi-phase output is correct. This is an empirical question, not an architectural one, and the staged decomposition (New Rec B) provides the validation mechanism. I accept that the resolution may favor integration-specialist's architecture if the chain-loading works reliably in practice. I do not accept the extraction as a premise before that validation.

---

### Dispute 2: Naming convention — two-tier versus no-prefix for reference files

**My claim:** Reference files should use type-prefixed naming: `handler-{name}.md` for subcommand handlers, `subsystem-{name}.md` for shared subsystems. This convention comes from integration-specialist (Recommendation 9) and I adopted it in New Recommendation C precisely because at 9+ reference files, the type prefix makes the dependency graph legible from a directory listing without requiring agents or contributors to read each file.

**Opposing position:** agentskills-specialist explicitly rejects the naming prefix approach (Recommendation 3, unchanged). The agentskills specification does not define file-type prefixes for references. agentskills-specialist argues that `dispute-parsing.md` is self-explanatory and the load trigger in SKILL.md provides all context needed about the file's role. Adding a taxonomy (`handler-`, `subsystem-`) "imposes classification overhead that may not scale."

**Why I will not concede:** The classification overhead argument fails at the file-count agentskills-specialist's own revised layout targets. The revised directory listing includes 11 reference files: 6 handler files, 3 subsystem files (`dispute-parsing.md`, `template-variables.md`, `validation-rules.md`), 1 multi-round file, 1 operational-notes file, plus 5 existing agentskills reference files — totaling 16 files in `references/`. At 16 files, a directory listing without prefixes is navigable only by someone who already knows the architecture. A contributor encountering this for the first time cannot distinguish handler files from subsystem files from documentation files without reading each one. The two-tier prefix resolves this in O(1) from the filename alone. agentskills-specialist's concern about "classification overhead" applies when there are 3-4 files; it does not apply at 16.

**Counter-argument I must acknowledge:** agentskills-specialist is correct that the agentskills specification does not define file-type prefixes, and introducing conventions beyond what the specification mandates creates a custom layer that future skill authors must learn. If conversus reference files are ever used as a model for other skills, the prefix convention adds friction.

**Proposed resolution path:** This is a minor convention decision, but it should be decided before Phase 1 execution to avoid retroactive renames. I propose a compromise: adopt `handler-` prefix for subcommand handler files (this is the most important distinction — these are dispatch targets) and use plain names for subsystem files (`dispute-parsing.md`, `preset-resolution.md`). This gives the highest-value disambiguation (handlers versus everything else) without imposing a three-tier taxonomy. The handler prefix is intuitive and maps directly to the dispatch table structure. This is a bilateral resolution between my position and agentskills-specialist's position, conceding the `subsystem-` prefix while maintaining `handler-`.

---

### Dispute 3: Dispute-parsing extraction timing — immediate P2 versus conditional on handler extraction success

**My claim (as modified in revision):** Dispute-parsing extraction should be deferred to P2 and made conditional on the success of handler extractions (New Recommendation B, Phase 3). The subsystem is 28 lines. The token savings are negligible. Its four consumers span the run engine, converge, gate, and Phase 6 — meaning it is relevant to the majority of invocation paths. If agents struggle with reference loading in Phase 1-2 handler extractions, dispute-parsing should stay inline as a 28-line gotcha.

**Opposing position:** integration-specialist maintains extraction is correct (Recommendation 4, Sustained) and proposes a specific loading model: dispute-parsing loads from `references/handler-run.md` (now `subsystem-dispute-parsing.md` in their architecture), not from individual consumer handlers, to avoid redundant reads. agentskills-specialist likewise maintains extraction (Recommendation 3, Maintained). apm-specialist revised to support `references/dispute-parsing.md` as well. All three opponents treat the extraction as settled and dispute only the loading model.

**Why I will not concede — partially:** The loading model integration-specialist proposes (load from handler-run.md transitively) works if the run engine is in a reference file. But in my preferred architecture (engine in SKILL.md), the dispute-parsing content is already in context for converge and gate invocations because SKILL.md is always loaded. Extracting it to a separate file then requiring SKILL.md to contain a load trigger "if processing synthesis outputs, read references/dispute-parsing.md" partially defeats the extraction — the trigger is inline in the always-loaded body, and the agent loads an additional file for 28 lines. The case for extraction assumes the engine is out of SKILL.md.

**Counter-argument I must acknowledge:** The interface-contract argument for extraction remains real regardless of engine placement. Even if dispute-parsing stays at 28 lines in SKILL.md, its structural markers (`<!-- CONVERSUS:DISPUTES_BEGIN/END -->`) constitute a stable interface where changes are breaking changes affecting templates, the linter, and all output consumers. Making that interface physically addressable as a reference file is architecturally cleaner even if the token savings are negligible.

**Proposed resolution path:** This dispute is coupled to Dispute 1 (engine placement). If the empirical validation in Phase 2 shows that run engine extraction to a reference file is reliable, dispute-parsing extraction follows naturally with integration-specialist's loading model (load from handler-run.md). If engine extraction fails and the engine stays in SKILL.md, dispute-parsing should also stay inline, and the interface contract should be documented with a comment block in SKILL.md rather than a separate file. The resolution of Dispute 1 determines the resolution of Dispute 3.

---

### Dispute 4: Validation rules as a shared reference file versus co-location in handler files

**My claim (from Recommendation 6, modified):** Validation rules should not be a standalone reference file loaded via SKILL.md. Instead, validation logic should be embedded within each handler reference file (co-located with the handler it serves), with a brief canonical validation pattern (~10-15 lines) in the run engine core. Each handler says "Apply the canonical validation pattern from SKILL.md core" rather than loading a separate file.

**Opposing position:** agentskills-specialist maintains a `references/validation-rules.md` for shared patterns appearing in three or more handlers (Recommendation 5, Revised), loaded from each handler reference file via inline trigger. The file scope is limited to genuinely shared patterns (agent name regex, heading validation, path existence checks, standard error message format) to justify the cross-reference overhead.

**Why I will not concede:** agentskills-specialist's scoping criterion ("patterns appearing in 3+ handlers") is reasonable in principle but creates a new classification problem: someone must determine at decomposition time which patterns meet the threshold and re-classify as the pattern set evolves. If a new validation pattern is added to two handlers, it does not qualify for the shared file — but if a third handler later adopts it, it retroactively qualifies. This creates maintenance classification work that my co-location approach avoids. Co-location means each handler reference file is fully self-contained: one file load gives the agent everything it needs, with no second load for validation patterns. The agentskills best practices explicitly endorse self-contained handler files as the decomposition goal.

**Counter-argument I must acknowledge:** agentskills-specialist's position avoids validation drift across handlers. If agent name regex changes and the rule is duplicated in six handler files, all six must be updated. A single `validation-rules.md` updates once. The synchronization benefit is real, and my canonical-pattern-in-SKILL.md approach requires SKILL.md to be updated when shared validation changes — which means SKILL.md continues to carry more content than the decomposition targets.

**Proposed resolution path:** Defer this decision until handler files are drafted in Phase 2 (per New Recommendation B). Count the actual shared patterns across the six handler drafts. If the count of genuinely shared patterns (appearing verbatim in 3+ handlers) is 3 or fewer, co-locate in each handler file with a comment noting the shared pattern. If the count is 4 or more, create `references/validation-rules.md` per agentskills-specialist's revised recommendation. The threshold decision is empirical and should not be made before the handler files exist.

---

## Convergence

### Convergence 1: Gate handler is the first extraction target

**Shared position:** The gate handler (~300 lines, zero-shared-state, no interactive prompts, self-contained config and output schema) is the highest-priority, lowest-risk extraction target. It should be extracted first to `references/handler-gate.md` and serve as both a meaningful improvement and an empirical test of the reference-loading mechanism.

**Agreeing agents:** All five agents. functional-decomposition (Recommendation 1, Surviving). integration-specialist (Recommendation 3, Sustained). apm-specialist (N1 — gate as sole candidate for APM sub-skill after reference extraction proves stable). agentskills-specialist (Recommendation 1, gate handler among six extracted). agents-md-specialist (New Recommendation B — reference extraction first, gate is the anchor).

**Strength:** Unanimous.

**Path to convergence:** Universal agreement from Phase 1. No reviewer challenged the extraction boundary, the naming, or the trigger mechanism. This is the implementation starting point regardless of how Disputes 1-4 resolve.

---

### Convergence 2: APM sub-skills are the wrong primary decomposition axis for conversus now

**Shared position:** APM sub-skill promotion solves a distribution problem (different consumers need different capabilities). Conversus has a context window problem (one consumer needs different details at different moments). The agentskills `references/` model — conditional file loading triggered by runtime state — directly addresses the actual problem. APM sub-skills may be appropriate for gate in the future after reference extraction proves stable, but should not drive the current decomposition.

**Agreeing agents:** All five agents. apm-specialist reversed its original position entirely (Recommendation 1, Revised). functional-decomposition (consistent throughout). integration-specialist (consistent throughout). agentskills-specialist (consistent throughout). agents-md-specialist implicitly (sequencing: reference extraction first).

**Strength:** Unanimous.

**Path to convergence:** apm-specialist's self-correction in Phase 3 (cross-review) was decisive. The key insight — install-time optimization (APM's domain) versus invocation-time optimization (agentskills' domain) — resolved the structural question cleanly.

---

### Convergence 3: Two-class load trigger model (Class A dispatch vs. Class B config-conditional)

**Shared position:** Load triggers divide into two classes with different risk profiles. Class A (dispatch-table triggers): fire at invocation time before execution, route to handler reference files, are safe and unambiguous. Class B (config-conditional triggers): fire mid-execution based on config inspection (presence of `preset:` field, `rounds > 1`), are riskier, require explicit fallback behavior ("If the file cannot be loaded, halt and report the error").

**Agreeing agents:** functional-decomposition (Recommendation 8, Modified — originated this classification). integration-specialist (N2 — adopted and reinforced). agentskills-specialist (Recommendation 9, Revised — adopted two-tier model). apm-specialist (N2 — explicit load triggers as critical success factor).

**Strength:** Majority (4 of 5; agents-md-specialist did not address this directly).

**Path to convergence:** functional-decomposition's Recommendation 8 modification identified the distinction; integration-specialist's N2 adopted it; agentskills-specialist's revised Recommendation 9 formalized it into a two-tier structure. The convergence happened organically across Phase 3 revisions without a direct challenge from any reviewer.

---

### Convergence 4: Staged decomposition with empirical validation gates

**Shared position:** The decomposition should not be executed as an all-or-nothing structural change. Extract the most self-contained handler first (gate), validate that reference loading works reliably in practice, then proceed to remaining handlers, then conditional subsystems. Each phase is gated on the previous phase's success.

**Agreeing agents:** functional-decomposition (New Recommendation B). agents-md-specialist (New Recommendation B — sequence reference extraction first). agentskills-specialist (implicitly — revised positions defer multi-round and subsystem decisions). integration-specialist (N4 antipattern placement framing implies phased implementation). apm-specialist (Recommendation 8 — defer until spec suite stabilizes).

**Strength:** Majority (4 of 5 explicitly; integration-specialist implicitly).

**Path to convergence:** agents-md-specialist's Phase 3 dangerous contradiction (DC-1) proposed staged extraction as a safeguard. functional-decomposition adopted it as New Recommendation B. The concern — that active spec development (specs 012-020 queued) creates restructuring drag if all-or-nothing extraction fails — is shared across reviewers.

---

### Convergence 5: AGENTS.md and SKILL.md serve different audiences and must not duplicate runtime contracts

**Shared position:** SKILL.md (and its reference files) is authoritative for runtime execution behavior. AGENTS.md files are authoritative for contribution workflow. Where content overlaps, AGENTS.md contains a pointer to the authoritative location ("See `references/subsystem-preset-resolution.md` for the full specification") and the linter command for compliance checking. It does not duplicate the runtime rules. The single-source-of-truth convention prevents the drift that inline rule restatement creates.

**Agreeing agents:** All five agents. agents-md-specialist (New Recommendation A, Recommendation 6 maintained). functional-decomposition (New Recommendation A — separate contribution content before decomposition). integration-specialist (N3 — AGENTS.md for contribution, reference files for runtime). agentskills-specialist (New Recommendation A — triage contribution content before extraction). apm-specialist (revision framing throughout).

**Strength:** Unanimous.

**Path to convergence:** agents-md-specialist's dangerous contradiction (DC-2, original review) identified the dual-ownership problem. All reviewers accepted the correction in Phase 3. The pointer-only AGENTS.md model was the natural resolution.

---

## Final Position Statement

### Non-Negotiables

**1. The run engine core must not be extracted until empirical validation demonstrates that chain-loading through two reference hops is reliable for converge and gate invocations.**

This is the load-bearing constraint in my position. I accept that integration-specialist's architecture is cleaner in the ideal case. I do not accept it as a safe default before validation. The failure mode — agent attempts multi-phase orchestration with a one-paragraph engine summary — is high-severity and silent. The validation gate (Phase 1: extract gate, test; Phase 2: if chain-loading works, extract engine) is the correct sequencing. I will not agree to engine extraction as a simultaneous step with handler extractions.

**2. Staged execution with empirical validation gates is not optional.**

New Recommendation B is not a process preference — it is a safety constraint for a specification system that has no automated rollback. If Phase 1 extraction fails (agent does not follow reference load triggers), every subsequent extraction compounds the failure. The staged approach with a validation gate after each phase is the minimum responsible process for a decomposition of this scope. I will not agree to all-at-once execution of Recommendations 1-5.

**3. The contribution-content triage (New Recommendation A) must precede all reference file extractions.**

Extracting handler content to reference files before tagging and separating contribution-oriented lines (antipattern check instructions, template naming conventions, linter invocation guidance) guarantees that contribution content is scattered across reference files, making the future AGENTS.md work harder to collect. The preparatory step is small (agents-md-specialist estimates 200-400 tokens), sequential, and should take under 30 minutes. It is not negotiable as a prerequisite.

### Flexibility

**1. Run engine placement is conditionally negotiable.**

If the Phase 1 empirical validation (gate extraction + converge invocation test) demonstrates that chain-loading is reliable, I will accept extracting the run engine to `references/handler-run.md` per integration-specialist's revised architecture. This is the highest-priority dispute, and I hold it as a non-negotiable only until the empirical gate is cleared.

**2. The naming convention for subsystem reference files is negotiable.**

I maintain `handler-` prefix for dispatch-target files. I will accept plain names for subsystem files (`dispute-parsing.md` instead of `subsystem-dispute-parsing.md`) as a bilateral compromise with agentskills-specialist. The handler/non-handler distinction is the operationally important one; the subsystem prefix is a navigability enhancement that is not worth a sustained dispute.

**3. Token budget targets are negotiable as acknowledged exceptions.**

I accept integration-specialist's and agentskills-specialist's framing: the 5,000-token guideline is a recommendation for typical skills, not a hard ceiling for orchestration engines. A SKILL.md that is 60% over the guideline but requires zero multi-hop chain reads for any invocation path is better than one that meets the guideline and silently degrades on converge or run. The token budget documentation should record an acknowledged exception for conversus, not claim compliance through an indefensible summary.
