# APM Cross-Review of Spec-Kit's Review

**Cross-reviewer**: APM (Agent Package Manager)
**Reviewing**: spec-kit's review of Subject Arbitration (Phase 6)
**Date**: 2026-03-19
**Type**: Cooperative conversus cross-review

---

## Dangerous Contradictions

### DC-1: Cooperative-only restriction -- accept and constrain vs. reject and ship

Spec-kit's review **accepts** the cooperative-only restriction as valid and works within it. Its recommendations reinforce the constraint: P2-5 asks to "acknowledge the non-cooperative arbitration templates and define their status" as "draft templates prepared for future extension," and explicitly states "enabling arbitration for other modes requires a separate spec."

APM's review calls this a **consistency defect** and recommends removing FR-004 entirely (P1-1): "enable all four modes from launch since the templates are already written and tested." APM frames the cooperative-only restriction as dead code and delayed value delivery.

These are incompatible recommendations. If spec-kit's P2-5 is adopted, the non-cooperative templates are formally declared experimental and gated behind a future spec. If APM's P1-1 is adopted, all four modes ship immediately with no additional specification work. The spec cannot do both. The danger: APM's recommendation to ship all modes without a spec analyzing game-theoretic implications for non-cooperative arbitration could produce arbitration behavior that is semantically wrong for adversarial modes. Spec-kit correctly identifies that "enabling arbitration for other modes requires a separate spec that analyzes the game-theoretic implications" -- a winner-take-all arbiter operates under fundamentally different legitimacy conditions than a cooperative one, and shipping templates without specifying those conditions is not the same as shipping validated behavior.

**Risk**: Adopting APM's position ships four arbitration modes with only one mode's semantics formally specified. Adopting spec-kit's position delays value from ready templates behind a spec-writing bottleneck.

### DC-2: Decision authority vs. information asymmetry -- overlapping critique, incompatible reframes

Both reviews flag the same assumption as too narrow: "Subject arbitration is only meaningful when the deliberation agents represent external perspectives and the subject has its own distinct operational perspective."

Spec-kit reframes around **decision authority**: "the meaningful distinction is not external-vs-internal perspective but rather authority-to-decide vs. authority-to-advise" (Off-Base Assumption #1). Its P2-7 recommendation replaces the assumption with: "Subject arbitration is meaningful when the arbiter has both decision authority over the target artifact and a declared grounding document that constrains that authority."

APM reframes around **integration scope**: "Subject arbitration is also meaningful when the agents represent *internal* perspectives... and the subject is the system that must integrate all of their work" (Off-Base Assumption #1). APM's P3-10 says the assumption "unnecessarily narrows the design's applicability" for prisoners-dilemma and red-blue modes.

These reframes contradict each other. Spec-kit's framing makes the grounding document the source of legitimacy -- authority is constrained by the document, not by the arbiter's knowledge. APM's framing makes the arbiter's unique position (cross-cutting constraints, production behavior, actual usage patterns) the source of legitimacy -- the arbiter knows things no individual agent knows. Under spec-kit's model, a project owner with a constitution but no operational knowledge is a valid arbiter. Under APM's model, a system with deep operational knowledge but no formal decision authority is a valid arbiter. Both cannot be the foundational justification simultaneously, and the spec must choose which legitimacy model governs when these two sources conflict.

**Risk**: If both reframes are adopted without reconciliation, the spec would contain two contradictory justifications for when arbitration is appropriate, leaving implementers without clear guidance on who qualifies as an arbiter.

### DC-3: "No new recommendations" -- accept as absolute vs. carve out exceptions

Spec-kit's review does not flag any problem with the "no new recommendations" constraint (FR-015.5). Its Missed Opportunity #6 discusses the Confidence Assessment section but treats it as disconnected from the scope constraint -- a separate gap about actionability, not a tension with FR-015.5. Spec-kit implicitly accepts the absolute prohibition.

APM's review identifies a direct contradiction between the spec and the template (Off-Base Assumption #3): "The template says 'note it as an observation in the Confidence Assessment, not as a ruling.' The spec's formal requirements should explicitly carve out the observation exception." APM's P1-3 recommends reconciling this gap by allowing observations that are excluded from binding decisions.

This is a correctness-level disagreement. If spec-kit's implicit acceptance holds, an arbiter that notes ANY new observation -- even one explicitly excluded from rulings -- violates the spec. If APM's carve-out is adopted, the arbiter can surface new signals as long as they are labeled as observations and not binding. The template already encourages the behavior APM wants to formalize. The danger is that without resolution, an LLM following the spec's requirements section would suppress observations that the template's instructions tell it to include.

**Risk**: A literal reading of the spec (which an LLM will follow) suppresses a behavior the template explicitly encourages, creating silent information loss during arbitration.

---

## Tensions

### T-1: Structured output -- same diagnosis, different prescriptions

Both reviews identify the lack of machine-readable output as a gap. Spec-kit's Missed Opportunity #1 proposes "structured markers (e.g., `<!-- RULING: dispute-id -->`) or a YAML front matter block in the resolution." APM's Missed Opportunity #9 proposes "a machine-readable summary sidecar" (`resolution.summary.yml`).

These are architecturally different approaches. Spec-kit embeds structure inside the existing markdown file. APM creates a separate artifact alongside it. Embedded markers keep one file but complicate template authoring and parsing. A sidecar keeps the resolution clean but doubles the output artifacts and requires the orchestrator to produce and manage both files. The tension is real but not dangerous -- both solve the problem, and the spec could adopt either without breaking anything. However, adopting both (embedded markers AND a sidecar) would create redundant structured data that could drift out of sync.

### T-2: Grounding document -- single authoritative source vs. composable context graph

Spec-kit's Missed Opportunity #5 recommends a **convention**: "arbiter.grounding SHOULD be the constitution path." This preserves the single-path model but gives it semantic meaning within spec-kit projects.

APM's P2-4 recommends a **structural change**: "Support `grounding` as a list of paths, not just a single path." This changes the schema to accept multiple grounding documents, allowing decision frameworks that span architecture decision records, constitutions, and operational requirements.

These pull in opposite directions. Spec-kit wants to constrain and name the single grounding path (it should be the constitution). APM wants to expand the grounding field to accept multiple paths (the decision framework is rarely one document). A single grounding document that IS the constitution is clean and auditable. A grounding list that spans multiple documents is flexible but dilutes the constraint -- if the arbiter can ground rulings in any of five documents, the citation requirement becomes weaker. The tension reflects a genuine design tradeoff between specificity (one document, one authority) and expressiveness (multiple documents, richer context).

### T-3: Trigger evaluation fragility -- same problem, different enforcement mechanisms

Both reviews flag the `### Remaining Disputes` heading dependency as fragile. Spec-kit's P1-3 recommends elevating it to a constraint with a "template linting rule" that checks for the heading's presence during template loading. APM's P1-2 recommends replacing the heading with "a machine-readable marker (e.g., `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`)" and updating FR-011 to reference the marker.

Spec-kit preserves the human-readable heading and adds enforcement. APM replaces the human-readable heading with a machine-readable marker. Spec-kit's approach is backward-compatible (existing templates keep working, linting is additive). APM's approach is a breaking change to Phase 5 templates (they must add HTML comments). The tension is between preserving the current contract with enforcement vs. replacing the contract with a more robust one.

### T-4: Downstream integration -- spec-kit pipeline vs. APM packaging ecosystem

Spec-kit frames nearly every recommendation through downstream SDD pipeline consumption: `/speckit.specify --input`, `/speckit.plan`, `/speckit.checklist`. Its recommendations assume arbitration output feeds into spec-kit commands.

APM frames recommendations through packaging and distribution: arbiter configs as reusable artifacts, hook points for lifecycle events, context linking for grounding documents, primitive taxonomy for the arbiter concept.

Neither is wrong, but they pull the spec in different directions. Spec-kit wants arbitration output optimized for a specific downstream consumer (the SDD pipeline). APM wants arbitration configuration optimized for reuse across projects. A spec that satisfies both could become overspecified -- adding structured output for spec-kit's parser AND packaging conventions for APM's compile pipeline AND hooks for APM's lifecycle system significantly expands the scope of what was designed as a minimal Phase 6 addition.

### T-5: Schema versioning -- urgent vs. absent

APM's P2-5 explicitly recommends adding `schema: 1` or `version: 1` to `conversus.yml`, citing APM's own `apm.yml` versioning as precedent. This is presented as a design integrity requirement.

Spec-kit's review does not mention schema versioning at all. Its recommendations add fields and conventions to the existing schema without any versioning concern.

The tension: APM sees schema evolution as a first-class problem that must be solved before the next breaking change. Spec-kit implicitly treats the schema as stable enough that versioning is unnecessary. If APM is right, every recommendation from both reviews that modifies `conversus.yml` (adding structured output formats, grounding lists, hook points) makes the eventual versioning migration harder. If spec-kit is right by omission, introducing versioning now adds ceremony to a young, fast-moving schema.

---

## Safe Agreements

### SA-1: Template-per-mode extensibility is architecturally correct

Both reviews independently validate the `templates/{mode}/arbitration.md` convention. Spec-kit: "Template-driven extensibility follows spec-kit's own extension model... each new capability is a template, not a code change" (Alignment, bullet 2). APM: "Template-per-mode convention is correct... mirrors APM's own convention-based file discovery" (Alignment, bullet 1). Both frameworks use the same pattern internally, and both confirm it is the right choice here. No disagreement exists on this point.

### SA-2: Backward compatibility is correctly implemented

Both reviews confirm that the optional `arbiter` field preserves existing behavior. Spec-kit: "Backward compatibility is a first-class design constraint, not an afterthought. FR-005 and SC-004 explicitly require that omitting the arbiter field produces identical output" (Alignment, bullet 6). APM: "Backward compatibility is properly preserved. The `arbiter` field is fully optional, omitting it produces identical Phase 1-5 behavior" (Alignment, bullet 4). Neither review identifies any regression risk from the Phase 6 addition.

### SA-3: Grounding-document-as-citation-source is a sound integrity mechanism

Both reviews endorse the core design: arbitration decisions must cite a declared grounding document. Spec-kit: "Grounding document requirement maps directly to spec-kit's constitution pattern. Both enforce that decisions cite a declared framework" (Alignment, bullet 1). APM: "Grounding-document-as-citation-source is a strong integrity mechanism... maps directly to APM's constitution injection pattern" (Alignment, bullet 2). The reviews diverge on how grounding should be configured (single path vs. list, convention vs. schema change) but agree completely on the principle that grounding-constrained arbitration is the right model.

### SA-4: The `### Remaining Disputes` heading dependency is a fragile contract that must be hardened

Both reviews flag this as a real problem. Spec-kit calls it "a cross-template coupling that spec-kit would flag as a constitution violation" (Missed Opportunity #3) and recommends elevating it from assumption to constraint (P1-3). APM calls it "a fragile contract" (Off-Base Assumption #2) and recommends formalizing it with machine-readable markers (P1-2). The diagnosis is identical. The proposed solutions differ (linting vs. markers), but both agree the current assumption-based approach is insufficient and must be hardened before Phase 6 ships.

---

## Summary

The two reviews share substantial common ground on fundamentals (template conventions, backward compatibility, grounding integrity, trigger fragility). The dangerous contradictions cluster around **scope** (how many modes to ship), **legitimacy** (what makes an arbiter qualified), and **constraint interpretation** (whether observations violate the "no new recommendations" rule). The tensions are genuine design tradeoffs rather than errors -- structured output format, grounding cardinality, enforcement mechanism, and downstream integration priorities all involve legitimate competing values that the spec author must adjudicate.

APM's recommendation to the spec author: resolve DC-1 by adopting spec-kit's position (keep cooperative-only, formally status the other templates as drafts), resolve DC-2 by synthesizing both reframes (decision authority constrained by a grounding document, informed by the arbiter's unique integration perspective), and resolve DC-3 by adopting APM's position (explicitly carve out observations from the "no new recommendations" constraint to match the template's actual instructions).
