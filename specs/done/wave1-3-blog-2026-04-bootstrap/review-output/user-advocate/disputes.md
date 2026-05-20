# Remaining Disputes: User Advocate Perspective

**Date**: 2026-04-03
**Basis**: Revised reviews from code-verifier, user-advocate, and editor

---

## Resolved Items (no remaining dispute)

The following items reached consensus across all three reviewers and are not listed below:

- **P1-3 entry point inconsistency**: CLOSED. All three agree no inconsistency exists in the current code.
- **Two-track promotion strategy**: All three agree Post 05 goes to LinkedIn first, Post 04 to HN/Python communities second.
- **"43 specs" count**: All three agree this is P2, not P1. Verify at publication time.
- **Free/paid framing tension**: All three agree this is minor (P3), compatible framings, not contradictions.

---

## Dispute 1: Entry Point Bug -- Does a Committed-State Fix Block Publishing?

**What**: The editor's revision (Issue 3.0) lists the `core.toml` entry point fix as P1 and states "the committed state is broken" and "this fix must be committed before any wheel is published." The code-verifier's revision says P1-3 is CLOSED with no action required because the working copy is correct. The user-advocate's revision marks the entry point as closed.

**User-advocate position**: CLOSED. The code-verifier confirmed both files now read `engine.cli:cli`. The fix exists. Committing the working copy is a housekeeping step, not a publishing blocker. The blog does not reference `core.toml` internals.

**Editor position**: P1 blocker. The committed state has `engine.cli:main`, which is broken. The fix must be committed before a wheel is published.

**Code-verifier position**: CLOSED. No inconsistency exists in the current code. The fix is present.

**Blocks publishing?** No. All three agree the fix exists in the working copy. The editor is right that the fix must be committed, but committing an already-written one-line change is a trivial prerequisite, not a dispute about what needs to change. This is a sequencing detail, not a content disagreement.

---

## Dispute 2: "All 8 Modes" Claim -- Blog Clarification vs CLI Extension

**What**: The blog says "all 8 modes" ship with the free tier. The `decide` CLI command only accepts 4 modes. All 8 are available via `conversus run` with a config file.

**User-advocate position**: HIGH severity. This is a first-run failure. A new user reads "all 8 modes," tries `conversus decide --mode negotiation`, gets a Click error. The blog must either clarify the distinction or the CLI must be extended before publication. Preference: extend the CLI so the claim is true at every surface, not just the engine level.

**Editor position**: P2. Add one sentence: "All 8 modes are available via config files; the `decide` CLI command supports the original four for quick ad-hoc use." The code-verifier confirms this is a deliberate design choice, not an oversight, so the blog text should be fixed rather than the CLI.

**Code-verifier position**: P2. The design is intentional (both `decide` and `linter/validate.py` restrict to 4 modes). The blog's claim is accurate for the engine but inaccurate for the CLI experience. Recommends a one-sentence clarification.

**Blocks publishing?** Yes, but the fix is small. All three agree the gap exists and must be addressed. The dispute is whether to fix the blog text (editor and code-verifier) or fix the CLI (user-advocate preference). Minimum viable fix: one clarifying sentence in the blog. The CLI extension is a separate product decision that should not block the blog.

---

## Dispute 3: Game-Form Table -- Trim to 3-4 Rows vs Annotate All 8

**What**: Post 05's 8-row game-form table presents equilibrium concepts (Bayesian Nash, Core stability, Envy-freeness, Incentive compatibility) without definitions.

**User-advocate position**: Trim to 4 rows (cooperative, winner-take-all, prisoner's dilemma, negotiation). Link the full table as a reference page. This is P1 -- it is a comprehension barrier for the target audience.

**Editor position**: P1. Either (a) trim to 3-4 rows with a link to a reference page, or (b) add a "when to use" column with plain-language descriptions. Prefers option (a).

**Code-verifier position**: Acknowledges the table is "accurate but not reader-ready." Does not assign its own priority but accepts that the editorial question is real. Notes the terms are all correctly used.

**Blocks publishing?** The editor and user-advocate both classify this as P1. The code-verifier does not object. The remaining dispute is minor: exactly how many rows to keep (3 vs 4) and which modes to feature. This is an editorial judgment call, not a substantive disagreement. Consensus exists that the table must be reduced or annotated.

---

## Dispute 4: PyPI Availability -- How Prominently to Flag It

**What**: `pip install conversus` appears repeatedly in both posts as if it works today. Post 04's closing paragraph qualifies this ("packages are locally buildable; PyPI publication is a separate step"), but the qualification is easy to miss.

**User-advocate position**: CRITICAL. If `pip install conversus` returns a 404, the blog's central promise is broken. This must be verified before publication. If PyPI is not live, the blog framing must change fundamentally -- not just add a disclaimer.

**Editor position**: P1. Add a callout box or bold note near the top of Post 04 after the fold stating the current status. Alternatively, reframe from "is a real thing" to "is now buildable."

**Code-verifier position**: Notes the qualification exists in Post 04's closing but does not assign priority. Flags that the "trust gap runs in both directions."

**Blocks publishing?** Yes. All three agree this must be addressed. The dispute is about degree: the editor wants a visible disclaimer or reframe; the user-advocate wants a more fundamental framing change if PyPI is not live. Resolution depends on whether PyPI publication happens before blog publication. If it does, the dispute is moot. If it does not, the editor's "reframe to buildable" is the minimum fix; the user-advocate would prefer stronger language.

---

## Dispute 5: "Enterprise-Grade" Language -- Cut vs Review

**What**: Posts 04-05 use "enterprise-grade" and marketing-register language in closing paragraphs. Posts 01-03 stay in technical register throughout.

**User-advocate position**: Cut "enterprise-grade" everywhere. The marketing register causes readers to mentally reclassify the post from "useful engineering content" to "vendor blog." This reclassification is sticky and colors how they read everything.

**Editor position**: P1 (upgraded from P2 based on user-advocate argument). Cut "enterprise-grade" everywhere. Revise closing paragraphs of both posts to stay in technical register.

**Code-verifier position**: No position stated. This is outside the code-verifier's scope (style, not factual accuracy).

**Blocks publishing?** The editor says yes (P1). The user-advocate says yes. No dissent from the code-verifier. This is effectively resolved -- consensus to cut. Not a live dispute.

---

## Dispute 6: Post 05 Explicit CTA -- Required or Optional

**What**: Post 05 ends with an implicit call to action ("Build the scoring function. Measure equilibrium quality. Track convergence.") but never says `pip install conversus` or links to the quickstart.

**User-advocate position**: This is the "highest-ROI single change across both posts." One sentence converts a convinced reader into someone who tries the product.

**Editor position**: P1. Add a closing line: "conversus is open source. `pip install conversus` gets you the deliberation engine. `pip install conversus-solvers` adds the scoring layer. [Quickstart guide link]."

**Code-verifier position**: No position stated. Outside scope.

**Blocks publishing?** The editor says yes (P1). The user-advocate strongly agrees. No dissent. This is effectively resolved -- consensus to add CTA. Not a live dispute.

---

## Dispute 7: README Gaps -- Addressed or Deferred

**What**: The README has internal inconsistencies ("four competition modes" on line 5 vs 8 modes listed on line 13), a generic clone URL, and no `pip install` path. The 12 doc fix recommendations from the synthesis do not cover the README.

**User-advocate position**: Medium severity. Should ship alongside P2 fixes. The README is the first thing a GitHub visitor sees.

**Editor position**: Not mentioned in the editor's revision. The editor does not address README gaps.

**Code-verifier position**: P2. The README deserves at least a P2 doc fix recommendation. Lists four specific issues.

**Blocks publishing?** No. The user-advocate and code-verifier agree it is P2/medium, not a blocker. The editor's silence is not dissent -- it is a gap in coverage. The dispute is whether to add a README doc fix to the existing 12 recommendations. Consensus leans toward yes at P2.

---

## Dispute 8: Jargon Glossary -- Inline Definitions vs Glossary Box vs Table Reduction

**What**: Eleven terms across both posts are used without sufficient explanation (Nash equilibrium, ZOPA, payoff function, MCP server, etc.).

**User-advocate position**: The jargon is a systemic concern. The two-track promotion strategy mitigates it for Post 04 (engineering audience expects jargon) but not for Post 05 (LinkedIn audience does not). MCP must be glossed at least once.

**Editor position**: P2 (Issue 9.2). Add inline definitions or a brief glossary box for Nash equilibrium, ZOPA, and payoff function at first use. Three sentences would widen the funnel meaningfully.

**Code-verifier position**: Confirms all terms are correctly used. Notes the issue is "pedagogical, not factual."

**Blocks publishing?** No -- both the user-advocate and editor classify this as P2, not P1. The dispute is minor: the user-advocate wants broader coverage (eleven terms), the editor proposes three priority terms. The minimum viable fix is the editor's three inline definitions plus one MCP gloss. Not a blocker but should be addressed.

---

## Summary: Live Disputes Requiring a Decision

| # | Dispute | Severity | Decision needed |
|---|---------|----------|-----------------|
| 2 | "All 8 modes" -- fix blog text or extend CLI? | High | Blog clarification is the minimum fix. CLI extension is a separate product decision. |
| 4 | PyPI availability -- disclaimer, reframe, or publish to PyPI first? | Critical | Depends on whether PyPI publication precedes blog publication. If not, degree of reframing is the question. |
| 7 | README gaps -- add to doc fix list or defer? | Medium | Lean toward adding as P2. Editor has not weighed in. |
| 8 | Jargon scope -- three priority terms or broader coverage? | Medium | Editor's three-term minimum is pragmatic. MCP gloss should be added regardless. |

All other items have reached effective consensus or are outside the scope of publishing-blocker decisions.
