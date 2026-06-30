# Domain Framework

DomainPlugin abstract base class defining the scoring interface, lifecycle hooks, and integration points for domain-specific deliberation logic (spec 030).

This module contains the full domain plugin infrastructure. `DomainPlugin` is the abstract base class that domain implementations extend, providing overridable hooks for extraction, scoring, verdict determination, and recommendation generation. `VariableExtractor` is a runtime-checkable protocol for data collection. `DomainContext`, `DomainScore`, `DomainRecord`, and `TrendResult` are frozen Pydantic models that flow through the pipeline. `Scaffold` defines the weight/threshold/hard-block configuration loaded from YAML or JSON. Pure functions handle weighted scoring (`_compute_weighted_score`), hard block evaluation (`_check_hard_blocks`, `_evaluate_single_hard_block`), verdict logic (`_determine_verdict`), and recommendation generation (`_build_recommendations`).

::: deliberator.domains.base
    options:
      members:
        - DomainContext
        - DomainScore
        - DomainRecord
        - TrendResult
        - Scaffold
        - load_scaffold
        - VariableExtractor
        - DomainPlugin
        - _compute_weighted_score
        - _check_hard_blocks
        - _evaluate_single_hard_block
        - _evaluate_hard_block_rules
        - _determine_verdict
        - _build_recommendations
        - _linear_slope
