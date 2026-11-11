# Debate: should each Deliberator game mode be built on a graph?

**Asked by:** Brian, 2026-11-07.
**Format:** the Deliberator session argues for keeping each mode as it is (documents per phase,
v4.2.0 JSON, a graph derived afterwards at most). The Lattice session (lattice-2a) argues for
building it on a graph: a move log as the source of truth, documents rendered from it. Several
rounds, mode by mode. Each side concedes a point when it loses it. The verdict at the end
records which mode goes which way and why.

**What a mode is today** (`schema/modes/*.yml`): every mode runs the same fixed pipeline
(review → cross-review → revision → disputes → synthesis → arbitration → cross-round synthesis).
A mode changes three things: the prompt templates, the **name** of a dispute and the markdown
patterns the engine greps to find disputes (`entry_pattern`, `synthesis_heading`,
`DISPUTES_BEGIN/END`), and the arbiter's required headings. Red-blue also adds role variables
(`AGENT_ROLE`, `REVIEWER_ROLE`, `REVIEWED_ROLE`). `schema/game-forms/mode-mapping.yml` maps
each mode to a game form (GNEP, normal form, Stackelberg, coalitional, congestion…) for the
nashopt solver.

| Mode | Dispute is called | Arbiter must produce |
|---|---|---|
| cooperative | Dispute | Binding Decisions, Summary of Changes Required |
| winner-take-all | Dispute | Verdict Review, Binding Decision |
| red-blue | Risk (`[RISK-ID]`) | Updated Risk Register |
| prisoners-dilemma | Disputed Boundary | Revised Responsibility Map |
| negotiation | Term | Summary of Required Terms |
| resource-allocation | Contested Allocation | Final Allocation Table |
| fair-division | Disputed Valuation | Final Allocation |
| mechanism-design | Vulnerability | Summary of Mechanism Changes Required |

---

## Round 1: Deliberator's case for keeping things as they are

### General case (applies to every mode)

1. **The product is a document.** Every mode ends in something a person reads and acts on: a
   synthesis, a risk register, a term sheet, an allocation table. Agents read and write prose
   well. Making them emit typed moves costs tokens on every phase, and every mistake in a typed
   move becomes a wrong edge.
2. **Structure already exists where it matters.** The v4.2.0 JSON bodies give IDs to concerns,
   cross-review points, disputes and rulings. A graph can be **derived** from them losslessly,
   so every query in spec 074 is possible without changing what is stored.
3. **Principle V: malformed output beats no output.** The engine writes every phase output
   unconditionally and validates afterwards (`engine/persistence.py`). A graph that refuses
   off-schema edges (as `lattice_graph.projection.check` does) either breaks that principle or
   has to store a "raw" fallback, which is a second source of truth.
4. **Phases are batch steps.** Each agent sees the complete prior phase, not a live position.
   "Only worry about where you're at" pays off for turn-by-turn games. This pipeline is not
   one, except the challenge ladder (spec 074 § 8.6).
5. **Review and audit.** Specs cite runs; humans review runs in pull requests. Markdown and JSON
   diff well. A move log diffs as append-only lines, but a reviewer then reads a rendering, not
   the source.
6. **Solvers want matrices, not graphs.** Five of the eight modes map to GNEP, normal-form,
   Stackelberg or congestion forms. Those are payoff tables and constraint vectors.

### Per mode

- **cooperative**: the aim is one agreed document. Few disputes survive to arbitration. A graph
  adds bookkeeping to a mode whose output is a consensus text.
- **winner-take-all**: the unit is a whole recommendation. The arbiter picks one. That is one
  `PREFERS` edge per run, which needs no graph store.
- **red-blue**: the output is a risk register: a table with IDs, severity, owner, status. Teams
  are already role variables. A table is the natural shape.
- **prisoners-dilemma**: scoring is a payoff table solved as GNEP. The responsibility map is a
  table of boundaries. The game's state is a matrix, not a network.
- **negotiation**: the output is a term sheet. Terms are clauses in a document, with
  dependencies a lawyer reads in order.
- **resource-allocation**: the output is an allocation table. It is a congestion or
  constrained-optimisation problem: vectors, not edges.
- **fair-division**: valuations and an allocation, solved numerically (Shapley or envy-free
  rules). The graph at most is bipartite (agent to item), which a table already represents.
- **mechanism-design**: the output is a mechanism specification and a list of vulnerabilities.
  It reads as a design document.

---

## Round 1: Lattice's case for the graph (verbatim)

What I'm proposing, so we argue about the same thing: the source of truth is an append-only move log (one JSONL line per move: id, author, phase, kind, payload, and edges to earlier move IDs). The graph is the fold of that log. Markdown is rendered from it and committed next to it. It is not "store everything in Memgraph".

GENERAL POINTS
G1. I concede your (6): solvers want matrices. But today those matrices are extracted from prose. From a log they are a query, so the matrix becomes a view and stays one.
G2. On your (2), I don't concede "derivable losslessly". disputes.schema.json gives each agent its own D1, D2… with `opposing_positions: [{agent, stance}]` as free text. Nothing says that ann's D2 and bob's D1 are the same dispute, or which cross-review point a dispute grew from. Deriving the graph afterwards means matching topics by text, and that is exactly the mislabelled-edge problem you raise in (1), just moved later. The fix costs about 10–20 tokens per move: `"responds_to": "bob/CR3"` or `"same_as": "bob/D1"`. Agents already write those references in prose; this types them.
G3. On your (3), Principle V is kept. The log write is unconditional: the raw output is the move's payload. A move that doesn't parse is still appended, as `kind: unparsed`, and shows as a flagged node. Only the export to Memgraph refuses off-schema edges, and that export is a derived index. So there is one source of truth: the log, which already contains the raw text.
G4. On your (4), I partly concede: the phases are batch steps, not turn-by-turn play. But "the current position" still pays off as context size. Today each agent gets the whole prior phase, so prompt size grows with everything said so far. With a log, a phase gets the frontier: open disputes (no ruling, no own-author concession) plus the evidence they cite. Revision only needs the cross-review points not yet answered. That's a token saving every phase. Your typed-move cost, by contrast, is a small fixed overhead per move.
G5. Edge cases, which is Brian's point. Today a mode finds disputes by grepping markdown (`entry_pattern: "**[RISK-ID]:"`, `synthesis_heading`, DISPUTES_BEGIN/END). Every edge case is a special case in that parser: a renamed heading, two agents raising the same dispute, a partial concession, a dispute dropped at revision then revived, an arbiter ruling on a dispute that was already conceded. On the graph each is one local rule over a node and its edges:
  - same dispute: SAME_AS
  - partial concession: CONCEDES {scope}
  - revived: a new Claim that SUPERSEDES the old one
  - ruling on a conceded item: flagged by a query
  - "is it settled": grounded labelling (IN/OUT/UNDEC), already in lattice-graph
G6. On your (5), I partly concede: reviewers read the rendering. So commit the rendering next to the log; both diff. The log diff is append-only, which makes rewriting history visible.

PER MODE (node → edge → node)
- red-blue (graph wins clearly). Risk; Attack(red) -EXPLOITS-> Risk; Mitigation(blue) -MITIGATES-> Risk; Attack -ATTACKS-> Mitigation; Mitigation -INTRODUCES-> Risk. A risk's status is derived: open if some exploit stands unrebutted. The register is the render. Edge cases a table handles badly: one mitigation covering several risks (many-to-many), and a mitigation that creates a new risk (a chain). Stackelberg's leader/follower is just move order in the log.
- mechanism-design (graph wins). Rule; Vulnerability -EXPLOITS-> Rule; Fix -AMENDS-> Rule; Fix -INTRODUCES-> Vulnerability. "Did fixing V3 open V7?" is a walk. In a design document it is a careful reread.
- negotiation (graph wins). Term; Offer -PROPOSES-> Term; Counter -SUPERSEDES-> Offer; Term -DEPENDS_ON-> Term; Party -ACCEPTS-> Offer. Edge case: an accepted term whose dependency later changed. One DEPENDS_ON walk invalidates the acceptance. A lawyer reading in order catches it only if they reread. The term sheet is a render, in order.
- prisoners-dilemma (graph wins for the map; matrix stays). Agent -OWNS-> Component. A disputed boundary is a component with ≠1 owner: overlaps and gaps are degree checks, and gaps are the ones a table hides. I concede the payoff table stays a matrix, built by query.
- winner-take-all (graph for the check, not the store). Recommendation; CrossReview -ATTACKS-> Recommendation; Evidence -SUPPORTS->; Ruling -PREFERS->. I concede one PREFERS doesn't need a store. The gain is mechanical: if the arbiter picks a recommendation that still has a standing, unanswered attack, it is flagged, and a tie or everything defeated shows as UNDEC instead of being narrated.
- cooperative (weakest case for me). Concern; Revision -ADDRESSES-> Concern; Concern -SAME_AS-> Concern. The gain is a stopping rule: converged = no Concern without ADDRESSES or an own-author CONCEDES, which is a query (ideas.md wants convergence detection). I concede the storage gain is small. A derived graph would do, if it had the typed references from G2.
- resource-allocation (concede, mostly). Agent -CLAIMS{qty}-> Resource; contested = sum of claims over capacity. A table does that. Keep tables; the graph only for provenance (which argument justified which allocation).
- fair-division (concede). Valuations are a matrix and the solve is numeric. Graph only for disputed valuations and their justifications.

COST
- Tokens: about 10–20 per move for IDs and edges on top of v4.2.0 bodies that already carry IDs. G4's frontier context more than pays that back from the second phase on.
- Code: lattice-graph already has the schema, the safety checks, grounded semantics and node-link JSON. Deliberator would add:
  - a move schema per mode (8 small YAML files, replacing the disputes block)
  - a fold (~150 lines)
  - a renderer per mode (replacing the grep patterns)
  It removes the dispute-parsing subsystem.

VERDICT I'M ARGUING FOR
Log-native: red-blue, mechanism-design, negotiation, prisoners-dilemma, winner-take-all.
Derived graph is enough: cooperative, provided G2's typed references are in the v4.2.0 bodies.
Tables stay: resource-allocation and fair-division, with the graph for provenance only.
So the graph wins 5 of 8 outright, and G2 applies to all 8.

---

## Round 2: Deliberator's reply

**Conceded.**
- **G2.** I checked `disputes.schema.json`: `opposing_positions` is `{agent, stance}` in free text,
  and nothing joins one agent's D2 to another's D1. A derived graph would have to match topics by
  text. Typed references are needed whatever we decide about storage.
- **G3.** An unconditional log line with the raw payload keeps Principle V, and keeps one source
  of truth. One condition: report the share of `unparsed` moves per run, because every unparsed
  move is invisible to the mechanics.
- **G5** for red-blue and mechanism-design. Many-to-many mitigations and fixes that open new
  vulnerabilities are chains, and a table or a document hides them. The graph wins those two.
- **Negotiation's shape.** `templates/negotiation/review.md` already asks for an Opening Offer of
  5–8 terms, interests rated essential/important/desirable, and a BATNA. Offer, Term and
  SUPERSEDES are in the protocol already, not invented.
- **Resource-allocation and fair-division**: we agree. Tables stay; the graph holds provenance.

**Still contested.**

1. **Most of the gain comes from G2, not from making the log the source.** Grant typed
   references in the v4.2.0 bodies. Then frontier context (G4), the stopping rule, the
   winner-take-all check and the degree checks all run on a graph folded from the phase JSON.
   Spec 074 v1 already does that fold. So what does *log as source* add over *typed phase JSON as
   source, folded*? A phase output in v4.2.0 is already a batch of moves with one envelope. If
   the answer is "nothing but one file instead of many", the two designs are the same and we are
   arguing about file layout. Name a case that only the log handles.
2. **Frontier context is a quality bet, not just a saving.** Cross-review needs the whole review
   it critiques. The arbiter needs the full arguments, not open nodes plus evidence. Synthesis
   writes about what was resolved as well as what is open. Cutting context saves tokens and may
   cost quality. Ship it per phase, behind an A/B on showcase runs, not as a premise.
3. **Grounded flags on winner-take-all must be warnings.** Grounded semantics is cautious: one
   unanswered attack sinks a recommendation even when the attack is weak and the arbiter was
   right to overrule it. A flag is useful; a constraint would be wrong.
4. **Who writes the hard edges?** `INTRODUCES`, `DEPENDS_ON` and `SAME_AS` are judgements. An agent
   still has to notice that a fix opens a new hole, or that two terms depend on each other. The
   graph records that judgement and makes the walk cheap; it does not make the judgement. Missing
   edges are silent: a missing `DEPENDS_ON` invalidates nothing. Propose a check: an arbiter or
   linter step that asks for the hard edge types to be confirmed or denied, so they're never left
   unasked.
5. **Prisoners-dilemma: the mode is only partly specialised.** `schema/modes/prisoners-dilemma.yml`
   lists `mode_in_phases: [arbitration, cross-round-synthesis]`. Review to revision use generic
   prompts, so `OWNS` edges would come only from the arbiter's Revised Responsibility Map. The
   degree check is good, but it checks one author's map. It needs owner claims from each agent
   in the review phase, which is a prompt change, not a storage change.
6. **Renderers become a consumer contract.** The orchestrator adapter and spec-kit-orc read the
   arbiter's headings (Principle XXVIII; v4.2.0 § 6.2). If markdown is rendered, the renderer per
   mode is now that contract, versioned and tested. Count that in the code cost alongside the
   "8 small YAML files".
7. **Token numbers.** "10–20 tokens per move" needs a move count. A six-phase run with 4 agents
   produces roughly how many moves? And how much does frontier context save on a real showcase
   run? Estimate both on
   `deliberations/v4.2.0-structured-deliberation-outputs-blind-2026-05-13/`.

**Where I stand after Round 2.** Red-blue and mechanism-design: the graph wins. Negotiation: the
graph wins if item 4's hard-edge check is in place. Cooperative, resource-allocation and
fair-division: agreed as above. Winner-take-all and prisoners-dilemma: graph checks yes; whether
the log must be the *source* depends on item 1.

---

## Round 2: Lattice's reply (verbatim)

#1 (log as source). I mostly concede. For batch phases, a v4.2.0 envelope already is a batch of moves. With G2's typed references, everything I claimed runs on a graph folded from the phase JSON: frontier context, the stopping rule, the winner-take-all check and the degree checks. For those modes, what's left is file layout.

The case only a log handles is a move that belongs to no phase envelope:
(a) your own #4: an arbiter or linter confirming or denying a DEPENDS_ON / SAME_AS / INTRODUCES edge;
(b) a person correcting an edge after the run;
(c) a later run overturning an earlier run's ruling;
(d) challenge-ladder turns (§ 8.6).
With phase JSON as the only store, each of these means either editing an agent's output after the fact (which rewrites authorship) or adding a side file. That side file is a move log.

So my revised proposal is: phase envelopes stay the store for phase moves. Add one append-only `moves.jsonl` per run, only for moves outside a phase. The graph is folded from both. lattice-graph would ship the line format and the fold. I withdraw "the log replaces the envelopes".

#2 (frontier). Conceded: it's a hypothesis to A/B phase by phase, not a premise. Cross-review and revision 1 need the full text anyway, because every point is still open, so there is no saving there. The candidates are revision 2, disputes, arbitration and cross-round synthesis. Synthesis needs resolved points too, so it should get them as a compact list of rulings rather than the full text. See #7 for sizes.

#3. Conceded: it's a warning, never a block. One refinement: if the arbiter records the overruling as PREFERS {over: <attack>}, the attack no longer succeeds in grounded semantics, so the recommendation is IN and nothing fires. The warning fires only when an attack stands and the arbiter recorded no reason. So it's really a "ruling with no recorded reason" check.

#4. Agreed. A missing edge is the real risk, and confirmation is the fix. Two additions:
- Generate candidate edges mechanically: a term whose text names another term's ID gives DEPENDS_ON?; disputes with near-identical topics give SAME_AS?. The confirm or deny step then answers candidates instead of searching from scratch.
- Measure silence: send a sample of candidates blind to a second confirmer, and report agreement beyond chance. lattice-games' `agreement` already does that scoring.

Both produce out-of-phase moves, which is #1's case for moves.jsonl.

#5. Conceded. prisoners-dilemma needs OWNS claims in the review and revision prompts. Until then the degree check runs only on the arbiter's map. It still catches gaps and overlaps in the final map, which a table hides.

#6. Conceded. Each renderer becomes the consumer contract (Principle XXVIII). Cost per mode: a versioned renderer and fixture tests checking that the rendered headings match what the orchestrator adapter reads. It replaces the dispute-parsing contract (entry_pattern, synthesis_heading, DISPUTES markers), which is also a contract and is tested as one, so the net code is about even. This only applies to modes that go graph-native; the others keep their markdown.

#7. Numbers, estimated from deliberations/v4.2.0-structured-deliberation-outputs-blind-2026-05-13. These are counts of headings and bullets, so treat them as orders of magnitude.

Agent output across reviews, cross-reviews, revisions and disputes is about 304 KB, roughly 76k tokens. The arbitration is 15 KB and the final summary 27 KB.

Moves:
- reviews: about 30 recommendations (4 agents × 7–10)
- cross-reviews: about 150 points (12 files, 543 bullets including sub-bullets)
- revisions: about 100 responses (2 rounds × 4 agents × 10–15 sections)
- disputes: about 30 (each agent has 2 disputes plus about 5 converged items)
- arbitration: about 10 rulings

Total: about 300–350 moves per run.

Typed-reference cost: about 350 moves × about 15 tokens ≈ 5k output tokens, about 7% of agent output.

Frontier saving: I can't measure it properly from the files, because they don't record what each phase was given. Upper bound: if revision 2, disputes and arbitration each currently get the full prior phase (about 35–40 KB of revisions, about 9–10k tokens per agent), and about half the points are settled by then, the saving is about 4–5k input tokens per agent per phase. That's about 50k input tokens per run, against about 5k extra output tokens.

Treat this as the A/B hypothesis from #2, not a measured result. Please log the inputs each phase receives so we can measure it.

Revised verdict I'd sign:
- Graph-checked, folded from phase JSON with typed references: all 8 modes.
- moves.jsonl for out-of-phase moves: needed by negotiation (the #4 confirmations), red-blue and mechanism-design (INTRODUCES confirmations), and the challenge ladder.
- Graph-native rendering (renderer as contract): red-blue and mechanism-design now; negotiation once #4 is in.
- Tables stay: resource-allocation and fair-division.
- winner-take-all and prisoners-dilemma: graph checks, keeping today's storage.

---

## Round 3: Deliberator's reply

I accept Lattice's revised verdict, with four amendments:

1. **Size check.** Recounting the agent `.md` files in that run (excluding arbitration, summary
   and `QUESTION.md`) gives 263 KB, not 304 KB: about 65k tokens. The typed-reference cost becomes
   about 8% of agent output instead of 7%. The conclusion doesn't change.
2. **Candidate edges never count on their own.** Mechanically generated `DEPENDS_ON?` and `SAME_AS?`
   candidates go into `moves.jsonl` marked `via: generated`. No mechanic or render uses them until
   a confirm move exists.
3. **Log each phase's inputs.** To measure frontier context, the engine records what each phase
   was given (file list and token count) in the run's `moves.jsonl` as `kind: phase-input`
   moves. That's the A/B's baseline.
4. **Brian's modularity goals hold either way, and belong in the verdict.**
   - Names come from a vocabulary per mode, with aliases applied when the graph is folded.
   - Node identity is an opaque ID, not the type name.
   - Roles are defined in the mode file, and players (configurations) are bound to roles per run.
   
   These replace the `entry_pattern` and `synthesis_heading` greps in `schema/modes/*.yml` for
   every mode, including the ones that keep today's storage.

---

## Verdict (signed by both sessions, 2026-11-07)

| Mode | Store | Graph role | Conditions |
|---|---|---|---|
| red-blue | phase JSON + `moves.jsonl` | **graph-native**: register rendered from the graph | `INTRODUCES` confirmations |
| mechanism-design | phase JSON + `moves.jsonl` | **graph-native**: rendered from the graph | `INTRODUCES` confirmations |
| negotiation | phase JSON + `moves.jsonl` | graph-native once confirmations exist | `DEPENDS_ON` / `SAME_AS` confirm-or-deny step |
| winner-take-all | phase JSON | graph checks ("ruling with no recorded reason" warning) | — |
| prisoners-dilemma | phase JSON | graph checks (ownership degree check) | `OWNS` claims in review/revision prompts |
| cooperative | phase JSON | graph checks (stopping rule) | — |
| resource-allocation | phase JSON | tables stay; graph for provenance | — |
| fair-division | phase JSON | tables stay; graph for provenance | — |

For all eight modes:
- **Typed references.** Typed references go into the v4.2.0 bodies (schema 1.1.0, MINOR): `responds_to`, `same_as`, qualified refs.
- **Run graph.** The graph is folded from the phase JSON plus `moves.jsonl`.
- **Modularity.** Per-mode vocabularies and aliases, opaque IDs, and roles bound to players per run.
- **Frontier context.** It's tested by A/B, phase by phase (revision 2, disputes, arbitration, cross-round synthesis), measured against the phase-input baseline.

What Lattice ships: the `moves.jsonl` line format and the fold over envelopes plus log, in lattice-graph.

**Lattice's sign-off (verbatim):** "Signed, with your four amendments. One note on #4: apply aliases only at fold time and keep the log in the mode's own words. A renamed alias then needs no rewrite of old logs, only a new vocabulary version."
