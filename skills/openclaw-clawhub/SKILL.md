---
name: openclaw-clawhub
description: "ClawHub public registry for OpenClaw skills and plugins. Use when discovering, installing, publishing, verifying, or updating ClawHub packages; using the clawhub CLI; understanding package scopes, owners, and reviews; or browsing the registry at clawhub.ai. Triggers on: clawhub, clawhub CLI, clawhub login, clawhub publish, publish skill, publish plugin, registry, browse skills, browse plugins, install from clawhub, clawhub transfer, clawhub sync, package scope, owner scope, clawhub review, clawhub install, clawhub update, clawhub verify, skill marketplace, plugin marketplace."
---

# OpenClaw ClawHub

ClawHub is the public registry for OpenClaw skills and plugins. OpenClaw
operators use it to discover and install community packages; skill and
plugin authors use it to publish their work.

The registry lives at https://clawhub.ai. Two CLI surfaces interact with it:

- **`openclaw skills` / `openclaw plugins`** — install, update, verify from
  inside OpenClaw.
- **`clawhub`** (standalone CLI) — publisher workflows: login, publish,
  transfer, sync.

For the full CLI reference, see `references/cli.md`. For publishing details,
see `references/publishing.md`.

## Quick start

```bash
# Discover a package
openclaw skills search "calendar"
openclaw plugins search "calendar"

# Install it
openclaw skills install <slug>
openclaw plugins install <slug>

# Update an installed package
openclaw skills update <slug>
openclaw plugins update <slug>

# Verify integrity
openclaw skills verify <slug>
```

## For publishers

```bash
# One-time login
clawhub login

# Publish a skill (from a skill folder)
clawhub publish

# Update an existing version
clawhub publish --version 1.2.0

# Transfer ownership
clawhub transfer <slug> --to @new-owner

# Sync local state with the registry
clawhub sync
```

Every publish targets a **publisher owner** (`@alice`, `@openclaw`, etc.).
Personal owners are created for users; org owners can have multiple members.
The server decides whether the signed-in user is allowed to publish under
each owner.

## Browse

The web UI at https://clawhub.ai shows:

- Search across skills and plugins
- Per-package page with versions, reviews, owner info
- Owner pages with all packages by that publisher
- Org pages with member lists

For programmatic browse, the registry also exposes a JSON API.

## Verifying installs

`openclaw skills verify <slug>` checks:

- The installed package matches its declared hash from the registry
- Required dependencies are present
- The package's `SKILL.md` frontmatter parses
- The package's manifest claims no surprising capabilities

A failed verify exits non-zero and is safe in CI.

## See also

- `references/cli.md` — full CLI reference for both `openclaw skills/plugins`
  and the standalone `clawhub` CLI.
- `references/publishing.md` — owners, scopes, reviews, the publish flow,
  and version semantics.
- `skills/openclaw-plugins/references/plugin-inventory.md` — bundled
  plugins that ship with OpenClaw (separate from ClawHub-published
  community plugins).
- `skills/openclaw-tools/references/skill-workshop.md` — Skill Workshop,
  the editor for reviewing and proposing new skills.