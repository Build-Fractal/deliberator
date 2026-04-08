# Remaining Disputes Across Revised Reviews

**Author**: Editor (disputes arbiter)
**Date**: 2026-04-03
**Sources**: Revised reviews from code-verifier, user-advocate, and editor

---

## Dispute 1: Entry Point Bug (Issue 3.0) -- Is It Still a P1 Blocker?

**What**: The editor's revision (Issue 3.0) still classifies `core.toml` entry point as P1, stating "the committed state is broken" and "this fix must be committed before any wheel is published." The code-verifier's revision says P1-3 is CLOSED with no action required, since both files now read `engine.cli:cli` in the working copy.

**Editor's position**: The committed state had `engine.cli:main`. Even though the working copy is fixed, the fix is uncommitted. It remains P1 until the commit lands. The dependency chain (commit fix -> ship doc fixes -> publish blog) still applies.

**Code-verifier's position**: P1-3 is CLOSED. The current code is correct. No inconsistency exists. The original finding was based on a stale reading.

**User-advocate's position**: Agrees with code-verifier -- entry point is closed, no inconsistency exists.

**My position**: The editor is right on process, the code-verifier is right on current state. These are not contradictory -- the fix exists in the working copy but needs to be committed. This is a mechanical step (one `git commit`), not a design dispute. The real question is whether "commit a fix that already exists on disk" belongs on a P1 list or is just a housekeeping task. It does not block publishing decisions or require any editorial changes.

**Blocks publishing?** No. The fix exists. It needs to be committed before a wheel is built, which is a build prerequisite, not a blog-publishing prerequisite. All three reviewers agree the code is correct in the working copy.

---

## Dispute 2: "All 8 Modes" Blog Claim vs 4-Mode `decide` CLI

**What**: Post 05 says "the free tier ships the complete deliberation engine. All 8 modes." The `decide` CLI command accepts only 4 modes (cooperative, winner-take-all, prisoners-dilemma, red-blue). All 8 work via `conversus run` with a config file.

**Code-verifier's position**: The blog is technically true at the engine level but misleading at the CLI surface. Classified as P2 non-blocking. Recommends one clarifying sentence: "All 8 modes are available via config files; the `decide` CLI command supports the original four for quick ad-hoc use."

**User-advocate's position**: This is a "broken promise at the CLI level" and a high-severity finding. A new user who reads "all 8 modes" and tries `conversus decide --mode negotiation` gets an error. Should be resolved before publication -- either clarify the blog or extend the CLI.

**Editor's position**: Not explicitly classified in the editor's revision. The editor's Issue 9.1 (game-form table) and Issue 10.1 (missing CTA) are related but do not directly address the 4/8 mode discrepancy.

**My position**: The code-verifier's one-sentence fix is the right resolution. The claim is not false -- the engine does support all 8 modes. But the user-advocate is right that a reader's first CLI experiment will fail. One clarifying sentence in the blog resolves this without requiring a CLI change. This is P2: should fix before publishing, does not block the editorial process.

**Blocks publishing?** No. One sentence fixes it. But it must be fixed -- publishing "all 8 modes" without qualification would cause a concrete first-run failure.

---

## Dispute 3: Game-Form Table -- Trim to 3-4 Rows (P1) or Annotate (P2)?

**What**: The 8-row game-form table in Post 05 uses terms like "Bayesian Nash equilibrium," "Core stability," "Envy-freeness," and "Incentive compatibility" without definitions.

**Editor's position**: P1. Trim to 3-4 rows covering the most commonly used game forms, with a link to a full reference page. The table is a comprehension barrier for readers without game-theory backgrounds.

**User-advocate's position**: Agrees with trimming to 4 rows (cooperative, winner-take-all, prisoner's dilemma, negotiation). Links the full 8-mode table as a reference page.

**Code-verifier's position**: All terms are correctly used. The issue is pedagogical, not factual. Defers to editorial judgment on severity.

**My position**: The editor and user-advocate agree on the fix (trim to 3-4 rows). The only question is severity. Given the two-track promotion strategy (Post 05 goes to LinkedIn first, targeting practitioners who may not have GT backgrounds), P1 is justified. An incomprehensible table in the middle of the lead acquisition post will cause readers to abandon.

**Blocks publishing?** Yes -- this is the one substantive content edit that all three reviews agree is needed before Post 05 goes to LinkedIn. The disagreement is only on severity (P1 vs P2), not on whether it needs fixing.

---

## Dispute 4: PyPI Availability -- Blog Narrative Problem or Factual Blocker?

**What**: Post 04 repeatedly uses `pip install conversus` as if it works today. The closing paragraph qualifies this ("packages are locally buildable; PyPI publication is a separate step"), but the qualification is easy to miss.

**Editor's position**: P1. The qualification is insufficient. The entire narrative arc of Post 04 collapses if the reader cannot try `pip install conversus`. Recommends a callout box or bold note near the top.

**User-advocate's position**: Elevated to critical. If `pip install conversus` returns a 404, the blog's central promise is broken. Must verify PyPI availability before publication.

**Code-verifier's position**: Does not classify severity directly but notes the blog's qualifying sentence is "load-bearing" and acknowledges the user-advocate's concern about the trust gap running in both directions.

**My position**: The editor and user-advocate are aligned -- this must be addressed. The disagreement is on the fix: the editor recommends reframing the language (say "buildable" instead of implying availability), while the user-advocate implies the package should actually be published to PyPI. The practical answer depends on whether PyPI publication is feasible before blog launch. If yes, publish first. If no, reframe the language per the editor's recommendation. Either way, the current text cannot go live as-is.

**Blocks publishing?** Yes, for Post 04 specifically. Post 05 does not depend on `pip install` being live (its CTA is about the methodology pattern). Post 04's entire arc depends on it.

---

## Dispute 5: "Enterprise-Grade" Language -- P1 or P2?

**What**: Posts 04-05 use "enterprise-grade" and marketing-register language in closing paragraphs that diverges from the technical register of Posts 01-03.

**Editor's position**: Upgraded to P1 (from original P2). Marketing register breaks reader trust. Cut "enterprise-grade" everywhere. Revise closing paragraphs to stay in technical register.

**User-advocate's position**: Implicitly supports the concern through the broader argument that readers who detect marketing language mentally reclassify the entire post as "vendor blog." Does not assign a specific priority to this item.

**Code-verifier's position**: No opinion expressed. Outside scope of code verification.

**My position**: The editor is right to upgrade this. "Enterprise-grade" is the kind of term that triggers an immediate credibility downgrade for the HN/dev-community audiences these posts target. Cutting it costs nothing and removes a real reader-trust risk. P1 is appropriate.

**Blocks publishing?** No -- it is a find-and-replace edit, not a structural change. But it should be treated as required, not optional.

---

## Dispute 6: README Gaps -- Covered by Doc Fixes or Separate Track?

**What**: The README has internal inconsistencies ("four competition modes" on line 5 vs 8 modes listed on line 13), a generic clone URL, and no `pip install` path. The 12 doc fix recommendations in the synthesis do not address the README.

**Code-verifier's position**: The README deserves at least a P2 doc fix recommendation. Flags it as a gap not caught by the other reviews.

**User-advocate's position**: Lists "README contradicts both blog and docs" as medium severity, not addressed in synthesis fixes.

**Editor's position**: Does not mention the README in the revision.

**My position**: The code-verifier and user-advocate are aligned that the README is a gap. The editor's silence is not disagreement -- it is an omission. The README is the first thing a GitHub visitor sees. Its "four competition modes" claim directly contradicts the blog's "all 8 modes" messaging. This should be added as a P2 doc fix recommendation, addressed alongside the existing P2 fixes. It does not need its own priority track.

**Blocks publishing?** No. The README is on GitHub, not on the blog or docs site. A reader arriving from LinkedIn or HN will hit the blog or docs first. But it should be fixed in the same pass as P2 doc fixes to avoid a contradictory first impression for GitHub visitors.

---

## Dispute 7: Post 04 Audience Strategy -- Rewrite or Reroute?

**What**: Post 04 opens with a feature inventory and engineering narrative without explaining what conversus is. A cold reader will not know what the product does.

**User-advocate's original position**: Post 04 needs a product-pitch opening so cold readers can follow along.

**User-advocate's revised position**: Adopted the editor's two-track promotion strategy. Post 04 does NOT need a rewrite. It needs a single context sentence and a different promotion channel (HN/Python communities, not LinkedIn).

**Editor's position**: Post 04 is an engineering retrospective for a mid-funnel audience. Rewriting it as a pitch would weaken it for its natural audience. Route it to the right channel instead.

**Code-verifier's position**: No opinion on audience strategy.

**My position**: This dispute is resolved. The user-advocate adopted the editor's position in the revision. The agreed fix is one context sentence after the opening feature inventory, plus deliberate channel routing (Post 05 first to LinkedIn, Post 04 second to HN). No rewrite needed.

**Blocks publishing?** No. This is resolved.

---

## Summary: What Actually Blocks Publishing

| # | Dispute | Status | Blocks? | Resolution path |
|---|---------|--------|---------|-----------------|
| 1 | Entry point commit | Resolved (all agree fix exists) | No | Commit the working-copy fix |
| 2 | "All 8 modes" vs 4-mode CLI | Minor disagreement on severity | No | One clarifying sentence in Post 05 |
| 3 | Game-form table trim | Agreed on fix, minor severity dispute | Yes (Post 05) | Trim to 3-4 rows, link full table as reference |
| 4 | PyPI availability | Agreed it must be addressed | Yes (Post 04) | Either publish to PyPI first or reframe language |
| 5 | "Enterprise-grade" language | Agreed to cut | No | Find-and-replace edit |
| 6 | README gaps | Agreed but unaddressed in synthesis | No | Add P2 doc fix recommendation |
| 7 | Post 04 audience strategy | Resolved | No | One context sentence + channel routing |

**True blockers**: Only disputes 3 and 4 require substantive work before publishing. Dispute 3 (game-form table) blocks Post 05. Dispute 4 (PyPI availability) blocks Post 04. Everything else is either resolved or requires only minor text edits.
