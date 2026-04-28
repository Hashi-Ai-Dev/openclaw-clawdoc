---
name: openclaw-config
description: OpenClaw gateway configuration reference. Use when auditing, editing, or troubleshooting openclaw.json. Covers ALL config keys: agents, channels, memory, tools, providers, session, messages, sandbox, plugins, env, model routing. Triggers on: "config", "openclaw.json", "configuration", "config reference", "config audit", "gateway config", "session config", "channel config", "runtime", "model routing", "env vars", "gateway won't start", "config error", "how to configure", "openclaw doctor".
---

# OpenClaw Config Reference

Complete reference for `~/.openclaw/openclaw.json`.

## Quick cheatsheet

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "provider/model", fallbacks: [] },
      memorySearch: { provider: "openai" },
      subagents: { maxConcurrent: 3, runTimeoutSeconds: 300 },
      contextPruning: { mode: "cache-ttl" },
    },
    list: [{ id, model, bindings, skills, runtime: { type: "acp" } }]
  },
  memory: { backend: "builtin", citations: "auto" },
  plugins: { slots: { memory: "openclaw-honcho" }, entries: {} },
  channels: { discord: { token: "BOT", dmPolicy: "pairing" } },
  tools: { profile: "coding", elevated: { enabled: false } },
  session: { scope: "per-sender", dmScope: "main" },
  env: { vars: {} }
}
```

## Critical defaults (safety)

| Feature | Default | Risk if enabled accidentally |
|---------|---------|----------------------------|
| `tools.loopDetection` | `false` | Infinite loops run forever |
| `execApprovals` | not set | Any user can trigger exec |
| `session.maintenance.enforce` | not set | Sessions grow unbounded |

## Common fixes

**Honcho as memory (most common misconfig):**
```json5
plugins: {
  slots: { memory: "openclaw-honcho" },
  entries: { "openclaw-honcho": { enabled: true, config: { baseUrl: "http://127.0.0.1:8000" } } }
}
```
Restart required. Do NOT set `memory.backend` — the slot override handles it.

**Discord bot silent:**
- `dmPolicy: "pairing"` — approve via `openclaw pairing approve discord <CODE>`
- `allowFrom` must include your Discord user ID
- Enable Message Content Intent in Discord Developer Portal

## Config editing

**`config.patch`** (preferred — partial merge):
```javascript
gateway(action: "config.patch", raw: "{ channels: { telegram: { enabled: true } } }", baseHash: "<hash>")
```
- Objects merge recursively
- `null` deletes a key
- Arrays replace entirely

**`config.apply`** (full replacement — use sparingly)

**Hot reload:** Gateway watches `~/.openclaw/openclaw.json` and auto-reloads. Restart required for: `memory.backend`, `plugins.slots`, `agents.defaults.*`.

**Rate limit:** 3 config writes per 60 seconds per device.

## Secrets

Use SecretRefs instead of plaintext:
```json5
{ apiKeyRef: "secret:my-key" }
```
Stored under `~/.openclaw/credentials/`. Startup fails fast on unresolved refs.

## Restart triggers

| Require restart | Hot-reload only |
|----------------|-----------------|
| `memory.backend` | `tools.web.search.apiKey` |
| `plugins.slots` | `agents.defaults.memorySearch.remote` |
| `agents.defaults.*` | Channel `enabled` |
| `session.identityLinks` | Most other changes |

## References

- `references/gateway-config.md` — full config reference (all keys)
- `references/secrets.md` — SecretRef details
- `references/config-channels.md` — channel config
- `openclaw-memory/references/memory-config.md` — memory knobs
- `openclaw-concepts/references/session.md` — session system
- `openclaw-troubleshooting/references/diagnostic-flowchart.md` — triage
