# The Mechanist: Cross-Review of The Purist

**Reviewer**: The Mechanist (operational/engine perspective)
**Subject**: The Purist's dispute resolution positions
**Date**: 2026-03-19

---

## Dangerous Contradictions

### 1. Blocker 1 — Pattern-match trigger vs. the spec's own fail-open mandate

The Purist selects Option A (pattern-match `**Dispute:**`) and builds a careful argument about definitional precision: "A predicate must have a precise positive definition." This is formally sound and operationally lethal. The Purist's own review never addresses FR-012's explicit directive: "better to run the arbiter unnecessarily than to skip it when disputes exist." Pattern-matching fails closed. When a Phase 5 synthesizer writes `**Unresolved issue:**` or `- Dispute:` (no bold) or any natural-language variant the regex does not anticipate, the engine evaluates the trigger as false and Phase 6 does not run. Real disputes are silently dropped.

The Purist's false-positive scenario -- "All disputes were resolved during deliberation" appearing between markers -- is real but recoverable. The arbiter reads zero disputes, produces a trivial endorsement, and the engine writes a vacuous `resolution.md`. The cost is one wasted LLM invocation. The Purist's own preferred outcome for Blocker 4 (defense-in-depth, all three surfaces) reveals an implicit preference for over-detection over under-detection. But on Blocker 1, the Purist reverses this preference and selects the mechanism that under-detects. These two positions cannot coexist. Either the spec should err toward catching too much (Blocker 4 logic) or toward catching only what matches a known pattern (Blocker 1 logic). The Purist applies both principles selectively without reconciling them.

The argument that "the fallback already uses `**Dispute:` pattern matching, so the primary should too" proves the opposite of what the Purist intends. If primary and fallback use the same pattern, they are not independent mechanisms. They are the same mechanism executed twice. The structural markers become pure ceremony -- they add complexity without adding coverage. Defense-in-depth requires that the two mechanisms test different things, which is exactly what content-negative (primary) plus pattern-match (fallback) achieves.

### 2. Blocker 2 — Activation condition demands vs. unenforceable v1 constraints

The Purist criticizes every other agent for failing to define when the deferred structured output becomes required, then proposes an activation condition: "Structured extraction becomes a P1 requirement when any downstream system depends on machine-readable arbitration output." This sounds rigorous. It is not. The trigger -- "when any downstream system declares a dependency" -- is an event that occurs outside the spec's control surface. No actor in the conversus system monitors downstream dependency declarations. No engine check fires when this condition is met. The Purist has written an activation condition that is itself unactivatable.

This contradicts the Purist's own standard from Blocker 3: "If a requirement cannot be tested, it cannot be verified. If it cannot be verified, it is not a requirement." The activation condition cannot be tested by the engine, cannot be verified by any automated process, and depends entirely on a future human recognizing that the condition has been met. By the Purist's own criteria, this activation condition is not a requirement -- it is an aspiration wearing a requirement's clothes. The same criticism the Purist levels against SHOULD-level prose conventions ("LLMs do not distinguish between SHOULD and MUST in their prompt") applies symmetrically: no system distinguishes between "activation condition exists in the spec" and "activation condition does not exist" unless something checks for it.

The mechanist position avoids this trap by deferring cleanly without pretending the deferral has a machine-checkable trigger. Honest deferral is better than pseudo-rigorous activation conditions that no system monitors.

### 3. Blocker 3 — SC-010 introduces a validation burden the spec cannot discharge

The Purist and I agree that success criteria are P1. The dangerous contradiction is in the content of SC-010: "A post-hoc audit of all `**Ruling:**` or equivalent decision entries must confirm grounding citations." This SC requires the engine to parse `**Ruling:**` entries inside the Binding Decisions section -- the same prose-convention parsing that the Purist explicitly rejected for Blocker 2. On Blocker 2, the Purist argues that SHOULD-level labeled sub-fields are "not a contract" because "LLMs do not distinguish between SHOULD and MUST." On Blocker 3, the Purist writes an SC that depends on `**Ruling:**` entries existing in a parseable form. If the arbiter does not produce labeled `**Ruling:**` entries (which it has no MUST-level obligation to do under the Purist's own Blocker 2 position), SC-010 has nothing to audit.

The mechanist's SC-010 avoids this by testing at the section level: "No binding decision in `resolution.md` cites a `docs` entry as the sole authority for a ruling. At least one `grounding` citation appears in every ruling's rationale." This is still difficult to validate mechanically on unstructured prose, but it does not depend on a sub-field convention that the Purist's own Blocker 2 position refuses to mandate.

---

## Tensions

### 1. Definitional precision vs. operational resilience (Blocker 1)

The Purist and I share a commitment to unambiguous spec language but disagree on which ambiguity is worse. The Purist fears false positives: the trigger fires when no disputes exist, wasting an arbiter invocation. I fear false negatives: the trigger does not fire when disputes do exist, silently dropping unresolved conflicts. Both are real risks. The tension is irreducible because the two failure modes have asymmetric costs, and we weight them differently. The Purist weights correctness of the trigger predicate (it should fire if and only if disputes exist). I weight safety of the system (it should never silently skip disputes, even at the cost of occasional unnecessary invocations). FR-012's fail-open directive suggests the spec authors share my weighting, but the Purist's argument about mechanism alignment (primary and fallback should agree) is a legitimate design concern that I do not fully resolve.

### 2. Contract completeness vs. premature formalization (Blocker 2)

The Purist wants every deferred item to have an explicit activation condition. I want clean deferrals that do not pretend to be more rigorous than they are. The tension is genuine: a deferral without a trigger risks being forgotten indefinitely, but a trigger that no system monitors risks creating false confidence that the transition is managed. The Purist's activation condition ("when any downstream system declares a dependency") is the right kind of question but the wrong kind of answer -- it requires human judgment to evaluate, which means it is a process obligation, not a specification constraint. My approach accepts that some transitions are inherently process-driven and keeps them out of the formal spec. Neither position is clean. The Purist's is more explicit; mine is more honest about what the spec can actually enforce.

### 3. Scope of engine validation (Blocker 4)

We both select Option C (all three surfaces) and agree that engine validation is the authoritative backstop. The tension is in emphasis. The Purist treats the three surfaces as co-equal ("defense in depth is not a luxury") and argues from architectural symmetry with FR-015. I treat the engine as the only load-bearing surface and the other two as probability modifiers. This matters when the surfaces conflict: if the template says one thing and the engine validates another (due to a maintenance drift the Purist acknowledges as a real risk), whose verdict wins? Under my hierarchy, the engine always wins. Under the Purist's co-equal model, the conflict itself is a specification defect that must be resolved before proceeding. In practice this tension rarely manifests, but it reveals a deeper disagreement about whether the spec is a static document or an executable contract.

---

## Safe Agreements

### 1. Success criteria are P1 and block implementation (Blocker 3)

No daylight between our positions. The Purist states: "If a requirement cannot be tested, it cannot be verified. If it cannot be verified, it is not a requirement." I state: "A requirement without a test is a requirement the engine cannot verify. A requirement the engine cannot verify is dead letter." We arrive at the same conclusion from different premises -- the Purist from formal completeness, I from operational necessity -- but the conclusion is identical. Our proposed SC-008 through SC-013 entries are substantively aligned, differing only in phrasing. Either set resolves the blocker.

### 2. FR-024 needs template-level restatement (Blocker 4)

Both reviews independently identify the asymmetry between FR-015 (behavioral constraints restated in the template) and FR-024 (citation boundary not restated). The Purist's argument from architectural consistency is compelling: "If one gets template enforcement, both should." My argument from operational necessity arrives at the same place: the arbiter does not read the spec, so constraints invisible to the arbiter are constraints the arbiter cannot follow. We both propose adding the citation boundary to the FR-015 instruction list and to the template authoring contract invariants. The proposed text is nearly identical.

### 3. The v1 output contract is FR-018 section headings (Blocker 2)

Both reviews reject prose conventions as a v1 contract obligation. The Purist says: "A SHOULD-level instruction in a template is not a contract -- it is a suggestion to an LLM." I say: "An unenforceable SHOULD is worse than no SHOULD -- it creates false confidence." We both place the advisory schema in a standalone deferred section with SHOULD-level language for v2 planning. The Purist adds an activation condition I consider unenforceable (see Dangerous Contradictions #2), but the core agreement -- headings only for v1, schema deferred to v2 -- is solid and sufficient to resolve the blocker.
