"""Trials: link review runs into one graph and keep them in bounds.

A single review run is one sample of a noisy process. This module treats a folder of runs as
trials of the same experiments and answers three questions:

1. **Which runs belong together?** Runs are linked by what they reviewed (``subject``: a hash of
   the targets) and how (``config``: reviewers, lenses, model, protocol). Same subject and
   config makes a run a ``RERUN_OF`` the first one. Declared links add ``DEPENDS_ON`` between
   subjects (B was built from A).
2. **Which findings are the same issue?** Findings on one subject are matched across runs by
   where they point (``name:line``) and what they say (word overlap). Each issue gets a
   *stand rate*: the share of the subject's runs in which it was raised and still stood.
3. **Which runs are out of bounds?** A constrained fit finds one verdict level per subject
   that stays as close as possible to every run's verdict while obeying the hard rules
   (if B depends on A, B can't be in better shape than A). It is weighted isotonic regression
   over the dependency graph, solved exactly by Dykstra's alternating projections. A run is
   out of bounds when its verdict is further than ``tolerance`` from the fit, when it misses
   issues the other runs agree on, when it alone raises a serious issue, or when its token
   use is far outside its config's usual range (median ± k·MAD).

The fit also says where the next rerun buys the most: subjects whose issues are unstable
(stand rates near one half) and whose runs are few.

Outputs, next to the runs: ``trials.json`` (machine contract), ``trials.md`` (people) and
``trials.graph.json`` (node-link JSON via lattice-graph). Declared links live in
``links.jsonl``, one ``{"kind": "depends_on", "from": ..., "to": ...}`` per line, where each
end is a run id or a subject hash.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from engine.review.protocol import Protocol, load_protocol

TRIALS_VERSION = "1.0.0"
LINKS_FILE = "links.jsonl"
_RANK = {"pass": 0, "changes": 1, "block": 2}
_VERDICTS = ("pass", "changes", "block")
_SEV_WEIGHT = {"block": 3.0, "major": 2.0, "minor": 1.0}
_STANDING = ("stands", "contested")
LinkKind = Literal["depends_on"]


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunFinding:
    ref: str
    sev: str
    claim: str
    at: str | None
    status: str


@dataclass(frozen=True)
class Run:
    run_id: str
    subject: str
    config: str
    verdict: str
    started: str
    findings: tuple[RunFinding, ...]
    tokens: int
    cost_usd: float | None
    target_names: tuple[str, ...]

    @staticmethod
    def from_review_json(data: Mapping[str, Any]) -> Run | None:
        """A run from review.json, or None when it predates subject/config (schema 1.0.0)."""
        if not data.get("subject") or not data.get("config"):
            return None
        usage = data.get("usage") or {}
        findings = tuple(
            RunFinding(
                ref=f["ref"], sev=f.get("sev", "minor"), claim=f.get("claim", ""),
                at=f.get("at"), status=f.get("status", "stands"),
            )
            for f in data.get("findings", [])
            if not f.get("duplicate_of")
        )
        tokens = int(usage.get("input_tokens") or 0) + int(usage.get("output_tokens") or 0)
        return Run(
            run_id=data["run_id"], subject=data["subject"], config=data["config"],
            verdict=data["verdict"], started=data.get("started", ""), findings=findings,
            tokens=tokens, cost_usd=usage.get("cost_usd"),
            target_names=tuple(t["name"] for t in data.get("targets", [])),
        )


@dataclass(frozen=True)
class Link:
    kind: LinkKind
    source: str  # run id or subject hash
    target: str


def load_runs(root: Path) -> tuple[list[Run], int]:
    """Every run under `root` with a 1.1.0+ review.json, and how many older ones were skipped."""
    runs, skipped = [], 0
    for path in sorted(root.glob("*/review.json")):
        try:
            run = Run.from_review_json(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError, KeyError):
            run = None
        if run is None:
            skipped += 1
        else:
            runs.append(run)
    runs.sort(key=lambda r: (r.started, r.run_id))
    return runs, skipped


def load_links(root: Path) -> list[Link]:
    path = root / LINKS_FILE
    if not path.is_file():
        return []
    links = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        links.append(Link(kind=item["kind"], source=item["from"], target=item["to"]))
    return links


def add_link(root: Path, kind: LinkKind, source: str, target: str) -> Link:
    """Append a declared link: `source` depends on `target` (run ids or subject hashes)."""
    root.mkdir(parents=True, exist_ok=True)
    with (root / LINKS_FILE).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"kind": kind, "from": source, "to": target}) + "\n")
    return Link(kind=kind, source=source, target=target)


# ---------------------------------------------------------------------------
# Matching findings across runs
# ---------------------------------------------------------------------------

_WORD = re.compile(r"[a-z][a-z0-9_]{2,}")
_STOP = frozenset(
    [
        "the", "and", "for", "with", "not", "but", "are", "was", "were", "this", "that",
        "from", "into", "when", "then", "than", "have", "has", "its", "can", "will",
        "would", "should", "could", "may", "might", "any", "all", "one", "only", "also",
        "even", "just", "does", "doesn"
    ]
)
_AT = re.compile(r"([^\s:]+):(\d+)")


def _words(text: str) -> frozenset[str]:
    return frozenset(w for w in _WORD.findall(text.lower()) if w not in _STOP)


def _where(at: str | None) -> tuple[str, int] | None:
    m = _AT.search(at or "")
    return (m.group(1), int(m.group(2))) if m else None


def _similar(a: RunFinding, b: RunFinding, *, line_slack: int = 3) -> float:
    """0..1: how likely two findings are the same issue."""
    if a.claim.strip().lower() == b.claim.strip().lower() and (a.at or "") == (b.at or ""):
        return 1.0
    wa, wb = _words(a.claim), _words(b.claim)
    overlap = len(wa & wb) / len(wa | wb) if wa and wb else 0.0
    pa, pb = _where(a.at), _where(b.at)
    near = pa is not None and pb is not None and pa[0] == pb[0] and abs(pa[1] - pb[1]) <= line_slack
    if near and overlap >= 0.12:
        return min(1.0, overlap + 0.5)
    return overlap


@dataclass
class _Cluster:
    members: dict[str, RunFinding] = field(default_factory=dict)  # run id -> finding


def match_issues(runs: Sequence[Run], threshold: float = 0.4) -> list[_Cluster]:
    """Greedy, deterministic clustering: at most one finding per run in each issue."""
    clusters: list[_Cluster] = []
    for run in runs:
        for f in sorted(run.findings, key=lambda x: (-_SEV_WEIGHT.get(x.sev, 1), x.ref)):
            best, best_score = None, threshold
            for c in clusters:
                if run.run_id in c.members:
                    continue
                score = max(_similar(f, g) for g in c.members.values())
                if score >= best_score:
                    best, best_score = c, score
            if best is None:
                best = _Cluster()
                clusters.append(best)
            best.members[run.run_id] = f
    return clusters


# ---------------------------------------------------------------------------
# The constrained fit
# ---------------------------------------------------------------------------


def isotonic_fit(
    values: Mapping[str, float],
    weights: Mapping[str, float],
    above: Iterable[tuple[str, str]],
    *,
    iterations: int = 2000,
    tol: float = 1e-9,
) -> dict[str, float]:
    """Weighted least squares subject to f[b] >= f[a] for each (a, b) in `above`.

    Minimises sum_w (f - values)^2 over the order constraints: weighted isotonic regression on
    a DAG. Dykstra's algorithm (alternating projections with corrections) converges to the
    exact projection; graphs here are small, so this is instant. Returns `values` unchanged
    when no constraint binds.
    """
    pairs = [(a, b) for a, b in above if a in values and b in values and a != b]
    f = dict(values)
    if not pairs:
        return f
    corrections: list[dict[str, float]] = [{} for _ in pairs]
    for _ in range(iterations):
        moved = 0.0
        for i, (a, b) in enumerate(pairs):
            # Dykstra: add back this constraint's last correction, project, store the new one.
            y = {k: f[k] + corrections[i].get(k, 0.0) for k in (a, b)}
            gap = y[a] - y[b]
            if gap > 0:
                ia, ib = 1.0 / weights.get(a, 1.0), 1.0 / weights.get(b, 1.0)
                share = gap / (ia + ib)
                proj = {a: y[a] - share * ia, b: y[b] + share * ib}
            else:
                proj = y
            corrections[i] = {k: y[k] - proj[k] for k in (a, b)}
            for k in (a, b):
                moved = max(moved, abs(proj[k] - f[k]))
                f[k] = proj[k]
        if moved < tol:
            break
    return f


def _mad_bounds(xs: Sequence[float], k: float) -> tuple[float, float]:
    m = median(xs)
    mad = median(abs(x - m) for x in xs)
    spread = max(mad * 1.4826, 0.1 * abs(m))  # MAD floor: 10% of the median
    return m - k * spread, m + k * spread


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------


class Issue(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str
    subject: str
    claim: str
    at: str | None
    sev: str
    raised_in: int
    stood_in: int
    runs: int
    stand_rate: float
    stability: Literal["stable", "unstable", "noise"]
    refs: dict[str, str]  # run id -> finding ref


class TrialRun(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: str
    subject: str
    config: str
    verdict: str
    rerun_of: str | None
    tokens: int
    verdict_residual: float
    missed: tuple[str, ...]  # stable issues this run did not have standing
    lone: tuple[str, ...]  # serious issues only this run raised
    token_bounds: tuple[float, float] | None
    out_of_bounds: tuple[str, ...]  # reasons; empty when in bounds


class Subject(BaseModel):
    model_config = ConfigDict(frozen=True)

    subject: str
    targets: tuple[str, ...]
    runs: int
    observed: float  # mean verdict rank, 0 pass .. 2 block
    fitted: float  # after the dependency constraints
    verdict: str  # consensus: from issues that stand in at least half the runs
    fitted_verdict: str
    depends_on: tuple[str, ...]
    unstable_issues: int
    rerun_priority: float


class TrialsReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    schema_version: Literal["1.0.0"] = TRIALS_VERSION
    root: str
    tolerance: float
    subjects: tuple[Subject, ...]
    runs: tuple[TrialRun, ...]
    issues: tuple[Issue, ...]
    violations: tuple[str, ...]  # consensus verdicts that break a dependency rule
    skipped_runs: int

    @property
    def out_of_bounds(self) -> tuple[TrialRun, ...]:
        return tuple(r for r in self.runs if r.out_of_bounds)

    @property
    def exit_code(self) -> int:
        """0 in bounds, 1 when any run is out of bounds or a dependency rule is broken."""
        return 1 if self.out_of_bounds or self.violations else 0


def _verdict_name(level: float) -> str:
    return _VERDICTS[min(2, max(0, round(level)))]


def analyse(
    runs: Sequence[Run],
    links: Sequence[Link] = (),
    *,
    protocol: Protocol | None = None,
    root: Path | str = "",
    tolerance: float = 0.75,
    stable_at: float = 0.67,
    noise_at: float = 0.34,
    token_k: float = 3.0,
    skipped: int = 0,
) -> TrialsReport:
    """Link runs, match issues, fit verdicts under the dependency rules, flag what's out of bounds."""
    protocol = protocol or load_protocol()
    by_subject: dict[str, list[Run]] = defaultdict(list)
    for r in runs:
        by_subject[r.subject].append(r)
    run_subject = {r.run_id: r.subject for r in runs}

    def subject_of(ref: str) -> str | None:
        return run_subject.get(ref) or (ref if ref in by_subject else None)

    depends: dict[str, set[str]] = defaultdict(set)  # subject -> subjects it depends on
    for link in links:
        a, b = subject_of(link.source), subject_of(link.target)
        if link.kind == "depends_on" and a and b and a != b:
            depends[a].add(b)

    # Reruns: same subject and config link to the first such run.
    first: dict[tuple[str, str], str] = {}
    rerun_of: dict[str, str | None] = {}
    for r in runs:
        key = (r.subject, r.config)
        rerun_of[r.run_id] = first.get(key)
        first.setdefault(key, r.run_id)

    # Issues per subject.
    issues: list[Issue] = []
    standing_by_run: dict[str, set[str]] = defaultdict(set)
    for subject, group in sorted(by_subject.items()):
        n = len(group)
        for i, c in enumerate(match_issues(group)):
            stood = [rid for rid, f in c.members.items() if f.status in _STANDING]
            rate = len(stood) / n
            stability = "stable" if rate >= stable_at else "noise" if rate <= noise_at else "unstable"
            sev = Counter(f.sev for f in c.members.values()).most_common(1)[0][0]
            lead = max(c.members.values(), key=lambda f: (f.status in _STANDING, len(f.claim)))
            key = f"{subject}/I{i + 1}"
            for rid in stood:
                standing_by_run[rid].add(key)
            issues.append(Issue(
                key=key, subject=subject, claim=lead.claim, at=lead.at, sev=sev,
                raised_in=len(c.members), stood_in=len(stood), runs=n,
                stand_rate=round(rate, 3), stability=stability,
                refs={rid: f.ref for rid, f in c.members.items()},
            ))
    issues_by_subject: dict[str, list[Issue]] = defaultdict(list)
    for issue in issues:
        issues_by_subject[issue.subject].append(issue)

    # Constrained fit of verdict levels: f[dependant] >= f[dependency].
    observed = {s: sum(_RANK[r.verdict] for r in g) / len(g) for s, g in by_subject.items()}
    weights = {s: float(len(g)) for s, g in by_subject.items()}
    above = [(dep, s) for s, deps in depends.items() for dep in deps]
    fitted = isotonic_fit(observed, weights, above)

    def consensus(subject: str) -> str:
        worst = "pass"
        for issue in issues_by_subject[subject]:
            if issue.stand_rate >= 0.5:
                v = protocol.verdict.get(issue.sev, "pass")  # type: ignore[call-overload]
                if _RANK[v] > _RANK[worst]:
                    worst = v
        return worst

    consensus_verdict = {s: consensus(s) for s in by_subject}
    violations = tuple(
        f"{s} is {consensus_verdict[s]} but depends on {dep}, which is {consensus_verdict[dep]}"
        for dep, s in above
        if _RANK[consensus_verdict[s]] < _RANK[consensus_verdict[dep]]
    )

    # Token bounds per config (needs at least three runs to mean anything).
    tokens_by_config: dict[str, list[float]] = defaultdict(list)
    for r in runs:
        if r.tokens:
            tokens_by_config[r.config].append(float(r.tokens))
    token_bounds = {
        c: _mad_bounds(xs, token_k) for c, xs in tokens_by_config.items() if len(xs) >= 3
    }

    trial_runs = []
    for r in runs:
        group = by_subject[r.subject]
        subject_issues = issues_by_subject[r.subject]
        residual = abs(_RANK[r.verdict] - fitted[r.subject])
        mine = standing_by_run[r.run_id]
        missed = tuple(i.key for i in subject_issues if i.stability == "stable" and i.key not in mine)
        lone = tuple(
            i.key for i in subject_issues
            if len(group) >= 3 and i.raised_in == 1 and r.run_id in i.refs
            and i.key in mine and i.sev in ("block", "major")
        )
        bounds = token_bounds.get(r.config)
        reasons = []
        if len(group) >= 2 and residual > tolerance:
            reasons.append(
                f"verdict {r.verdict} is {residual:.2f} from the fitted {fitted[r.subject]:.2f}"
            )
        stable_count = sum(1 for i in subject_issues if i.stability == "stable")
        if stable_count and len(missed) / stable_count > 0.5:
            reasons.append(f"missed {len(missed)} of {stable_count} stable issues")
        if lone:
            reasons.append(f"alone raised {len(lone)} serious issue(s)")
        if bounds and r.tokens and not bounds[0] <= r.tokens <= bounds[1]:
            reasons.append(f"tokens {r.tokens} outside {bounds[0]:.0f}..{bounds[1]:.0f}")
        trial_runs.append(TrialRun(
            run_id=r.run_id, subject=r.subject, config=r.config, verdict=r.verdict,
            rerun_of=rerun_of[r.run_id], tokens=r.tokens,
            verdict_residual=round(residual, 3), missed=missed, lone=lone,
            token_bounds=(round(bounds[0]), round(bounds[1])) if bounds else None,
            out_of_bounds=tuple(reasons),
        ))

    subjects = []
    for s, group in sorted(by_subject.items()):
        unstable = [i for i in issues_by_subject[s] if i.stability == "unstable"]
        # Uncertainty per issue p(1-p), weighted by severity; a rerun's value shrinks as 1/sqrt(n).
        spread = sum(_SEV_WEIGHT.get(i.sev, 1) * i.stand_rate * (1 - i.stand_rate)
                     for i in issues_by_subject[s])
        verdict_var = sum((_RANK[r.verdict] - observed[s]) ** 2 for r in group) / len(group)
        priority = (spread + verdict_var) / math.sqrt(len(group))
        names = sorted({n for r in group for n in r.target_names})
        subjects.append(Subject(
            subject=s, targets=tuple(names), runs=len(group),
            observed=round(observed[s], 3), fitted=round(fitted[s], 3),
            verdict=consensus_verdict[s], fitted_verdict=_verdict_name(fitted[s]),
            depends_on=tuple(sorted(depends.get(s, ()))),
            unstable_issues=len(unstable), rerun_priority=round(priority, 3),
        ))
    subjects.sort(key=lambda x: -x.rerun_priority)

    return TrialsReport(
        root=str(root), tolerance=tolerance, subjects=tuple(subjects), runs=tuple(trial_runs),
        issues=tuple(sorted(issues, key=lambda i: (i.subject, -i.stand_rate, i.key))),
        violations=violations, skipped_runs=skipped,
    )


# ---------------------------------------------------------------------------
# Graph and rendering
# ---------------------------------------------------------------------------


def trials_schema() -> Any:
    from lattice_graph.schema import EdgeType, GraphSchema, NodeType

    return GraphSchema(
        name="deliberator-trials",
        version=TRIALS_VERSION,
        nodes=(
            NodeType(name="Subject", description="What was reviewed, by content hash"),
            NodeType(name="Config", description="Reviewers, lenses, model and protocol"),
            NodeType(name="Trial", description="One review run"),
            NodeType(name="Issue", description="One finding, matched across runs"),
        ),
        edges=(
            EdgeType(name="REVIEWS", sources=("Trial",), targets=("Subject",)),
            EdgeType(name="RUN_WITH", sources=("Trial",), targets=("Config",)),
            EdgeType(name="RERUN_OF", sources=("Trial",), targets=("Trial",)),
            EdgeType(name="RAISES", sources=("Trial",), targets=("Issue",)),
            EdgeType(name="ABOUT", sources=("Issue",), targets=("Subject",)),
            EdgeType(name="DEPENDS_ON", sources=("Subject",), targets=("Subject",)),
        ),
    )


def trials_graph(report: TrialsReport) -> dict[str, Any]:
    from lattice_graph.build import node_link
    from lattice_graph.projection import Edge, Node, Projection, check

    nodes, edges = [], []
    for s in report.subjects:
        nodes.append(Node(label="Subject", key=f"subject:{s.subject}", props={
            "targets": list(s.targets), "runs": s.runs, "verdict": s.verdict,
            "fitted": s.fitted, "rerun_priority": s.rerun_priority}))
        edges += [Edge(type="DEPENDS_ON", source=f"subject:{s.subject}", target=f"subject:{d}")
                  for d in s.depends_on]
    for c in sorted({r.config for r in report.runs}):
        nodes.append(Node(label="Config", key=f"config:{c}"))
    for r in report.runs:
        key = f"trial:{r.run_id}"
        nodes.append(Node(label="Trial", key=key, props={
            "verdict": r.verdict, "tokens": r.tokens, "residual": r.verdict_residual,
            "out_of_bounds": list(r.out_of_bounds)}))
        edges += [Edge(type="REVIEWS", source=key, target=f"subject:{r.subject}"),
                  Edge(type="RUN_WITH", source=key, target=f"config:{r.config}")]
        if r.rerun_of:
            edges.append(Edge(type="RERUN_OF", source=key, target=f"trial:{r.rerun_of}"))
    for i in report.issues:
        nodes.append(Node(label="Issue", key=f"issue:{i.key}", props={
            "claim": i.claim, "at": i.at, "sev": i.sev, "stand_rate": i.stand_rate,
            "stability": i.stability}))
        edges.append(Edge(type="ABOUT", source=f"issue:{i.key}", target=f"subject:{i.subject}"))
        for rid, ref in i.refs.items():
            edges.append(Edge(type="RAISES", source=f"trial:{rid}", target=f"issue:{i.key}",
                              props={"ref": ref}))
    projection = Projection(nodes=tuple(nodes), edges=tuple(edges))
    schema = trials_schema()
    check(projection, schema)
    return node_link(projection, schema)


def render_markdown(report: TrialsReport) -> str:
    out = ["# Trials", ""]
    out.append(
        f"{len(report.runs)} runs over {len(report.subjects)} subject(s); "
        f"{len(report.out_of_bounds)} out of bounds (tolerance {report.tolerance})."
    )
    if report.skipped_runs:
        out.append(f"{report.skipped_runs} older run(s) without subject/config were skipped.")
    if report.violations:
        out += ["", "## Dependency rules broken", ""] + [f"- {v}" for v in report.violations]
    out += ["", "## Subjects (next rerun goes to the top one)", "",
            "| Subject | Targets | Runs | Verdict | Observed | Fitted | Unstable issues | Priority |",
            "|---|---|---|---|---|---|---|---|"]
    for s in report.subjects:
        out.append(f"| `{s.subject}` | {', '.join(s.targets)} | {s.runs} | {s.verdict} | "
                   f"{s.observed:.2f} | {s.fitted:.2f} | {s.unstable_issues} | "
                   f"{s.rerun_priority:.2f} |")
    out += ["", "## Runs", "", "| Run | Verdict | Residual | Tokens | Out of bounds |",
            "|---|---|---|---|---|"]
    for r in report.runs:
        out.append(f"| `{r.run_id}` | {r.verdict} | {r.verdict_residual:.2f} | {r.tokens:,} | "
                   f"{'; '.join(r.out_of_bounds) or '-'} |")
    out += ["", "## Issues", "", "| Issue | Sev | Stood in | Stability | Claim | At |",
            "|---|---|---|---|---|---|"]
    for i in report.issues:
        claim = i.claim.replace("|", "/")
        out.append(f"| `{i.key.split('/')[-1]}` | {i.sev} | {i.stood_in}/{i.runs} | "
                   f"{i.stability} | {claim} | {i.at or '-'} |")
    return "\n".join(out) + "\n"


def run_trials(root: Path, *, tolerance: float = 0.75, write: bool = True) -> TrialsReport:
    """Analyse every run under `root` and (by default) write trials.json/.md/.graph.json."""
    runs, skipped = load_runs(root)
    report = analyse(runs, load_links(root), root=root, tolerance=tolerance, skipped=skipped)
    if write:
        (root / "trials.json").write_text(report.model_dump_json(indent=1), encoding="utf-8")
        (root / "trials.md").write_text(render_markdown(report), encoding="utf-8")
        (root / "trials.graph.json").write_text(
            json.dumps(trials_graph(report), indent=1), encoding="utf-8")
    return report
