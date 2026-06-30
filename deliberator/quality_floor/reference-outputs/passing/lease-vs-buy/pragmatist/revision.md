# Pragmatist Revision: Lease vs Buy Decision

**Revision:** 1
**Cross-review source:** Devil's Advocate

---

## Recommendation Dispositions

### Recommendation 1: Require numerical cost model — **Surviving**

Both reviews converge here without friction. The Devil's Advocate cross-review (Safe Agreements §4) calls this "the single highest-impact spec improvement both perspectives endorse." The DA's emphasis on scenario modeling (exit points at 18, 30, 42 months) doesn't contradict the cost table — it extends it. I accept the integration fix from the DA cross-review (Dangerous Contradictions §1): the 5-year cost model should include early-exit columns at multiple horizons rather than existing as a separate analysis. One table, multiple time slices. This is a strictly better version of my original recommendation and doesn't increase scope materially — the exit-cost data informs the same comparison.

**Modified scope:** The cost model should include exit-cost estimates at 24 and 36 months alongside the primary 60-month comparison. This absorbs the DA's early-exit modeling request without creating a parallel analytical track.

### Recommendation 2: Add insurance to decision criteria — **Surviving**

Uncontested. Both reviews independently identified this gap with consistent magnitude estimates ($30-80/month or $200-500/year). The DA cross-review (Safe Agreements §1) confirms this as "a clear, uncontested addition." No modification needed.

### Recommendation 3: Specify state for tax treatment — **Surviving**

Uncontested. Both reviews agree on magnitude ($1,000-2,500), both note "mid-Atlantic" is too vague, both recommend the same fix. The DA cross-review (Safe Agreements §2) calls it "a clean, costless spec improvement." No modification needed.

### Recommendation 4: Reframe flexibility as "early exit cost" — **Modified**

The DA cross-review (Dangerous Contradictions §2) correctly identifies that my reframing and the DA's optionality-pricing lens point in opposite directions if both are adopted without reconciliation. My reframe was designed to deflate leasing's flexibility advantage; the DA's optionality pricing was designed to inflate it. The DA proposes a clean resolution: model early exit costs for *both* lease and purchase at the same time points, then compute the net difference — that net difference *is* the option price.

I accept this. My original framing was directionally biased (it assumed the numbers would favor buying). The right move is to make the criterion structurally neutral — "cost to change course at 24 and 36 months under each structure" — and let the numbers decide. If buying is genuinely more flexible (my position), the model will show it. If leasing's structured exit has value at certain horizons (DA's position), the model will show that too.

**Modified wording:** Reframe "flexibility if circumstances change" as "cost to exit or change vehicles at 24 and 36 months under both lease and purchase structures." This is directionally neutral and subsumes both the exit-cost and optionality-premium framings.

### Recommendation 5: Ask about down payment strategy — **Modified**

The DA cross-review (Dangerous Contradictions §4) proposes modeling three scenarios ($5K on purchase, $5K on lease, $5K invested with $0 down) rather than asking a qualitative question about whether to deploy the money. That's a better approach — it converts a subjective judgment into a computation. My original framing asked the question; the DA's framing answers it.

**Modified approach:** Instead of adding a question to the spec, add a requirement that the cost model show the $0-down variant alongside the $5K-down variant for the purchase scenario, and note that $5K down on a lease is unrecoverable in a total loss. This keeps the down payment within the numerical model rather than making it a standalone question.

### Recommendation 6: Request residual value estimate — **Surviving**

Both reviews agree this is the load-bearing variable (DA cross-review Safe Agreements §3). The DA adds a useful caution about post-2020 market abnormality making historical assumptions unreliable. I accept that the estimate should include a range (e.g., 45-55% retention for Accord/Camry class) rather than a point estimate. This is an enrichment, not a contradiction.

**Minor modification:** Request a residual value estimate with a stated assumption range rather than a single figure. This absorbs the DA's volatility concern without weakening the recommendation.

### Recommendation 7: Remove or downweight maintenance risk — **Modified**

The DA cross-review (Dangerous Contradictions §3) makes a fair point: my original recommendation to *remove* maintenance from the criteria also removes the asker's disclosed reliance on dealer service pricing (they stated they are not mechanically inclined). Dismissing it entirely is too aggressive. The DA's integration fix — keep maintenance in the model but quantify it with real service-interval costs — is the right call.

The DA cross-review also surfaces a subtle point I missed: the warranty-coverage argument for buying only holds if the asker doesn't exit early and lose remaining warranty on a sale. If early exit is in the model (per Recommendation 1's modified scope), maintenance costs at different exit points need to be accounted for.

**Modified approach:** Keep maintenance as a line item in the cost model with estimated service-interval costs for the named vehicles (oil, tires, brakes, scheduled maintenance). Do not treat it as a qualitative differentiator between lease and buy — quantify it. Note that warranty coverage applies equally under both structures for the first 36 months / 36,000 miles.

### Recommendation 8: Add sensitivity check for interest rates — **Surviving**

The DA cross-review (Tensions §5) notes that if the rate sensitivity analysis shows buying wins at every rate, the DA's uncertainty arguments lose force. That's exactly the point — run the numbers and find out. Neither review disputes the value of this check. No modification needed.

---

## New Recommendations

### New Recommendation A: Note CPO as a sidebar option (Priority: P3)

The DA's original review (Off-Base Assumptions §3, Recommendations §3) elevates CPO to P1, arguing it frequently dominates both new-buy and new-lease on TCO. In my cross-review of the DA, I pushed back on this — the asker scoped to new vehicles with current-model MSRPs, and expanding to CPO doubles the analysis. However, the DA's core point has merit: a 2-3 year old Accord/Camry with CPO warranty at $22-26K would likely dominate both options on pure TCO.

The right balance: the spec should note that CPO is worth investigating as an alternative, but not require the answering agent to build a full third cost model. A sentence in the question like "If certified pre-owned materially changes the calculus, note the approximate savings" gives the agent license to mention it without mandating a tripled analysis.

### New Recommendation B: Acknowledge vehicle-sizing risk from children (Priority: P3)

The DA cross-review (Tensions §4) surfaces an implication of the "two young children" detail that I used only as a wear-and-tear cost signal. The DA reads it as a vehicle-sizing risk: the family may outgrow a sedan by year 3, making a lease's structured exit to a three-row vehicle genuinely valuable. I treated the children as a cost to leasing (disposition fees); the DA treats them as a value of leasing (structured upgrade path).

Both readings are legitimate. The spec should acknowledge this explicitly — something like "If family growth makes a vehicle change likely before year 5, how does that affect the lease-vs-buy comparison?" This doesn't change my buy recommendation (selling a purchased car to buy an SUV is straightforward), but it does strengthen the case for including 36-month exit costs in the model, which I've already absorbed into Recommendation 1.

---

## Position Summary

The core recommendation survives: buying is the right call for this asker's profile, and the question should demand a numerical cost model to prove it rather than leaving the answer to principle-based argument. The DA's cross-review didn't challenge the buy conclusion directly — it challenged the *robustness* of the analysis supporting it. That's a legitimate and useful critique. The most important revision is absorbing early-exit modeling into the primary cost table rather than treating the 5-year horizon as a certainty. The asker stated 5 years; I still treat that as the planning baseline. But including exit costs at 24 and 36 months makes the recommendation resilient to life changes rather than fragile to them. This is the DA's strongest contribution, and it makes the analysis strictly better without expanding scope into scenario-planning territory.

What changed: flexibility is now modeled neutrally (cost to exit under both structures) rather than pre-loaded to favor buying. Maintenance stays in the model as a quantified line item rather than being dismissed. The down payment question is resolved through modeling rather than by asking a qualitative question. CPO gets a sidebar mention. Vehicle-sizing risk from children is acknowledged. These are all refinements that improve the spec without changing the direction — they make the buy case more honest by not suppressing the scenarios where leasing has genuine advantages.

What survived without modification: the demand for a numerical cost model (Recommendation 1's core), insurance inclusion (Recommendation 2), state-specific tax treatment (Recommendation 3), residual value estimation (Recommendation 6), and interest rate sensitivity (Recommendation 8). These five items were independently validated by both reviews and constitute the uncontested foundation of the spec improvement. The strongest remaining recommendation is still Recommendation 1 — require a side-by-side cost model with real numbers, now enriched with early-exit columns at 24 and 36 months. Without it, the question invites opinion. With it, the question demands proof.
