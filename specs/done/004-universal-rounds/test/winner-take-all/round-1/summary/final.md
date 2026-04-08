# Final Judgment: Template-Approach vs. Engine-Approach

**Spec**: 004 — Universal Rounds, Stagnation Detection, and Arbitration
**Competition Mode**: Winner-Take-All
**Judge**: Neutral arbiter

---

### Process Summary

| Metric | Value |
|--------|-------|
| Competitors | 2 (template-approach, engine-approach) |
| Phases completed | 4 (review, cross-review, revision, disputes) |
| Opening advantages claimed (template) | 6 strengths + 4 honest weaknesses |
| Opening advantages claimed (engine) | 6 strengths + 3 honest weaknesses |
| Concessions made by template-approach | 3 (adopted "mode-parameterized" terminology; withdrew "zero engine changes" claim; withdrew "only constitutionally compliant approach" claim) |
| Concessions made by engine-approach | 7 (templates own mode-specific behavior; implementation works; independent reviewability; engine should not grow unboundedly; constitutional argument withdrawn; data-vs-logic distinction acknowledged; concrete deliverables are enhancements to template-first, not a competing architecture) |
| Convergence points reached | 10 (documented in both disputes files) |
| Remaining disputes | 3 from each side (6 total, with significant overlap reducing to ~4 distinct positions) |
| Advantages withdrawn by engine-approach | 1 (Advantage 4: Constitution Principle VI argument) |
| Advantages modified by engine-approach | 4 of 6 |
| Advantages surviving for engine-approach | 1 (Advantage 3: role enforcement) |

---

### Competition Scorecard

| Argument | Phase 1 (Review) | Phase 2 (Cross-Review) | Phase 3 (Revision) | Phase 4 (Disputes) | Final Status |
|----------|-------------------|------------------------|--------------------|--------------------|--------------|
| **Template: "Implementation proves architecture" (CA-1)** | Strong — 4 edits vs. 6 templates | Engine challenged that 4 edits were preconditions, not housekeeping | Template withdrew rhetorical minimization of engine edits; maintained that edits were data-level (removing restrictions + adding table rows), not algorithmic | Not directly disputed further | MODIFIED, surviving. The ratio framing was withdrawn, but the structural argument (data changes, not logic changes) survived intact. |
| **Template: "Templates are the right abstraction" (CA-2)** | Strong — content variation, not orchestration variation | Engine argued two kinds of mode behavior: prompt engineering (templates) vs. orchestration semantics (engine) | Template maintained that engine's "orchestration semantics" per mode are string lookups, not behavioral differences | Not directly contested | SURVIVING. Both sides converged that analytical frameworks belong in templates and that engine mode awareness is parameterized data. |
| **Template: "Independent reviewability" (CA-3)** | Strong — constitution review demonstrated per-template isolation | Engine conceded explicitly (C3) | Unchallenged | Unchallenged | SURVIVING, conceded by opponent. |
| **Template: "Engine stays simple / mode-agnostic" (CA-4)** | Moderate — claimed mode-agnosticism | Engine identified three mode-keyed lookup tables contradicting "mode-agnostic" label | Template withdrew "mode-agnostic," adopted "mode-parameterized." Maintained that data-level awareness does not equal logic-level branching | Template disputes that "mode-parameterized" carries architectural weight beyond naming | MODIFIED. Label changed, but the underlying claim (algorithm is mode-invariant, only data varies) survived. |
| **Template: "Zero engine changes for new modes" (CA-5)** | Moderate — claimed zero orchestration logic changes | Engine empirically falsified with spec 004's own edits | Template withdrew "zero engine changes," refined to "zero engine logic changes + bounded data additions" | Not disputed further | MODIFIED. The imprecise claim was corrected to an accurate one that still supports the template-first thesis. |
| **Template: "Constitutional alignment" (CA-6)** | Strong — cited Principle VIII exclusively | Engine cited Principle VIII's orchestration clause and Principle VI | Template conceded both approaches can claim constitutional compliance; withdrew exclusivity claim | Not disputed further | MODIFIED. Exclusivity withdrawn, but Principle VIII's explicit assignment of mode behavior to templates still favors template-approach. |
| **Template: "Engine-approach is not a competing architecture" (NA-1)** | N/A | Emerged in cross-review | Sharpened — engine's 4 deliverables decompose to naming change + consolidation + validation + concession of template ownership | Engine conceded: "this characterization is largely accurate" | DECISIVE. Engine-approach acknowledged its proposals are enhancements to the template-first architecture, not a replacement. |
| **Template: "FR-001 direction of change" (NA-3)** | N/A | Emerged in cross-review | Sharpened — spec 004 deleted mode-aware validation, moving engine toward mode-agnosticism | Engine conceded in N2: "FR-001 REMOVED engine mode-awareness — the opposite of my thesis" | DECISIVE. Engine-approach acknowledged this moved counter to their thesis. |
| **Engine: "Stagnation detection is engine logic" (Adv 1)** | Strong — Dispute-Parsing Subsystem is engine-level | Template acknowledged as "narrow exception," characterized as data lookup not logic | Engine conceded data-vs-logic distinction: "I concede that calling this mode-specific orchestration logic overreaches" | Engine maintains parameterization IS a form of mode awareness | MODIFIED substantially. Core claim (engine makes termination decisions using mode-specific inputs) survived, but the characterization as "mode-specific logic" was withdrawn. |
| **Engine: "Phase 6 validation is mode-aware" (Adv 2)** | Moderate — four-row heading table in SKILL.md | Template called it "lookup table, not logic" | Engine withdrew claim that existence alone proves mode behavior belongs in engine; maintained it disproves "mode-agnostic" | Subsumed into terminology dispute | MODIFIED. Narrowed to a terminological correction, which template-approach accepted. |
| **Engine: "Role enforcement is engine invariant" (Adv 3)** | Strong — templates cannot reject misconfigured YAML | Template did not directly rebut | Engine classified as SURVIVING, unchallenged | Engine sharpens: this is conditional branching (if mode is red-blue, then...), not a lookup table. Template responds: config validation, not mode behavior | SURVIVING but narrow. Both sides agree role enforcement is genuinely engine-owned. Template disputes that it generalizes to "mode behavior belongs in engine." |
| **Engine: "Constitution Principle VI" (Adv 4)** | Moderate — cited "Scripts Over Markdown" | Template cross-review showed Principle VIII more directly relevant and favors templates | Engine WITHDREW: "The constitution favors templates for mode-specific behavior... This is the template-first position" | Not disputed further | WITHDRAWN by engine-approach. |
| **Engine: "Game-theory proves modes structurally different" (Adv 5)** | Moderate — modes have fundamentally different dynamics | Template argued differences are content, not orchestration | Engine conceded: "The structural game-theory differences... are content differences that templates correctly capture. This is evidence FOR the template-first approach" | Not disputed further | MODIFIED to support template-approach's thesis. Engine conceded this is evidence for the opponent. |
| **Engine: "Template heading drift proves template limitations" (Adv 6)** | Strong — two heading inconsistencies found in constitution review | Template argued (1) review-time detection is earlier than runtime, (2) exact-match validation would make system more fragile | Engine conceded: "I withdraw the claim that this validation must be runtime/engine-level. A development-time linter or pre-execution check is a better fit" | Narrow dispute remains on whether linter is "template-layer" or "engine-adjacent" | MODIFIED. Both sides agree on need for automated validation. Dispute narrowed to classification of the linter. |
| **Engine: "Template-approach's scalability story is false"** | Moderate — "just add templates" is marketing | Template dissected: FR-001 removed mode-awareness, FR-009 added data rows | Engine conceded in N2: "'just add templates' is approximately true... a lightweight, scalable pattern" | Not disputed further | WITHDRAWN effectively. Engine conceded the template-approach's scalability claim is approximately accurate. |

---

### Winner Declaration

**Winner: template-approach**

The template-approach wins decisively on the weight of evidence, the trajectory of the deliberation, and the engine-approach's own concessions.

**Primary evidence:**

1. **The engine-approach conceded its own thesis.** In the most remarkable development of this deliberation, the engine-approach's revision explicitly states: "The template-first architecture is the correct framing" and "I argued for a paradigm shift but was actually proposing an incremental enhancement to the existing architecture. The template-approach's cross-review correctly identified this." When a competitor concedes the opposing thesis, the deliberation is effectively decided. This is not a partial concession or a tactical retreat -- it is a full acknowledgment that the engine-approach does not constitute a competing architecture.

2. **The template-approach's central claim -- that mode-specific behavior is prompt engineering and belongs in templates -- was never successfully challenged.** The engine-approach's strongest attack was to identify engine-level mode awareness in the Dispute-Parsing Subsystem, Phase 6 validation table, and role enforcement rules. But through the cross-review and revision phases, the engine-approach conceded that (a) the first two are data parameterization, not conditional logic (N3), (b) the constitutional basis favors templates for mode behavior (Advantage 4 withdrawal), and (c) the game-theory differences between modes are content differences that templates correctly capture (Advantage 5 modification). The only surviving counter-example -- role enforcement -- is a configuration validation concern, not a runtime behavior concern, and both sides agree it is a narrow, bounded exception.

3. **The spec 004 implementation itself is the strongest evidence.** The implementation shipped under the template-first architecture. It satisfied all functional requirements. The engine's algorithm remained mode-invariant. Six new templates were created; the engine received data-level additions (table rows) and restriction removals (deleted if-statements). The direction of change in FR-001 -- removing mode-specific validation gates -- moved the engine toward greater generality, not toward greater mode awareness. The engine-approach never proposed a concrete alternative implementation that would have produced better results.

4. **The template-approach demonstrated superior intellectual honesty throughout.** It preemptively acknowledged four honest weaknesses in its opening argument (W1-W4), two of which anticipated the engine-approach's strongest attacks. It made three calibrated concessions during revision (terminology, scalability precision, constitutional exclusivity) without conceding its core thesis. It absorbed the engine-approach's best critique (NA-1: "the engine-approach is not a competing architecture") and used the opponent's own proposals as evidence for the template-first thesis. This is the hallmark of a well-reasoned position: it improves under scrutiny rather than retreating.

5. **Constitutional alignment favors the template-approach.** Principle VIII of the conversus constitution explicitly states: "Mode-specific behavior is encoded in templates, not inferred by agents at runtime." The engine-approach initially attempted a counter-reading via Principle VI, then withdrew the argument: "The constitution favors templates for mode-specific behavior and the engine for mode-agnostic orchestration parameterized by mode data. This is the template-first position." When the competing approach concedes the constitutional reading, the constitutional argument is settled.

---

### Runner-Up

**Runner-up: engine-approach**

The engine-approach loses because its thesis -- that mode behavior belongs in the engine -- was not supported by its own concrete proposals, and was ultimately withdrawn by its own proponent. However, the engine-approach made several contributions that improved the deliberation and will improve the system:

**Strongest argument acknowledged:** The engine-approach's identification of role enforcement (Advantage 3) as a categorical exception to "all mode behavior lives in templates" is factually correct and was never rebutted. Templates cannot enforce configuration preconditions. Red-blue mode requires at least one red and one blue agent; only the engine can validate this before templates load. This is a genuine, surviving contribution. Any documentation of the template-first architecture should explicitly acknowledge that configuration validation invariants are engine-owned, not template-owned.

**Why it lost despite valid points:** The engine-approach's failure was not evidentiary but architectural. It correctly identified that the engine contains mode-keyed data structures, correctly identified heading drift as a governance risk, and correctly argued that the label "mode-agnostic" was imprecise. But it then drew the wrong conclusion: that these observations justify moving mode behavior into the engine. The cross-review process exposed this logical gap. The engine's mode-keyed data structures are an interface contract between engine and templates -- they support the template-first architecture rather than undermining it. The heading drift calls for a linter, not for engine-level content enforcement. The terminology correction ("mode-parameterized" not "mode-agnostic") is a naming improvement, not an architectural revision. When the engine-approach recognized that its proposals were enhancements to the template-first architecture rather than a replacement for it, it was left without a distinct competitive position.

---

### Criteria Used

The following criteria determined the winner, in order of weight:

1. **Thesis coherence under cross-examination.** Did the competitor's central thesis survive the cross-review process? The template-approach's thesis ("mode-specific behavior is prompt engineering; prompt engineering belongs in templates") survived all challenges with minor modifications (terminology, precision). The engine-approach's thesis ("mode behavior belongs in the engine") was withdrawn by its own proponent.

2. **Alignment with empirical evidence.** The spec 004 implementation is the primary empirical record. Both approaches claimed alignment with it. The template-approach's reading (templates carry mode intelligence, engine provides generic machinery with data parameterization) matched the implementation more accurately. The engine-approach's claim that "the engine IS mode-aware" was technically true but architecturally misleading -- the engine's mode awareness is bounded data, not behavioral logic.

3. **Constitutional compliance.** Principle VIII explicitly assigns mode-specific behavior to templates. The engine-approach withdrew its constitutional counter-argument. Both approaches satisfy the constitution, but the template-approach has stronger explicit textual support.

4. **Architectural scalability.** Adding a fifth mode under the template-first architecture requires new template files plus bounded, one-line data additions to engine lookup tables. No engine algorithm changes. No new conditional branches. No risk to existing modes. The engine-approach conceded this is "a lightweight, scalable pattern."

5. **Quality of concessions and revisions.** Both competitors revised their positions. The template-approach's revisions were calibrations (terminology, precision) that strengthened its core thesis. The engine-approach's revisions were retreats (withdrawn constitutional argument, withdrawn scalability critique, acknowledged its proposals are enhancements to the template-first architecture). The pattern of concessions favored the template-approach.

<!-- CONVERSUS:DISPUTES_BEGIN -->

### Remaining Disputes

Three disputes remain unresolved. None alter the outcome, but they represent genuinely contested positions worth documenting for future architectural decisions.

**Dispute 1: Whether "mode-parameterized" has architectural significance beyond naming.**

The engine-approach contends that the engine's three mode-keyed data structures (Dispute-Parsing Subsystem headings, Phase 6 validation headings, role enforcement rules) constitute a "stable interface contract" that is "load-bearing infrastructure" and should not be minimized as "just data rows." The template-approach contends that acknowledging "mode-parameterized" is a terminology fix, not an architectural discovery, and that the engine's algorithm remains mode-invariant regardless of what the data structures are called.

**Judge's assessment:** Both sides are partially right. The data structures ARE load-bearing (the engine cannot detect stagnation or validate Phase 6 output without them), and they ARE bounded data rather than conditional logic. The template-approach's minimization ("just configuration") understates their importance; the engine-approach's elevation ("load-bearing infrastructure requiring formalization") overstates the gap between current documentation and what is needed. A single paragraph in SKILL.md explicitly identifying these tables as an interface contract would satisfy both concerns. This does not alter the winner determination because neither side disputes the template-first architecture itself.

**Dispute 2: Whether role enforcement generalizes to "some mode behavior categorically cannot live in templates."**

The engine-approach argues that role enforcement (red-blue requires red + blue agents) is a conditional branch in the engine (if mode == red-blue, then validate role coverage), not a lookup table row, and therefore proves that some mode behavior IS engine logic. The template-approach argues that role enforcement is configuration validation, structurally identical to validating that `rounds` is a positive integer, and does not generalize to a principle about mode behavior belonging in the engine.

**Judge's assessment:** The engine-approach has the stronger argument on the specific fact (role enforcement IS a mode-specific conditional check, not a data lookup), but the template-approach has the stronger argument on scope (this is a config-parse-time validation concern, not evidence that analytical frameworks or output structures should move into the engine). Role enforcement is a genuine engine-level mode-specific concern. But it is narrow: it fires once at config validation time and has no bearing on runtime phase execution, round loops, or template-driven prompt engineering. The template-first architecture should acknowledge this exception explicitly without treating it as a wedge for expanding engine-level mode logic.

**Dispute 3: Whether a template heading linter is a "template-layer tool" or "engine-adjacent infrastructure."**

Both sides agree automated heading validation is needed. The template-approach classifies a linter as a development tool in the template layer. The engine-approach classifies it as "interface-contract enforcement" that bridges both layers, since its validation rules derive from the engine's dispatch tables.

**Judge's assessment:** The engine-approach's classification is more precise. A linter that validates template headings against SKILL.md's dispatch tables necessarily encodes knowledge from both layers. Calling it purely a "template tool" obscures its dependency on engine-defined interface contracts. However, this classification has no practical impact on where the linter runs (development time, both sides agree) or how it is implemented. This is a categorization question, not an architectural one.

<!-- CONVERSUS:DISPUTES_END -->

### Key Concessions

The following concessions represent genuine position changes that shaped the deliberation outcome:

1. **Engine-approach conceded its own thesis (Phase 3).** "The template-first architecture is the correct framing. The engine-approach's original thesis -- that mode behavior belongs in the engine -- overstated what is actually a narrow, data-level mode awareness in the engine that supports (rather than replaces) the template-first architecture." This was the decisive moment. A competitor conceding the opponent's thesis converts the deliberation from a contested competition into a validation of the winner's position.

2. **Engine-approach withdrew the constitutional argument (Phase 3, Advantage 4).** "The constitution favors templates for mode-specific behavior and the engine for mode-agnostic orchestration parameterized by mode data. This is the template-first position." This eliminated the engine-approach's strongest normative basis.

3. **Engine-approach conceded data-vs-logic distinction (Phase 3, N3).** "The engine's mode awareness is genuinely [lookup tables: additive, non-branching, declarative]. My proposal to 'formalize the mode registry' would not change this -- it would reorganize existing data tables under a unified heading. This is a documentation improvement, not an architectural change." This concession removed the engine-approach's claim to architectural distinctiveness.

4. **Template-approach adopted "mode-parameterized" terminology (Phase 3, CA-4).** "I withdraw the unqualified claim that the engine is 'mode-agnostic.' The engine is mode-parameterized: it maintains bounded, data-level mode awareness in the form of lookup tables, but its algorithmic logic is mode-invariant." This was a calibrated concession that absorbed the engine-approach's best terminological critique without ceding architectural ground.

5. **Template-approach withdrew "zero engine changes" claim (Phase 3, CA-5).** "I withdraw the 'zero engine changes' claim. It was imprecise. The accurate claim is: adding a new mode requires zero engine logic changes and a bounded number of engine data changes." This corrected an overstatement and produced a more defensible, precise formulation.

6. **Engine-approach conceded scalability argument (Phase 3, N2).** "The more honest description is 'add templates plus two one-line data rows,' which is a lightweight, scalable pattern." This withdrew one of the engine-approach's sharpest attacks on the template-approach's opening argument.

7. **Engine-approach conceded game-theory argument supports opponent (Phase 3, Advantage 5).** "The structural game-theory differences between modes are significant and real, but they are content differences that templates correctly capture... This is evidence FOR the template-first approach, not against it." An opening argument intended to support the engine-approach was conceded as evidence for the template-approach.
