# The Pragmatist: Cross-Review of The Purist

**Reviewer**: The Pragmatist
**Reviewing**: The Purist's positions on Blockers 1-4
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: Blocker 1 -- The Purist's trigger definition defeats the marker architecture it claims to defend

The Purist argues that Option A (pattern-matching `**Dispute:**`) is correct because it provides "a precise positive definition" and aligns the primary mechanism with the fallback. But The Purist simultaneously endorses the structural markers as the correct trigger surface -- the entire FR-011 amendment is built around the `CONVERSUS:DISPUTES_BEGIN/END` markers. This is contradictory. The markers were introduced specifically to decouple trigger evaluation from Markdown formatting conventions (v1 convergence point 5). Pattern-matching `**Dispute:**` inside the markers makes the markers load-bearing brackets around a regex check -- the same regex check the fallback already performs on the `### Remaining Disputes` heading. The Purist has written an amendment that preserves the markers' syntax while eliminating their semantic purpose. The primary mechanism becomes the fallback mechanism with extra XML. This is not alignment between two mechanisms; it is collapse into one mechanism wearing two costumes.

The danger: if adopted, future spec authors will see two mechanisms that do the same thing and conclude that one is redundant. They will remove the markers (the newer, less-tested surface) and the spec loses its only formatting-independent trigger path. The Purist's "alignment" creates a latent architectural regression.

### DC-2: Blocker 4 -- The Purist demands defense in depth but rejects the same principle in Blocker 2

In Blocker 4, The Purist's core argument is defense in depth: "the correct answer is: everywhere it can be enforced." Spec-level FR, template-level instruction, AND validation-level checking. Three layers. No gaps. But in Blocker 2, The Purist explicitly rejects SHOULD-level prose conventions in the template, arguing that "a SHOULD-level instruction in a template is not a contract -- it is a suggestion to an LLM. LLMs do not distinguish between SHOULD and MUST in their prompt." This directly contradicts the Blocker 4 position. In Blocker 4, the template instruction is a one-sentence SHOULD-equivalent that shapes LLM behavior. In Blocker 2, the template instruction is a SHOULD-level convention that shapes LLM output format. They are architecturally identical -- template instructions aimed at LLM compliance -- yet The Purist endorses one and dismisses the other.

The danger: The Purist's Blocker 2 position (defer all structured output guidance to v2) means v1 arbiter output will be freeform prose under FR-018 headings. Every v1 run produces output with different internal structure. When v2 extraction arrives, the inconsistency in the training corpus will make extraction harder, not easier. The Purist's own activation condition -- "when any downstream system depends on machine-readable arbitration output" -- triggers against output that The Purist's own v1 position made unreliable. The deferred schema activates into a data quality problem that the deferral created.

### DC-3: Blocker 3 -- The Purist's SC-010 is unimplementable under The Purist's own Blocker 4 validation position

The Purist proposes SC-010: "No binding decision in `resolution.md` MAY cite a `docs` entry as the sole basis for a ruling. Every binding decision MUST cite at least one principle, requirement, or constraint from the `grounding` document. A post-hoc audit of all `**Ruling:**` or equivalent decision entries must confirm grounding citations." This SC requires automated detection of citation sources in prose -- determining whether a phrase like "as established in the architectural principles" refers to the grounding document or a docs entry. In Blocker 4, The Purist proposes extending FR-023 to perform exactly this kind of citation validation, acknowledging it as a validation-layer check.

But this is the NLP problem. The Purist's own amended FR-023 uses the phrase "contains at least one reference to the grounding document path or its content." Path matching is string comparison. "Its content" matching is semantic similarity. The SC demands a post-hoc audit that "must confirm grounding citations" -- but the confirmation mechanism is undefined. If it requires human audit, it is not an automated SC. If it requires machine parsing of citation intent from prose, it is an NLP extraction problem that The Purist explicitly deferred to v2 in Blocker 2. The Purist has written a success criterion whose verification mechanism depends on capabilities the spec does not yet have.

---

## Tensions

### T-1: Completeness vs. implementability -- The Purist's SC set is more thorough but harder to test

The Purist proposes six SCs (SC-008 through SC-013). I propose four (SC-008 through SC-011). The Purist's additions -- SC-010 (citation grounding audit), SC-011 (per-file attribution), SC-012 (numbered requirement references) -- are formally correct. Every FR should have an SC. But SC-010 requires citation-source detection (see DC-3), SC-011 requires parsing "Summary of Changes Required" entries for file paths, and SC-012 requires distinguishing "FR-003" from "the validation requirement" in prose. These are extraction problems, not validation problems. My SCs are testable with structural checks (heading presence, file existence, overwrite behavior). The Purist's SCs require semantic parsing. The tension: The Purist's SCs are more complete as a specification artifact but less useful as a testing contract because they demand capabilities that v1 does not build.

### T-2: Activation conditions -- valuable mechanism, wrong trigger

The Purist's activation condition for the deferred structured output schema is genuinely useful. No other agent proposed one. "Structured extraction becomes a P1 requirement when any downstream system declares a dependency on structured arbitration data" is a clear, testable trigger. The tension: the trigger is externally defined ("the first spec that declares a dependency") which means it cannot be evaluated from within this spec's scope. It requires cross-spec dependency tracking that the conversus framework does not currently support. A trigger that depends on infrastructure the spec ecosystem does not have is not actionable -- it is a correct statement about a future world. I would prefer a time-boxed trigger ("re-evaluate after 5 production arbitration runs") that is evaluable without new infrastructure, even though it is less formally precise.

### T-3: Single-regex testability vs. formatting fragility

The Purist's claim that Option A makes the trigger "testable with a single regex" is true and appealing. `^\\s*\\*\\*Dispute` is a clean predicate. My Option B definition ("non-whitespace, non-HTML-comment content") is also a clean predicate but over a broader domain. The tension is real: Option A is more precise but more fragile (one formatting deviation kills it). Option B is less precise but more robust (only whitespace and comments can suppress it). The Purist frames this as "defined convention vs. undefined convention." I frame it as "brittle positive match vs. robust negative match." Neither framing is wrong. The question is which failure mode you prefer -- and FR-012's "default to true" principle tips toward robustness, not precision.

---

## Safe Agreements

### SA-1: Success criteria are P1 and must be written now

Complete alignment. The Purist and I both classify missing SCs as P1. The Purist's argument -- "the cost of writing SCs is measured in minutes, the cost of discovering incompatible implementations is measured in debugging sessions" -- is the same argument I make. We agree on SC-008 (failure semantics) and SC-009 (partial output with warnings) almost verbatim. The SC numbering, structure, and Given/When/Then implicit framing are compatible. The disagreement is on scope (six vs. four SCs), not priority or necessity.

### SA-2: The template is the runtime enforcement surface for LLM agents

Both reviews converge on this. The Purist states: "The agent does not read the spec. It reads its template. An unenforced constraint is not a constraint." I state: "LLM agents see prompts, not specs." We both add the citation boundary instruction to the template authoring contract. We both cite the FR-015 precedent (behavioral constraints already restated as template instructions). The Purist goes further with FR-023 validation; I consider that a v2 concern. But on the core thesis -- the template is where agent-facing constraints must live -- there is no daylight between us.

### SA-3: FR-024 belongs in the spec as a normative requirement

Neither review disputes that the citation boundary should be a spec-level FR. APM's position that FR-024 alone is sufficient was rejected by both of us. The Purist and I both endorse Option C (spec + template). The only difference is whether FR-023 validation should also cover citation sources (Purist: yes now; Pragmatist: v2 concern). On the normative standing of the citation boundary as a formal requirement, we are fully aligned.
