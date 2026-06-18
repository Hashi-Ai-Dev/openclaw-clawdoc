# Changelog

All notable changes to ClawDoc are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
ClawDoc adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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