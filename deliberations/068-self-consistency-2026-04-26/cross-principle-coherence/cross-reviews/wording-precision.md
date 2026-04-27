# Cross-Review of wording-precision's Phase 1 Review

**Reviewer**: cross-principle-coherence
**Target**: wording-precision/review.md
**Constitution**: CONSTITUTION-v2.3.2-candidate.md

## Executive Framing

wording-precision focused on the *intra-principle* normative grammar of XVI (MUST vs descriptive prose, undefined terms, passive voice, weak "claims" verb), while my Phase 1 review focused on *inter-principle* coherence (XVI ↔ VII, XVI ↔ XI, XVI ↔ V, XVI ↔ XXIV). The two reviews land on the same single largest defect — XVI narrows VII's unconditional "structurally identical output" claim without VII being amended — but reach it from different directions. wording-precision frames it as a missing carve-out sentence; I frame it as a unilateral redefinition of VII via the "(Principle VII applies)" parenthetical at line 476. Both framings are correct and compatible, and both reviews independently arrive at the same P1 fix: state the exception explicitly.

There are also genuine tensions where our prescriptions, if both applied verbatim, would produce slightly different texts that need coordination, and a small set of points where we appear to disagree but on closer reading are talking about distinct objects (intra-principle clarity vs cross-principle obligation).

---

## Dangerous Contradictions

### 1. Pinning storage location: "output directory" vs deterministic-tree placement

- **Their claim**: wording-precision Recommendation #6 (P2) prescribes pinning storage as "persisted to the run's output directory and reused for the lifetime of that directory" (review.md L83-84). The justification is auditability — reviewers need to know where to look.
- **My claim**: My Missed Opportunity on Principle X (review.md L25) prescribes that pinned parameters land "in a deterministic location in the output tree (e.g., next to `summary/final.md`)" so persistence is observable per Principle X's "one obvious way to find the result" (constitution L283).
- **Why this is dangerous**: Both fixes name a location, but "the run's output directory" (theirs) is a weaker constraint than "deterministic location adjacent to summary/final.md" (mine). If the constitution adopts the loose phrasing, an implementation could legitimately stash parameters in any subdirectory of the run output and still satisfy XVI — but fail to satisfy X's findability requirement. If both fixes land textually independent, a future PR can comply with one and violate the other while citing XVI as authority.
- **Resolution**: Coordinate on a single phrasing that satisfies both: "Pinned parameter values MUST be persisted to a deterministic path inside the run's output directory (recommended: `parameters.json` adjacent to `summary/final.md`) and MUST be reused for the lifetime of that directory." This makes the location both *named* (theirs) and *predictable per X* (mine).
- **Confidence**: High that the contradiction is real. Medium-high that the unified phrasing closes it without other side effects.

### 2. Cross-run variance bound: shape-only vs shape + caching policy

- **Their claim**: wording-precision Recommendation #5 (P2) bounds cross-run variance as "Cross-run variance in resolved parameter *values* is acceptable; cross-run variance in the assembled objective function's *shape* (parameter names, template selection, gap-identifier set) is prohibited" (review.md L77-78).
- **My claim**: My Off-Base #1 (review.md L34) flags that "Repeating a deliberation with the same input does NOT re-call the LLM" is presented as a property but is actually a policy with no enforcement principle backing it — meaning the *cache hit* is the load-bearing promise, not the shape stability.
- **Why this is dangerous**: Their fix bounds *what may differ across runs of the assembled function*; mine bounds *whether the cache is consulted on re-run at all*. These are different properties. Two runs of the same conversus.yml could produce identical *shape* (their bound is satisfied) yet still re-call the LLM (my concern is unaddressed) if the cache is invalidated for any reason. If wording-precision's text lands without my caching-enforcement clarification, a future implementation could cite XVI compliance while still re-invoking the LLM on every run.
- **Resolution**: Both bounds are needed and they nest cleanly: "(a) the LLM MUST NOT be re-invoked for parameter resolution within a single deliberation run; (b) cross-run variance in resolved parameter *values* is acceptable; (c) cross-run variance in the assembled objective function's *shape* is prohibited." Clauses (a) and (b)+(c) operate at different scopes and do not collide.
- **Confidence**: High. The two recommendations are addressing genuinely different failure modes; merging them is straightforward.

### 3. "Per deliberation run" definition vs the run/deliberation terminology drift wording-precision flagged in their internal-contradiction check

- **Their claim**: wording-precision Recommendation #2 (P1) defines "deliberation run" as "a single invocation of the run engine producing one output directory; retries within an invocation are part of the same run, separate `/conversus run` invocations are different runs" (review.md L60). Their internal-contradiction check (L121-122) also flags that lines 463 and 466 use "deliberation" and "deliberation run" interchangeably and recommends consolidating.
- **My claim**: My Missed Opportunity on Principle III (review.md L28) raises the *adjacent* question of what happens when a deliberation is *re-run after a pipeline implementation change* — i.e., across versions of conversus, not across invocations of the same version.
- **Why this is dangerous**: wording-precision's definition only addresses within-version run identity. If the constitution adopts their definition verbatim, a re-run after a `conversus` upgrade is *unambiguously a separate run* (different invocation, different output directory) — which means cross-version cache reuse is implicitly prohibited. If a future implementation depends on cross-version cache reuse (e.g., to preserve user pinning across point upgrades), it would be in silent violation. My Principle III concern surfaces this; their definition foreclosures it.
- **Resolution**: Adopt their definition (it is the right one for the within-version case) and add a forward-pointing sentence: "Cross-version cache reuse is out of scope of this principle; if a future spec requires version-stable pinning, it must extend Principle III." This preserves their precision while leaving the III interaction explicit instead of silently foreclosed.
- **Confidence**: Medium-high. The clash is real but only matters if cross-version reuse is ever needed, which is not currently specified.

---

## Tensions

### 1. Normative grammar (theirs) vs cross-reference density (mine)

- **Their claim**: Most of wording-precision's recommendations (#1, #4, #6, #7, #9, #10) tighten *the prose inside XVI itself* — converting "are pinned" → "MUST be pinned", "claims" → "requires", naming agents, defining terms. Their model is: XVI must be self-contained and mechanically checkable.
- **My claim**: Most of my recommendations add *cross-references to other principles* — XI for SSOT, XXIV for safety-critical defense-in-depth, V for observability, II for stable interfaces. My model is: XVI is part of a network and should make its dependencies explicit.
- **Tension**: Both are valid, but if both are adopted in full, XVI grows considerably. wording-precision adds normative verbs and inline definitions; I add cross-reference parentheticals. The result could double the length of the principle's first bullet and dilute readability — exactly the kind of "paragraphs of caveats" Principle X (L295) warns against.
- **Coordination**: Layer the fixes — wording-precision's MUSTs and definitions land in the bullet body, my cross-references land in a single consolidated parenthetical at the end of the bullet ("(Principles VII, XI, XXIV apply; see Clarification (v2.3.2) below)"). This keeps the body lean while preserving cross-principle visibility.
- **Confidence**: Medium. There is no hard contradiction; this is a co-authoring problem.

### 2. "Claims" → "requires" (theirs) vs my framing of the same passage as a *unilateral redefinition*

- **Their claim**: wording-precision Recommendation #4 (P2) treats "Principle XVI claims" (constitution L491) as a soft-language defect and prescribes substituting "requires" (review.md L70-72).
- **My claim**: My Off-Base #2 (review.md L35) reads the same passage differently — not as soft language about XVI's *own* obligations, but as a *narrowing of VII* that VII has not been amended to acknowledge. My fix is to amend VII or add a carve-out sentence; theirs is to swap the verb.
- **Tension**: Their fix makes XVI's self-claim more normative but does not address the VII coherence problem. Mine addresses the VII coherence problem but does not improve XVI's self-claim. *Both fixes are needed and neither subsumes the other* — but a reader could mistake them as alternatives.
- **Coordination**: Apply both. Replace "claims" with "requires" *and* add the carve-out: "Principle XVI requires within-run determinism for the assembled objective function and cross-run reproducibility once parameters are pinned. This carves an explicit exception to Principle VII's unconditional 'structurally identical output' (L162-163): the assembled objective function is the determinism boundary, not the LLM-resolved parameter values that feed into it."
- **Confidence**: High. The two fixes are complementary; only the framing makes them look like alternatives.

### 3. Stage 2 disambiguation (theirs) vs observability obligation (mine)

- **Their claim**: wording-precision Recommendation #7 (P2) splits stage 2 into question-generation and answer-extraction substeps (review.md L88-91), each stochastic and pinned together.
- **My claim**: My Missed Opportunity on Principle V (review.md L26) prescribes a phase report line for the stochastic step: "parameters resolved: 7 pinned (3 from cache, 4 newly resolved)."
- **Tension**: If their disambiguation lands, the V observability line needs to report on *both* substeps to be honest ("7 questions generated, 7 answers extracted, 7 pinned"). If only one of the two recommendations lands, the observability shape doesn't match the principle's stated stage structure.
- **Coordination**: Treat them as joint or neither. Recommended joint phrasing: "Stage 2 emits a phase report line per Principle V: '{N} gap identifiers resolved ({K} from cache, {N-K} newly resolved across question generation and answer extraction).'" This satisfies both recommendations with a single sentence.
- **Confidence**: Medium. The tension is small but real; the joint fix is cheap.

### 4. Pinning agent (theirs) vs "no ambient state" reconciliation (mine)

- **Their claim**: wording-precision Recommendation #10 (P3) names an agent for the pinning operation: "The run orchestrator MUST pin resolved parameter values..." (review.md L106-108).
- **My claim**: My Missed Opportunity on Principle VII line 167 (review.md L23) flags that the pinned-parameter cache *is* persisted state and needs to be distinguished from the "ambient state" VII prohibits.
- **Tension**: Naming the orchestrator as the pinning agent makes the cache *attributable*, which is a precondition for distinguishing it from ambient state. But neither review individually closes the loop. A reader of theirs alone might think "orchestrator pins, done" without realizing they have just created a piece of persistent state that needs to be sanctioned by VII; a reader of mine alone might think "the cache is sanctioned persistence" without knowing who owns it.
- **Coordination**: "The run orchestrator MUST pin resolved parameter values (a sanctioned form of explicit, keyed persistence as distinguished from the ambient state Principle VII prohibits)."
- **Confidence**: Medium-high. Both fixes are individually weak and jointly sufficient.

### 5. Spec-FR citation (theirs) vs my XXIV cross-reference for enforcement

- **Their claim**: wording-precision Recommendation #8 (P2) prescribes citing a specific spec FR or contract test for the pinning behavior (review.md L93-97), so the descriptive claim anchors to a verifiable artifact.
- **My claim**: My Missed Opportunity on Principle XXIV (review.md L29) prescribes cross-referencing XXIV (Safety-Critical Defense-in-Depth) for the test obligation, since re-resolution mid-run is exactly the silent-drift failure mode XXIV exists to catch with "Contract test reproducing the failure scenario" (constitution L730-733).
- **Tension**: They want a *spec citation*; I want a *constitutional cross-reference*. Both point at the same underlying need (a test that locks the behavior in) but at different abstraction levels. If only theirs lands, the test obligation is anchored to a spec but not to a constitutional principle that survives the spec being closed. If only mine lands, the test obligation has constitutional weight but no concrete pointer.
- **Coordination**: Apply both — "Pinning behavior is verified by a contract test per Principle XXIV (specifically spec 013 FR-{N} / test {path})." This gives the principle both teeth and a pointer.
- **Confidence**: High. They are non-rival and address adjacent needs.

---

## Safe Agreements

### 1. The VII ↔ XVI determinism contradiction is the single largest defect

- **Their claim**: wording-precision Off-Base #2 (review.md L45) states "'Cross-run variance is acceptable' (L467) appears to contradict Principle VII directly. VII at L162-163 says 'Given the same inputs, conversus MUST produce structurally identical output.' XVI now says cross-run variance in parameter values is acceptable... This is a real internal contradiction that the v2.3.2 amendment was meant to resolve and only partly does." Their P1 Recommendation #3 prescribes an explicit carve-out sentence.
- **My claim**: My Executive Summary (review.md L7) and Off-Base #2 (L35) reach the same conclusion: "VII as written (lines 161-175) makes no such conditional claim... XVI is *narrowing* VII without VII being amended to acknowledge the narrowing. The parenthetical reads like a reference but is functionally a unilateral redefinition." My Recommendation #1 prescribes scoping VII.
- **Agreement**: Both reviews independently identify the same defect, both rate it P1, and both prescribe an explicit carve-out / scope-narrowing sentence. The only difference is direction: wording-precision prefers amending XVI's clarification; I prefer amending VII *or* adding the carve-out in XVI's clarification. Either lands the same fix.
- **Confidence**: Very high. Two independent reviewers landing on the same load-bearing flaw with the same severity is itself evidence the flaw is real.

### 2. Pinning is descriptive prose, not a normative obligation

- **Their claim**: wording-precision Recommendation #1 (P1, the most important per their executive summary) — "Promote pinning from description to obligation" (review.md L51-55).
- **My claim**: My Off-Base #1 (review.md L34) — "XVI's wording presents 'cached values are reused' as a property when it is actually a policy that has no enforcement principle backing it elsewhere in the document."
- **Agreement**: We both flag that the pinning behavior is asserted as if it were a fact. wording-precision's fix is intra-principle (add MUSTs to XVI); mine is inter-principle (cross-reference XI for SSOT enforcement). Both fixes can land together: MUSTs make the obligation local; the XI cross-reference makes it part of the broader SSOT discipline. The combination is stronger than either alone.
- **Confidence**: Very high.

### 3. The v2.3.2 amendment correctly inverts the discipline ("pin the output, don't make the LLM deterministic")

- **Their claim**: wording-precision Alignment bullet (review.md L19) — "Explicit non-claim about LLM determinism (L493-495): 'It does NOT claim the LLM gap-filling step itself is deterministic' pre-empts the most likely future misreading. Negative scoping ('we do not claim X') is rare in this constitution and is exactly the right tool here."
- **My claim**: My Executive Summary (review.md L9) — "The clarification block at lines 491-498 is the strongest part of the amendment from a cross-principle perspective: it scopes the determinism claim, names the prohibited future change... and inverts the discipline from 'make the LLM deterministic' to 'pin and cache its output.'"
- **Agreement**: Both reviews single out the determinism-scope clarification as the strongest part of the amendment. Theirs praises the *negative scoping* as a precision win; mine praises the *inversion of discipline* as a coherence win. Same passage, complementary reads.
- **Confidence**: Very high. This is a stable foundation to build the remaining fixes on top of.

### 4. The falsification clause is unusually concrete for a constitution

- **Their claim**: wording-precision Alignment bullet (review.md L11) — "Falsification clause is concrete (L496-498): 'A future PR that re-resolves parameters mid-deliberation, or that lets parameter values drift during a single optimization run, violates this principle.' This sentence is unusually precise for a constitution — it names two specific code behaviors that constitute violation, which a reviewer can mechanically check against."
- **My claim**: My Missed Opportunity on Principle XXIV (review.md L29) implicitly endorses the falsification clause's concreteness by recommending it be linked to XXIV's contract-test requirement: "the Clarification block (lines 491-498) names the prohibition... but does not designate which test layer enforces it."
- **Agreement**: Both reviews recognize the falsification clause as a precision asset; the only delta is whether to leave it standalone (theirs) or attach it to XXIV's test-layer requirement (mine). These are not rival readings — adding the XXIV link strengthens the clause without weakening it.
- **Confidence**: High.

---

## Summary

The two reviews are highly complementary — wording-precision tightens XVI's normative grammar; my review wires XVI into the constitutional network. The single biggest defect (VII ↔ XVI cross-run determinism contradiction) is identified by both reviews, rated P1 by both, and resolvable with a single carve-out sentence. The remaining tensions are co-authoring problems, not substantive disagreements: most can be resolved by composing both fixes rather than choosing between them. The three "dangerous contradictions" identified above are places where adopting only one review's prescription would leave a gap the other review's prescription would close — coordination, not arbitration, is the right disposition.
