# Disputes Analysis: Code-Verifier Perspective

**Reviewer**: code-verifier
**Date**: 2026-04-03
**Basis**: Revised reviews from code-verifier, user-advocate, and editor

---

## Dispute 1: Entry Point Bug Status (P1-3 / Issue 3.0)

**What**: Whether `core.toml` has a broken entry point (`engine.cli:main` vs `engine.cli:cli`).

**Code-verifier position**: CLOSED. Both `pyproject.toml` and `core.toml` currently declare `engine.cli:cli`. The fix is in the working copy. No inconsistency exists in the current code. No action required on the blog side.

**Editor position**: Acknowledges the fix exists in the working copy but insists the *committed* state is broken and the fix "must be committed before any wheel is published." Lists it as P1 Issue 3.0 -- the top of the must-fix list.

**User-advocate position**: Accepts it is closed per code-verifier confirmation.

**Assessment**: This is not a true dispute -- it is a sequencing disagreement. Both sides agree the fix exists and the current code is correct. The editor is right that the fix must be committed; the code-verifier is right that there is no blog-side action. The resolution is: commit the working-copy fix before publication. No blog text change needed.

**Blocks publishing?** No, as long as the `core.toml` fix is committed before any wheel build. This is a build/release prerequisite, not a blog prerequisite.

---

## Dispute 2: "All 8 Modes" Claim Severity

**What**: Post 05 says "all 8 modes" ship in the free tier. The `decide` CLI command only accepts 4 modes (cooperative, winner-take-all, prisoners-dilemma, red-blue). All 8 are available via `conversus run` with a config file.

**Code-verifier position**: P2 non-blocking. The claim is technically accurate at the engine level. The 4-mode restriction on `decide` is a deliberate design choice (confirmed by matching restriction in `linter/validate.py`). One clarifying sentence in the blog resolves this: "All 8 modes are available via config files; the `decide` CLI command supports the original four for quick ad-hoc use."

**User-advocate position**: High severity, potentially blocking. Calls it "a broken promise at the CLI level" and "a first-run failure caused directly by the blog's claim." Recommends either clarifying the blog or extending the CLI before publication.

**Editor position**: Does not assign a separate issue number to this; it is subsumed into the broader accuracy review. No explicit disagreement with either position.

**Assessment**: The code-verifier's P2 classification is correct. The claim is factually true for the engine; the gap is between the blog's framing and the CLI's surface area. A one-sentence clarification is sufficient. Extending the CLI is disproportionate -- the 4-mode restriction is intentional design, not an oversight. The user-advocate's "blocking" classification overstates the impact: a reader who hits the Click error will see the valid choices listed in the error message itself.

**Blocks publishing?** No. A one-sentence clarification in Post 05 resolves this without code changes.

---

## Dispute 3: "Enterprise-Grade" Language Severity

**What**: Posts 04-05 use "enterprise-grade" and other marketing-register language that diverges from the technical tone of Posts 01-03.

**Code-verifier position**: Not addressed. The code-verifier review does not evaluate tone or marketing language -- this is outside the verification scope.

**Editor position**: P1. Promoted from P2 based on user-advocate's argument. "Enterprise-grade" should be cut everywhere. Closing paragraphs of both posts should be revised to stay in technical register. A reader who mentally reclassifies the post as "vendor marketing" will not reach the CTA.

**User-advocate position**: Agrees with editor. The tonal shift from Posts 01-03 causes readers to discount the content.

**Assessment**: The code-verifier has no position on this -- it is a style/editorial concern, not a factual accuracy concern. The editor and user-advocate are aligned. No dispute exists between those two reviewers.

**Blocks publishing?** The code-verifier defers to the editor and user-advocate on this. Their consensus (P1, must fix) should stand.

---

## Dispute 4: Game-Form Table Treatment

**What**: The 8-row game-form table in Post 05 uses undefined game-theory terms (Bayesian Nash equilibrium, Core stability, Envy-freeness, Incentive compatibility).

**Code-verifier position**: All terms are used correctly. The table is factually accurate. The code-verifier's scope ends at accuracy verification.

**Editor position**: P1. Originally classified as a pacing issue; upgraded to P1 comprehension barrier after user-advocate cross-review. Recommends trimming to 3-4 rows with a link to a full reference page, or adding a plain-language "when to use" column.

**User-advocate position**: Agrees with editor. The table is the point where readers without game-theory background cannot continue.

**Assessment**: No factual dispute. The code-verifier confirms the table is accurate; the editor and user-advocate confirm it is incomprehensible to a significant share of the target audience. These are compatible findings. The recommendation to trim to 3-4 rows is reasonable and does not introduce any factual inaccuracy.

**Blocks publishing?** The code-verifier defers to editor/user-advocate. Their consensus (P1, must fix) should stand.

---

## Dispute 5: PyPI Availability Framing

**What**: Post 04 repeatedly says `pip install conversus` as if it works today. The closing paragraph qualifies this ("PyPI publication is a separate step"), but the qualification is easy to miss.

**Code-verifier position**: Not directly evaluated in the code-verifier review. The code-verifier scope covers whether code matches claims, not whether a distribution channel is live.

**Editor position**: P1 (Issue 2.1). The post implies `pip install` works today; it does not. This is also a "narrative collapse" -- the engineering arc has no payoff if the reader cannot try the thing. Recommends a callout box or reframing to "buildable" rather than "installable."

**User-advocate position**: Flags as Critical. "If `pip install conversus` returns a 404, the blog itself is making a promise it cannot keep." Elevates PyPI availability to "must verify before blog publication."

**Assessment**: The editor and user-advocate are aligned that this is high-severity. The code-verifier has no contrary position. This is not a dispute -- it is consensus.

**Blocks publishing?** Yes. All reviewers who address this agree: either PyPI must be live, or the language must be changed before publication. This is the one issue with genuine blocking consensus.

---

## Dispute 6: Post 05 Missing Explicit CTA

**What**: Post 05 ends with an inspiring closing ("Build the scoring function. Measure equilibrium quality. Track convergence.") but never tells the reader to `pip install conversus` or links to the quickstart.

**Code-verifier position**: Not addressed. Outside verification scope.

**Editor position**: P1 (Issue 10.1). "Highest-ROI single change across both posts." Recommends adding a brief closing line with install commands and quickstart link.

**User-advocate position**: Agrees. "One sentence converts a reader who is already convinced into someone who actually tries the product."

**Assessment**: No dispute. Editor and user-advocate are aligned. The code-verifier has no contrary position.

**Blocks publishing?** Editor and user-advocate both classify as P1. Their consensus should stand.

---

## Dispute 7: README Coverage in Doc Fixes

**What**: The 12 doc fix recommendations from the synthesis do not address `README.md`, which has internal inconsistencies ("four competition modes" on line 5 vs 8 modes listed on line 13), a generic clone URL, and no `pip install` path.

**Code-verifier position**: P2. The README is the first thing a GitHub visitor sees. Its gaps deserve a doc fix recommendation.

**Editor position**: Not mentioned in the editor's revision.

**User-advocate position**: Flags "Address README separately" as a valid gap not caught by other reviews.

**Assessment**: Minor disagreement by omission. The code-verifier and user-advocate want a README fix added to the doc fix list. The editor does not address it. This is likely an oversight, not a disagreement.

**Blocks publishing?** No. P2 -- should be addressed but does not block blog publication.

---

## Dispute 8: Simplification Pattern (Exclusions and Module Counts)

**What**: The blog mentions 2 of 4 `core.toml` exclusion patterns and names 5 of 8 paid modules. Each simplification is individually minor, but the pattern suggests the posts were not reviewed for verifiability.

**Code-verifier position**: P3. Individually minor. Recommends adding "and other premium modules" or listing all four exclusions.

**User-advocate position**: Frames this as a trust-erosion pattern. "Simplifications a reader can easily verify erode trust when the reader finds discrepancies."

**Editor position**: Not explicitly addressed as a standalone concern.

**Assessment**: The user-advocate's trust-erosion framing is valid but does not change the priority. A reader who digs into `core.toml` to verify exclusion patterns is deep enough in the codebase that they will not be confused by a blog simplification. P3 is appropriate.

**Blocks publishing?** No.

---

## Dispute 9: Two-Track Promotion Strategy

**What**: Whether Post 05 should publish first (LinkedIn) and Post 04 second (HN/Python communities), and whether Post 04 needs a product-pitch rewrite.

**Code-verifier position**: No position. Outside verification scope.

**Editor position**: Post 05 first to LinkedIn, Post 04 second to HN. Both posts keep their current structure. Post 04 needs only a single context sentence, not a rewrite.

**User-advocate position**: Originally recommended rewriting Post 04's opening as a product pitch. Revised: accepts editor's two-track strategy. Post 04 is an engineering retrospective that serves a different audience. No rewrite needed; add one context sentence.

**Assessment**: Resolved. The user-advocate retracted the rewrite recommendation and adopted the editor's two-track approach. No remaining dispute.

**Blocks publishing?** No. Consensus reached.

---

## Summary: Remaining Disputes

| # | Dispute | Blocks publishing? | Status |
|---|---------|-------------------|--------|
| 1 | Entry point committed vs working copy | No | Resolved -- commit the fix before wheel build |
| 2 | "All 8 modes" severity (P2 vs blocking) | No | Code-verifier: P2 with one-sentence fix. User-advocate wants higher severity. One sentence resolves it. |
| 3 | "Enterprise-grade" tone | Deferred to editor | Code-verifier has no position; editor/user-advocate consensus is P1 |
| 4 | Game-form table treatment | Deferred to editor | Factually accurate; pedagogically insufficient. Editor/user-advocate consensus is P1 |
| 5 | PyPI availability framing | **Yes** | All reviewers agree: must resolve before publication |
| 6 | Missing CTA in Post 05 | Deferred to editor | Editor/user-advocate consensus is P1 |
| 7 | README in doc fixes | No | P2, likely editor oversight |
| 8 | Simplification pattern severity | No | P3, trust-erosion framing acknowledged but does not change priority |
| 9 | Two-track promotion | No | Resolved -- all reviewers agree |

**Only one issue has genuine blocking consensus: PyPI availability (Dispute 5).** Either `pip install conversus` must resolve on PyPI before publication, or the blog language must be reframed to "buildable" rather than "installable."

**The only active inter-reviewer disagreement is Dispute 2** ("all 8 modes" severity). The code-verifier classifies it P2; the user-advocate pushes for higher. The code-verifier maintains P2: the claim is technically true, the CLI error message itself shows valid choices, and a one-sentence clarification is sufficient.
