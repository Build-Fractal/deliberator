# Test Architect -- Remaining Disputes

**Phase**: 4 -- Disputes
**Date**: 2026-04-16
**Input**: All three revised positions (test-architect, engine-implementor, consumer-advocate)

---

## Dispute 1: Mock provider fix approach -- realistic response mode vs parse_synthesis fixture test

**My revised position**: Replace mock provider modification with a targeted `parse_synthesis()` fixture test using a known-good markdown string. I withdrew my original "realistic response mode" recommendation in favor of the consumer-advocate's lighter alternative.

**Engine-implementor's revised position (R14)**: "The mock provider must return output that exercises the production synthesis parsing path, not the bare-except fallback. Either enhance mock provider or add a 'realistic mock' mode. Priority: P0."

**The disagreement**: I explicitly withdrew the mock provider rewrite in my revision (section "What I Withdraw", item 1), accepting the consumer-advocate's argument that it "entangles mock provider behavior with synthesis format expectations and blurs the clean separation between the structural smoke tier and the semantic quality tier." The engine-implementor's R14 goes in the opposite direction -- they adopted my *original* position after I abandoned it.

The consumer-advocate's revised position aligns with mine: they list "Fix mock provider to return parseable synthesis" as their P0 item 1, but their section 3.1 also says they accept the fixture-test approach ("the fix: the mock provider needs a realistic response mode"). This is internally inconsistent in the consumer-advocate's revision -- they cite the approach I withdrew while also accepting the fixture test I endorsed.

**Why I hold my revised position**: The fixture test solves the actual problem (synthesis parser regressions are invisible) without the cost of maintaining a second mock mode that must track every change to the prompt templates and synthesis format. A realistic mock mode creates a coupling between mock provider output and synthesis parser expectations. When the synthesis format evolves, the mock must be updated in lockstep -- this is the same maintenance burden that SKILL.md divergence creates, and all three reviewers agree SKILL.md divergence is a problem. We should not recreate the same pattern.

The engine-implementor's concern -- that the smoke tier tests the fallback path -- is valid, but the fixture test addresses it directly: the parser has its own dedicated regression test, and the smoke tier's job is to verify structural pipeline completion, not parser correctness. These are separate concerns and should be tested separately.

**Resolution needed**: The spec author must decide: (a) add a `parse_synthesis()` fixture test and accept that smoke-tier mock runs exercise the fallback path, or (b) enhance the mock provider with a realistic mode that exercises the production path in every smoke test. I advocate (a). The engine-implementor advocates (b). Both solve the regression detection problem; they differ on where the test boundary should be.

---

## Dispute 2: Red-blue smoke test -- adhoc path vs pre-built YAML

**My revised position**: The red-blue smoke test should use the adhoc path (`build_adhoc_config -> parse_config -> run_engine`) because this serves as both the mode test and the G1 regression test. My revision section "What I Modify", item 4 identifies the tension: the engine-implementor's R1 ("use pre-built YAML configs for red-blue") and their G1 position ("the smoke test IS the regression test") are contradictory. If the smoke test uses pre-built YAML, it bypasses the adhoc path entirely, and the G1 regression is untested.

**Engine-implementor's revised position (R1)**: "Red-blue tests must use pre-built YAML configs, not the adhoc decide path." R1 is listed as unchanged in their revised table.

**The disagreement**: These positions are directly contradictory. Either the red-blue smoke test goes through the adhoc path (my position) or it uses pre-built YAML (engine-implementor's R1). The engine-implementor's S-3 adopts my xfail resolution for the *first eval run* scoping (exclude red-blue from promptfoo, add a pytest xfail test), but R1 remains unchanged -- meaning even after G1 is fixed, the engine-implementor wants red-blue smoke tests to use pre-built YAML rather than the adhoc path.

**Why I hold my position**: The adhoc path is the path real users take when they run `conversus decide "Q" --mode red-blue`. If the smoke test uses pre-built YAML, it tests a path that only config-file users exercise. The most common consumer invocation (ad-hoc CLI decide) remains untested for red-blue. The G1 fix makes the adhoc path work; after the fix, the smoke test should use that path to prevent G1 from regressing.

The xfail test is a *temporary* measure for the first eval run. Once G1 is fixed, the xfail flips to pass, and the now-passing adhoc-path test should become the permanent red-blue smoke test. The engine-implementor's R1 would make the pre-built YAML the permanent test, with the adhoc path relegated to a side test. I believe this inverts the priority: the adhoc path is the higher-risk, higher-traffic path and should be the primary smoke test.

**Resolution needed**: After G1 is fixed, should the primary red-blue smoke test use the adhoc decide path or a pre-built YAML config? Having both is fine, but which is the smoke-tier gate?

---

## Dispute 3: Consumer-advocate's P0 item 5 -- settings cascade at P0

**My revised position**: Settings cascade *isolation* in test fixtures is P0 (accepted from engine-implementor's R9). Settings cascade *testing* (verifying the provider key wins at each level) is P1. These are different things. Isolation is infrastructure; testing is coverage.

**Consumer-advocate's revised position**: "Test all 5 settings cascade levels including env vars" at P0 (their revised item 5).

**The disagreement**: The consumer-advocate places the full cascade test matrix at P0 ("must fix before implementation"). My revised priority list places it at P1, after the P0 bug fixes and infrastructure. The engine-implementor's revised R9 upgrades isolation to must-fix but does not elevate the cascade test cases themselves to P0.

**Why I hold my position**: P0 items are those without which the eval suite cannot produce meaningful results. The mock provider parse issue, multi-round pipeline gaps, and the red-blue adhoc path are P0 because they determine whether smoke tests are testing production code or fallback code. The settings cascade is important but it is a *correctness* concern, not a *meaningfulness* concern. The eval suite can run and produce meaningful results with hardcoded mock provider in tests even if the cascade is not yet tested. The cascade tests should be written soon (P1) but they do not block the eval suite's initial deployment.

The consumer-advocate's argument is that Desktop Extension users depend on the env var cascade layer. This is true, but the eval suite's first job is to catch engine regressions on every commit (smoke tier), not to validate every consumer configuration path. Cascade testing is a functional-tier concern that belongs at P1.

---

## Dispute 4: Persistence round-trip tests -- P1 vs P2 vs P3

**My revised position**: P3 for persistence round-trip testing. My revision explicitly withdrew persistence internals from eval-suite scope (section "What I Withdraw", item 3), accepting the engine-implementor's point that persistence write/read is a unit-test concern for `engine/tests/`, not an eval-suite concern.

**Consumer-advocate's revised position**: P1, item 20 -- "Add persistence round-trip tests (persist, list, show)."

**Engine-implementor's revised position**: Does not explicitly prioritize persistence round-trip, but M-6 (R8) focuses on using persistence as an access mechanism for intermediate artifacts in quality tests.

**The disagreement**: The consumer-advocate places persistence testing two priority tiers higher than I do. Their argument (revision section 4.1) is that `persist_deliberation()` and `list_deliberations()` are existing engine features called by `engine/handlers.py` today, not future features. They frame these as "tests of existing engine features that the paid tier will depend on."

**Why I hold my position**: The eval suite's scope is externally observable behavior validated through the engine's defined surfaces (CLI, MCP, SDK). Persistence write/read is an internal mechanism. The eval suite should test that `conversus decide` produces correct output and that the output can be retrieved via `list_deliberations` -- but this is an integration test (P3 in my revised table), not a P1 functional test. The consumer-advocate is right that the code exists and is called today, but not every existing code path belongs in the eval suite at P1. The engine's own `engine/tests/` directory is the right home for persistence unit tests. The eval suite should exercise persistence only as a side effect of end-to-end tests, not as a dedicated test dimension.

If the spec author agrees persistence is eval-suite scope (not unit-test scope), I would accept P2. I cannot accept P1 ahead of arbiter tests, iteration loop tests, and schema snapshot tests, all of which test externally observable pipeline behavior rather than internal storage mechanics.

---

## Dispute 5: Desktop Extension content scanner testing -- scope boundary

**My revised position**: I did not include Desktop Extension content scanner testing in my revised priority list at any priority level. I acknowledged the consumer-advocate's finding as "excellent" in my cross-review (section 3.1) but did not assign it a priority in my revision.

**Consumer-advocate's revised position**: P1 (item 18) -- "Test Desktop Extension content scanner for all 7 MCP prompts."

**Engine-implementor's revised position (M-7, item 1)**: "Valid concern, but this is a Desktop Extension integration test, not an engine eval test. The role-split workaround in `design_deliberation()` and `analyze_documents()` is engine code, but the content scanner is a Claude Desktop platform constraint. I acknowledge this exists but maintain it belongs in Desktop Extension CI, not Spec 061."

**The disagreement**: I agree with the engine-implementor's scope assessment. The content scanner is a platform constraint external to the conversus engine. Testing that prompts pass the content scanner is testing the integration between the engine's MCP server and Claude Desktop's platform behavior. This belongs in the Desktop Extension's own CI pipeline, not in the engine eval suite.

The consumer-advocate argues the MCP server already uses a role-split workaround, making it engine code. But the workaround exists to accommodate an external constraint. If the content scanner rules change, the workaround must change, but that is a Desktop Extension concern. The engine eval suite should test that the MCP server produces correct deliberation results, not that its prompt formatting satisfies an external platform's content policy.

**Resolution needed**: Does the engine eval suite test platform-specific integration constraints, or only engine-internal correctness? If the former, the content scanner test belongs. If the latter, it belongs in Desktop Extension CI. I advocate the latter.

---

## Dispute 6: Extended modes -- concrete test cases vs error-or-success semantics

**Resolved with residual concern.** All three reviewers agree the 4 extended modes (negotiation, resource-allocation, fair-division, mechanism-design) need concrete test cases rather than "(if supported in decide)." The engine-implementor's R18 says each must produce "either a valid output or a clear, documented error." The consumer-advocate agrees. I agree with this framing.

**Residual concern**: Nobody has verified whether these modes actually work through the adhoc path. The engine-implementor's original review (section 3.1.1) says "these likely work structurally but I have not verified their template variables are populated." This uncertainty should be resolved before writing the test cases. The spec should require: before R18's test cases are written, the spec author must confirm (by running each mode once with mock provider) whether extended modes produce output or errors via the adhoc decide path. The test expectations depend on this empirical fact, and no reviewer has established it.

This is not a dispute between reviewers -- it is an unresolved question that all three reviewers deferred. I flag it here because the test design depends on the answer.

---

## Summary of disputes

| # | Topic | My position | Opposing position | Opposing agent |
|---|-------|-------------|-------------------|----------------|
| 1 | Mock provider approach | Fixture test for parse_synthesis; do not modify mock provider | Enhance mock provider with realistic response mode (R14) | Engine-implementor |
| 2 | Red-blue smoke path | Adhoc path (build_adhoc_config -> parse_config -> run_engine) | Pre-built YAML config (R1, unchanged) | Engine-implementor |
| 3 | Settings cascade priority | Isolation P0, cascade testing P1 | Full cascade testing at P0 | Consumer-advocate |
| 4 | Persistence round-trip priority | P3 (unit-test scope, not eval-suite scope) | P1 (existing engine feature) | Consumer-advocate |
| 5 | Content scanner testing scope | Out of scope for engine eval suite | P1 in engine eval suite | Consumer-advocate |
| 6 | Extended modes (residual) | Empirical verification needed before test design | No reviewer disagrees, but none resolved it either | All (unresolved) |

**Escalation recommendation**: Disputes 1 and 2 are the most consequential because they affect the architecture of the smoke tier. If the mock provider is enhanced (dispute 1, engine-implementor's position) and red-blue uses pre-built YAML (dispute 2, engine-implementor's position), the smoke tier tests a realistic-but-artificial path. If the fixture test is used (dispute 1, my position) and red-blue uses the adhoc path (dispute 2, my position), the smoke tier tests the actual user path with a separate parser regression test. These are coherent alternative philosophies about what the smoke tier should validate, and the spec author should choose one consistently.
