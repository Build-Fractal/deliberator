# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.5.0](https://github.com/Build-Fractal/conversus-oss/compare/v0.4.0...v0.5.0) (2026-06-30)


### ⚠ BREAKING CHANGES

* Project renamed from `conversus` to `deliberator` across all living surfaces. Pre-first-PyPI-publish, so no external migration burden — but every internal reference, doc, manifest, and import path is touched.

### rename

* conversus → deliberator (project, package, CLI, repo) ([#169](https://github.com/Build-Fractal/conversus-oss/issues/169)) ([8791dd3](https://github.com/Build-Fractal/conversus-oss/commit/8791dd335f6d62a5c7e23803a98075f040e3a4db))


### Added

* **047-phase5:** negotiation AgentFeatures time-ranged ZOPA fields ([#126](https://github.com/Build-Fractal/conversus-oss/issues/126)) ([d88164a](https://github.com/Build-Fractal/conversus-oss/commit/d88164ae16e7dd5ddf4547ad7146b5573dc86bd4))
* **060 Phase 2:** wire MCP context through to claude-desktop provider ([1857ce4](https://github.com/Build-Fractal/conversus-oss/commit/1857ce4d31c8c391c6c9b332fd45e7d56868ed6b))
* add "demo" provider alias + default to demo for Desktop Extension ([618d1c4](https://github.com/Build-Fractal/conversus-oss/commit/618d1c477c32b0e42b9ef5207cd2cfc6f292e576))
* add conversus_login MCP tool to hand-written server + manifest ([cfb0706](https://github.com/Build-Fractal/conversus-oss/commit/cfb0706759d524649954b1e38a938d44195830ec))
* add Design Deliberation prompt — guided multi-turn config builder ([d428438](https://github.com/Build-Fractal/conversus-oss/commit/d428438ed65fdb939ea69552888497f1ec2d9d86))
* **ci:** close Principle XXII remediation — per-channel vendoring gates ([#142](https://github.com/Build-Fractal/conversus-oss/issues/142)) ([8a1ff5c](https://github.com/Build-Fractal/conversus-oss/commit/8a1ff5cae629b00fbc7e1c11fe069e7994788787))
* **constitution:** v2.2.0 → v2.3.0 — implement spec 066 amendment package ([#19](https://github.com/Build-Fractal/conversus-oss/issues/19)) ([cc54ef6](https://github.com/Build-Fractal/conversus-oss/commit/cc54ef6c25ad642d2993a59ffa9dad950979b94d))
* **constitution:** v2.3.1 → v2.3.2 — Principle XVI determinism scope ([#29](https://github.com/Build-Fractal/conversus-oss/issues/29)) ([804f8ee](https://github.com/Build-Fractal/conversus-oss/commit/804f8eeee4822980a5b0a7c19eb8ffa7cc5af215))
* **constitution:** v2.3.2 → v2.4.0 — Constitutional Inclusion Criteria gate (MINOR) ([#32](https://github.com/Build-Fractal/conversus-oss/issues/32)) ([e43701c](https://github.com/Build-Fractal/conversus-oss/commit/e43701c4f584f8a946d38789921aeb75ad62d71c))
* **constitution:** v2.4.0 → v2.5.0 — Principle XXVIII (Test-Fix Boundary Preservation) ([#46](https://github.com/Build-Fractal/conversus-oss/issues/46)) ([2ec0e8a](https://github.com/Build-Fractal/conversus-oss/commit/2ec0e8a10856c5980295c6cebf1a9a3c46f854b2))
* **constitution:** v2.5.0 → v2.6.0 — Principle XVI Option A refactor (path (c)) + Governance path (c) definition ([#95](https://github.com/Build-Fractal/conversus-oss/issues/95)) ([f06e026](https://github.com/Build-Fractal/conversus-oss/commit/f06e0267c28a5b78e909a68d16435f296f8498f9))
* **constitution:** v2.6.0 → v3.0.0 — VI/X removal + Principle II stable-interfaces + Number Stability governance ([#98](https://github.com/Build-Fractal/conversus-oss/issues/98)) ([8c4a308](https://github.com/Build-Fractal/conversus-oss/commit/8c4a3088e679e743dab83ae8f5a54d47b9eb8ca7))
* **constitution:** v3.1.3 → v3.2.0 — pathway taxonomy migrated to Governance subsection ([#116](https://github.com/Build-Fractal/conversus-oss/issues/116)) ([fca80fe](https://github.com/Build-Fractal/conversus-oss/commit/fca80fedc300adccbe13232c0eba2748083f0e68))
* conversus snap — PreToolUse hook prototype for Claude Code ([#152](https://github.com/Build-Fractal/conversus-oss/issues/152)) ([6bfa733](https://github.com/Build-Fractal/conversus-oss/commit/6bfa7337a2c79780754060dde8e55e17d02b42ac))
* default provider to claude-desktop, pipe-delimited option descriptions ([79f73bf](https://github.com/Build-Fractal/conversus-oss/commit/79f73bf2baff4e3bd091c180833e52d6e014621a))
* **docs:** guided /conversus design flow + manual config walkthrough ([07811e4](https://github.com/Build-Fractal/conversus-oss/commit/07811e49791bda6d5ffe14226d4295b43400c98f))
* engine-first /conversus skill + 28 pytest tests ([2c0a2ff](https://github.com/Build-Fractal/conversus-oss/commit/2c0a2ffdb2534dfb2133109dcbecc3dbea98a869))
* **engine:** claude-code-subprocess judge for deepeval (closes [#87](https://github.com/Build-Fractal/conversus-oss/issues/87)) ([#89](https://github.com/Build-Fractal/conversus-oss/issues/89)) ([ddcfa43](https://github.com/Build-Fractal/conversus-oss/commit/ddcfa435e3b7b41831e4d62cd75c9a9d4777e57d))
* **engine:** close spec 006 — resolution.md parser + FR-P2-7 SC tests + move to done/ ([#70](https://github.com/Build-Fractal/conversus-oss/issues/70)) ([4bc8626](https://github.com/Build-Fractal/conversus-oss/commit/4bc862608f601dde739e31f2b54dbfbe6e5919b1))
* **engine:** context-aware default provider — claude-code in Claude Code sessions ([#133](https://github.com/Build-Fractal/conversus-oss/issues/133)) ([18ef4dc](https://github.com/Build-Fractal/conversus-oss/commit/18ef4dc7448113a98de0ef387c5a8ec4a5c919f8))
* **engine:** default deepeval deliberation provider to claude-code (OAuth-friendly) ([#86](https://github.com/Build-Fractal/conversus-oss/issues/86)) ([72a29a0](https://github.com/Build-Fractal/conversus-oss/commit/72a29a028c474d212de45c56aa01d74d7376dcf4))
* **engine:** spec 006 Phase 2 FR-P2-1 + FR-P2-2 — strict inter-round validation + arbiter/→arbitration/ path rename ([#65](https://github.com/Build-Fractal/conversus-oss/issues/65)) ([51f153f](https://github.com/Build-Fractal/conversus-oss/commit/51f153f006db4cb5c2fe4e37c8b395de828ae76c))
* **engine:** spec 006 Phase 2 FR-P2-3 + FR-P2-5 — round-loop parity test + template variable wiring (+ surprise fix: stale prior_arbitration_path after retroactive move) ([#66](https://github.com/Build-Fractal/conversus-oss/issues/66)) ([f797085](https://github.com/Build-Fractal/conversus-oss/commit/f79708568ca067ee46d4aff186a449826e431661))
* **engine:** spec 006 Phase 2 FR-P2-4 — influence-aware dispute counting (accounting logic only) ([#67](https://github.com/Build-Fractal/conversus-oss/issues/67)) ([0ba6fe7](https://github.com/Build-Fractal/conversus-oss/commit/0ba6fe72fa2f0d6c7d98fa1aed706ea04108b94f))
* **engine:** spec 006 Phase 2 FR-P2-6 — cross-round Resolution Attribution wiring ([#69](https://github.com/Build-Fractal/conversus-oss/issues/69)) ([b20607e](https://github.com/Build-Fractal/conversus-oss/commit/b20607eb56fbc7051b7a4dea163acc276eeedb77))
* **engine:** spec 057 SC-001 — init writes settings.yml; legacy settings.json migrated ([#72](https://github.com/Build-Fractal/conversus-oss/issues/72)) ([03344c1](https://github.com/Build-Fractal/conversus-oss/commit/03344c1651109d470e5e3a9bd996b4ae02fcfcc6))
* **engine:** spec 057 SC-003 — settings cascade display in `conversus status` ([#71](https://github.com/Build-Fractal/conversus-oss/issues/71)) ([431d2ea](https://github.com/Build-Fractal/conversus-oss/commit/431d2ea827c2c978593f688a1184f02bc41b1216))
* **engine:** spec 057 SC-004 — per-provider credentials with deliberation-amended migration ([#74](https://github.com/Build-Fractal/conversus-oss/issues/74)) ([8451196](https://github.com/Build-Fractal/conversus-oss/commit/8451196f4b3de57003184d2428c4f2a71f61924a))
* **engine:** spec 061 step 7 — deepeval quality tests for deliberation pipeline ([#83](https://github.com/Build-Fractal/conversus-oss/issues/83)) ([e9c39d4](https://github.com/Build-Fractal/conversus-oss/commit/e9c39d4c3da9757e8d2ec00cb57b91c45a987f81))
* **engine:** spec 061 step 8 — baseline-snapshot capture infrastructure ([#93](https://github.com/Build-Fractal/conversus-oss/issues/93)) ([e1e22ba](https://github.com/Build-Fractal/conversus-oss/commit/e1e22ba9948e0b1d45134d59ec938ba5fb00d6a4))
* **engine:** spec 072 — credential source display in conversus status (closes [#73](https://github.com/Build-Fractal/conversus-oss/issues/73)) ([#76](https://github.com/Build-Fractal/conversus-oss/issues/76)) ([b8934c9](https://github.com/Build-Fractal/conversus-oss/commit/b8934c943151c9110f2c1d5f1f27bb4df7c3e14b))
* **evals:** add engine eval suite — spec 061 + promptfoo baseline ([59a7bf3](https://github.com/Build-Fractal/conversus-oss/commit/59a7bf38ec93b85068ece16c011a711200ca2e60))
* **evals:** CI workflow + Ollama local model support ([01de8fb](https://github.com/Build-Fractal/conversus-oss/commit/01de8fba673d6645d5a42ae155071c207170ddf8))
* expose login on MCP surface — Desktop users auth from chat ([9a367ab](https://github.com/Build-Fractal/conversus-oss/commit/9a367ab9c324eb116bf7caf785077cbaf9c2b249))
* **extension:** user_config settings + env var cascade for Desktop users ([8a0f997](https://github.com/Build-Fractal/conversus-oss/commit/8a0f9975ebbfe43361212f39b02a0a09befc2047))
* implement spec 006 inter-round arbitration + housekeeping ([47ab8c6](https://github.com/Build-Fractal/conversus-oss/commit/47ab8c61595a9eca0d10cd9bf6721c200cb5f44d))
* implement spec 055 capability registry with per-surface adapters ([de2fd47](https://github.com/Build-Fractal/conversus-oss/commit/de2fd4774a09cd0960b33e067e9427e81f5b0673))
* implement spec 056 — deliberation persistence + list/show tools ([5f49c4e](https://github.com/Build-Fractal/conversus-oss/commit/5f49c4ee66944d63c5b555db645501c24443de36))
* implement spec 057 — settings cascade (.conversus/ directory) ([6a73aa2](https://github.com/Build-Fractal/conversus-oss/commit/6a73aa27724df67837e5b38122c6a6b5785d549f))
* implement spec 059 — MCP prompts + CLI skill viewer ([c38c3ef](https://github.com/Build-Fractal/conversus-oss/commit/c38c3eff89951f6c4fc97d575d8635c46189069f))
* initial conversus open-source extraction (Apache-2.0) ([1bfd62c](https://github.com/Build-Fractal/conversus-oss/commit/1bfd62c99d1c665fb62766eeddd182bb3bad28a4))
* **linter:** add XII dead-infrastructure linter ([#136](https://github.com/Build-Fractal/conversus-oss/issues/136)) ([15f0f2f](https://github.com/Build-Fractal/conversus-oss/commit/15f0f2fa330b96c4bca632bbc3a55f3e4dfd3fa9))
* **linter:** close Principle V remediation — cross-mode output_contract coverage ([#139](https://github.com/Build-Fractal/conversus-oss/issues/139)) ([8b80a4c](https://github.com/Build-Fractal/conversus-oss/commit/8b80a4ca4aa8e0954ddc1c1cf88ba43a5bb351f3))
* **linter:** spec 047 — structured Duration parser + temporal classifier (Phases 1-4) ([#82](https://github.com/Build-Fractal/conversus-oss/issues/82)) ([115f1fc](https://github.com/Build-Fractal/conversus-oss/commit/115f1fc1d5351fc6630bd719b5d6dcc156e1bcaf))
* **lint:** scripts/lint-test-fixes.py + advisory CI workflow ([#49](https://github.com/Build-Fractal/conversus-oss/issues/49)) ([55b9372](https://github.com/Build-Fractal/conversus-oss/commit/55b93722c1f164137ae7ec5e4d7618f508939c77))
* **mcp:** Phase 2 drift guard + add 2 missing tool decorators ([#22](https://github.com/Build-Fractal/conversus-oss/issues/22)) ([fa2291c](https://github.com/Build-Fractal/conversus-oss/commit/fa2291c0b7fa3611e0c8aa0b151319abd646226f))
* **mcp:** support CONVERSUS_DISABLED_TOOLS env var to hide tools ([#14](https://github.com/Build-Fractal/conversus-oss/issues/14)) ([850d0b0](https://github.com/Build-Fractal/conversus-oss/commit/850d0b007fda324a6d6f910087cf5a83cde191a3))
* **packaging:** force-include mcp_server.py + capabilities.py in wheel ([#11](https://github.com/Build-Fractal/conversus-oss/issues/11)) ([da12b53](https://github.com/Build-Fractal/conversus-oss/commit/da12b53bfa5817c3072030fa7d6255fef6428d43))
* **packaging:** project manifest.json tools[] from CAPABILITIES registry ([#18](https://github.com/Build-Fractal/conversus-oss/issues/18)) ([3493da9](https://github.com/Build-Fractal/conversus-oss/commit/3493da96862609da2e340c9db45db72d64a505e5))
* **plugin:** add init, status, login, logout slash commands ([dc9053e](https://github.com/Build-Fractal/conversus-oss/commit/dc9053e82dbb9c831022ecec2644271f92ba7801))
* **plugin:** restructure to official Claude Code / Cowork format + marketplace ([d5e898d](https://github.com/Build-Fractal/conversus-oss/commit/d5e898d135f423f404b4f145c73e47f5c166d6a4))
* **pr-template:** add Principle XXVIII test-fix discipline section ([#48](https://github.com/Build-Fractal/conversus-oss/issues/48)) ([22e1958](https://github.com/Build-Fractal/conversus-oss/commit/22e19583d82a9f508836d1090ebe75d6a1c27f5c))
* **projector:** add compile-check validation before overwriting generated files ([3a02d98](https://github.com/Build-Fractal/conversus-oss/commit/3a02d9817f2defa8612d6977f5ec4ecd90367a7a))
* **prompts:** add analyze_documents — multi-agent doc analysis ([290b900](https://github.com/Build-Fractal/conversus-oss/commit/290b900caade2f53d19ee139f463075fe9abf1c5))
* **prompts:** guided flow — analyze, recommend, explain, confirm before running ([644b50c](https://github.com/Build-Fractal/conversus-oss/commit/644b50cb70155221a9777fd08ce6192cb2cd64ca))
* **prompts:** role-split pattern + enriched tool descriptions ([344cc14](https://github.com/Build-Fractal/conversus-oss/commit/344cc142901d6cf2bd2bc73a6c9389eaac9580bc))
* **providers:** wire token tracking across all providers + live integration tests ([#8](https://github.com/Build-Fractal/conversus-oss/issues/8)) ([b7e8bd2](https://github.com/Build-Fractal/conversus-oss/commit/b7e8bd2c431e54b6ca05f1db1256681e540a8669))
* **registry:** spec 064 — capability discovery via entry points ([#2](https://github.com/Build-Fractal/conversus-oss/issues/2)) ([d8f7f81](https://github.com/Build-Fractal/conversus-oss/commit/d8f7f810cbbedc6e916dedf4433af2c29d90726d))
* **registry:** spec 064.1 — runtime registration of discovered capabilities ([#4](https://github.com/Build-Fractal/conversus-oss/issues/4)) ([8ee7cc3](https://github.com/Build-Fractal/conversus-oss/commit/8ee7cc3b2cfa8a6e159d8e9ffe49cdc216f78200))
* **safety:** close Principle XXIV remediation — enumerated safety perimeters ([2e8d349](https://github.com/Build-Fractal/conversus-oss/commit/2e8d3493b527088ccc7cf6dd13372205309e8b5d))
* **safety:** close Principle XXIV remediation — enumerated safety perimeters ([#141](https://github.com/Build-Fractal/conversus-oss/issues/141)) ([4e39b90](https://github.com/Build-Fractal/conversus-oss/commit/4e39b901bd0a19deb12805b6f3e969ebd90a46c3))
* **scripts:** strip-constitution-for-blind.py — spec 067 §4.2 reference impl ([#25](https://github.com/Build-Fractal/conversus-oss/issues/25)) ([57f0eee](https://github.com/Build-Fractal/conversus-oss/commit/57f0eee05c23f66fb072b75e3b0caf749b77cfe8))
* security tests + provider API keys + default provider anthropic ([efab853](https://github.com/Build-Fractal/conversus-oss/commit/efab853712f4e1abe491320af8f0a4fe575ab541))
* spec 060 + claude-desktop provider skeleton + demo alias ([7b61889](https://github.com/Build-Fractal/conversus-oss/commit/7b618898bb700d80ce5662016bd1490b2c347f90))
* **spec-059:** Phase 2 CLI skill viewer + Phase 3 help meta-skill ([#132](https://github.com/Build-Fractal/conversus-oss/issues/132)) ([56d4ae5](https://github.com/Build-Fractal/conversus-oss/commit/56d4ae501acd9a0df824d0349f16e58773859c70))
* **spec-073:** file spec 070 closure correction (path b) + verification trail ([#117](https://github.com/Build-Fractal/conversus-oss/issues/117)) ([cc0a811](https://github.com/Build-Fractal/conversus-oss/commit/cc0a811b6b5b7257adbacc4aa8accd1d99aaa2d4))
* **test:** close Principle XXVI remediation — mode×provider matrix meta-test ([#140](https://github.com/Build-Fractal/conversus-oss/issues/140)) ([edf6dbf](https://github.com/Build-Fractal/conversus-oss/commit/edf6dbfb9f8ed3a9320a00337a779d6b04df355a))
* three-layer distribution — PyPI, MCP server, Claude Code plugin + docs ([b3730dd](https://github.com/Build-Fractal/conversus-oss/commit/b3730dd4b449adb86bc2d9bdca5b0b31739d521f))
* v4.0.0 constitutional tier extraction + suite admission ([#134](https://github.com/Build-Fractal/conversus-oss/issues/134)) ([79fcf0f](https://github.com/Build-Fractal/conversus-oss/commit/79fcf0f6b4909a83f8879461ddab821c9ccf3c3e))
* **v4.2.0:** § 5.2 renderer — deterministic JSON → Markdown ([#156](https://github.com/Build-Fractal/conversus-oss/issues/156)) ([e3e54c7](https://github.com/Build-Fractal/conversus-oss/commit/e3e54c729c211c6f07cbe4ba82af7f5cffd095b8))
* **v4.2.0:** F2c — schema-validate CI gate + persist_output + 18 fixtures ([#154](https://github.com/Build-Fractal/conversus-oss/issues/154)) ([5fffdde](https://github.com/Build-Fractal/conversus-oss/commit/5fffdde1fb48eb9843c619cdbce619edbec1b229))
* **wheel:** ship quality-floor + antipatterns as wheel package data ([#1](https://github.com/Build-Fractal/conversus-oss/issues/1)) ([0f10158](https://github.com/Build-Fractal/conversus-oss/commit/0f101583115a0754517f3ad94b0d2708fdb7bbb4))


### Fixed

* add `-type f` so find only matches regular files. ([6943d1a](https://github.com/Build-Fractal/conversus-oss/commit/6943d1ad52bae1c02c753c07dcdc04e2fdc52e0c))
* add antipatterns/ catalog from conversus repo ([2f442b3](https://github.com/Build-Fractal/conversus-oss/commit/2f442b3fcbe44f7e3afa9bed2ca4d703aaaccc2b))
* add quality-floor/ fixtures from conversus repo — fixes 4 test failures ([c8c26d6](https://github.com/Build-Fractal/conversus-oss/commit/c8c26d6a5ec09061e16516cb7ea33ee32f8d6caa))
* **anthropic:** respect OAuth subscription concurrency + retry 429s with jitter ([#6](https://github.com/Build-Fractal/conversus-oss/issues/6)) ([880b9e3](https://github.com/Build-Fractal/conversus-oss/commit/880b9e37d25f9fa24f9a9f83fcc592f443ce7d89))
* **ci:** flatten artifacts with -type f to avoid name collision ([6943d1a](https://github.com/Build-Fractal/conversus-oss/commit/6943d1ad52bae1c02c753c07dcdc04e2fdc52e0c))
* **ci:** revert artifact actions to v4 — immutable releases incompatible with v7/v8 ([e9df51d](https://github.com/Build-Fractal/conversus-oss/commit/e9df51d4710e0fe7cdfc5a15e5dea965d2a05a75))
* **ci:** revert softprops/action-gh-release to v2 ([a54ad9b](https://github.com/Build-Fractal/conversus-oss/commit/a54ad9bc4c865025bfb3784ca77dfd96d5a55ba8))
* **ci:** unbreak linter-checks + .mcpb bundle smoke ([#153](https://github.com/Build-Fractal/conversus-oss/issues/153)) ([9383d54](https://github.com/Build-Fractal/conversus-oss/commit/9383d54bab4203cdf521974e4302269c46582649))
* **ci:** use removesuffix, drop deprecated macos-13 runner ([b0956f7](https://github.com/Build-Fractal/conversus-oss/commit/b0956f727212718c1befb58abb4a045b3a767dd6))
* **claude-code:** parse current claude CLI single-object JSON output ([#9](https://github.com/Build-Fractal/conversus-oss/issues/9)) ([b00e64c](https://github.com/Build-Fractal/conversus-oss/commit/b00e64cae0539daaf16ce319507cfa3e22deaee5))
* **claude-code:** treat tool-use-only responses as success ([#5](https://github.com/Build-Fractal/conversus-oss/issues/5)) ([9c1df23](https://github.com/Build-Fractal/conversus-oss/commit/9c1df23d91154ce8e5bafba10992a70ff60d00a0))
* claude-desktop falls back to anthropic credentials when no MCP context ([791ef95](https://github.com/Build-Fractal/conversus-oss/commit/791ef95cc1a0a4d6501b6d2d8a82c2482ccdb6b3))
* **cli:** accept --provider claude-desktop + demo (sync Click choices with registry) ([#162](https://github.com/Build-Fractal/conversus-oss/issues/162)) ([2b4ca3b](https://github.com/Build-Fractal/conversus-oss/commit/2b4ca3bf13e43725da1d7fe8b36166a2701b363b))
* **config:** apply target's two-pass path resolution to arbiter.grounding ([#168](https://github.com/Build-Fractal/conversus-oss/issues/168)) ([a95d6f5](https://github.com/Build-Fractal/conversus-oss/commit/a95d6f536d0d7155aea147ff965da77ea0350367))
* **constitution:** v2.3.0 → v2.3.1 — XV registry-boundary clarification (PATCH) ([#20](https://github.com/Build-Fractal/conversus-oss/issues/20)) ([833c0e4](https://github.com/Build-Fractal/conversus-oss/commit/833c0e412f53cd6896e30d724c6430e7e6a23d5c))
* **constitution:** v3.0.0 → v3.1.0 — cycle 2B retroactive Origin Amendment records (closes [#96](https://github.com/Build-Fractal/conversus-oss/issues/96)) ([#103](https://github.com/Build-Fractal/conversus-oss/issues/103)) ([47caa27](https://github.com/Build-Fractal/conversus-oss/commit/47caa273913948ac0eed9eb4ba18c078a282907f))
* **constitution:** v3.1.0 → v3.1.1 — cycle 2C XIX labels-only sub-headings (closes [#97](https://github.com/Build-Fractal/conversus-oss/issues/97)) ([#104](https://github.com/Build-Fractal/conversus-oss/issues/104)) ([767f47d](https://github.com/Build-Fractal/conversus-oss/commit/767f47dd29aeb38db73c22e7553f25b43c7a1e61))
* **constitution:** v3.1.1 → v3.1.2 — Principle II same-version no-reuse elaboration ([#105](https://github.com/Build-Fractal/conversus-oss/issues/105)) ([f1d2374](https://github.com/Build-Fractal/conversus-oss/commit/f1d23743925bc5630466ddc64f3f69e31a0cb905))
* **constitution:** v3.1.2 → v3.1.3 — cycle 2C bullet-split follow-on ([#107](https://github.com/Build-Fractal/conversus-oss/issues/107)) ([945ab77](https://github.com/Build-Fractal/conversus-oss/commit/945ab77256c286295ddf72be3ba1833ba966a095))
* **constitution:** v3.2.0 → v3.2.1 — Governance operational-guidance list discharge ([#118](https://github.com/Build-Fractal/conversus-oss/issues/118)) ([29ed6eb](https://github.com/Build-Fractal/conversus-oss/commit/29ed6eb164b78164c9a116a2d0809ce98eb3bff7))
* **constitution:** v3.2.1 → v3.2.2 — cycle 3D gate calibration positive worked example ([#124](https://github.com/Build-Fractal/conversus-oss/issues/124)) ([2533fc3](https://github.com/Build-Fractal/conversus-oss/commit/2533fc342e234b67fbebff8a4f2190c11a2c70be))
* **constitution:** v3.2.2 → v3.2.3 — issue [#94](https://github.com/Build-Fractal/conversus-oss/issues/94) shape→assembly-form rename ([#130](https://github.com/Build-Fractal/conversus-oss/issues/130)) ([8d1ea9a](https://github.com/Build-Fractal/conversus-oss/commit/8d1ea9af616125ae9c4af61f01c7cdbf1e38403a))
* correct install URLs — conversus-oss (not conversus) ([28a602f](https://github.com/Build-Fractal/conversus-oss/commit/28a602fd4cddf410133878cefad244f9dcd3475b))
* **cost+test:** spec 061 step 13 §3.1.9 gaps + cost-formula bug fix ([#115](https://github.com/Build-Fractal/conversus-oss/issues/115)) ([8c05f54](https://github.com/Build-Fractal/conversus-oss/commit/8c05f544eb189b4d20828c1eb69eb9fb12949f59))
* **engine:** isolate arbiter context — drop target_files inlining ([#135](https://github.com/Build-Fractal/conversus-oss/issues/135)) ([2825bb4](https://github.com/Build-Fractal/conversus-oss/commit/2825bb43668ae4f2b29ef0875e86d7ee043aaddd))
* **engine:** silent-stub abort + claude-code model passthrough + decide --model ([#52](https://github.com/Build-Fractal/conversus-oss/issues/52)) ([9017de7](https://github.com/Build-Fractal/conversus-oss/commit/9017de75faba338a654388989c1b8139fb92d9f3))
* **engine:** terminal-phase isolation — outer-loop retry for synthesis + arbitration ([#144](https://github.com/Build-Fractal/conversus-oss/issues/144)) ([bfc2a28](https://github.com/Build-Fractal/conversus-oss/commit/bfc2a28912cd56878405347f67af512896ad70df))
* **extension:** add required title field to manifest prompts ([0ba9811](https://github.com/Build-Fractal/conversus-oss/commit/0ba981118e085698d49cb6d6cf902972e6f558a2))
* **extension:** bundle presets/, schema/, templates/ + set CWD for engine ([39e891f](https://github.com/Build-Fractal/conversus-oss/commit/39e891f17d4808e0df21d0dc767a5c4eb88c760f))
* **extension:** CONVERSUS_ROOT env var for bundled runtime data discovery ([8c6720f](https://github.com/Build-Fractal/conversus-oss/commit/8c6720fcb101755faf8ad056ca734a12d75c3934))
* **extension:** correct user_config schema — add required title field ([dc1cf1c](https://github.com/Build-Fractal/conversus-oss/commit/dc1cf1c7655ca297137ca34f9e82d0ff29c8ca9a))
* **extension:** declare prompts in manifest.json — required by MCPB spec ([6cda717](https://github.com/Build-Fractal/conversus-oss/commit/6cda717b07b42b2e64d8e46ab2338ad6bf859ef5))
* **extension:** long_description is markdown, not plain text ([6b63b12](https://github.com/Build-Fractal/conversus-oss/commit/6b63b12362fc24aab29c8e97ed50968d9f90ad1a))
* **extension:** normalize manifest.json whitespace after tools[] patch ([5fe7007](https://github.com/Build-Fractal/conversus-oss/commit/5fe70071ff46759422a1eeeb4e51d19a1cd4ed05))
* **extension:** prompts need text field, not title — different schema from user_config ([a891554](https://github.com/Build-Fractal/conversus-oss/commit/a8915540d4bb4c2611ac1d6b5f409c4a8c190a19))
* **extension:** remove user_config — schema incompatible with Claude Desktop ([ff750e2](https://github.com/Build-Fractal/conversus-oss/commit/ff750e2cba239cd149320d3a316abd429fdd7f62))
* **extension:** restore hand-written MCPB tool descriptions via adapter overrides ([a3898f7](https://github.com/Build-Fractal/conversus-oss/commit/a3898f7c428dcbddc27a6d240cc8b996ea36d5bc))
* **extension:** rewrite manifest + add dedicated docs page ([8b6b2e3](https://github.com/Build-Fractal/conversus-oss/commit/8b6b2e36b26caa84ac3fec7f4c2e927853cdf12c))
* **extension:** setup section stays in Desktop session, no terminal reference ([d25d8f9](https://github.com/Build-Fractal/conversus-oss/commit/d25d8f98d29c7571643802da8242f127de16e235))
* **extension:** shorten long_description, add "Try it" prompts, document walkthrough ([8784187](https://github.com/Build-Fractal/conversus-oss/commit/878418774d52cf2134d545b96e4d235fd1e8e85f))
* **G11:** use resolve_execution_provider in MCP handlers ([a2d11f6](https://github.com/Build-Fractal/conversus-oss/commit/a2d11f61a8ed4057abef5470c90c2836f8fa58e4))
* **G1:** red-blue mode in adhoc decide + eval coverage ([bb9c2e9](https://github.com/Build-Fractal/conversus-oss/commit/bb9c2e993ea53d7d425f575bc4ae707f98c86209))
* **G2,G12:** target path resolution + provider whitelist ([59c3bd5](https://github.com/Build-Fractal/conversus-oss/commit/59c3bd5f0621b74ba3f518c9daf7d2667626ea2a))
* **handlers,tests:** resolve find_project_root shadowing + quality-floor path drift ([#42](https://github.com/Build-Fractal/conversus-oss/issues/42)) ([6df9e52](https://github.com/Build-Fractal/conversus-oss/commit/6df9e5234c019e53228bcb7831e622613f9e8f6d))
* **linter:** make tier_coherence robust to monorepo nesting ([#137](https://github.com/Build-Fractal/conversus-oss/issues/137)) ([24858f0](https://github.com/Build-Fractal/conversus-oss/commit/24858f0d46c7b69c3dace6a8c8ec4254ff125886))
* **mcp:** surface errors for invalid provider/mode instead of silent run ([#45](https://github.com/Build-Fractal/conversus-oss/issues/45)) ([63e23f2](https://github.com/Build-Fractal/conversus-oss/commit/63e23f24d6e836291f41c5dbc1dbcc34b433acde))
* **mock:** synthesis-phase returns parseable markdown ([bff707b](https://github.com/Build-Fractal/conversus-oss/commit/bff707b3daf5fe6cedd7fa5c124c1811af036a7f))
* **P0:** remove from __future__ import annotations from Pydantic model files ([dbc44aa](https://github.com/Build-Fractal/conversus-oss/commit/dbc44aad2dd0921228a278ad8421b5478db72768))
* **persistence:** project root discovery + settings-aware persistence ([9604979](https://github.com/Build-Fractal/conversus-oss/commit/9604979f42bfb9fdaeb84d06f206d93a46959593))
* **prompts:** return list[dict] not str — FastMCP requires Message objects ([660abf4](https://github.com/Build-Fractal/conversus-oss/commit/660abf4c6e2a2885fcd44fb0a918c43aa5d6560e))
* **prompts:** simplify design_deliberation to avoid injection detection ([e22f8cc](https://github.com/Build-Fractal/conversus-oss/commit/e22f8cc61cbbe70d74e700287ca3b92f482ff4d3))
* **red-blue:** three-layer contract break → false-PASS on dangerous deliberations ([#10](https://github.com/Build-Fractal/conversus-oss/issues/10)) ([6450d91](https://github.com/Build-Fractal/conversus-oss/commit/6450d91f0809103b9a938e2a4cf3cfd1cbf43cc0))
* resolve all test failures for standalone OSS repo ([8a201f5](https://github.com/Build-Fractal/conversus-oss/commit/8a201f58e7fe3572f05880d86a6408e8376342dc))
* **skills:** drop 'subscription' from OAuth marker regex (closes [#59](https://github.com/Build-Fractal/conversus-oss/issues/59)) ([#81](https://github.com/Build-Fractal/conversus-oss/issues/81)) ([6def53c](https://github.com/Build-Fractal/conversus-oss/commit/6def53c18c7ad54e7a12f27907daa1561c24e391))
* **skills:** install probe + OAuth provider preflight + version bump ([#51](https://github.com/Build-Fractal/conversus-oss/issues/51)) ([134717e](https://github.com/Build-Fractal/conversus-oss/commit/134717efd41ad394adfcf8209f40f3e96ff260c3))
* **snap:** honor ANTHROPIC_API_KEY over stored OAuth in auth resolution ([#155](https://github.com/Build-Fractal/conversus-oss/issues/155)) ([c126b03](https://github.com/Build-Fractal/conversus-oss/commit/c126b038a1d70d9e5df589558d5ff61ca0635d59))
* **spec:** 067 §4.3.1 — use existing role presets, do NOT hand-roll ([#23](https://github.com/Build-Fractal/conversus-oss/issues/23)) ([d262e4a](https://github.com/Build-Fractal/conversus-oss/commit/d262e4a2140553274d4073f616aa2f2ad57af298))
* **spec:** annotate spec 066 §7 as superseded by spec 067 ([#24](https://github.com/Build-Fractal/conversus-oss/issues/24)) ([6a17f95](https://github.com/Build-Fractal/conversus-oss/commit/6a17f951f0cf909ad05cacad04f46641b7009609))
* **strip:** exclude HTML comment blocks from --date leakage scan + add tests ([#108](https://github.com/Build-Fractal/conversus-oss/issues/108)) ([fd88285](https://github.com/Build-Fractal/conversus-oss/commit/fd88285b6da952fa9ece5c1436d74e4007574091))
* **test:** allow provider aliases in registry instantiation test ([160fc5c](https://github.com/Build-Fractal/conversus-oss/commit/160fc5c2b998e99cc9406b9a90d5fcd17ed7eab6))
* **tests:** skip optional-extra tests when mcp / deepeval unavailable ([#160](https://github.com/Build-Fractal/conversus-oss/issues/160)) ([323ff49](https://github.com/Build-Fractal/conversus-oss/commit/323ff498fe0c71f3770dc1c8929117129f136c4c))
* **test:** un-xfail strip-script test — version mismatch was test bug, not script bug ([#138](https://github.com/Build-Fractal/conversus-oss/issues/138)) ([f420097](https://github.com/Build-Fractal/conversus-oss/commit/f4200974b27e7bd81fada799487bbbb81a8bc5bc))
* use JetBrains Mono for code blocks instead of Space Grotesk ([c8eb347](https://github.com/Build-Fractal/conversus-oss/commit/c8eb347a3b2a7d3a05955b9d7964e98f1c9d51cb))
* **wheel:** promote conversus.paths from private ([#3](https://github.com/Build-Fractal/conversus-oss/issues/3)) ([bf79adb](https://github.com/Build-Fractal/conversus-oss/commit/bf79adbab99d67f4670cddc83448913763564447))


### Changed

* **061:** apply P0 deliberation findings to spec ([a20c556](https://github.com/Build-Fractal/conversus-oss/commit/a20c556774c60778ca8a646d6c32c9499e070c47))
* add first-deliberation tutorial + specs/deliberations index ([4492fc7](https://github.com/Build-Fractal/conversus-oss/commit/4492fc72b178d28a2be1362ca9f0b3cc5108a6d5))
* **audit-sweep-3:** mkdocs repo_url, CLI count, Cowork refs, schema drift ([#163](https://github.com/Build-Fractal/conversus-oss/issues/163)) ([8050079](https://github.com/Build-Fractal/conversus-oss/commit/8050079bd21206b1a9b803476896f8e05d74f5f7))
* **audit:** nav reorder + gotchas disclaimer honesty ([#166](https://github.com/Build-Fractal/conversus-oss/issues/166)) ([91e98b1](https://github.com/Build-Fractal/conversus-oss/commit/91e98b14907ba93f38d0d87649f9b3b899310913))
* **audit:** troubleshooting page + README CLI completeness + quickstart fail-recipe ([#165](https://github.com/Build-Fractal/conversus-oss/issues/165)) ([783bdb2](https://github.com/Build-Fractal/conversus-oss/commit/783bdb28c425069b0f9860276b56100f2d80000c))
* **deliberation:** naming prompt for fractal namespace consolidation ([#28](https://github.com/Build-Fractal/conversus-oss/issues/28)) ([bbe40f3](https://github.com/Build-Fractal/conversus-oss/commit/bbe40f333894a43dd78cfbe2b0a130fbbb411514))
* **engine:** characterize _gated_dispatch concurrency semantics (closes [#61](https://github.com/Build-Fractal/conversus-oss/issues/61)) ([#80](https://github.com/Build-Fractal/conversus-oss/issues/80)) ([e55d8d5](https://github.com/Build-Fractal/conversus-oss/commit/e55d8d5b52c512c9bd2f7efeae98c2e0694650c6))
* **engine:** propagate Optional[str] model through dispatch (closes [#54](https://github.com/Build-Fractal/conversus-oss/issues/54)) ([#128](https://github.com/Build-Fractal/conversus-oss/issues/128)) ([7ceba50](https://github.com/Build-Fractal/conversus-oss/commit/7ceba50af252337be246941ebea1890be7a54bfa))
* **engine:** switch deepeval judge to Anthropic (spec 061 step 7 follow-up) ([#85](https://github.com/Build-Fractal/conversus-oss/issues/85)) ([cbfb061](https://github.com/Build-Fractal/conversus-oss/commit/cbfb0613bf8d574d2ef5fb107c01e080616cfe7f))
* **examples:** add 4 working configs covering distinct deliberation patterns ([#164](https://github.com/Build-Fractal/conversus-oss/issues/164)) ([091135f](https://github.com/Build-Fractal/conversus-oss/commit/091135fade32b6352483ec542db12e019f812785))
* **extension:** break out all 8 modes + add setup helper section ([8bd53e3](https://github.com/Build-Fractal/conversus-oss/commit/8bd53e338edce77aa080bd49da817fed0d3b5f3c))
* **extension:** expand long_description with pipeline walkthrough and non-tech guide link ([c471c16](https://github.com/Build-Fractal/conversus-oss/commit/c471c166d2c9c4894a822f51ec4bd138223a0b26))
* **extension:** real-world example prompts, not developer-centric ones ([6e793eb](https://github.com/Build-Fractal/conversus-oss/commit/6e793eb6b706313f512ddd9879a273f8b31caa0c))
* **gotchas:** add FastMCP prompt return type gotcha ([0dcb47f](https://github.com/Build-Fractal/conversus-oss/commit/0dcb47faa73491ac32f6efcbb8eda685c1f06829))
* **gotchas:** add MCPB prompt manifest declaration requirement ([fd2cca1](https://github.com/Build-Fractal/conversus-oss/commit/fd2cca1da3b6faf942c4c596ec076ef7c368cf8b))
* **gotchas:** add MCPB user_config title requirement ([861559d](https://github.com/Build-Fractal/conversus-oss/commit/861559d2793a893fc49aa49a3cd3889ec4f423a9))
* **governance:** commit verification deliberation artifacts + log entries ([#31](https://github.com/Build-Fractal/conversus-oss/issues/31)) ([bb6bffe](https://github.com/Build-Fractal/conversus-oss/commit/bb6bffe186dabd8caab3c745c2ce17e3eb7ae39c))
* **governance:** CONSTITUTIONAL_CONVERSATIONS.md log + first entry ([#16](https://github.com/Build-Fractal/conversus-oss/issues/16)) ([b8f40b7](https://github.com/Build-Fractal/conversus-oss/commit/b8f40b7312f422112cd8af4794c7a4b8b345b089))
* **governance:** post-v2.4.0 gap analysis artifacts + log entry ([#34](https://github.com/Build-Fractal/conversus-oss/issues/34)) ([1216402](https://github.com/Build-Fractal/conversus-oss/commit/1216402a37f961886ead0ad773e7345d2fb20c23))
* **oss-launch:** Day 2 polish — README/CONTRIBUTING rewrite + invocation sweep ([#161](https://github.com/Build-Fractal/conversus-oss/issues/161)) ([b45852c](https://github.com/Build-Fractal/conversus-oss/commit/b45852c4c4194c20490d8627ebbd5ddb490d99e7))
* **plugin:** split monolithic skill into 4 focused slash commands ([87cd8d1](https://github.com/Build-Fractal/conversus-oss/commit/87cd8d181a3debc80f94be645055a4cbbaaf4f34))
* **sdk:** stop apologizing for namespace split — explain the architecture ([#167](https://github.com/Build-Fractal/conversus-oss/issues/167)) ([81423ee](https://github.com/Build-Fractal/conversus-oss/commit/81423ee5aa625576b455d922942478d2cb597776))
* **spec-049:** provider auth audit — add claude-desktop, document openai-compat adapter pattern (closes [#62](https://github.com/Build-Fractal/conversus-oss/issues/62)) ([#88](https://github.com/Build-Fractal/conversus-oss/issues/88)) ([4813aa8](https://github.com/Build-Fractal/conversus-oss/commit/4813aa8d210d78b2ad212bb6332a4e61c72b6bf5))
* **spec-061:** annotation corrections per strip-script-061-substeps deliberation ([#114](https://github.com/Build-Fractal/conversus-oss/issues/114)) ([a718567](https://github.com/Build-Fractal/conversus-oss/commit/a718567ec5fa08cbba0c08159556ba9682a2fee8))
* **spec-067:** add §4.6 — Test-fix discipline during verification ([#47](https://github.com/Build-Fractal/conversus-oss/issues/47)) ([ee7f20a](https://github.com/Build-Fractal/conversus-oss/commit/ee7f20a27bd117addb69e49871d92e4979df04b5))
* **spec:** 065 — path to open source (launch readiness gates) ([#15](https://github.com/Build-Fractal/conversus-oss/issues/15)) ([e24416b](https://github.com/Build-Fractal/conversus-oss/commit/e24416bdec51d924fa3b1ef627736055fc09548d))
* **spec:** 066 — constitution v2.3.0 amendment package ([#17](https://github.com/Build-Fractal/conversus-oss/issues/17)) ([8dc14a8](https://github.com/Build-Fractal/conversus-oss/commit/8dc14a8e6bf1622a96645d8f37bbe2a23d7ef937))
* **spec:** 067 — verification methodology requires BOTH self-consistency AND blind ([#21](https://github.com/Build-Fractal/conversus-oss/issues/21)) ([938f4c6](https://github.com/Build-Fractal/conversus-oss/commit/938f4c63634433759b7cec069fb3aed5c3f48672))
* **spec:** 067 v2 — re-verification trigger + cost reporting (post-v2.4.0 gap) ([#35](https://github.com/Build-Fractal/conversus-oss/issues/35)) ([34b57eb](https://github.com/Build-Fractal/conversus-oss/commit/34b57ebd9106f9983f42adc2d78cd6e6f9a416d7))
* **spec:** 068 — Principle XVI determinism-scope clarification (PATCH) ([#26](https://github.com/Build-Fractal/conversus-oss/issues/26)) ([43715fc](https://github.com/Build-Fractal/conversus-oss/commit/43715fc2a2b9df85be6bd7472c58f02ab0e9bf90))
* **spec:** 069 — mechanical verification gate for constitutional inclusion (MINOR) ([#27](https://github.com/Build-Fractal/conversus-oss/issues/27)) ([a0aa68c](https://github.com/Build-Fractal/conversus-oss/commit/a0aa68c170fa35efa223612b7eabb9f27f1d5b0c))
* **spec:** 070 — audit grandfathered principles (VI, X, XVI) against v2.4.0 gate ([#36](https://github.com/Build-Fractal/conversus-oss/issues/36)) ([c055f6b](https://github.com/Build-Fractal/conversus-oss/commit/c055f6b1017d07272b31bc7dbbfe03d2ba3e2c7b))
* **spec:** 071 — Test-Fix Boundary Preservation (proposed Principle XXVIII) ([#43](https://github.com/Build-Fractal/conversus-oss/issues/43)) ([0d7ccd5](https://github.com/Build-Fractal/conversus-oss/commit/0d7ccd58f56c33f95d28fe3e2321efd8a205f473))

## [Unreleased]

### Renamed
- **MAJOR — Project renamed from `conversus` to `deliberator`** (2026-06-23, pre-first-publish). Targets: PyPI package, CLI entry point, Python foundation package (`conversus/` → `deliberator/`; `engine/` and `linter/` unchanged), GitHub repo (`Build-Fractal/conversus-oss` → `Build-Fractal/deliberator`), MCP tool names (`conversus_*` → `deliberator_*`), slash commands (`/conversus:*` → `/deliberator:*`), config filename (`conversus.yml` → `deliberator.yml`), and user dotfile dir (`~/.conversus/` → `~/.deliberator/`). Pre-rename artifacts in `deliberations/`, `specs/`, and pre-2026-06-23 CHANGELOG / CONSTITUTIONAL_CONVERSATIONS entries are preserved verbatim per audit-trail discipline. Tier 2 governance event logged as a substrate-standup carve-out (precedent: v4.2.0 bootstrap-paradox). Full rationale + scope: [RENAME.md](RENAME.md). Targeted publish version: `v1.0.0` as `deliberator`.

### Changed
- **MAJOR — v3.2.3 → v4.0.0 constitutional tier extraction**. CONSTITUTION.md restructured from a flat 28-slot constitution into a hierarchical three-tier system. 10 principles relocated to Tier 1 (Universal) at `../build-fractal/CONSTITUTION.md`; 10 to Tier 2 (Suite) at `../build-fractal/conversus/CONSTITUTION.md`. 6 retained as component-tier in this repo's `CONSTITUTION.md`. 2 retired markers (VI, X) preserved per Principle II number-stability. All prior Sync Impact Report comment blocks preserved as audit trail. Three-deliberation ratification (originating + self-consistency + blind); 12 fixes applied across spec v1 → v2 → v3. See `specs/v4.0.0-tier-extraction/spec.md`.

### Added
- `engine/tests/test_mode_provider_matrix.py`: cross-product meta-test closing the **Component-tier Principle XXVI Provisional gap**. Exercises 8 modes × {`mock`, `demo`} = 16 cells end-to-end via `run_pipeline()`, plus 13 dispatch-only provider-instantiation checks covering every other registered provider (`anthropic`, `openai`, `claude-code`, `claude-desktop`, `aider`, `opencode`, `codex`, `copilot`, `gemini`, `pi`, `ollama`, `llama-cpp`, `vllm`). Source-of-truth assertions pin the parametrize breadth to `conversus.schemas.modes.VALID_MODES` and `engine.execution.providers.PROVIDER_REGISTRY`; adding a new mode or provider without updating the matrix trips the meta-test. CONFORMANCE.md XXVI row flipped Provisional → Satisfied (closed 2026-05-11).
- `linter/tier_coherence.py`: tier-coherence linter satisfying Constitutional Inclusion Criterion 1 for v4.0.0. Checks (a) cross-tier duplication via dual-signal (identity-marker + 5-gram Jaccard >0.85) with escape-hatch exclusion list; (b) post-relocation orphans; (c) cross-reference resolution (filesystem paths AND canonical monorepo GitHub URLs per v4.0.0 erratum C1); (d) version-field consistency. Plus weakening-words flagging per spec §6.10.
- `scripts/v4-tier-extraction.py`: one-shot relocation script that produced the v4.0.0 tier split with byte-equal preservation verification. Reusable for any future tier-restructure amendment that needs byte-equality guarantees.
- `scripts/v4-url-references.py`: idempotent conversion script for the v4.0.0 erratum C1 — converts filesystem-relative cross-tier references to canonical GitHub URLs. Re-runnable when the canonical URL prefix changes (e.g., future build-fractal/ extraction to its own repo).
- `CONFORMANCE.md`: this repo's formal conformance declaration to the build-fractal/conversus suite governance contract. Status: Provisional (5 open remediations: V, XII, XXII, XXIV, XXVI). Inheritance references use canonical GitHub URLs for standalone repo usability.
- Suite admission via Q2 ADMIT-PROVISIONAL of originating deliberation 2026-05-06.

### Fixed
- **v4.0.0 erratum C1 (2026-05-08)**: cross-tier references in `CONSTITUTION.md` and `CONFORMANCE.md` were filesystem-relative paths (`../build-fractal/...`), which broke standalone repo usability — readers cloning conversus-oss alone or viewing it on github.com saw dangling references to nonexistent paths. Erratum converts all such references to canonical GitHub URLs (`https://github.com/Build-Fractal/build-fractal-mono/blob/main/...`). Single-source-of-truth model preserved; repo standalone usability restored. No principle text changed. See `specs/v4.0.0-tier-extraction/spec.md` §13 v4 fixes subsection.

## [0.4.0] - 2026-05-01

The "Principle XXVIII era" — constitutional discipline established and applied across 30+ PRs.

### Added

- **Constitution v2.5.0 — Principle XXVIII (Test-Fix Boundary Preservation)** ratified with override-with-rationale precedent (#46).
- **Operational scaffolding for XXVIII**: `.github/pull_request_template.md` with structured `test-fix-category` marker (#48), `scripts/lint-test-fixes.py` advisory CI lint with skip-discipline + diff-shape consistency checks (#49), spec 067 §4.6 binding the 4-subagent investigation pattern as canonical first response (#47).
- **Spec 047 (Duration Parser) Phases 1-4**: new `conversus/schemas/duration.py` with `Duration`, `TemporalMatch`, 5-tier parser (ISO 8601 / numeric+unit / colloquial / fiscal / category inference) covering 7 temporal categories. Replaces `_CONSTRAINT_PATTERN` regex in `linter/question_classifier.py`. Adds `extract_temporal_constraints()` API (#82).
- **Spec 061 step 7 — deepeval quality layer**: `engine/tests/test_evals.py` with 5 GEval metrics (Review Independence, Cross-Review Adversarial, Revision Responsiveness, Dispute Specificity, Synthesis Grounding) per spec §3.2.1. All `@pytest.mark.eval`, excluded from default CI (#83).
- **Anthropic-backed deepeval judge**: `_build_judge()` factory using `AnthropicModel` instead of OpenAI default (#85).
- **Claude-code-subprocess judge** (`engine.eval_judge.ClaudeCodeJudge`): closes the OAuth-user gap so the deepeval suite runs without `ANTHROPIC_API_KEY` when both `CONVERSUS_EVAL_PROVIDER` and `CONVERSUS_EVAL_JUDGE_PROVIDER` are set to `claude-code` (#89).
- **Spec 057 SC-003 — settings cascade display**: `engine/handlers.py::status_cli` now shows per-key resolution (env / project / global / default) with new `inspect_settings_cascade` API (#71).
- **Spec 057 SC-004 — per-provider credentials**: storage moves from monolithic `~/.conversus/auth.json` to per-provider `~/.conversus/credentials/{provider}.json` with lazy migration, atomic writes (`os.replace` via `.tmp`), 0o700/0o600 permissions, and per-provider file lock with 200ms timeout (#74).
- **Spec 072 — credential source display**: per-provider source attribution in `conversus status` (per-provider-file / legacy-fallback / env-var / none) via `inspect_credential_source` (#76).
- **Spec 006 Phase 2 — inter-round arbitration completion**: 7 FRs across 5 PRs (#65, #66, #67, #69, #70). Strict validation (FR-003), `arbiter/`→`arbitration/` path rename (FR-006), round-loop parity test (FR-P2-3), template variable wiring (FR-P2-5), influence-aware dispute counting (FR-P2-4), cross-round Resolution Attribution (FR-P2-6), SC-002/003/007/008 end-to-end tests (FR-P2-7), `linter/arbitration_parser.py` (issue #68).

### Changed

- **`engine.dispatch._gated_dispatch` documented**: clarifies actual concurrency semantics (asyncio.gather across agents; fail-fast via `return_exceptions=True` + sequential post-processing). Corrects the prior session's deliberation miscall (#80).
- **`conversus init` writes `.conversus/settings.yml`** (was `settings.json`). Legacy `settings.json` files are preserved on disk and content is migrated on first init (#72).
- **`OutputManager.get_arbitration_path` returns `{base}/arbitration/resolution.md`** (was `{base}/arbiter/`). All path-aware tests updated (#65).
- **`decide --model X` flag** added; threads through to `run_engine` (#52). Regression tests in #56.
- **OAuth marker regex**: drops `subscription` token from preflight to eliminate the false-positive surface (#81).

### Fixed

- **Silent-stub deliberation** when claude-code subprocess returned an error string as agent content (Bug 3a). New `FatalProviderResponseError` aborts the pipeline rather than synthesizing the error string as if it were valid output (#52).
- **claude-code provider model leak** (Bug 3b): the legacy `claude-sonnet-4-20250514` literal substituted with the provider's own default to prevent OAuth sessions hitting unreachable models (#52).
- **`find_project_root` import shadowing** in `engine/handlers.py` (PR #42, pre-0.4.0 — referenced for context).
- **Stale `prior_arbitration_path`** after `retroactive_move_to_round_1` — Round 2's context builders received a path that no longer existed. Surfaced by FR-P2-3's parity test (#66).
- **Cross-round Resolution Attribution wiring void** — template had the section + placeholders shipped, but the runtime never populated `arbitration_paths`/`arbitration_rulings`. Surfaced by FR-P2-6 (#69).
- **Test isolation gap in SC-004**: pre-existing tests patched `DEFAULT_AUTH_PATH` only; with per-provider files now active, those tests would have started reading the user's real OAuth tokens. Fixed by pinning `DEFAULT_CREDENTIALS_DIR` everywhere `DEFAULT_AUTH_PATH` was already pinned (#74).
- **Principle XI single-source-of-truth violation in CLI status**: the `status` command duplicated auth logic instead of delegating to `status_cli` handler. Refactored to delegate (#71).

### Deprecated

- **`specs/EXECUTION-ORDER.md`**: deprecated 2026-05-01. Source of truth is now `specs/STATUS.md` + `git log specs/done/` + `CONSTITUTIONAL_CONVERSATIONS.md`. File preserved as historical artifact (#90).

### Specs closed in 0.4.0

`006`, `057`, `064`, `071`, `072`. Plus 4 reopened/promoted specs added to the active list (`047`, `048`, `056`, `059`) and 7 specs still in active development as of release.

### Verification trail

- **2 conversus deliberations** run during the session: session-review meta-review (verdict: ACCEPTED WITH RECOMMENDATIONS); SC-004 strategy review (verdict: SHIP WITH MODIFICATIONS, all applied).
- **6 production bugs caught by Principle XXVIII discipline** across the 30+ PRs: stale path (#66), wiring void (#69), test isolation gap (#74), Principle XI violation (#71), GEval lazy-init (#83), intrinsic keyword detection (#82), regex-greedy-newline edge case (#70).

### Cross-refs

- `CONSTITUTION.md` v2.5.0 (with override-with-rationale paragraph in SIR)
- `CONSTITUTIONAL_CONVERSATIONS.md` 2026-04-29 entry (governance log of the override)
- `deliberations/071-self-consistency-2026-04-28/`, `deliberations/071-blind-2026-04-28/`, `deliberations/071-blind-v2-2026-04-29/` (XXVIII verification trail)
- `deliberations/session-review-2026-04-29/`, `deliberations/057-sc4-migration-strategy-2026-04-30/`, `deliberations/070-spec-review-2026-04-28/` (other deliberations referenced)

## [0.3.0] and earlier

Pre-0.4.0 history is in git log. Notable closures: spec 042 (12 execution providers), spec 052 (open-source extraction), spec 054 (public documentation), spec 055 (capability registry), spec 064 (capability discovery), spec 066 (constitution v2.3.0), spec 069 (mechanical verification gate / Constitutional Inclusion Criteria gate, v2.4.0).
