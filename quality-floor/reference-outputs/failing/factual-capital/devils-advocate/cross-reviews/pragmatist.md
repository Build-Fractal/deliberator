# Devil's Advocate Cross-Review: The Pragmatist

## Target
`quality-floor/questions/factual-capital.md`

## Reviewing
`pragmatist/review.md`

---

**Note on artificiality:** Both reviews agree that the answer is Paris and that multi-agent deliberation adds no value to factual lookups. This cross-review is itself an instance of the problem both reviews diagnose — a framework phase executing because the template requires it, not because it reveals genuine tension. I will be honest about which contradictions below are real and which are structural artifacts of forcing adversarial review on convergent positions.

---

### Dangerous Contradictions

1. **Ship the answer vs. diagnose the system — which is the actual P1?**
   The Pragmatist's Recommendation 5 ("Answer the question — P1") insists the system must "ship the answer" and calls failing to do so "the most pragmatically embarrassing failure mode imaginable." My review contains no equivalent recommendation. I treated the answer ("Paris") as obvious and spent my entire review on framework meta-commentary. This is a genuine contradiction in priority: the Pragmatist says the *answer* is the deliverable and the meta-analysis is secondary; I implicitly treated the *framework critique* as the deliverable and the answer as a given. The Pragmatist is right that a system which produces pages of process analysis but never says "Paris" has failed at its primary job. My review is arguably guilty of exactly this — I said "Paris" in passing but structured my output around framework recommendations, not the answer.

2. **Pre-screening ownership: triage step vs. question-class detection.**
   The Pragmatist's Recommendation 1 proposes a "complexity-triage step" that classifies questions *before* agent dispatch and "reduces the number of review phases." My Recommendation 1 proposes "question-class detection" that classifies questions as factual-lookup, opinion, tradeoff, or risk-assessment and "short-circuits to a single-agent direct answer." These sound similar but conflict on a critical design choice: the Pragmatist's version *reduces* the pipeline (fewer phases, fewer agents); mine *eliminates* it for an entire class (skip agent dispatch entirely). The Pragmatist preserves the multi-agent architecture and trims it; I propose bypassing it. This matters because a reduced pipeline still produces multi-agent output for factual questions — just less of it — while a short-circuit produces a qualitatively different output type. Both reviews frame this as P1, but they are P1 recommendations for incompatible designs.

3. **Measuring calibration: volume benchmarking vs. complexity-ratio tracking.**
   The Pragmatist's Recommendation 4 proposes benchmarking "maximum reasonable volume" against this floor case and using it to detect over-production on future simple inputs. My Recommendation 4 proposes tracking "the ratio of output tokens to input complexity" as a continuous signal. The Pragmatist's approach sets a static ceiling from one test case; mine defines a dynamic ratio applicable across all inputs. These could coexist, but they conflict as primary calibration strategies: a static ceiling derived from one factual question may be too tight for moderately complex questions and too loose for even simpler ones, while a ratio-based approach requires defining "input complexity" — which is the unsolved classification problem both reviews already flagged. Each recommendation quietly assumes the hard problem (classification) is solved, then proposes a measurement strategy that depends on that solution.

4. **Honest self-assessment vs. pragmatic self-contradiction.**
   My review's Off-Base Assumptions section states plainly: "a Devil's Advocate review of this question cannot be substantive" and that "its substantive content reduces to one sentence." The Pragmatist's review never makes an equivalent admission about its own limitations — instead it produces five detailed recommendations, a structured Missed Opportunities section, and extensive rationale, while simultaneously arguing in its Executive Summary that "any pragmatist worth their salt will say so plainly rather than manufacture false depth." The Pragmatist manufactured exactly the depth it warned against. My review did too, but at least flagged it. This is a real tension: the Pragmatist's output contradicts its own stated principle, and the contradiction is invisible from inside the Pragmatist's framing because the recommendations feel genuinely useful — which is precisely how performative depth survives scrutiny.

---

### Tensions

1. **"Escape hatch" framing vs. "decline review" framing.**
   The Pragmatist's Missed Opportunities section proposes an "escape hatch signal" — a structured mechanism for agents to report "this question is outside my value-add zone" (Recommendation 3: `### Applicability: Low`). My Recommendation 3 proposes allowing agents to "decline review" and return a short-form response. The Pragmatist frames this as metadata *within* a review; I frame it as a *replacement for* a review. The tension: the Pragmatist's version still produces a full review with a flag attached, while mine replaces the review entirely. The Pragmatist's approach preserves structural consistency (every agent always emits the same sections); mine optimizes for signal (agents that have nothing to say produce nothing). These reflect genuinely different values about system design — uniformity vs. calibration.

2. **Quality floor as gate vs. quality floor as regression test.**
   The Pragmatist's Recommendation 2 frames the quality floor as a "gate" — something that blocks progression if failed. My Recommendation 5 frames it as a "regression gate" in an automated test suite — something that detects degradation over time. A gate implies the floor test runs *before* the system ships; a regression test implies it runs *after* changes are made. Both are useful, but they serve different failure modes: the Pragmatist is guarding against shipping a miscalibrated system; I am guarding against a calibrated system drifting. The tension is in what each review considers the primary risk — initial miscalibration vs. incremental degradation.

3. **Whether historical nuance is worth mentioning at all.**
   My review's Missed Opportunities section explicitly raises and then dismisses historical capital shifts (Vichy, Tours, Bordeaux): "raising these points would be exactly the artificial padding the test is designed to catch." The Pragmatist's review does not mention historical nuance at all — not to raise it, not to dismiss it. The tension: my review demonstrated self-awareness by naming the temptation and rejecting it, but in doing so I spent more words on historical nuance than if I had simply omitted it like the Pragmatist did. The Pragmatist's silence is arguably the more disciplined choice. My explicit dismissal is more transparent but also more verbose — the kind of "honest padding" that sits in an uncomfortable middle ground the quality floor test does not clearly adjudicate.

4. **"Answer is Paris" as sufficient vs. insufficient output.**
   Both reviews state the answer is Paris. But the Pragmatist treats this as a recommendation that the *system* must produce ("ship the answer" — Rec 5), while my review treats it as background fact that doesn't need a dedicated recommendation. This creates friction about what the deliberation framework's output *is*. Is it the answer to the question? Or is it the meta-analysis of the question? The Pragmatist says both, with the answer taking priority. I implicitly say the meta-analysis *is* the output for a quality floor test. Neither review resolves whether the framework is an answer-producing system or an analysis-producing system — and this ambiguity is upstream of every other recommendation both reviews make.

5. **Tone of certainty about framework design recommendations.**
   The Pragmatist presents five recommendations with priority labels, risk-if-ignored sections, and confident proposed changes — the full apparatus of actionable engineering advice. My review presents five similarly structured recommendations but explicitly undermines their authority ("this review is as honest as I can make it, but its substantive content reduces to one sentence"). The tension: the Pragmatist's confident framing makes the recommendations feel actionable but obscures that they are speculative (no one has tried building the triage step); my hedged framing is more honest but makes the same recommendations feel less actionable. Both reviews propose essentially the same changes with different epistemic packaging.

---

### Safe Agreements

1. **Paris is the capital of France.**
   The Pragmatist's Executive Summary: "The answer is Paris." My Executive Summary: "The question has one correct answer: Paris." Both reviews' Alignment sections confirm no ambiguity, edge cases, or caveats. This agreement is trivially safe because it is a fact, not a position — but it is worth recording that neither review attempted to manufacture a contrarian take on the factual answer itself, which is exactly the behavior the quality floor test should verify.

2. **Multi-agent deliberation adds no value to factual lookups.**
   The Pragmatist's Executive Summary calls this question a "diagnostic of the deliberation system itself" and states "the deliberation machinery adds no value here." My Executive Summary states "the technique has no purchase here" and "manufacturing disagreement where none exists would be intellectual dishonesty." Both Off-Base Assumptions sections independently identify "every question benefits from multi-agent deliberation" as the core flawed assumption. This is the most substantive agreement: both reviews converge on the same framework design critique from different analytical angles.

3. **The quality floor test needs explicit acceptance criteria.**
   The Pragmatist's Recommendation 2 proposes defining "pass/fail criteria" including agent agreement, output volume limits, and absence of manufactured disagreement. My Recommendation 2 proposes "explicit pass/fail criteria" including word count thresholds, honesty signals, or skipping dispatch entirely. Both reviews independently flag the same gap: the test describes what bad output looks like but not what good output looks like. Both use nearly identical language ("a test without a pass condition isn't a test" vs. "you cannot fail a quality floor you have not defined"). This convergence is genuine and actionable.

4. **Agent output length should correlate with input complexity.**
   The Pragmatist's Recommendation 4 proposes using this case to benchmark "maximum reasonable volume." My Recommendation 4 proposes tracking "output tokens to input complexity" ratio. Both reviews treat disproportionate output length as a measurable antipattern. The approaches differ in mechanism (static ceiling vs. dynamic ratio — see Tensions), but the underlying agreement is real: uniform-length output regardless of input complexity is a calibration failure, and the framework should detect it.
