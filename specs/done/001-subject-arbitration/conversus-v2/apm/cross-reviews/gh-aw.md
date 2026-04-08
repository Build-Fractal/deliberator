# APM Cross-Review of gh-aw's v2 Review

**Cross-reviewer**: APM (Agent Package Manager)
**Reviewing**: gh-aw v2 review of Subject Arbitration spec
**Date**: 2026-03-19

---

## Dangerous Contradictions

### 1. FR-022/FR-023 disambiguation would paper over a real ambiguity rather than resolve it

gh-aw's P1-1 recommendation asks for a single sentence in FR-022 clarifying that "malformed output" means agent-process failure, not output-content validation. APM agrees the ambiguity exists (gh-aw's Missed Opportunity #3 is well-diagnosed), but the proposed fix is dangerous. Drawing the line at "the process did not complete" versus "the process completed but produced incomplete content" creates a third category the spec still does not handle: the process completed, produced output, but the output is *structurally unintelligible* (e.g., raw YAML dump, a refusal message, or output in a language the engine cannot parse). This is neither a process failure (the agent ran to completion) nor an FR-023 validation failure (there are no section headings to validate against because the output is not prose). gh-aw's proposed disambiguation would route this case to FR-023 (file written with warning), preserving garbage as a deliverable. APM's position: the disambiguation needs three tiers, not two. Process failure (FR-022, no file). Structural unintelligibility (new, no file, diagnostic emitted). Incomplete-but-parseable prose (FR-023, file written with warning). Collapsing the first two into FR-022 or the last two into FR-023 creates a gap either way.

### 2. Directory-based template separation contradicts the packaging distribution model

gh-aw's Off-Base Assumption #1 maintains that `templates/_draft/` is simpler and more reliable than content-based draft markers, citing gh-aw's own compilation model where discoverability is location-based. This is correct within gh-aw's single-repo workflow model but dangerous for distributed template packages. In APM's distribution model, a conversus template package ships as a self-contained artifact with a declared file manifest. A `_draft/` directory requires the *consumer's* engine to understand a directory-naming convention that is not part of the conversus spec -- it is a gh-aw ecosystem convention. The content-based marker (`<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`) is self-describing: any engine can parse it without knowing the directory convention of the source repository. gh-aw is right that glob-based discovery will find files regardless of markers, but the solution is not to move files -- it is to make the engine's template loader filter by marker, which is a one-time implementation cost. Moving to directory separation would couple the spec to a layout convention that breaks when templates are flattened during packaging. APM agrees with gh-aw's P2-3 recommendation (add a normative FR for draft filtering) as the correct fix, but the underlying preference for directory separation is the wrong direction for the ecosystem.

### 3. The `{REMAINING_DISPUTES}` empty-extraction concern conflates two distinct failure modes

gh-aw's Missed Opportunity #2 describes a scenario where Phase 5 output contains markers with only whitespace between them and `trigger: always` causes Phase 6 to run with an empty `{REMAINING_DISPUTES}`. gh-aw then claims the endorsement template path and the dispute-resolution template path "appear to use the same template, creating ambiguity." This conflation is dangerous because it suggests the solution is template-level branching (gh-aw's Off-Base #2 proposes conditional template logic or a separate endorsement format). But the actual problem is simpler: the engine should emit a diagnostic when extraction produces empty content while the trigger evaluated to true. gh-aw correctly identifies this in P3-6, but the framing in Missed Opportunity #2 and Off-Base #2 pushes toward template complexity (conditional logic, separate output formats) that would make the template authoring contract significantly harder to satisfy. The endorsement path is not a template design problem -- it is a data-flow validation problem. Adding template conditionals for the no-disputes case would violate the spec's design principle that templates are static instruction sets, not programs.

### 4. Defining "dispute entry" as "any non-whitespace content" is underspecified in the wrong direction

gh-aw's P1-2 recommends that "any non-whitespace content between the markers constitutes at least one dispute entry." This is presented as simple and unambiguous, but it is dangerously loose. A stray HTML comment, a blank line rendered as `&nbsp;`, or a Phase 5 template artifact (e.g., a section divider or explanatory note placed between the markers) would all trigger Phase 6 dispatch despite no actual disputes existing. The trigger is the gate for an expensive LLM arbitration call. A false positive wastes resources and produces a spurious `resolution.md` that downstream consumers must then evaluate. APM's position: "dispute entry" should be defined as content matching the `**Dispute:**` pattern (consistent with the heading-based fallback) or, at minimum, as any line starting with a Markdown bold marker. "Non-whitespace" is too permissive for a trigger that controls agent dispatch.

---

## Tensions

### 1. Template authoring contract scope: gh-aw wants engine enforcement, APM wants author guidance

gh-aw's review praises the template authoring contract (Alignment #5) but then identifies gaps where the engine should enforce what the contract states (P2-3 for draft filtering, P2-4 for `docs` citation boundary in the template itself). APM's review also identifies a contract gap (per-file attribution per FR-026 not in the contract) but frames it as a documentation problem, not an engine enforcement problem. The tension: gh-aw consistently pushes enforcement toward the engine (validate markers, parse templates for compliance, emit diagnostics), while APM pushes enforcement toward the template authoring surface (make the contract complete so authors produce correct templates). Both are valid strategies, but they produce different implementation profiles. Engine enforcement is more reliable but couples the engine to template internals. Author-side enforcement is more portable but relies on discipline. The spec currently leans toward gh-aw's model (FR-023 validates output, Constraints section requires engine filtering), but the template authoring contract leans toward APM's model (invariants for authors, not engine validation rules). This hybrid should be acknowledged.

### 2. Structured output timing: gh-aw defers cleanly, APM wants forward-compatibility constraints now

gh-aw's P3-8 recommends moving the structured output schema to a standalone "Future Work" section -- a documentation reorganization. APM's Missed Opportunity #2 argues that the spec should constrain Binding Decisions entry structure *now* (e.g., `**Dispute:**`, `**Ruling:**` sub-headings) to ensure the deferred extraction mechanism has a reliable parsing target. gh-aw treats the structured output deferral as a clean boundary: v1 does prose, v2 does structured, no coupling needed. APM treats it as a forward-compatibility risk: if v1 prose is unstructured, v2 extraction becomes a fragile parsing problem. Both positions are defensible. The tension is about how much v1 should constrain itself for v2's benefit. gh-aw prioritizes v1 simplicity; APM prioritizes v2 viability.

### 3. Grounding document integrity: gh-aw trusts the stability assumption, APM wants verification

gh-aw's review does not flag the grounding document stability assumption as a concern. APM's Off-Base #1 argues that the stability assumption is aspirational without a hash-based verification mechanism. gh-aw's silence is consistent with its operational model: in CI pipelines, inputs are typically immutable (checked-out at a specific commit). APM's concern is consistent with its distribution model: in a multi-user packaging context, the grounding document might be a shared file that is edited concurrently. The tension is environmental: the spec does not specify the execution context, so both assumptions are valid.

### 4. Citation boundary enforceability: gh-aw wants template instructions, APM trusts FR-024 alone

gh-aw's P2-4 recommends adding a seventh instruction to FR-015 explicitly telling the arbiter to cite grounding as authority and docs only for context. APM's review notes FR-024 as correctly specified (Alignment #2) without recommending additional template instructions. The tension: gh-aw sees the template as the enforcement surface (the arbiter only follows template instructions, so the boundary must be in the template). APM sees the spec requirement as sufficient (FR-024 is normative, the engine validates output, the template inherits the constraint). This reflects a deeper disagreement about where normative requirements bind -- at the spec level (APM) or at the prompt level (gh-aw). For LLM-based agents, gh-aw's position is arguably more practical since the agent only sees its prompt, not the spec.

### 5. Endorsement path specification: gh-aw wants explicit handling, APM is silent

gh-aw's Off-Base #2 and P2-5 argue that the `trigger: always` + no disputes path needs explicit specification (either a separate output format, conditional template logic, or an acknowledgment that endorsement is implicit). APM's review does not flag this path. The tension is about spec completeness versus spec minimalism. gh-aw wants every dispatch path fully specified. APM accepts that some paths can be handled by the arbiter's interpretation of existing instructions. This reflects gh-aw's CI background (every branch must have a defined outcome) versus APM's agent background (agents can handle ambiguous instructions within a well-scoped context).

---

## Safe Agreements

### 1. FR-022 failure semantics are correctly specified and represent the strongest consensus point

Both reviews identify FR-022 as faithfully implementing the synthesis recommendation. gh-aw's Alignment #1 calls it "the cleanest consensus point." APM's Alignment #3 calls it "unanimous convergence." The Phase 5-as-terminal-state fallback, diagnostic warning emission, no partial writes, and Phase 1-5 record preservation are agreed by both agents as correctly specified. No amendments needed to the core failure path.

### 2. Structural HTML markers as primary trigger mechanism are correctly adopted

Both reviews confirm FR-011's dual-mechanism approach (markers primary, heading fallback) is the right design. gh-aw's Alignment #2 notes it "directly implements gh-aw's revised P1-2 position." APM's Alignment #1 notes it "directly implements APM's Dispute 3 position." The convergence is genuine -- both agents advocated for this independently and the spec adopted it from both directions. The only divergence is on the definition of "dispute entry" within the markers (see Dangerous Contradiction #4), not on the mechanism itself.

### 3. The `docs` vs. `grounding` citation-authority distinction is correctly formalized

Both reviews endorse FR-024 without reservation. gh-aw's Alignment is implicit (not flagged as a concern; the Missed Opportunity #5 is about *operational confusion*, not specification correctness). APM's Alignment #2 calls the phrasing "precisely calibrated." The divergence on whether the template should restate this boundary (gh-aw yes, APM silent) is a tension about enforcement surface, not about the requirement itself. The requirement as specified in FR-024 is agreed as correct.

### 4. Output validation (FR-023) strikes the correct balance

Both reviews endorse the warn-but-write approach for output validation. gh-aw's Alignment #3 approves "heading-presence check, informational rather than blocking." APM's Alignment #4 approves avoiding "the failure mode where valid reasoning is discarded because the agent used a slightly different heading name." The agreement that malformed output should be flagged but preserved (not discarded) is a shared position that reflects both agents' experience with LLM output variability.

---

## Summary

gh-aw's review is operationally rigorous and identifies real gaps -- particularly the FR-022/FR-023 ambiguity and the underspecified "dispute entry" definition. However, its proposed fixes tend toward engine-level enforcement and definitional looseness (e.g., "any non-whitespace") that would create new problems. The directory-separation preference for draft templates is well-reasoned within gh-aw's compilation model but incompatible with APM's distribution model. The strongest shared ground is on failure semantics, trigger mechanism, citation authority, and output validation -- these are safe to treat as settled.
