# Synthesis Report: Wave 1-3 Blog Posts (04 & 05) Validation

**Synthesizer**: Convergence Agent
**Date**: 2026-04-03
**Inputs**: Revised reviews and disputes from code-verifier, user-advocate, and editor

---

## 1. Convergence Summary

All three agents agree on the following after cross-review and revision:

1. **The posts are technically accurate.** All 8 payoff formulas match source code exactly. Package configs, test counts, free/paid boundaries, AMPL qualifications, and blog categories are all verified correct. No factual errors exist in the blog text.

2. **Technical accuracy is necessary but not sufficient for publication.** The code-verifier's clean scorecard does not mean "ready to publish." The posts must also be accessible to the target audience (user-advocate) and tonally consistent with the existing series (editor).

3. **Post 05 is the right first-contact post.** It names a real problem (agent inconsistency), explains the pattern, and gives actionable advice. Post 04 is an engineering retrospective for a different, mid-funnel audience.

4. **Two-track promotion is the correct strategy.** Post 05 goes to LinkedIn and newsletters first. Post 04 goes to Hacker News and Python communities at least 24 hours later. This was the user-advocate's biggest revision -- the original recommendation to rewrite Post 04 as a product pitch was retracted in favor of the editor's channel-routing approach.

5. **The entry point inconsistency (P1-3) is closed.** Both `pyproject.toml` and `core.toml` declare `engine.cli:cli`. The code-verifier confirmed this; all three agents accept it. The editor notes the fix may still be uncommitted, which is a build prerequisite (one `git commit`), not a content dispute.

6. **Doc fixes P0 and P1 are hard dependencies.** The blog cannot go live while `docs/index.md` says `git clone + uv sync` and the blog says `pip install conversus`. All three agents agree the dependency chain must be respected.

---

## 2. Resolved Items

The following reached full consensus across all three reviewers:

| # | Item | Resolution | Source |
|---|------|------------|--------|
| R1 | Entry point `cli` vs `main` | CLOSED. Both config files declare `engine.cli:cli`. Commit the working-copy state as a housekeeping step before any wheel build. | Code-verifier revision Section 8; all agents concur |
| R2 | Two-track promotion strategy | Post 05 first (LinkedIn, newsletters). Post 04 second (HN, Python communities, dev.to), 24h+ later. No rewrite of Post 04 needed -- add one context sentence only. | Editor revision Issue 6.1; user-advocate revised Section 1 |
| R3 | "Enterprise-grade" language | CUT everywhere. Revise closing paragraphs of both posts to stay in the technical register of Posts 01-03. "No nag screens, no degraded output" makes the same point without the marketing register. | Editor P1 Issue 4.2; user-advocate concurs; code-verifier defers |
| R4 | Post 05 explicit CTA | ADD a closing line after "The Bottom Line": `conversus is open source. pip install conversus gets you the deliberation engine. pip install conversus-solvers adds the scoring layer. [Quickstart guide link].` | Editor P1 Issue 10.1; user-advocate calls it "highest-ROI single change" |
| R5 | "43 specs" count | P2, not P1. Verify at publication time. The number establishes scale, not a precise claim readers depend on. | All three agents agree on downgrade |
| R6 | Free/paid framing tension | P3. Compatible framings between Post 04 (four justifications) and Post 05 (creative vs analytical layers), not contradictions. | Editor Issue 4.1; user-advocate revised Section 6 |
| R7 | Post 04 context sentence | Add one sentence after the feature-inventory opening: "conversus is an open-source framework that runs structured debates between AI agents and scores the results with game theory. The feature list above is what we needed to package." | User-advocate revised Section 1; editor concurs |
| R8 | `RoundFeatures` context | Add one comment or sentence before the worked example: "Conversus extracts these features automatically from agent output during the cross-review phase." | Editor Issue 8.2; user-advocate Section 2 |
| R9 | AMPL claim clarification | Add one sentence: "Today, the AMPL tier optimizes deliberation configuration (rounds, agents, budget). Per-mode game-form templates ship in a future wave." | Editor Issue 2.2 |
| R10 | README gaps | Add to doc fix list as P2. Four issues: "four competition modes" vs 8, generic clone URL, no `pip install` path, possibly broken doc links. | Code-verifier Section 7; user-advocate Section 6 |

---

## 3. Remaining Disputes -- Decisions

### 3A. PyPI Availability

**Dispute**: The user-advocate classifies this as Critical ("the blog's central promise is broken if pip install returns a 404"). The editor classifies it as P1 and recommends reframing the language. The code-verifier notes the qualifying sentence in Post 04's closing is "load-bearing."

**Decision**: Reframe blog language to "locally buildable" until PyPI publication is confirmed. Do not block the blog on PyPI. Specifically:
- In Post 04, add a visible callout after the fold: "Packages are buildable today via `scripts/build-packages.sh`. PyPI publication follows when the distribution channel is ready."
- Replace instances of `pip install conversus` that read as "do this now" with language like "once published, `pip install conversus` is all you need" or "the build produces a wheel you can `pip install` locally."
- The qualifying sentence in Post 04's closing paragraph is insufficient on its own -- the reframing must appear earlier in the post where the `pip install` narrative begins.

This resolves the dispute by satisfying both positions: the blog does not make a promise it cannot keep (user-advocate), and the engineering narrative is preserved (editor). PyPI publication becomes a follow-up task, not a blocker.

### 3B. "All 8 Modes" Claim

**Dispute**: The code-verifier classifies this as P2 (one-sentence fix). The user-advocate classifies it as High (first-run failure, potentially blocking). The editor does not assign a separate issue number.

**Decision**: Add one sentence clarifying: "`decide` supports 4 modes for quick ad-hoc use (cooperative, winner-take-all, prisoners-dilemma, red-blue); all 8 modes are available via `conversus run` with a config file." This goes in Post 05 near the "all 8 modes" claim. Do not extend the CLI -- the 4-mode restriction is a deliberate design choice confirmed by the code-verifier (both `decide` and `linter/validate.py` share it).

### 3C. Game-Form Table

**Dispute**: The editor and user-advocate both classify this as P1 (comprehension barrier). The code-verifier confirms factual accuracy but defers on severity. Minor disagreement on exactly how many rows to keep (3 vs 4).

**Decision**: Trim to 4 rows with a "when to use" column. Keep: cooperative, winner-take-all, prisoners-dilemma, negotiation. These cover the most common use cases and include one from the newer set (negotiation). Add a "When to use" column with plain-language descriptions (e.g., "Agents must share a resource fairly" for cooperative). Link the full 8-mode table as a reference page in the docs. This is P1 for Post 05.

### 3D. Jargon Definitions

**Dispute**: The user-advocate catalogued 11 terms; the editor recommends inline definitions for 3 priority terms. The code-verifier confirms all terms are correctly used and the issue is pedagogical.

**Decision**: Add inline definitions for four terms at first use in Post 05:
- **Nash equilibrium**: "a state where no agent can improve its score by changing strategy alone"
- **ZOPA**: "Zone of Possible Agreement -- the range where both parties can accept a deal"
- **Payoff function**: "a mathematical function that scores agent output and returns a number" (this definition already exists in Post 05 but appears after several unglossed uses -- move it earlier)
- **MCP**: "Model Context Protocol -- the protocol that lets AI assistants call external tools"

The remaining 7 terms from the user-advocate's list are either already glossed (payoff function), removed by the table trim (Pareto optimality, envy-freeness, incentive compatibility), or acceptable for Post 04's engineering audience (Hatch, force-include, importlib.resources).

---

## 4. Final Verdict

**PUBLISH WITH REVISIONS.** No additional review round is needed. The revisions are specific, scoped, and agreed upon. The remaining disputes (3A-3D above) are resolved by the decisions in this synthesis. No reviewer identified a structural problem that requires rethinking either post's narrative.

Both posts earn an A- from the editor. The code-verifier confirms 100% factual accuracy across all 8 payoff formulas, all package configs, and all test counts. The user-advocate rates Post 05 at 7/10 shareability, rising to 9/10 with the four edits in the shipping checklist below.

---

## 5. Shipping Checklist

Ordered by dependency. Items within the same priority tier can be parallelized.

### Pre-publication (must complete before either post goes live)

| # | Task | Priority | Owner | Dependency |
|---|------|----------|-------|------------|
| 1 | Commit `core.toml` entry point fix (`engine.cli:cli`) if uncommitted | P0 | Build | None |
| 2 | Apply P0 doc fixes: `docs/index.md` add `pip install` path, fix org URLs from `clariti-care` to `Build-Fractal`, fix license badge from "proprietary" to "MIT" | P0 | Docs | None |
| 3 | Cut "enterprise-grade" from both posts. Revise closing paragraphs to technical register. | P1 | Editorial | None |
| 4 | Trim Post 05 game-form table to 4 rows (cooperative, winner-take-all, prisoners-dilemma, negotiation) with "when to use" column. Link full table as reference page. | P1 | Editorial | None |
| 5 | Add explicit CTA to Post 05 closing (pip install + quickstart link) | P1 | Editorial | None |
| 6 | Add `decide` mode caveat sentence to Post 05 near "all 8 modes" claim | P1 | Editorial | None |
| 7 | Reframe Post 04 `pip install` language to "locally buildable" with visible callout after fold | P1 | Editorial | None |
| 8 | Add inline definitions for Nash equilibrium, ZOPA, payoff function (move earlier), MCP at first use in Post 05 | P1 | Editorial | None |
| 9 | Add context sentence to Post 04 opening (what conversus is, one sentence) | P1 | Editorial | None |
| 10 | Add `RoundFeatures` context comment/sentence before worked example in Post 05 | P1 | Editorial | None |
| 11 | Apply P1 doc fixes: quickstart add `pip install` path, SDK import path clarification | P1 | Docs | After #2 |

### Post-publication / parallel track

| # | Task | Priority | Owner | Dependency |
|---|------|----------|-------|------------|
| 12 | Apply P2 doc fixes: AMPL clarification sentence, README alignment (4 issues), config reference updates | P2 | Docs | None |
| 13 | Publish to TestPyPI or PyPI (unblocks future removal of "locally buildable" caveat) | P2 | Build | After #1 |
| 14 | Verify "43 specs" count is still accurate | P2 | Editorial | At publication time |
| 15 | Add cross-reference pointers between Posts 03-04-05 | P3 | Editorial | None |
| 16 | Normalize em dash style in Post 04-05 body text | P3 | Editorial | None |

### Publication sequence

| Step | Action | Channel | Timing |
|------|--------|---------|--------|
| A | Publish Post 05 ("Why Your AI Agents Give Different Answers") | LinkedIn, Twitter, AI newsletters | Day 1 |
| B | Publish Post 04 ("From Heuristics to pip install") | Hacker News, Python communities, dev.to | Day 2+ (at least 24h after Post 05) |
| C | Cross-link both posts | Both channels | After both are live |

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

All substantive disputes have been resolved by synthesis decisions in Section 3. The following records the final state for traceability:

1. **PyPI availability** -- RESOLVED. Reframe blog language to "locally buildable." Do not block on PyPI publication. User-advocate wanted PyPI live first; editor wanted reframing; synthesis chose reframing as the pragmatic path.

2. **"All 8 modes" severity** -- RESOLVED. P1 blog clarification (one sentence). Code-verifier and editor said P2; user-advocate said High/blocking. Synthesis classifies as P1 (must fix before publishing) but confirms a one-sentence blog edit is sufficient -- no CLI extension required.

3. **Game-form table row count** -- RESOLVED. 4 rows (cooperative, winner-take-all, prisoners-dilemma, negotiation) with a "when to use" column. Minor disagreement on 3 vs 4 rows resolved in favor of 4 to include one newer mode.

4. **Jargon scope** -- RESOLVED. 4 inline definitions (Nash equilibrium, ZOPA, payoff function, MCP). Editor proposed 3; user-advocate proposed 11; synthesis chose 4, covering the terms that appear in Post 05 before any gloss.

No disputes remain open. The blog is cleared for publication pending completion of the shipping checklist above.
<!-- CONVERSUS:DISPUTES_END -->
