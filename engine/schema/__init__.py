"""Schema package for v4.2.0 Structured Deliberation Outputs (Component Principle XXIX).

Public API:
- slot_parser: parses agent prose into structured slot fields per SLOT_SYNTAX.md
- v1/: versioned JSON Schema files (envelope + per-output-type body schemas + validator-error)

The slot syntax contract is specified in `SLOT_SYNTAX.md` (ratified via v4.2.0 F1).
The validator class is in `engine.schema_validator` (one level up).
"""
