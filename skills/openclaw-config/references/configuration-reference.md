---
summary: "Gateway config reference for core OpenClaw keys, defaults, and links to dedicated subsystem references"
read_when:
  - You need exact field-level config semantics or defaults
  - You are validating channel, model, gateway, or tool config blocks
title: "Configuration reference"
---

Core config reference for `~/.openclaw/openclaw.json`. For a task-oriented
overview, see `configuration.md`. Channel- and plugin-owned command catalogs
and deep memory/QMD knobs live on their own pages rather than on this one.

## Top-level keys

| Key | What it does | Hot-reload? | Reference |
|-----|--------------|:-----------:|-----------|
| `agents.*` | Agent defaults, multi-agent routing | mostly hot | `config-agents.md` |
| `channels.*` | Channel plugins (per-plugin block) | hot (when added) | `config-channels.md` |
| `tools.*` | Tool profiles, allow/deny, elevated policy | hot | `config-tools.md` |
| `providers.*` | LLM provider registration (custom + bundled) | restart required | `providers.md` |
| `memory.*` | Memory backend selection and config | restart required | `memory.md` |
| `session.*` | Session persistence, compaction, history limit | hot | `config-agents.md` |
| `messages.*` | Delivery, TTS, voice, ack reactions | hot | `config-agents.md` |
| `sandbox.*` | Sandbox mode, scope, workspace access | hot | `sandboxing.md` |
| `plugins.*` | Plugin slot registration and per-plugin config | restart required | `plugins.md` |
| `gateway.*` | Gateway bind, auth, TLS, telemetry | mostly restart | `gateway.md` |
| `secrets.*` | SecretRef providers | hot | `secrets.md` |
| `env.*` | Env-var passthrough to agent runtime | hot | `environment.md` |
| `bindings` | Channel → agent routing | hot | `agents-bindings.md` |

## Config format

JSON5 (comments + trailing commas allowed). All fields are optional —
OpenClaw uses safe defaults when omitted.

## Field-level lookup

Three ways to find the exact schema for a key:

1. `openclaw config schema` — prints the live JSON Schema used for validation
   and the Control UI. Bundled/plugin/channel metadata is merged in when
   available.
2. `config.schema.lookup` tool action — returns one path-scoped schema node
   for drill-down tooling. Use this from inside an agent.
3. `pnpm config:docs:check` / `pnpm config:docs:gen` — internal CLI for
   validating the config-doc baseline hash against the current schema
   surface.

## Default behaviors

When a key is missing, OpenClaw uses safe defaults:

- `agents.defaults.model.primary` — falls back to `OPENCLAW_DEFAULT_MODEL`
  env var, then to the first configured provider's first model.
- `channels.*` — channel is disabled unless its config block exists.
- `tools.profile` — `"coding"` for new local configs; `null` for existing
  configs.
- `sandbox.mode` — `"all"` if `sandbox.enabled: true`, otherwise off.
- `gateway.bind` — `127.0.0.1:18789` (loopback only).
- `gateway.auth.mode` — `"token"` if `OPENCLAW_GATEWAY_TOKEN` is set,
  otherwise `"none"` (loopback only).

## Deep references

- `config-agents.md` — agents, session, messages
- `config-channels.md` — channel plugins
- `config-tools.md` — tools, providers, elevated policy
- `secrets.md` — SecretRef contract
- `sandboxing.md` — sandbox modes and scopes
- `gateway.md` — gateway runtime
- `authentication.md` — model provider auth
- `doctor.md` — health checks and migrations

For channel- and plugin-specific command catalogs and deep memory/QMD knobs,
see the owning skill's references.

## Example

```json5
// Most OpenClaw config lives at ~/.openclaw/openclaw.json
{
  "agents": { "defaults": { "model": { "primary": "minimax/MiniMax-M3" } } },
  "memory": { "backend": "builtin" },
  "plugins": { "entries": { "openclaw-honcho": { "enabled": true } } }
}
```
