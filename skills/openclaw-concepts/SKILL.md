---
name: openclaw-concepts
description: OpenClaw core concepts. Use when explaining architecture, memory, sessions, compaction, streaming, multi-agent design, sandboxing, agent bootstrap, message flow, queue modes, model failover, system prompt, SOUL.md, or timezone. Triggers on: "how does it work", "architecture", "session", "compaction", "streaming", "bootstrap", "context", "agent loop", "queue", "message flow", "failover".
---

# OpenClaw Concepts

## Gateway architecture

Single Gateway daemon (port 18789) owns all messaging surfaces. Nodes/clients connect via WebSocket. One gateway per host — only place that opens WhatsApp session.

## Agent bootstrap

Files injected on first turn of each session:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Operating instructions + memory |
| `SOUL.md` | Persona, boundaries, tone |
| `TOOLS.md` | User-maintained tool notes |
| `BOOTSTRAP.md` | One-time first-run ritual (deleted after) |
| `IDENTITY.md` | Name/emoji |
| `USER.md` | User profile |
| `HEARTBEAT.md` | Periodic task list |

## Memory

Three files the agent writes:
- **`MEMORY.md`** — long-term curated facts
- **`memory/YYYY-MM-DD.md`** — daily running notes
- **`DREAMS.md`** — dreaming diary (experimental)

Tools: `memory_search` (semantic), `memory_get` (file/lines). **Active memory** plugin surfaces relevant memory proactively before main reply.

## Session

Transcripts: `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`
- `scope: "per-sender"` — each sender gets isolated session
- `dmScope: "main"` — all DMs share main session key

## Compaction

Chunked summarization when context nears limit. `memoryFlush` runs silent turn before compaction to store durable memories. Post-compaction reinjects `["Session Startup", "Red Lines"]` from AGENTS.md.

## Streaming + chunking

**Block streaming**: emit completed blocks as assistant writes.  
**Preview streaming** (Telegram/Discord/Slack): update temp preview message while generating.

Controls: `blockStreamingDefault`, `blockStreamingBreak`, `blockStreamingCoalesce`. Discord `maxLinesPerMessage` (default 17) prevents UI clipping.

## Queue modes

| Mode | Behavior |
|------|----------|
| `collect` (default) | Coalesce queued messages into single followup turn |
| `steer` | Inject immediately, cancel pending tools after next boundary |
| `followup` | Enqueue for next turn after current run ends |
| `steer-backlog` | Steer now AND preserve for followup |

**Inbound dedupe + debounce**: short-lived cache prevents duplicate runs; rapid messages batched.

## Agent loop

1. Acquire session write lock
2. Resolve model + auth profile
3. Load skills snapshot
4. Assemble system prompt (base + skills + bootstrap)
5. Run `runEmbeddedPiAgent` → stream tool/assistant/lifecycle events
6. On timeout → abort; On error → return usage metadata

Global lane cap + per-session lane serialization prevents tool/session races.

## Model failover

Two-stage: (1) auth profile rotation within provider → (2) model fallback to next in `fallbacks[]`. Only persists fallback-owned fields — avoids overwriting manual `/model` changes.

## System prompt

Built per run: Tooling guidance → Safety reminder → Skills (on-demand) → Self-Update rules → Workspace → Docs path → Date/Time → Runtime → Reasoning visibility.

## SOUL.md

Personality layer in the high-priority instruction slot. Tone, opinions, brevity, humor, boundaries. Short + sharp beats long + vague.

## Sandbox

- `mode: "off|non-main|all"` — when to sandbox
- `scope: "session|agent|shared"` — isolation level
- `workspaceAccess: "none|ro|rw"`
- Docker: Chromium + CDP in container, noVNC URL injected

## Task Flow

Managed multi-step orchestration: **managed** (owns lifecycle) or **mirrored** (observes external tasks). Cancel sticky across restarts.

## References

- `references/architecture.md` — gateway deep dive
- `references/session.md` — session system
- `references/compaction.md` — compaction + memory flush
- `references/streaming.md` — block streaming and preview mode details
- `references/progress-drafts.md` — editable progress messages during long turns
- `references/queue.md` — queue lanes + semantics
- `references/system-prompt.md` — prompt assembly
- `references/soul.md` — SOUL.md guide
- `references/sandboxing.md` — sandbox details
