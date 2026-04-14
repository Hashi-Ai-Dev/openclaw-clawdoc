---
name: openclaw-concepts
description: OpenClaw core concepts. Use when explaining architecture, memory, sessions, compaction, streaming, multi-agent design, sandboxing, agent bootstrap, message flow, queue modes, model failover, system prompt, SOUL.md, or timezone. Triggers on: "how does it work", "architecture", "session", "compaction", "streaming", "bootstrap", "context", "agent loop", "queue", "message flow", "failover".
---

# OpenClaw Concepts

## Gateway architecture

- **Single long-lived Gateway** owns all messaging surfaces (WhatsApp/Baileys, Telegram/grammY, Slack, Discord, Signal, iMessage, WebChat)
- **Control clients** (macOS app, CLI, web UI) connect over WebSocket on port 18789
- **Nodes** (macOS/iOS/Android/headless) connect over WebSocket with `role: node`
- One Gateway per host — only place that opens WhatsApp session
- Canvas served at `/__openclaw__/canvas/` and `/__openclaw__/a2ui/` on same port

## Agent bootstrap

OpenClaw injects these files into agent context on first turn of each session:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Operating instructions + memory |
| `SOUL.md` | Persona, boundaries, tone |
| `TOOLS.md` | User-maintained tool notes |
| `BOOTSTRAP.md` | One-time first-run ritual (deleted after) |
| `IDENTITY.md` | Agent name/emoji |
| `USER.md` | User profile |
| `HEARTBEAT.md` | Periodic task清单 |

## Memory

Three files the agent writes to:

- **`MEMORY.md`** — long-term durable facts/preferences
- **`memory/YYYY-MM-DD.md`** — daily running notes
- **`DREAMS.md`** — dreaming diary (experimental)

Tools: `memory_search` (semantic), `memory_get` (specific file/lines)

**Active memory** (optional plugin): a blocking sub-agent that runs before the main reply for eligible sessions, surfacing relevant memory proactively. Enable via `plugins.entries.active-memory`.

**Dreaming** (experimental): background memory consolidation with light/deep/REM phases that promote short-term signals into `MEMORY.md`.

## Session

Session transcripts stored as JSONL at:
`~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

Session grouping:
- `scope: "per-sender"` — each sender gets isolated session in channel
- `dmScope: "main"` — all DMs share main session key

## Compaction

Chunked summarization when context nears token limit:
- `mode: "safeguard"` — chunked summarization for long histories
- `memoryFlush` runs silent turn before compaction to store durable memories
- Post-compaction reinjects `["Session Startup", "Red Lines"]` AGENTS.md sections

## Streaming + chunking

Two separate layers:

1. **Block streaming**: emit completed blocks as assistant writes (channel messages, not token deltas)
2. **Preview streaming** (Telegram/Discord/Slack): update a temporary preview message while generating

Controls:
- `blockStreamingDefault: "on"|"off"` — channel default
- `blockStreamingBreak: "text_end"|"message_end"` — when to flush chunks
- `blockStreamingChunk: {minChars, maxChars}` — chunk size bounds
- `blockStreamingCoalesce: {minChars?, maxChars?, idleMs?}` — merge consecutive blocks before send
- Discord `maxLinesPerMessage` (default 17) prevents UI clipping

## Message flow + queueing

```
Inbound message → routing/bindings → session key → queue → agent run → outbound
```

**Queue modes** (per channel, steer how inbound messages interact with active runs):
- `collect`: coalesce all queued messages into a single followup turn (default)
- `steer`: inject immediately into current run (cancel pending tools after next boundary)
- `followup`: enqueue for next turn after current run ends
- `steer-backlog`: steer now AND preserve for followup turn

**Inbound dedupe**: short-lived cache prevents duplicate agent runs from channel reconnects.

**Inbound debounce**: rapid consecutive messages from same sender batched into one turn (`debounceMs`).

## Agent loop

Serialized per-session run that:
1. Acquires session write lock
2. Resolves model + auth profile
3. Loads skills snapshot
4. Assembles system prompt from base + skills + bootstrap
5. Runs `runEmbeddedPiAgent` → streams tool/assistant/lifecycle events
6. On timeout → aborts run
7. On lifecycle end/error → returns usage metadata

Concurrency: global lane cap (`maxConcurrent`) + per-session lane serialization prevents tool/session races.

## Model failover

Two-stage fallback:
1. **Auth profile rotation** within current provider (cooldowns per profile)
2. **Model fallback** to next model in `agents.defaults.model.fallbacks`

Runtime persists only the fallback-owned fields (`providerOverride`, `modelOverride`, `authProfileOverride`) to avoid overwriting manual `/model` changes during retry.

## System prompt

OpenClaw builds a custom prompt per run (not the pi-coding-agent default). Fixed sections:
- **Tooling**: structured-tool reminder + runtime guidance (cron for future work, exec/process for background commands, sessions_spawn for large tasks)
- **Safety**: short guardrail reminder (advisory, not enforced)
- **Skills**: on-demand skill loading
- **OpenClaw Self-Update**: config tools (`config.patch`, `config.apply`, `update.run` only on explicit request)
- **Workspace**: working directory
- **Documentation**: local docs path
- **Current Date & Time**: user-local timezone
- **Runtime**: host/OS/node/model/repo root
- **Reasoning**: visibility level + /reasoning toggle

## SOUL.md

`SOUL.md` is the personality layer. It goes in the high-priority instruction slot — not buried in the user turn.

What goes in it: tone, opinions, brevity, humor, boundaries, bluntness defaults.
What doesn't: life story, changelog, security policy dump.

Short + sharp beats long + vague. Use the Molty prompt to rewrite it with actual personality.

## Timezone

- Message envelopes: host-local by default, configurable via `envelopeTimezone: "local"|"utc"|"user"|IANA`
- `envelopeElapsed: "on"|"off"` controls elapsed time suffixes
- `agents.defaults.userTimezone` tells the model the user's timezone

## Usage tracking

- Pulls provider usage/quota directly from their APIs (not estimates)
- Shows in `/status`, `/usage`, `openclaw status --usage`
- Supports: Anthropic (OAuth), GitHub Copilot (OAuth), Gemini CLI (OAuth), OpenAI Codex (OAuth), MiniMax (API key or OAuth), Xiaomi MiMo, z.ai
- Hidden when no usable auth resolved

## Tool policies + profiles

**Profiles** (`minimal`, `coding`, `messaging`, `full`):
- `coding`: fs + runtime + web + sessions + memory + cron + media
- `minimal`: session_status only

**Tool groups**: `fs`, `runtime`, `web`, `sessions`, `memory`, `automation`, `messaging`, `ui`, `media`, `nodes`

**Exec approvals**: `tools.exec.ask: "off|on-miss|always"` controls interactive exec approval. On channels with native approval cards, agent uses those first.

## Sandbox

- `mode: "off|non-main|all"` — when to sandbox
- `scope: "session|agent|shared"` — isolation level
- `workspaceAccess: "none|ro|rw"` — agent workspace access
- `backend: "docker|ssh|openshell"`
- Sandboxed browser: Chromium + CDP in container, noVNC URL injected

## Task Flow

Managed multi-step flow orchestration above background tasks:
- **Managed mode**: Task Flow owns lifecycle end-to-end, creates tasks as flow steps
- **Mirrored mode**: observes external tasks, tracks progress without owning creation
- Cancel is sticky across restarts (`openclaw tasks flow cancel`)

## OpenAI Chat Completions API

Gateway can serve an OpenAI-compatible HTTP endpoint (`POST /v1/chat/completions`) when enabled. Runs through the same agent codepath as `openclaw agent`, so routing/permissions/config match. Treat as **full operator-access surface** — no per-user tool boundary.

## References

- `references/architecture.md` — gateway architecture
- `references/session.md` — session system
- `references/compaction.md` — compaction + memory flush
- `references/streaming.md` — block streaming + chunking details
- `references/messages.md` — message flow, sessions, queueing
- `references/agent-loop.md` — agent loop lifecycle
- `references/queue.md` — command queue + lane semantics
- `references/model-failover.md` — model failover + auth profile rotation
- `references/system-prompt.md` — system prompt assembly
- `references/soul.md` — SOUL.md personality guide
- `references/timezone.md` — timezone handling
- `references/usage-tracking.md` — usage tracking surfaces
- `references/sandboxing.md` — sandbox details
- `references/rpc.md` — RPC reference
