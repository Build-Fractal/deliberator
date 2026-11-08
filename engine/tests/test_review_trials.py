"""Trials: runs linked into a graph, issues matched across runs, a constrained fit, bounds."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("lattice_graph")

from engine.review.trials import (
    Link,
    Run,
    RunFinding,
    add_link,
    analyse,
    isotonic_fit,
    match_issues,
    run_trials,
)


def _f(ref: str, claim: str, at: str | None = None, sev: str = "major",
       status: str = "stands") -> RunFinding:
    return RunFinding(ref=ref, sev=sev, claim=claim, at=at, status=status)


def _run(run_id: str, verdict: str, findings: list[RunFinding], *, subject: str = "s1",
         config: str = "c1", tokens: int = 60_000) -> Run:
    return Run(run_id=run_id, subject=subject, config=config, verdict=verdict,
               started=run_id, findings=tuple(findings), tokens=tokens, cost_usd=None,
               target_names=("install.sh",))


SSH = "SSH choice computed but never used for clone"
EXTRAS = "--extras flag silently dropped for local installs"


def test_isotonic_fit_without_binding_constraints_is_identity() -> None:
    assert isotonic_fit({"a": 0.0, "b": 2.0}, {"a": 1, "b": 1}, [("a", "b")]) == {"a": 0.0, "b": 2.0}


def test_isotonic_fit_pools_violators_by_weight() -> None:
    # b must be >= a, but observed a=2 (3 runs), b=0 (1 run): pooled at the weighted mean 1.5.
    fit = isotonic_fit({"a": 2.0, "b": 0.0}, {"a": 3, "b": 1}, [("a", "b")])
    assert fit["a"] == pytest.approx(1.5, abs=1e-6)
    assert fit["b"] == pytest.approx(1.5, abs=1e-6)


def test_isotonic_fit_chain() -> None:
    # a <= b <= c with observed 2, 1, 0 (equal weights): everything pools to 1.
    fit = isotonic_fit({"a": 2.0, "b": 1.0, "c": 0.0}, {}, [("a", "b"), ("b", "c")])
    for k in "abc":
        assert fit[k] == pytest.approx(1.0, abs=1e-6)


def test_matching_uses_location_and_wording() -> None:
    runs = [
        _run("r1", "changes", [_f("ann/F1", SSH, "install.sh:42"), _f("bob/F1", EXTRAS)]),
        _run("r2", "changes", [_f("ann/F2", "Computed SSH clone choice is ignored",
                                  "install.sh:43"),
                               _f("cat/F1", "Unrelated wording entirely about logging")]),
    ]
    clusters = match_issues(runs)
    sizes = sorted(len(c.members) for c in clusters)
    assert sizes == [1, 1, 2]


def test_stable_issue_missed_and_verdict_outlier_are_out_of_bounds() -> None:
    runs = [_run(f"r{i}", "changes", [_f(f"ann/F{i}", SSH, "install.sh:42")]) for i in range(4)]
    runs.append(_run("r9", "pass", []))
    report = analyse(runs)
    [subject] = report.subjects
    assert subject.verdict == "changes"
    [issue] = report.issues
    assert issue.stood_in == 4 and issue.stability == "stable"
    flagged = {r.run_id: r.out_of_bounds for r in report.runs if r.out_of_bounds}
    assert list(flagged) == ["r9"]
    assert any("missed 1 of 1" in reason for reason in flagged["r9"])
    assert report.exit_code == 1


def test_lone_serious_issue_and_token_outlier() -> None:
    runs = [_run(f"r{i}", "changes", [_f("ann/F1", SSH, "install.sh:42")]) for i in range(4)]
    runs.append(_run("r5", "block", [_f("ann/F1", SSH, "install.sh:42"),
                                     _f("bob/F1", "Deletes home directory", sev="block")],
                     tokens=400_000))
    report = analyse(runs)
    r5 = next(r for r in report.runs if r.run_id == "r5")
    assert r5.lone and any("alone raised" in x for x in r5.out_of_bounds)
    assert any("tokens" in x for x in r5.out_of_bounds)
    assert all(not r.out_of_bounds for r in report.runs if r.run_id != "r5")


def test_reruns_link_to_the_first_run_of_the_same_setup() -> None:
    runs = [_run("r1", "pass", []), _run("r2", "pass", []), _run("r3", "pass", [], config="c2")]
    by_id = {r.run_id: r for r in analyse(runs).runs}
    assert by_id["r1"].rerun_of is None
    assert by_id["r2"].rerun_of == "r1"
    assert by_id["r3"].rerun_of is None


def test_dependency_rule_pulls_fit_and_reports_violation() -> None:
    # B was built from A. A blocks in every run; B passes: B can't be better than A.
    a = [_run(f"a{i}", "block", [_f("ann/F1", "Drops users table", sev="block")], subject="A")
         for i in range(2)]
    b = [_run(f"b{i}", "pass", [], subject="B") for i in range(2)]
    report = analyse(a + b, [Link(kind="depends_on", source="b0", target="A")])
    subjects = {s.subject: s for s in report.subjects}
    assert subjects["B"].depends_on == ("A",)
    assert subjects["A"].fitted == pytest.approx(1.0, abs=1e-3)
    assert subjects["B"].fitted == pytest.approx(1.0, abs=1e-3)
    assert report.violations == ("B is pass but depends on A, which is block",)
    assert report.exit_code == 1


def test_rerun_priority_prefers_unstable_subjects() -> None:
    steady = [_run(f"s{i}", "changes", [_f("ann/F1", SSH, "x:1")], subject="steady")
              for i in range(4)]
    shaky = [_run(f"k{i}", "changes" if i % 2 else "pass",
                  [_f("ann/F1", EXTRAS, "y:1")] if i % 2 else [], subject="shaky")
             for i in range(4)]
    report = analyse(steady + shaky)
    assert report.subjects[0].subject == "shaky"
    assert report.subjects[0].unstable_issues == 1


def test_run_trials_reads_review_json_and_writes_outputs(tmp_path: Path) -> None:
    for i, verdict in enumerate(["changes", "changes", "pass"]):
        d = tmp_path / f"run{i}"
        d.mkdir()
        findings = [] if verdict == "pass" else [
            {"ref": "ann/F1", "sev": "major", "claim": SSH, "at": "install.sh:42",
             "status": "stands"}]
        (d / "review.json").write_text(json.dumps({
            "schema_version": "1.1.0", "run_id": f"run{i}", "subject": "s", "config": "c",
            "verdict": verdict, "started": f"2026-11-08T00:00:0{i}", "findings": findings,
            "targets": [{"name": "install.sh", "sha256": "x", "lines": 1}],
            "usage": {"input_tokens": 1000, "output_tokens": 100},
        }))
    old = tmp_path / "old"
    old.mkdir()
    (old / "review.json").write_text(json.dumps({"schema_version": "1.0.0", "run_id": "old",
                                                 "verdict": "pass", "findings": []}))
    add_link(tmp_path, "depends_on", "run0", "s")  # self-link: ignored
    report = run_trials(tmp_path)
    assert report.skipped_runs == 1
    assert len(report.runs) == 3
    graph = json.loads((tmp_path / "trials.graph.json").read_text())
    labels = {n["label"] for n in graph["nodes"]}
    assert labels == {"Subject", "Config", "Trial", "Issue"}
    assert "# Trials" in (tmp_path / "trials.md").read_text()
