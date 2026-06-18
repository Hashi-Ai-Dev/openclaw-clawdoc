# Changelog

All notable changes to ClawDoc are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
ClawDoc adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [v1.6.25] — 2026-06-18

### Added
- `CHANGELOG.md` — first curated changelog file (Keep-a-Changelog format)
- README "Scope" section — explicit fences for what ClawDoc does and does not do
- README "How ClawDoc routes requests" diagram — Mermaid flow showing master → area skill → reference docs → answer

### Changed
- `SOUL.md` expanded with operating posture, routing flow, and scope fences; routing and citation discipline now part of the public persona
- Install guides (`AGENT_INSTALL.md`, `SKILLS_INSTALL.md`), `QUICKSTART.md`, and `agent-template/README.md` bumped in lockstep with manifest — eliminates the v1.6.21 tag fix-up dance

### Notes
- Zero audit drift found on pre-pass: `routing_audit.py`, `claim_audit.py`, `metadata_audit.py`, `validate_repo.py`, `safety_scanner.py` all clean
- No `tracked_openclaw_version` change — still 2026.6.8 (no OpenClaw sync in this release)

## [v1.6.24] — 2026-06-18

### Changed
- Audit polish: 12 findings consolidated from a full 4-agent public-repo audit
- 3 broken reference doc links fixed
- 3 stale model references in examples corrected
- Manifest consistency, README polish, install-guide "Try an example" block, scanner allowlist fix

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
- Install guides + agent-template bumped in the same commit as the OpenClaw 2026.6.8 sync (eliminates the v1.6.20-era tag fix-up dance)

### Added
- 28 modified reference docs applied, 4 new docs added

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
- Skill routing maintenance pass — triggered by 19-day drift gap between v1.6.14 and v1.6.15; found and closed routing gaps

## [v1.6.14] — 2026-05-27

### Added
- Processed all 4 deferred areas from the v2026.5.26 sync: `cli` (14), `gateway` (18 new), `plugins` (12+3), `tools` (11+1)
- 55 references applied, 3 deferred (plugins: `codex-harness-reference`, `codex-harness`, `sdk-subpaths`)

### Fixed
- `.mdx` file undercount: `railway.mdx` was missed by `find -name "*.md"`; corrected formula in sync skills

## [v1.6.13] — 2026-05-27

### Added
- OpenClaw v2026.5.26 sync: 5 new reference docs, 43 modified

## [v1.6.12] — 2026-05-24

### Added
- OpenClaw v2026.5.22 sync: 3 new reference docs, 29 modified

## [v1.6.11] — 2026-05-22

### Changed
- Skill routing audit: added missing trigger keywords

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
- `openclaw-sync` skill reference doc count formula corrected

## [v1.5.x and earlier] — 2026-04 to 2026-05

Rapid iteration period: 28 releases from v1.0 through v1.5.14 covering:

- Initial release (11 skills, 90 files)
- Skills expansion to 22 routable skills
- Reference doc growth from 90 → 487+
- `SKILL.md` restructuring with trigger keywords
- OpenClaw sync pipeline (`openclaw-sync` skill)
- Multiple OpenClaw version syncs (2026.4.x → 2026.5.x)
- Quickstart guide, examples expansion (4 → 12)
- Onboarding skill (`clawdoc-onboarding`)
- Install reference docs and platform guides

For the full release-by-release history, see [GitHub Releases](https://github.com/Hashi-Ai-Dev/openclaw-clawdoc/releases).