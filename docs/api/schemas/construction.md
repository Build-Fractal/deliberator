# Construction Pipeline

Guided objective function construction from natural-language prompts through decision classification, template selection, gap analysis, and final assembly (spec 014).

This module implements the full construction pipeline: classifying a user's natural-language prompt into a `DecisionType`, selecting candidate objective templates, extracting explicit parameters, identifying gaps (missing required parameters), filling those gaps via a `GapFiller` strategy, and assembling the final `AssembledObjective`. The pipeline can run non-interactively (fail on gaps) or interactively (prompt the user). Template loading functions read objective and constraint templates from the bundled YAML schema files.

::: deliberator.schemas.construction
    options:
      members:
        - DecisionType
        - AssembledObjective
        - SourceProvenance
        - GapFiller
        - NonInteractiveGapFiller
        - InteractiveGapFiller
        - TemplateSelector
        - classify_decision_type
        - select_candidate_templates
        - extract_explicit_parameters
        - identify_gaps
        - fill_parameter_gaps
        - assemble_objective
        - construct_objective
        - load_objective_templates
        - load_constraint_templates
