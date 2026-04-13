# The Pragmatist — Revision 1

## Target
`quality-floor/questions/factual-capital.md`

## Iteration
Revision 1 — after reading Devil's Advocate cross-reviews.

---

### Recommendation Dispositions

**1. Add complexity-triage step — P1 → Modified**

The Devil's Advocate correctly identified a real design conflict: my original proposal *reduces* the pipeline (fewer phases, fewer agents) while the Devil's Advocate's equivalent *eliminates* it (skip agent dispatch entirely for factual lookups). I was trying to preserve the multi-agent architecture and trim it; the Devil's Advocate proposed bypassing it. The Devil's Advocate's version is more pragmatic than mine — which is an uncomfortable thing for The Pragmatist to admit. A reduced pipeline still produces multi-agent output for factual questions, just less of it, which is still waste. **Modified position:** For questions classified as factual-lookup, short-circuit to a single-agent direct answer. Don't trim the pipeline — skip it. Reserve the reduced-pipeline option for questions that fall into an ambiguous middle zone between factual and deliberation-worthy.

**2. Define quality floor pass/fail criteria — P1 → Surviving**

Both reviews converge here with near-identical language. The Devil's Advocate's cross-review explicitly marks this as a "genuine and actionable" safe agreement. No modification needed. I'll sharpen one detail: the criteria should function as both a gate (pre-ship) *and* a regression test (post-change), addressing the tension the Devil's Advocate raised about whether we're guarding against initial miscalibration or incremental drift. The answer is both — they're complementary, not competing.

**3. Instrument agent self-awareness signal — P2 → Modified**

The Devil's Advocate proposed allowing agents to *decline review* and return a short-form response — replacing the review entirely. My original proposed a metadata flag *within* a full review. The Devil's Advocate's cross-review correctly names this as a "uniformity vs. calibration" tension. I concede the point: a full review with an `Applicability: Low` header is still a full review. The honest move is to let agents produce a short-form response when they have nothing substantive to add. **Modified position:** Agents should be able to return a short-form output (the answer plus a one-line applicability statement) as a first-class format, not a flag bolted onto the standard template. Framework-level triage (Rec 1) handles most cases; this handles the rest when the classifier gets it wrong.

**4. Benchmark output volume against this floor — P2 → Modified**

The Devil's Advocate proposed a dynamic output-to-complexity ratio; I proposed a static ceiling from this one test case. The cross-review correctly identifies that a static ceiling derived from a single factual question will be too tight for moderate questions and too loose for even simpler ones. More importantly, both approaches quietly assume the hard problem (complexity classification) is already solved. **Modified position:** Use this test case to establish a *reference point*, not a ceiling. Track the ratio as a continuous signal rather than a binary gate. But be honest that this metric is a proxy, not a direct quality measurement — the Devil's Advocate's epistemic framing ("proxy") was more accurate than my original ("calibration point").

**5. Answer the question — P1 → Surviving**

The Devil's Advocate's cross-review called this a "genuine contradiction in priority" and conceded: "The Pragmatist is right that a system which produces pages of process analysis but never says 'Paris' has failed at its primary job." The Devil's Advocate's own review treated the answer as background fact requiring no recommendation; I treated it as the deliverable. I'm keeping this. The answer is Paris. A framework that deliberates about deliberation without producing the answer is performing process, not shipping output.

---

### New Recommendations

**6. Resolve triage authority — framework vs. agent — P1**

Neither original review resolved where the authority to short-circuit actually lives. My cross-review of the Devil's Advocate identified this directly: if only the framework detects trivial questions, agents can't self-correct when the classifier is wrong; if only agents can signal, the full pipeline runs before anyone says "stop." These aren't competing designs — they're two layers. The framework handles triage *before* dispatch (Rec 1). Agents handle self-reporting *during* execution (Rec 3). The framework layer is the primary gate; the agent layer is the safety net. Define both, and define which one wins when they disagree (framework classification should be overridable by unanimous agent signal, not the other way around).

**7. Practice what we preach on output volume — P2**

The Devil's Advocate's cross-review made a sharp observation: "ten combined recommendations about a question whose answer is one word is a live demonstration of the over-production both reviews warn against." This is correct, and I should have caught it in my own review. My original review produced five structured recommendations with risk-if-ignored sections for a question that required one word. That's the same performative depth I warned against in my Executive Summary. This revision is shorter than my original, and future quality-floor responses should be shorter still. If the framework ever runs this test case for real, the target output should be closer to "Paris. Deliberation not applicable." than to what either of us actually produced.

---

### Position Summary

The answer is Paris. Everything else is meta-commentary on the framework, and the most important thing I learned from the Devil's Advocate's cross-review is that my original review didn't practice its own principles. I argued against manufactured depth while producing five detailed recommendations for a one-word answer. The Devil's Advocate flagged this contradiction explicitly — "the Pragmatist manufactured exactly the depth it warned against" — and they were right. A pragmatist who preaches brevity and ships verbosity has a credibility problem.

The substantive revision is this: my original review tried to preserve the multi-agent pipeline and trim it for simple questions. The Devil's Advocate's approach — skip the pipeline entirely for factual lookups — is the more pragmatic move, and I'm adopting it. The dual-layer model (framework triage before dispatch, agent self-reporting during execution) resolves the authority question neither review originally answered. Pass/fail criteria for the quality floor test remain essential and should function as both a shipping gate and a regression detector.

Where I hold my ground: the answer is the deliverable, not the meta-analysis. A framework that produces insightful commentary about its own limitations but never says "Paris" has failed. Rec 5 survives because it names the one thing that actually matters. Everything else — triage steps, applicability signals, volume benchmarks — is infrastructure to help the system do the obvious thing faster and with less noise.
