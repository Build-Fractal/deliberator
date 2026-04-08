# plugin-engineer Cross-Review of optimization-engineer

**Cross-reviewer**: plugin-engineer
**Reviewing**: optimization-engineer Phase 1 review of spec 023
**Date**: 2026-04-01

---

## Agreements

### 1. MIP formulation is correct but over-engineered for current scale

optimization-engineer's analysis is precise: the binary selection formulation is mathematically equivalent to grid search, and for 135 grid points, the MIP solver overhead likely exceeds the grid search time. I agree this should be documented (P1-1) to set correct expectations.

However, I disagree that this is a weakness. The MIP formulation is an extensibility investment:
- Adding constraints (e.g., "agent count must be odd" or "at least 2 iterations for mode X") requires one AMPL constraint line, not a conditional in the grid search loop.
- Scaling to continuous variables (e.g., fractional iterations, budget allocation across components) requires changing the variable declarations, not rewriting the search algorithm.
- Warm-starting from previous solutions is supported by MIP solvers, not by grid search.

The current overhead is acceptable given the extensibility benefits.

### 2. Quality and cost model verification is thorough

The exact match verification at all grid points (0% error) is strong evidence. optimization-engineer correctly notes that FR-004's "within 5%" threshold is exceeded.

### 3. Grid point enumeration is correct

The range bounds (rounds 1-5, iterations 1-3, agents 2-max) and the max_agents clamping to [2, 10] match the spec.

---

## Tensions

### 1. General-purpose API model validation

optimization-engineer recommends basic model validation in `solve_ampl()` (P2-1). I have a different view: AMPL itself validates models during `eval()` or `read()`. Adding a wrapper-level validator would duplicate AMPL's parsing logic (poorly -- we cannot match AMPL's parser). The better approach is to catch AMPL's parse errors and wrap them in a user-friendly exception:

```python
try:
    ampl.eval(model)
except Exception as e:
    raise ValueError(f"AMPL model parse error: {e}") from e
```

This gives users a clear error without reimplementing AMPL's parser.

### 2. Performance documentation priority

optimization-engineer's P1-1 (document MIP-vs-grid-search performance trade-off) is valid content but P1 seems too high. Users of the config optimizer API do not choose between MIP and grid search -- the dispatch layer chooses automatically. The documentation is informational, not safety-critical. I would classify this as P2.

---

## Missed Opportunities

### 1. No discussion of the AMPL model string as infrastructure

The AMPL model is stored as a Python string constant (`CONVERSUS_CONFIG_MODEL`). optimization-engineer reviews the model's mathematical content but not its distribution mechanism. For the general-purpose API, users may want to provide custom models. The API supports this via the `model` parameter. But the built-in conversus model is not extractable as a standalone `.mod` file that users can inspect, modify, and pass back. Adding a function to write the model to a `.mod` file would improve usability:

```python
def write_config_model(path: str) -> None:
    """Write the conversus config AMPL model to a .mod file."""
    with open(path, 'w') as f:
        f.write(CONVERSUS_CONFIG_MODEL)
```

### 2. No analysis of HiGHS solver options

optimization-engineer discusses the model formulation in detail but does not review the HiGHS configuration. The only option set is `time_limit`. HiGHS has many other options (threads, presolve level, MIP gap tolerance) that could affect solution quality and performance. For the trivial binary selection problem, defaults are fine. For the general-purpose API, exposing solver options would be valuable.
