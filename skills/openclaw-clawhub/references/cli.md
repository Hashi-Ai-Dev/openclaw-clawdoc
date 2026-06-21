---
summary: "ClawHub CLI entry points for discovering, installing, publishing, and verifying OpenClaw skills and plugins"
read_when:
  - You want to use ClawHub from the command line
  - You want to install ClawHub skills or plugins through OpenClaw
  - You want to publish ClawHub packages
title: "ClawHub CLI"
---

OpenClaw has two command-line entry points for ClawHub:

- **`openclaw skills` and `openclaw plugins`** install and manage ClawHub
  packages inside OpenClaw.
- **The standalone `clawhub` CLI** handles publisher workflows such as
  login, publish, transfer, and sync.

## Discover and install

Use OpenClaw commands when you want to install or update packages for a
local OpenClaw agent or Gateway.

```bash
openclaw skills search "calendar"
openclaw skills install <slug>
openclaw skills update <slug>
openclaw skills verify <slug>

openclaw plugins search "calendar"
openclaw plugins install <slug>
openclaw plugins update <slug>
openclaw plugins verify <slug>
```

## Update all installed packages

```bash
openclaw skills update --all
openclaw plugins update --all
```

## Verify all installed packages

```bash
openclaw skills verify --all
openclaw plugins verify --all
```

`verify --all` is safe in CI — it exits non-zero if any installed package
fails its integrity check.

## Publisher CLI: `clawhub`

The standalone `clawhub` CLI handles publishing, owner management, and
registry sync. It is installed separately from OpenClaw.

```bash
# Login (opens browser for OAuth)
clawhub login

# Check who you're signed in as
clawhub whoami

# Publish from a skill or plugin folder
clawhub publish

# Publish a specific version
clawhub publish --version 1.2.0

# Transfer ownership of a package
clawhub transfer <slug> --to @new-owner

# Sync local state with the registry
clawhub sync
```

## Search output

`openclaw skills search <query>` and `openclaw plugins search <query>` print
a tabular result:

```
SLUG                    OWNER        VERSION   DESCRIPTION
@openclaw/calendar      @openclaw    1.4.2     Calendar integration via CalDAV
@alice/ical-bridge      @alice       0.9.0     iCloud calendar sync
```

Use `openclaw skills search --json <query>` for machine-readable output.

## Install paths

Packages install to `~/.openclaw/skills/` (skills) or
`~/.openclaw/plugins/` (plugins). The installed path is shown by
`openclaw skills list --paths` and `openclaw plugins list --paths`.

## Version pinning

Pin a package to a specific version in your config:

```json5
{
  skills: {
    installed: {
      "@openclaw/calendar": "1.4.2",
    },
  },
}
```

OpenClaw refuses to auto-update pinned packages. Run
`openclaw skills update <slug>` explicitly to bump.

## Removal

```bash
openclaw skills remove <slug>
openclaw plugins remove <slug>
```

Removal deletes the installed folder. It does NOT call any uninstall hook in
the package — packages should clean up after themselves at shutdown, not
uninstall.

## See also

- `publishing.md` — owners, scopes, reviews.
- `openclaw-tools/references/skill-workshop.md` — Skill Workshop.