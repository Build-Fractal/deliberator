# Consumer Advocate — Remaining Disputes

**Date**: 2026-04-16
**Phase**: 4 — Disputes
**Basis**: Revised positions from all three reviewers

---

## Dispute 1: Mock provider fix strategy — realistic response mode vs. fixture test

**My position**: The mock provider needs a "realistic response mode" that returns well-structured markdown per phase and mode (my revision section 3.1, adopting the test-architect's original finding).

**Test-architect's revised position**: Withdraw the mock provider rewrite. Instead, add a single targeted smoke test that calls `parse_synthesis()` directly with a known-good markdown fixture. The mock provider stays cheap and deterministic. (Their "What I Withdraw" section 1.)

**Engine-implementor's revised position**: Either enhance the mock provider to return synthesis-parseable output, or acknowledge the smoke tier tests the fallback path and add a "realistic mock" mode. The former is preferable. (Their M-2, R14.)

**Why I dispute the test-architect's position**: The test-architect's fixture test solves the wrong problem. It verifies that `parse_synthesis()` works when given correct input. That was never in question. The problem is that every smoke test using mock provider exercises the bare-except fallback path, meaning the entire smoke tier cannot detect regressions in the production parse path as integrated through the actual pipeline. A fixture test of the parser in isolation does not close that gap. If someone changes how `StructuredDeliberation.from_events()` invokes parsing, or how event accumulation feeds into synthesis, the fixture test passes while the smoke tier remains blind.

The engine-implementor agrees with me on this point. The test-architect's withdrawal is premature. The mock provider realistic mode does not need to be a "test infrastructure project" -- it needs to return output with the correct markdown heading structure (`## Headline`, `## Summary`, etc.) so that the normal parse path succeeds. This is a template change in the mock provider, not a new subsystem.

**Resolution I seek**: The spec should require the mock provider to return synthesis-parseable markdown (the engine-implementor's R14), not replace it with a fixture test. The fixture test can exist as a supplemental unit test, but it cannot substitute for end-to-end smoke coverage of the production parse path.

---

## Dispute 2: Desktop Extension content scanner testing scope

**My position**: All 7 MCP prompts must be tested against content scanner patterns. This is P1 because if a prompt format change breaks the role-split workaround, Desktop users see failures with no engine-level explanation. (My revision section 2.5.)

**Engine-implementor's revised position**: "Valid concern, but this is a Desktop Extension integration test, not an engine eval test. The role-split workaround in `design_deliberation()` and `analyze_documents()` is engine code, but the content scanner is a Claude Desktop platform constraint. I acknowledge this exists but maintain it belongs in Desktop Extension CI, not Spec 061." (Their M-7, item 1.)

**Test-architect's revised position**: Silent on this in their revision -- they endorsed my finding in their original cross-review but did not include it in their revised priority table.

**Why I dispute the engine-implementor's position**: The role-split workaround is in `mcp_server.py`, which is engine code tested by the eval suite. The workaround exists because the prompt format directly determines whether the MCP server works in its primary consumer environment. Calling this a "Desktop platform constraint" is technically accurate but practically misleading -- the constraint is enforced on engine-authored prompts. If the engine changes a prompt's structure and breaks the role-split pattern, the Desktop Extension CI would need to replicate the full MCP server invocation to catch it. That is exactly what the engine eval suite already does.

The boundary argument would hold if the content scanner were an external system the engine cannot influence. But the engine controls the prompt text. The scanner rules are known. Testing that engine-authored prompts satisfy known constraints of the primary consumer is a legitimate engine eval concern.

**Resolution I seek**: Include at minimum a smoke-level test that the 7 MCP prompts do not contain patterns known to trigger the content scanner (specifically: instructional directives in the user role without the role-split pattern). This can be a static lint rather than a runtime test, but it must live in the engine eval suite because the prompts are engine code.

---

## Dispute 3: `conversus status` — remove or specify

**My position**: If `conversus status` does not exist, remove it from the test list. If it should exist, specify it. (Referenced in my cross-review, adopted by the engine-implementor in M-5.)

**Engine-implementor's revised position**: Agrees fully -- "the spec cannot list tests for a command that may not exist and mark it 'verify.'" Upgraded to a must-fix spec correctness issue. (Their M-5, R-CLI.)

**Test-architect's revised position**: Silent in their revision. Their original cross-review noted it as DC-2 but said only that the engine-implementor "underweighted" it. Their revised priority table does not include `conversus status` at all.

**Why this remains a dispute**: There is no disagreement on the principle, but the test-architect's omission from their priority list concerns me. If the spec author reads the test-architect's revision as the implementation guide, `conversus status` will fall through the cracks. It is listed in the spec's section 3.1.3 as a test target. If it is not a real command, the spec has a factual error that must be corrected before implementation begins.

**Resolution I seek**: All three reviewers should explicitly flag `conversus status` in section 3.1.3 as requiring resolution. The engine-implementor and I agree. The test-architect should confirm.

---

## Dispute 4: Persistence round-trip test priority

**My position**: P1 -- `persist_deliberation()` and `list_deliberations()` are shipping engine code called by handlers today. Testing the round-trip is not a future concern. (My revision section 4.1, item 2; original review section 4.1, item 3.)

**Test-architect's revised position**: Demoted to P3. Persistence internals withdrawn from eval scope. The round-trip test "remains valid as an integration test ... but it is P3, not P2." (Their "What I Withdraw" section 3; revised table, bottom.)

**Engine-implementor's revised position**: Silent on persistence priority in their revision. They reference R8 (intermediate artifact access via `run_pipeline`) but do not assign priority to a persistence round-trip test.

**Why I dispute the test-architect's P3**: The test-architect withdrew persistence *internals* (disabled-via-settings, old-deliberation-cleanup) from eval scope, which I agree with. But they swept the round-trip test into the same demotion. These are different things. The round-trip -- persist a deliberation, list it, show it -- is externally observable behavior exposed through the CLI (`conversus show`, `conversus list`) and the MCP handler (`list_deliberations`). It is not a unit test of file I/O; it is a consumer-facing feature test.

The paid tier will build on this persistence layer for team deliberation history. If the round-trip is broken and no test catches it until P3 implementation, the paid tier team will discover it as a blocker during integration. Testing it at P1 is cheap insurance.

**Resolution I seek**: Separate the round-trip integration test from the persistence internals. The internals are correctly P3 or out of scope. The round-trip is P1 because it tests externally observable commands that consumers use today.

---

## Dispute 5: MCP tool count as a smoke test

**My position (revised)**: I withdrew the Cursor 40-tool limit assertion from the eval suite in my revision (section 1.3), accepting the test-architect's reframing as a static documentation concern.

**Test-architect's revised position**: Accepted the MCP tool count assertion at P2 as a consumer-facing constraint the eval suite should enforce. (Their "Items I Did Not Originally Address", from consumer-advocate, item 3.)

**Why this is now a dispute in the opposite direction**: After my withdrawal, the test-architect adopted my original position and placed it at P2. I withdrew because the test-architect's cross-review argued it was a static documentation concern about the user's total MCP portfolio, not a behavioral test. Now the test-architect's revision includes it. Either it is in scope or it is not.

On reflection, the test-architect's P2 placement is reasonable. Conversus currently exposes 4 tools, which is well under the 40-tool limit, so the test is trivially passing. But the tool count could grow. A static assertion that `len(mcp_tools) <= N` is a one-line test that prevents accidental tool proliferation. I reverse my withdrawal and accept the test-architect's P2.

**Resolution I seek**: This is not a true dispute -- I am signaling that I re-adopt the test-architect's P2 position after initially withdrawing. The synthesis should include MCP tool count at P2.

---

## Dispute 6: Red-blue smoke test path -- adhoc vs. pre-built YAML

**Engine-implementor's revised position (R1)**: "Red-blue tests must use pre-built YAML configs, not the adhoc decide path." Listed as must-fix, unchanged from original. (Their revised table, R1.)

**Test-architect's revised position**: The red-blue smoke test should use the adhoc path (`build_adhoc_config -> parse_config -> run_engine`), not pre-built YAML. This serves as both the mode test and the G1 regression test. Using pre-built YAML bypasses `build_adhoc_config` and leaves the G1 regression path untested. The engine-implementor's R1 and their G1 position are in tension. (Test-architect "What I Modify" section 4.)

**My position**: The test-architect is correct on this one. The G1 bug is specifically in the adhoc path (`build_adhoc_config` generates invalid red-blue config). If the smoke test uses pre-built YAML, it tests that the engine can run red-blue but not that the adhoc interface can generate valid red-blue config. Since `conversus decide "Q" --mode red-blue` is how Desktop and Claude Code users invoke red-blue (they do not write YAML configs), the adhoc path is the consumer-relevant path.

Both paths need testing, but the primary smoke test for red-blue should use adhoc. A supplementary test can use pre-built YAML to verify the engine handles red-blue config correctly independent of the adhoc builder.

**Resolution I seek**: The spec should test red-blue through the adhoc path as the primary smoke test (after G1 is fixed), with an xfail marker before the fix. A separate test can use pre-built YAML for engine-level red-blue validation. The engine-implementor's R1 should be modified to say "add a pre-built YAML red-blue test in addition to the adhoc path test," not "use pre-built YAML instead of adhoc."

---

## Dispute 7: SDK surface priority -- P0 vs. P1

**My revised position**: P1, downgraded from my original P0 per the test-architect's reasoning. (My revision section 1.6.)

**Test-architect's revised position**: P1, upgraded from their original P2. (Their "What I Modify" section 1.)

**Engine-implementor's revised position**: Must fix (R13), which in their table sits alongside other P1 items. (Their M-1, R13.)

**Status**: This is now resolved. All three reviewers converge on P1. I include it here only to confirm the dispute from my original review (P0) is closed. No further action needed.

---

## Items with no remaining dispute

The following items from my revision have full three-way agreement. I list them to confirm they are settled:

- **Settings cascade env var layer at P0**: All three agree.
- **`quality_indicators` schema fix**: All three agree it is a must-fix.
- **First eval run excludes red-blue**: All three agree (with xfail addition from the test-architect).
- **SKILL.md parity moves to step 4-5**: All three agree.
- **CI/CD governance exit codes at P1**: Both I and the engine-implementor agree (R17). Test-architect accepts from me at P1.
- **JSON error output consistency**: All three agree.
- **Multi-round pipeline tests at P0**: Test-architect and engine-implementor agree. I accepted this in my revision.
- **Promptfoo shell quoting (wrapper + test)**: All three agree.
- **Quality threshold calibration from baselines**: All three agree on my methodology.
- **G11 dual provider resolution path**: All three agree.
- **Pydantic schema snapshot testing at P1**: All three agree.

---

## Summary

I have 5 active disputes (1, 2, 4, 6 are substantive; 3 is about ensuring the test-architect explicitly addresses `conversus status`), 1 self-correction (5, where I re-adopt the test-architect's position), and 1 closed dispute (7, resolved by convergence).

The most consequential dispute is #1 (mock provider strategy). The test-architect and I are on opposite sides, with the engine-implementor siding with me. If the fixture-test approach prevails, the smoke tier will test the parser in isolation but not the production integration path through `from_events()`. This is the single largest remaining disagreement across all three reviews.

The second most consequential is #6 (red-blue adhoc vs. YAML). The test-architect and I are aligned against the engine-implementor's R1. The consumer perspective is clear: users invoke red-blue through `conversus decide`, not through hand-authored YAML. The primary test must exercise the path users take.
