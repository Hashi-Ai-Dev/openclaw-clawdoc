---
name: openclaw-config
description: OpenClaw gateway configuration reference. Use when auditing, editing, or troubleshooting openclaw.json. Covers all config keys: agents, channels, memory, tools, providers, session, messages, sandbox, and plugins. Triggers on: "config", "openclaw.json", "configuration", "config reference", "config audit", "gateway config".
---

# OpenClaw Config Reference

Core configuration reference for `~/.openclaw/openclaw.json`. See bundled docs for deep dives.

## Quick cheatsheet

```json5
{
  // Agent defaults
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "minimax/MiniMax-M2.7" },
      memorySearch: { provider: "openai" },  // or gemini, voyage, mistral, bedrock, ollama, local
    }
  },
  // Memory backend
  memory: {
    backend: "builtin",  // or "qmd"
    citations: "auto",
    qmd: { includeDefaultMemory: true }
  },
  // Plugins
  plugins: {
    slots: { memory: "openclaw-honcho" },  // override for Honcho
    entries: { "openclaw-honcho": { enabled: true, config: { baseUrl: "http://127.0.0.1:8000" } } }
  },
  // Channels (Discord example)
  channels: {
    discord: {
      token: "BOT_TOKEN",
      dmPolicy: "pairing",
      allowFrom: ["1234567890"],
      guilds: { "GUILD_ID": { channels: { "CHANNEL_ID": { allow: true } } } }
    }
  },
  // Tools
  tools: {
    profile: "coding",
    elevated: { enabled: true, allowFrom: { discord: ["1234567890"] } }
  },
  // Session
  session: { scope: "per-sender", dmScope: "main" }
}
```

## Key paths

| Path | Type | Description |
|------|------|-------------|
| `agents.defaults.workspace` | `string` | Agent working directory |
| `agents.defaults.model` | `object` | Primary + fallback models |
| `agents.defaults.memorySearch` | `object` | Embedding provider config |
| `agents.defaults.skills` | `string[]` | Default skill allowlist |
| `memory.backend` | `string` | `"builtin"` or `"qmd"` |
| `memory.citations` | `string` | `"auto"` `"on"` `"off"` |
| `plugins.slots.memory` | `string` | Memory plugin override |
| `plugins.entries.PLUGIN.config` | `object` | Per-plugin config |
| `channels.discord.token` | `string` | Bot token |
| `channels.discord.dmPolicy` | `string` | `pairing\|allowlist\|open\|disabled` |
| `tools.elevated.enabled` | `boolean` | Elevated exec |
| `tools.elevated.allowFrom` | `object` | Per-channel sender allowlist |
| `session.scope` | `string` | `per-sender\|global` |
| `session.dmScope` | `string` | `main\|per-peer\|per-channel-peer` |
| `messages.ackReaction` | `string` | Reaction after bot reads |
| `agents.defaults.compaction` | `object` | Context compaction settings |
| `agents.defaults.heartbeat` | `object` | Periodic heartbeat runs |
| `agents.defaults.sandbox` | `object` | Sandbox config |
| `agents.list[]` | `array` | Per-agent overrides |
| `bindings[]` | `array` | Agent routing rules |

## Common fixes

### Enable Honcho as memory backend
```json5
plugins: { slots: { memory: "openclaw-honcho" } }
```
Then restart gateway.

### Discord bot not responding
- Check `dmPolicy`: `"pairing"` requires pairing approval
- Check `allowFrom` contains your Discord ID
- Enable Message Content Intent in Discord Developer Portal

### Memory search not working
```bash
openclaw memory status  # diagnose
openclaw memory index --force  # rebuild index
```
Provider auto-detected in order: local → openai → gemini → voyage → mistral → bedrock

### Config validation
```bash
python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null && echo "valid"
```

## Gateway restart triggers

**Require restart:** `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`
**Dynamic (no restart):** `tools.web.search.apiKey`, `agents.defaults.memorySearch.remote`

## Secrets management

OpenClaw supports **SecretRefs** — credentials stored as references instead of plaintext:

```json5
models: {
  providers: {
    openai: { apiKeyRef: "secret:openai-key" }
  }
}
```

- Secrets resolve into an in-memory snapshot at startup/reload
- Startup fails fast on unresolved active refs
- Inactive surfaces (disabled plugins/channels) don't block startup
- Reload is atomic: full success or keep last-known-good snapshot
- Secrets stored under `~/.openclaw/credentials/`

## Retry policy

Per-provider retry defaults:

| Provider | Attempts | Min delay | Max delay | Jitter |
|----------|----------|-----------|-----------|--------|
| Telegram | 3 | 400ms | 30000ms | 0.1 |
| Discord | 3 | 500ms | 30000ms | 0.1 |

Discord retries only on HTTP 429. Telegram retries on 429, timeout, transient network errors.

## References

Load these for detailed topics:
- `openclaw-memory/references/memory-config.md` — all memory config knobs
- `openclaw-channels/references/channel-routing.md` — routing rules + session keys
- `openclaw-agents/references/multi-agent.md` — full multi-agent guide
- `openclaw-concepts/references/session.md` — session system
- `openclaw-concepts/references/compaction.md` — compaction + memory flush
- `openclaw-concepts/references/sandboxing.md` — sandbox config
- `openclaw-plugins/references/plugin-architecture.md` — plugin system
- `openclaw-plugins/references/context-engine.md` — context engine + plugin memory
- `openclaw-providers/references/providers.md` — all providers
