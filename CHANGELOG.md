# Changelog

All notable changes to ClawDoc are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
ClawDoc adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [v1.7.2] — 2026-06-21

### Added
- **Tracked OpenClaw bumped 2026.6.8 → 2026.6.9.** Full sync of the 2026.6.9 doc surface.
- **33 new reference docs** under `openclaw-plugins/references/` (24 per-provider plugin stubs), `openclaw-providers/references/` (`gmi`, `qwen-oauth`), `openclaw-platforms/references/ios`, `openclaw-gateway/references/{pairing,security/audit-checks}`, `openclaw-concepts/references/{date-time,refactor/database-first}`, and `openclaw-reference/references/{code-mode,prompt-caching}`.
- New external surfaces documented: Zalo ClawBot (`zaloclawbot.md`), GitHub Copilot plugin (`copilot.md`), per-provider plugin registry (24 files under `plugins/reference/`), Codex Harness plugin (`codex.md` under `plugins/reference/`), OpenTelemetry plugin diagnostics (`diagnostics-otel.md`), QA Lab plugin (`qa-lab.md`).

### Changed
- **102 reference docs updated** to match OpenClaw 2026.6.9 content, across providers (24), tools (12), concepts (12), plugins (12), reference (11), gateway (11), cli (11), channels (6), platforms (3), nodes (2), help (2), automation (2).
- Headline behavior updates: richer Telegram delivery (Group bot identity, `includeGroupHistoryContext`), agent recovery (retries, terminal outcomes, usage after compaction), Codex integration (GPT-5.3 Spark OAuth, automatic plugin approvals, remote-node `exec` as a dynamic tool), slimmer distribution (provider plugins ship as standalone npm releases, external channel plugins load at Gateway startup), Control UI (session workspace rail, extension health), iOS Watch controls, Android chat context, Codex Hosted Search, Firecrawl keyless `web_fetch`, transcript-hygiene incomplete-reasoning-only-turns rule, secrets audit improvements.

### Notes
- Reference doc count: 584 → 619. Skills and examples unchanged.
- This is the full 2026.6.9 sync per the `clawdoc-update` pipeline; no deferred items remain.

## [v1.7.1] — 2026-06-21

### Added
- **New ref doc:** `skills/openclaw-channels/references/zaloclawbot.md` — Zalo ClawBot channel setup through the external `@zalo-platforms/openclaw-zaloclawbot` plugin (QR-code login, owner-bound private bot, Zalo Bot Platform APIs).
- **New ref doc:** `skills/openclaw-plugins/references/cohere-plugin.md` — Cohere provider plugin distribution and surface.

### Changed
- `tracked_openclaw` bumped from `2026.6.8` to `2026.6.9`.
- `skills/openclaw-channels/references/telegram.md` — added "Group bot identity" section: explicit mention of the configured bot handle addresses the selected OpenClaw agent, even when the agent persona name differs from the Telegram username.
- `skills/openclaw-tools/references/firecrawl.md` — added "Keyless Firecrawl `web_fetch`" section: explicitly-selected Firecrawl web_fetch fallback supports starter access without an API key; auto-detection still requires a configured `FIRECRAWL_API_KEY`.
- `skills/openclaw-reference/references/transcript-hygiene.md` — added "Global rule: incomplete reasoning-only turns" section: assistant turns that hit the provider output limit with only thinking/redacted-thinking content are omitted from the in-memory replay copy. Stored transcripts are not rewritten.

### Notes
- This release is a focused sync against OpenClaw 2026.6.9. It captures the new user-facing surfaces (Zalo ClawBot, Cohere externalized plugin, keyless Firecrawl, the Group bot identity rule, the new transcript-hygiene rule) and skips the 100+ small provider-doc upstream tweaks (those are content-preserving and re-checked in the next full sync).
- Audit chain: 9/9 validators clean (0 HIGH, 6 MEDIUM all verified by design per the audit notes). Pre-Flight checks all PASS.
- Manifest file_counts: skills 24 (unchanged), reference_docs 586 (+2 vs v1.7.0's 584), examples 24 (unchanged).

## [v1.6.27] — 2026-06-18

### Fixed
- Public-language scan on CHANGELOG.md v1.6.25 entry (after-the-fact cleanup — no public impact)

## [v1.7.0] — 2026-06-18

### Added
- **New skill:** `openclaw-prose` — OpenProse workflow language (`/prose` slash command, `.prose` files, multi-agent orchestration). 1 SKILL.md + 6 ref docs.
- **6 new ref docs:**
  - `skills/openclaw-channels/references/sms.md` — Twilio SMS channel setup, webhooks, allowlists
  - `skills/openclaw-channels/references/wechat.md` — Tencent iLink Bot (openclaw-weixin) channel
  - `skills/openclaw-providers/references/cohere.md` — Cohere provider, default model `cohere/command-a-03-2025`
  - `skills/openclaw-plugins/references/codex-supervisor.md` — Codex app-server supervisor plugin
  - `skills/openclaw-tools/references/x-search.md` — X (Twitter) search tool
  - `skills/openclaw-tools/references/goal.md` — session goal state machine + tools
- **12 new examples:**
  - 9 channel examples (SMS, WeChat, iMessage-native, Signal, Slack, Matrix, Teams, WhatsApp, Zalo)
  - 3 platform examples (Skill Workshop, codex-harness, production-deploy)
- **6 new internal validators** (workspace-only, not shipped):
  - `doc_index_builder.py` — builds CLAWDOC_DOC_INDEX.json with per-doc lifecycle metadata
  - `upstream_drift_detector.py` — drift distribution + cross-tab
  - `routing_coverage_validator.py` — per-skill coverage + cross-references
  - `doc_lifecycle_linter.py` — active docs that mention removed behavior
  - `example_runtime_validator.py` — JSON validity + secret scan + channel coverage
  - `duplicate_doc_detector.py` — same-H1 and same-snippet duplicates

### Changed
- `openclaw-master/SKILL.md` Skill map table now covers all 24 routable skills (was 10); description lists all 24 skills for routing
- `openclaw-tools/SKILL.md` description: added 7 Skill Workshop triggers (skill workshop, skill_workshop, workshop, approve skill, propose skill, skill proposal, quarantine skill)
- `openclaw-concepts/SKILL.md` description: added 9 latent triggers (presence, OpenClaw SDK, OAuth flows)
- `openclaw-troubleshooting/SKILL.md` description: tightened (removed generic "not working", "failed", "issue", "error" triggers; kept domain-specific)
- `openclaw-plugins/SKILL.md` description: added ClawHub vocabulary (clawhub CLI, publish, registry)
- `openclaw-providers/SKILL.md`: 50+ → 62 (matches canonical count)
- `bluebubbles.md` converted to "Coming from BlueBubbles" migration-from guide (was a setup guide)
- `wizard.md`: BlueBubbles marked removed; iMessage promoted
- `automation/references/logging.md` → 1-line pointer to `openclaw-logging/references/logging.md`
- `README.md`: badges bumped (24 skills, 584 refs, 24 examples); 12 new examples added to the table; `openclaw-prose` added to skill tree
- `assets/clawdoc-banner.png` restored + HTML overlay added with v1.7.0 stats

### Fixed
- **Master skill routing gap:** 12 of 22 skills were not in (now 24 after openclaw-clawhub also added) `openclaw-master`'s skill map. Fixed.
- **Latent trigger-keyword gaps:** presence, OpenClaw SDK, OAuth-in-concepts were body content but no triggers. Fixed.
- **Provider count inconsistency:** `50+` vs `43+` vs `60+` across files. Standardized to 62.
- **Logging duplication:** 3 skills had their own `logging.md`. Consolidated to canonical + 2 pointers.
- **OpenProse trigger blind spot:** "skill workshop" wasn't in `openclaw-tools` triggers. Added.

### Notes
- No new OpenClaw sync. v2026.6.8 is still the current stable upstream.
- Reference doc count: 542 → 584 (+42 net: 6 H5 + 12 config + 16 macOS + 6 openclaw-prose + 2 openclaw-clawhub).
- Skill count: 22 → 24 (added openclaw-prose and openclaw-clawhub).
- Example count: 12 → 24 (12 new examples).
- All audit checks pass clean: routing, claim, metadata, validate_repo, safety_scanner, doc_index_builder + 5 new validators.
- Pre-Release Power Release Gate (8 stages) passed; VERDICT.md filed in `audit-output/v1.7.0-pre-release/`.

## [v1.6.26] — 2026-06-18

### Fixed
- **BlueBubbles / iMessage recommendation inversion** (3 docs disagreed; user-facing bug). Our own `imessage.md` already documented the BlueBubbles removal, but `channel-index.md` and `references/wizard.md` still recommended BlueBubbles, and `bluebubbles.md` was framed as a setup guide rather than a migration-from guide.
  - `skills/openclaw-channels/references/channel-index.md` — BlueBubbles moved to a "Removed channels (migration-only)" section; iMessage promoted to "Recommended for iMessage"
  - `skills/openclaw-channels/references/bluebubbles.md` — converted to a "Coming from BlueBubbles" migration-from guide with a config-translation table (channels.bluebubbles.\* → channels.imessage.\*) and step-by-step cutover
  - `skills/openclaw-reference/references/wizard.md` — channel list and provider-list fixed to recommend iMessage, mark BlueBubbles as removed

### Notes
- No new reference docs, no OpenClaw sync. Reference doc count remains 542; tracked OpenClaw version remains 2026.6.8.
- This is a hotfix ahead of v1.7.0 (Content Freshness + Drift Prevention); v1.6.26 + v1.7.0 form the two-step path the audit (2026-06-18) recommended.

## [v1.6.25] — 2026-06-18

### Added
- `CHANGELOG.md` — first curated changelog file (Keep-a-Changelog format)
- README "Scope" section — explicit fences for what ClawDoc does and does not do
- README "How ClawDoc routes requests" diagram — Mermaid flow showing how `openclaw-master` routes questions to area skills and reference docs

### Changed
- `SOUL.md` expanded with operating posture, routing flow, and scope fences; routing and citation discipline now part of the public persona
- Install guides (`AGENT_INSTALL.md`, `SKILLS_INSTALL.md`), `QUICKSTART.md`, and `agent-template/README.md` updated to match the release version

### Notes
- No `tracked_openclaw_version` change — still 2026.6.8 (no OpenClaw sync in this release)

## [v1.6.24] — 2026-06-18

### Changed
- Audit polish: 12 documentation issues fixed across the skill tree, manifest, scanner, and install guides
- 3 broken reference doc links fixed (in `openclaw-cli/SKILL.md`, `openclaw-nodes/SKILL.md`, `openclaw-providers/SKILL.md`)
- 3 example configs updated to the current default model (`install-verify.json`, `memory-builtin.json`, `multi-agent-discord.json`)
- Manifest: added `IDENTITY.md`, `USER.md`, `TOOLS.md` to the public `allowed_paths` list in `CLAWDOC_MANIFEST.json`
- Scanner: `scripts/safety_scanner.py` allow-list now includes the three root template files
- README: provider count updated to match actual (`50+` → `60+`), new Contents section, link to `examples/README.md`, reworded channels line
- Install guides (`AGENT_INSTALL.md`, `SKILLS_INSTALL.md`): added "Try an example" block with `openclaw config merge` command

## [v1.6.23] — 2026-06-17

### Changed
- Description trim pass across skill frontmatter
- Added `examples/README.md` documenting all 12 ready-to-use configs

## [v1.6.22] — 2026-06-17

### Fixed
- Corrected stale `reproducible_count` in `CLAWDOC_MANIFEST.json` (542, was 536)

### Added
- 2 new reference docs: `openclaw-tools/parallel-search`, `openclaw-tools/skill-workshop`
- 23 reference docs updated across `plugins/` and `tools/`

## [v1.6.21] — 2026-06-17

### Fixed
- Install guides and agent-template version metadata updated in lockstep with the OpenClaw 2026.6.8 sync

### Added
- 28 modified reference docs applied, 4 new docs added (25 docs deferred to v1.6.22)

## [v1.6.20] — 2026-06-16

### Fixed
- Closed 4 routing gaps
- Removed stale pre-commit test file

## [v1.6.19] — 2026-06-15

### Fixed
- Caught and corrected metadata drift from v1.6.18

## [v1.6.18] — 2026-06-15

### Fixed
- Corrected stale content claims in README + agent-template

## [v1.6.17] — 2026-06-15

### Fixed
- Public metadata sync: bumped to v1.6.16 / 2026.6.6 / 535 docs

## [v1.6.16] — 2026-06-15

### Changed
- Structural cleanup: deduplication, routing dead-zone elimination, YAML validation across the skill tree

## [v1.6.15] — 2026-06-15

### Changed
- Skill routing maintenance pass — closed 30 routing gaps in skill descriptions across 8 `SKILL.md` files
- Tracked OpenClaw version bump: 2026.5.26 → 2026.6.6 (no doc changes in this OpenClaw release)

### Fixed
- Reference doc count corrected to 561 in `CLAWDOC_MANIFEST.json` and the `README.md` badge (now includes `railway.mdx`; manifest and README count had not been updated since v1.6.14)

## [v1.6.14] — 2026-05-27

### Added
- Processed all 4 deferred areas from the v2026.5.26 sync: `cli` (14), `gateway` (18 new), `plugins` (12+3), `tools` (11+1)
- 55 references applied, 3 deferred (plugins: `codex-harness-reference`, `codex-harness`, `sdk-subpaths`)

## [v1.6.13] — 2026-05-27

### Added
- OpenClaw v2026.5.26 sync: 5 new reference docs, 43 modified (4 areas deferred to v1.6.14)

## [v1.6.12] — 2026-05-24

### Added
- OpenClaw v2026.5.22 sync: 3 new reference docs, 29 modified (6 areas deferred to v1.6.13)

## [v1.6.11] — 2026-05-22

### Changed
- Skill routing audit: added missing trigger keywords

## [v1.6.10] — 2026-05-22

### Added
- OpenClaw v2026.5.20 sync: 2 new reference docs, 27 modified (1 deferred)

## [v1.6.9] — 2026-05-21

### Added
- OpenClaw v2026.5.19 sync: 58 modified reference docs (1 deferred — `install/podman`, no matching skill ref)

## [v1.6.8] — 2026-05-19

### Changed
- Version bump and asset refresh

## [v1.6.7] — 2026-05-19

### Fixed
- `clawdoc_version` corrected from `v1.6.6b` to `v1.6.7` (the previous version string was not valid SemVer)

## [v1.6.6] — 2026-05-19

### Added
- OpenClaw v2026.5.18 sync (final batch): 8 remaining deferred reference docs applied (channels, concepts, config, cli)

## [v1.6.5] — 2026-05-19

### Added
- OpenClaw v2026.5.18 sync (main batch): 70 modified reference docs applied

## [v1.6.4] — 2026-05-19

### Added
- OpenClaw v2026.5.18 sync (safe batch): 3 modified reference docs applied

## [v1.6.3] — 2026-05-19

### Changed
- `tracked_openclaw_version` → 2026.5.18; `ref_docs` → 523 in `CLAWDOC_MANIFEST.json`

## [v1.6.2] — 2026-05-15

### Fixed
- `README.md` reference doc count badge synced to 520
- Linked 3 orphan install reference docs from `SKILL.md` descriptions

## [v1.6.1] — 2026-05-15

### Changed
- Maintainer hardening: agent-facing docs policy added

## [v1.6.0] — 2026-05-08

### Added
- Dual install modes: persistent-agent (Mode 1) and skills-only (Mode 2)
- `AGENT_INSTALL.md` — Mode 1 install guide
- `SKILLS_INSTALL.md` — Mode 2 install guide
- Public `agent-template/` containing `SOUL.md`, `AGENTS.md`, `README.md` for new agents
- `CLAWDOC_MANIFEST.json` — machine-readable repo contents
- `scripts/validate_repo.py` — repo integrity validator
- `scripts/safety_scanner.py` — public/private workspace boundary scanner
- `.github/workflows/validate.yml` — CI for both validators

### Fixed
- Reference docs count corrected from stale 508 → 487 (now includes `.mdx` files)

## [v1.5.x and earlier] — 2026-04 to 2026-05

Rapid iteration period: 28 releases from v1.0 through v1.5.14 covering:

- Initial release (11 skills, 90 files)
- Skills expansion to 22 routable skills
- Reference doc growth from 90 → 487+
- `SKILL.md` restructuring with trigger keywords
- Multiple OpenClaw upstream version syncs (2026.4.x → 2026.5.x)
- Quickstart guide, examples expansion (4 → 12)
- Onboarding skill (`clawdoc-onboarding`)
- Install reference docs and platform guides

For the full release-by-release history, see [GitHub Releases](https://github.com/Hashi-Ai-Dev/openclaw-clawdoc/releases).