"""Core domain plugin infrastructure: models, ABC, scoring, scaffolds.

Implements the base layer for domain-specific review plugins (spec 030).

Design rules:
  - All state models are frozen Pydantic (immutable).
  - Scoring logic is generic — works for any domain given variables + scaffold.
  - Domains only provide extractors and scaffolds.
  - This module imports nothing from ``engine/``, ``linter/``, ``web/``,
    or ``mcp_server``.
  - Dependencies limited to pydantic + stdlib.
"""

from __future__ import annotations

import json
import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, Field

logger = logging.getLogger("deliberator.domains")


# ---------------------------------------------------------------------------
# DomainContext — frozen input context for extraction
# ---------------------------------------------------------------------------


class DomainContext(BaseModel):
    """Input context passed to domain extractors.

    Captures the workspace, changed files, and any domain-specific metadata
    needed for variable extraction.  Frozen — extractors cannot mutate this.
    """

    model_config = {"frozen": True}

    workspace: Path
    changed_files: list[Path] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# DomainScore — frozen scoring result
# ---------------------------------------------------------------------------


class DomainScore(BaseModel):
    """Result of scoring extracted variables against a scaffold.

    ``overall`` is the weighted composite in [0, 1].
    ``hard_blocks`` lists triggered blocking conditions (if any, verdict is "block").
    ``verdict`` is one of "pass", "block", or "revise".
    ``recommendations`` are ordered by descending impact.
    ``variables`` contains the raw extracted values used for scoring.
    """

    model_config = {"frozen": True}

    overall: float = Field(ge=0.0, le=1.0)
    dimensions: dict[str, float] = Field(default_factory=dict)
    hard_blocks: list[str] = Field(default_factory=list)
    verdict: Literal["pass", "block", "revise"]
    recommendations: list[str] = Field(default_factory=list)
    variables: dict[str, Any] = Field(default_factory=dict)
    scaffold_name: str = ""


# ---------------------------------------------------------------------------
# DomainRecord — frozen persistence record
# ---------------------------------------------------------------------------


class DomainRecord(BaseModel):
    """A persisted review record linking score, context, and timestamps.

    Each record has a UUID, the domain name, the score, a serializable
    summary of the context, and optional equilibrium/convergence metadata.
    """

    model_config = {"frozen": True}

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    domain: str
    score: DomainScore
    context_summary: dict[str, Any] = Field(default_factory=dict)
    equilibrium_score: float | None = None
    convergence: str | None = None


# ---------------------------------------------------------------------------
# TrendResult — frozen trend analysis result
# ---------------------------------------------------------------------------


class TrendResult(BaseModel):
    """Result of a trend analysis over a series of domain records.

    ``slope`` is the OLS linear regression slope over ``values``.
    ``direction`` classifies the trend.
    ``alert`` is True if a threshold was crossed.
    """

    model_config = {"frozen": True}

    field: str
    values: list[float] = Field(default_factory=list)
    slope: float = 0.0
    direction: Literal["improving", "declining", "stable"] = "stable"
    alert: bool = False


# ---------------------------------------------------------------------------
# Scaffold — frozen scoring scaffold loaded from YAML/JSON
# ---------------------------------------------------------------------------


class Scaffold(BaseModel):
    """A scoring scaffold defining weights, thresholds, and hard blocks.

    Loaded from a JSON or YAML file in the domain's scaffold directory.
    Weights map dimension names to their relative importance.
    Thresholds map dimension names to minimum acceptable scores.
    Hard blocks list conditions that force a "block" verdict.
    """

    model_config = {"frozen": True}

    name: str
    description: str = ""
    weights: dict[str, float] = Field(default_factory=dict)
    thresholds: dict[str, float] = Field(default_factory=dict)
    hard_blocks: list[str] = Field(default_factory=list)


def load_scaffold(path: Path) -> Scaffold:
    """Load a scaffold from a YAML or JSON file.

    Args:
        path: Path to the scaffold file (.yml, .yaml, or .json).

    Returns:
        A validated Scaffold instance.

    Raises:
        FileNotFoundError: If the path does not exist.
        ValueError: If the file cannot be parsed.
    """
    if not path.exists():
        raise FileNotFoundError(f"Scaffold file not found: {path}")

    text = path.read_text(encoding="utf-8")

    try:
        if path.suffix in (".yml", ".yaml"):
            import yaml
            data = yaml.safe_load(text)
        else:
            data = json.loads(text)
    except Exception as exc:
        raise ValueError(f"Failed to parse scaffold file {path}: {exc}") from exc

    return Scaffold(**data)


#: Extensions tried when resolving a scaffold by name, in priority order.
_SCAFFOLD_EXTENSIONS: tuple[str, ...] = (".yml", ".yaml", ".json")


def _resolve_scaffold_path(scaffold_dir: Path, name: str) -> Path:
    """Resolve a scaffold name to an actual file path.

    Tries extensions in :data:`_SCAFFOLD_EXTENSIONS` order and returns the
    first match that exists on disk.

    Args:
        scaffold_dir: Directory containing scaffold files.
        name: Scaffold name (without extension).

    Returns:
        Path to the first matching scaffold file.

    Raises:
        FileNotFoundError: If no file matches any candidate extension.
    """
    for ext in _SCAFFOLD_EXTENSIONS:
        candidate = scaffold_dir / f"{name}{ext}"
        if candidate.exists():
            return candidate

    tried = ", ".join(
        f"{name}{ext}" for ext in _SCAFFOLD_EXTENSIONS
    )
    raise FileNotFoundError(
        f"Scaffold '{name}' not found in {scaffold_dir} "
        f"(tried: {tried})"
    )


# ---------------------------------------------------------------------------
# VariableExtractor — protocol for domain-specific extraction
# ---------------------------------------------------------------------------


@runtime_checkable
class VariableExtractor(Protocol):
    """Protocol for domain-specific variable extractors.

    Each extractor declares its ``name`` and the ``variables`` it produces,
    then implements ``extract()`` to compute them from a DomainContext.
    """

    name: str
    variables: list[str]

    def extract(self, context: DomainContext) -> dict[str, Any]:
        """Extract variables from the domain context.

        Args:
            context: The frozen domain context.

        Returns:
            Dict mapping variable names to extracted values.
        """
        ...


# ---------------------------------------------------------------------------
# Scoring pure functions
# ---------------------------------------------------------------------------


def _linear_slope(values: list[float]) -> float:
    """Compute the slope of a simple linear regression over values.

    Uses OLS: slope = sum((x_i - x_mean)(y_i - y_mean)) / sum((x_i - x_mean)^2)
    where x_i = 0, 1, 2, ... and y_i = values[i].

    Returns 0.0 if fewer than 2 data points.
    """
    n = len(values)
    if n < 2:
        return 0.0

    x_mean = (n - 1) / 2.0
    y_mean = sum(values) / n

    numerator = 0.0
    denominator = 0.0
    for i, y in enumerate(values):
        dx = i - x_mean
        numerator += dx * (y - y_mean)
        denominator += dx * dx

    if denominator == 0.0:
        return 0.0

    return numerator / denominator


def _compute_weighted_score(
    variables: dict[str, Any],
    weights: dict[str, float],
) -> tuple[float, dict[str, float]]:
    """Compute a weighted composite score from variables and weights.

    Each dimension score is the variable value (clamped to [0, 1]).
    The composite is the weighted average of dimension scores.

    Returns:
        Tuple of (overall_score, dimension_scores).
    """
    dimensions: dict[str, float] = {}
    total_weight = 0.0
    weighted_sum = 0.0

    for dim, weight in weights.items():
        raw = variables.get(dim)
        if raw is None:
            continue
        # Clamp to [0, 1]
        val = max(0.0, min(1.0, float(raw)))
        dimensions[dim] = val
        weighted_sum += val * weight
        total_weight += weight

    if total_weight == 0.0:
        return 0.0, dimensions

    overall = weighted_sum / total_weight
    return max(0.0, min(1.0, overall)), dimensions


def _check_hard_blocks(
    variables: dict[str, Any],
    hard_block_conditions: list[str],
) -> list[str]:
    """Evaluate hard block conditions against extracted variables.

    Each condition is a string of the form ``"variable_name < threshold"``
    or ``"variable_name > threshold"``.  If the condition is met, the
    variable name is added to the triggered list.

    Supported operators: ``<``, ``>``, ``<=``, ``>=``, ``==``.

    Returns:
        List of triggered hard block condition strings.
    """
    triggered: list[str] = []

    ops = {
        "<": lambda a, b: a < b,
        ">": lambda a, b: a > b,
        "<=": lambda a, b: a <= b,
        ">=": lambda a, b: a >= b,
        "==": lambda a, b: a == b,
    }

    for condition in hard_block_conditions:
        parts = condition.split()
        if len(parts) != 3:
            logger.warning("Invalid hard block condition: %s", condition)
            continue

        var_name, op, threshold_str = parts

        if op not in ops:
            logger.warning("Unknown operator in hard block: %s", condition)
            continue

        raw = variables.get(var_name)
        if raw is None:
            continue

        try:
            threshold = float(threshold_str)
            value = float(raw)
        except (ValueError, TypeError):
            continue

        if ops[op](value, threshold):
            triggered.append(condition)

    return triggered


def _determine_verdict(
    overall: float,
    hard_blocks: list[str],
    thresholds: dict[str, float],
    dimensions: dict[str, float],
) -> Literal["pass", "block", "revise"]:
    """Determine the verdict based on score, hard blocks, and thresholds.

    - If any hard block is triggered: "block".
    - If any dimension is below its threshold: "revise".
    - Otherwise: "pass".
    """
    if hard_blocks:
        return "block"

    for dim, threshold in thresholds.items():
        dim_score = dimensions.get(dim, 0.0)
        if dim_score < threshold:
            return "revise"

    return "pass"


def _evaluate_single_hard_block(rule: str, variables: dict[str, Any]) -> bool:
    """Evaluate a single hard block rule against extracted variables.

    Supported rule forms:
      - ``"secrets_exposed"``           — truthy check (bare variable name)
      - ``"critical_vulns > 0"``        — numeric comparison
      - ``"has_spec == false"``         — boolean equality check

    Supported operators: ``==``, ``!=``, ``>=``, ``<=``, ``>``, ``<``.

    Args:
        rule: The hard block rule string.
        variables: The extracted variable dict.

    Returns:
        True if the rule is triggered (i.e. the block condition is met).
    """
    rule = rule.strip()

    # Comparison operators — check longest operators first to avoid
    # matching ``>=`` as ``>`` + ``=``.
    for op_str, op_fn in [
        ("==", lambda a, b: a == b),
        ("!=", lambda a, b: a != b),
        (">=", lambda a, b: a >= b),
        ("<=", lambda a, b: a <= b),
        (">", lambda a, b: a > b),
        ("<", lambda a, b: a < b),
    ]:
        if op_str in rule:
            parts = rule.split(op_str, 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                rhs_str = parts[1].strip().lower()
                value = variables.get(var_name)
                if value is None:
                    continue

                # Parse RHS
                if rhs_str in ("true", "false"):
                    rhs: Any = rhs_str == "true"
                    lhs = bool(value)
                else:
                    try:
                        rhs = float(rhs_str)
                        lhs = (
                            float(value)
                            if not isinstance(value, bool)
                            else (1.0 if value else 0.0)
                        )
                    except (ValueError, TypeError):
                        continue

                return op_fn(lhs, rhs)

    # Simple truthy check — rule is a bare variable name
    value = variables.get(rule)
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value > 0
    return bool(value)


def _evaluate_hard_block_rules(
    rules: list[str],
    variables: dict[str, Any],
) -> list[str]:
    """Evaluate a list of hard block rules, returning triggered ones.

    Args:
        rules: List of hard block rule strings.
        variables: The extracted variable dict.

    Returns:
        List of triggered rule strings.
    """
    triggered: list[str] = []
    for rule in rules:
        if _evaluate_single_hard_block(rule, variables):
            triggered.append(rule)
    return triggered


def _build_recommendations(
    dimensions: dict[str, float],
    thresholds: dict[str, float],
    weights: dict[str, float],
) -> list[str]:
    """Build recommendations ordered by impact (weight * gap).

    Dimensions below their threshold generate recommendations.
    Sorted by descending impact = weight * (threshold - score).
    """
    recs: list[tuple[float, str]] = []

    for dim, threshold in thresholds.items():
        score = dimensions.get(dim, 0.0)
        if score < threshold:
            weight = weights.get(dim, 1.0)
            gap = threshold - score
            impact = weight * gap
            recs.append((
                impact,
                f"Improve '{dim}': score {score:.2f} is below "
                f"threshold {threshold:.2f} (impact weight: {weight:.1f})",
            ))

    recs.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in recs]


# ---------------------------------------------------------------------------
# DomainPlugin — abstract base class
# ---------------------------------------------------------------------------


class DomainPlugin(ABC):
    """Abstract base class for domain-specific review plugins.

    Subclasses provide extractors and scaffold directories.  The scoring,
    record creation, and persistence logic is generic and inherited.

    The ``score()`` method works for any domain: it takes variables and a
    scaffold, computes weighted composite scores, evaluates hard blocks,
    and determines a verdict.  Domains only need to supply extractors
    (via ``get_extractors()``) and scaffold files.

    Subclasses may override the scoring hooks to customise behaviour:

    - ``get_dimension_variables()`` — map dimension names to variable lists.
    - ``normalize_variable()`` — domain-specific value normalisation.
    - ``score_dimension()`` — score a single dimension from variables.
    - ``evaluate_hard_blocks()`` — evaluate hard block rules.
    - ``determine_verdict()`` — map scores to pass/block/revise.
    - ``build_recommendations()`` — produce ordered improvement advice.
    """

    name: str
    version: str
    scaffold_dir: Path

    @abstractmethod
    def get_extractors(self) -> list[VariableExtractor]:
        """Return the list of variable extractors for this domain.

        Each extractor produces a subset of the variables needed for scoring.
        Results from all extractors are merged (later extractors can override
        earlier ones if they share variable names).

        Returns:
            List of VariableExtractor instances.
        """
        ...

    # ------------------------------------------------------------------
    # Scoring hooks — override in subclasses to customise scoring
    # ------------------------------------------------------------------

    def get_dimension_variables(self) -> dict[str, list[str]]:
        """Return a mapping from dimension names to their constituent variables.

        When this returns a non-empty dict, ``score()`` computes per-dimension
        scores via ``score_dimension()`` and then weights them.

        When empty (default), ``score()`` maps scaffold weight keys directly
        to variable values (simple 1:1 scoring).

        Returns:
            Dict mapping dimension name to list of variable names.
        """
        return {}

    def normalize_variable(self, name: str, value: Any) -> float | None:
        """Normalize a raw variable value to [0, 1] for scoring.

        Default implementation converts to float and clamps to [0, 1].
        Returns None if the value cannot be converted.

        Args:
            name: The variable name.
            value: The raw extracted value.

        Returns:
            Normalized float in [0, 1], or None if not normalizable.
        """
        if value is None:
            return None
        try:
            fval = float(value)
            return max(0.0, min(1.0, fval))
        except (ValueError, TypeError):
            return None

    def score_dimension(
        self, dimension: str, variables: dict[str, Any],
    ) -> float | None:
        """Score a single dimension as the average of its normalized variables.

        Override to provide dimension-specific scoring logic.

        Args:
            dimension: The dimension name.
            variables: The full extracted variable dict.

        Returns:
            Float score in [0, 1], or None if no variables have values.
        """
        dim_vars = self.get_dimension_variables()
        var_names = dim_vars.get(dimension, [])
        if not var_names:
            return None

        scores: list[float] = []
        for name in var_names:
            raw = variables.get(name)
            normalized = self.normalize_variable(name, raw)
            if normalized is not None:
                scores.append(normalized)

        if not scores:
            return None

        return sum(scores) / len(scores)

    def evaluate_hard_blocks(
        self,
        rules: list[str],
        variables: dict[str, Any],
    ) -> list[str]:
        """Evaluate hard block rules against extracted variables.

        Each rule is one of:
          - A bare variable name (truthy check): ``"secrets_exposed"``
          - A comparison: ``"critical_vulns > 0"``
          - A boolean equality: ``"has_spec == false"``

        Supported operators: ``<``, ``>``, ``<=``, ``>=``, ``==``, ``!=``.

        Args:
            rules: List of hard block rule strings.
            variables: The extracted variable dict.

        Returns:
            List of triggered rule strings.
        """
        return _evaluate_hard_block_rules(rules, variables)

    def determine_verdict(
        self,
        overall: float,
        hard_blocks: list[str],
        thresholds: dict[str, float],
        dimensions: dict[str, float],
        variables: dict[str, Any],
    ) -> Literal["pass", "block", "revise"]:
        """Determine the verdict from scores, blocks, and thresholds.

        Default logic:
          - Any hard block triggered -> ``"block"``.
          - Any dimension below its threshold -> ``"revise"``.
          - Otherwise -> ``"pass"``.

        Override to implement domain-specific verdict rules (e.g. checking
        ``minimum_overall`` or ``minimum_*`` threshold conventions).

        Args:
            overall: Weighted composite score.
            hard_blocks: List of triggered hard block rules.
            thresholds: Scaffold threshold dict.
            dimensions: Dict of dimension scores.
            variables: The raw extracted variables.

        Returns:
            One of ``"pass"``, ``"block"``, or ``"revise"``.
        """
        return _determine_verdict(overall, hard_blocks, thresholds, dimensions)

    def build_recommendations(
        self,
        dimension_scores: dict[str, float | None],
        weights: dict[str, float],
        thresholds: dict[str, float],
        variables: dict[str, Any],
    ) -> list[str]:
        """Generate ordered improvement recommendations.

        Default implementation produces generic recommendations for dimensions
        below their thresholds, ordered by impact (weight * gap).

        Override to provide domain-specific advice.

        Args:
            dimension_scores: Dimension name -> score (may contain None).
            weights: Scaffold weight dict.
            thresholds: Scaffold threshold dict.
            variables: The raw extracted variables.

        Returns:
            List of recommendation strings, highest impact first.
        """
        clean = {k: v for k, v in dimension_scores.items() if v is not None}
        return _build_recommendations(clean, thresholds, weights)

    # ------------------------------------------------------------------
    # Core pipeline — extract, score, create_record
    # ------------------------------------------------------------------

    def extract(self, context: DomainContext) -> dict[str, Any]:
        """Run all extractors and merge their results.

        Args:
            context: The frozen domain context.

        Returns:
            Merged dict of all extracted variables.
        """
        merged: dict[str, Any] = {}
        for extractor in self.get_extractors():
            try:
                result = extractor.extract(context)
                merged.update(result)
            except Exception:
                logger.warning(
                    "Extractor '%s' in domain '%s' raised, skipping.",
                    extractor.name,
                    self.name,
                    exc_info=True,
                )
        return merged

    def score(
        self,
        variables: dict[str, Any],
        scaffold: str | Scaffold,
    ) -> DomainScore:
        """Score variables against a scaffold.

        If ``scaffold`` is a string, it is treated as the scaffold name
        and resolved from ``self.scaffold_dir`` by trying extensions
        ``.yml``, ``.yaml``, and ``.json`` in order.

        The pipeline delegates to overridable hooks at each step:

        1. Load scaffold (if string).
        2. Compute dimension scores — via ``score_dimension()`` when
           ``get_dimension_variables()`` is non-empty, otherwise via
           direct variable-to-weight mapping.
        3. Compute weighted overall from dimension scores.
        4. Evaluate hard blocks via ``evaluate_hard_blocks()``.
        5. Determine verdict via ``determine_verdict()``.
        6. Build recommendations via ``build_recommendations()``.

        Args:
            variables: Extracted variable dict.
            scaffold: A Scaffold instance or the name of a scaffold file.

        Returns:
            A frozen DomainScore with verdict, dimensions, and recommendations.

        Raises:
            FileNotFoundError: If no scaffold file is found for the name.
        """
        if isinstance(scaffold, str):
            scaffold_path = _resolve_scaffold_path(
                self.scaffold_dir, scaffold,
            )
            scaffold = load_scaffold(scaffold_path)

        dim_var_map = self.get_dimension_variables()

        if dim_var_map:
            # Dimension-based scoring: each weight key maps to a dimension
            # composed of multiple variables, scored via hooks.
            dimension_scores_raw: dict[str, float | None] = {}
            for dim in scaffold.weights:
                dimension_scores_raw[dim] = self.score_dimension(
                    dim, variables,
                )

            # Compute weighted overall from non-None dimension scores
            total_weight = 0.0
            weighted_sum = 0.0
            for dim, dscore in dimension_scores_raw.items():
                weight = scaffold.weights.get(dim, 0.0)
                if dscore is not None and weight > 0:
                    weighted_sum += weight * dscore
                    total_weight += weight

            overall = weighted_sum / total_weight if total_weight > 0 else 0.0

            # Clean dimensions for output (remove None entries)
            dimensions = {
                k: v for k, v in dimension_scores_raw.items()
                if v is not None
            }
        else:
            # Simple 1:1 scoring: weight keys are variable names directly
            overall, dimensions = _compute_weighted_score(
                variables, scaffold.weights,
            )
            dimension_scores_raw = {k: v for k, v in dimensions.items()}

        hard_blocks = self.evaluate_hard_blocks(
            scaffold.hard_blocks, variables,
        )
        verdict = self.determine_verdict(
            overall, hard_blocks, scaffold.thresholds, dimensions, variables,
        )
        recommendations = self.build_recommendations(
            dimension_scores_raw, scaffold.weights,
            scaffold.thresholds, variables,
        )

        return DomainScore(
            overall=overall,
            dimensions=dimensions,
            hard_blocks=hard_blocks,
            verdict=verdict,
            recommendations=recommendations,
            variables=variables,
            scaffold_name=scaffold.name,
        )

    def create_record(
        self,
        score: DomainScore,
        context: DomainContext,
        equilibrium_score: float | None = None,
        convergence: str | None = None,
    ) -> DomainRecord:
        """Build a DomainRecord for persistence.

        Args:
            score: The computed domain score.
            context: The domain context (serialized to summary).
            equilibrium_score: Optional equilibrium quality metric.
            convergence: Optional convergence state string.

        Returns:
            A frozen DomainRecord ready for storage.
        """
        context_summary: dict[str, Any] = {
            "workspace": str(context.workspace),
            "changed_files_count": len(context.changed_files),
            "metadata_keys": list(context.metadata.keys()),
        }

        return DomainRecord(
            domain=self.name,
            score=score,
            context_summary=context_summary,
            equilibrium_score=equilibrium_score,
            convergence=convergence,
        )
