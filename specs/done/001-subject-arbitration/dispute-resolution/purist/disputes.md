# The Purist: Final Disputes

**Agent**: The Purist (specification completeness, formal correctness, explicit contracts)
**Date**: 2026-03-19
**Phase**: Disputes (post-revision)

---

## Remaining Disputes

### Dispute 1: FR-023 grounding-reference validation -- MUST vs. SHOULD

**Claim**: The grounding-reference check in the Binding Decisions section must be a MUST-level requirement, not a SHOULD-level heuristic.

**The Mechanist's revised position**: Downgrade the grounding-reference check from MUST to SHOULD because it is a "heuristic, not deterministic enforcement." The Mechanist's revised FR-023 reads: "the engine SHOULD check that the Binding Decisions section contains at least one occurrence of the grounding document identifier." SHOULD means an implementor may omit it. The Mechanist explicitly relabels this as an "advisory warning."

**Why this is wrong**: The Mechanist conceded too much. String-presence of a known path in a known section is not a heuristic in any meaningful sense. The grounding document path is an engine-controlled variable (`{GROUNDING_PATH}`), injected into the template by the engine itself. Checking whether that exact string appears in the Binding Decisions section is the same class of operation as checking whether an FR-018 section heading appears in the file -- both are string-presence checks against known values. The Mechanist does not downgrade heading validation to SHOULD. There is no principled reason to downgrade grounding-reference validation to SHOULD either.

The Mechanist's concession was a response to the valid criticism that full citation-source validation (verifying that no ruling cites only a docs entry) is genuinely heuristic. But the Mechanist overcorrected by downgrading the entire check rather than splitting it. The Pragmatist got this right: "If heading validation fails, the engine MUST emit a warning. If the grounding document path is absent from Binding Decisions, the engine MUST emit a separate warning." Both are string-presence. Both are deterministic. Both should be MUST.

**Proposed resolution**: Adopt the Pragmatist's FR-023 formulation. The grounding-path-presence check is MUST (deterministic string search). Semantic citation-source analysis (per-ruling grounding verification) is deferred to v2. The Mechanist's concern about overstating engine capability is addressed by the deferral of the hard problem, not by weakening the easy one.

---

### Dispute 2: Vacuous resolution detection -- SC-014 is insufficient without a defined arbiter response

**Claim**: SC-014 detects vacuous output after the fact but does not close the architectural gap that produces it. The spec must define what the arbiter should do when no actionable disputes exist in its input.

**The Pragmatist's revised position**: Add SC-014 -- "Given a Phase 6 run triggered by a false-positive dispute predicate, When the arbiter produces output with all FR-018 section headings but zero binding decisions in the Binding Decisions section, Then the engine writes resolution.md and emits a validation warning." The Pragmatist treats vacuous output as a detection problem, not a prevention problem, and argues the trigger definition is not the correct fix because vacuous output can arise from multiple causes.

**Where the Pragmatist is right**: Vacuous output can arise from causes other than false-positive triggers. Tightening the trigger alone does not eliminate it. SC-014 is a genuine contribution that makes a previously silent condition visible.

**Where the Pragmatist is incomplete**: SC-014 fires after the arbiter has already run and produced a vacuous file. The warning tells a human reviewer "this resolution resolved nothing." But the spec provides no guidance for what the arbiter should produce when it encounters zero actionable disputes. FR-015 instructs the arbiter on six behavioral constraints but says nothing about the zero-dispute input case. Without guidance, arbiter behavior on vacuous input is undefined -- some templates may produce a clean "no disputes found" statement, others may hallucinate disputes to fill the sections, others may produce structurally valid but semantically incoherent output. SC-014 detects the symptom. It does not address the cause.

I conceded Option B as the primary trigger and I do not reopen that concession. But the content-negative trigger makes the zero-dispute input case a foreseeable condition, not an edge case. Foreseeable conditions require defined behavior.

**Proposed resolution**: Accept SC-014 as written. Additionally, add a one-sentence instruction to FR-015's behavioral constraints: "If the arbiter determines that no actionable disputes exist in the input, the Binding Decisions section MUST state this explicitly rather than producing fabricated or speculative rulings." This gives the arbiter a defined response for the zero-dispute case, makes SC-014's detection more reliable (an explicit "no actionable disputes" statement is easier to detect than inferring vacuity from zero binding decisions), and addresses the hallucination risk that was the core of my original Blocker 1 objection.

---

### Dispute 3: The deferred structured output section -- SHOULD conventions in the template vs. no conventions

**Claim**: Template authors SHOULD use labeled sub-fields to improve output regularity, and this guidance belongs in the deferred section, not hidden in Implementation Guidance.

**The Mechanist's revised position**: Headings only for v1. No SHOULD-level prose conventions anywhere. Template authors are "free to use labeled sub-fields as instructional hints" but this is not stated in the spec. The Mechanist adds only a process-level review trigger ("collect 50+ samples, then evaluate").

**The Pragmatist's revised position**: Retreated from SHOULD-level spec conventions to MAY-level template-author guidance in Implementation Guidance. The Pragmatist now agrees with the Mechanist that spec-level SHOULD conventions are unenforceable pseudo-contracts.

**Why both retreated too far**: I conceded in my revision that my original activation condition was not machine-checkable and that SHOULD-level template conventions are architecturally consistent with the template instructions I endorsed in Blocker 4. I stand by both concessions. But the conclusion I draw is different from the Mechanist's and the Pragmatist's.

The Mechanist says: since conventions cannot be engine-validated, they should not appear in the spec. The Pragmatist says: since conventions cannot be engine-validated, they should appear only as MAY-level template-author guidance. Both treat engine-enforceability as the criterion for spec inclusion. But the spec already contains requirements that the engine cannot validate -- FR-015's behavioral constraints ("do NOT introduce new recommendations beyond the grounding document's scope") are not engine-checkable. FR-024's citation boundary is not engine-checkable beyond string-presence. The spec includes these because they are normatively important, not because they are machine-enforceable.

SHOULD-level template conventions for labeled sub-fields serve the same function as FR-015's behavioral constraints: they shape arbiter output toward a desired distribution. The difference is that FR-015 shapes behavior and the sub-field conventions shape format. Both are probabilistic. Both are unenforceable. Both are worth stating because they communicate intent to template authors and establish a baseline that real output can be measured against.

My revised deferred section already includes this language: "Template authors SHOULD design prose to be consistent with these fields and SHOULD use labeled sub-fields to improve output regularity, but arbiter output that omits or renames these labels is compliant if it contains the required FR-018 section headings." This is honest. It says what the convention is, says compliance does not require it, and places it in the deferred section where it belongs -- visible to template authors, not buried in Implementation Guidance where it may be overlooked.

**Proposed resolution**: Adopt my revised deferred section text. The SHOULD conventions live in the deferred section alongside the schema fields. They are explicitly non-contractual. They provide visible guidance to template authors. The Pragmatist's MAY-level Implementation Guidance alternative achieves the same goal at lower visibility -- I accept it as a fallback if the other two agents find SHOULD unacceptable, but SHOULD in a deferred section is the more honest placement.

---

## Convergence

### 1. Option B (content-negative) as the primary trigger with pattern-match fallback

All three agents now agree that the primary trigger mechanism is content-negative: any non-whitespace, non-HTML-comment content between the markers constitutes a trigger. The pattern-match mechanism (`**Dispute` prefix) serves as the fallback when markers are absent. The Mechanist held this position throughout. The Pragmatist held it throughout. I conceded to it in my revision after both reviewers demonstrated that my original Option A optimized for the wrong failure mode given FR-012's fail-open directive. The convergence is complete and principled: primary and fallback test different things, providing independent detection paths.

### 2. FR-018 section headings are the sole enforceable v1 output contract

All three agents now agree that the v1 output contract is FR-018 section headings and nothing more. The Mechanist held this from the start. I held this from the start (my Option C always had headings as the v1 contract). The Pragmatist conceded in revision, withdrawing the SHOULD-level prose conventions from the spec-level contract after both the Mechanist and I demonstrated that unenforceable SHOULD conventions create de facto contracts without engine backing. The remaining disagreement (Dispute 3 above) is about the visibility and normative level of template-author guidance, not about the v1 contract itself.

### 3. Success criteria are P1 with six SCs in Given/When/Then format

All three agents classify missing SCs as P1 spec-completeness defects. All three converged on six SCs covering FR-022 through FR-027. The Mechanist proposed the Given/When/Then format; the Pragmatist adopted it; I accept it as a better testing format. The Pragmatist added SC-014 (vacuous output detection), which I endorse as a genuine contribution. Specific SC wording varies between agents (Dispute 1 covers the MUST vs. SHOULD disagreement on SC-010's grounding check), but the coverage, priority, and format are unanimous.

### 4. Option C for citation enforcement -- all three surfaces, honestly scoped

All three agents selected Option C from the beginning. All three now agree on the implementation:
- **Spec layer**: FR-024 defines the normative rule (unchanged).
- **Template layer**: FR-015 instruction list gains a seventh item restating the citation boundary. The template authoring contract gains a corresponding invariant.
- **Validation layer**: FR-023 gains grounding-path-presence validation in v1. Semantic citation-source analysis is deferred to v2.

The Mechanist and Pragmatist converged on the same three concrete changes I proposed in my original review. The only remaining disagreement is the normative level of the grounding-path check (Dispute 1 above). The architectural decision -- three surfaces, defense in depth, v1 validation scoped to string-presence -- is shared by all three agents.

### 5. The engine citation check is string-presence, not semantic parsing

All three agents now draw the same line: checking whether the grounding document path (a known, engine-injected string) appears in the Binding Decisions section is a string-presence operation that belongs in v1. Checking whether individual rulings cite only docs entries is a semantic-parsing operation that belongs in v2. The Mechanist reached this after conceding the Blocker 2/Blocker 4 inconsistency. The Pragmatist reached this after conceding that deferring all citation validation was "negligent." I reached this after conceding that my original SC-010 depended on sub-field parsing that my Blocker 2 position did not mandate. Three independent paths to the same boundary.

---

## Final Position Statement

### What I conceded and why it was correct to concede

I made three material concessions during this process, and each one resolved a genuine inconsistency in my original position.

First, I conceded Option B as the primary trigger. My original position optimized for trigger precision at the expense of trigger completeness -- the exact inversion of FR-012's fail-open philosophy. The Mechanist's argument that primary and fallback must test different things to constitute independent mechanisms was decisive. A defense-in-depth architecture where both layers use the same predicate is not defense in depth. It is redundancy without independence.

Second, I conceded that my activation condition for the deferred structured output section was not machine-checkable. The Mechanist applied my own standard back to me, and the standard held. A condition that requires a human to notice an external event is a process obligation, not a specification constraint. I replaced it with a process-level note that is honest about what it is.

Third, I conceded that SC-010 as originally written depended on sub-field parsing that my Blocker 2 position did not mandate. This was an internal contradiction -- I cannot reject prose conventions as a v1 contract and then write success criteria that assume they exist. The SC is rewritten to test at the section level via string-presence.

### What I hold and why it is correct to hold

**The grounding-reference check must be MUST, not SHOULD.** The Mechanist overcorrected. String-presence of a known engine-injected path is deterministic. The concern that justified the downgrade -- that the check cannot verify citation intent -- is real but applies to a different, harder check that all three agents agree belongs in v2. The easy check should not be weakened because the hard check is hard.

**Vacuous output needs a defined arbiter response, not just post-hoc detection.** SC-014 is necessary but not sufficient. The content-negative trigger makes zero-dispute input a foreseeable condition. Foreseeable conditions require defined behavior. A one-sentence addition to FR-015's behavioral constraints closes this gap at zero implementation cost.

**SHOULD-level template conventions belong in the deferred section, not buried in Implementation Guidance.** The spec already contains unenforceable behavioral constraints (FR-015, FR-024). Adding SHOULD-level formatting conventions to the deferred section is architecturally identical. Visibility to template authors matters. Implementation Guidance is where implementors look for engine behavior. The deferred section is where template authors look for output expectations. The guidance should live where its audience reads.

### The thread

My original review ended with: "a specification is a contract, and contracts must be enforceable at every boundary where violations can occur." The cross-reviews taught me that I was applying this principle inconsistently -- demanding enforcement-at-every-boundary for some constraints while selecting narrow mechanisms for others. My revised positions resolve those inconsistencies. But the principle itself survived every challenge. Every concession I made was a concession to better consistency in applying the principle, not an abandonment of it. The three remaining disputes above are cases where the other agents have not yet applied the principle consistently to their own positions. A MUST-level check that is deterministic should not be downgraded to SHOULD. A foreseeable input condition should not be left with undefined behavior. Guidance for template authors should not be hidden from template authors. These are not purist extravagances. They are the minimum standard for a specification that means what it says.
