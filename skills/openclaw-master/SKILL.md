---
name: openclaw-master
description: OpenClaw configuration expert and system doctor. Use when answering any OpenClaw question: config audits, plugin integration, memory backends, multi-agent setup, channel configuration, troubleshooting, agent design, CLI commands, provider setup, SOUL.md, streaming, queue modes, model failover, sandbox, Task Flow, Lobster, Diff viewer. Triggers on: "openclaw", "config", "gateway", "agent", "memory", "channel", "plugin", "troubleshoot", "how do I", "how does", "why is", "not working", "error", "cli", "hook", "pairing", "ACP", "streaming", "queue".
---

# OpenClaw Master Reference

Top-level routing skill for OpenClaw questions. Routes to specialized skills.

## Skill map

| Skill | When to use |
|-------|-------------|
| `openclaw-config` | Config audits, gateway keys, secrets, retry, failover |
| `openclaw-memory` | Memory backends, embeddings, active memory, dreaming |
| `openclaw-agents` | Multi-agent, bindings, sandbox, tool policies |
| `openclaw-channels` | Discord, Telegram, WhatsApp, Slack, Signal, Matrix, routing |
| `openclaw-concepts` | Architecture, session, compaction, streaming, queue, bootstrap |
| `openclaw-troubleshooting` | Diagnosis, errors, ACP, hooks, pairing failures |
| `openclaw-plugins` | Plugin slots, installing plugins, context engine |
| `openclaw-tools` | exec, browser, cron, sessions, subagents, ACP, Lobster |
| `openclaw-cli` | CLI commands: status, gateway, plugins, memory, agents |
| `openclaw-providers` | OpenAI, Anthropic, Gemini, Bedrock, Ollama, 40+ more |

## Quick reference

| Situation | Action |
|-----------|--------|
| Config changes | `gateway` tool (`config.get` / `config.patch` / `config.apply`) |
| Plugin install | `clawdhub` or clone to `~/.openclaw/skills/` |
| Validate config | `python3 -m json.tool ~/.openclaw/openclaw.json` |
| Gateway status | `openclaw status` |
| Gateway restart | `openclaw gateway restart` (confirm first!) |

### Config location: `~/.openclaw/openclaw.json`
### Logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

## Common fixes

| Error | Fix |
|-------|-----|
| `plugin disabled (memory slot)` | Set `plugins.slots.memory` |
| `Port already in use` | Gateway running — don't restart |
| Embedding 404 | Bad `memorySearch.remote.baseUrl` |
| Discord silent | `dmPolicy: "pairing"` — approve via `openclaw pairing approve` |
| ACP won't spawn | `/acp doctor` then `/acp spawn codex --bind here` |
| Hook not firing | `openclaw hooks list` → `openclaw hooks enable <name>` |
| Pairing code expired | Codes expire 1h, max 3 pending per channel |

## Architecture

Gateway daemon (port 18789) owns all messaging surfaces. Three memory backends: **builtin** (SQLite), **QMD** (local sidecar), **Honcho** (cross-session plugin). Multi-agent via `agents.list[]` + `bindings[]`.

## Tool profiles

| Profile | Includes |
|---------|----------|
| `minimal` | `session_status` only |
| `coding` | fs + runtime + web + sessions + memory + cron + media |
| `messaging` | messaging tools + sessions |
| `full` | No restriction |

## Memory backends

| Backend | Config key | Best for |
|---------|-----------|----------|
| `builtin` | `memory.backend: "builtin"` | Default, no extras |
| `qmd` | `memory.backend: "qmd"` | Local file indexing |
| `Honcho` | `plugins.slots.memory: "openclaw-honcho"` | Cross-session, hosted |

## Channel DM policies

| Policy | Behavior |
|--------|----------|
| `pairing` (default) | Code → approve via `openclaw pairing approve` |
| `allowlist` | Only `allowFrom` list |
| `open` | Allow all (`allowFrom: ["*"]`) |
| `disabled` | Ignore all |

## Message queue modes

`collect` (default) · `steer` · `followup` · `steer-backlog`

## Gateway restart

**Require restart:** `memory.backend`, `plugins.entries.*.enabled`, `agents.defaults.*`  
**Dynamic:** `tools.web.search.apiKey`, `agents.defaults.memorySearch.remote`

## References

- `openclaw-config/references/gateway-config.md` — full config reference
- `openclaw-memory/references/memory-config.md` — all memory knobs
- `openclaw-agents/references/multi-agent.md` — full multi-agent guide
- `openclaw-channels/references/discord.md` — Discord reference
- `openclaw-channels/references/pairing.md` — pairing flow
- `openclaw-concepts/references/session.md` — session system
- `openclaw-concepts/references/compaction.md` — compaction
- `openclaw-troubleshooting/references/diagnostic-flowchart.md` — triage tree
- `openclaw-tools/references/acp-agents.md` — ACP runtime
- `openclaw-providers/references/providers/index.md` — 50+ provider list
