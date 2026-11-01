# Graph-data-structure game theory for Deliberator (and Lattice)

**Date:** 2026-11-01
**Author:** research note for Brian Slater (Build Fractal)
**Status:** research. Nothing here is a spec or a decision.
**Question:** If Deliberator's storage moves to a graph, which games can be built where the
*state* is the stored graph, the *moves* are graph mutations, and the *payoff or winner* is a
graph query or algorithm? What schema supports them, and which backend should come first?

How this note separates things:

- **Fact** sections state what the literature or the documentation says, with a URL for each
  claim. Claims I could not confirm from a primary or near-primary source are marked
  **UNVERIFIED**.
- **Recommendation** sections are my proposals. They are labelled as such.
- Classic network games on a *fixed* graph (congestion games, network formation and so on)
  are background only and are mostly left out.

---

## 0. Grounding: what Deliberator already stores, and how

These observations come from the repository at this commit, not from outside sources.

- The pipeline is fixed: agents review a target, cross-review each other, revise, record the
  disputes that remain, and an arbiter rules (`README.md`). Each phase is written to disk
  under `deliberations/<id>/<agent>/{review,cross-reviews/*,revision,revision_2,disputes}.md`,
  with `arbitration/resolution.md` and `summary/final.md`.
- The disputes files already have the shape of an argument graph. Each dispute lists
  "My claim", "Opposing position(s)", "Why I will not concede", "Counter-argument" and a
  "Proposed resolution path" (for example
  `deliberations/v4.2.0-structured-deliberation-outputs-blind-2026-05-13/risk-auditor/disputes.md`).
- The arbiter's resolution lists the principles it relies on by number, with line ranges
  ("Principle VIII (Templating Engines Over Inference) … (L161-183)"). For each dispute it
  gives the positions, a ruling, a grounding citation, a rejected position and the required
  changes ("§ 11 implementation order must specify …").
- Specs then cite rulings by hand: "Self-consistency arbitration 2026-05-12 at
  `deliberations/v4.1.0-…-self-consistency-2026-05-12/arbitration/resolution.md` (commit
  `8f90e2d`) … Four D-conditions (D1-D4) produced v4"
  (`specs/v4.1.0-persistence-contract-discipline/spec.md`). The v4.2.0 spec has an F-condition
  ledger whose columns are `F# | Summary | Lands in`, with rows such as `F1 … | § 11, § 9.1`
  (`specs/v4.2.0-structured-deliberation-outputs/spec.md`). Older reviews use D1–D3 rows
  marked "Conceded at P2" or "Accepted at P2"
  (`specs/done/009-guided-execution/conversus-review/round-2/*/revision.md`).
- `specs/ideas.md` already plans "YAML output now → Memgraph/pgvector when game engine
  materializes → cross-run analysis". Under "Deliberation as Training Data" it sketches Cypher
  such as `MATCH (a:Agent)-[:CONCEDED]->(p:Position)<-[:CHALLENGED]-(b:Agent)`.
- Spec 046 (commentator agents) already defines a `commentary/graph.jsonl` stream of
  `entity`, `relation` (e.g. `conceded_to`), `event` and `pattern` records, and its SC-007 asks
  for cross-run queries such as "how many times has fp-guru conceded?".
- `schema/game-forms/` has normal-form, coalitional (with `solution_concept: shapley`),
  Stackelberg, Bayesian, repeated and other forms. All of them score fixed payoff tables
  extracted from text. None of them treats the record itself as the game state. That gap is
  what this note is about.
- Lattice already has this design. `designs/versioned-graph/design.md` stores history in
  Memgraph as `(:Commit)-[:PARENT]->(:Commit)`, `(:Commit)-[:CONTAINS]->(:Change)` and
  `(:Commit)-[:FROM_PROPOSAL]->(:Proposal)`, and Lattice's `CONSTITUTION.md` keeps "SQLite,
  Postgres, Memgraph and NetworkX" in adapter packages. Lattice's `VISION.md` says "Everything
  is a proposal" and "The users are the mechanical Turks".

So the hand-placed backlinks are already a typed graph. It is just written as prose.

---

## 1. Abstract argumentation: the closest fit

### 1.1 Facts

**Dung frameworks.** Dung (1995) defines an argumentation framework as a set of arguments
and a binary *attack* relation. Semantics then pick out acceptable sets of arguments, called
extensions. The paper's title already links this to "n-person games"
([Vidal library record](https://jmvidal.cse.sc.edu/lib/dung95a.html); *Artificial
Intelligence* 77(2):321–357). The **grounded** extension is the least fixed point of Dung's
defence function ([Grossi & Modgil, IJCAI 2015](https://object.cloud.sdsc.edu/v1/AUTH_da4962d3368042ac8337e2dfdd3e7bf3/ml-papers-txt/IJCAI/2015/on_the_graded_acceptability_of_arguments__052ee36f.txt)).
**Preferred** extensions are maximal admissible sets. **Stable** extensions attack every
argument outside themselves. (These two definitions are standard textbook material. I did not
re-fetch them from Dung's text, so treat the wording as **UNVERIFIED**.)

**Complexity.** Grounded acceptance can be decided in polynomial time
([Lehtonen et al., KR 2024](https://proceedings.kr.org/2024/49/kr2024-0049-lehtonen-et-al.pdf)).
Skeptical acceptance under preferred semantics is Π₂ᵖ-complete
([Dvořák, Järvisalo, Wallner & Woltran, AIJ 2014](https://www.cs.helsinki.fi/u/mjarvisa/papers/dvorak-jarvisalo-wallner-woltran.aij14.pdf);
[Bengel et al., KR 2025](https://proceedings.kr.org/2025/13/kr2025-0013-bengel-et-al.pdf)).
In practice, grounded semantics is cheap enough to recompute on every write. Preferred
semantics needs a solver.

**Dialogue (discussion) games.** Acceptance can be proved by a two-player game. The
proponent tries to establish an argument and the opponent tries to block it, and the
proponent's burden is heavier: the opponent only needs to win one branch. Caminada and
Podlaszewski show that an argument is in the grounded extension if and only if the proponent
can persuade a maximally sceptical opponent in a Mackenzie-style dialogue
([COMMA paper](https://mysite.cs.cf.ac.uk/CaminadaM/publications/COMMA_grounded_game.pdf);
[BNAIC demo](https://mysite.cs.cf.ac.uk/CaminadaM/publications/BNAIC_grounded_demo.pdf)).
Modgil and Caminada (2009) is the standard reference for argument-game proof theories, as
cited by [Soto et al., KR 2025](https://proceedings.kr.org/2025/54/kr2025-0054-soto-et-al.pdf).
That paper also treats acceptance as a two-party zero-sum dialogue game. Skeptical preferred
semantics has a two-phase game
([JELIA 2016](https://www.cl.cam.ac.uk/~zs315/papers/JELIA2016.pdf)).

**Bipolar frameworks** add a *support* relation, disjoint from attack. Support chains combine
with attacks into "supported" and "secondary" (indirect) attacks
([Cayrol & Lagasquie-Schiex line, ORBilu record](https://orbilu.uni.lu/handle/10993/14507);
[Potyka, KR 2020](https://proceedings.kr.org/2020/69/kr2020-0069-potyka.pdf)). Oren, Norman
and Preece revised some bipolar semantics for evidential reasoning
([ArgMAS 2007](https://users.cs.cf.ac.uk/A.D.Preece/publications/download/argmas2007.pdf)).
This matters for Deliberator, because "evidence supports a claim" is as common as "a claim
attacks a claim".

**Gradual (weighted) semantics** give each argument a number instead of in/out.
- *h-categoriser:* this goes back to Besnard and Hunter's argument trees
  ([AIJ 128, 2001](https://www.cs.uni-potsdam.de/wv/publications/DBLP_journals/ai/BesnardH01.html)).
  The usual form is `h(a) = 1 / (1 + Σ_{b attacks a} h(b))`. That exact formula is from
  memory and is **UNVERIFIED** against the primary text. The worked values in
  [this extension-ranking paper](https://arxiv.org/pdf/2504.21683) are consistent with it.
- *Ranking-based semantics:* Amgoud and Ben-Naim turn any attack graph into a ranking from
  most to least accepted, and their burden-based semantics compares burden vectors
  lexicographically ([Amgoud & Ben-Naim](https://www.irit.fr/~Jonathan.Ben-Naim/documents/amgoudBennaim1.pdf);
  [α-BBS, KR 2016](https://www.irit.fr/~Jonathan.Ben-Naim/documents/2016/amgoudBennaimDoderVesicKR16.pdf)).
- *DF-QuAD* (Rago, Toni, Aurisicchio & Baroni, 2016) works on attack-and-support graphs that
  have base scores. It merges each argument's attackers into one force and its supporters into
  another, then moves the base score up or down by whichever force is larger. Unlike the
  earlier QuAD, it is discontinuity-free
  ([Imperial Spiral](https://spiral.imperial.ac.uk/handle/10044/1/41698);
  [CAF 2016 slides](https://www.cs.cf.ac.uk/caf2016/assets/slides/Rago.pdf)). The
  aggregation is `F(v₁..vₙ) = 1 − Π(1 − vᵢ)`. The combination is `v₀ − v₀·|vs−va|` when the
  attack force `va` is at least the support force `vs`, and `v₀ + (1−v₀)·|vs−va|` otherwise.
  Both formulas are from memory and **UNVERIFIED** against the paper text.
- *Attribution inside the graph:* Yin, Potyka and Toni define Shapley-based **Relation
  Attribution Explanations** that score each attack or support edge's contribution to a
  topic argument's strength. Exact computation is exponential, so they give a sampling
  approximation ([IJCAI 2024 / arXiv 2404.14304](https://arxiv.org/abs/2404.14304)). This links
  §1 to §3 directly.

**Tools.** ASPARTIX encodes each semantics as an answer-set program, and extensions
correspond to answer sets
([ASPARTIX-V, ASPOCP 2021](https://dbai.tuwien.ac.at/research/argumentation/aspartix/papers/ASPOCP_2021.pdf);
[arXiv 2109.03166](https://arxiv.org/abs/2109.03166)). ICCMA, the International Competition on
Computational Models of Argumentation, is biennial and started in 2015
([ICCMA'15 system descriptions](https://arxiv.org/pdf/1510.05373)). Editions after 2021 and
current solver rankings are **UNVERIFIED** here.

### 1.2 Mapping onto deliberation (recommendation)

| Deliberator artefact | Argumentation object |
|---|---|
| A recommendation or "My claim" in `review.md` / `disputes.md` | Argument (a `Claim` node) |
| A cross-review objection, or "Counter-argument to their position" | `ATTACKS` edge (Challenge → Claim) |
| Evidence quoted with a file and line | Supporter in a bipolar framework (`SUPPORTS`) |
| "Withdrawn" / "Conceded at P2" in a revision | The agent retracts its own argument, or accepts that an attack succeeds (`CONCEDES`) |
| "Modified" | A new argument that `SUPERSEDES` the old one |
| Arbiter ruling with "Rejected position" | An external preference that turns one attack into a *defeat* and blocks the reverse attack |
| "Grounding citation: Principle VIII" | `CITES` a `Principle` node. Principles act as unattackable base arguments within a run |

The fit is close because Deliberator already runs the game: cross-review is the opponent's
move, revision is the proponent's reply, and arbitration is the referee. What the graph adds
is that the outcome can be *computed*, not just narrated.

---

## 2. Combinatorial and extensive-form games whose positions are graphs

### 2.1 Facts

- **Hackenbush** is played on a picture of coloured edges connected to a ground line. A move
  deletes an edge, and everything no longer connected to the ground falls away. Blue-Red
  Hackenbush positions have values that are surreal numbers. Adding green edges gives
  nimbers such as ∗ ([Hackenbush](https://en.wikipedia.org/wiki/Hackenbush)). Conway's
  *On Numbers and Games* connects the theory of games with the theory of transfinite numbers
  ([ONAG prologue](https://www.cut-the-knot.org/books/ONAG/prologue.shtml)). *Winning Ways*
  (Berlekamp, Conway & Guy, 1982) covers "adding games" including Hackenbush
  ([Winning Ways](https://en.wikipedia.org/wiki/Winning_Ways_for_Your_Mathematical_Plays)).
- In Conway's theory, a game *is* its pair of option sets {L | R}, defined recursively. So a
  game is a rooted DAG of positions. (This is standard CGT. I did not quote it from ONAG
  directly, so it is **UNVERIFIED** as wording.)
- **Extensive-form games** are stored as trees: chance, player and terminal nodes, with
  information sets. OpenSpiel is DeepMind's open framework for search and RL over n-player,
  sequential or simultaneous, perfect- or imperfect-information games
  ([Lanctot et al., arXiv 1908.09453](https://arxiv.org/abs/1908.09453)).
- **Infinite games on graphs** (briefly). In reachability and parity games, two players move
  a token along the edges of a graph, and the winner depends on which vertices or priorities
  the play visits. Parity games can be decided in quasipolynomial time
  ([Calude et al., STOC 2017](https://www.cs.auckland.ac.nz/~cristian/crispapers/paritygame-stoc.pdf)),
  which also gives quasipolynomial μ-calculus model checking
  ([Computational Complexity blog](https://blog.computationalcomplexity.org/2024/09/favorite-theorems-parity-games.html)).
  Whether parity games can be solved in polynomial time is still open
  ([Parys](https://ar5iv.labs.arxiv.org/html/1904.12446)).
- **Debate as a game for AI oversight.** Irving, Christiano and Amodei propose a zero-sum
  debate in which two agents take turns making statements and a human judges. In an MNIST
  toy setting, debate raised a sparse classifier's accuracy from 59.4% to 88.9% with 6 pixels
  ([arXiv 1805.00899](https://arxiv.org/abs/1805.00899)).

### 2.2 What this gives Deliberator (recommendation)

- A deliberation run *is* an extensive-form game tree: phases are plies, agents are players,
  and blind runs (where agents cannot see each other's output) are imperfect information.
  Storing `Run → Phase → Move` with `NEXT` edges makes every past run a replayable game
  record. OpenSpiel-style analysis then becomes possible later, for example "what should an
  agent have conceded?".
- The **Hackenbush view of a dispute** is useful as a mental model. A claim stays standing
  while some chain of `SUPPORTS` edges connects it to "ground" (a `Principle` or verified
  `Evidence`). An attack that cuts the last support drops everything above it. That is a
  reachability query, and it turns "unsupported claim" into a computed state rather than a
  reviewer's judgement.
- Parity and reachability games are more than Deliberator needs today. They become relevant
  if anyone wants to check *protocol* properties, such as "every dispute eventually
  reaches a ruling".

---

## 3. Cooperative games over graphs: crediting contributions

### 3.1 Facts

- **Myerson value.** Given a TU game and an undirected graph of who can cooperate with whom,
  the Myerson value is the Shapley value of the graph-restricted game, in which a coalition is
  worth the sum of its connected components' worths. It is the unique rule that satisfies
  component efficiency and *fairness*: adding a link changes the two endpoints' payoffs by the
  same amount. It coincides with the Shapley value when the graph is connected
  ([Myerson value](https://en.wikipedia.org/wiki/Myerson_value); *Math. Oper. Res.*
  2(3):225–229, 1977, DOI 10.1287/moor.2.3.225;
  [Leipzig lecture notes](https://www.wifa.uni-leipzig.de/fileadmin/Fakult%C3%A4t_Wifa/Institut_f%C3%BCr_Theoretische_Volkswirtschaftslehre/Professur_Mikro%C3%B6konomik/Angewandte_Koop_Spieltheorie/Vorlesung10Graphen.pdf)).
- **Shapley value of database facts.** Livshits, Bertossi, Kimelfeld and Sebag score how much
  each tuple contributes to a query answer. They identify tractable query classes and give
  approximations for the hard ones
  ([ICDT 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICDT.2020.20)).
  Later work computes these values from Boolean *provenance* compiled into circuits
  ([arXiv 2112.08874](https://arxiv.org/pdf/2112.08874)). Bertossi and Kimelfeld survey the
  area ([survey](https://arxivlens.com/paperview/details/the-shapley-value-in-database-management-7110-1373433)).
- **Data Shapley.** Ghorbani and Zou value training points with Shapley values, using Monte
  Carlo and gradient estimators. Low-value points tend to be outliers or corrupted labels
  ([ICML 2019](https://proceedings.mlr.press/v97/ghorbani19c.html)).
- **Shapley over argument edges:** see Yin, Potyka and Toni in §1.1
  ([arXiv 2404.14304](https://arxiv.org/abs/2404.14304)).
- Shapley-style credit can be inflated by submitting duplicate or near-duplicate
  contributions (replication). I believe there is literature on this, but I did not find a
  primary source in this pass, so it is **UNVERIFIED**.

### 3.2 Crediting a curated graph (recommendation)

The value function should be defined *by a graph query*, so the game is pinned to the
stored record:

> v(S) = number (or weight) of `Ruling` nodes whose winning `Claim` stays IN under grounded
> semantics when only `Evidence` contributed by agents in S is kept.

This is a provenance game, in the sense of Livshits et al. The Myerson restriction is natural
when S must also be connected through `CITES` or `RESPONDS_TO` edges. Evidence that nobody
built on then earns nothing, which is the fairness property doing useful work. Deliberator
already declares `solution_concept: shapley` in `schema/game-forms/coalitional.yml`. The new
step is to compute v from the graph instead of from extracted text.

---

## 4. Mechanisms for truthful crowd curation

### 4.1 Facts

- **Peer prediction** (Miller, Resnick & Zeckhauser, 2005). Each rater reports a signal. The
  report is scored, with a proper scoring rule, against the beliefs it implies about another
  rater's report. Truth-telling is then a strict Bayesian Nash equilibrium
  ([Resnick's page](https://presnick.people.si.umich.edu/papers/elicit/index.html);
  *Management Science* 51(9):1359–1373). People in lab experiments do not always tell the
  truth under these mechanisms, possibly because the mechanisms have several equilibria
  ([arXiv 1603.07319](https://arxiv.org/pdf/1603.07319)).
- **Bayesian Truth Serum** (Prelec, 2004). Each person gives an answer and a prediction of
  how others will answer. Answers score well when they are "surprisingly common", meaning more
  common than the group predicted, which removes the bias towards consensus
  ([summary](https://stafforini.com/works/prelec-2004-bayesian-truth-serum/);
  *Science* 306:462–466).
- **Effort-aware agreement** (Dasgupta & Ghosh, 2013). The mechanism pays for agreeing with a
  reference rater on the same task, then subtracts a statistic that penalises blind
  agreement, so only effort pays. Full effort with truthful reports gives every agent its
  highest payoff ([arXiv 1303.0799](https://arxiv.org/abs/1303.0799)).
- **Games with a purpose.** In the ESP game, two players who cannot communicate both see an
  image and score when they type the same word. Taboo words push them towards new labels. A
  pair produced about 3.89 labels per minute
  ([CHI 2004, dblp](https://dblp.uni-trier.de/rec/conf/chi/AhnD04.html);
  [ESP game](https://en.wikipedia.org/wiki/ESP_game)). Von Ahn and Dabbish later generalised
  this into templates: *output-agreement* (ESP), *inversion-problem* (Peekaboom) and
  *input-agreement* (TagATune)
  ([overview](https://en.wikipedia.org/wiki/Human-based_computation_game); the original CACM
  2008 text was not fetched, **UNVERIFIED** in detail).
- **Knowledge-graph curation games.**
  - Magnus Manske's *Wikidata Game* was succeeded by the *Distributed Game*. Its sub-games
    are plugged in through JSON, and its tasks are yes/no answers designed for mobile
    ([Phabricator T243146](https://phabricator.wikimedia.org/T243146);
    [Manske slides](https://docs.google.com/presentation/d/1-zDD9w02ry8dr9BIGncQGub7ibkKBQBgKeP_ef0s2Js/htmlpresent)).
    A 2026 Google Summer of Code project is reviving it
    ([T387248](https://phabricator.wikimedia.org/T387248)). Edit volumes and accuracy figures
    are **UNVERIFIED**.
  - *OntoGame* (Siorpaes & Hepp) hides Semantic Web annotation tasks inside multiplayer
    games. For example, OntoPronto classifies eBay goods against eClassOWL. The evidence for it
    was preliminary ([ESWC 2008](https://link.springer.com/doi/10.1007/978-3-540-68234-9_54);
    *IEEE Intelligent Systems* 23(3), DOI 10.1109/MIS.2008.45).
- **Crowd science.** Foldit players produced models good enough to solve the structure of the
  Mason-Pfizer monkey virus protease after more than a decade of failed attempts
  ([Baker lab](https://www.bakerlab.org/2015/11/26/crystal-structure-of-a-monomeric-retroviral-protease-solved-by-protein-folding-game-players/);
  PDB [3SQF](https://rcsb.org/structure/3sqf)). Phylo turned multiple sequence alignment
  into a casual puzzle. More than 12,000 users submitted more than 350,000 solutions and
  improved up to 70% of the alignment blocks considered
  ([PLoS ONE 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3296692)).

### 4.2 Lesson for a graph store (recommendation)

All of these mechanisms score a contributor *against other contributors' graph writes*, not
against an oracle. In graph terms, each task is a small subgraph, such as a candidate
`SAME_AS` edge. Each answer is a proposed edge, and the score is a query over the set of
proposed edges for that task. Deliberator already has the two independent reports that peer
prediction needs: the *blind* and *self-consistency* arbitrations of the same spec
(`deliberations/*-blind-*` and `*-self-consistency-*`). They are an output-agreement game that
nobody scores yet.

---

## 5. Reputation and ranking as graph algorithms

### 5.1 Facts

- **PageRank** ranks nodes by the stationary distribution of a random surfer (Page, Brin,
  Motwani & Winograd, Stanford InfoLab 1999, `http://ilpubs.stanford.edu:8090/422/`. That URL is
  from memory and was not fetched, so it is **UNVERIFIED**).
- **EigenTrust** computes global trust from local trust ratings by distributed power
  iteration, anchored on pre-trusted peers. In simulation it substantially reduced
  inauthentic downloads even when malicious peers colluded
  ([Kamvar, Schlosser & Garcia-Molina, WWW 2003](https://zoo.cs.yale.edu/classes/cs457/fall13/Eigentrust.pdf)).
  The claim that it held up with up to 70% malicious peers comes from a search summary and is
  **UNVERIFIED**.
- **Manipulation resistance.** Cheng and Friedman show that no *symmetric* reputation
  function is sybilproof, and they construct asymmetric "flow-like" ones that are
  ([summary](https://ericfode.github.io/agent-harness-wiki/raw/papers/cheng-friedman-2005-sybilproof-reputation-mechanisms);
  [Friedman talk abstract](https://www.cs.cornell.edu/~kash/abstracts/april3_07.htm)). Sybil
  attacks are especially powerful against global mechanisms such as PageRank, and still
  effective against personalised PageRank
  ([Liu, Parkes & Seuken, AAMAS 2016](https://econcs.seas.harvard.edu/resource/liuaamas16pdf);
  see also [AAMAS 2021](https://archive.illc.uva.nl/AAMAS-2021/pdfs/p1263.pdf) on Seuken and
  Parkes's impossibility result).
- **Pairwise-comparison graphs.** TrueSkill generalises Elo. It tracks uncertainty, models
  draws, handles many players and teams, and is inferred by message passing on a factor graph
  ([Herbrich, Minka & Graepel, NIPS 2006](https://papers.nips.cc/paper_files/paper/2006/file/f44ee263952e65b3610b8ba51229d1f9-Paper.pdf)).
  Chatbot Arena fits a Bradley-Terry model to crowdsourced pairwise votes between anonymous
  LLMs, with confidence intervals and active pair sampling
  ([Chiang et al., ICML 2024](https://arxiv.org/abs/2403.04132)).
- **Q&A reputation.** On Stack Exchange, reputation unlocks privileges, starts at 1 and
  cannot fall below 1, and accepting your own answer earns nothing
  ([Stack Overflow for Teams help](https://stackoverflowteams.com/help/whats-reputation)).
  The "+10 per upvote" figure comes only from mirrors, so it is **UNVERIFIED**.
- **Edit wars.** Most Wikipedia articles are peaceful. Conflict comes in bursts, memory
  effects matter, a few editors fight most wars, and there are three long-run patterns,
  including articles that reach consensus and articles that never do
  ([Yasseri et al., PLoS ONE 2012](https://arxiv.org/abs/1202.3643)).

### 5.2 Lesson (recommendation)

Ranking on the deliberation graph is straightforward. The main risk is **sybils and
collusion**. In Deliberator, "agents" are prompts that the operator configures, so one person
can create unlimited sybils for free. Global PageRank over `ENDORSES` edges between agents is
therefore the wrong primitive. Use personalised or pre-trusted anchors, as EigenTrust does, and
score agents on outcomes the arbiter fixed, not on what peers said about them.

---

## 6. Deliberation and opinion graphs in the wild

### 6.1 Facts

- **pol.is.** Participants vote agree, disagree or pass on short statements. Polis groups
  participants with k-means over their vote patterns, and a PCA projection shows the opinion
  space ([Computational Democracy Project: opinion groups](https://compdemocracy.org/opinion-groups)).
  It is open source under AGPL-3.0 ([open-source page](https://compdemocracy.org/open-source)).
  A 2026 empirical study looks at 119 Polis conversations
  ([arXiv 2608.28368](https://arxiv.org/pdf/2608.28368)). The Small et al. 2021 *Recerca*
  paper on Polis's algorithms was not retrieved and is **UNVERIFIED**.
  **Name note:** pol.is / Polis (the Computational Democracy Project) has no connection that I
  found to The Polis Center, the Indianapolis research centre Brian is partnering with. Keep
  the two names apart in any public write-up.
- **Kialo** structures a debate as a tree. The thesis is the root, and every claim is a pro or
  con of exactly one parent. Research datasets include Durmus et al.'s 47,219 claims over 741
  topics with impact votes ([arXiv 2106.00976](https://arxiv.org/pdf/2106.00976)) and a 1,560
  discussion snapshot ([GraphNLI, arXiv 2202.08175](https://arxiv.org/pdf/2202.08175)).
- **Liquid democracy.** Delegations form a directed graph, and votes flow to sinks (voters
  who delegate to no one). Purely local delegation mechanisms cannot be guaranteed to beat
  direct voting, but a non-local mechanism provably can under mild assumptions
  ([Kahng, Mackenzie & Procaccia, JAIR 2021](https://jair.org/index.php/jair/article/view/12261)).

### 6.2 Lesson (recommendation)

Kialo's single-parent tree is too weak for Deliberator, because one piece of evidence often
attacks several claims, so Deliberator needs a DAG with cycles allowed. Polis shows a scoring
idea that is cheap and hard to game: rather than rewarding the majority, reward statements
that win agreement *across* opinion clusters. In Deliberator, a recommendation that agents
with different lenses (risk-auditor, naive-reader, external-scholar) all keep is worth more
than one kept by three similar agents. Liquid-democracy graphs are a model for arbiter
delegation, such as an arbiter delegating a sub-question to a specialist. They need cycle
detection, which is a graph query.

---

## 7. Implementation: what each backend gives you

### 7.1 Facts

- **Plain text with links.** Obsidian's internal link syntax is `[[Note]]` or `[[Note|text]]`.
  Backlinks and the graph view are derived from those links. Links written in HTML do not
  appear in either ([Obsidian help](https://help.obsidian.md/Linking%20notes%20and%20files/Internal%20links);
  [forum report](https://forum.obsidian.md/t/internal-links-using-html-do-not-appear-as-backlinks-or-show-up-in-graph-view/36559)).
  Logseq follows a similar outline-and-link model (**UNVERIFIED**, not checked this pass).
- **NetworkX** is an in-memory Python library. `node_link_data` and `node_link_graph`
  round-trip a graph to JSON, and since 3.4 the `link` keyword is deprecated in favour of
  `edges` ([NetworkX docs](https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.json_graph.node_link_data.html)).
  It includes PageRank and a large algorithm library. I did not fetch the algorithm reference
  page in this pass, so the specific algorithm list is **UNVERIFIED**.
- **Memgraph + MAGE.** MAGE is the open-source library of Memgraph query modules, written in
  C, C++, Python or Rust and called from Cypher. It includes `pagerank.get()`, a streaming
  `pagerank_online`, Louvain community detection and `community_detection_online`
  ([MAGE on GitHub](https://github.com/memgraph/mage);
  [query modules](https://memgraph.com/docs/memgraph-lab/features/query-modules)). Triggers
  fire on CREATE, UPDATE or DELETE for nodes or edges, and run either BEFORE COMMIT (inside
  the transaction) or AFTER COMMIT (asynchronously). They expose `createdVertices`,
  `createdEdges` and similar variables, and they persist on disk
  ([Memgraph triggers](https://memgraph.com/docs/fundamentals/triggers)). Lattice already uses
  Memgraph for its versioned history (`lattice/designs/versioned-graph/design.md`). Licence
  terms for Memgraph and MAGE were not checked and are **UNVERIFIED**.
- **Neo4j + GDS.** The Graph Data Science library's Community Edition includes all
  algorithms, including PageRank and Louvain, but caps concurrency at 4 and the model catalogue
  at 3 models, and has no Arrow import/export or catalogue backup
  ([GDS introduction](https://neo4j.com/docs/graph-data-science/current/introduction/)).
  Neo4j database licensing was not checked, so it is **UNVERIFIED**.
- **Argumentation solvers** (ASPARTIX and the other ICCMA entrants, §1.1) read their own
  formats. Exporting the attack subgraph is a few lines of code.

### 7.2 Adoption order (recommendation)

1. **Markdown stays the source of truth. Add a parser and a derived NetworkX graph.** This
   follows the project's own Principle XI (single source of truth: "All other representations
   MUST be derived from that source"), which the arbiter cites in
   `deliberations/v4.2.0-…-blind-2026-05-13/arbitration/resolution.md`. Make the existing
   hand-written references machine-readable with a small, strict link grammar, for example
   `[[ruling:v4.1.0-…-self-consistency-2026-05-12#Q2]]`, `[[principle:XI]]`, `[[spec:v4.2.0#§11]]`,
   `[[commit:8f90e2d]]`. Lint it the way `linter/` already lints. Build the graph in NetworkX
   and write a `graph.json` (node-link) next to each run, which supersedes the free-form
   `graph.jsonl` in spec 046. Every mechanic in §9 can run here first, in CI, for no extra cost
   and with no new service.
2. **Memgraph as a rebuildable index** once you need any of these: live queries *during* a
   deliberation (convergence detection, as `ideas.md` plans), triggers that score each move as
   it is written, or cross-run queries over hundreds of runs. Load it from the same
   `graph.json`, so it can always be thrown away and rebuilt. This also matches Lattice, so the
   two products can share Cypher, a schema file and the query gateway (Lattice's cypher-guard
   design).
3. **Neo4j + GDS only if needed later.** Choose it if a specific GDS algorithm or the Neo4j
   ecosystem is required, or for a hosted customer that already runs Neo4j. The Community
   concurrency cap of 4 is not a problem at this scale. Running two Cypher databases is.
4. **ASPARTIX or another ICCMA solver as an optional extra**, only for preferred or stable
   semantics. Grounded labelling is about 20 lines of Python (see §9.1).

---

## 8. Proposed graph schema for Deliberator (recommendation)

### 8.1 Node labels

| Label | Key properties | Source in today's files |
|---|---|---|
| `Run` | `id`, `kind` (originating / self-consistency / blind / rerun), `mode`, `date`, `config_hash` | `deliberations/<id>/conversus.yml` |
| `Phase` | `run_id`, `name` (review / cross-review / revision / revision_2 / disputes / arbitration / synthesis), `ord` | directory layout |
| `Agent` | `name`, `provider`, `model`, `role`, `lens` | config `agents:` |
| `Claim` (Position) | `id`, `text`, `priority` (P0–P3), `status` (surviving / withdrawn / modified), `grounded` (IN/OUT/UNDEC, derived), `strength` (derived) | numbered recommendations, "My claim" |
| `Evidence` | `id`, `kind` (file-line / test / quote / external URL), `locator`, `hash` | quotes with `file:line` |
| `Challenge` | `id`, `text`, `severity` | cross-review objections, "Counter-argument …" |
| `Concession` | `id`, `quote`, `scope` (full / partial / priority-change) | "Conceded at P2", "I was wrong" |
| `Dispute` | `id`, `title` | `## Dispute:` headings |
| `Ruling` | `id`, `verdict`, `confidence` (new, see 9.5), `rationale` | `arbitration/resolution.md` sections |
| `Condition` | `id` (C1…, D1…, E1…, F1…), `series`, `summary` | spec ledgers |
| `Principle` | `number` (e.g. XI), `tier`, `title`, `lines` | `CONSTITUTION.md` |
| `SpecSection` | `spec_id`, `version`, `anchor` (e.g. `§ 11`) | spec headings |
| `Commit` | `sha`, `repo`, `at` | "(commit `8f90e2d`)" |
| `Spec` / `SpecVersion` | `id`, `version` (v1…v5) | spec headers and changelogs |

### 8.2 Edge types

| Edge | From → To | Meaning |
|---|---|---|
| `AUTHORED` | Agent → Claim / Challenge / Evidence / Concession / Ruling | who made the move |
| `IN_PHASE` | any move → Phase; `OF_RUN` Phase → Run | when |
| `ATTACKS` | Challenge or Claim → Claim; also Challenge → `SUPPORTS` edge, reified as a node when needed | Dung attack |
| `SUPPORTS` | Evidence or Claim → Claim | bipolar support |
| `CONCEDES` | Concession → Claim or Challenge; `BY` Concession → Agent | retraction or acceptance |
| `SUPERSEDES` | Claim → Claim; SpecVersion → SpecVersion; Ruling → Ruling | modified claim, new version, overturned ruling |
| `DISPUTES` | Dispute → Claim (2 or more) | the positions in a dispute |
| `RULED_ON` | Ruling → Dispute | arbitration |
| `PREFERS` | Ruling → Claim (`{over: claim_id}`) | adopted and rejected positions |
| `CITES` | Ruling / Claim / Condition → Principle / Evidence / SpecSection / Ruling | grounding and precedent |
| `PRODUCES` | Ruling → Condition | "Four D-conditions (D1-D4) produced v4" |
| `LANDS_IN` | Condition → SpecSection | the "Lands in" column |
| `RESULTED_IN` | Condition → SpecVersion; `AT_COMMIT` any → Commit | provenance |
| `RESPONDS_TO` | any move → the move it answers | dialogue structure (for the §1 games) |

### 8.3 How today's hand-written references map

| Hand-written text (verbatim pattern) | Graph |
|---|---|
| "Self-consistency arbitration … at `deliberations/X/arbitration/resolution.md` (commit `8f90e2d`). Ruled Q1 PASS-WITH-CLARIFICATIONS …" | `(:SpecVersion {v4})<-[:RESULTED_IN]-(:Condition)<-[:PRODUCES]-(:Ruling {verdict})-[:OF_RUN]->(:Run {id:X})`, with `(:Ruling)-[:AT_COMMIT]->(:Commit {sha:'8f90e2d'})` |
| Ledger row `F1 \| Sequencing … \| § 11, § 9.1` | `(:Condition {id:'F1'})-[:LANDS_IN]->(:SpecSection {anchor:'§ 11'})` and `-[:LANDS_IN]->(:SpecSection {anchor:'§ 9.1'})` |
| "Grounding citation: Principle VIII … (L161-183)" | `(:Ruling)-[:CITES {lines:'L161-183'}]->(:Principle {number:'VIII'})` |
| "Rejected position: Naive-reader's parallel development approach" | `(:Ruling)-[:PREFERS {over: c_naive}]->(c_impl:Claim)`, with `(:Ruling)-[:RULED_ON]->(:Dispute)` |
| "D1 \| … \| **Conceded at P2** \| IA concedes in Round 2 …" | `(:Concession {scope:'priority-change', to:'P2'})-[:CONCEDES]->(:Claim)`, `(:Concession)-[:BY]->(:Agent {name:'integration-architect'})` |
| "SDET conceded (revision §6 item 6). Lands in Phase A." | `Concession -[:CONCEDES]-> Claim`, `Claim -[:LANDS_IN]-> SpecSection {anchor:'Phase A'}` |
| spec 046 `{"kind":"conceded_to","source":"fp-guru","target":"sdet"}` | derived: `(fp)-[:AUTHORED]->(:Concession)-[:CONCEDES]->(:Claim)<-[:AUTHORED]-(sdet)` |

Two design rules:
- Moves are **append-only**. A retraction is a new `Concession` node, never a deletion. This
  keeps every past state queryable, which is how Lattice's `Commit`/`Change` history already
  works.
- Derived properties (`grounded`, `strength`, ratings) are written by named jobs and marked
  as derived, so nobody hand-edits a score.

---

## 9. Game mechanics on that schema (recommendation)

Each mechanic lists its moves, its scoring query, the theory behind it and how it resists
gaming. The Cypher examples are written in Neo4j 5 syntax. Whether Memgraph supports
`EXISTS { … }` subqueries with an inner `WHERE` was not checked, so that is **UNVERIFIED**. If
it does not, rewrite them with `OPTIONAL MATCH … WHERE x IS NULL`. Fixed-point algorithms run in
Python (NetworkX, or a MAGE Python module) and write results back as properties.

### 9.1 Survival: grounded-extension scoring of positions

**Moves:** add a `Claim`, add `ATTACKS` or `SUPPORTS`, add a `Concession`, and (arbiter only)
add `PREFERS`.

**Scoring:** build the *defeat* graph. Take every `ATTACKS` edge, drop any attack on a
claim the arbiter `PREFERS` over the attacker, and drop attacks whose author later conceded
them. Compute the grounded labelling, then give each agent points for its claims that end IN.

```python
def grounded(G):              # G: nx.DiGraph of defeats, edge a->b means a defeats b
    lab, changed = {}, True
    while changed:
        changed = False
        for n in G:
            if n in lab: continue
            atk = list(G.predecessors(n))
            if all(lab.get(a) == "OUT" for a in atk):
                lab[n] = "IN"; changed = True
            elif any(lab.get(a) == "IN" for a in atk):
                lab[n] = "OUT"; changed = True
    return {n: lab.get(n, "UNDEC") for n in G}
```

```cypher
// After the job writes c.grounded:
MATCH (a:Agent)-[:AUTHORED]->(c:Claim)-[:IN_PHASE]->(:Phase)-[:OF_RUN]->(r:Run {id:$run})
RETURN a.name,
       sum(CASE c.grounded WHEN 'IN' THEN 3 WHEN 'UNDEC' THEN 1 ELSE 0 END) AS survival
ORDER BY survival DESC;
```

**Theory:** Dung's grounded semantics, and the Caminada/Modgil result that IN means the
proponent wins the grounded discussion game against a maximally sceptical opponent (§1.1).
Use DF-QuAD or the h-categoriser as a secondary score, `c.strength`, so that UNDEC claims
still get a ranking.

**Resistance to gaming:**
- *Spam attacks.* Grounded semantics is sceptical, so any unanswered attack makes its target
  OUT or UNDEC. Only count an `ATTACKS` edge if it has at least one `SUPPORTS` from `Evidence`
  with a resolvable locator. A linter can check this (does the file and line exist, does the
  hash match).
- *Mutual-attack stalemates* (A attacks B and B attacks A gives UNDEC for both). These are
  exactly the disputes the arbiter exists for, and its `PREFERS` edge breaks the symmetry.
  Treating arbiter preferences as attack-filters follows *preference-based argumentation*
  (Amgoud & Cayrol). That attribution is from memory, so it is **UNVERIFIED**.
- *Self-dealing.* An agent's support for its own claim earns no survival points.

### 9.2 Challenge ladder: the discussion game as a move protocol

**Moves:** alternating, enforced by the engine. The proponent puts forward a `Claim`. The
opponent must `ATTACKS` it with a new or existing argument. The proponent must answer that
attacker, and may not repeat an argument already used in this line (the grounded game's
no-repeat rule). A player who cannot move loses, or may `CONCEDES`.

**Scoring:** the winner of each line is computed. Call a line *won* for the proponent if every
opponent attack in it has an IN counter-attack by the proponent.

```cypher
// Challenges an agent faced that are still unanswered
MATCH (me:Agent {name:$agent})-[:AUTHORED]->(c:Claim)<-[:ATTACKS]-(x)
WHERE NOT EXISTS { MATCH (x)<-[:ATTACKS]-(y)<-[:AUTHORED]-(me) WHERE y.grounded = 'IN' }
  AND NOT EXISTS { MATCH (:Concession)-[:CONCEDES]->(c) }
RETURN c.id, x.id AS open_challenge;
```

**Theory:** dialogue games for grounded acceptance (§1.1). Irving et al.'s debate is the AI
version of the same zero-sum game (§2.1).

**Resistance to gaming:** the rules restrict what a move may be (no repeats, one reply per
attack per turn). A query run as a BEFORE COMMIT trigger in Memgraph, or a CI check in
NetworkX, can reject illegal moves before they are written. Stalling is impossible because
an unanswered challenge counts as a loss at phase close.

### 9.3 Concession harvest: preference pairs for DPO

**Moves:** `CONCEDES`, plus the arbiter's `PREFERS`.

**Scoring:** an agent is paid for an honest concession when the claim it gave up ends up OUT
and the claim it conceded to ends up IN, which an independent ruling confirms. It loses
points for conceding to a claim that ends OUT, which is capitulation. Every confirmed pair is
also exported as a DPO training triple. DPO trains directly on (preferred, rejected) pairs
without a separate reward model ([Rafailov et al., arXiv 2305.18290](https://arxiv.org/abs/2305.18290)).

```cypher
MATCH (cz:Concession)-[:CONCEDES]->(lost:Claim)<-[:ATTACKS]-(won)
MATCH (won)<-[:SUPPORTS]-(e:Evidence)
OPTIONAL MATCH (r:Ruling)-[p:PREFERS]->(won) WHERE p.over = lost.id
WITH cz, lost, won, collect(e.locator) AS evidence, r
WHERE lost.grounded = 'OUT' AND won.grounded = 'IN'
RETURN lost.text AS rejected, won.text AS chosen, evidence,
       r IS NOT NULL AS arbiter_confirmed, cz.quote;
```

**Theory:** the ideas.md flywheel, made precise. The pair is a preference edge, and the
grounded labelling and the ruling are two independent checks on its direction.

**Resistance to gaming:** if concessions were paid naively, agents would concede to farm
pairs. Pay only for pairs that the *outcome* confirms, de-duplicate by evidence hash, and cap
the pairs per dispute. Export only arbiter-confirmed pairs for training, so the model does not
learn from agents agreeing with each other.

### 9.4 Decisive-evidence credit: Shapley / Myerson over rulings

**Moves:** contributing `Evidence` and `SUPPORTS` edges.

**Scoring:** the cooperative game from §3.2. The players are agents (or, at finer grain,
evidence nodes). `v(S)` is the number of rulings whose preferred claim stays IN when only the
evidence from S is kept. With the Myerson restriction, coalitions count only through
connected components of the `RESPONDS_TO`/`CITES` interaction graph. Estimate by Monte Carlo
over permutations, as Data Shapley does, with each sample re-running `grounded()` on the
filtered subgraph.

```cypher
// Candidate "pivotal" evidence: removing it would flip a ruling's winner.
// This cheap first pass finds supports with no alternative IN supporter.
MATCH (r:Ruling)-[p:PREFERS]->(w:Claim)<-[:SUPPORTS]-(e:Evidence)<-[:AUTHORED]-(a:Agent)
WHERE NOT EXISTS {
  MATCH (w)<-[:SUPPORTS]-(e2:Evidence) WHERE e2 <> e AND e2.grounded <> 'OUT' }
RETURN a.name, count(DISTINCT r) AS pivotal_rulings ORDER BY pivotal_rulings DESC;
```

**Theory:** the Myerson value, Shapley values of tuples over provenance (Livshits et al.),
Data Shapley, and relation-attribution Shapley inside argument graphs (Yin, Potyka & Toni) (§3).

**Resistance to gaming:** *replication*, meaning many near-copies of one piece of evidence to
gain extra Shapley credit (the literature on this is **UNVERIFIED**, §3.1). Collapse evidence
by `hash` or by locator range before computing, so copies merge into one player. The Myerson
restriction pays nothing for evidence nobody engaged with. Cost grows exponentially if
computed exactly, so sample, and compute only per run and per ruling.

### 9.5 Arbiter calibration: blind-versus-self agreement, scored with peer prediction

**Moves:** each `Ruling` gets a stated `confidence` (new field). The same question is already
arbitrated more than once: originating, self-consistency, rerun and blind.

**Scoring:**
- *Where an outcome exists later:* a `SUPERSEDES` edge from a later ruling, or a ratified
  spec that reverses a condition. Give each arbiter a Brier score: `(confidence − survived)²`
  averaged over its rulings.
- *Where no outcome exists:* score the blind arbiter against the self-consistency arbiter on
  the same `Q` as an output-agreement game. Apply the Dasgupta-Ghosh correction: subtract the
  base rate at which two arbiters agree on *random* pairs of questions, so that rubber-stamping
  "PASS" everywhere earns nothing.

```cypher
MATCH (q:Question)<-[:RULED_ON]-(b:Ruling)-[:OF_RUN]->(:Run {kind:'blind'}),
      (q)<-[:RULED_ON]-(s:Ruling)-[:OF_RUN]->(:Run {kind:'self-consistency'})
WITH count(*) AS n, sum(CASE WHEN b.verdict_class = s.verdict_class THEN 1 ELSE 0 END) AS agree
MATCH (x:Ruling)
WITH n, agree, x.verdict_class AS v, count(*) AS c
WITH n, agree, collect(c) AS cs, sum(c) AS total
RETURN toFloat(agree)/n
     - reduce(acc = 0.0, k IN cs | acc + (toFloat(k)/total)^2) AS chance_corrected_agreement;
```

(`Question` is one Q1/Q2/Q3 item. Add it as a node if per-question rulings are split out.
`verdict_class` collapses verdict variants such as PASS-WITH-CLARIFICATIONS into a small
enum.)

**Theory:** proper scoring rules, peer prediction, BTS and Dasgupta-Ghosh (§4.1). The
project's own CONSTITUTIONAL_CONVERSATIONS.md records that the project was biased towards
ratifying its own proposals. A chance-corrected agreement score measures that bias directly.

**Resistance to gaming:** blindness (already a protocol rule) prevents copying. The
chance correction punishes always giving the same verdict. Peer prediction has uninformative
equilibria in which everyone gives the same answer
([lab evidence](https://arxiv.org/pdf/1603.07319)). That is why the Brier term on later
outcomes should dominate whenever outcomes exist.

### 9.6 Agent-pair ladder: Elo / Bradley-Terry / TrueSkill over the ruling graph

**Moves:** none beyond the normal pipeline. Every `Ruling -[:PREFERS {over}]->` edge between
claims by two different agents is one match.

**Scoring:** fit Bradley-Terry, or TrueSkill for multi-agent disputes and draws (a ruling
that adopts a merged position counts as a draw). Rate *(provider, model, role prompt)*
configurations, not names.

```cypher
MATCH (r:Ruling)-[p:PREFERS]->(w:Claim)<-[:AUTHORED]-(wa:Agent),
      (l:Claim {id:p.over})<-[:AUTHORED]-(la:Agent)
WHERE wa <> la
RETURN wa.provider + '/' + wa.model + '/' + wa.role AS winner,
       la.provider + '/' + la.model + '/' + la.role AS loser, r.id, r.run_id;
// feed rows to a Bradley-Terry / TrueSkill fit in Python
```

**Theory:** Elo/TrueSkill ([NIPS 2006](https://papers.nips.cc/paper_files/paper/2006/file/f44ee263952e65b3610b8ba51229d1f9-Paper.pdf))
and Chatbot Arena's Bradley-Terry with active pair sampling
([ICML 2024](https://arxiv.org/abs/2403.04132)). Active sampling maps onto ideas.md's
"cross-review pair trimming": fund the matchups with the most uncertainty.

**Resistance to gaming:** the arbiter, not the agents, records the result. Rate only
blind-run rulings so the arbiter cannot favour a known configuration, and report confidence
intervals. The arbiter is a single point of bias, so the ladder is only as trustworthy as the
calibration score in 9.5. Show the two together.

---

## 10. The same mechanics for Lattice (human contributors)

Lattice's model already *is* a graph-state game. "Every change is a proposal", "evidence rules
run before approval", history is `Commit`/`Change`/`Proposal` nodes, and contributors answer
micro-tasks ("Are these the same?", "What rights tier is this?") (`lattice/VISION.md`,
`designs/versioned-graph/design.md`). The mapping:

| Deliberator mechanic | Lattice version |
|---|---|
| 9.1 survival | A `Proposal` is a claim, a reviewer's objection is an `ATTACKS` edge, and attached evidence is `SUPPORTS`. A proposal is *approvable* when it is IN, which is a computed precondition for the approver alongside Lattice's existing evidence rules. |
| 9.2 challenge ladder | A structured objection flow on proposals: an objection must cite evidence, and the proposer must answer or concede. This keeps review disputes from turning into Wikipedia-style revert wars (§5.1). |
| 9.3 concession harvest | Rejected and approved proposal pairs on the same entity are labelled training data for the extraction models, for example in payer-index's crowd-verified extraction. |
| 9.4 Shapley/Myerson credit | "Every contribution is credited in the history". Credit a contributor by their Myerson value over the commits that a published merge depends on, so a dead-end branch earns nothing and a key `SAME_AS` link earns a lot. |
| 9.5 calibration / peer prediction | The Wikidata-Game pattern: route the same yes/no task to two internal contributors and score them by chance-corrected agreement. Feed earned trust from this score and from later reversals, since a `Commit` that is later reverted counts as an outcome. |
| 9.6 ladders | Probably not needed for humans. A per-domain trust score (EigenTrust over the approval graph, anchored on the organisation's pre-trusted curators) fits Lattice's "agreement and earned trust control quality" better. |

Differences to respect:
- Lattice's workforce is internal and identified, so sybil risk is lower than in open crowds.
  Collusion between colleagues, and deference to seniority, are higher risks. Keep the
  self-approval audit Lattice already plans. Blind task routing (the contributor cannot see
  the other contributor's answer) is the main defence.
- Lattice is permissioned. A score query must run through the same cypher-guard gateway, and
  a contributor's score must not leak data the contributor cannot see. Mark history and score
  labels as excluded from retrieval, as Lattice's D6 already does for `:Commit`.
- Shared code: one schema file for the argument edges (`ATTACKS`, `SUPPORTS`, `CONCEDES`,
  `PREFERS`, `CITES`), one `grounded()` module and one scoring package, used by both products.
  Lattice's `CONSTITUTION.md` already puts NetworkX and Memgraph in adapter packages, so a
  framework-agnostic scoring core fits.

---

## 11. Open questions and risks

**Goodhart.** Once survival, credit or Elo is visible to the agents (through prompts or
fine-tuning), agents will optimise the score rather than the review. Mitigations: keep scores
out of agent prompts, measure on blind runs, and rotate which mechanic counts. The repo
already contains a warning: the project found it was systematically biased towards ratifying
its own proposals (`CONSTITUTIONAL_CONVERSATIONS.md`). Any score that rewards agreement with
the arbiter makes that bias worse unless 9.5 is in place.

**Collusion and sybils.** In Deliberator, one operator configures every agent, so collusion
costs nothing. Scores are useful for *comparing configurations* and *diagnosing runs*, not as
a market among independent players. In Lattice, contributors are real people, so the
peer-prediction literature applies, including its weak points: several equilibria, and
truth-telling failures observed in the lab (§4.1). No symmetric reputation function is
sybilproof (§5.1), so trust must be anchored.

**Extraction fidelity.** Every mechanic depends on the parser getting `ATTACKS` versus
`SUPPORTS` and `CONCEDES` right from prose. An LLM extractor (spec 046's `graph-extraction.md`)
will mislabel some edges. Prefer the structured outputs from v4.2.0 (JSON-schema'd phase
outputs), where agents emit typed IDs directly, and treat LLM extraction as a fallback with a
confidence on each edge.

**Semantics choice is a value judgement.** Grounded semantics is cautious: when in doubt, a
claim is out. Preferred semantics is credulous and much more expensive. For a review tool,
cautious is the right default, but it means one well-evidenced unanswered challenge can sink
a good claim. Explain this in the UI.

**Cost.**
- Grounded labelling and Cypher scoring cost close to nothing.
- Exact Shapley is exponential. Monte Carlo needs many grounded recomputations per ruling,
  which is fine per run but not per keystroke.
- Preferred or stable semantics needs a SAT/ASP solver.
- The largest cost is *tokens*: asking agents for confidences, evidence locators and typed
  moves makes every phase output longer.

**Schema stability.** Spec 046 commits to "schema changes require a major version bump" for
`graph.jsonl`. Settle the edge vocabulary (§8.2) before anyone builds on it, and version it
under Principle XXVIII's persistence-contract discipline, which already requires a declared
`schema_version`.

**Open research questions**
1. Should arbiter `PREFERS` edges be attackable? That would make a higher-order game, close to
   Villata et al.'s attacks on support links ([ORBilu](https://orbilu.uni.lu/handle/10993/14507)).
2. Can a precedent graph (`Ruling -CITES-> Ruling`) be ranked so that rulings later overturned
   by `SUPERSEDES` lose authority? This is a PageRank-style authority score with negative
   edges, and its manipulation properties are unknown.
3. Does survival scoring correlate with what a human reviewer later finds useful? Test this
   on the existing showcase deliberations before building any UI.

---

## 12. Bottom line (recommendation)

- Keep markdown as the source of truth. Add a strict link grammar for the references you
  already write by hand. Derive a NetworkX graph and a node-link `graph.json` per run.
- Ship mechanics in this order: 9.1 survival (cheap, explainable), 9.3 concession harvest
  (directly feeds the training-data flywheel), 9.5 arbiter calibration (guards against the
  ratification bias), then 9.6 ladders, 9.4 credit and 9.2 the move-protocol game.
- Add Memgraph as a rebuildable index when live or cross-run queries are needed, sharing
  schema and gateway code with Lattice. Use Neo4j GDS only for a specific need.
