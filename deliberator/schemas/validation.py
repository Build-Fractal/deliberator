"""Solver validation flow — config generation and verdict models (spec 027, 037).

Generates a deliberator.yml configuration that launches a validation
deliberation against a solver's solution.  Agents are auto-generated
from the problem type and given solution-critique prompts (not generic
review prompts).

No solver or LLM imports — pure config generation and Pydantic models.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Sensitivity finding model (FR-005)
# ---------------------------------------------------------------------------

class SensitivityFinding(BaseModel):
    """A single sensitivity analysis finding (FR-004, FR-005).

    Structured record of what happens when a key parameter changes.
    """

    parameter: str = Field(description="Name of the parameter tested.")
    change: str = Field(
        description="Magnitude and direction of change, e.g. '+10%', '-10%'."
    )
    feasibility_impact: Literal["feasible", "marginal", "infeasible", "unknown"] = Field(
        description="Effect on solution feasibility."
    )
    objective_impact: str = Field(
        description="Effect on objective value, e.g. '+5.2%', '-12%', 'unchanged'."
    )


# ---------------------------------------------------------------------------
# Constraint addition model (spec 037, H-4)
# ---------------------------------------------------------------------------

class ConstraintAddition(BaseModel):
    """A typed constraint proposal from the validation deliberation (H-4).

    Replaces free-form strings with structured constraint metadata so
    downstream solvers can consume additions programmatically.
    """

    model_config = {"frozen": True}

    constraint_type: str  # e.g., "bound", "cardinality", "precedence"
    expression: str  # e.g., "x[1] + x[2] <= 100"
    parameters: dict[str, Any] = {}
    target_solver: str = "any"  # "ampl", "any", etc.
    rationale: str = ""  # why this constraint is needed


# ---------------------------------------------------------------------------
# Solver solution input schema (spec 037, D-1)
# ---------------------------------------------------------------------------

class SolverSolution(BaseModel):
    """Structured representation of a solver's output (D-1).

    Provides a typed schema for feeding solver results into the
    validation deliberation, replacing unstructured file references.
    """

    model_config = {"frozen": True}

    objective_value: float | None = None
    variable_assignments: dict[str, Any] = {}
    solver_status: str = "unknown"
    constraints_satisfied: list[str] = []
    solve_time_ms: float | None = None


# ---------------------------------------------------------------------------
# Validation verdict model (FR-008, FR-009)
# ---------------------------------------------------------------------------

class ValidationVerdict(BaseModel):
    """Structured validation verdict for a solver solution (FR-008).

    Captures the multi-agent consensus on whether a solution should be
    accepted, revised, or rejected, along with supporting evidence.
    """

    verdict: Literal["accept", "revise", "reject"]
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Confidence in the verdict, 0.0 to 1.0.",
    )
    sensitivity_findings: list[SensitivityFinding] = Field(
        default_factory=list,
        description="Structured sensitivity analysis results (FR-004).",
    )
    constraint_additions: list[ConstraintAddition] = Field(
        default_factory=list,
        description="Typed constraint proposals to improve the solution (FR-009, H-4).",
    )
    summary: str = Field(
        description="Plain-language summary of the validation outcome.",
    )


# ---------------------------------------------------------------------------
# Agent prompt templates (FR-002, FR-004)
# ---------------------------------------------------------------------------

_SENSITIVITY_INSTRUCTIONS = """\
Reason about what would happen if key parameters changed significantly.
Which parameters is the solution most sensitive to? Where are the tipping points?
For each critical parameter, assess whether feasibility or objective quality
degrades gracefully or collapses abruptly.
Structure findings as: parameter, change, feasibility_impact, objective_impact"""

# Problem-type to agent definitions mapping (FR-002).
# Each agent has a name and a base prompt.  The sensitivity-analyst
# always includes the sensitivity instructions.

_AGENT_TEMPLATES: dict[str, list[dict[str, str]]] = {
    "general": [
        {
            "name": "optimality-auditor",
            "prompt": (
                "You are the Optimality Auditor. Examine whether the solution "
                "achieves the best possible objective value given the constraints. "
                "Look for slack in constraints that suggests room for improvement. "
                "Identify any dominated alternatives the solver may have missed."
            ),
        },
        {
            "name": "sensitivity-analyst",
            "prompt": (
                "You are the Sensitivity Analyst. Your primary task is to assess "
                "how robust this solution is to changes in the input parameters.\n\n"
                + _SENSITIVITY_INSTRUCTIONS
            ),
        },
        {
            "name": "constraint-verifier",
            "prompt": (
                "You are the Constraint Verifier. Check that every constraint in "
                "the problem formulation is satisfied by the solution. Look for "
                "implicit constraints the formulation may have missed. Propose "
                "additional constraints if the solution exploits loopholes."
            ),
        },
    ],
    "assignment": [
        {
            "name": "efficiency-advocate",
            "prompt": (
                "You are the Efficiency Advocate. Evaluate whether the assignment "
                "maximizes total value or minimizes total cost. Look for swaps "
                "that would improve the objective without violating constraints."
            ),
        },
        {
            "name": "fairness-advocate",
            "prompt": (
                "You are the Fairness Advocate. Examine whether the assignment "
                "distributes resources equitably. Flag cases where the best "
                "resources are concentrated on low-priority tasks or where "
                "some stakeholders are systematically disadvantaged.\n\n"
                + _SENSITIVITY_INSTRUCTIONS
            ),
        },
        {
            "name": "constraint-auditor",
            "prompt": (
                "You are the Constraint Auditor. Verify that all assignment "
                "constraints (capacity, eligibility, exclusivity) are satisfied. "
                "Identify missing constraints that could lead to degenerate "
                "assignments. Propose constraint additions to prevent issues."
            ),
        },
    ],
    "portfolio": [
        {
            "name": "return-maximizer",
            "prompt": (
                "You are the Return Maximizer. Evaluate whether the portfolio "
                "allocation achieves the best risk-adjusted return. Identify "
                "underweighted high-return assets and overweighted low-return "
                "assets."
            ),
        },
        {
            "name": "risk-minimizer",
            "prompt": (
                "You are the Risk Minimizer. Assess the portfolio's exposure "
                "to downside risk, concentration risk, and tail events. Flag "
                "allocations that create excessive single-asset or sector "
                "exposure.\n\n"
                + _SENSITIVITY_INSTRUCTIONS
            ),
        },
        {
            "name": "diversification-advocate",
            "prompt": (
                "You are the Diversification Advocate. Check that the portfolio "
                "is adequately diversified across asset classes, sectors, and "
                "geographies. Propose rebalancing if correlation between "
                "holdings is too high."
            ),
        },
    ],
    "negotiation": [
        {
            "name": "party-a-advocate",
            "prompt": (
                "You are the Party A Advocate. Represent party A's interests "
                "and evaluate whether the proposed agreement adequately "
                "addresses their priorities, constraints, and reservation "
                "values. Flag concessions that fall below their BATNA."
            ),
        },
        {
            "name": "party-b-advocate",
            "prompt": (
                "You are the Party B Advocate. Represent party B's interests "
                "and evaluate whether the proposed agreement adequately "
                "addresses their priorities, constraints, and reservation "
                "values. Flag concessions that fall below their BATNA.\n\n"
                + _SENSITIVITY_INSTRUCTIONS
            ),
        },
        {
            "name": "mediator",
            "prompt": (
                "You are the Mediator. Assess whether the proposed agreement "
                "represents a balanced outcome that both parties can accept. "
                "Identify Pareto improvements — changes that benefit one party "
                "without harming the other. Flag zero-sum traps."
            ),
        },
    ],
    "resource_allocation": [
        {
            "name": "efficiency-advocate",
            "prompt": (
                "You are the Efficiency Advocate. Evaluate whether the "
                "allocation maximizes total output or value per unit of "
                "resource consumed. Identify idle or underutilized resources "
                "and propose reallocation to higher-value uses."
            ),
        },
        {
            "name": "fairness-advocate",
            "prompt": (
                "You are the Fairness Advocate. Examine whether resources are "
                "distributed equitably across stakeholders. Flag allocations "
                "where some parties receive disproportionately little relative "
                "to their needs or contributions.\n\n"
                + _SENSITIVITY_INSTRUCTIONS
            ),
        },
        {
            "name": "utilization-auditor",
            "prompt": (
                "You are the Utilization Auditor. Verify that capacity "
                "constraints are respected and that utilization rates are "
                "reasonable. Flag over-allocated resources at risk of "
                "bottleneck and under-allocated resources being wasted."
            ),
        },
    ],
    "fair_division": [
        {
            "name": "envy-checker",
            "prompt": (
                "You are the Envy Checker. Determine whether the division is "
                "envy-free — does any party prefer another party's allocation "
                "to their own? Identify the most envious party and quantify "
                "the degree of envy."
            ),
        },
        {
            "name": "proportionality-advocate",
            "prompt": (
                "You are the Proportionality Advocate. Verify that each party "
                "receives at least their proportional share (1/n of total "
                "value by their own valuation). Flag violations and propose "
                "transfers to restore proportionality.\n\n"
                + _SENSITIVITY_INSTRUCTIONS
            ),
        },
        {
            "name": "valuation-auditor",
            "prompt": (
                "You are the Valuation Auditor. Scrutinize the reported "
                "valuations for consistency and strategic misrepresentation. "
                "Flag suspiciously low or high valuations that could "
                "manipulate the division outcome."
            ),
        },
    ],
    "mechanism_design": [
        {
            "name": "incentive-analyst",
            "prompt": (
                "You are the Incentive Analyst. Evaluate whether the mechanism "
                "is incentive-compatible — do participants maximize their "
                "utility by reporting truthfully? Identify opportunities for "
                "strategic manipulation or collusion."
            ),
        },
        {
            "name": "efficiency-advocate",
            "prompt": (
                "You are the Efficiency Advocate. Assess whether the mechanism "
                "achieves allocative efficiency — does it maximize total "
                "welfare? Identify deadweight loss and propose mechanism "
                "modifications to reduce it.\n\n"
                + _SENSITIVITY_INSTRUCTIONS
            ),
        },
        {
            "name": "gaming-adversary",
            "prompt": (
                "You are the Gaming Adversary. Actively try to find strategies "
                "that exploit the mechanism. Attempt to game the rules, "
                "collude with other participants, or misreport preferences "
                "to achieve an unfair advantage. Report all vulnerabilities."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# Config generation (FR-001, FR-002, FR-003)
# ---------------------------------------------------------------------------

def generate_validation_config(
    solution_path: Path,
    problem_path: Path | None = None,
    objective_path: Path | None = None,
    problem_type: str = "general",
    output_dir: Path = Path("validation-output"),
    solution: SolverSolution | None = None,
) -> dict[str, Any]:
    """Generate a deliberator config dict for validating a solver solution.

    The returned dict can be written as YAML to produce a ``deliberator.yml``
    that runs a validation deliberation.

    Args:
        solution_path: Path to the solver's solution file (e.g. solution.yml).
        problem_path: Path to the original problem.md.  Optional.
        objective_path: Path to the objective.yml.  Optional.
        problem_type: One of the keys in ``_AGENT_TEMPLATES`` (e.g.
            ``"general"``, ``"assignment"``, ``"portfolio"``, ``"negotiation"``,
            ``"resource_allocation"``, ``"fair_division"``,
            ``"mechanism_design"``).
            Determines which agent perspectives are generated (FR-002).
        output_dir: Where validation output is written.
        solution: Optional structured solver output.  When provided, the
            solver status, objective value, and variable assignments are
            embedded in the config so agents can reference concrete numbers
            instead of parsing files.

    Returns:
        Dict suitable for ``yaml.dump()`` to produce a valid ``deliberator.yml``.

    Raises:
        ValueError: If *problem_type* is not recognized.

    .. rubric:: Phase 2 — CLI integration (tracked, not yet implemented)

    A ``deliberator validate`` CLI command will wrap this function, accepting
    file paths and ``--problem-type`` as arguments, writing the generated
    config to disk, and optionally launching the deliberation in one step.

    .. rubric:: Phase 3 — solver integrations (tracked, not yet implemented)

    Direct integrations with AMPL, HiGHS, and other solvers will
    auto-populate the ``SolverSolution`` parameter from solver output
    files, removing the need for manual construction.
    """
    if problem_type not in _AGENT_TEMPLATES:
        raise ValueError(
            f"Unknown problem_type '{problem_type}'. "
            f"Valid types: {sorted(_AGENT_TEMPLATES.keys())}."
        )

    # Build target list (FR-003): solution + problem + objective
    targets: list[str] = [str(solution_path)]
    if problem_path is not None:
        targets.append(str(problem_path))
    if objective_path is not None:
        targets.append(str(objective_path))

    # Build agent entries (FR-002)
    agents: list[dict[str, str]] = []
    for template in _AGENT_TEMPLATES[problem_type]:
        agents.append({
            "name": template["name"],
            "prompt": template["prompt"],
        })

    config: dict[str, Any] = {
        "mode": "cooperative",
        "target": targets if len(targets) > 1 else targets[0],
        "output": str(output_dir),
        "iterations": 1,
        "rounds": 1,
        "agents": agents,
    }

    # Embed structured solver output when provided (D-1)
    if solution is not None:
        config["solution"] = solution.model_dump()

    return config


# ---------------------------------------------------------------------------
# Utility: check whether an agent prompt contains sensitivity instructions
# ---------------------------------------------------------------------------

def has_sensitivity_instructions(prompt: str) -> bool:
    """Return True if *prompt* contains the structured sensitivity analysis block."""
    return "feasibility_impact, objective_impact" in prompt
