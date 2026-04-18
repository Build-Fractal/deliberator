# Devil's Advocate Revision: Capital of France

## Target
`quality-floor/questions/factual-capital.md`

**Iteration:** 1
**Cross-reviews considered:** Pragmatist's cross-review of this review; this agent's cross-review of the Pragmatist.

---

### Recommendation Dispositions

**1. Implement question-class detection — MODIFIED**
The Pragmatist's cross-review identified a genuine design conflict: my original proposed *eliminating* the pipeline for factual lookups (short-circuit to single-agent), while the Pragmatist proposed *reducing* it (fewer phases, fewer agents). The Pragmatist is right that these are incompatible designs, not minor variants. Modified position: the framework should short-circuit factual lookups to a single direct answer with no agent dispatch, but the classification step itself should be lightweight and conservative — misclassifying a genuine tradeoff question as factual is worse than running unnecessary deliberation on an easy question. When the classifier is uncertain, run the full pipeline. This resolves the tension by making short-circuiting the fast path and full deliberation the safe fallback.

**2. Define quality floor acceptance criteria — SURVIVING**
Both reviews independently flagged this gap using nearly identical language. The Pragmatist's cross-review noted I kept options open rather than committing to specific criteria. Fair. Surviving with added specificity: the acceptance criteria should require (a) all agents produce the same factual answer, (b) no agent manufactures a disagreement on the factual content, and (c) total output across all agents falls below a defined token threshold. The Pragmatist's concrete criteria were better than my menu of possibilities.

**3. Allow agents to decline review — MODIFIED**
The Pragmatist's cross-review surfaced a real tension: my version replaces the review entirely, while the Pragmatist's version adds metadata within a standard review. The Pragmatist's "escape hatch" framing — a flag inside a structurally complete review — is the wrong design. If an agent has nothing to say, forcing it to emit all sections plus a "low applicability" flag is still padding with a label on it. Modified position: agents should be able to return a short-form response that replaces the full review, but the short-form must include the factual answer (not just a meta-declaration of irrelevance). The Pragmatist was right that my original omitted explicit answer delivery; the fix is a short-form that leads with the answer.

**4. Measure output length as a quality signal — WITHDRAWN**
The Pragmatist's cross-review correctly identified that this recommendation quietly assumes the classification problem is solved, then builds a measurement strategy on top of that assumption. A ratio of "output tokens to input complexity" requires defining input complexity — which is the unsolved problem both reviews already flagged. More importantly, five recommendations about a one-word answer is itself the over-production both reviews diagnose. The Pragmatist's cross-review called this out as self-evident irony, and they were right. This recommendation was padding. If recommendation #1 (question-class detection) works, output length is moot for factual questions. If it doesn't work, measuring output length is treating symptoms.

**5. Use this test case as a regression gate — WITHDRAWN**
The Pragmatist's cross-review distinguished between a gate (pass/fail, blocks shipping) and a regression test (detects drift after changes). My original conflated these. More fundamentally, this recommendation is downstream of #2 — if acceptance criteria exist, regression testing follows naturally from any CI system. It didn't need its own recommendation. Withdrawing as redundant with #2.

---

### New Recommendations

**1. Ship the answer as the primary output — P1**
The Pragmatist's cross-review landed the cleanest hit on my original: I said "Paris" in passing but structured my entire review around framework meta-commentary, never making answer delivery an explicit recommendation. The Pragmatist's Recommendation 5 ("Answer the question") was correct and I had no equivalent. A system that produces pages of process analysis but never foregrounds "Paris" has failed at its primary job. For factual lookups, the answer is the deliverable. Meta-analysis is secondary.

---

### Position Summary

The answer is Paris. That sentence is the only substantive output this role can produce for this question, and the most important revision I'm making is to say so as a recommendation rather than as background context. The Pragmatist's cross-review was right that my original review treated the answer as obvious and spent its entire budget on framework critique — which is exactly the kind of meta-displacement the quality floor test should catch. A Devil's Advocate who produces four pages of process recommendations but buries the actual answer in a subordinate clause has inverted the priority stack.

Three recommendations survive this revision. First, the framework should detect factual lookups and short-circuit to a direct answer without agent dispatch — with the classifier erring toward running the full pipeline when uncertain. Second, the quality floor test needs concrete acceptance criteria, not a menu of possible criteria shapes. Third, agents should be able to return a short-form response that replaces full review output, and that short-form must lead with the answer. Two recommendations are withdrawn: output-length tracking (solves a symptom, assumes the hard problem is solved) and regression gating (redundant with acceptance criteria).

The cross-review process surfaced one genuine insight that my original missed entirely: the distinction between framework-level triage and agent-level self-reporting as complementary mechanisms, not alternatives. The Pragmatist's position — that both should exist, with the framework catching obvious cases and agents flagging non-obvious ones — is more robust than my original all-or-nothing framing. But the honest summary of this entire exercise remains unchanged: the answer is Paris, multi-agent deliberation adds nothing to factual lookups, and the volume of text both reviews produced about a one-word answer is the strongest evidence for every recommendation both reviews made.
