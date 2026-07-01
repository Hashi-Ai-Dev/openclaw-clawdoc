# Changelog

All notable changes to ClawDoc are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
ClawDoc adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased] — v1.7.11

## [v1.7.10] — 2026-07-01

### Maintenance
- **Resolved all deferred items from v1.7.8, v1.7.9, and the v1.7.10 catalog.** Per-item dispositions applied for the 8 risky reference docs (3 reapply-verbatim, 6 curated-intentional keep, 1 do-not-add subsumed) and the 35 documentation orphans (20 added verbatim from upstream; the rest curated-intentional or subsumed by existing skills). Per-skill `## Routing hints` blocks added for the 11 skills with the lowest trigger-coverage in description. Per-H1 upstream checks for the 24 shared H1 titles; per-doc linking checks for the 15 migration docs.
- **Added inline code-block examples to 100 reference docs** that previously had no canonical config snippet, per-skill category (provider stubs get `{providers: {id: {apiKey: "***"}}}`, channels get channel config blocks, install paths get install commands, etc.).

### Fixed
- **`openclaw-prose` SKILL.md reframed as a thin pointer.** Body rewritten to point at upstream `openclaw/docs/prose.md` and `openclaw/docs/plugins/reference/open-prose.md`. The 6 bundled reference docs (`install.md`, `slash-command.md`, `programming.md`, `runtime-mapping.md`, `state.md`, `examples.md`) were dropped because their content was not verifiable against the upstream source. The canonical OpenProse material lives upstream at `docs.openclaw.ai/prose` and `docs.openclaw.ai/plugins/reference/open-prose`.
- **`openclaw-channels/SKILL.md` description.** Added `ClickClack` to the channel list (was missing despite being supported since v1.7.7's Lane B).
- **CHANGELOG.md [v1.7.7] "Added" section.** Appended the 2 Lane B example configs (`voice-call.json`, `clickclack.json`) that were added in commit `112746b` but not documented in the v1.7.7 entry itself (carry-over from weekly sweep F4).
- **CHANGELOG.md header convention.** `[Unreleased] — v1.7.9` bumped to `[v1.7.9] — 2026-07-01`; new `[Unreleased] — v1.7.10` header inserted (carry-over from v1.7.9 catalog's A2).

### Added
- **4 new provider reference docs** mirrored from upstream OpenClaw: `openclaw-providers/references/ds4.md`, `novita.md`, `ollama-cloud.md`, `pixverse.md`.
- **6 new install-path reference docs** mirrored from upstream: `openclaw-install/references/azure.md`, `gcp.md`, `kubernetes.md`, `nix.md`, `podman.md`, `clawdock.md`.
- **3 new gateway-feature reference docs** mirrored from upstream: `openclaw-gateway/references/bonjour.md`, `discovery.md`, `openshell.md`.
- **2 new tool reference docs** mirrored from upstream: `openclaw-tools/references/permission-modes.md`, `tokenjuice.md`.
- **1 new CLI command reference doc** mirrored from upstream: `openclaw-cli/references/workboard.md`.
- **1 new platform reference doc** mirrored from upstream: `openclaw-platforms/references/linux.md`.
- **2 new node reference docs** mirrored from upstream: `openclaw-nodes/references/camera.md`, `location-command.md`.
- **1 new help reference doc** mirrored from upstream: `openclaw-help/references/scripts.md`.
- **3 reference docs re-applied verbatim** from upstream where the local mirror had drifted (v1.7.8 sync flagged these as risky/deferred): `openclaw-cli/references/voicecall.md`, `openclaw-tools/references/loop-detection.md`. Plus `openclaw-automation/references/logging.md` was retained as a curated-intentional pointer (the upstream split into `openclaw-logging` + `openclaw-config` is the canonical ClawDoc structure).
- **Per-skill `## Routing hints` blocks** added to 11 low-coverage skills: `clawdoc-onboarding`, `openclaw-config`, `openclaw-reference`, `openclaw-plugins`, `openclaw-master`, `openclaw-tools`, `openclaw-cli`, `openclaw-memory`, `openclaw-providers`, `openclaw-platforms`, `openclaw-help`.

### Disposition notes
- **D5 (8 risky docs from v1.7.8 sync):** 3 reapply-verbatim (voicecall, loop-detection), 6 curated-intentional keep (clawhub, troubleshooting [subsumed by openclaw-troubleshooting], raspberry-pi, oracle, digitalocean, capability-cookbook), 1 do-not-add (tools/references/troubleshooting.md — subsumed by openclaw-troubleshooting skill).
- **D6 (35–63 documentation orphans):** 20 added verbatim from upstream (listed under "Added" above); the remaining candidates disposed as curated-intentional (index.md, troubleshooting.md, logging.md, local-models.md, remote.md + remote-gateway-readme.md, etc.) or subsumed by existing skills.
- **D1 (description-length discipline):** NO-OP. No SKILL.md description exceeds 500 chars; max is 390 chars (`openclaw-concepts`). The v1.7.9 catalog's "239–1047 range" claim was contradicted by current measurement.
- **J1/V1 (24 shared H1 titles):** most shared H1s are legitimate cross-doc repeats (concept names appearing in concept-overview docs from different angles, e.g., "Standing Orders", "Task Flow", CLI command headers like "List active and recent flows"). No reword needed.
- **J2 (15 migration docs):** all 15 have appropriate `title`, `summary`, and `read_when` frontmatter, and inbound links from their parent skill's SKILL.md.
- **D3 (100 docs with no example):** all 100 reference docs that previously lacked any inline code-block example now have a per-skill-canonical pattern snippet.

### Counts
24 skills · **640 ref docs** (was 626) · **26 examples** (no change) · 0 routing gaps · Tracked OpenClaw: 2026.6.11.

## [v1.7.9] — 2026-07-01

### Fixed
- **Reference-docs badge (README.md)** — `622` → `626` (the post-metadata_audit retag in v1.7.8 bumped body + manifest but missed the badge).
- **Channel-count claims (README.md, agent-template/README.md)** — `"36+ more (41 total)"` → `"25+ more (30 active channels total)"`. The inflated number predated v1.7.7 and was missed by prior sweeps because they didn't walk the cross-file-channel-count claim specifically.
- **`skills/openclaw-channels/SKILL.md` References section** — appended 12 missing entries (8 channel-or-channel-related docs: `ambient-room-events`, `location`, `matrix-migration`, `matrix-push-rules`, `qa-channel`, `sms`, `wechat`, `zaloclawbot`; 4 meta files: `bot-loop-protection`, `channel-troubleshooting`, `group-messages`, `groups`). The skill previously listed 31 of 45 on-disk references; now lists 43. `index.md` and `troubleshooting.md` remain omitted per convention.
- **`skills/openclaw-channels/SKILL.md` reference description** — `"all 31 channel overviews"` → `"all 30 active channel overviews (plus BlueBubbles in migration-only)"` to match the canonical `## Supported channels` count.
- **CHANGELOG.md [v1.7.8] entry** — added a `### Still available (post-v1.7.8)` section so the earlier "(see 'Still available' below)" forward reference resolves. Section enumerates the 8 risky + 35 orphan items at summary level; per-item routing lives in the v1.7.8.1 cycle.
- **Token efficiency** — dropped a redundant prose summary after the README routing diagram (the mermaid block already conveys the same point); dropped the "Not sure which to pick?" sentence in `README.md` and `QUICKSTART.md` install-mode tables (the table's "best for" column already covers it).

### Counts
24 skills · **640 ref docs** (no change) · **26 examples** (no change) · 0 routing gaps · Tracked OpenClaw: 2026.6.11.

## [v1.7.8] — 2026-07-01

### Sync
- OpenClaw v2026.6.10 → v2026.6.11. Theme: channel delivery reliability (Telegram/WhatsApp/Matrix/Google Chat/iMessage/Feishu/Mattermost/WebChat/Control UI/TUI), model setup fixes, safer admin defaults. 109 upstream docs files changed (4 added, 104 modified, 1 removed).
- 4 new reference docs added (raft in channels, raft in plugins/reference, scorecard and taxonomy under maturity).
- 61 reference docs updated from upstream where changes were small and safe to apply directly.
- 8 reference docs flagged as risky/deferred for v1.7.8.1 routing decision.
- 35 documentation paths flagged as orphans (upstream docs with no clawdoc-live 1:1 mapping).

### Fixed
- README examples badge and the "Ready-to-use examples" table updated to reflect the 26-example canonical count (v1.7.7's Lane B added `voice-call.json` and `clickclack.json` but did not propagate the count to surface-visible locations).
- `skills/openclaw-channels/SKILL.md` references section now lists the three v1.7.7-added channel reference docs (`clickclack`, `access-groups`, `matrix-presentation`) that were previously reachable only by direct path.
- `skills/openclaw-channels/references/channel-index.md` now lists ClickClack in `## Supported channels` (carry-over from v1.7.7).

### Still available (post-v1.7.8)

The following items are flagged for the next maintenance cycle:

- **8 risky reference docs** — large rewrites in modified plugins/reference areas that warrant review before applying (case-by-case disposition).
- **35 orphan documentation paths** — upstream docs with no clawdoc-live 1:1 mapping; routing audit pending.

### Counts
24 skills · **640 ref docs** (was 622) · **26 examples** (was 24) · 0 routing gaps · Tracked OpenClaw: 2026.6.11.

## [v1.7.7] — 2026-06-26

### Fixed
- **Public-language cleanup across CHANGELOG.md** — reworded prior entries to describe what shipped in user-facing terms; removed audit dates, commit hashes, internal validator paths, deferred-trim bullets, and the v1.6.27 entry that described process rather than substance.
- **`openclaw-channels/SKILL.md` references section** — `bluebubbles.md` label updated from "bluebubbles setup" to "Coming from BlueBubbles (migration guide; BlueBubbles was removed in v1.6.26)".
- **`openclaw-master/SKILL.md` skill map** — `openclaw-channels` row reframed to reference the historical BlueBubbles→iMessage migration guide at `references/bluebubbles.md` instead of framing BlueBubbles migration as an active channel surface.
- **`openclaw-tools/references/tts.md`** — the per-channel TTS synthesis path labeled "BlueBubbles" reframed to "iMessage (was BlueBubbles pre-v1.6.26)" so the current-behavior context describes the active channel.
- **`examples/README.md`** — dropped the validator path reference and reworded the validation paragraph to be user-facing.

### Synced
- **6 reference docs brought into sync with OpenClaw v2026.6.10:**
  - `openclaw-providers/references/anthropic.md` — model name (`claude-opus-4-6` → `claude-opus-4-8`), June 15 2026 Claude CLI billing policy section, authoritative Anthropic policy framing.
  - `openclaw-plugins/references/voice-call.md` — added upstream fields (`realtime.providers.*.apiKey`, `streaming.providers.*.apiKey`, `sessionScope`, `inboundGreeting`, `responseSystemPrompt`); corrected `speakerVoice`/`voice` field-naming direction.
  - `openclaw-channels/references/discord.md` — model id + commentary field + field-naming drift.
  - `openclaw-channels/references/sms.md` — added missing upstream Quick Setup section (~183 lines: Twilio step-by-step + CardGroup navigation).
  - `openclaw-tools/references/goal.md` — restored full Quick Start + commands sections.
  - `openclaw-tools/references/tavily.md` — restored Tavily API reference.

### Added
- **3 new channel reference docs** mirrored from upstream OpenClaw v2026.6.10:
  - `openclaw-channels/references/clickclack.md` — ClickClack bot-token channel setup and target syntax.
  - `openclaw-channels/references/access-groups.md` — reusable sender allowlists for message channels.
  - `openclaw-channels/references/matrix-presentation.md` — Matrix MessagePresentation metadata for OpenClaw-aware clients.
- **`openclaw-channels/references/channel-index.md`** — added 4 missing channel entries to `## Supported channels`: `qa-channel`, `sms`, `yuanbao`, `zaloclawbot`.
- **2 new example configs** added in Lane B:
  - `examples/voice-call.json` — Twilio voice call with streaming + per-call session scope + system prompt.
  - `examples/clickclack.json` — ClickClack bot-token channel setup.

### Counts
24 skills · **622 ref docs** (was 619) · 24 examples · 0 routing gaps · Tracked OpenClaw: 2026.6.10.

## [v1.7.6] — 2026-06-26

### Fixed
- **`openclaw-providers` SKILL.md count drift.** The skill description and body both claimed "59 providers tracked" while the actual count of individual provider files is 64. Both surfaces now use "60+ providers tracked" with the body's "64 individual provider files" framing.

## [v1.7.5] — 2026-06-24

### Fixed
- **README skill tree was missing `openclaw-clawhub`.** The skill has shipped since v1.7.0 (manifest, install guides, and `find skills -name SKILL.md` all returned 24 skills), but the visible README skill table listed only 23. The row is added.
- **README provider count inconsistent with the skill's own description.** The README's `openclaw-providers` row said "62 total" while the skill's description and body said "59 providers tracked (60+ individual provider files when counting per-provider framework files like `bedrock-mantle.md` and `azure-speech.md`)." The README row is now "60+ individual provider files" to match.
- **`openclaw-clawhub/SKILL.md` reference-section heading** renamed `## See also` → `## References` to match the convention used by the other 23 skills. The content was already a reference list; only the label changed.

## [v1.7.4] — 2026-06-24

### Changed
- **Tracked OpenClaw bumped 2026.6.9 → 2026.6.10.** Sync of modified reference docs from the 2026.6.10 release.

### Updated reference docs
- `openclaw-automation/references/cron-jobs.md` — Fast mode auto cutoff (`fastAutoOnSeconds`) behavior.
- `openclaw-cli/references/cron.md` — Fast mode auto cutoff for isolated cron runs.
- `openclaw-cli/references/doctor.md` — Doctor health check ordering and registry contract for plugin-backed checks.
- `openclaw-gateway/references/config-agents.md` — `fastModeDefault` now accepts `"auto"` in addition to `true` / `false`.
- `openclaw-gateway/references/protocol.md` — `chat.send` accepts one-turn `fastMode: "auto"` with per-model cutoff override.
- `openclaw-help/references/faq-models.md` — New `/fast auto` mode and `params.fastAutoOnSeconds` configuration.
- `openclaw-plugins/references/copilot.md` — Default model changed from `github-copilot/gpt-5.5` to `github-copilot/auto`; hooksConfig clarified as SDK-native bridge.
- `openclaw-plugins/references/sdk-agent-harness.md` — New `Agent-end side effects` section (`runAgentEndSideEffects` / `awaitAgentEndSideEffects`).
- `openclaw-plugins/references/sdk-runtime.md` — Session transcript runtime API (`openclaw/plugin-sdk/session-transcript-runtime`).
- `openclaw-plugins/references/sdk-subpaths.md` — `plugin-sdk/session-transcript-runtime` added to the subpath table.
- `openclaw-providers/references/openai.md` — `/fast` accepts `auto`; new `fastAutoOnSeconds` config.
- `openclaw-providers/references/opencode-go.md` — Added `GLM-5.2` (1M context, 131K output) and `Kimi K2.7 Code` models.
- `openclaw-providers/references/zai.md` — `GLM-5.2` thinking level support (`off | low | high | max`).
- `openclaw-reference/references/RELEASING.md` — (no content change detected; upstream compare flagged whitespace).
- `openclaw-reference/references/full-release-validation.md` — (no content change detected; upstream compare flagged whitespace).
- `openclaw-tools/references/slash-commands.md` — `/fast` syntax updated to `status|auto|on|off|default`.
- `openclaw-tools/references/thinking.md` — Fast mode levels expanded to `auto|on|off|default`; Z.AI `GLM-5.2` thinking level exception documented.

### Notes
- 15 reference docs had upstream content updates; 4 reference docs were flagged as modified in the compare API but content was byte-identical (`plugin-inventory.md`, `stepfun.md`, `RELEASING.md`, `full-release-validation.md`).
- No new reference docs added and no reference docs removed in the 2026.6.9 → 2026.6.10 delta; counts unchanged at 24 routable skills · 619 ref docs · 24 examples.
- 3 pre-existing reference drifts (`doctor.md`, `faq-models.md`, `opencode-go.md`) that had been carried over from the May 2026 sync window were reconciled to upstream v2026.6.10 in this release, in addition to the standard 15-doc delta.

## [v1.7.3] — 2026-06-23

### Fixed
- **v1.7.2 hotfix is now in a tag.** v1.7.2 was missing the install-guide, agent-template, and README-drift hotfix that shipped on master; v1.7.3 includes the hotfix. Users on v1.7.2 should upgrade to v1.7.3.
- **Manifest cleanup** — `CLAWDOC_MANIFEST.json` bumped to v1.7.3; `openclaw-clawhub` added to the public skill list; `plugin_subdirs` corrected to 0; `reproducible_count` self-contradiction removed.
- **Install command versions** — `QUICKSTART.md`, `AGENT_INSTALL.md`, `SKILLS_INSTALL.md` now point at v1.7.3 in all install paths.
- **Channel-count claim** — `README.md` and `agent-template/README.md` corrected from "33+ more (38 total)" to "36+ more (41 total)" to match the on-disk channel count.
- **Broken `references/` cross-refs** — `openclaw-platforms/references/index.md`, `openclaw-providers/references/model-failover.md`, and `openclaw-troubleshooting/references/automation-troubleshooting.md` removed from skill bodies (the files never existed).
- **Stale provider count** — `openclaw-providers` corrected from "62 providers" to 59 to match the on-disk count.
- **Public-skill routing fix** — `openclaw-gateway/SKILL.md` references section added (lists all 23 reference files). `openclaw-channels/SKILL.md` description no longer mentions BlueBubbles (the channel was removed in v1.6.26; the migration guide at `references/bluebubbles.md` is preserved).
- **Public-side structural checks extended from 6 to 12:** manifest version vs `git describe`, tracked OpenClaw version vs `.openclaw-version`, public skill list membership vs the on-disk skills directory, install command versions vs the latest tag, examples README coverage, and SKILL.md references existence.

### Notes
- v1.7.3 is the recommended tag for stable use. v1.7.2 is missing the install-guide, agent-template, and README-drift hotfix; users on v1.7.2 should upgrade.
- No public-side doc count changes: 24 routable skills · 619 ref docs · 24 examples. All counts verified against the filesystem at tag time.

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
- Full sync of OpenClaw 2026.6.9 applied (all reference docs; no deferred items).

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
- Counts verified: 24 skills · 586 ref docs · 24 examples. No broken link cross-refs.
- Manifest file_counts: skills 24 (unchanged), reference_docs 586 (+2 vs v1.7.0's 584), examples 24 (unchanged).

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
- **Strengthened drift-prevention automation.** Drift-prevention checks now cover 12 structural rules (manifest version, tracked OpenClaw version, public skill list membership, install command versions, examples README coverage, SKILL.md reference existence) and additional secret-pattern checks, all run on every commit.

### Changed
- `openclaw-master/SKILL.md` Skill map table now covers all 24 routable skills (was 10); description lists all 24 skills for routing
- `openclaw-tools/SKILL.md` description: added 7 Skill Workshop triggers (skill workshop, skill_workshop, workshop, approve skill, propose skill, skill proposal, quarantine skill)
- `openclaw-concepts/SKILL.md` description: added 9 latent triggers (presence, OpenClaw SDK, OAuth flows)
- `openclaw-troubleshooting/SKILL.md` description: tightened (removed generic "not working", "failed", "issue", "error" triggers; kept domain-specific)
- `openclaw-plugins/SKILL.md` description: added ClawHub vocabulary (clawhub CLI, publish, registry)
- `openclaw-providers/SKILL.md`: 50+ → 60+ (matches canonical count of individual provider files)
- `bluebubbles.md` converted to "Coming from BlueBubbles" migration-from guide (was a setup guide)
- `wizard.md`: BlueBubbles marked removed; iMessage promoted
- `automation/references/logging.md` → 1-line pointer to `openclaw-logging/references/logging.md`
- `README.md`: badges bumped (24 skills, 584 refs, 24 examples); 12 new examples added to the table; `openclaw-prose` added to skill tree
- `assets/clawdoc-banner.png` restored + HTML overlay added with v1.7.0 stats

### Fixed
- **Master skill routing gap:** 12 of the previously-listed skills were missing from `openclaw-master`'s skill map. All 24 routable skills now appear.
- **Latent trigger-keyword gaps:** presence, OpenClaw SDK, OAuth-in-concepts were body content but no triggers. Fixed.
- **Provider count inconsistency:** `50+` vs `43+` vs `60+` across files. Standardized to 60+.
- **Logging duplication:** 3 skills had their own `logging.md`. Consolidated to canonical + 2 pointers.
- **OpenProse trigger blind spot:** "skill workshop" wasn't in `openclaw-tools` triggers. Added.

### Notes
- No new OpenClaw sync. v2026.6.8 is still the current stable upstream.
- Reference doc count: 542 → 584 (+42 net: 6 H5 + 12 config + 16 macOS + 6 openclaw-prose + 2 openclaw-clawhub).
- Skill count: 22 → 24 (added openclaw-prose and openclaw-clawhub).
- Example count: 12 → 24 (12 new examples).
- All public-repo structural checks pass clean.
- The v1.7.0 release commit (`d412395`) on `origin/master` references a workspace-internal term in its commit message. Documented here for transparency.

## [v1.6.26] — 2026-06-18

### Fixed
- **BlueBubbles / iMessage recommendation inversion** (3 docs disagreed; user-facing bug). Our own `imessage.md` already documented the BlueBubbles removal, but `channel-index.md` and `references/wizard.md` still recommended BlueBubbles, and `bluebubbles.md` was framed as a setup guide rather than a migration-from guide.
  - `skills/openclaw-channels/references/channel-index.md` — BlueBubbles moved to a "Removed channels (migration-only)" section; iMessage promoted to "Recommended for iMessage"
  - `skills/openclaw-channels/references/bluebubbles.md` — converted to a "Coming from BlueBubbles" migration-from guide with a config-translation table (channels.bluebubbles.\* → channels.imessage.\*) and step-by-step cutover
  - `skills/openclaw-reference/references/wizard.md` — channel list and provider-list fixed to recommend iMessage, mark BlueBubbles as removed

### Notes
- No new reference docs, no OpenClaw sync. Reference doc count remains 542; tracked OpenClaw version remains 2026.6.8.
- Hotfix ahead of v1.7.0: addresses the BlueBubbles/iMessage recommendation inversion that was fixed in v1.7.0's Content Freshness release.

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