---
summary: "Doctor command: health checks, config migrations, and repair steps"
read_when:
  - Adding or modifying doctor migrations
  - Introducing breaking config changes
title: "Doctor"
---

`openclaw doctor` is the repair + migration tool for OpenClaw. It fixes stale
config/state, checks health, and provides actionable repair steps.

## Quick start

```bash
openclaw doctor
```

### Headless and automation modes

- `--yes`: Accept defaults without prompting (including restart/service/
  sandbox repair steps when applicable).
- `--fix`: Run all automatic repairs non-interactively.
- `--dry-run`: Show what would change without modifying anything.
- `--json`: Machine-readable output for CI/scripts.

```bash
openclaw doctor --yes
openclaw doctor --fix
openclaw doctor --dry-run
openclaw doctor --json | jq '.findings[] | select(.severity == "high")'
```

## What doctor checks

### Config validity

- Schema correctness against the current schema version
- Deprecated keys still in use (with auto-fix suggestions)
- Migrations pending from prior versions
- Plaintext credentials in tracked files (calls into `secrets audit`)

### State directory health

- Workspace directory exists and is writable
- `auth-profiles.json` permissions are 0600
- `agents/*/agent/models.json` files match the active config
- Database files (Honcho, memory-core) are healthy

### Plugin / channel health

- All enabled plugins load successfully
- Channel configs reference real plugin names
- No orphan or duplicated plugin slots

### Gateway health

- Bound port is reachable
- Auth mode matches deployment posture (loopback vs public)
- Required directories exist

## Migrations

When OpenClaw upgrades with breaking config changes, doctor applies
migrations automatically (with `--fix`) or interactively (default). Common
migrations:

- Renamed config keys (old → new)
- New required fields populated with safe defaults
- Removed fields pruned
- Plugin slot reorganizations

Migrations are versioned and idempotent — running doctor twice is safe.

## Repair actions

Some repair steps modify state beyond config:

- `restart gateway`: `openclaw gateway restart`
- `regenerate models.json`: rebuilds `agents/*/agent/models.json`
- `rebuild auth-profiles`: re-derives profiles from config + env
- `repair sandbox`: re-applies sandbox profile to running sandbox

Doctor prompts before any repair that modifies runtime state, unless `--yes`
or `--fix` is passed.

## Common exit codes

- `0` — clean, no action needed
- `1` — findings reported, no automatic fix available
- `2` — repair performed, gateway restart recommended
- `3` — repair performed, gateway restart required (already restarted
  with `--fix`)

## When to run

- After upgrading OpenClaw
- After editing config manually
- Before reporting a bug (the issue template asks for `openclaw doctor --json`)
- In CI, as a pre-merge check