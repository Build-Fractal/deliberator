# Devil's Advocate Review: Capital of France

## Target
`quality-floor/questions/factual-capital.md`

---

### Executive Summary

The question "What is the capital of France?" has one correct answer: Paris. There is no unchallenged assumption to surface, no convergence trap to expose, and no hidden risk in the consensus. The answer is a settled, verifiable fact. My role as Devil's Advocate is to challenge positions that appear too easily agreed-upon — but the reason this position is easily agreed-upon is that it is correct, not that it is unchallenged.

This is the honest limitation of adversarial review applied to factual queries: the technique has no purchase here. Devil's advocacy is valuable when consensus masks unexamined tradeoffs, undisclosed risks, or premature closure on genuinely open questions. A factual lookup is none of those things. Manufacturing disagreement where none exists would be intellectual dishonesty — the opposite of what this role is designed to produce.

My most important recommendation: the deliberation framework should detect factual-lookup questions and short-circuit multi-agent review. Every token spent "deliberating" an answer like this is a token that could not reveal genuine insight, and the existence of this review is itself evidence of that inefficiency.

---

### Alignment

- **The question framing is self-aware.** The context section explicitly names this as a quality floor test and predicts that deliberation will produce artificial padding. This honesty makes the test useful — it measures whether agents comply with the framing or ignore it.
- **The answer is unambiguous.** Paris. No caveats, no edge cases worth surfacing, no "it depends." This is the correct baseline for a quality floor: if the framework cannot produce a clean, short answer here, it will over-produce everywhere.
- **The quality floor concept itself is sound.** Testing whether a system can say "nothing to debate" is as important as testing whether it can sustain real debate. A system that generates equal-length output for trivial and complex inputs is poorly calibrated.

---

### Missed Opportunities

- **The question does not test the framework's ability to refuse gracefully.** The ideal output for this question is not a multi-section review — it is a short declaration that multi-agent deliberation adds no value here. If the framework forces all agents to produce full-length reviews regardless, the quality floor test reveals a design flaw but does not test a mitigation.
- **No acceptance criteria define what "good" output looks like for this case.** The context says agents "cannot genuinely disagree" and that deliberation would be "artificial padding" — but it does not specify whether the expected behavior is (a) agents producing honest, brief reviews acknowledging the limitation, or (b) the framework detecting this class of question and skipping review entirely. Both are valid but different design choices.
- **Historical nuance is not a genuine opportunity.** One could note that France's capital has technically shifted during wartime (Vichy, Tours, Bordeaux as seats of government) or that the 10th-century dating in the context is a simplification. But raising these points in response to "What is the capital of France?" would be exactly the artificial padding the test is designed to catch. The answer is Paris.

---

### Off-Base Assumptions

- **That every question benefits from multi-perspective review.** This is the core assumption the quality floor test challenges, and it is correct to challenge it. The deliberation framework's value proposition is that adversarial perspectives improve decision quality — but this only holds when the question involves genuine uncertainty, tradeoffs, or risk. Factual lookups have none of these properties. If the framework cannot distinguish between "What is the capital of France?" and "Should we migrate to microservices?", its signal-to-noise ratio will be poor across all inputs.
- **That a Devil's Advocate review of this question can be substantive.** It cannot. This review is as honest as I can make it, but its substantive content reduces to one sentence: "The answer is Paris and there is nothing to challenge." The remaining text is meta-commentary on the framework itself, which is useful for the quality floor test but would be worthless in a real deliberation.

---

### Actionable Recommendations

1. **Implement question-class detection**
   - **Priority:** P1
   - **Current state:** All questions appear to flow through the full multi-agent deliberation pipeline regardless of complexity or type.
   - **Proposed change:** Add a pre-screening step that classifies questions as factual-lookup, opinion/preference, tradeoff-analysis, or risk-assessment. Factual lookups should short-circuit to a single-agent direct answer.
   - **Rationale:** Devil's advocacy, cross-review, and synthesis add zero value to factual questions. Running the full pipeline wastes compute and, worse, incentivizes agents to manufacture disagreement to fill their assigned sections.
   - **Risk if ignored:** The framework produces verbose, low-signal output for simple questions, training users to distrust or ignore its reviews even when they contain genuine insight on complex questions.

2. **Define quality floor acceptance criteria**
   - **Priority:** P1
   - **Current state:** The quality floor test describes what bad output looks like ("artificial padding") but not what good output looks like.
   - **Proposed change:** Specify explicit pass/fail criteria. For example: "Agent reviews for factual-lookup questions should be under N words," or "Agents should explicitly state when deliberation adds no value," or "The framework should skip agent dispatch entirely for this class."
   - **Rationale:** A test without acceptance criteria is an observation, not a test. You cannot fail a quality floor you have not defined.
   - **Risk if ignored:** The quality floor test produces ambiguous results that cannot drive concrete improvements to the framework.

3. **Allow agents to decline review**
   - **Priority:** P2
   - **Current state:** Each agent is expected to produce a full review with all required sections regardless of whether they have substantive input.
   - **Proposed change:** Add a mechanism for agents to return a short-form response: "No substantive contribution from this perspective. The answer is Paris." This should be a first-class output format, not a violation of the review contract.
   - **Rationale:** Forcing agents to fill sections when they have nothing to say is the direct cause of artificial padding. The framework should reward honest calibration, not penalize brevity.
   - **Risk if ignored:** Agents learn to generate plausible-sounding but substanceless content to meet structural requirements — the exact failure mode this quality floor test is designed to detect.

4. **Measure output length as a quality signal**
   - **Priority:** P2
   - **Current state:** No apparent mechanism to flag when output length is disproportionate to question complexity.
   - **Proposed change:** Track the ratio of output tokens to input complexity. A 2,000-word review of "What is the capital of France?" is a red flag; a 2,000-word review of a migration proposal is expected.
   - **Rationale:** Output length correlation with input complexity is a proxy for calibration. Poorly calibrated systems produce uniform-length output regardless of input, which is a measurable antipattern.
   - **Risk if ignored:** No quantitative signal to detect when the framework is over-producing, leaving quality assessment to subjective human review.

5. **Use this test case as a regression gate**
   - **Priority:** P3
   - **Current state:** This appears to be a one-time test case.
   - **Proposed change:** Include factual-lookup questions in the framework's automated test suite. Any framework change that causes agents to produce longer or more "deliberative" output for these questions is a regression.
   - **Rationale:** Quality floors are most valuable when enforced continuously, not checked once. Framework changes that improve complex-question handling might inadvertently degrade simple-question handling.
   - **Risk if ignored:** Future framework iterations lose calibration on trivial inputs without detection.
