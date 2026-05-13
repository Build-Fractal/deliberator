# Feature Specification: v4.2.0 Structured Deliberation Outputs (JSON Schema)

**Feature ID:** `v4.2.0-structured-deliberation-outputs`
**Created:** 2026-05-12
**Status:** **v5 / post-blind-verification / pre-ratification** (2026-05-13)
**Depends On:** v4.1.0-persistence-contract-discipline (Tier 2 Principle XXVIII must be ratified; that ratification — commit `551f647` in `clariti-care/payer-index-mono`, `build-fractal/conversus/CONSTITUTION.md` L490-644 — is the doctrinal anchor this spec implements).
**Governed by:** `https://github.com/clariti-care/payer-index-mono/blob/main/build-fractal/conversus/GOVERNANCE.md` § Pathway Taxonomy (**MINOR** pathway — additive component-tier discipline; no existing principle removed, renamed, or substantively re-scoped).
**Pathway:** MINOR
**Tier target:** **Component (Tier 3)** — conversus-oss-specific implementation of Tier 2 Principle XXVIII. Tier placement was **TIER-3-CONFIRMED** by the originating arbitration (`deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` Q3).

---

## Changelog: v4 → v5

The **blind verification arbitration** (2026-05-13, `deliberations/v4.2.0-structured-deliberation-outputs-blind-2026-05-13/arbitration/resolution.md`) returned **IMPLEMENTABLE-WITH-CLARIFICATIONS on Q1**, **MODERATE-RISK-MANAGEABLE on Q2**, and **HOLDS-AS-DOCTRINE on Q3**. Combined disposition: **PROCEED TO RATIFICATION with F-conditions F1-F4 applied to produce spec v5**. The blind verification stage is the final verification gate; v5 is the ratification-ready spec.

| F# | Summary | Lands in |
|---|---|---|
| F1 | **Sequencing and dependency gates.** § 11 implementation order specifies template slot syntax completion as a prerequisite gate before validator error specification development begins (unidirectional dependency, not parallel tracks). § 9.1 clarifies that technical specification gaps (template syntax, validator interface, CI implementation) are prerequisite to operational capacity validation; governance framework development may proceed in parallel. | § 11, § 9.1 |
| F2 | **Concrete implementation specifications.** § 5.1 replaces v4 validator pseudocode with concrete Python 3.12 class signatures (Principle IX: explicit type annotations + Pydantic v2 models): `SchemaValidator`, `ValidationResult`, `ValidationWarning`. § 5.4 replaces the CI gate prose with a complete GitHub Actions workflow YAML example. § 5.1 adds a performance budget validation subsection requiring measurement against representative large outputs (>100K char synthesis) before architectural lock-in of the <100ms target. | § 5.1, § 5.4 |
| F3 | **CONSUMER-CONTRACT.md six-section template.** § 7.1 converts from descriptive content specification to a fully-fleshed normative template — each of the six section headings written verbatim, required language under each heading, worked example for conversus-oss declaring deliberation-output schemas. Engineers writing CONSUMER-CONTRACT.md should be able to copy-paste-adapt the template. | § 7.1 |
| F4 | **Doctrinal archaeology separation.** Accumulated changelog entries (v1→v2→v3→v4→v5), C/D/E/F-condition fix-ledger rows, and historical context narratives moved to a new **Appendix A: Deliberation Archaeology** at the end of the spec. §§ 9, 9.1, 9.2, 11 normative cores (temporal-constraint rule, E2 technical precondition, D5 categorical prohibitions, E4 precedent-citation requirement, § 9.2 cross-tier weakening verification matrix, § 11 implementation order + tiered rollout dates) are retained in-line. Goal: a reader who wants to implement v5 reads §§ 1-8 + § 9 + § 10 + § 11 (normative core); a reader who wants ratification audit trail reads Appendix A. | New Appendix A; §§ 9, 11 |

F1-F4 are clarifications and structural separation; no v4 substantive decision is reopened. In particular: the D1 non-blocking validator architecture is preserved verbatim (F2's class signatures wrap the existing `path.write_bytes(content)`-before-warning architecture, they do not reverse it); the D5+E2+E4 layered containment on the temporal-constraint accommodation (§ 9.1) is preserved verbatim; the § 9.2 cross-tier weakening verification matrix is preserved verbatim. **v5 PROCEEDS TO RATIFICATION.**

**Prior-version changelogs (v1→v2 C1-C10, v2→v3 D1-D15, v3→v4 E1-E4) are moved to Appendix A: Deliberation Archaeology** as part of F4's separation of normative core from ratification audit trail. Readers implementing v5 do not need to read those changelogs; readers auditing the ratification trail will find them in Appendix A.

---

## 1. Motivation

**Document status.** This spec (v5) has completed the full four-stage verification protocol per § 9: originating (PASSed with C1-C10 → v2), self-consistency (FAIL-CONTRADICTION on Q3 → D1-D15 applied → v3), self-consistency rerun (PASS-WITH-CLARIFICATIONS on Q1/Q2/Q3 → E1-E4 applied → v4), and blind verification (IMPLEMENTABLE-WITH-CLARIFICATIONS on Q1, MODERATE-RISK-MANAGEABLE on Q2, HOLDS-AS-DOCTRINE on Q3 → F1-F4 applied → this v5). All four stages PASSed under their respective verdict variants. Combined disposition: **PROCEED TO RATIFICATION.**

Tier 2 Principle XXVIII ("Persistence Contract Discipline") was ratified 2026-05-12 (`build-fractal/conversus/CONSTITUTION.md` L490-644) with a universal 2026-12-01 remediation deadline for all conversus-suite products. The principle mandates: declared schemas with `schema_version` (SemVer), mechanical CI enforcement, versioning bump procedure, cross-product `CONSUMER-CONTRACT.md` files declaring stable surfaces, and explicit declaration scope. Schema declaration without mechanical enforcement is itself a violation.

Conversus-oss's load-bearing persistent state surface is the **deliberation output set** — six output types produced per phase per deliberation. These outputs are persisted to disk under `deliberations/{deliberation-id}/`, consumed by:
- Subsequent phases within the same deliberation (e.g., phase 5 synthesis reads phases 1-4 outputs);
- The arbiter's grep-based triggers (e.g., `disputes_remain`);
- The orchestrator adapter (`scripts/dispatch/adapters/tool/conversus.sh`), which currently parses markdown headings to extract verdicts;
- Human readers reviewing the audit trail.

Today the contract between producer (agent prose) and consumers (engine triggers, downstream phases, orchestrator adapter) lives in **display text** — markdown headings, prose patterns, and parser-grep regexes — and silently short-circuits when prose drifts. This spec is the first concrete implementation of Principle XXVIII for conversus-oss.

### 1.1 Three recurring production bugs this spec addresses

These are the load-bearing motivation. The spec must cite each one as an existence proof that the current display-text contract is broken.

**Bug A — Phase 5 prompt-overflow crash (recurring).** Synthesis prompt assembles all phase 1-4 outputs as free-form markdown concatenation. Two production incidents documented:
- 2026-05-06 arbitration silent-failure: synthesis prompt exceeded ~230K chars, arbitration phase dispatched then crashed silently in ~1ms (memory: `project_conversus_arbitration_crash_2026_05_06.md`). Phases 1-5 succeeded; only arbitration crashed at dispatch.
- v4.1.0 originating deliberation (2026-05-11): same class of overflow, different manifestation — rate-limit response surfaced rather than silent crash, but root cause identical (unbounded prose concatenation).

Both incidents stem from synthesis output being unbounded prose. Structured JSON output constrains the prompt assembly path: the engine can serialize only specific fields (e.g., `verdict` + `conditions` without `rationale` prose), bounding synthesis prompt size deterministically.

**Bug B — Phase 2 cross-review persistence quirk.** Engine warnings show cross-review files expected at `{agent}/cross-reviews/{other-agent}.md` sometimes don't persist to disk; downstream phases consume "in-memory" cross-reviews that aren't on disk. Format-contract drift between agents' emitted markdown structure and engine's file-storage expectations: agents emit headings/structure that the engine's writer doesn't recognize as a valid cross-review, so the writer silently elides them. This is a class-of-bug expression of "contract lives in display text" — the storage layer's parse contract is undocumented and grep-fragile.

**Bug C — Phase 6 `disputes_remain` trigger silently missed.** The v4.1.0 blind-verification synthesis used "Critical Unresolved Tensions" terminology where the engine grep-matches for `DISPUTES_BEGIN`/`DISPUTES_END` markers. Arbiter didn't fire even though tensions existed; manual arbitration was required (memory: `project_conversus_pr23_meta_cl.md`, "manual challenge-loop orchestration pattern"). **This bug is the cleanest example of why structural schema enforcement matters** — an agent emitting prose that happens not to match the engine's parser regex causes the engine to silently skip the dispute-resolution phase. Under JSON Schema, the trigger becomes `len(synthesis["disputes"]) > 0` — structural, not regex.

**Real-time confirmation.** The originating arbitration of this very spec (2026-05-13) was produced *manually* because Phase 6 didn't fire — the Phase 5 synthesizer wrote "Remaining Disputes" rather than the engine's expected marker pair. That is Bug C reproducing in the deliberation tasked with verifying the bug's fix. See `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` "Process Note".

### 1.2 Doctrinal anchor

Principle XXVIII sub-clause 1 mandates declared schemas in a discoverable location. Sub-clause 2 mandates mechanical CI enforcement. Sub-clause 3 mandates `schema_version` (SemVer by default). Sub-clause 4 mandates `CONSUMER-CONTRACT.md` declaring stable surfaces consumed by cross-product code. Sub-clause 5 mandates explicit declaration of display-text surfaces (or migration off them). This spec satisfies all five sub-clauses for the conversus-oss deliberation output set.

---

## 2. Goals

1. **Single JSON Schema family** defining all six conversus deliberation output types, with a common envelope (agent identity, deliberation context, timestamp, target file refs, `schema_version`, stage/engine/commit provenance) plus per-type bodies. Schema `$id` base: `https://build-fractal.org/conversus/schema/v1/`.
2. **`schema_version` field on every output**, populated by the engine at write time, conforming to Principle XXVIII sub-clause 3 (SemVer with documented total ordering). Initial release: `1.0.0-rc.1` per C10.
3. **PR-required CI gate** validating every agent output against the schema before commit, per Principle XXVIII sub-clause 2. The gate runs in `conversus-oss` CI on every PR that touches `deliberations/**` or `engine/**`; failures block merge.
4. **Backward-compatibility / migration path** for existing markdown-format deliberation outputs. The v4.1.0 audit trail (4 deliberations, ~150 markdown files) must remain readable. Migration strategy in § 11.
5. **Human-readable rendering path.** JSON outputs are accompanied by an engine-generated `.md` companion so the audit trail is human-readable without specialized tooling. Default: JSON is canonical; companion `.md` is rendered-for-humans, regenerable from JSON.
6. **`CONSUMER-CONTRACT.md`** at conversus-oss repo root declaring the JSON Schema as a stable surface consumed by the orchestrator adapter (and any future conversus-suite consumer), per Principle XXVIII sub-clause 4.

---

## 3. Non-goals

- **Not** proposing structured-schema discipline for non-deliberation conversus artifacts (engine state, provider auth tokens, evaluation results, mode templates). Those are separate persistent state surfaces with their own contract decisions to make.
- **Not** mandating JSON Schema for `CONSTITUTION.md`, `CONFORMANCE.md`, `COMPLIANCE.md`, or `GOVERNANCE.md`. Constitutional documents have their own conventions (markdown with structured headings) and are out of scope.
- **Not** requiring agents to write JSON directly in their prose. Agents emit structured prose in defined slots; the engine wraps in a JSON envelope on write. Agent prompts change; agent output format from the agent's perspective stays close to current prose conventions (with explicit field markers).
- **Not** replacing the engine dispatch architecture, the phase pipeline, or the agent abstraction. This spec changes only the format of the artifacts written to disk and consumed by downstream phases + external consumers.
- **Not** retroactively re-emitting historical deliberation outputs in JSON. The migration path (§ 11) is forward-only: new deliberations use JSON; historical markdown deliberations remain as-is and continue to render readably.

---

## 4. Schema

### 4.0 Schema location declaration (D9)

Per Principle XXVIII sub-clause 1 (CONSTITUTION.md L505-510), the schema location MUST be declared in the producer repo's `CONFORMANCE.md` and linked from both `README.md` AND `CLAUDE.md`. v3 satisfies this textually:

- **Canonical location:** `engine/schema/v1/*.schema.json` inside `Build-Fractal/conversus-oss/`.
- **Declared in:** `conversus-oss/CONFORMANCE.md` Persistence-Contract row (updated per § 6.1 D9). The row names the directory, the file-naming convention (`{output-type}.schema.json` + `envelope.schema.json` + `validator-error.schema.json`), and the `$id` URI base.
- **Linked from:** `conversus-oss/README.md` and `conversus-oss/CLAUDE.md` "Persistence Contract" sections (added per § 6.1 D10), each linking to `CONSUMER-CONTRACT.md` (which in turn links to the schema directory).

This satisfies XXVIII sub-clause 1's "discoverable location" + "linked from BOTH" textual requirements.

The canonical schema language is **JSON Schema** (Draft 2020-12). The canonical wire format on disk is **JSON** (`.json` files). All schema files live under `engine/schema/v1/` and are addressable by `$id` URIs anchored at `https://build-fractal.org/conversus/schema/v1/`. This choice — both schema language and file format are JSON — was unanimously converged on by all four originating-deliberation agents (per `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` Q2 Per-axis finding 5: "XML's CDATA-escaping burden on agent prose containing `<`, `>`, `&` characters; JSON Schema's Python `jsonschema` library being a near-universal dependency; JSON Schema's superior validation error messages; ubiquitous shell-tool parsing (`jq`) vs xmllint specialized tooling"). The previous XSD strawman is retired.

### 4.1 Common envelope

Every output document is a JSON object with the following envelope fields wrapping a `body` object whose shape is determined by `output_type`:

```json
{
  "$schema": "https://build-fractal.org/conversus/schema/v1/envelope.schema.json",
  "schema_version": "1.0.0-rc.1",
  "output_type": "review",
  "agent_name": "pragmatist",
  "deliberation_id": "v4.2.0-structured-deliberation-outputs-originating-2026-05-12",
  "deliberation_stage": "originating",
  "engine_version": "0.7.3",
  "source_commit": "551f647",
  "phase_iteration": 1,
  "timestamp": "2026-05-12T15:42:08Z",
  "target_files": ["specs/v4.2.0-structured-deliberation-outputs/spec.md"],
  "body": { /* per-type body */ }
}
```

The envelope JSON Schema (`engine/schema/v1/envelope.schema.json`):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://build-fractal.org/conversus/schema/v1/envelope.schema.json",
  "title": "Conversus Deliberation Output Envelope",
  "type": "object",
  "required": [
    "schema_version", "output_type", "agent_name",
    "deliberation_id", "deliberation_stage", "engine_version",
    "source_commit", "timestamp", "body"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+(-[A-Za-z0-9.-]+)?$"
    },
    "output_type": {
      "type": "string",
      "enum": ["review", "cross-review", "revision", "disputes", "synthesis", "arbitration"]
    },
    "agent_name": { "type": "string", "minLength": 1 },
    "deliberation_id": { "type": "string", "minLength": 1 },
    "deliberation_stage": {
      "type": "string",
      "enum": ["originating", "self-consistency", "blind"]
    },
    "engine_version": { "type": "string", "minLength": 1 },
    "source_commit": { "type": "string", "minLength": 4 },
    "phase_iteration": { "type": "integer", "minimum": 1 },
    "timestamp": { "type": "string", "format": "date-time" },
    "target_files": {
      "type": "array",
      "items": { "type": "string" }
    },
    "body": { "type": "object" }
  },
  "allOf": [
    { "if": { "properties": { "output_type": { "const": "review" } } },
      "then": { "properties": { "body": { "$ref": "review.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "cross-review" } } },
      "then": { "properties": { "body": { "$ref": "cross-review.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "revision" } } },
      "then": { "properties": { "body": { "$ref": "revision.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "disputes" } } },
      "then": { "properties": { "body": { "$ref": "disputes.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "synthesis" } } },
      "then": { "properties": { "body": { "$ref": "synthesis.schema.json" } } } },
    { "if": { "properties": { "output_type": { "const": "arbitration" } } },
      "then": { "properties": { "body": { "$ref": "arbitration.schema.json" } } } }
  ]
}
```

Required fields (per C6): `schema_version`, `output_type`, `agent_name`, `deliberation_id`, `deliberation_stage`, `engine_version`, `source_commit`, `timestamp`, `body`. Optional: `phase_iteration` (omitted for single-iteration phases), `target_files` (omitted for synthesis/arbitration where the target is the deliberation as a whole).

The three envelope identity fields added by C6 — `deliberation_stage`, `engine_version`, `source_commit` — make every output traceable to its exact production context (which stage of the four-stage methodology, which engine build, which spec commit was under review).

### 4.2 `review.schema.json` — Phase 1, initial review per agent

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/review.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["summary_assessment", "strengths", "concerns", "questions", "recommendation"],
  "properties": {
    "summary_assessment": { "type": "string", "minLength": 1 },
    "strengths": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "text"],
        "properties": {
          "id": { "type": "string", "pattern": "^S[0-9]+$" },
          "text": { "type": "string", "minLength": 1 }
        }
      }
    },
    "concerns": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "severity", "text"],
        "properties": {
          "id": { "type": "string", "pattern": "^C[0-9]+$" },
          "severity": { "enum": ["blocking", "substantive", "nit"] },
          "text": { "type": "string", "minLength": 1 }
        }
      }
    },
    "questions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "text"],
        "properties": {
          "id": { "type": "string", "pattern": "^Q[0-9]+$" },
          "text": { "type": "string", "minLength": 1 }
        }
      }
    },
    "recommendation": {
      "enum": ["APPROVE-AS-DRAFTED", "APPROVE-WITH-FIXES", "BLOCK", "ABSTAIN"]
    }
  }
}
```

`severity` is an enum: `blocking` (must-fix for ratification), `substantive` (should-fix), `nit` (cosmetic). The engine routes blocking concerns into the dispute set for phase 2.

### 4.3 `cross-review.schema.json` — Phase 2, agent X reviews agent Y's review

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/cross-review.schema.json",
  "type": "object",
  "required": ["reviewing_agent", "agreement_points", "disagreement_points", "new_concerns_raised"],
  "properties": {
    "reviewing_agent": { "type": "string", "minLength": 1 },
    "agreement_points": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ref", "text"],
        "properties": {
          "ref": { "type": "string" },
          "text": { "type": "string" }
        }
      }
    },
    "disagreement_points": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ref", "stance", "our_position", "their_position"],
        "properties": {
          "ref": { "type": "string" },
          "stance": { "enum": ["disagree", "partial-disagree"] },
          "our_position": { "type": "string" },
          "their_position": { "type": "string" }
        }
      }
    },
    "new_concerns_raised": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "severity", "text"],
        "properties": {
          "id": { "type": "string", "pattern": "^CR[0-9]+$" },
          "severity": { "enum": ["blocking", "substantive", "nit"] },
          "text": { "type": "string" }
        }
      }
    }
  }
}
```

`reviewing_agent` names whose review is being cross-reviewed; the wrapper `agent_name` in the envelope names the cross-reviewer. The `ref` on disagreement / agreement points lets phase 5 trace dispute lineage back to phase 1 origins. **This fixes Bug B**: cross-review files have a deterministic structure the engine writer recognizes; format drift can't elide them.

### 4.4 `revision.schema.json` — Phase 3, agent updates own position

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/revision.schema.json",
  "type": "object",
  "required": ["iteration", "position_changes", "updated_recommendation"],
  "properties": {
    "iteration": { "type": "integer", "minimum": 1 },
    "position_changes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ref", "delta", "prior", "revised", "triggered_by"],
        "properties": {
          "ref": { "type": "string" },
          "delta": { "enum": ["strengthened", "softened", "withdrawn", "unchanged"] },
          "prior": { "type": "string" },
          "revised": { "type": "string" },
          "triggered_by": { "type": "string" }
        }
      }
    },
    "updated_recommendation": {
      "enum": ["APPROVE-AS-DRAFTED", "APPROVE-WITH-FIXES", "BLOCK", "ABSTAIN"]
    }
  }
}
```

`iteration` matches `phase_iteration` on the envelope; multiple revision iterations are supported (e.g., `revision.json` + `revision_2.json`).

### 4.5 `disputes.schema.json` — Phase 4, agent consolidates remaining disagreements

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/disputes.schema.json",
  "type": "object",
  "required": ["disputes"],
  "properties": {
    "disputes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "severity", "topic", "our_position", "opposing_positions", "proposed_resolution", "fallback_if_unresolved"],
        "properties": {
          "id": { "type": "string", "pattern": "^D[0-9]+$" },
          "severity": { "enum": ["blocking", "substantive"] },
          "topic": { "type": "string" },
          "our_position": { "type": "string" },
          "opposing_positions": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["agent", "stance"],
              "properties": {
                "agent": { "type": "string" },
                "stance": { "type": "string" }
              }
            }
          },
          "proposed_resolution": { "type": "string" },
          "fallback_if_unresolved": { "type": "string" }
        }
      }
    }
  }
}
```

### 4.6 `synthesis.schema.json` — Phase 5, single agent integrates all prior outputs

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/synthesis.schema.json",
  "type": "object",
  "required": ["agreement_areas", "disputes", "emergent_patterns", "recommendation_to_arbiter"],
  "properties": {
    "agreement_areas": {
      "type": "array",
      "items": { "type": "string" }
    },
    "disputes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "severity", "topic", "positions", "synthesizer_assessment"],
        "properties": {
          "id": { "type": "string", "pattern": "^D[0-9]+$" },
          "severity": { "enum": ["blocking", "substantive"] },
          "topic": { "type": "string" },
          "positions": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["agent", "stance"],
              "properties": {
                "agent": { "type": "string" },
                "stance": { "type": "string" }
              }
            }
          },
          "synthesizer_assessment": { "type": "string" }
        }
      }
    },
    "emergent_patterns": {
      "type": "array",
      "items": { "type": "string" }
    },
    "recommendation_to_arbiter": { "type": "string" }
  }
}
```

**This fixes Bug C**: the engine's `disputes_remain` trigger becomes the JSON-path expression `len([d for d in synthesis["body"]["disputes"] if d["severity"] == "blocking"]) > 0`. Structural, not regex. No prose drift can hide a dispute from the trigger.

**This also fixes Bug A**: the engine's synthesis-prompt assembler can serialize only specific subtrees per downstream consumer — e.g., the arbitration prompt receives `disputes` + `recommendation_to_arbiter` only, not the full `agreement_areas` + `emergent_patterns` prose. Synthesis prompt size becomes bounded by the union of dispute count × per-dispute schema-cap, not by free prose.

### 4.7 `arbitration.schema.json` — Phase 6, arbiter's binding verdict

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/arbitration.schema.json",
  "type": "object",
  "required": ["process_note", "decision_framework", "per_question_rulings", "combined_disposition", "ruling_lines"],
  "properties": {
    "process_note": { "type": "string" },
    "decision_framework": { "type": "string" },
    "per_question_rulings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["question", "verdict", "rationale", "conditions"],
        "properties": {
          "question": { "type": "string", "pattern": "^Q[0-9]+$" },
          "verdict": {
            "enum": [
              "APPROVE-AS-DRAFTED", "APPROVE-WITH-FIXES", "BLOCK",
              "PASS-WITH-CLARIFICATIONS", "FAIL-OVERSTRETCH",
              "TIER-3-CONFIRMED", "RECURSION-EXEMPTED"
            ]
          },
          "rationale": { "type": "string" },
          "conditions": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["id", "priority", "description", "applies_to_section"],
              "properties": {
                "id": { "type": "string", "pattern": "^C[0-9]+$" },
                "priority": { "enum": ["P1", "P2", "P3"] },
                "description": { "type": "string" },
                "applies_to_section": { "type": "string" }
              }
            }
          }
        }
      }
    },
    "combined_disposition": {
      "enum": ["PROCEED-TO-RATIFICATION", "PROCEED-TO-NEXT-STAGE", "PROCEED-TO-SELF-CONSISTENCY", "RETURN-TO-REVIEW", "BLOCK"]
    },
    "ruling_lines": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["question", "verdict", "rationale"],
        "properties": {
          "question": { "type": "string", "pattern": "^Q[0-9]+$" },
          "verdict": { "type": "string" },
          "rationale": { "type": "string" }
        }
      }
    }
  }
}
```

`verdict` enum is intentionally union-typed across the verdict vocabularies used by originating, self-consistency, and blind verification stages (cf. v4.1.0 spec's verdict vocabulary). The enum is closed; new verdict values require a schema MINOR bump.

The redundant `ruling_lines` array (a denormalized projection of `per_question_rulings`) exists for adapter convenience — orchestrator currently grep-extracts one-line ruling summaries and benefits from a flat list. Validator enforces that `ruling_lines` entries match the question/verdict pairs in `per_question_rulings`.

### 4.8 Schema versioning (C8, C10)

The wire format version is named in the envelope's `schema_version` field. **Initial release: `1.0.0-rc.1`** (per C10). After one ratification cycle of clean operation (≥30 days of real production deliberations producing conformant outputs with zero unplanned schema bumps), the version bumps to `1.0.0`. The release-candidate suffix is a stability signal to consumers that the schema may receive ergonomic refinement during the rc window.

Bumps follow Principle XXVIII sub-clause 3 (SemVer) with the C8 consumer-impact qualification:

- **MAJOR** (incompatible): removed required field; removed enum value; type narrowing of an existing field (e.g., `string` → `string` with new `pattern`); **renaming a field even when technically additive** (consumers parse by name, so renames break them); **adding a required field** (existing conformant outputs become non-conformant).
- **MINOR** (additive): adding an optional field; adding a new enum value; adding a new output type to the `output_type` enum; loosening a constraint (e.g., relaxing a `pattern`).
- **PATCH** (clarification): refining a description / docstring; tightening a `pattern` or `enum` in a way no existing real output violates (verified against the historical fixture corpus); fixing a typo in a constraint.

A schema bump that *would* be MINOR by raw schema diff but breaks consumers because of a field-name dependency is classified MAJOR. The validator carries a single `current_supported_versions` allowlist (per Principle XXVIII C2 versioning gate). Outputs with `schema_version` outside the allowlist emit a validation warning to the deliberation event stream; the engine still writes the file (per D1 non-blocking discipline); the PR-required CI gate (§ 5.4) blocks merge on allowlist violation.

**Schema-advancement authority (D7).** The `1.0.0-rc.1` → `1.0.0` promotion decision is made by the **conversus-oss maintainer set** (the same set with merge authority on `main`), per the criteria below, recorded as a PR landing the version bump in `engine/schema/v1/envelope.schema.json` plus the `current_supported_versions` allowlist update in `engine/schema_validator.py`:

- **Quantitative criterion:** ≥30 days have elapsed since `1.0.0-rc.1` was first emitted in production, and during that window the CI schema-validation gate has run on every PR touching `deliberations/**` or `engine/**` with **zero unplanned schema bumps** (i.e., no MAJOR or MINOR amendments to the schema other than the rc-window ergonomic refinements anticipated by C10).
- **Qualitative criterion:** at least one full six-phase deliberation has been re-emitted under each migrated mode (per § 11 step 3) with all emitted JSON conforming to the schema, AND the orchestrator adapter migration (§ 6.2) has landed and parsed at least one real production arbitration successfully.
- **Audit trail:** the version-bump PR cites the deliberation-id corpus the quantitative criterion was measured against, and links to the green CI runs that confirm zero unplanned bumps.

The same authority applies to subsequent MAJOR / MINOR / PATCH bumps documented in this sub-section; the criteria for those bumps are the version-bump procedure itself (consumer impact + SemVer rules), not the rc-window criteria above.

### 4.9 Validator error object schema (C9)

Validation failures emit structured error objects, themselves a stable interface (so consumer tooling can rely on the failure surface). The error object schema (`engine/schema/v1/validator-error.schema.json`):

```json
{
  "$id": "https://build-fractal.org/conversus/schema/v1/validator-error.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["field_path", "error_code", "human_message", "expected_type", "actual_value"],
  "properties": {
    "field_path": {
      "type": "string",
      "description": "JSON pointer to the offending field, e.g., '/body/disputes/0/severity'"
    },
    "error_code": {
      "type": "string",
      "enum": [
        "REQUIRED_FIELD_MISSING",
        "TYPE_MISMATCH",
        "ENUM_VIOLATION",
        "PATTERN_VIOLATION",
        "ADDITIONAL_PROPERTY_FORBIDDEN",
        "SCHEMA_VERSION_UNSUPPORTED",
        "ENVELOPE_BODY_TYPE_MISMATCH",
        "ARRAY_MIN_ITEMS_VIOLATION"
      ]
    },
    "human_message": {
      "type": "string",
      "description": "Human-friendly explanation of the failure."
    },
    "expected_type": {
      "type": "string",
      "description": "The schema-declared expected shape (type or pattern or enum)."
    },
    "actual_value": {
      "description": "The actual value at field_path; may be any JSON type or null when field is missing."
    },
    "suggested_fix": {
      "type": "string",
      "description": "Optional: best-effort suggestion (e.g., 'change \"MAYBE\" to one of {APPROVE-AS-DRAFTED, APPROVE-WITH-FIXES, BLOCK}')."
    }
  }
}
```

This makes validator failures themselves machine-parseable and stable across schema versions.

---

## 5. Implementation

### 5.1 Engine changes (`conversus-oss/engine/`) — **non-blocking warning-based validation** (D1)

**Load-bearing constitutional constraint (Tier 2 Principle V, CONSTITUTION.md L76-78):**

> "Output validation (e.g., Phase 6 heading checks) emits **warnings** for malformed output but **does NOT block file writes**. Malformed output is better than no output."

The engine-side validation architecture for this spec MUST conform to that pillar. The validator runs at write-time and produces structured warnings, but the file IS ALWAYS WRITTEN. Mechanical enforcement bite (per Principle XXVIII sub-clause 2) is preserved at the PR-required CI gate (§ 5.4), which DOES block merge on validation failure. Write-time non-blocking + PR-time blocking together satisfy both Principle V and Principle XXVIII without contradiction. This is the load-bearing inversion from v2 — v2 had the validator abort the phase on failure (which directly negated Principle V); v3 has the validator emit warnings and always proceed (which preserves Principle V).

- **`engine/schema/v1/*.schema.json`** — JSON Schema files, one per output type plus the envelope plus the validator-error schema, anchored at `$id` base `https://build-fractal.org/conversus/schema/v1/`. JSON Schema Draft 2020-12. The Python `jsonschema` library (>= 4.x) is the canonical validator; it satisfies Principle XXVIII C2's mechanical-enforceability bar (binary pass/fail, field-presence check, type check, value-constraint check) without the XSD strawman's CDATA-escaping defect.

- **`engine/schema_validator.py`** — single entry point invoked on every agent output write. **Concrete Python 3.12 + Pydantic v2 class signatures (F2, Principle IX explicit type annotations + Pydantic models):**

  ```python
  from pathlib import Path
  from typing import Literal
  from pydantic import BaseModel, ConfigDict, Field


  class ValidationWarning(BaseModel):
      """Single conformance defect raised by the validator.

      Conforms to engine/schema/v1/validator-error.schema.json (§ 4.9).
      """
      model_config = ConfigDict(frozen=True, extra="forbid")

      field_path: str = Field(
          ...,
          description="JSON pointer to the offending field, e.g., '/body/disputes/0/severity'.",
      )
      error_code: Literal[
          "REQUIRED_FIELD_MISSING",
          "TYPE_MISMATCH",
          "ENUM_VIOLATION",
          "PATTERN_VIOLATION",
          "ADDITIONAL_PROPERTY_FORBIDDEN",
          "SCHEMA_VERSION_UNSUPPORTED",
          "ENVELOPE_BODY_TYPE_MISMATCH",
          "ARRAY_MIN_ITEMS_VIOLATION",
      ]
      severity: Literal["error", "warning"] = "warning"
      message: str = Field(..., min_length=1, description="Human-friendly explanation.")
      expected: str = Field(..., description="Schema-declared expected shape (type/pattern/enum).")
      actual: str = Field(..., description="Stringified actual value at field_path; '' when missing.")
      suggested_fix: str | None = None

      def to_dict(self) -> dict[str, str | None]:
          """Serialize for sidecar JSON + event stream. Pydantic v2 model_dump."""
          return self.model_dump(mode="json")


  class ValidationResult(BaseModel):
      """Aggregate result of a single validate() call.

      `is_conformant` is True iff `warnings` contains no entry with severity='error'.
      """
      model_config = ConfigDict(frozen=True, extra="forbid")

      is_conformant: bool
      warnings: list[ValidationWarning] = Field(default_factory=list)
      schema_version: str = Field(..., description="schema_version field read from envelope.")
      output_type: str = Field(..., description="output_type field read from envelope.")
      validation_duration_ms: float = Field(..., ge=0.0)


  class SchemaValidator:
      """Non-blocking JSON Schema validator for conversus deliberation outputs.

      Conforms to Principle V (non-blocking writes; CONSTITUTION.md L76-78) by design:
      `validate()` NEVER raises on conformance failure; it returns a structured
      ValidationResult. Callers (engine/persistence.py) ALWAYS proceed to write
      regardless of `is_conformant`. Mechanical enforcement bite lives at the
      PR-required CI gate (§ 5.4), not at write-time.
      """

      def __init__(self, schema_dir: Path) -> None:
          """Initialize validator with compiled schemas from schema_dir.

          Compilation is cached in memory for the process lifetime (performance
          discipline per § 5.1 performance budget validation framework).
          """
          ...

      def validate(self, content: bytes, schema_version: str) -> ValidationResult:
          """Validate `content` (raw bytes of a single deliberation output JSON file)
          against the schema selected by `schema_version` + envelope.output_type.

          MUST NOT raise on conformance failure. MUST raise only on infrastructure
          failure (e.g., schema file missing from schema_dir at construction time).
          Returns ValidationResult with is_conformant=False on any error-severity
          warning; warnings-only outputs return is_conformant=True with a non-empty
          `warnings` list.
          """
          ...

      def emit_warning(self, result: ValidationResult, output_path: Path) -> None:
          """Emit non-conformance to two channels: deliberation event stream
          (event='schema_validation_failed') + sibling .validation-warnings.json
          sidecar at `output_path.with_suffix(output_path.suffix + '.validation-warnings.json')`.

          Idempotent: calling twice for the same output path overwrites the sidecar.
          """
          ...
  ```

  **Integration points.**
  - **Called from:** `engine/persistence.py` (see below) on every output write. No other module instantiates `SchemaValidator` directly.
  - **Validator import failure handling:** if `schema_dir` is missing or schemas are malformed at construction time, `SchemaValidator.__init__` raises `RuntimeError`. The engine's persistence layer catches this once at startup and falls back to write-only mode (no validation, prominent log warning); per Principle V, validator unavailability MUST NOT block writes.
  - **Sidecar location:** `.validation-warnings.json` is written as a sibling to the output JSON, e.g., for `deliberations/{id}/phase-1/pragmatist/review.json` the sidecar is `deliberations/{id}/phase-1/pragmatist/review.json.validation-warnings.json`. CI § 5.4 detects sidecar presence and blocks merge.

- **`engine/persistence.py`** — the load-bearing non-blocking inversion lives here. **Concrete signature (F2, Principle IX):**

  ```python
  from pathlib import Path

  from engine.schema_validator import SchemaValidator

  def persist_output(
      path: Path,
      content: bytes,
      validator: SchemaValidator,
      event_stream: "EventStream",  # opaque to this signature; engine-local type
  ) -> None:
      """Persist a deliberation output to disk with non-blocking validation.

      Order of operations is load-bearing:
      1. `path.write_bytes(content)` — UNCONDITIONAL. Per Principle V
         (CONSTITUTION.md L76-78): "malformed output is better than no output".
         This MUST be the first side effect.
      2. validator.validate(content, schema_version) — produces ValidationResult.
      3. If not result.is_conformant: emit warning + write sidecar.

      There is no exception path that prevents step 1. SchemaValidator.validate()
      is contractually non-raising on conformance failure.
      """
      # Step 1 — unconditional write (Principle V).
      path.write_bytes(content)

      # Step 2 — validate after write. Validator unavailability is handled at
      # engine startup; here we assume `validator` is constructed successfully.
      schema_version = _read_schema_version(content)
      result = validator.validate(content, schema_version)

      # Step 3 — emit warning if non-conformant.
      if not result.is_conformant:
          event_stream.warn(
              event="schema_validation_failed",
              path=str(path),
              errors=[w.to_dict() for w in result.warnings],
          )
          validator.emit_warning(result, path)
  ```

  **The write at step 1 is unconditional.** Malformed output is preferred over no output, per Principle V. There is no `SchemaViolation` exception path in the persistence layer. F2's concrete signatures are added context for engineers implementing the engine; they do NOT reverse D1's non-blocking architecture, and the `path.write_bytes(content)` call MUST remain the first side effect of `persist_output`.

- **`engine/templates.py` + `templates/{mode}/`** — mode templates updated so agent prompts emit prose in explicit slots (e.g., `<<<STRENGTHS_BEGIN>>> ... <<<STRENGTHS_END>>>`). The engine's output wrapper parses agent prose, extracts slot values, and assembles a JSON envelope. Agents do NOT emit JSON directly; the engine assembles.

- **`engine/cli/run.py`** — adds `--validate-outputs` flag (default `true`). `--no-validate-outputs` disables the validation pass entirely (no warnings produced, no sidecar written). The flag's purpose is debugging / dev-loop speed, not bypassing enforcement: the file would be written either way; disabling validation only suppresses the warning record. The engine logs a prominent notice when the flag is set and records it in the deliberation event stream.

**Implementation performance discipline (D13).** The validator SHOULD complete in <100ms per output as an **operational target**. The `jsonschema` library on representative production-sized outputs (~20-50KB JSON) routinely completes in single-digit milliseconds; the 100ms target provides ~10-20× headroom. **This is implementation discipline, not a constitutional bar.** If a validator implementation exceeds 100ms in practice, the validator is the bug — fix the validator (caching compiled schemas, profiling hot paths) before relaxing the operational target. The CI gate (§ 5.4) runs the validator over the worked-example fixture corpus and asserts P99 latency < 100ms; failing that assertion blocks the merge of validator-implementation changes (not deliberation content). The <100ms number is recorded here as implementation discipline because that is what it actually is — operational engineering practice on a Python library with known performance characteristics — not as a constitutional mandate that would require constitutional-amendment process to relax.

#### 5.1.1 Performance budget validation framework (F2)

Before architectural lock-in of the <100ms operational target, the validator implementation MUST be measured against representative large outputs from real production deliberations. This validation MUST complete and PASS before § 11's implementation order proceeds past step 2 (the schemas+validator+renderer PR). The framework is intentionally bounded — it is one measurement campaign on the worked-example corpus, not an ongoing benchmark suite.

**Sample set.** The fixture corpus measured is:
- The four worked-example fixtures from § 5.3 (conformant + missing-required + wrong-type + enum-violation).
- The `synthesis.json` outputs from the v4.1.0 deliberation set (4 deliberations × 1 synthesis each = 4 outputs), specifically chosen because the v4.1.0 originating synthesis exceeded ~230K characters of free-form prose (cf. § 1.1 Bug A; memory `project_conversus_arbitration_crash_2026_05_06.md`). These represent the upper bound of realistic synthesis output size and exercise the validator's worst-case branch on body-schema dispatch + array-of-disputes traversal.
- The `arbitration.json` outputs from the same v4.1.0 deliberation set (4 outputs), which exercise the per-question-rulings + conditions + ruling_lines redundant-projection cross-check.

**Measurement methodology.**
- **Warm-cache:** validator is constructed once; schemas are compiled and cached in memory; each fixture is validated 100 times in sequence; latencies recorded as p50/p95/p99.
- **Cold-cache:** validator is reconstructed for each measurement (worst case for production startup); each fixture is validated 10 times in sequence; latencies recorded as p50/p95/p99.
- Both modes run on the standard conversus-oss CI runner (Ubuntu 22.04, default GitHub Actions instance).
- The measurement script lives at `engine/tests/test_validator_performance.py` and emits a `validator-performance-report.json` artifact uploaded by CI.

**Failure mode.** If warm-cache p99 across the synthesis-corpus subset exceeds 100ms:
- The validator is the bug per D13 — first remediation is to profile and fix.
- If after remediation warm-cache p99 still exceeds 100ms on a sustained basis, the validator MUST degrade gracefully: emit a `validator_latency_budget_exceeded` warning to the deliberation event stream, skip per-output validation for outputs above a size threshold (`len(content) > 100_000` bytes), and rely on the PR-required CI gate (§ 5.4) for those outputs instead. Skipping at write-time NEVER blocks the write per Principle V.
- The architectural lock-in of <100ms in § 4.8 + § 5.4 is contingent on this measurement passing. If it fails after remediation, § 4.8's "<100ms" reference is reclassified as "best-effort target with documented degradation behavior" and the spec is amended via a PATCH bump (per § 4.8 SemVer rules) to record the operational ceiling.

The performance budget validation is itself a prerequisite gate in § 11 (see F1 sequencing); validator+schema work cannot proceed past the schemas+validator PR until this campaign has run and the report is green or the documented degradation has been applied.

Advanced validations beyond write-time scope — cross-reference integrity (does `ruling_lines[i].question` match a real `per_question_rulings[j].question`?), full constraint validation across documents — run at the same write-time path, contributing additional `ValidatorError` entries to the result; they do not block the write either. C5's tiered staging defines when those advanced checks promote from advisory-only to PR-required-blocking at the CI gate.

### 5.2 Companion markdown rendering

- **`engine/render_md.py`** — pure function `json_to_md(json_path: Path) -> str`. The engine writes both `phase-1/review.json` (canonical) and `phase-1/review.md` (rendered companion) on every phase. The `.md` companion is regenerable from JSON; if someone edits `.md` directly, CI gates fail (the renderer is the only sanctioned writer of `.md` files under `deliberations/**`).
- Default rendering: section headings per output type, agent identity in the H1, structured body as nested H2/H3, enum values in backticks. The rendering is deterministic and reproducible.

### 5.3 Worked-example fixtures (per Principle XXVIII sub-clause 2 + D14)

Principle XXVIII sub-clause 2 (CONSTITUTION.md L538-545) requires each product to ship at least **three test fixtures**: (a) a known-conformant artifact that passes validation, (b) a known-non-conformant artifact with a missing required field that fails validation, and (c) a known-non-conformant artifact with a wrong field type that fails validation. v3 covers all three plus an additional enum-violation fixture to demonstrate the closed-enum mechanism the schema relies on heavily:

- **(a) Conformant —** `engine/tests/fixtures/schema/arbitration_conformant.json` — a passing arbitration output with all required envelope fields, all required body fields, valid enum values, and correctly-typed values throughout. Validator returns `is_conformant=True`, `errors=[]`.
- **(b) Missing required field —** `engine/tests/fixtures/schema/arbitration_missing_ruling.json` — missing required `per_question_rulings` entry for `Q3`. Validator returns `is_conformant=False`, error with `field_path=/body/per_question_rulings`, `error_code=REQUIRED_FIELD_MISSING` (or `ARRAY_MIN_ITEMS_VIOLATION` depending on whether the missing item is enforced via array `minItems` or array-membership cross-check).
- **(c) Wrong field type —** `engine/tests/fixtures/schema/arbitration_wrong_type.json` — `"phase_iteration": "1"` (string where integer required). Validator returns `is_conformant=False`, error with `field_path=/phase_iteration`, `error_code=TYPE_MISMATCH`, `expected_type=integer`, `actual_value="1"`.
- **(d) Enum violation (additional) —** `engine/tests/fixtures/schema/arbitration_wrong_verdict_type.json` — `"verdict": "MAYBE"` (value outside enum). Validator returns `is_conformant=False`, error with `field_path=/body/per_question_rulings/0/verdict`, `error_code=ENUM_VIOLATION`, `expected_type` listing the enum, `suggested_fix` proposing the closest valid value.

**Fixture scope coverage (D14).** Across (a)-(d) the fixture corpus mechanically demonstrates: **field presence** (b), **type checking** (c), **value constraints / enum membership** (d), and **end-to-end conformant baseline** (a). XXVIII sub-clause 2 explicitly names "field presence, types, and value constraints" as the enforcement surface; the four fixture types cover that surface in full.

Each fixture is paired with an expected validator output assertion in `engine/tests/test_schema_validator.py`. CI failure on any fixture mismatch blocks merge of validator-implementation changes (not deliberation content — per D1, deliberation content is never blocked at write-time).

### 5.4 CI gate (PR-required, merge-blocking — the enforcement bite)

D1 makes write-time validation non-blocking. The mechanical-enforcement teeth Principle XXVIII sub-clause 2 requires therefore live at the **PR-required CI gate** below. This is where the merge actually blocks; this is where producer code's conformance is enforced.

**Constitutional authority (E1).** The PR-blocking CI gate specified in this sub-section derives its authority from two ratified principles: **Tier 1 Principle II (Stable Interfaces)** — `build-fractal/CONSTITUTION.md` — which requires that declared technical contracts (here, the JSON Schema as a stable wire format) be enforced against regression at the point of code change; and **Tier 2 Principle XXVIII sub-clause 2 (mechanical CI enforcement, PR-required)** — `build-fractal/conversus/CONSTITUTION.md` L490-644 — which mandates that schema declarations carry mechanical CI bite at PR-time and explicitly forbids schema declaration without mechanical enforcement as a XXVIII violation. The PR-blocking posture below is the operationalization of both citations; absent it, the spec would itself violate XXVIII sub-clause 2.

**Complete GitHub Actions workflow YAML (F2 normative example).** The workflow below is the reference implementation of the PR-required CI gate. Engineers MAY adapt step names and Python versions, but the four jobs (forward-validation, drift-detection-bidirectional, schema-version-bump-detection, fixture+renderer tests), their merge-blocking posture, and their trigger paths are normative.

```yaml
# .github/workflows/schema-validate.yml
name: schema-validate

on:
  pull_request:
    paths:
      - 'deliberations/**'
      - 'engine/schema/**'
      - 'engine/schema_validator.py'
      - 'engine/persistence.py'
      - 'engine/render_md.py'
      - 'engine/tests/fixtures/schema/**'

# Required-check posture: every job in this workflow is configured as a
# required status check on the `main` branch protection rule. Failure of any
# job blocks PR merge per Principle XXVIII sub-clause 2 (mechanical CI
# enforcement, PR-required) + Tier 1 Principle II (Stable Interfaces).
jobs:
  validate-conformance:
    # Forward-validation: every JSON file under deliberations/ must conform to
    # the current schema. Sidecar .validation-warnings.json files indicate
    # producer code emitted a malformed file at write-time and MUST be fixed
    # before merge.
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install validator
        run: pip install -e '.[test]'
      - name: Run forward-validation over deliberations/
        run: python -m engine.schema_validator --all deliberations/
      - name: Assert no .validation-warnings.json sidecars present
        run: |
          if find deliberations -name '*.validation-warnings.json' | grep -q .; then
            echo "::error::Validation sidecars found — producer code emitted malformed outputs."
            find deliberations -name '*.validation-warnings.json'
            exit 1
          fi

  drift-detection-bidirectional:
    # D12 + Principle XXVIII sub-clause 2 ("Validation MUST be bidirectional").
    # Whenever the schema itself changes, re-validate the entire pre-existing
    # deliberations corpus under the new schema. Catches schema edits that
    # silently break previously-conformant artifacts.
    if: contains(github.event.pull_request.changed_files, 'engine/schema/v1/')
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install validator
        run: pip install -e '.[test]'
      - name: Re-validate full corpus under new schema
        run: python -m engine.schema_validator --all deliberations/ --schema-dir engine/schema/v1/
      - name: Diff against baseline conformance
        run: python -m engine.tests.drift_detection --baseline-ref ${{ github.event.pull_request.base.sha }}

  schema-version-bump-detection:
    # D15 + Principle XXVIII sub-clause 3 ("silent format changes are a violation").
    # Any edit to a schema file MUST be accompanied by either a $id version path
    # bump, an envelope schema_version pattern/enum bump, or a [schema:no-bump-justified]
    # token in the PR description with a rationale.
    if: contains(github.event.pull_request.changed_files, 'engine/schema/v1/')
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Detect schema-version bump
        env:
          PR_BODY: ${{ github.event.pull_request.body }}
        run: |
          python -m engine.tests.version_bump_check \
            --base-ref ${{ github.event.pull_request.base.sha }} \
            --head-ref ${{ github.sha }} \
            --pr-body "$PR_BODY"

  fixture-and-renderer-tests:
    # Four worked-example fixtures (§ 5.3) + renderer round-trip
    # (JSON → MD → JSON bit-identical for canonical-form) + D13 operational
    # target assertion (P99 < 100ms over fixture corpus, per § 5.1.1
    # performance budget validation framework).
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install validator + test deps
        run: pip install -e '.[test]'
      - name: Run validator unit tests
        run: pytest engine/tests/test_schema_validator.py -v
      - name: Run renderer round-trip tests
        run: pytest engine/tests/test_render_md.py -v
      - name: Run performance budget assertion
        run: pytest engine/tests/test_validator_performance.py -v
      - name: Upload performance report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validator-performance-report
          path: validator-performance-report.json
```

**Pass/fail is binary; failure of any job blocks merge.** Required-check setting enforced on the `main` branch protection rule. The four jobs together discharge: § 5.4 forward-validation (`validate-conformance`), § 5.4 D12 bidirectional drift detection (`drift-detection-bidirectional`), § 5.4 D15 schema-version-bump detection (`schema-version-bump-detection`), and § 5.3 + § 5.1.1 fixture + renderer + performance tests (`fixture-and-renderer-tests`).

---

## 6. File edits per repo

### 6.1 `Build-Fractal/conversus-oss/` (this repo)

- `engine/schema/v1/*.schema.json` (new) — JSON Schema files.
- `engine/schema_validator.py` (new).
- `engine/render_md.py` (new).
- `engine/persistence.py` (modified) — adds validate-then-write.
- `engine/cli/run.py` (modified) — adds `--validate-outputs`.
- `engine/templates.py` + `templates/{mode}/*.md` (modified) — adds slot markers to agent prompts.
- `engine/tests/test_schema_validator.py` (new) + `engine/tests/fixtures/schema/*.json` (new).
- `.github/workflows/schema-validate.yml` (new).
- `CONSUMER-CONTRACT.md` (new, repo root) — declares the JSON Schema as a stable surface; full content specification per § 7.1 (D11). Names the specific schema surfaces and states the stability guarantee for each, per XXVIII sub-clause 5 (CONSTITUTION.md L572-577).
- `CONFORMANCE.md` (modified, repo root, D9) — the Persistence-Contract row is updated to: (a) name the canonical schema directory `engine/schema/v1/`, (b) name the file-naming convention (`{output-type}.schema.json` + `envelope.schema.json` + `validator-error.schema.json`), (c) cite the `$id` URI base `https://build-fractal.org/conversus/schema/v1/`, (d) cross-reference `CONSUMER-CONTRACT.md`. This satisfies XXVIII sub-clause 1's "documented in the repo's CONFORMANCE.md" textual requirement (CONSTITUTION.md L505-510).
- `STATE-FILES.md` (modified, if extant) — updates the deliberation-output entries to reference the new JSON schema location.
- `CLAUDE.md` (modified, repo root, D10) — adds a "Persistence Contract" section that **explicitly links to `CONSUMER-CONTRACT.md`**. The link is mandatory per XXVIII sub-clause 1's textual requirement that the discoverable location be "linked from **BOTH** the repo's top-level `README.md` AND its `CLAUDE.md`" (CONSTITUTION.md L508-510, emphasis in the constitutional text via the "BOTH" qualifier).
- `README.md` (modified, repo root, D10) — adds the same "Persistence Contract" link to `CONSUMER-CONTRACT.md`. The README link and the CLAUDE.md link are both required; satisfying only one fails XXVIII sub-clause 1.

### 6.2 `Build-Fractal/orchestrator/` (formerly spec-kit-orc)

- `scripts/dispatch/adapters/tool/conversus.sh` (modified) — replaces the existing grep-of-markdown parser with a JSON parser. New parser invokes `jq -r '.body.ruling_lines[].verdict' {arbitration.json}` (or equivalent Python) to extract verdict lines. Markdown-format outputs are still consumed for backward compatibility during the migration window (§ 11); JSON is preferred when both are present.
- `scripts/dispatch/adapters/tool/conversus.adapter.md` (new or modified) — declares the adapter's dependency on the conversus-oss JSON Schema, names the version range it supports, and references conversus-oss's `CONSUMER-CONTRACT.md`. Mirrors Principle XXVIII C3 (consumer-side declaration).
- Adapter CI: orchestrator CI gains a "conversus-json-fixture" job that runs the adapter against a vendored copy of conversus-oss's fixture set; failure blocks merge in orchestrator.

### 6.3 `clariti-care/payer-index-mono/build-fractal/conversus/CONFORMANCE.md`

- Update the conversus-oss row to reflect that this spec is the active satisfaction track for Principle XXVIII. Status moves from "Remediation-Blocked" (current, per v4.1.0) to "Remediation-In-Progress" on spec ratification, and to "Compliant" on completion of § 11 step 6.

---

## 7. Cross-product implications

The orchestrator adapter is the load-bearing consumer-side surface. Today the adapter (`scripts/dispatch/adapters/tool/conversus.sh`) hardcodes three brittle paths and grep patterns against conversus-oss outputs. Principle XXVIII C3 mandates `CONSUMER-CONTRACT.md` on the producer side declaring stable surfaces consumed by cross-product code; this spec produces that file. The adapter's parsing approach migrates from `grep` over markdown headings to `jq` (or Python `json.load`) over conformant JSON — a substantially simpler and more reliable consumer-side implementation, which was one of the load-bearing reasons the originating arbitration converged on JSON over XML (no specialized tooling like `xmllint`; ubiquitous shell parsing via `jq`).

After ratification:
1. Conversus-oss `CONSUMER-CONTRACT.md` declares the JSON Schema as stable.
2. Orchestrator's adapter declares it consumes that schema (version range `>=1.0.0-rc.1,<2.0.0` initially).
3. Both products' CI verifies the contract — conversus-oss CI validates every emitted JSON; orchestrator CI validates that its adapter correctly parses a vendored fixture set.
4. A schema MAJOR bump in conversus-oss requires coordinated adapter update in the orchestrator, sequenced via the cross-repo CI pattern in `build-fractal/conversus/CLAUDE.md` ("Cross-repo work" section).

No other suite product currently consumes deliberation outputs structurally (conversus-enhanced consumes solver outputs, not deliberation outputs). If a future sibling adds a consumer, it inherits the same `CONSUMER-CONTRACT.md` pattern.

### 7.1 CONSUMER-CONTRACT.md six-section template (D11 + F3)

Per XXVIII sub-clause 5 (CONSTITUTION.md L572-577), the producer's `CONSUMER-CONTRACT.md` MUST explicitly name each declared stable surface AND state its stability guarantee. Bare existence of the document does not satisfy the sub-clause.

**F3 normative template.** The block below is the verbatim content engineers should copy into `conversus-oss/CONSUMER-CONTRACT.md`, filling in any product-specific placeholders (none for conversus-oss; the template is fully populated for this product). The six section headings (`## 1. Consumed Surface Declaration`, `## 2. Schema Version Pinning`, etc.) and the required language under each heading are normative — sub-clause 5 compliance is verified at PR-time by a CI grep check on section heading presence + required-language tokens.

````markdown
# Consumer Contract — conversus-oss

This document declares the stable surfaces conversus-oss exports for cross-product consumption under Tier 2 Principle XXVIII sub-clause 4. Cross-product consumers — including but not limited to the orchestrator adapter at `Build-Fractal/orchestrator/scripts/dispatch/adapters/tool/conversus.sh` — MUST consult this document before depending on any conversus-oss output surface. Surfaces NOT declared here are NOT stable and may change without notice.

## 1. Consumed Surface Declaration

The producer (conversus-oss) declares the following surfaces are consumable by cross-product code. Each surface has an explicit stability guarantee in § 2 below.

**Schema surfaces** (canonical, JSON Schema Draft 2020-12, anchored at `https://build-fractal.org/conversus/schema/v1/`):

- `engine/schema/v1/envelope.schema.json` — `$id=https://build-fractal.org/conversus/schema/v1/envelope.schema.json` — the common envelope wrapping every deliberation output.
- `engine/schema/v1/review.schema.json` — body schema for Phase 1 agent reviews.
- `engine/schema/v1/cross-review.schema.json` — body schema for Phase 2 cross-reviews.
- `engine/schema/v1/revision.schema.json` — body schema for Phase 3 agent position revisions.
- `engine/schema/v1/disputes.schema.json` — body schema for Phase 4 consolidated disputes.
- `engine/schema/v1/synthesis.schema.json` — body schema for Phase 5 synthesis.
- `engine/schema/v1/arbitration.schema.json` — body schema for Phase 6 arbitration.
- `engine/schema/v1/validator-error.schema.json` — body schema for validator error objects (used by both producer-side warning emission and consumer-side error parsing).

**File-naming surfaces** (display-text, declared stable per XXVIII sub-clause 5):

- Companion `.md` rendered file naming: `{output-type}.md` as siblings to `{output-type}.json` under `deliberations/{deliberation-id}/{phase-dir}/{agent}/`.
- `.validation-warnings.json` sidecar file naming: `{output-path}.validation-warnings.json` siblings to non-conformant JSON outputs (per § 5.1 D1 architecture in the v4.2.0 spec).

**Explicitly undeclared surfaces.** Heading text inside rendered `.md` companions, prose ordering inside body fields, and any grep-match on rendered Markdown are **NOT** declared stable. Consumers parsing rendered-MD heading text for semantic content are violating XXVIII sub-clause 4. The JSON envelope + body schemas above are the stable parse target.

## 2. Schema Version Pinning

The producer commits to the following stability guarantee for every schema surface listed in § 1:

> The set of REQUIRED fields, the `enum` values of constrained fields, the `pattern` regexes on string fields, and the field names of OPTIONAL fields are stable across PATCH and MINOR `schema_version` bumps. Removal of a REQUIRED field, removal of an enum value, narrowing of a `pattern`, or renaming of any field requires a MAJOR `schema_version` bump per the v4.2.0 spec § 4.8 SemVer rules and triggers cross-product consumer migration per XXVIII sub-clause 4.

Consumers MUST pin a `schema_version` range:
- **Initial pin (recommended):** `>=1.0.0-rc.1, <2.0.0` — accepts the release-candidate baseline and all future MINOR/PATCH refinements within MAJOR 1.
- **Tighter pin (optional):** `>=1.0.0-rc.1, <1.1.0` — opts out of MINOR additions; useful for consumers that want explicit migration review on any additive change.

The producer's `current_supported_versions` allowlist (enforced by `engine/schema_validator.py`) is, at this writing, `>=1.0.0-rc.1, <2.0.0`. Consumers SHOULD track this allowlist when pinning.

## 3. Stability Guarantee

The stability guarantee per surface category:

**Schema surfaces.** Per § 2 above: stable across PATCH and MINOR; MAJOR bump required for any breaking change (removal, narrowing, rename, addition of REQUIRED field, removal of enum value).

**File-naming surfaces.** Stable across PATCH and MINOR. File-naming convention renames (e.g., changing `.validation-warnings.json` sidecar suffix) require a MAJOR `schema_version` bump even though the file naming is technically out-of-band from the schema content; consumer impact is identical (broken consumer parsers).

**Deprecation policy.** When a MAJOR bump occurs, the previous MAJOR receives a **90-day support window** during which both versions are accepted by the producer's `current_supported_versions` allowlist. After the window the previous MAJOR is removed from the allowlist; subsequent outputs MUST conform to the new MAJOR. The producer publishes the MAJOR-bump PR + window-end date at least 90 days before window end; consumers MUST migrate within the window.

**Schema-advancement authority.** The `1.0.0-rc.1` → `1.0.0` promotion and all subsequent bumps are authorized by the conversus-oss maintainer set per the v4.2.0 spec § 4.8 (D7) criteria.

## 4. Consumer-Side Obligations

Cross-product consumers MUST:

- **(a)** Consume the declared JSON schema, not display text in rendered MD. Grep-on-Markdown consumers are XXVIII sub-clause 4 violations and will silently break on MINOR producer changes.
- **(b)** Pin a `schema_version` range explicitly in the consumer's own configuration (e.g., orchestrator adapter declares `>=1.0.0-rc.1, <2.0.0` in `scripts/dispatch/adapters/tool/conversus.adapter.md`).
- **(c)** Ship consumer-side fixtures in the consumer's own CI per XXVIII sub-clause 4 ("Producer-side fixtures alone do not satisfy this sub-clause"). The consumer's CI MUST run its parser against a vendored copy of the producer's fixture set at `engine/tests/fixtures/schema/`.
- **(d)** Coordinate migration on MAJOR `schema_version` bumps via the cross-repo sequencing pattern in `build-fractal/conversus/CLAUDE.md` ("Cross-repo work" section): producer MAJOR-bump PR lands first; consumer pins are updated in a follow-up PR within the 90-day deprecation window.
- **(e)** Read validator error objects (`validator-error.schema.json`) when surfacing producer-side warnings to end users; do not parse the `human_message` field as semantic content (it is undeclared display-text within the schema).

## 5. Producer-Side Enforcement

The producer's enforcement of every guarantee in §§ 2-3 is mechanically verified at PR-time by:

- **Fixture corpus:** `engine/tests/fixtures/schema/` — four worked examples (conformant + missing-required + wrong-type + enum-violation) per v4.2.0 spec § 5.3.
- **CI workflow:** `.github/workflows/schema-validate.yml` — four jobs (forward-validation, drift-detection-bidirectional, schema-version-bump-detection, fixture+renderer tests) per v4.2.0 spec § 5.4. Required status checks on `main`.
- **Performance budget validation:** one-time measurement campaign at `engine/tests/test_validator_performance.py` against representative large outputs from v4.1.0 deliberations per v4.2.0 spec § 5.1.1.

Consumers can verify producer-side enforcement is live by checking the green CI history on PRs touching `engine/schema/v1/` or `deliberations/**`.

## 6. Change Coordination

Schema-affecting changes follow this coordination flow:

- **PATCH / MINOR bumps.** Producer lands the change in a single PR. Consumers MAY ignore (their existing pin continues to satisfy the new version). Producer notifies consumers via PR description + `CONSUMER-CONTRACT.md` changelog entry.
- **MAJOR bumps.** Producer lands the schema change in PR-1 with the MAJOR bump and the 90-day window-end date announced in `CONSUMER-CONTRACT.md`. Consumers receive a notification (issue filed in each declared consumer repo) on PR-1 merge. Consumers update pins + parsers in their own PRs within 90 days, landing each consumer-side PR after its corresponding cross-product testing confirms the new MAJOR is parsed correctly. The producer's `current_supported_versions` allowlist accepts both MAJOR versions during the window; after window end, only the new MAJOR is accepted.
- **Schema retirement.** Same flow as MAJOR bump: 90-day window during which both versions are accepted.

For governance amendments that materially change § 1's surface list, the change follows the v4.2.0 spec's § 4.8 schema-advancement-authority decision pathway (conversus-oss maintainer set; PR audit trail; quantitative + qualitative criteria documented in the bump PR).

---

Pointer to the schema directory: `engine/schema/v1/`. Individual schema files are listed in § 1 above.

Pointer to the producer-side enforcement implementation: `engine/schema_validator.py`, `engine/persistence.py`, `.github/workflows/schema-validate.yml`.
````

The template above is normative for the `CONSUMER-CONTRACT.md` file produced by § 6.1. The file MUST contain all six numbered section headings (`## 1. Consumed Surface Declaration` through `## 6. Change Coordination`) with content matching the shape above. Sub-clause 5 compliance is verified at PR-time by a CI check that grep-confirms each section heading exists in the file (lightweight structural check); a second check grep-confirms the stability-guarantee paragraph in § 2 is present verbatim.

---

## 8. Inclusion Criteria (Principle XXVIII satisfaction check)

Per Principle XXVIII's three-prong test and spec 070 (Constitutional Inclusion Criteria):

- **Universal applicability within conversus-oss:** Every deliberation produces all six output types. Schema applies universally to conversus-oss deliberations without exception. The migration window (§ 11) is bounded and time-limited; no permanent carve-out.
- **Mechanical verifiability:** JSON Schema validation is the canonical mechanical-enforcement primitive (binary pass/fail, field-presence check, type check, value-constraint check) with a sub-100ms runtime budget (C2). Three worked-example fixtures (§ 5.3) demonstrate enforcement bite per Principle XXVIII C6.
- **Non-redundance with existing principles:** No existing principle mandates a deliberation output schema. The current markdown templates document expectations but do not enforce them (Bug B and Bug C are existence proofs of unenforced expectations).

---

## 9. Verification methodology

Run the standard four-stage methodology per spec 067, mirroring v4.1.0:

1. **Originating deliberation** (4 agents). Anchor: this spec's content + Principle XXVIII grounding. Agents: engineer, schema-design-expert, adapter-consumer, devils-advocate. Output: `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/`. **Status: COMPLETE; APPROVE-WITH-FIXES on Q1+Q2, TIER-3-CONFIRMED on Q3 (the originating "RECURSION-EXEMPTED" label is retired in v3 in favor of temporal-constraint scope language per D4); conditions C1-C10 applied to produce v2.**
2. **Self-consistency verification** (4 different agents). Focus: contradiction with existing engine architecture, mode-template constraints, plugin entry-point partition (free/paid boundary per spec 033). Output: `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-2026-05-13/`. **Status: COMPLETE (manual arbitration); PASS-WITH-CLARIFICATIONS on Q1+Q2; FAIL-CONTRADICTION on Q3 (v2 § 5.1 blocking-validation contradicted Tier 2 Principle V); D-conditions D1-D15 applied to produce this v3.** Self-consistency re-run against v3 follows.
3. **Self-consistency re-run** (4 different agents). Triggered by the FAIL-CONTRADICTION on Q3 in stage 2; scoped to confirming the D1 Principle V fix and the D2-D15 clarifications hold. Output: `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-rerun-2026-05-13/` (or equivalent dated subdirectory).
4. **Blind verification** (4 fresh agents, no prior context). Focus: pure-reading review of the spec without prior deliberation context.
5. **Ratification.** If combined disposition across all stages is PROCEED-TO-RATIFICATION, the spec promotes to `Build-Fractal/conversus-oss/CONSTITUTION.md` Component-tier principle.

Per v4.1.0 D-conditions D1 and D3: within each verification stage, Q1 constitutional coherence assessment MUST complete before Q2 evidence base adequacy analysis; ratification-blocking issues must be evaluated before enforcement-mechanism design issues.

### 9.1 Methodological recursion — temporal-constraint scope (D2, D4, D5)

**v3 reframing.** v2 invoked a "RECURSION-EXEMPTED" verdict on this question and cited Tier 1 Principle II as justification. The self-consistency arbitration identified two problems with that framing: (1) Principle II governs **interface stability for technical contracts** (dispatch tables, template variables, schema-versioned wire formats), not procedural-methodology accommodations for verification cycles — citing it here was doctrinally invalid (D2); and (2) the "exemption" framing structurally resembles the v4.1.0 override-with-rationale stretch rejected by v4.1.0 self-consistency, and risks creating a re-invocable precedent unless explicitly contained (D4 + D5). v3 strikes the Principle II citation and replaces "exemption" with **temporal-constraint scope** language, mirroring v4.1.0's temporal-vs-membership-universality precedent.

**The temporal-constraint framing.** v4.2.0 is the spec that **creates** the JSON schema infrastructure. Verification outputs for v4.2.0 are produced by the four-stage methodology *while v4.2.0 is being verified* — therefore they predate the existence of the schemas they would otherwise be required to conform to. This is a **bootstrap paradox** at the moment of standing up the schema infrastructure: the schemas come into existence only on ratification of this spec, so any verification output emitted *before* ratification cannot logically conform to a schema that does not yet exist. Asking v4.2.0's verification trail to use JSON is asking it to conform to a contract that comes into existence on the very ratification it is verifying.

This is logically equivalent to v4.1.0's temporal-vs-membership distinction: v4.1.0 ruled that a principle binds all products that exist at ratification time (membership universal) but does not retroactively bind products that did not exist at ratification time (temporal limitation). v4.2.0's case is the same structure, applied to artifacts rather than products: the schema binds all verification outputs produced *after* schema ratification, but does not retroactively bind outputs produced *before* schema ratification — because before-ratification outputs cannot conform to a schema that does not yet exist. The accommodation is therefore not "relief from a Tier 2 principle"; it is **scope clarification** — the schema's temporal scope precedes its existence by construction.

**Anti-precedent language (D5).** This temporal-constraint accommodation applies **only** to specs that ratify the schema infrastructure they would otherwise be required to use. Future amendments creating new validation infrastructure are NOT exempt from using existing validation infrastructure — they remain bound by Principle XXVIII and by the schemas this spec produces. The accommodation does not generalize to "amendments adjacent to schema infrastructure," "amendments touching validation pathways," or any other re-invocable framing. The one and only case the accommodation covers is the bootstrap paradox of a spec standing up its own schema substrate. Subsequent specs — including future MAJOR `schema_version` bumps, future schema additions for new output types, and future amendments that touch the validator implementation — MUST conform to whatever schema is in force at the time of their own verification. There is no recursion-exemption pattern; there is a one-time bootstrap scope clarification.

**Technical precondition for accommodation invocation (E2).** Layered on top of the categorical prohibitions above, the accommodation applies **only when both** of the following technical conditions are met at the moment verification begins:

(a) **No JSON Schema yet exists for the artifact stream in question.** "Exists" means a ratified `engine/schema/v{N}/*.schema.json` file is in force in `Build-Fractal/conversus-oss/main` at the time the originating deliberation emits its first artifact. Draft-but-unratified schema files do not satisfy "exists" for the purpose of the technical precondition (the bootstrap paradox is a property of the actual artifact stream, not a hypothetical).

(b) **Ratification of the spec invoking the accommodation is what stands up that schema.** The spec's own ratification event is what publishes the first ratified schema for the artifact stream. If the schema would exist independently of the spec, the precondition fails.

The conjunction mechanically excludes — by construction, not by interpretive judgment — the following cases:
- **v2/ (or later) schema versions.** A v1/ schema would already exist; condition (a) fails. MAJOR bumps to existing schemas are NOT bootstrap-paradox cases.
- **New output types added to an existing schema directory.** The schema directory already exists with at least one ratified output-type file; condition (a) fails for the directory even if the specific new output type has no prior schema.
- **Validator amendments.** The schema is not changing; condition (a) is moot, but condition (b) fails because ratification is not standing up new schema infrastructure.

Any spec failing either condition (a) or (b) does not satisfy the technical precondition for accommodation invocation and remains bound by the schema in force at verification time. The technical precondition is the primary gate; the categorical prohibitions above are the secondary gate; both must be satisfied for the accommodation to apply.

**Precedent-citation requirement (E4).** Any future constitutional amendment invoking temporal-constraint reasoning of the shape used in this spec MUST cite **BOTH boundary precedents** in its originating-deliberation anchor materials:
1. **This spec (v4.2.0)** — `specs/v4.2.0-structured-deliberation-outputs/spec.md` § 9.1 (bootstrap-paradox scope clarification) and § 9.2 (cross-tier weakening assessment).
2. **The v4.1.0 self-consistency arbitration** — commit `8f90e2d` — which established the temporal-vs-membership-universality precedent and rejected the uniformly-available override-with-rationale framing.

Citing both is required because they jointly define the **boundary** of the temporal-constraint pattern: v4.1.0 establishes the underlying logical-impossibility scope-clarification shape (membership-universal does not imply retroactive); v4.2.0 establishes that the shape is one-time-substrate-standup containable but does NOT generalize to schema-adjacent amendments. An amendment citing only one of the two precedents is invoking a partial reading of the pattern and MUST be rejected at originating stage.

The citation triggers a **mandatory constitutional-coherence review** at the originating stage: the originating deliberation MUST include an explicit analysis verifying (a) the proposed accommodation satisfies the E2 technical precondition above, (b) the proposed accommodation falls outside the categorical prohibitions (D5), and (c) the proposed accommodation does not extend the temporal-constraint pattern beyond the v4.1.0+v4.2.0 boundary precedents. Failure to perform this analysis in the originating anchor materials is a procedural defect that blocks ratification regardless of substantive merit. This makes precedent-stretching visible at the earliest stage rather than allowing it to accumulate through downstream deliberation rounds.

**Practical consequence.** The verification trail for v4.2.0 itself stays markdown — a fixed point in the migration. The first spec ratified after v4.2.0 implementation completion is bound to use JSON for its verification outputs (per § 11 Tier T1 from the ratification of v4.2.0 onward, parallel-format support is in place; specs ratified after T3 — 2026-10-01 — MUST emit JSON).

**Technical-operational sequencing (F1).** Operational capacity validation — staffing, CI runner budget, schema-maintainer workload, downstream consumer migration coordination — depends on the underlying technical specifications being clarified first. The dependency is unidirectional: clarified specs (template slot syntax, validator interface, CI implementation per F2's class signatures and workflow YAML) → operational capacity validation. The blind verification arbitration's planning-authority ruling (item 2, Q1) makes this explicit: technical specification gaps MUST be resolved before operational capacity validation can proceed. The hybrid approach permitted under that ruling applies ONLY to governance framework development (e.g., the schema-advancement-authority decision pathway in § 4.8, the consumer-coordination flow in § 7.1 step 6), which MAY proceed in parallel with technical specification work because the governance frameworks operate on a longer timescale than implementation. Core technical foundations — slot syntax, validator class signatures, CI workflow YAML, performance budget validation — are NOT eligible for parallel operational planning; they must be specified, implemented, and measured before capacity planning becomes meaningful.

### 9.2 Cross-tier weakening assessment (D3, E3)

Per Tier 2 Constitution L649-664 (cross-tier weakening prohibition operational definition), any component-tier amendment MUST be assessed against the three weakening criteria. This sub-section discharges that obligation for v4.2.0 via a **systematic verification matrix** (E3) — citation-backed per-criterion analysis replacing v3's conclusory prose. Each criterion is structured as four rows: criterion text (constitutional citation) → v4.2.0 specific behavior → verification (cited evidence in the spec or in ratified principles) → conclusion.

#### Criterion (i) — Implicit relief

| Row | Content |
|---|---|
| **Criterion text** | "The accommodation must not grant implicit relief from a Tier 2 principle without invoking the formal Relief pathway in `COMPLIANCE.md` Part VI." (`build-fractal/conversus/CONSTITUTION.md` L649-664) |
| **v4.2.0 specific behavior** | § 9.1's temporal-constraint scope clarification: Principle XXVIII applies to verification outputs produced *after* this spec's ratification, but does not bind outputs produced *before* ratification (because the schema does not yet exist at that time). |
| **Verification** | (a) The Relief pathway in `COMPLIANCE.md` Part VI is constructed for **ongoing structural inability** to satisfy a principle (e.g., a product that cannot satisfy a principle without a migration that takes longer than the remediation deadline). v4.2.0's situation is **one-time logical impossibility at substrate standup** — a strictly bounded property of a single ratification event, not an ongoing condition. (b) Structurally identical to **v4.1.0's ratified temporal-vs-membership distinction** (commit `8f90e2d`), which v4.1.0 self-consistency arbitration confirmed is not Relief — it is scope clarification because strict reading is logically impossible, not merely inconvenient. The same logical structure applies here: there is no v4.2.0-pre-ratification schema for pre-ratification outputs to conform to, by construction. (c) The E2 technical precondition (above) and the D5 categorical prohibitions jointly contain the accommodation to a single instance — no second invocation is structurally available without re-ratification through the standard pathway. |
| **Conclusion** | **Criterion (i) is NOT triggered.** Relief is for ongoing structural inability; v4.2.0's situation is one-time logical impossibility resolved at ratification. The accommodation is scope clarification, mirroring a precedent already ratified at v4.1.0. |

#### Criterion (ii) — Implementation-impact shift

| Row | Content |
|---|---|
| **Criterion text** | "The amendment must not introduce interpretation language that would cause existing implementations to no longer satisfy the upper-tier principle." (`build-fractal/conversus/CONSTITUTION.md` L649-664) |
| **v4.2.0 specific behavior** | § 5.1 specifies a non-blocking warning-based validator that writes the file unconditionally and emits warnings into the deliberation event stream + `.validation-warnings.json` sidecar. § 5.4 specifies PR-time CI gates. § 4.0 declares the schema location. § 6.1 declares README + CLAUDE.md + CONFORMANCE.md update obligations. § 7.1 specifies CONSUMER-CONTRACT.md content. |
| **Verification (systematic matrix against existing Principle V-compliant implementations)** | The Tier 2 principles potentially in scope are Principle V (Observable Deliberation, L76-78) and Principle XXVIII (Persistence Contract Discipline, L490-644). The existing Principle V-compliant implementations in conversus-oss as of `main` HEAD are: (1) `engine/persistence.py` deliberation event-stream writer (writes unconditionally; no validation gating); (2) `engine/phase6_arbiter.py` heading-check warning emitter (logs warnings on malformed Phase 6 output; does not abort write); (3) `engine/templates.py` template renderer (writes rendered output unconditionally regardless of variable-substitution warnings). For each: **(1) persistence.py** — v3 § 5.1's pseudocode preserves `path.write_bytes(content)` as the unconditional first call; validation runs after the write and produces a sidecar warning record, never raising. Principle V satisfaction is preserved by construction. **(2) phase6_arbiter.py** — v3 makes no change to phase-6 heading-check behavior; v3 layers an *additional* warning emitter (schema validator) onto the same architecture. Existing warning-based behavior is extended, not replaced. Principle V satisfaction is preserved. **(3) templates.py** — v3 § 11 modifies templates to add slot markers but does not change the renderer's unconditional-write contract. The renderer remains warning-only; v3 § 11.1's semantic-equivalence CI gate operates at PR-time, not at template-render-time. Principle V satisfaction is preserved. Adjacent principle audit: Principle XXVIII compliance is **strengthened** by v3 (schemas, mechanical CI enforcement, version-bump detection, bidirectional drift detection, fixture coverage, consumer-contract content specification, README+CLAUDE linking, CONFORMANCE.md location declaration are all introduced or tightened). No existing principle's compliance is degraded by any clause of v3 or v4. |
| **Conclusion** | **Criterion (ii) is NOT triggered.** Every existing Principle V-compliant implementation in conversus-oss continues to satisfy Principle V under v3's architecture; the D1 reversal of v2 was specifically *to* preserve this property after the v2 framing violated it. The matrix above is the citation-backed evidence the agents requested for E3. |

#### Criterion (iii) — Suite-specific adaptation bypass

| Row | Content |
|---|---|
| **Criterion text** | "The amendment must not add a 'suite-specific adaptation' clause that effectively bypasses an upper-tier MUST clause." (`build-fractal/conversus/CONSTITUTION.md` L649-664) |
| **v4.2.0 specific behavior** | The temporal-constraint scope clarification in § 9.1 (with E2 technical precondition + D5 categorical prohibitions + E4 precedent-citation requirement) applies only to conversus-oss's verification outputs for this spec. |
| **Verification** | (a) **Framing check.** § 9.1's accommodation is framed as **logical-impossibility scope clarification at substrate standup**, not as "suite-specific adaptation" of any Tier 2 MUST clause. The clause does not invoke conversus-oss specificity as the basis for relief; it invokes universal-logical-impossibility (no schema exists, so no MUST can apply to outputs predating its existence). The same accommodation would apply to any product standing up its own validation substrate — the property is logical, not suite-local. (b) **MUST-clause inventory.** The Tier 2 Principle XXVIII MUST clauses are: declared schema (sub-clause 1), mechanical CI enforcement (sub-clause 2), version-bump discipline (sub-clause 3), cross-product consumer contracts (sub-clause 4), and explicit stable-surface declaration in CONSUMER-CONTRACT.md (sub-clause 5). Each is **satisfied** by v3/v4 for the outputs in the schema's temporal scope: sub-clause 1 (§ 4.0 + § 6.1), sub-clause 2 (§ 5.4 with E1 authority citation), sub-clause 3 (§ 5.4 schema-version-bump detection job), sub-clause 4 (§ 7.1 + § 6.2), sub-clause 5 (§ 7.1 six-section content specification). No MUST clause is bypassed. (c) **Containment check.** E2 technical precondition + D5 categorical prohibitions + E4 precedent-citation requirement jointly form a three-layer containment that mechanically excludes future re-invocation under adjacent framings. |
| **Conclusion** | **Criterion (iii) is NOT triggered.** No MUST clause is bypassed for outputs in the schema's temporal scope. Outputs that predate the schema's existence are not "exempted from" the MUST — the MUST does not apply to them because its referent does not yet exist. The containment language ensures no future amendment can repurpose the accommodation as a suite-specific adaptation. |

#### Overall conclusion

v4's accommodation is **temporal-constraint scope clarification, not cross-tier weakening.** All three criteria are NOT triggered under the systematic verification matrix above. The accommodation does not invoke the formal Relief pathway because Relief is structurally for ongoing inability; v4.2.0's situation is one-time logical impossibility resolved at ratification. The accommodation is contained by the D5 categorical prohibitions, the E2 technical precondition, and the E4 precedent-citation requirement. The matrix replaces v3's conclusory prose with citation-backed evidence per the agents' unanimous P1 request in the self-consistency rerun.

### 9.3 Forward-promotion pathway (D8)

The originating arbitration ruled TIER-3-CONFIRMED on Q3 because the evidence base for deliberation-output structural discipline is currently limited to conversus-oss. If a future conversus-suite sibling (e.g., a hypothetical `conversus-investigations`) begins producing deliberation-like artifacts, the Tier-3 placement should be re-evaluated for potential promotion to Tier 2 (Suite).

**Promotion trigger.** Promotion is triggered when a second conversus-suite product begins producing deliberation outputs *and* either (a) the second product independently produces a `CONSUMER-CONTRACT.md`-referenced JSON Schema for its own deliberation outputs, or (b) the second product imports / vendors the conversus-oss schemas.

**Promotion pathway.** Per `build-fractal/conversus/GOVERNANCE.md` § Pathway Taxonomy, a Tier-3 → Tier-2 promotion is a **MINOR amendment** at Tier 2 if the principle's substance does not change (only its scope expands from one product to the suite), or a MAJOR amendment if the promotion would require text changes to the existing component-tier principle that materially affect its meaning. The promotion follows the standard four-stage methodology (originating → self-consistency → blind verification → ratification). The originating deliberation MUST include an explicit evidence-base review showing the second product's deliberation outputs satisfy the same structural discipline this spec defines.

**Until promotion is triggered**, the principle remains at component tier in `conversus-oss/CONSTITUTION.md`. The forward-promotion pathway is documented here for traceability; it is not invoked at v4.2.0 ratification.

---

## 10. Conditions ledger

The applied-conditions ledger for this spec (C1-C10 from originating, D1-D15 from self-consistency, E1-E4 from self-consistency rerun, F1-F4 from blind verification) is moved to **Appendix A: Deliberation Archaeology** § A.3 as part of F4's separation of normative core from ratification audit trail. v5 applies F1-F4 (this changelog header summarizes the application); all prior conditions remain applied with no reversals.

---

## 11. Implementation order

Updated per C3 (dependency-ordered template migration with one-mode pilot), C5 (tiered staging), and F1 (sequencing + dependency gates).

**F1 prerequisite gate.** The implementation order below is a **unidirectional dependency chain**, not a set of parallel tracks. In particular, **template slot syntax specification MUST be complete before validator error specification development begins.** The validator's core function is parsing agent prose with slot markers; it cannot specify error semantics for a slot syntax that does not yet exist. Concretely: the work in step 3a's pilot (cooperative-mode template migration with explicit slot delimiter conventions — `<<<STRENGTHS_BEGIN>>> ... <<<STRENGTHS_END>>>` form per § 5.1, plus escape rules for content containing the delimiter literally, plus parser semantics for malformed slot pairs) MUST land before step 2's validator error specification + § 4.9 error-code semantics are finalized. Parallel work on these two tracks risks divergent interpretations of the slot syntax contract and is prohibited.

The performance budget validation framework (§ 5.1.1) is also a prerequisite gate: it MUST run and PASS (or apply documented graceful degradation) before step 2 lands as merged.

1. **Verify spec** via the four-stage methodology (§ 9).
2. **Add schemas + validator + renderer** to conversus-oss. Land as one PR with the three worked-example fixtures and CI gate. **Prerequisite (F1):** template slot syntax specification (delimiters, escape rules, parser semantics for malformed slot pairs) MUST be complete before validator error specification is finalized in this PR. **Prerequisite (F2):** performance budget validation framework (§ 5.1.1) MUST have measured the validator against the v4.1.0 synthesis-corpus subset and the report MUST be green (or documented degradation MUST have been applied).
3. **Migrate mode templates** to slot-marker form in **dependency order** (C3):
   - **3a. One-mode pilot.** Pick the most-used mode (**cooperative**) and migrate it first. Verify the migration on real production deliberations (re-emit at least one full six-phase deliberation in cooperative mode; validate every emitted JSON; regenerate MD companion; diff against the markdown the original template would have produced — see § 11.1 C4 gate). Block subsequent migrations until the pilot is green.
   - **3b. Remaining modes in dependency order.** The output types form a dependency chain: review → cross-review → revision → disputes → synthesis → arbitration. Within each mode, migrate output types in that order — review first (no upstream dependencies), arbitration last (depends on all five upstream types). One PR per (mode, output-type) pair. Each PR is independently testable.
   - The dependency analysis: cross-review consumes review structure; revision consumes own-prior-review + cross-reviews; disputes consumes prior phases' positions; synthesis consumes all phase 1-4 outputs; arbitration consumes synthesis (and optionally raw phase 1-4). Migrating arbitration before synthesis would create a JSON-consumer / markdown-producer mismatch.
4. **Migrate orchestrator adapter** to JSON consumer. Coordinated with conversus-oss `CONSUMER-CONTRACT.md` declaration.
5. **Re-render v4.1.0 audit trail as JSON.** Validation milestone: take the existing 4 deliberations for v4.1.0 (~150 markdown files) and re-emit each as JSON using a one-time `engine/migrate_md_to_json.py` tool. Validate every emitted JSON against the schema. This both backfills the audit trail and proves the schema accommodates real production deliberation outputs.
6. **Update conversus-oss CONFORMANCE.md row to Compliant.** Closes the Principle XXVIII remediation track ahead of the 2026-12-01 universal deadline.
7. **Deprecate markdown-format mode templates.** Archive under `templates/_archived_pre_json/` on the deprecation date.

### Tiered rollout dates (C5)

| Tier | Status | Date | Description |
|---|---|---|---|
| T1 | Parallel-format support | spec ratification (target 2026-06-01) | Engine writes both JSON canonical + MD companion. Adapter reads both; prefers JSON when present. CI is non-blocking. |
| T2 | Advisory CI on structured format | 2026-08-01 | CI emits warnings on JSON schema violations but does not block merge. Lets producers detect issues without stop-the-line. |
| T3 | Blocking CI on structured format | 2026-10-01 | PR-required CI gate (§ 5.4) blocks merge on schema violations. All new deliberations must be JSON-conformant. Write-time validation remains warning-only per § 5.1 D1 (Principle V); merge-block is at PR-time only. Markdown-only paths get explicit deprecation warnings in CI logs. |
| T4 | Markdown deprecation | 2026-12-01 | Engine reads JSON only. Markdown-reading code paths removed. Aligns with Principle XXVIII universal remediation deadline. |

**Post-cliff-date ratification handling (D6).** If ratification of this spec occurs **after** 2026-12-01 (the universal cliff date), the staged rollout above is collapsed: T1, T2, and T3 are treated as **simultaneously in-effect at ratification**, and T4 (markdown deprecation, engine reads JSON only) is treated as in-effect at ratification. There is no extended grace period beyond the constitutional cliff date for late ratification; the universality of the 2026-12-01 deadline (per CONSTITUTION.md L594-602) does not yield to a slower ratification path on this spec specifically. Concretely, late-ratification operations: (a) the schema-validate CI workflow lands as PR-required-blocking from day 1; (b) the parallel-MD-companion behavior is implemented but the adapter (§ 6.2) consumes JSON only; (c) the markdown-reading code paths are removed in the same PR train that lands the schema infrastructure, not in a follow-on train. The semantic-equivalence CI gate (§ 11.1 C4) is reduced to its historical-snapshot use only — it verifies the renderer produces equivalent output for the historical markdown corpus, but is not used as a forward gate on new template migrations (because all migrations land simultaneously at ratification).

### 11.1 Backward-compatibility window + semantic equivalence CI gate (C4)

Between ratification and 2026-12-01:
- New deliberations: JSON canonical + MD companion (per § 5.2).
- Historical deliberations (pre-ratification): markdown stays as-is. Optional: re-render via step 5 above.
- Engine reads both formats during the window. The persistence layer prefers JSON when both are present.
- Orchestrator adapter supports both formats during the window (per § 6.2).
- After 2026-12-01: engine reads JSON only.

**Semantic equivalence CI gate (C4).** During the migration window, a CI job runs the following round-trip test on every PR that modifies templates:
1. Take a representative input prompt for the (mode, output-type) under migration.
2. Render via the **old markdown template** → emit markdown output. Call this `MD_OLD`.
3. Render via the **new JSON template** → emit JSON output. Validate JSON against schema. Render JSON to MD companion via `engine/render_md.py`. Call this `MD_NEW`.
4. Diff `MD_OLD` against `MD_NEW`. Allowed differences: whitespace, ordering of equivalent enum-projected fields, deterministic field-formatting (e.g., timestamps reformatted to ISO-8601).
5. **Forbidden differences (CI fail):** missing section, missing structured field, divergent enum value, dropped concern/dispute, different verdict.

If the semantic content of `MD_NEW` differs from `MD_OLD` in a forbidden way, the migration is breaking — fail the build. Concrete fixtures live at `engine/tests/fixtures/semantic_equivalence/{mode}/{output-type}/` and are exercised by `pytest engine/tests/test_semantic_equivalence.py`. This is per Principle XXVIII C6 (worked-example fixtures with mechanical enforcement bite).

The CI gate is removed at T4 (2026-12-01) when markdown templates are deprecated and the equivalence question becomes moot.

---

## 12. Open questions

All five originating-arbitration open questions (OQ1-OQ5) are RESOLVED. The resolution detail is moved to **Appendix A: Deliberation Archaeology** § A.4 as part of F4's separation of normative core from ratification audit trail. The OQ5 doctrinal core (verification trail for v4.2.0 itself stays markdown by temporal-constraint scope) is governed normatively by § 9.1.

---

## Appendix A: Deliberation Archaeology

This appendix preserves the full ratification audit trail for v4.2.0 — accumulated changelogs, per-stage condition tables, applied-conditions ledger, originating open questions, methodology-recursion meta-signal narrative, document status checklist, and the per-version fix ledger. Readers implementing the spec (§§ 1-8 + § 9 normative core + § 10 + § 11 normative core) do NOT need to read this appendix. Readers auditing the four-stage verification methodology, tracing how each condition mapped to spec section landings, or evaluating future temporal-constraint precedent invocations (per § 9.1 E4) read this appendix.

### A.1 Recursion-exempted retirement note

The originating arbitration (2026-05-13) ruled **TIER-3-CONFIRMED + RECURSION-EXEMPTED on Q3**. The substantive accommodation (verification trail for v4.2.0 itself stays markdown because the JSON schemas come into existence only at ratification) was preserved across v2→v3→v4→v5. The verdict label "RECURSION-EXEMPTED" was retired in v3 (per D4) in favor of **temporal-constraint scope** language, mirroring v4.1.0's temporal-vs-membership-universality precedent. The doctrinal substance is unchanged; only the framing was sharpened to avoid implying a re-invocable exemption pattern. The current normative governance lives in § 9.1 (with D5 categorical prohibitions, E2 technical precondition, and E4 precedent-citation requirement jointly forming a three-layer containment).

### A.2 Accumulated changelogs (v1 → v2 → v3 → v4)

#### A.2.1 Changelog: v3 → v4

The **self-consistency rerun arbitration** (2026-05-13, `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-rerun-2026-05-13/arbitration/resolution.md`) returned **PASS-WITH-CLARIFICATIONS on Q1, Q2, and Q3**. Combined disposition: **PROCEED TO BLIND VERIFICATION with E-conditions applied to produce spec v4**. E-conditions are clarifications, not contradictions — they preserve v3's structural decisions (D1 non-blocking validation, D2 Principle II strike, D4-D5 temporal-constraint reframing, D9-D15 XXVIII discharge surfaces) and tighten the surrounding text.

| E# | Summary | Lands in |
|---|---|---|
| E1 | **§ 5.4 authority citation.** Add explicit constitutional authority grounding for the PR-blocking CI gate: cite Tier 1 Principle II (Stable Interfaces) + Tier 2 Principle XXVIII sub-clause 2 (mechanical CI enforcement, PR-required). Closes the implicit-authority gap the principle-xxviii-fit-auditor and strict-reader independently flagged. | § 5.4 |
| E2 | **§ 9.1 D5 technical condition.** Layer a technical precondition on top of the existing categorical prohibitions: the accommodation applies only when (a) no JSON Schema yet exists for the artifact stream in question, AND (b) ratification of this spec is what stands up that schema. Mechanically excludes v2/ schema versions, new output types added to an existing schema, and validator amendments. | § 9.1 |
| E3 | **§ 9.2 systematic verification matrix.** Replace v3's conclusory prose with citation-backed per-criterion analysis (criterion text → v4.2.0 specific behavior → verification → conclusion). For criterion (ii), the verification enumerates existing Principle V-compliant implementations in conversus-oss (`engine/persistence.py`, `engine/phase6_arbiter.py`, `engine/templates.py`) and demonstrates each remains compliant under v3/v4 architecture. | § 9.2 |
| E4 | **§ 9.1 precedent-citation requirement.** Future temporal-constraint amendments MUST cite BOTH v4.2.0 (this spec) AND v4.1.0 self-consistency arbitration commit `8f90e2d` as boundary precedents. Citation triggers mandatory constitutional-coherence review at originating stage verifying the E2 technical precondition, the D5 categorical prohibitions, and non-extension beyond the boundary precedents. | § 9.1 |

E1-E4 are smaller-scope than D1-D15: most edits are 1-3 sentences, except E3 which is a matrix rewrite of § 9.2. No v3 structural decision is reopened by v4; in particular, the originating arbitration's TIER-3-CONFIRMED ruling on Q3 (Tier 3 placement) is preserved, the temporal-constraint accommodation is preserved (not eliminated), and the migration philosophy (tiered rollout) is preserved.

#### A.2.2 Changelog: v2 → v3

The **self-consistency arbitration** (2026-05-13, `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-2026-05-13/arbitration/resolution.md`) returned **PASS-WITH-CLARIFICATIONS** on Q1 and Q2 and **FAIL-CONTRADICTION on Q3**. The load-bearing finding was that v2 § 5.1's blocking-validation language ("the engine logs the error array to the deliberation event stream and aborts the phase (does not write the malformed file)") **directly contradicts ratified Tier 2 Principle V** (CONSTITUTION.md L76-78: "Output validation … emits warnings for malformed output but does NOT block file writes. Malformed output is better than no output"). All four self-consistency agents independently identified this. Per cross-tier weakening prohibition (CONSTITUTION.md L685), a component-tier amendment cannot grant relief from a Tier 2 principle.

v3 applies fifteen D-conditions to resolve the contradiction and close the Q1+Q2 clarifications:

| D# | Priority | Summary | Lands in |
|---|---|---|---|
| D1 | P1 (Q3-blocking) | **Rewrite § 5.1 as non-blocking, warning-based validation.** Engine writes the file unconditionally; on schema violation it logs the `ValidatorError` array and emits a prominent warning. CI gates block at PR-time; engine writes never block at write-time. | § 5.1, § 5.4 |
| D2 | P1 (Q3-blocking) | Strike the Principle II citation in § 9.1; replace with temporal-constraint rationale. | § 9.1 |
| D3 | P1 | New § 9.2 — explicit cross-tier weakening assessment against CONSTITUTION.md L649-664 criteria (i), (ii), (iii). | § 9.2 (new) |
| D4 | P1 | Replace "RECURSION-EXEMPTED" language with **temporal-constraint framing** ("v4.2.0 verification outputs predate JSON schema availability by construction") throughout § 9.1, § 12 OQ5, § 13. Mirrors v4.1.0's temporal-vs-membership-universality precedent. | § 9.1, § 12, § 13 |
| D5 | P1 | Add **anti-precedent language**: this temporal-constraint accommodation applies only to specs that ratify the schema infrastructure they would otherwise be required to use. Future schema-related amendments are NOT exempt from using existing validation infrastructure. | § 9.1, § 9.2 |
| D6 | P2 | Post-cliff-date ratification handling: if ratification occurs after 2026-12-01, T4 is treated as in-effect at ratification with T1-T3 collapsed. | § 11 |
| D7 | P2 | Schema-advancement-authority — who decides the `1.0.0-rc.1` → `1.0.0` bump after 30 days clean operation, and by what criteria. | § 4.8 |
| D8 | P2 | Forward-promotion pathway — one paragraph for the case where a future conversus-* sibling produces deliberation-like artifacts, referencing GOVERNANCE.md pattern-promotion. | § 9.3 (new) |
| D9 | P1 | Declare `engine/schema/v1/` location in `conversus-oss/CONFORMANCE.md` per XXVIII sub-clause 1 textual requirement (CONSTITUTION.md L505-510). | § 4.0 (new), § 6.1 |
| D10 | P1 | Add README.md and CLAUDE.md links to CONSUMER-CONTRACT.md per XXVIII sub-clause 1 (CONSTITUTION.md L508-510 — "BOTH"). | § 6.1 |
| D11 | P1 | Complete CONSUMER-CONTRACT.md content specification per XXVIII sub-clause 5 — explicitly name schema surfaces and state the stability guarantee. | § 7.1 (new) |
| D12 | P1 | Bidirectional drift-detection CI per XXVIII sub-clause 2 — any change to `engine/schema/v1/*.schema.json` triggers re-validation of all existing producer code outputs under the new schema. Warning-only at write-time (D1 consistency); mechanically detected at CI-time. | § 5.4 |
| D13 | P2 | Reframe § 5.1's <100ms language as **implementation discipline**, not constitutional mandate. | § 5.1 |
| D14 | P2 | Document fixture validation scope coverage per XXVIII sub-clause 2 — fixtures cover field presence, types, value constraints, enum violations (three fixture types minimum). | § 5.3 |
| D15 | P2 | Specify CI detection for schema-version-not-bumped-on-schema-edit per XXVIII sub-clause 3 ("silent format changes are a violation"). | § 5.4 |

**D1 is the load-bearing reversal.** v2's framing — "aborts the phase, does not write the malformed file" — is **inverted** in v3: validation is advisory, runs at write-time, emits warnings into the deliberation event stream, but the file is **always written**. Mechanical enforcement bite is preserved at the PR-required CI gate (per XXVIII sub-clause 2), which DOES block merge on validation failure. The constitutional pillar Principle V protects ("malformed output is better than no output") is preserved at the engine's write path.

**D4 + D5 are the load-bearing reframing.** v2's "RECURSION-EXEMPTED" verdict structurally resembled the v4.1.0 override-with-rationale stretch that v4.1.0 self-consistency rejected when applied uniformly. The self-consistency arbitration identified that this accommodation can be precedent-safe **only if reframed as temporal constraint** (mirroring v4.1.0's temporal-vs-membership distinction): v4.2.0 verification outputs cannot conform to a schema that does not yet exist (bootstrap paradox; the schemas are produced *by this very spec*). v3 reframes "exemption" → "temporal scope precedes existence," and the anti-precedent language (D5) explicitly contains the accommodation to this one-time bootstrap and bars future schema-related amendments from invoking the same shape.

#### A.2.3 Changelog: v1 → v2

The originating arbitration (2026-05-13) returned APPROVE-WITH-FIXES on Q1 and Q2 with conditions C1-C10, and TIER-3-CONFIRMED + RECURSION-EXEMPTED on Q3. v2 applies all ten conditions verbatim. The single most consequential change is **C1**: the canonical schema language and file format switch from XML + XSD to **JSON + JSON Schema**. All four originating agents converged independently on this.

| C# | Priority | Summary | Lands in |
|---|---|---|---|
| C1 | P1 | Canonical format flipped from XML+XSD → JSON + JSON Schema. Namespace becomes a JSON Schema `$id` URI. Validator architecture uses Python `jsonschema`. | § 4, § 5.1, § 7 |
| C2 | P1 | Validator runtime budget: **<100ms per output**. If a validator implementation exceeds this, the validator is the bug, not the schema. | § 5.1 |
| C3 | P1 | Dependency-ordered template migration with one-mode pilot (cooperative first). | § 11 |
| C4 | P1 | Semantic equivalence testing as CI gate — re-render structured output back to markdown and diff against the markdown the original template would have produced. | § 11.1 |
| C5 | P2 | Tiered/staged rollout: parallel-format support → advisory CI → blocking CI → markdown deprecation. | § 11, § 11.1 |
| C6 | P1 | Envelope identity-field expansion: `deliberation_stage`, `engine_version`, `source_commit`. | § 4.1 |
| C8 | P2 | SemVer bump qualification: MAJOR / MINOR / PATCH definitions with consumer-impact qualification. Adding REQUIRED fields is MAJOR. | § 4.8 |
| C9 | P2 | Validator error-object schema (`field_path`, `error_code`, `human_message`, `expected_type`, `actual_value`, `suggested_fix`). | § 4.9 (new), § 5.1 |
| C10 | P3 | Initial schema version is `1.0.0-rc.1`. Bump to `1.0.0` after one ratification cycle of clean operation. | § 4.8 |

(C7 is subsumed by C1 in the arbitration's own consolidation; the Q2-axis restatement is folded into § 4.)

### A.3 Applied-conditions ledger (originating C1-C10)

Quoting verbatim from `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md`:

- **C1 (P1)** — § 4 + § 5.1 — switch canonical format from XML+XSD to **JSON Schema**. Update all six body-schema definitions and the common envelope to JSON Schema syntax. Update § 3 non-goals to remove the "XSD strawman" framing. *Applied in v2: §§ 4, 5.1, 7 fully rewritten; § 3 strawman language removed.*
- **C2 (P1)** — § 5.1 — establish **<100ms per-output validation performance budget** for write-time validation with early performance testing to fix scope before commitment. *Applied in v2: § 5.1 "Performance budget (C2)" paragraph + § 5.4 CI gate enforces P99 < 100ms.*
- **C3 (P1)** — § 11 — specify **dependency-ordered template migration**: review → cross-review → revision → disputes → synthesis → arbitration, with one-mode pilot. *Applied in v2: § 11 steps 3a-3b.*
- **C4 (P1)** — § 11.1 — explicitly enumerate **semantic equivalence testing** as a CI gate during the migration window: structured-parsed verdicts must match grep-extracted verdicts on all historical arbitration outputs. *Applied in v2: § 11.1 "Semantic equivalence CI gate (C4)".*
- **C5 (P2)** — § 11 — adopt **tiered/staged implementation**: v1.0.0 basic structural validation by 2026-12-01, advanced features (cross-reference integrity, full constraint validation) in v1.1.0 after performance validation. *Applied in v2: § 11 tiered rollout table + § 5.1 advanced-validation deferral language.*
- **C6 (P1)** — § 4.1 envelope — add required fields `deliberation_stage`, `engine_version`, `source_commit`. *Applied in v2: § 4.1 envelope schema + example.*
- **C8 (P2)** — § 4.8 — refine SemVer bump policy with explicit consumer-impact qualification (field rename = MAJOR even if technically additive when consumer parses by name). *Applied in v2: § 4.8 expanded.*
- **C9 (P2)** — § 5.1 — specify validator error-object schema (`field_path`, `error_code`, `human_message`). *Applied in v2: § 4.9 (new sub-section) + § 5.1 reference.*
- **C10 (P3)** — § 4.8 — adopt **1.0.0-rc.1 versioning** strategy with bounded iteration period ending by constitutional deadline. *Applied in v2: § 4.8 initial-version language + § 2 goal 2.*

(C7 was consolidated into C1 by the arbitration; it does not appear as a separate ledger entry.)

### A.4 Resolved originating open questions

- **OQ1 — Tier placement.** **RESOLVED: TIER-3-CONFIRMED.** Re-evaluate at the first conversus-suite sibling that produces deliberation-like artifacts. *(Q3 ruling.)*
- **OQ2 — XSD vs JSON Schema vs Pydantic-XML for the validator.** **RESOLVED: JSON Schema.** Unanimous P1 convergence across all four agents. *(C1 + C7 in arbitration, applied in v2 § 4 + § 5.1.)*
- **OQ3 — Companion MD generation: XSLT vs Python renderer.** **RESOLVED: Python renderer.** No agent challenged the strawman. *(Q1 Per-axis finding 6.)*
- **OQ4 — Deprecation cliff date.** **RESOLVED: 2026-12-01.** Constitutional deadline non-negotiability unanimous. *(Q1 Per-axis finding 7.)*
- **OQ5 — Methodological recursion.** **RESOLVED: TEMPORAL-CONSTRAINT SCOPE** (v3, per self-consistency D4; sharpened with E2 technical precondition + E4 precedent-citation requirement in v4). Markdown verification trail stays for v4.2.0 itself because v4.2.0's verification outputs are produced before the JSON schemas it ratifies come into existence (bootstrap paradox); JSON mandatory for subsequent specs. Anti-precedent language (§ 9.1 D5) contains the accommodation to this one-time bootstrap and bars future re-invocation. The originating-stage "RECURSION-EXEMPTED" verdict label is retired; the substance (markdown stays for v4.2.0) is preserved under a doctrinally-correct framing. Normative governance: § 9.1.

### A.5 Methodology recursion + meta-signal footnote

Running this spec through the four-stage verification uses the methodology whose outputs it schematizes. Two meta-signals to watch for:

- **If the methodology can't sustain its own self-improvement at this stage** — e.g., if the originating deliberation hits Bug A (prompt overflow) or Bug C (trigger miss) while reviewing the very spec that fixes them — that is a strong signal the migration is overdue and should be sequenced ahead of further v4.x amendments. **Status:** Bug C *did* manifest in the originating arbitration (the Phase 5 synthesizer wrote "Remaining Disputes" rather than the engine's expected marker pair; the arbiter dispatch silently missed; manual arbitration was produced — see `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` "Process Note"). This is real-time confirmation that the spec's structural-detection thesis is correct.
- **If the blind verification surfaces "should this spec require JSON for ITS OWN verification outputs?"** as a load-bearing question, the answer is **temporal-constraint scope** per § 9.1 (D4): v4.2.0 verification outputs predate JSON schema availability by construction, so they cannot logically conform to a schema that does not yet exist. The verification trail for v4.2.0 itself stays markdown — a fixed point in the migration. Anti-precedent language (§ 9.1 D5) bars future re-invocation under "adjacent" framings. JSON is mandatory for specs ratified after v4.2.0 implementation completion.

**Status update at v5 (post-blind-verification).** The blind verification did surface implementation-clarification concerns (Q1 IMPLEMENTABLE-WITH-CLARIFICATIONS via F1-F3) and noted the doctrinal-archaeology accumulation as a presentation problem (Q3 HOLDS-AS-DOCTRINE via F4 separation). It did NOT reopen the temporal-constraint scope ruling; the OQ5-substance fixed point holds.

### A.6 Fix ledger

| Version | Date | Change | Source |
|---|---|---|---|
| v1 | 2026-05-12 | Initial draft. XSD strawman. | Author. |
| v2 | 2026-05-13 | Applied C1-C10 from originating arbitration. C1: format flipped XML+XSD → JSON + JSON Schema (all six body schemas + envelope rewritten in §§ 4.1-4.7; § 5.1 validator architecture rewritten around Python `jsonschema`; § 7 adapter parsing migrated grep/`xmllint` → `jq`/Python `json.load`). C2: <100ms validation budget (§ 5.1) with P99 CI assertion (§ 5.4). C3: dependency-ordered template migration with cooperative-mode pilot (§ 11 step 3). C4: semantic equivalence CI gate during migration window (§ 11.1). C5: four-tier rollout (§ 11). C6: three additional required envelope fields (§ 4.1). C8: SemVer bump qualification with consumer-impact rule (§ 4.8). C9: validator error-object schema (§ 4.9 new). C10: initial schema version `1.0.0-rc.1` (§ 4.8, § 2 goal 2). | `deliberations/v4.2.0-structured-deliberation-outputs-originating-2026-05-12/arbitration/resolution.md` |
| v3 | 2026-05-13 | Applied D1-D15 from self-consistency arbitration. **D1 (load-bearing reversal):** § 5.1 rewritten as non-blocking warning-based validation; engine writes the file unconditionally; PR-required CI gate (§ 5.4) carries the enforcement bite. Resolves Q3 FAIL-CONTRADICTION against Tier 2 Principle V ("does NOT block file writes"). **D2:** struck Principle II misattribution in § 9.1. **D3:** new § 9.2 cross-tier weakening assessment against CONSTITUTION.md L649-664 criteria (i)/(ii)/(iii); conclusion: scope clarification, not relief. **D4 + D5 (load-bearing reframing):** replaced "RECURSION-EXEMPTED" with temporal-constraint scope language throughout § 9.1, § 12 OQ5, § 13; mirrors v4.1.0's temporal-vs-membership-universality precedent; added anti-precedent containment language barring future re-invocation. **D6:** post-cliff-date ratification handling in § 11 (T1-T3 collapsed, T4 in-effect at ratification). **D7:** schema-advancement authority in § 4.8 (maintainer set + quantitative/qualitative criteria for 1.0.0-rc.1 → 1.0.0 promotion). **D8:** new § 9.3 forward-promotion pathway for Tier-3 → Tier-2 when a second sibling produces deliberation outputs. **D9:** schema-location declaration in CONFORMANCE.md (§ 4.0 new, § 6.1). **D10:** README + CLAUDE.md links to CONSUMER-CONTRACT.md (§ 6.1). **D11:** complete CONSUMER-CONTRACT.md content specification in § 7.1 (new) with six required sections. **D12:** bidirectional drift-detection CI job (§ 5.4). **D13:** <100ms reframed as implementation discipline, not constitutional mandate (§ 5.1). **D14:** fixture scope expanded to four types covering field presence, type checking, value constraints, baseline (§ 5.3). **D15:** schema-version-bump CI detection job (§ 5.4). | `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-2026-05-13/arbitration/resolution.md` |
| v4 | 2026-05-13 | Applied E1-E4 from self-consistency rerun arbitration (PASS-WITH-CLARIFICATIONS on Q1+Q2+Q3; combined disposition PROCEED-TO-BLIND-VERIFICATION). **E1:** § 5.4 gains explicit constitutional authority citation for the PR-blocking CI gate, grounding it in Tier 1 Principle II (Stable Interfaces) + Tier 2 Principle XXVIII sub-clause 2 (mechanical CI enforcement, PR-required). Closes the implicit-authority gap flagged by the principle-xxviii-fit-auditor and strict-reader. **E2:** § 9.1 D5 paragraph gains a technical precondition layered on top of the existing categorical prohibitions: the accommodation applies only when (a) no JSON Schema yet exists for the artifact stream in question AND (b) the spec's own ratification stands up that schema. Mechanically excludes v2/ (or later) schema versions, new output types added to an existing schema, and validator amendments. **E3:** § 9.2 rewritten as a systematic verification matrix (citation-backed per-criterion analysis: criterion text → v4.2.0 specific behavior → verification → conclusion). Criterion (ii)'s verification enumerates existing Principle V-compliant implementations (`engine/persistence.py`, `engine/phase6_arbiter.py`, `engine/templates.py`) and demonstrates each remains compliant under v3/v4 architecture. Replaces v3's conclusory prose with citation-backed evidence per the agents' unanimous P1 request. **E4:** § 9.1 gains a precedent-citation requirement — future temporal-constraint amendments MUST cite BOTH v4.2.0 (this spec) AND v4.1.0 self-consistency arbitration commit `8f90e2d` as boundary precedents; citation triggers mandatory constitutional-coherence review at originating stage. Makes precedent-stretching visible at the earliest stage. | `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-rerun-2026-05-13/arbitration/resolution.md` |
| v5 | 2026-05-13 | Applied F1-F4 from blind verification arbitration (Q1 IMPLEMENTABLE-WITH-CLARIFICATIONS; Q2 MODERATE-RISK-MANAGEABLE; Q3 HOLDS-AS-DOCTRINE; combined disposition PROCEED-TO-RATIFICATION). **F1 (sequencing + dependency gates):** § 11 implementation order now specifies template slot syntax completion as a prerequisite gate before validator error specification development begins (unidirectional dependency, not parallel tracks). § 9.1 gains a technical-operational sequencing paragraph: technical specification gaps must be resolved before operational capacity validation can proceed; hybrid only permitted for governance framework development. **F2 (concrete implementation specifications):** § 5.1 validator pseudocode replaced with concrete Python 3.12 + Pydantic v2 class signatures (`SchemaValidator`, `ValidationResult`, `ValidationWarning`) per Principle IX (explicit type annotations + Pydantic models). § 5.4 prose CI gate replaced with a complete GitHub Actions workflow YAML example (four normative jobs: validate-conformance, drift-detection-bidirectional, schema-version-bump-detection, fixture-and-renderer-tests). New § 5.1.1 performance budget validation framework requires warm-cache + cold-cache measurement against the v4.1.0 synthesis-corpus subset (representative outputs >100K char) before architectural lock-in of the <100ms target; graceful-degradation behavior documented for the failure mode. **F3 (CONSUMER-CONTRACT.md six-section template):** § 7.1 converted from descriptive content specification to a fully-fleshed normative template with each of the six section headings written verbatim (Consumed Surface Declaration / Schema Version Pinning / Stability Guarantee / Consumer-Side Obligations / Producer-Side Enforcement / Change Coordination), required language under each heading, and a worked example for conversus-oss declaring deliberation-output schemas. Engineers can copy-paste-adapt. **F4 (doctrinal archaeology separation):** new Appendix A: Deliberation Archaeology consolidates accumulated v1→v2, v2→v3, v3→v4 changelogs (§§ A.2.1-A.2.3), applied-conditions ledger (§ A.3), resolved originating open questions (§ A.4), methodology recursion meta-signal footnote (§ A.5), and fix ledger (§ A.6). §§ 9 + 11 normative cores (temporal-constraint rule + E2 technical precondition + D5 categorical prohibitions + E4 precedent-citation requirement; § 9.2 cross-tier weakening verification matrix; § 11 implementation order + tiered rollout dates) are retained in-line. | `deliberations/v4.2.0-structured-deliberation-outputs-blind-2026-05-13/arbitration/resolution.md` |

### A.7 Document status checklist

- [x] § 1 Motivation grounded in three concrete bugs with citations + real-time Bug C reproduction confirmation + four-stage methodology completion note.
- [x] § 2 Goals enumerated (6 goals, each tied to Principle XXVIII sub-clause).
- [x] § 3 Non-goals enumerated.
- [x] § 4 Schema specified with JSON Schema definitions for all six output types + envelope + validator-error object.
- [x] § 5 Implementation specified with engine file paths + CI workflow YAML (F2) + Python class signatures (F2) + performance budget validation framework (F2 § 5.1.1).
- [x] § 6 File edits per repo enumerated (conversus-oss + orchestrator + payer-index-mono).
- [x] § 7 Cross-product implications mapped (orchestrator adapter migration); § 7.1 six-section CONSUMER-CONTRACT.md template (F3) normative.
- [x] § 8 Inclusion criteria checked against Principle XXVIII three-prong test.
- [x] § 9 Verification methodology specified; all four stages COMPLETE (originating PASS via C1-C10 → v2; self-consistency FAIL-CONTRADICTION on Q3 → D1-D15 → v3; self-consistency rerun PASS-WITH-CLARIFICATIONS → E1-E4 → v4; blind verification IMPLEMENTABLE-WITH-CLARIFICATIONS + MODERATE-RISK-MANAGEABLE + HOLDS-AS-DOCTRINE → F1-F4 → v5).
- [x] § 9.1 Methodological recursion reframed as temporal-constraint scope (D2, D4, D5); E2 technical precondition + E4 precedent-citation requirement layered on D5; F1 technical-operational sequencing paragraph added.
- [x] § 9.2 Cross-tier weakening assessment (D3, E3) — systematic verification matrix; criteria (i)/(ii)/(iii) all NOT triggered with citation-backed evidence.
- [x] § 9.3 Forward-promotion pathway documented (D8).
- [x] § 10 Conditions ledger pointer to Appendix A § A.3 (F4 separation).
- [x] § 11 Implementation order with F1 prerequisite gate (template slot syntax before validator error specification) + dependency-ordered migration + tiered rollout + post-cliff handling (D6).
- [x] § 12 Open questions pointer to Appendix A § A.4 (F4 separation).
- [x] Appendix A consolidates all archaeology (changelogs, applied-conditions ledger, open questions, methodology meta-signal, fix ledger, document status checklist).

End of v5 spec. **PROCEED-TO-RATIFICATION.**
