---
name: openclaw-config
description: OpenClaw gateway configuration reference. Use when auditing, editing, or troubleshooting openclaw.json. Covers ALL config keys: agents, channels, memory, tools, providers, session, messages, sandbox, plugins, env, model routing. Triggers on: "config", "openclaw.json", "configuration", "config reference", "config audit", "gateway config", "session config", "channel config".
---

# OpenClaw Config Reference

Complete reference for `~/.openclaw/openclaw.json`. Every significant top-level key documented.

## Quick cheatsheet

```json5
{
  // Agent defaults
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "minimax/MiniMax-M2.7", fallbacks: [] },
      memorySearch: { provider: "openai" },
      subagents: { model, allowAgents, maxConcurrent, runTimeoutSeconds },
      contextPruning: { mode: "cache-ttl", softTrim, hardClear },
      cliBackends: ["chatgpt", "claude", "gemini"],
      systemPromptOverride: null,
      skipBootstrap: false,
      repoRoot: null,
      imageMaxDimensionPx: 1200,
      userTimezone: null,
      timeFormat: null,
    },
    list: [{ name, model, bindings, skills, runtime: { type: "acp", acp: {} } }]
  },
  // Memory backend
  memory: { backend: "builtin", citations: "auto", qmd: {} },
  plugins: {
    slots: { memory: "openclaw-honcho" },
    entries: { "openclaw-honcho": { enabled: true, config: {} } }
  },
  // Channels
  channels: {
    discord: { token: "BOT", dmPolicy: "pairing" },
    modelByChannel: { "discord/CHANNEL_ID": "openai/gpt-4.1-mini" }
  },
  // Tools
  tools: {
    profile: "coding",
    elevated: { enabled: false },
    loopDetection: { enabled: false, historySize: 10, warningThreshold: 3 },
    sessions: { visibility: "tree" },
    byProvider: {},
    experimental: { planTool: false }
  },
  // Session
  session: {
    scope: "per-sender",
    dmScope: "main",
    maintenance: { maxDiskBytes: null, highWaterBytes: null, resetArchiveRetention: null },
    agentToAgent: { maxPingPongTurns: 5 },
    sendPolicy: [],
    parentForkMaxTokens: null
  },
  // Env / config organization
  env: { vars: {}, shellEnv: { enabled: false } },
  // Model routing
  models: { mode: "merge", providers: {} },
}
```

## Key paths (complete)

### agents.defaults.*

| Path | Type | Description |
|------|------|-------------|
| `agents.defaults.workspace` | `string` | Agent working directory |
| `agents.defaults.model` | `object` | Primary + fallback models |
| `agents.defaults.memorySearch` | `object` | Embedding provider: provider, model, baseUrl, collection |
| `agents.defaults.skills` | `string[]` | Default skill allowlist |
| `agents.defaults.subagents` | `object` | `model`, `allowAgents[]`, `maxConcurrent`, `runTimeoutSeconds`, `archiveAfterMinutes` |
| `agents.defaults.contextPruning` | `object` | **In-memory only** — does NOT touch session history on disk. `mode: "cache-ttl"`, `softTrim`, `hardClear`, `tools.deny`, `keepLastAssistants` |
| `agents.defaults.cliBackends` | `string[]` | Text-only CLI fallback backends for provider outages |
| `agents.defaults.systemPromptOverride` | `string\|null` | Fixed system prompt replacement |
| `agents.defaults.skipBootstrap` | `boolean` | Skip workspace bootstrap files |
| `agents.defaults.repoRoot` | `string\|null` | Optional repo root for system prompt |
| `agents.defaults.imageMaxDimensionPx` | `number` | Image downscaling (default 1200) |
| `agents.defaults.userTimezone` | `string\|null` | Timezone for system prompt (e.g. "America/New_York") |
| `agents.defaults.timeFormat` | `string\|null` | Time format string |
| `agents.defaults.heartbeat` | `object` | `showOk`, `showAlerts`, `useIndicator` for compact heartbeat |
| `agents.defaults.compaction` | `object` | Context compaction settings |
| `agents.defaults.sandbox` | `object` | Sandbox config |

### agents.list[].*

| Path | Type | Description |
|------|------|-------------|
| `agents.list[].runtime.type` | `string` | `"agent"` (default) or `"acp"` |
| `agents.list[].runtime.acp` | `object` | ACP harness: `agent`, `backend`, `mode`, `cwd` |
| `agents.list[].thinkingDefault` | `string` | Per-agent thinking level override |
| `agents.list[].reasoningDefault` | `string` | Per-agent reasoning visibility |
| `agents.list[].fastModeDefault` | `boolean` | Per-agent fast mode |
| `agents.list[].subagents.requireAgentId` | `boolean` | Force explicit agentId in sessions_spawn |
| `agents.list[].memorySearch` | `object` | Per-agent memory search override |
| `agents.list[].skills` | `string[]` | Per-agent skill allowlist |

### channels.*

| Path | Type | Description |
|------|------|-------------|
| `channels.modelByChannel` | `object` | Per-channel-ID model pinning: `channels.telegram."-100123": "openai/gpt-4.1-mini"` |
| `channels.defaults.contextVisibility` | `string` | `all\|allowlist\|allowlist_quote` — supplemental context scope |
| `channels.defaults.heartbeat` | `object` | `showOk`, `showAlerts`, `useIndicator` |
| `messages.statusReactions.enabled` | `boolean` | Enables lifecycle status reactions on Slack/Discord/Telegram |

### tools.*

| Path | Type | Description |
|------|------|-------------|
| `tools.loopDetection` | `object` | **Disabled by default.** `enabled: true` opt-in. `historySize`, `warningThreshold`, `criticalThreshold`, `globalCircuitBreakerThreshold`. Thresholds must satisfy: warning < critical < global. Validation fails on misconfig. |
| `tools.experimental.planTool` | `boolean` | `update_plan` tool. Default `false` unless strict-agentic GPT-5 auto-enables. |
| `tools.sessions.visibility` | `string` | `self\|tree\|agent\|all`. Default `tree` — subagents see only sibling sessions. `all` requires no sandbox clamp. |
| `tools.sessions_spawn.attachments` | `object` | `enabled`, `maxTotalBytes`, `maxFiles`, `maxFileBytes`, `retainOnSessionKeep` |
| `tools.byProvider` | `object` | Per-provider/tool-profile overrides |

### session.*

| Path | Type | Description |
|------|------|-------------|
| `session.identityLinks` | `array` | Cross-channel session sharing via canonical ID → provider-prefixed peer mapping |
| `session.resetByType` | `object` | Per-type reset overrides: `thread`, `direct`, `group` with `mode/atHour/idleMinutes` |
| `session.maintenance` | `object` | `resetArchiveRetention` (duration or `false`), `maxDiskBytes`, `highWaterBytes`. **In `enforce` mode: actively deletes old sessions.** Default: no enforcement. |
| `session.agentToAgent.maxPingPongTurns` | `number` | Max turns in agent-to-agent exchange. `0` disables. Default `5`. |
| `session.sendPolicy` | `array` | Deny/allow by `channel`, `chatType`, `keyPrefix`. **First deny wins.** |
| `session.parentForkMaxTokens` | `number\|null` | Guard: prevent inheriting parent transcript when parent exceeds token threshold |

### env / config organization

| Path | Type | Description |
|------|------|-------------|
| `env.vars` | `object` | Static env vars injected into gateway process |
| `env.shellEnv.enabled` | `boolean` | Import current shell env into gateway |
| `${VAR}` substitution | `string` | Any config string can use `${VAR}` — substituted at load time |
| `$${VAR}` escaping | `string` | Literal `${VAR}` in config value |
| `$include` | `string` | Deep-merge external file: `$include: "./agents.json5"` |

### models.*

| Path | Type | Description |
|------|------|-------------|
| `models.mode` | `string` | `merge\|replace` — how per-model fields combine |
| `models.providers.*.auth` | `object` | Provider auth config |
| `models.providers.*.injectNumCtxForOpenAICompat` | `boolean` | Inject numCtx for OpenAI-compatible endpoints |
| `models.providers.*.request.headers` | `object` | Custom request headers |
| `models.providers.*.request.auth` | `string` | Auth mode: `authorization-bearer`, `header`, etc. |

## Critical: Safety features off by default

| Feature | Default | Risk if ignored |
|---------|---------|----------------|
| `tools.loopDetection` | `false` | Infinite tool loops can run forever |
| `agents.defaults.contextPruning` | not set | Tool results accumulate, context fills up |
| `execApprovals` (Discord/Slack/Matrix) | not set | Any Discord user could trigger exec |
| `session.maintenance.enforce` | not set | Session store grows unbounded |

## Common fixes

### Enable Honcho as memory backend
The single most common OpenClaw misconfiguration: both `memory-core` and `openclaw-honcho` fight for the memory slot.

**Fix:**
```json5
plugins: {
  slots: { memory: "openclaw-honcho" },   // claims the memory slot
  entries: {
    "openclaw-honcho": {                  // enable the plugin
      enabled: true,
      config: { baseUrl: "http://127.0.0.1:8000" }
    }
  }
}
```
Restart gateway required. Do not set `memory.backend` — the slot override handles it.

### Discord bot not responding
- `dmPolicy: "pairing"` requires pairing approval
- `allowFrom` must contain your Discord user ID
- Enable Message Content Intent in Discord Developer Portal

### Config validation
```bash
python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null && echo "valid"
```

## Secrets management

OpenClaw supports **SecretRefs** — credentials as references, not plaintext:

```json5
models: {
  providers: {
    openai: { apiKeyRef: "secret:openai-key" }
  }
}
```

- Resolves to in-memory snapshot at startup/reload
- Startup fails fast on unresolved active refs
- Inactive surfaces (disabled plugins/channels) don't block startup
- Atomic reload: full success or keep last-known-good snapshot
- Secrets stored under `~/.openclaw/credentials/`

## Retry policy

Per-provider retry defaults:

| Provider | Attempts | Min delay | Max delay | Jitter |
|----------|----------|-----------|-----------|--------|
| Telegram | 3 | 400ms | 30000ms | 0.1 |
| Discord | 3 | 500ms | 30000ms | 0.1 |

Discord retries only on HTTP 429. Telegram retries on 429, timeout, transient network errors.

## Gateway restart triggers

**Require restart:** `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`, `session.identityLinks`
**Dynamic (no restart):** `tools.web.search.apiKey`, `agents.defaults.memorySearch.remote`, channel-level `enabled`

## Config editing via gateway tool

Use the `gateway` tool (action: `config.patch` or `config.apply`) to edit config at runtime. These are rate-limited to **3 requests per 60 seconds** per device — excess calls return `UNAVAILABLE` with `retryAfterMs`.

### `config.patch` (preferred — partial update)

JSON merge patch semantics:
- Objects merge **recursively**
- `null` **deletes** a key
- Arrays **replace** entirely

```javascript
gateway(
  action: "config.patch",
  raw: "{ channels: { telegram: { groups: { \"*\": { requireMention: false } } } } }",
  baseHash: "<hash from config.get>"
)
```

**Always run `config.schema.lookup` first** to inspect the subtree you're editing.

### `config.apply` (full replacement)

Replaces the **entire config**. Use only when replacing the whole file. Otherwise prefer `config.patch`.

```javascript
gateway(
  action: "config.apply",
  raw: "{ ...entire config... }",
  baseHash: "<hash>"
)
```

### Config write rate limit

| Limit | Value |
|-------|-------|
| Requests | 3 per 60 seconds |
| Scope | per `deviceId + clientIp` |
| On exceed | `UNAVAILABLE` + `retryAfterMs` |

### Hot reload

The gateway watches `~/.openclaw/openclaw.json` and reloads automatically:

| Mode | Behavior |
|------|----------|
| `hybrid` (default) | Hot-apply safe changes; auto-restart for critical ones |
| `hot` | Hot-apply safe changes only; log warning for restart-needed changes |
| `restart` | Restart on any change |
| `off` | Manual restart only |

```json5
gateway: { reload: { mode: "hybrid", debounceMs: 300 } }
```

**What needs a restart:** `memory.backend`, `plugins.slots`, `agents.defaults.*`, `session.identityLinks`. All others hot-apply.

### Safe direct edit (alternative)

You can also edit `~/.openclaw/openclaw.json` directly — the gateway watches the file and auto-reloads. No restart needed for most changes.

## References

Load these for detailed topics:
- `openclaw-memory/references/memory-config.md` — all memory config knobs
- `openclaw-concepts/references/context.md` — context window system
- `openclaw-concepts/references/system-prompt.md` — system prompt assembly
- `openclaw-concepts/references/session.md` — session system
- `openclaw-concepts/references/compaction.md` — compaction (different from contextPruning)
- `openclaw-agents/references/multi-agent.md` — full multi-agent guide
- `openclaw-troubleshooting/references/diagnostic-flowchart.md` — symptom → fix mapping
