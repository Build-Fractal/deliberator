# Slot Syntax Specification — v4.2.0 F1 Prerequisite Gate

**Status:** RATIFIED (F1 prerequisite gate per spec v4.2.0 § 11)
**Version:** 1.0.0
**Spec source:** `specs/v4.2.0-structured-deliberation-outputs/spec.md` § 5.1, § 11
**Ratification PR:** (this PR — feat/v4.2.0-impl-f1-template-slot-syntax)

This document defines the canonical slot-marker syntax that deliberator mode templates use to delimit structured fields within agent prose. It is the load-bearing contract between (a) the templates agents fill, (b) the parser that extracts structured fields from filled prose, and (c) the JSON Schema validator that asserts conformance.

Per spec v4.2.0 § 11 F1: this specification MUST be complete and ratified BEFORE validator error specification (§ 4.9 error-code semantics) or the validator class implementation lands. Parser semantics specified here are the source-of-truth referenced by the validator.

---

## 1. Grammar

### 1.1 Slot markers

A slot is delimited by a matched pair of markers in agent prose:

```
<<<{NAME}_BEGIN>>>
{slot content}
<<<{NAME}_END>>>
```

Where:

- The literal sequences `<<<` (three left angle brackets) and `>>>` (three right angle brackets) are the slot-marker boundary delimiters.
- `{NAME}` is the slot identifier: a token matching the regex `[A-Z][A-Z0-9_]*` (uppercase ASCII letter followed by zero or more uppercase letters, digits, or underscores).
- `{NAME}_BEGIN` and `{NAME}_END` are the opening and closing suffix conventions. The suffix `_BEGIN` / `_END` is fixed; only the `{NAME}` portion varies per slot.
- `{slot content}` is the body of the slot — arbitrary text between the BEGIN and END markers.

Slot markers MUST appear at the start of a line (preceded only by optional ASCII whitespace `[ \t]*`) and MUST be followed by an end-of-line. Inline slot markers (e.g., within a paragraph) are NOT recognized as slot boundaries; they pass through to the slot body unchanged.

### 1.2 Slot names

Slot names are case-sensitive and follow `SCREAMING_SNAKE_CASE`. Names defined by each output type's schema are enumerated in the schema's `slot_definitions` table; see § 4 of the parent spec for the per-output-type list.

Example slot names from the cooperative mode review template:

- `STRENGTHS`
- `CONCERNS`
- `RECOMMENDATIONS`
- `DISPUTES`
- `VERDICT`

### 1.3 Worked example

A review-phase output with three slots:

```markdown
The proposal scopes well to a 4-week implementation window.

<<<STRENGTHS_BEGIN>>>
- Clear interface boundary at the persistence layer.
- Three worked-example fixtures per output type satisfy XXVIII C6.
- Tier 3 placement matches the evidence base.
<<<STRENGTHS_END>>>

<<<CONCERNS_BEGIN>>>
- The 100ms validator budget is unmeasured against real synthesis outputs.
- Markdown deprecation cliff overlaps with deliberator v1.0.0-rc cycle.
<<<CONCERNS_END>>>

<<<VERDICT_BEGIN>>>
APPROVE-WITH-FIXES
<<<VERDICT_END>>>
```

The parser extracts three slots: `STRENGTHS` (list-typed, three items), `CONCERNS` (list-typed, two items), `VERDICT` (string-typed, one value). Text outside slots ("The proposal scopes well...") is preserved as the prose preamble but is NOT a structured field.

---

## 2. Escape rules

Agent prose may legitimately contain the literal sequence `<<<` (three left angle brackets) — for example, when quoting code, regex patterns, or examples that themselves contain slot-marker-shaped tokens. The parser MUST NOT misinterpret such literals as slot boundaries.

### 2.1 The parser is conservative

The parser recognizes a slot boundary ONLY if ALL of the following hold:

1. The line starts with optional ASCII whitespace `[ \t]*` followed by `<<<`.
2. The next characters match the regex `[A-Z][A-Z0-9_]*` (a valid slot name token).
3. The slot name is followed by exactly `_BEGIN>>>` or `_END>>>`.
4. The closing `>>>` is followed by end-of-line (`\n`) or end-of-input.

ANY deviation from this exact form means the line is NOT a slot boundary; the line passes through to the surrounding text unchanged. This conservative rule means agent prose containing `<<<some text>>>`, `<<<NOT_A_SLOT>>>` (no `_BEGIN`/`_END` suffix), or `<<<STRENGTHS_BEGIN>>> followed by text on the same line` is preserved as prose.

### 2.2 No explicit escape character needed

The conservative recognition rule (§ 2.1) makes an explicit escape character unnecessary in practice. Agents may quote slot markers literally inside fenced code blocks, indented text, or simply by writing them inline (rather than on their own line).

If an agent absolutely needs a slot-shaped sequence at line-start AND wants it treated as prose (not a slot boundary), the recommended approach is to prefix with a non-whitespace character that takes the line out of slot-boundary form. For example:

```markdown
Note: the marker `_<<<EXAMPLE_BEGIN>>>` shows the slot-syntax form.
```

The leading `Note: ` prevents slot-boundary recognition.

### 2.3 No backslash escape

An earlier draft proposed a `\<<<` escape sequence. It was rejected because:

1. The conservative recognition rule (§ 2.1) already prevents accidental misinterpretation.
2. Backslash escape would require parser-side unescape logic in the slot body, adding complexity.
3. Agents producing markdown rarely encounter this case; the inline workaround (§ 2.2) suffices.

The slot syntax has NO escape sequences. The parser passes slot body characters through verbatim.

---

## 3. Parser semantics for malformed slot pairs

The parser MUST emit a validation warning (per Principle V: warning, not error) for each malformed condition. The persistence layer writes the file unconditionally; warnings are surfaced via the validator's event stream and the sidecar `.validation-warnings.json`.

This section enumerates the malformed conditions, the parser's recovery behavior, and the warning emitted in each case.

### 3.1 Unmatched BEGIN (no closing END)

**Input:**

```markdown
<<<STRENGTHS_BEGIN>>>
- Item 1
- Item 2

<<<CONCERNS_BEGIN>>>
- Concern A
<<<CONCERNS_END>>>
```

**Parser behavior:** Treats `STRENGTHS` slot content as everything from `<<<STRENGTHS_BEGIN>>>` up to (but not including) the next slot's `<<<CONCERNS_BEGIN>>>` line, OR up to end-of-input if no subsequent slot exists. The `CONCERNS` slot is parsed normally.

**Warning emitted:** `slot.unmatched_begin` with `field_path = "STRENGTHS"`, `expected = "<<<STRENGTHS_END>>>"`, `actual = "no closing marker found before next slot or EOF"`.

**Rationale:** Recovery preserves the agent's intent (the slot was opened, content followed) while flagging the structural error. The downstream JSON envelope is still emitted with the recovered slot content.

### 3.2 Unmatched END (no preceding BEGIN)

**Input:**

```markdown
<<<STRENGTHS_BEGIN>>>
- Item 1
<<<STRENGTHS_END>>>
<<<CONCERNS_END>>>
```

**Parser behavior:** The orphan `<<<CONCERNS_END>>>` is ignored. It does NOT become slot content; it is dropped from the parsed output.

**Warning emitted:** `slot.unmatched_end` with `field_path = "CONCERNS"`, `expected = "preceding <<<CONCERNS_BEGIN>>>"`, `actual = "no matching opening marker found"`.

**Rationale:** Dropping the orphan end is the least-surprising recovery. Treating it as prose would let agents accidentally inject slot-shaped content into the JSON envelope through misuse.

### 3.3 Nested same-name slots

**Input:**

```markdown
<<<STRENGTHS_BEGIN>>>
- Outer item
<<<STRENGTHS_BEGIN>>>
- Inner item
<<<STRENGTHS_END>>>
<<<STRENGTHS_END>>>
```

**Parser behavior:** The inner `<<<STRENGTHS_BEGIN>>>` is treated as slot content of the outer `STRENGTHS` slot (per the conservative rule applied at the prose level — same-name nesting is structurally ambiguous, so the parser does NOT open a new slot). The first matching `<<<STRENGTHS_END>>>` closes the outer slot. The second `<<<STRENGTHS_END>>>` becomes an unmatched END (handled per § 3.2).

**Warning emitted (two warnings):**

1. `slot.nested_same_name` with `field_path = "STRENGTHS"`, `expected = "no same-name slot nesting"`, `actual = "inner <<<STRENGTHS_BEGIN>>> appeared inside open STRENGTHS slot"`.
2. `slot.unmatched_end` (per § 3.2) for the trailing orphan.

**Rationale:** Same-name nesting is unambiguously a template-authoring error. The parser does NOT try to disambiguate; it surfaces the warning and recovers conservatively.

### 3.4 Nested different-name slots

**Input:**

```markdown
<<<STRENGTHS_BEGIN>>>
- Item with embedded reference: see <<<CONCERNS_BEGIN>>> for related.
- Item 2
<<<STRENGTHS_END>>>
```

**Parser behavior:** The inline `<<<CONCERNS_BEGIN>>>` inside the `STRENGTHS` slot body is NOT a slot boundary because it does not start a line (per § 2.1 rule 1). It passes through as slot content. The `STRENGTHS` slot is parsed normally with the inline text preserved.

**Warning emitted:** None. This is well-formed input.

**Note:** True line-start nesting (a `<<<CONCERNS_BEGIN>>>` line inside an open `STRENGTHS` slot) is NOT recognized as nesting. The conservative rule applies: only ONE slot is open at any line; if a different-name BEGIN appears at line-start while a slot is open, the parser treats it as opening a SIBLING slot, implicitly closing the prior open slot at the prior line (which then emits an `slot.unmatched_begin` warning per § 3.1).

The slot syntax DOES NOT support true nested structured slots. Use multiple sibling slots instead.

### 3.5 Empty slot content

**Input:**

```markdown
<<<VERDICT_BEGIN>>>
<<<VERDICT_END>>>
```

**Parser behavior:** The `VERDICT` slot is parsed with empty content (empty string after whitespace stripping).

**Warning emitted:** None at the parser level. The downstream JSON Schema validator MAY emit a warning if the schema requires non-empty content (per the `minLength` constraint on the corresponding field).

**Rationale:** Empty content is a valid parse result; whether it satisfies the schema's content constraints is a schema-level decision, not a parser-level one.

### 3.6 Unknown slot name (not in schema)

**Input:**

```markdown
<<<FOO_BEGIN>>>
arbitrary content
<<<FOO_END>>>
```

When the parser is invoked with a schema that does NOT declare the `FOO` slot:

**Parser behavior:** The `FOO` slot is parsed structurally (a well-formed BEGIN/END pair), but its content is NOT mapped to any field in the JSON envelope. The slot is dropped from the envelope output.

**Warning emitted:** `slot.unknown_name` with `field_path = "FOO"`, `expected = "<one of: {schema's declared slot names}>"`, `actual = "FOO not declared in schema"`.

**Rationale:** Templates evolve; agents may produce slots that the current schema doesn't know about. Treating this as a warning (not a fatal error) preserves forward-compatibility — a future schema version can declare the new slot without breaking older parsers.

### 3.7 Whitespace handling

The parser strips leading and trailing ASCII whitespace (spaces, tabs, newlines) from slot content during extraction. Interior whitespace (between non-whitespace characters within slot content) is preserved.

For list-typed slots (per the schema's `type: list` declaration), the parser additionally:

- Splits content on newline boundaries.
- Strips each line.
- Recognizes markdown list bullets (`- `, `* `, `+ `) at line-start; the bullet character is stripped during extraction.
- Drops empty lines.

The result is a list of strings, each string being the content of one list item.

For string-typed slots (per the schema's `type: string` declaration), the parser returns the whitespace-stripped slot content as a single string.

### 3.8 Determinism

The parser is deterministic: given identical input bytes and identical schema, the parser MUST produce identical parse output AND identical warning list (in identical order) every time. Warning order is the order of first occurrence in the input stream.

---

## 4. Validator integration

This § 4 is a forward reference to the validator implementation (F2 step). Including it here so the F1 spec's downstream contract is explicit.

The validator at `engine/schema_validator.py` (to be created in the F2 PR) imports a slot-parser module that implements this specification. The slot parser exposes:

```python
def parse_slots(content: str, schema: SchemaDefinition) -> ParseResult:
    """
    Parse agent prose into a slot dictionary + warnings list.

    Args:
        content: Raw agent prose (UTF-8 string).
        schema: The output type's schema, declaring valid slot names + types.

    Returns:
        ParseResult(slots: dict[str, Any], warnings: list[ValidationWarning])
        where slots maps slot name → extracted value (str or list[str] per type).
    """
```

The validator then maps `ParseResult.slots` into the JSON envelope per the schema's field mapping, validates the envelope against the JSON Schema (`engine/schema/v1/{output-type}.schema.json`), and emits any schema-level validation warnings.

Per Principle V: the validator NEVER blocks file writes. The persistence layer writes `path.write_bytes(content)` UNCONDITIONALLY before invoking the validator. Warnings are emitted to the event stream and the sidecar `.validation-warnings.json`.

---

## 5. Migration from existing markdown markers

The existing markdown templates use `DELIBERATOR:DISPUTES_BEGIN` / `DELIBERATOR:DISPUTES_END` markers (see `linter/validate.py`). Those markers are part of the pre-v4.2.0 markdown-only flow.

The new slot syntax `<<<NAME_BEGIN>>> ... <<<NAME_END>>>` (this spec) is for the v4.2.0 JSON envelope migration. The two conventions coexist during the parallel-format window (T1 through T3 per § 11 tiered rollout) and the markdown convention is deprecated at T4 (2026-12-01 cliff date).

Templates migrated to the new slot syntax MAY also retain the old `DELIBERATOR:DISPUTES_*` markers during the transition. The slot-parser ignores old-format markers (they're prose under the conservative recognition rule § 2.1). The legacy markdown linter at `linter/validate.py` continues to check old-format markers until T4.

---

## 6. Acceptance criteria for F1 ratification

This F1 prerequisite gate is **complete** (per spec v4.2.0 § 11) when ALL of the following hold:

- [x] Slot delimiter convention defined (§ 1.1, § 1.2).
- [x] Grammar formalized with regex + line-anchored boundaries (§ 1.1, § 1.2, § 2.1).
- [x] Escape rules documented (§ 2.1 conservative recognition rule + § 2.2 inline workaround).
- [x] Parser semantics for malformed slot pairs enumerated (§§ 3.1-3.6).
- [x] Whitespace handling specified (§ 3.7).
- [x] Determinism guaranteed (§ 3.8).
- [x] Worked example demonstrating the syntax end-to-end (§ 1.3).
- [x] Forward reference to validator integration (§ 4).
- [x] Migration path from existing markers documented (§ 5).

Per spec v4.2.0 § 11 F1: with this file merged, the F2 work (validator class signatures in § 5.1, CI workflow in § 5.4, performance budget validation in § 5.1.1) is unblocked.

---

## 7. Open questions deferred to F2

The following details are **out of scope** for F1 and will be specified when F2 lands:

- Error-code semantics for validation warnings (per parent spec § 4.9). F1 specifies warning *categories* (`slot.unmatched_begin`, `slot.unmatched_end`, `slot.nested_same_name`, `slot.unknown_name`); F2 will specify the structured `ValidationWarning` Pydantic model (per parent spec § 5.1 F2 class signatures) and the canonical error-code enum.
- Performance characteristics of the slot parser (e.g., maximum slot count per document, recursive parser cost). Per parent spec § 5.1.1, F2 includes a performance budget validation framework that measures actual parse latency against the v4.1.0 synthesis-corpus subset. The slot parser is invoked once per persisted output; its budget contribution is bounded by document size.
- Internationalization: slot names are uppercase ASCII (per § 1.2). Slot content is UTF-8 with no further restriction. Agent prose containing right-to-left text, combining characters, or surrogate pairs is preserved verbatim.

These deferrals are intentional. F1 establishes the contract; F2 implements it. Premature F2 work would violate the F1 prerequisite gate per parent spec § 11.
