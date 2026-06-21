---
summary: "Configuration overview: common tasks, quick setup, and links to the full reference"
read_when:
  - Setting up OpenClaw for the first time
  - Looking for common configuration patterns
  - Navigating to specific config sections
title: "Configuration"
---

OpenClaw reads an optional **JSON5** config from `~/.openclaw/openclaw.json`.
The active config path must be a regular file. Symlinked `openclaw.json`
layouts are unsupported for OpenClaw-owned writes; an atomic write may replace
the path instead of preserving the symlink. If you keep config outside the
default state directory, point `OPENCLAW_CONFIG_PATH` directly at the real
file.

If the file is missing, OpenClaw uses safe defaults. Common reasons to add a
config:

- Connect channels and control who can message the bot
- Set models, tools, sandboxing, or automation (cron, hooks)
- Tune sessions, media, networking, or UI

See the **full reference** (`configuration-reference.md`) for every available
field.

> **Tip:** Agents and automation should use `config.schema.lookup` for exact
> field-level docs before editing config. Use this page for task-oriented
> guidance.

## Common tasks

### Connect a channel

See `config-channels.md`. Each channel plugin is enabled by adding a
`channels.<plugin>` block to your config and restarting the gateway.

### Add an LLM provider

See `providers.md` (in `openclaw-providers` skill). Add an entry under
`providers.<name>` with `baseUrl`, `apiKey`, and at least one model.

### Set a default model

```json5
{
  agents: { defaults: { model: { primary: "YOUR_DEFAULT_MODEL" } } },
}
```

### Lock down tool access

```json5
{
  tools: { profile: "minimal", allow: ["session_status"] },
}
```

### Enable sandboxing

```json5
{
  sandbox: { enabled: true, mode: "all", scope: "agent" },
}
```

### Reload config without restart

Most config keys hot-reload. See `reload-behavior.md` for the full reload
table.

## Hot reload vs restart

Some keys hot-apply (most do); others require `openclaw gateway restart`. The
distinction matters for production: prefer keys that hot-apply when you can.

Restart-required: gateway bind, auth mode, plugin enable/disable, model
provider registration, operator scopes.

Hot-applies: agent defaults, channel config, tool policy, sandbox policy,
session config, model routing per-agent.

## Validation

Run `openclaw config check` to validate your config against the current
schema before applying.

Run `openclaw config merge examples/foo.json` to apply an example.

For automation, both commands exit non-zero on validation failure, so they're
safe in scripts.

## Related

- `configuration-reference.md` — full field map
- `config-channels.md` — channel-specific keys
- `config-agents.md` — agent-specific keys
- `config-tools.md` — tools and providers
- `doctor.md` — health checks and migrations
- `secrets.md` — SecretRef for credentials