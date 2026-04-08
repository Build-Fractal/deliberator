# Template Engineer Cross-Review of Game Theorist

## Review of Game Theorist's Round 1 Position

### Agreement Points

1. **GT-R1-01 (Negotiation bayesian mapping)**: Agree that the Stackelberg aspect is procedurally captured by the engine's phase structure. The template engineer's review confirmed the negotiation templates implement sequential offer/counter-offer through Phases 1-3. The formal mapping omission is a documentation gap, not a functional gap.

2. **GT-R1-02 (Envy-freeness in fair-division)**: Agree that the template correctly tests both envy-freeness and Shapley fairness. From a template perspective, the Envy-Free Analysis section is well-structured and the Valuation Matrix provides the right data for the check.

3. **Redundancy analysis**: Agree that no modes are redundant. Each mode produces structurally distinct template output — different section headings, different deliverables, different phase terminology.

### Challenges

1. **GT-R1-03 (keyword "settle" overlap)**: The game theorist flags "settle" as a potential false positive between negotiation and selection. From a template engineering perspective, this is a **low-risk concern**. The keyword classifier uses match count, so a selection-oriented problem text would have many more selection keywords than a single "settle" match. However, if this is a real concern, the fix is trivial: change `settle` to `settle\s+(?:on\s+terms|the\s+dispute|a\s+deal)` to require negotiation context. The current regex is defensible.

2. **GT-R1-04 ("ration" matching "rational")**: This is a **valid and actionable finding**. The template engineer agrees this is a bug. The regex `ration` will match "rational" (via substring) because the pattern does not enforce word boundaries. In a mechanism design problem text that discusses "rational agents" and also mentions "budget allocation," the "ration" match could push the classification toward RESOURCE_ALLOCATION even though "rational" is a mechanism design term. Recommend `\bration(?:ing|ed)?\b` to require full word match.

3. **GT-R1-05 (resource-allocation vs. fair-division user confusion)**: Agree this is a usability concern. From a template perspective, the two modes produce very different output (allocation tables with Shapley scores vs. envy-free matrices with proportionality checks), so the downstream impact of misclassification would be visible. The `/conversus mode` command should include a disambiguation prompt: "Does each party value items differently, or are you distributing objective quantities?"

4. **GT-R1-06 (Missing voting/social choice mode)**: **Disagree that this is a gap worth flagging.** The current scope is expanding from 4 to 8 modes. Adding a 9th mode for voting would require a new game form (social choice functions are not well-represented by the existing 10 game forms in `schema/game-forms/`). The winner-take-all mode with ranked agents can approximate committee voting. This is a future enhancement, not a gap in spec 028.

### Template Engineering Observations on Game Theory Claims

The game theorist did not review the template structural quality. From my domain: the mode-to-form mappings are CONSUMED by templates at synthesis time (the `{MODE}` variable is injected but the form mapping determines which solver runs). The game theorist's analysis of the mappings is necessary but not sufficient — the real test is whether the synthesis templates produce output that is CONSISTENT with the declared game form. For example:

- The resource-allocation synthesis requires a Shapley Value Assessment. Shapley values ARE the coalitional game form's solution concept. **Consistent.**
- The fair-division synthesis requires Envy-Free Analysis. Envy-freeness is a coalitional fairness criterion. **Consistent.**
- The mechanism-design synthesis requires a Property Assessment Matrix testing incentive compatibility. Incentive compatibility IS the mechanism design game form's central property. **Consistent.**
- The negotiation synthesis requires ZOPA Analysis. ZOPA is a negotiation concept but not formally a Bayesian game concept. The Bayesian connection is that agents have hidden types (preferences), and the ZOPA emerges from type inference. **Consistent but indirect.**

### Verdict

The game theorist's review is **sound** on the formal mappings but **incomplete** on the template-form consistency analysis. The "ration" keyword bug (GT-R1-04) is the most actionable finding. The voting/social choice gap (GT-R1-06) is out of scope for spec 028.
