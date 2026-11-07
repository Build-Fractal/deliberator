# Feature Specification: Graph Backend and Game Mechanics

**Feature ID**: `074-graph-backend`
**Created**: 2026-11-07
**Status**: Draft (v1). Not yet deliberated.
**Depends On**: v4.2.0 structured deliberation outputs (JSON phase outputs, `engine/schema/v1/`);
v4.1.0 persistence contract discipline (Principle XXVIII); `lattice-graph` (Build-Fractal/lattice,
branch `graph-games`, `packages/lattice-graph`), once it is published.
**Supersedes**: spec 046 FR-012 and SC-006/SC-007 (`commentary/graph.jsonl`).
**Research basis**: `docs/research/2026-11-01-graph-data-structure-game-theory.md` (the "note").
Section references like "note §9.1" point there. Claims the note marks **UNVERIFIED** are not
relied on here; where this spec touches one, it says so and says what has to be checked first.

---

## 1. Problem

A deliberation already has the shape of an argument graph: agents make claims, attack each
other's claims, concede, and an arbiter rules one position over another. Specs then cite those
rulings by hand ("ruling at `deliberations/X/arbitration/resolution.md` (commit `8f90e2d`)",
ledger rows `F1 | … | § 11, § 9.1`, "Principle VIII (L161-183)"). None of that is
machine-readable, so none of it can be checked, queried across runs or scored.

The outcome of a deliberation is narrated, not computed. We cannot answer "which claims stood",
"which agent configuration wins disputes on blind runs", "how often does the arbiter agree with
itself beyond chance" or "which concessions make good training pairs" without reading every file.

## 2. Goals

1. A derived, versioned `graph.json` per run, built in CI with no database, from the run's
   written outputs.
2. A strict link grammar for the references written by hand in specs and rulings, linted like
   `linter/` lints today.
3. One schema: `lattice-graph`'s `ARGUMENT_SCHEMA` combined with Deliberator's own types.
4. Six game mechanics on that graph, specified with their moves, scoring, gaming resistance and
   cost, shipped in a fixed order (§ 8).
5. A path to Memgraph as a rebuildable index, without making it a dependency.

## 3. Non-goals

- **No new source of truth.** The graph is always rebuilt from files. Nothing is written only to
  the graph (Principle XI).
- **No database in the default install or in CI.** NetworkX only.
- **No scores in agent prompts.** Scores are for operators comparing configurations and
  diagnosing runs, not a signal agents see (§ 9.1).
- **No re-emission of historical runs.** Old markdown runs get a best-effort graph (§ 5.3); they
  are not rewritten.
- **No change to the shared argument types inside Deliberator.** Changes go to Lattice (§ 11).
- Lattice's human-curation methods (`lattice-games`) are out of scope. These mechanics are for AI
  agents and stay in Deliberator.

## 4. Where the graph sits relative to storage

Brian confirmed on 2026-11-07 that no storage change is under way yet. This spec is therefore
the first storage proposal, and it keeps storage as it is:

| Layer | What it is | Status |
|---|---|---|
| Source of truth | Phase outputs on disk under `deliberations/<id>/…`: v4.2.0 JSON envelopes once the engine emits them, markdown before that; specs and `CONSTITUTION.md` for the hand-written references | v4.2.0 schemas and validator exist (`engine/schema/v1/`, `engine/schema_validator.py`); `persist_output` is not yet called by the engine |
| Derived graph | `deliberations/<id>/graph.json`, built by `deliberator graph build` | this spec |
| Optional index | Memgraph loaded from many `graph.json` files; thrown away and rebuilt at will | this spec, phase G4 |

Consequence: the graph's quality depends on structured outputs being wired in. Spec 074 does
not wire them in, but phase G1 (§ 10) is blocked until the engine writes v4.2.0 JSON for at
least the review, cross-review, revision, disputes and arbitration phases.

## 5. Sources of graph facts

Every node and edge records where it came from (`props.source`) and how it was obtained
(`props.via`), in descending order of trust:

| `via` | From | Used for scoring |
|---|---|---|
| `structured` | a typed field in a v4.2.0 JSON output | yes |
| `link` | a `[[kind:id#anchor]]` link in markdown (§ 6) | yes |
| `layout` | the directory layout and `deliberator.yml` (runs, phases, agents) | yes |
| `extracted` | an LLM extractor over prose (spec 046's `graph-extraction.md`), with `props.confidence` | **no**, by default |

Extraction is a fallback for historical runs. Mechanics ignore `extracted` edges unless the
operator passes `--include-extracted`, and every report says how many edges came from each
source. (Note §11, "Extraction fidelity".)

### 5.1 Additions needed in the v4.2.0 bodies (schema 1.1.0, MINOR, all optional)

The v1 bodies carry local IDs (`C3`, `CR2`, `D1`, `Q1`) but not the links the mechanics need.
Each addition is an optional field, so 1.0.x outputs stay valid (MINOR bump under Principle XXVIII):

| Body | Field to add | Why |
|---|---|---|
| `review.concerns[]`, `cross-review.new_concerns_raised[]` | `evidence[]: {kind, locator, hash?}` (`kind` ∈ file-line / test / quote / url) | `SUPPORTS` from `Evidence`; anti-spam rule in § 8.1 |
| `cross-review.disagreement_points[]` | `ref` MUST be qualified: `<agent>/<id>` (today a free string) | `ATTACKS` needs a resolvable target |
| `revision.position_changes[]` | when `delta = withdrawn`: `conceded_to?: <agent>/<id>` | `Concession` and what it conceded to |
| `disputes.disputes[].opposing_positions[]` | `ref?: <agent>/<id>` | `DISPUTES` edges to the claims involved |
| `arbitration` | `dispute_rulings[]: {dispute: <agent>/D<n>, prefers: <agent>/<id>, over: [<agent>/<id>], outcome: adopt / merge / defer, confidence: 0–1, cites: [link]}` | `RULED_ON`, `PREFERS`, calibration (§ 8.3) |
| `arbitration.per_question_rulings[]` | `confidence: 0–1` | calibration (§ 8.3) |

### 5.2 Node keys

Keys are global and stable: `<kind>:<run_id>/<agent>/<local_id>` for moves (for example
`claim:v4.2.0-…-blind-2026-05-13/risk-auditor/C3`), `run:<run_id>`, `principle:XI`,
`commit:<repo>@<sha7+>`, `spec:<spec_id>@<version>`, `section:<spec_id>#<anchor>`. The same
string is used as the link-grammar reference (§ 6), so a link in a spec and a node in a graph
name the same thing.

### 5.3 Historical markdown runs

About 920 committed files (markdown and config) across the existing runs. `deliberator graph build` builds
`layout` facts for every run, `link` facts wherever links exist, and `extracted` facts only when
asked. The showcase runs used for validation (§ 12) get hand-checked graphs committed as
fixtures.

## 6. Link grammar

Uses `lattice_graph.links.parse_links` unchanged: `[[kind:id]]` and `[[kind:id#anchor]]`, with
no whitespace inside a link. Deliberator declares these kinds:

| Kind | id | anchor | Resolves when |
|---|---|---|---|
| `run` | run id (directory name under `deliberations/`) | — | directory exists |
| `ruling` | run id | `Q<n>` or `D<n>` or a dispute key | run has an arbitration output containing that question or dispute |
| `dispute` | `<run_id>/<agent>/D<n>` | — | the disputes output contains it |
| `claim` | `<run_id>/<agent>/<local_id>` | — | the output contains it |
| `condition` | `<spec_id>/<series><n>` (e.g. `v4.2.0-structured-deliberation-outputs/F1`) | — | the spec's ledger has that row |
| `principle` | Roman numeral | — | heading exists in `CONSTITUTION.md` (or the Tier 2 suite constitution) |
| `spec` | spec id, optionally `@v<n>` | `§<n>` or `§<n>.<m>` (no space) | spec exists and has that heading |
| `commit` | `<sha>` or `<repo>@<sha>` | — | `git cat-file -e` succeeds in that repo |

Examples of today's text, and the linked form:

| Today | Linked |
|---|---|
| ruling at `deliberations/X/arbitration/resolution.md` (commit `8f90e2d`) | `[[ruling:X#Q2]]` (`[[commit:8f90e2d]]`) |
| `F1 \| … \| § 11, § 9.1` | `F1 \| … \| [[spec:v4.2.0-structured-deliberation-outputs#§11]], [[spec:…#§9.1]]` |
| Principle VIII (L161-183) | `[[principle:VIII]]` |
| "Conceded at P2" | `[[claim:<run>/<agent>/C3]]` conceded at P2 |

### 6.1 Lint

A new `linter/links.py`, run by the existing lint entry point and CI:

1. Malformed links and unknown kinds (from `parse_links`) fail.
2. Unresolved links (table above) fail.
3. **Migration mode:** for 60 days after merge, hand-written references that match the old
   patterns (`(commit \`[0-9a-f]{7,}\`)`, `Principle [IVXLC]+`, ledger "Lands in" cells) produce
   warnings with a suggested link. After that window, new or changed lines fail; untouched
   historical lines are left alone.
4. `deliberator graph links --fix` writes the suggested links for a human to review. It never
   rewrites text it cannot resolve.

## 7. Schema

```python
from lattice_graph.argument import ARGUMENT_SCHEMA
from lattice_graph.schema import combine
DELIBERATOR_GRAPH_SCHEMA = combine(ARGUMENT_SCHEMA, DELIBERATOR_SCHEMA)
```

`combine` refuses a name declared differently in two schemas, so Deliberator uses the shared
types exactly as Lattice declares them and adds only new names.

### 7.1 Shared types used as they are (from `ARGUMENT_SCHEMA`)

`Participant` (an agent), `Claim` (review concerns and strengths, revised positions),
`Challenge` (cross-review disagreements and new concerns), `Evidence`, `Concession`, `Ruling`,
`Principle`; edges `AUTHORED`, `ATTACKS`, `SUPPORTS`, `CONCEDES`, `SUPERSEDES`, `PREFERS`
(`props.over` = key of the worse argument), `CITES`, `RESPONDS_TO`.

Conventions Deliberator follows on the shared types:

- A `Participant` is an agent within one run. Its props: `name`, `provider`, `model`, `role`,
  `lens`, `config` (the `Configuration` key, § 7.2).
- `CONCEDES` always targets the conceder's **own** argument: "I withdraw C3". Accepting an
  opponent's challenge is expressed as conceding one's own claim, with `RESPONDS_TO` pointing at
  the challenge. (`from_projection` treats every conceded argument as withdrawn, so conceding
  *to* a challenge by targeting it would delete the challenge; see § 11, item 2.)
- A priority change ("Conceded at P2") is not a withdrawal. It is a new `Claim` that
  `SUPERSEDES` the old one, with the new priority.
- A ruling that adopts a merged position (`outcome: merge`) writes no `PREFERS` edge. It is a
  draw for the ladder (§ 8.4).

### 7.2 Deliberator's own types (`DELIBERATOR_SCHEMA`)

Nodes:

| Label | Key props | From |
|---|---|---|
| `Run` | `id`, `stage` (originating / self-consistency / blind / rerun), `mode`, `date`, `config_hash`, `engine_version`, `source_commit` | envelope, `deliberator.yml` |
| `Phase` | `run_id`, `name` (review … arbitration), `ord`, `iteration` | envelope `output_type`, `phase_iteration` |
| `Configuration` | `provider`, `model`, `role_prompt_hash`, `lens` | config; what ladders rate (§ 8.4) |
| `Dispute` | `id`, `topic`, `severity` | disputes output |
| `Question` | `run_id`, `id` (Q1…), `text` | `QUESTION.md`, arbitration |
| `Condition` | `id` (C1, D1, E1, F1…), `series`, `priority`, `summary` | arbitration conditions; spec ledgers |
| `Spec` / `SpecVersion` | `id`; `version` | spec headers and changelogs |
| `SpecSection` | `spec_id`, `anchor` | spec headings |
| `Commit` | `repo`, `sha` | links |

Edges:

| Edge | From → To |
|---|---|
| `IN_PHASE` | Claim / Challenge / Evidence / Concession / Ruling → Phase |
| `OF_RUN` | Phase / Question → Run |
| `RUN_BY` | Participant → Configuration |
| `DISPUTES` | Dispute → Claim / Challenge |
| `RULED_ON` | Ruling → Dispute / Question |
| `PRODUCES` | Ruling → Condition |
| `LANDS_IN` | Condition → SpecSection |
| `RESULTED_IN` | Condition → SpecVersion |
| `SECTION_OF` | SpecSection → SpecVersion; `VERSION_OF` SpecVersion → Spec |
| `AT_COMMIT` | Run / Ruling / SpecVersion → Commit |
| `GROUNDED_IN` | Ruling / Condition / Claim → SpecSection / Condition / Principle |
| `RERUN_OF` | Run → Run (self-consistency, blind and rerun stages of the same question) |

`GROUNDED_IN` exists only because the shared `CITES` cannot be widened from Deliberator
(`combine` forbids it). If Lattice widens `CITES` (§ 11, item 3), `GROUNDED_IN` is dropped
before 1.0.0.

### 7.3 Derived properties

`grounded` (in / out / undec), `strength`, `survival`, ratings and credits are written only by
named jobs (`deliberator graph score <mechanic>`), as `props.derived = {"<job>": "<version>"}`.
They are never read back from text and never hand-edited. Moves are add-only: a retraction is a
new `Concession`, never a deletion.

## 8. Mechanics

Shipped in this order. Each one is a pure function from `graph.json` (one run, or many) to a
report; nothing changes the run.

Two rules apply to all six:

- **One operator configures every agent**, so collusion and sybils cost nothing. A score is a
  measurement of a configuration on a run, not a payoff to a player. Nothing here is a market.
- **Goodhart.** Scores never enter prompts, fine-tuning data or agent-visible context, except the
  arbiter-confirmed DPO pairs of § 8.2, which are exported deliberately. Reports used to choose
  configurations are computed on blind runs.

### 8.1 Survival scoring (note §9.1)

- **Moves:** `Claim`, `ATTACKS`, `SUPPORTS`, `Concession`; arbiter `PREFERS`.
- **Scoring:** `lattice_graph.argument.from_projection` → `grounded`. An attack counts only if
  the attacker has at least one `SUPPORTS` from `Evidence` whose locator resolves (file and line
  exist at the run's `source_commit`; hash matches when given). Per participant:
  `survival = 3·|IN| + 1·|UNDEC|` over its claims, reported next to the raw counts, never alone.
- **Gaming:** unevidenced attack spam is filtered by the evidence rule. `SUPPORTS` from a
  participant to its own claim earns nothing. Mutual-attack stalemates are left UNDEC, which is
  what arbitration is for. Grounded semantics is cautious: one well-evidenced, unanswered
  challenge sinks a claim. Reports say so.
- **Cost:** polynomial; milliseconds per run. Recomputed on every build.
- **Not used:** gradual `strength` (h-categoriser, DF-QuAD). Their formulas are UNVERIFIED in
  the note. Adding them needs the formulas checked against the primary papers first.

### 8.2 Concession harvest (note §9.3)

- **Moves:** `Concession`, `RESPONDS_TO`, arbiter `PREFERS`.
- **Scoring:** a concession is *confirmed* when the withdrawn claim is OUT (or withdrawn) and
  the challenge it responded to is IN, **and** a ruling in the same run `PREFERS` that side.
  Confirmed pairs are exported as `(rejected, chosen, evidence, run, ruling)` DPO triples in
  `graph-exports/dpo.jsonl`. Conceding to something that ends OUT is reported as capitulation.
- **Gaming:** pairs are paid for by outcome, not by count. They are de-duplicated by evidence hash
  and capped at 3 pairs per dispute. Only arbiter-confirmed pairs are exported, so the model does
  not learn from agents simply agreeing. Pairs from extracted edges are never exported.
- **Cost:** a filter over survival's output.

### 8.3 Arbiter calibration (note §9.5)

- **Moves:** `confidence` on each ruling (§ 5.1); the existing staging (originating,
  self-consistency, blind) gives repeated rulings on the same `Question` via `RERUN_OF`.
- **Scoring:**
  - With an outcome (a later ruling `SUPERSEDES` it, or a ratified spec reverses a condition):
    Brier score `mean((confidence − upheld)²)` per arbiter configuration.
  - Without one: chance-corrected agreement between blind and self-consistency rulings on the
    same question, `(p_o − p_e) / (1 − p_e)`, with `p_e` from the pooled verdict-class
    distribution (Scott's π). Verdicts are collapsed into the classes `pass` (APPROVE-*,
    PASS-*), `fail` (BLOCK, FAIL-*) and `other`.
- **Gaming:** blindness is already a protocol rule. The chance correction gives always-PASS a
  score of zero. Brier dominates whenever outcomes exist, because agreement has uninformative
  equilibria. Shown next to every ladder (§ 8.4).
- **Cost:** trivial. Needs many runs before it means anything. Reports show `n` and stay silent
  below 20 paired questions.

### 8.4 Configuration ladder (note §9.6)

- **Moves:** none new. Each `PREFERS` between claims of two different configurations is one match;
  `outcome: merge` is a draw.
- **Scoring:** Bradley-Terry fit per `Configuration` (provider, model, role-prompt hash, lens),
  with confidence intervals. TrueSkill only if multi-party disputes turn out to be common.
- **Gaming:** the arbiter records results, agents don't. Rate blind-run rulings only. The ladder is
  only as good as the arbiter, so it is never shown without § 8.3's calibration.
- **Cost:** a small fit over all runs. Requires the cross-run index or a merged `graph.json` set.

### 8.5 Decisive-evidence credit (note §9.4)

- **Moves:** `Evidence` and `SUPPORTS`.
- **Scoring:** first pass, *pivotal evidence*: evidence whose removal flips a ruling's preferred
  claim from IN. One grounded recomputation per evidence node per ruling. Second pass, optional:
  Monte Carlo Shapley over evidence with `v(S)` = number of rulings whose preferred claim stays IN,
  restricted (Myerson) to evidence connected through `RESPONDS_TO`/`CITES`.
- **Gaming:** collapse evidence by hash or locator range before computing, so copies are one
  player. The Myerson restriction pays nothing for evidence nobody engaged with. (The note's
  replication-attack literature is UNVERIFIED; the collapse rule is adopted on its own merits.)
- **Cost:** pivotal pass is linear in evidence × rulings. Shapley is sampled, per run only, with
  a fixed sample budget and reported variance.

### 8.6 Challenge ladder (note §9.2)

The only mechanic that changes how a run is conducted, so it comes last and is opt-in
(`mode: challenge-ladder`).

- **Moves:** alternating, enforced by the engine. The proponent states a claim, the opponent must
  attack with evidence, and the proponent must answer that attack. No argument may be repeated in
  a line. A player who cannot move loses the line or concedes.
- **Scoring:** a line is won by the proponent if every attack in it has an IN counter-attack by the
  proponent. Unanswered challenges at phase close count as losses.
- **Gaming:** illegal moves are rejected before they are written, in the engine (not by a database
  trigger). Stalling loses.
- **Cost:** extra rounds and tokens: the largest cost in this spec. Measured on a pilot before it is
  offered as a mode.

## 9. Persistence contract

### 9.1 `graph.json`

```json
{
  "schema_version": "1.0.0",
  "schema": "deliberator-graph",
  "builder": {"deliberator": "0.4.0", "lattice_graph": "0.1.0"},
  "run": "run:<run_id>",
  "sources": {"structured": 412, "link": 37, "layout": 58, "extracted": 0},
  "graph": { "format": "lattice-graph/node-link@1", "nodes": [], "links": [] }
}
```

- `graph` is exactly `lattice_graph.build.node_link(projection, DELIBERATOR_GRAPH_SCHEMA)`.
  The wrapper carries Deliberator's `schema_version` (semver, Principle XXVIII sub-clause 3)
  because the lattice format string versions the container, not Deliberator's types.
- Deterministic: same inputs, same bytes (`json.dumps(sort_keys=True, indent=1)`).
- Declared in `engine/schema/graph/graph.schema.json` and in `CONSUMER-CONTRACT.md`.
- **MAJOR** for removing or renaming a label, edge type or property; **MINOR** for adding one.
- CI (`.github/workflows/`): builds `graph.json` for every changed run, validates it against the
  schema, round-trips it through `from_node_link`, and fails on drift between the committed
  file and a rebuild.

### 9.2 Spec 046

`commentary/graph.jsonl` is not built. Spec 046's SC-007 cross-run question ("how many times
has fp-guru conceded?") is answered by § 10's G2 query over `graph.json` files. 046 is amended to
reference this spec.

## 10. Phases

| Phase | Delivers | Blocked on |
|---|---|---|
| **G0** | Link grammar and lint (§ 6) in migration mode; `DELIBERATOR_SCHEMA` in code; `graph.json` contract | `lattice-graph` installable (§ 11) |
| **G1** | `deliberator graph build` from structured and layout facts; CI drift gate; survival (§ 8.1) | engine writing v4.2.0 JSON; schema 1.1.0 fields (§ 5.1) |
| **G2** | Concession harvest and DPO export (§ 8.2); calibration (§ 8.3); cross-run `deliberator graph query` over a directory of `graph.json` files, in NetworkX | G1 |
| **G3** | Configuration ladder (§ 8.4); decisive-evidence credit (§ 8.5) | enough blind runs (§ 8.3 `n`) |
| **G4** | Memgraph index: `deliberator graph load` runs `lattice_graph.projection.statements` through one gateway; MAGE only if a query needs it | a concrete need: live in-run queries, or cross-run queries too slow in NetworkX |
| **G5** | Challenge ladder mode (§ 8.6) pilot | G1–G2 results |

Neo4j/GDS: only for a concrete algorithm or customer need, and never alongside Memgraph.
Preferred or stable semantics (ASPARTIX or another ICCMA solver): only as an optional extra if a
mechanic needs it; none here does.

Packaging: everything graph-related is behind an optional extra, `deliberator[graph]`
(`lattice-graph`, `networkx`), so the core install is unchanged.

## 11. Requests to Lattice (`lattice-graph`)

Sent to the Lattice session; Deliberator does not redefine any of these.

1. **Python range.** `lattice-graph` declares `requires-python >=3.12,<3.13`. Deliberator
   declares `>=3.12`. On Python 3.13 or later `deliberator[graph]` would be uninstallable. Ask:
   widen to `>=3.12`.
2. **Concession semantics.** `from_projection` withdraws every `CONCEDES` target, whoever authored
   the concession and whatever its scope. Ask: (a) document that `CONCEDES` targets the
   conceder's own argument, and (b) only withdraw when the `Concession`'s author also authored
   the target. Otherwise one participant can "concede" another's claim and delete it.
3. **`CITES` endpoints.** `CITES` targets `Principle`, `Evidence` and `Ruling` only, and `combine`
   forbids widening it. Ask: allow a host to extend an edge type's endpoints (an explicit
   `extend` rather than a silent merge), or widen `CITES` to any node type. Until then Deliberator
   uses `GROUNDED_IN` (§ 7.2).
4. **Parallel edges collapse.** `to_networkx` keys parallel edges by type, and `statements`
   writes `MERGE (a)-[r:TYPE]->(b) SET r += $props`. Two `PREFERS` edges from one ruling to one
   claim with different `over` (a three-way dispute), or two `CITES` with different line ranges,
   collapse into one edge, and the second `over` overwrites the first. Ask: an optional edge
   `key` property that is part of edge identity in both NetworkX and the MERGE.
5. **Host schema version in node-link.** `FORMAT` versions the container. Ask: an optional
   `schema` and `schema_version` field in `node_link`, checked by `from_node_link`, so hosts
   don't each wrap it. Deliberator wraps it until then (§ 9.1).
6. **Licence and publication.** Deliberator is Apache-2.0. It can depend on `lattice-graph` only
   once it is on PyPI under a compatible permissive licence. Brian decides when and which.

## 12. Success criteria

- **SC-1** `deliberator graph build` on the same inputs produces byte-identical `graph.json`.
- **SC-2** Every `[[…]]` link in `specs/` and `deliberations/` resolves; CI fails on one that does
  not.
- **SC-3** On three showcase runs with hand-checked fixture graphs, `structured` edges match the
  fixture exactly, and the survival labels match a hand computation.
- **SC-4** Before any score is shown in a UI: on those runs, survival labels are compared with what
  a human reviewer marked as useful (note §11, open question 3). If they don't correlate, the UI
  is not built.
- **SC-5** Calibration reports agreement only with `n ≥ 20` paired questions and always shows
  `n`.
- **SC-6** No score, label or rating appears in any prompt the engine sends (checked by test).
- **SC-7** Loading the same `graph.json` set into Memgraph twice yields the same node and edge
  counts (G4).

## 13. Open questions

1. Should arbiter `PREFERS` edges themselves be attackable (a higher-order game)? Not in v1.
2. Should rulings overturned by `SUPERSEDES` lose authority in a precedent ranking? Its
   manipulation properties are unknown; not in v1.
3. Does a self-consistency run's arbiter count as a different `Configuration` from the
   originating one when only the prompt stage differs? Proposed: yes, keyed by role-prompt hash.
4. What should the 60-day link-migration window be measured from: merge date or the first
   release that ships the lint?
