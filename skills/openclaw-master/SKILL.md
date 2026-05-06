---
name: openclaw-master
description: OpenClaw configuration expert and system doctor. Use when answering OpenClaw questions about config audits, plugin integration, memory backends, multi-agent setup, channel configuration, troubleshooting, agent design, CLI commands, provider setup, SOUL.md, streaming, queue modes, model failover, sandbox, Task Flow, Lobster, Diff viewer
---

# OpenClaw Master Reference

Comprehensive OpenClaw knowledge base. This is the top-level skill that routes to specialized skills.

> **⚠️ OSS discipline:** Before publishing any release, new skill, or infrastructure change to the OSS repo, ALWAYS confirm with Hashi first. Not every feature belongs in the public release.

## Skill map

| Skill | When to use |
|-------|-------------|
| `openclaw-config` | Config audits, gateway config keys, secrets, retry, model failover, timezone, auth profiles, authentication |
| `openclaw-memory` | Memory backends (builtin/QMD/Honcho), embedding providers, active memory, dreaming, memory search |
| `openclaw-agents` | Multi-agent setup, bindings, sandbox, tool policies, exec approvals |
| `openclaw-channels` | Discord, Telegram, WhatsApp, Slack, Signal, Matrix, iMessage, routing, pairing, broadcast groups |
| `openclaw-concepts` | Architecture, session, compaction, streaming, bootstrap, queue modes, agent loop, system prompt, SOUL.md, Task Flow |
| `openclaw-troubleshooting` | Diagnosis, error codes, ACP, hooks, pairing, channel failures, gateway runbook |
| `openclaw-plugins` | Plugin slots, installing plugins, plugin config, context engine |
| `openclaw-tools` | Tool reference: exec, browser, cron, sessions, subagents, ACP, slash commands, Lobster, Diff viewer |
| `openclaw-cli` | CLI commands: status, gateway, plugins, memory, agents, channels, config, sessions, cron, hooks, pairing, ACP, MCP, secrets, doctor, update, skills |
| `openclaw-providers` | Model providers: OpenAI, Anthropic, Gemini, Bedrock, Ollama, DeepSeek, Groq, Together, and 30+ more |

## Quick reference

### Docs URLs (always current)
| Topic | URL |
|---|---|
| Config reference | https://docs.openclaw.ai/gateway/configuration-reference |
| CLI commands | https://docs.openclaw.ai/cli/index |
| Channels | https://docs.openclaw.ai/channels/index |
| Providers | https://docs.openclaw.ai/providers/index |
| Tools | https://docs.openclaw.ai/tools/index |
| Troubleshooting | https://docs.openclaw.ai/help/troubleshooting |
| OpenClaw docs | https://docs.openclaw.ai |
| ClawHub (skills) | https://clawhub.ai |

### Usage quick reference
| Situation | Action |
|---|---|
| Config changes | Use gateway tool (`config.get` / `config.patch` / `config.apply`) |
| Skill installation | `clawdhub` or clone to `~/.openclaw/skills/` |
| Bot mention in Discord | `<@bot-id>` not plain `@name` |
| `requireMention: true` | Respond only when pinged |
| `requireMention: false` | Always open in that channel |
| Bot-to-bot messaging | Requires `allowBots: "mentions"` on receiving side |

### Config location
```
/data/.openclaw/openclaw.json
```

### Logs
```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

### Gateway management
```bash
openclaw status              # check status
openclaw gateway restart    # restart (confirm first!)
ps aux | grep openclaw-gateway  # is it running?
```

### Validate config
```bash
python3 -m json.tool /data/.openclaw/openclaw.json > /dev/null && echo "valid"
```

### Key memory fix (Honcho)
```json5
plugins: { slots: { memory: "openclaw-honcho" } }
```

### Key config paths
- `agents.defaults.workspace` — agent working directory
- `agents.defaults.model` — primary + fallback models
- `agents.defaults.memorySearch` — embedding provider
- `memory.backend` — `"builtin"` or `"qmd"`
- `plugins.slots.memory` — memory plugin override
- `channels.discord.token` — bot token
- `tools.elevated.enabled` — elevated exec

### Common error fixes
- **"plugin disabled (memory slot)"** → set `plugins.slots.memory`
- **"Port already in use"** → gateway already running, don't restart
- **Embedding 404** → bad `memorySearch.remote.baseUrl` or invalid provider
- **Discord not routing** → format `guildId/channelId`
- **ACP agent not spawning** → run `/acp doctor`, then `/acp spawn codex --bind here`
- **Hook not firing** → `openclaw hooks list`, then `openclaw hooks enable HOOK_NAME`
- **Pairing code expired** → codes expire after 1 hour, max 3 pending per channel

## Architecture overview

Single Gateway daemon (port 18789) owns all messaging surfaces. Agents connect via WebSocket. Three memory backends: builtin (SQLite), QMD (local sidecar), Honcho (cross-session plugin). Multi-agent via `agents.list[]` + `bindings[]`.

## Memory architecture

Three backends:
1. **Builtin** — SQLite + vector search, auto-detects OpenAI/Gemini/Voyage/Mistral keys
2. **QMD** — Local sidecar with reranking, query expansion, extra paths
3. **Honcho** — Plugin `openclaw-honcho`, cross-session with user modeling

Tools: `memory_search` (semantic), `memory_get` (file/lines)
Plus Honcho tools: `honcho_context`, `honcho_ask`, `honcho_search_conclusions`, `honcho_search_messages`, `honcho_session`

**Active memory** (optional): blocking sub-agent that runs before main reply, surfacing relevant memory proactively.

**Dreaming** (experimental): background consolidation with light/deep/REM phases.

## Agent bootstrap files

Injected on first turn of session:
- `AGENTS.md` — operating instructions + memory
- `SOUL.md` — persona, boundaries, tone
- `TOOLS.md` — user-maintained tool notes
- `BOOTSTRAP.md` — one-time first-run ritual
- `IDENTITY.md` — name/emoji
- `USER.md` — user profile
- `HEARTBEAT.md` — periodic task list

## Multi-agent routing

Match order (most-specific wins):
1. `peer` (exact DM/group/channel id)
2. `parentPeer` (thread inheritance)
3. `guildId + roles` (Discord)
4. `guildId`
5. `teamId` (Slack)
6. `accountId` match
7. channel-level (`accountId: "*"`)
8. default agent

## Tool profiles

| Profile | Includes |
|---------|----------|
| `minimal` | `session_status` only |
| `coding` | `group:fs` + `group:runtime` + `group:web` + `group:sessions` + `group:memory` + `cron` + `image` + `image_generate` + `video_generate` |
| `messaging` | `group:messaging` + sessions tools |
| `full` | No restriction |

## Channel DM policies

| Policy | Behavior |
|--------|----------|
| `pairing` (default) | Code → owner approves |
| `allowlist` | Only `allowFrom` list |
| `open` | Allow all (`allowFrom: ["*"]`) |
| `disabled` | Ignore all |

## Gateway restart triggers

**Require restart:** `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`  
**Dynamic (no restart):** `tools.web.search.apiKey`, `agents.defaults.memorySearch.remote`

## CLI essentials

```bash
openclaw status          # gateway health
openclaw plugins list    # plugin status
openclaw memory status   # memory + provider
openclaw agents list     # agents + bindings
openclaw channels status # channel health
openclaw doctor          # diagnose + fix
openclaw doctor --fix    # auto-repair
```

## Message queue modes

| Mode | Behavior |
|------|----------|
| `collect` (default) | Coalesce queued messages into single followup turn |
| `steer` | Inject immediately into current run, cancel pending tools |
| `followup` | Enqueue for next turn after current run ends |
| `steer-backlog` | Steer now AND preserve for followup |

## Streaming modes

- `blockStreamingDefault: "on"|"off"` — default for channel
- `blockStreamingBreak: "text_end"|"message_end"` — chunk boundary flush
- `blockStreamingChunk: {minChars, maxChars}` — chunk size bounds
- `blockStreamingCoalesce: {minChars?, maxChars?, idleMs?}` — merge blocks before send
- Discord `maxLinesPerMessage` (default 17) prevents UI clipping

## Model failover

Two-stage: (1) auth profile rotation within provider → (2) model fallback to next in `agents.defaults.model.fallbacks`. Only persists fallback-owned fields to avoid overwriting manual `/model` changes.

## ACP agents (external coding harnesses)

```bash
/acp spawn codex --bind here     # spawn and bind to current channel
/acp spawn codex --mode persistent --thread auto  # persistent
/acp status                      # check runtime state
/acp cancel                      # stop current turn
/acp close                       # close session + remove bindings
/acp doctor                      # check readiness
```

## References structure

Each skill has a `references/` directory with deep-dive docs. Key ones:
- `openclaw-config/references/gateway-config.md` — full config reference
- `openclaw-config/references/retry.md` — retry policy
- `openclaw-config/references/model-failover.md` — model failover + auth profiles
- `openclaw-memory/references/memory-config.md` — all memory config knobs
- `openclaw-memory/references/memory-builtin.md` — builtin engine details
- `openclaw-memory/references/memory-honcho.md` — Honcho plugin details
- `openclaw-memory/references/dreaming.md` — dreaming system
- `openclaw-agents/references/multi-agent.md` — full multi-agent guide
- `openclaw-channels/references/discord.md` — Discord channel reference
- `openclaw-channels/references/channel-routing.md` — routing rules + session keys
- `openclaw-channels/references/pairing.md` — pairing + node device pairing
- `openclaw-concepts/references/architecture.md` — gateway architecture
- `openclaw-concepts/references/session.md` — session system
- `openclaw-concepts/references/compaction.md` — compaction + memory flush
- `openclaw-concepts/references/streaming.md` — block streaming + chunking
- `openclaw-concepts/references/queue.md` — command queue + lane semantics
- `openclaw-concepts/references/agent-loop.md` — agent loop lifecycle
- `openclaw-concepts/references/soul.md` — SOUL.md personality guide
- `openclaw-concepts/references/system-prompt.md` — system prompt assembly
- `openclaw-concepts/references/taskflow.md` — Task Flow orchestration
- `openclaw-troubleshooting/references/gateway-troubleshooting.md` — deep gateway runbook
- `openclaw-troubleshooting/references/hooks.md` — hook system
- `openclaw-plugins/references/plugin-architecture.md` — plugin system
- `openclaw-tools/references/acp-agents.md` — ACP agent runtime
- `openclaw-tools/references/lobster.md` — Lobster workflow DSL
- `openclaw-providers/references/providers.md` — all providers

Load these for detailed reference when answering complex config questions.
