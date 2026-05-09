"""Tests for the XII dead-infrastructure linter.

The linter must:
1. Pass against the live schema + templates (regression guard).
2. Detect a synthetic dead variable (mutation sanity).
3. Accept a `consumer:` annotation as proof of orchestrator-only consumption.
4. Reject a stale `consumer:` annotation when no template references the var (out of scope for v1; see comment).
"""

from __future__ import annotations

from pathlib import Path

import pytest

try:
    from .dead_infra import (
        ALL_MODES,
        find_dead_variables,
        load_schema,
        collect_template_variables,
    )
except ImportError:
    from dead_infra import (
        ALL_MODES,
        find_dead_variables,
        load_schema,
        collect_template_variables,
    )


def test_live_schema_has_no_dead_variables() -> None:
    """The shipped schema + templates must pass — regression guard."""
    schema = load_schema()
    template_vars = collect_template_variables(ALL_MODES)
    dead = find_dead_variables(schema, template_vars, verbose=False)
    assert dead == [], (
        "Dead variables detected:\n  "
        + "\n  ".join(f"{d.name}: {d.reason()}" for d in dead)
    )


def test_synthetic_dead_variable_is_flagged() -> None:
    """Inject a variable that no template references — linter must catch it."""
    schema = load_schema()
    schema["variables"]["FAKE_DEAD_VAR_FOR_TEST"] = {
        "type": "string",
        "description": "synthetic — should be flagged",
        "phases": ["review", "synthesis"],
        "required": False,
    }
    template_vars = collect_template_variables(ALL_MODES)
    dead = find_dead_variables(schema, template_vars, verbose=False)
    names = {d.name for d in dead}
    assert "FAKE_DEAD_VAR_FOR_TEST" in names


def test_consumer_annotation_exempts_orchestrator_only_variable() -> None:
    """A variable with `consumer:` set is not flagged even with zero template hits."""
    schema = load_schema()
    schema["variables"]["FAKE_ORCHESTRATOR_VAR"] = {
        "type": "string",
        "description": "synthetic — orchestrator-consumed",
        "phases": ["review"],
        "required": False,
        "consumer": "engine.test_consumer — explicit attribution",
    }
    template_vars = collect_template_variables(ALL_MODES)
    dead = find_dead_variables(schema, template_vars, verbose=False)
    names = {d.name for d in dead}
    assert "FAKE_ORCHESTRATOR_VAR" not in names


def test_variable_with_no_phases_is_skipped() -> None:
    """Variables without `phases:` are not dead infra — they're plugin-namespaced or orchestrator-side."""
    schema = load_schema()
    schema["variables"]["FAKE_NO_PHASES"] = {
        "type": "string",
        "description": "synthetic — no phases declared",
        "required": False,
    }
    template_vars = collect_template_variables(ALL_MODES)
    dead = find_dead_variables(schema, template_vars, verbose=False)
    names = {d.name for d in dead}
    assert "FAKE_NO_PHASES" not in names
