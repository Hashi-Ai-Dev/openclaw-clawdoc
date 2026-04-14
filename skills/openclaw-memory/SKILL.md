---
name: openclaw-memory
description: OpenClaw memory systems. Use when configuring memory backends, embedding providers, QMD, Honcho, active memory, dreaming, memory-wiki, or memory search. Triggers on: "memory", "memory search", "embedding", "QMD", "Honcho", "sqlite-vec", "vector search", "BM25", "hybrid search", "memory config", "active memory", "dreaming", "memory wiki", "citations", "recall", "context", "semantic search", "vector", "pgvector", "memory not working", "search results wrong", "vector database", "memory backend".
---

# OpenClaw Memory

OpenClaw memory spans three layers: **what files get written**, **which backend indexes them**, and **how search retrieves results**. Getting any one of those wrong means broken recall.

## Layer map

| Layer | Lives under | What it does |
|---|---|---|
| **Memory files** | `~/.openclaw/workspace/` | `MEMORY.md`, `memory/YYYY-MM-DD.md`, `DREAMS.md` |
| **Active memory backend** | `plugins.slots.memory` + `memory.backend` | Which plugin owns recall/search |
| **Search config** | `agents.defaults.memorySearch` | Which embedding provider, hybrid weights, MMR, decay |
| **Memory-wiki** | `plugins.entries.memory-wiki` | Optional compiled knowledge vault layer |

---

## The slot override: `plugins.slots.memory`

Every memory backend is selected through `plugins.slots.memory`. This is the single override point — you set the slot once, and all three backends plug in through it.

```json5
plugins: {
  slots: { memory: "memory-core" },  // default — builtin SQLite
  // slots: { memory: "openclaw-honcho" }  // Honcho
  // slots: { memory: "none" }  // disable memory plugins entirely
}
```

**⚠️ Never set `plugins.slots.memory` for Honcho.** Honcho registers its own tools (`honcho_context`, `honcho_search_conclusions`, `honcho_search_messages`, `honcho_session`, `honcho_ask`) directly — it does NOT replace `memory_search` and does NOT use the `memory` slot. Setting `slots.memory: "openclaw-honcho"` is wrong for Honcho. Leave `slots.memory` at its default (`memory-core`) when using Honcho. The Honcho config goes in `plugins.entries["openclaw-honcho"]` only. See [Honcho setup](#honcho) below.

---

## Three backends

### Builtin (default) — `memory-core`

No config needed. Auto-detects any OpenAI/Gemini/Voyage/Mistral/Bedrock API key and enables hybrid search.

```json5
plugins: { slots: { memory: "memory-core" } }
```

Best for: getting started, simple single-agent setups.

### QMD — local reranking sidecar

```json5
memory: { backend: "qmd" }
plugins: { slots: { memory: "memory-core" } }  // QMD hooks through memory-core
```

Adds: BM25 + vector reranking, query expansion, indexing of paths outside workspace, session transcript recall.

Prerequisites: `npm install -g @tobilu/qmd` (or `bun install -g @tobilu/qmd`), QMD on `PATH`.

QMD home: `~/.openclaw/agents/<agentId>/qmd/`. OpenClaw manages collection lifecycle automatically. Falls back to builtin if QMD is unavailable.

### Honcho — cross-session, user modeling

```json5
plugins: {
  slots: { memory: "openclaw-honcho" },
  entries: {
    "openclaw-honcho": {
      enabled: true,
      config: {
        workspaceId: "openclaw",        // memory isolation namespace
        baseUrl: "http://127.0.0.1:8000" // self-hosted; omit for managed
        // apiKey: "..."                 // only for managed api.honcho.dev
      }
    }
  }
}
```

| Hosting | `baseUrl` | `apiKey` |
|---|---|---|
| Self-hosted | `http://127.0.0.1:8000` (or your host) | omit |
| Managed (api.honcho.dev) | omit (defaults to managed) | required |

Tools registered: `honcho_context`, `honcho_search_conclusions`, `honcho_search_messages`, `honcho_session`, `honcho_ask`.

Honcho vs QMD vs builtin:

| | Builtin/QMD | Honcho |
|---|---|---|
| Storage | Workspace Markdown | Dedicated service (local or hosted) |
| Cross-session | Via memory files | Automatic after every turn |
| User modeling | Manual | Automatic profiles |
| Search | Vector + keyword hybrid | Semantic over observations |
| Multi-agent | Not tracked | Parent/child awareness |
| Tools | `memory_search`, `memory_get` | `honcho_*` + `memory_*` |
| Install | Built-in (builtin) / npm (QMD) | Plugin |

---

## Embedding providers

Configured under `agents.defaults.memorySearch`, used by builtin and QMD backends.

| Provider | ID | Auto | Notes |
|----------|-----|------|-------|
| OpenAI | `openai` | ✅ | `text-embedding-3-small` default |
| Gemini | `gemini` | ✅ | Supports multimodal (image + audio) |
| Voyage | `voyage` | ✅ | |
| Mistral | `mistral` | ✅ | |
| Ollama | `ollama` | ❌ | Set explicitly |
| Local | `local` | ✅ (first) | GGUF model, ~0.6GB auto-download |
| Bedrock | `bedrock` | ✅ | AWS SDK credential chain, no API key |

Auto-detect order: `local` → `openai` → `gemini` → `voyage` → `mistral` → `bedrock`

**Pinning a provider** (recommended for production):

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      // fallback: "gemini"  // optional failover
    }
  }
}
```

---

## Memory search config

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      query: {
        hybrid: {
          enabled: true,
          vectorWeight: 0.7,
          textWeight: 0.3,
          mmr: { enabled: true, lambda: 0.7 },
          temporalDecay: { enabled: true, halfLifeDays: 30 }
        }
      }
    }
  }
}
```

Key knobs:
- **`vectorWeight`/`textWeight`**: blend vector similarity + BM25. Defaults 0.7/0.3.
- **`mmr.enabled`**: diversity reranking — prevents near-duplicate results from dominating.
- **`temporalDecay.enabled`**: recency boost. Evergreen files (`MEMORY.md`, non-dated) never decayed.

---

## Citations

Controls whether search snippets include a `Source: <path#line>` footer appended to the snippet text.

```json5
memory.citations: "auto"  // "auto" | "on" | "off"
```

| Value | Behavior |
|-------|----------|
| `auto` | Include footer when path is available |
| `on` | Always include |
| `off` | Omit footer (path still passed to agent internally) |

Applies to all backends. Not specific to QMD — `memory.citations` is a top-level memory config key.

**What citations look like in practice:**
```
"...the gateway restart is required after config changes..."
Source: memory/2026-04-14.md#12
```
Citations are footer-only — they do not appear inline (e.g. `[1]` style). They tell the agent which file and line to read for verification, but the agent must call `memory_get` to retrieve the actual content.

---

## QMD extra paths and extraCollections

**Extra paths** (all backends via `memorySearch.extraPaths`):

```json5
agents: {
  defaults: {
    memorySearch: {
      extraPaths: ["../team-docs", "/srv/shared-notes"]
    }
  }
}
```

**QMD-only extra collections** (preserves explicit collection names for cross-agent sharing):

```json5
agents: {
  defaults: {
    memorySearch: {
      qmd: {
        extraCollections: [
          { name: "team-notes", path: "~/team-notes", pattern: "**/*.md" }
        ]
      }
    }
  }
}
```

`extraCollections` uses the same `{ name, path, pattern? }` shape as `memory.qmd.paths`, but is merged per-agent and can preserve explicit shared collection names when the path is outside the current workspace. If the same resolved path appears in both, QMD keeps the first and skips the duplicate.

---

## Active memory

A plugin-owned blocking sub-agent that runs **before the main reply** for eligible interactive sessions. It searches memory and injects a compact summary as hidden system context.

Not a backend — an enrichment layer on top of any backend.

```json5
plugins: {
  entries: {
    "active-memory": {
      enabled: true,
      config: {
        agents: ["main"],           // which agents can use it
        allowedChatTypes: ["direct"], // direct | group | channel
        queryMode: "recent",        // message | recent | full
        promptStyle: "balanced",    // balanced | strict | contextual | recall-heavy | precision-heavy | preference-only
        timeoutMs: 15000,
        maxSummaryChars: 220,
        modelFallback: "google/gemini-3-flash",
        logging: true
      }
    }
  }
}
```

Query modes:
- **`message`**: latest user message only. Fastest, strongest preference bias.
- **`recent`** (default): user message + small conversational tail. Balanced.
- **`full`**: entire conversation. Highest recall quality, slowest.

Prompt styles control how eagerly the sub-agent returns memory vs `NONE`. `balanced` is the default for `recent`. `preference-only` is tuned for habits, tastes, stable facts.

Session toggle (no config restart):
```
/active-memory status
/active-memory off
/active-memory on
```

Debug in session:
```
/verbose on   → shows Active Memory status line after reply
/trace on     → shows the recalled memory content
```

---

## Dreaming (experimental)

Background consolidation: collects short-term signals → scores → promotes qualified items to `MEMORY.md`. Disabled by default.

```json5
plugins: {
  entries: {
    "memory-core": {
      config: {
        dreaming: {
          enabled: true,
          frequency: "0 3 * * *"  // cron; default 3am
        }
      }
    }
  }
}
```

Three phases (internal):
- **Light**: ingest + dedupe recent signals, no durable write
- **Deep**: rank candidates, promote to `MEMORY.md`
- **REM**: extract themes and reflections, no durable write

Output:
- Machine state: `memory/.dreams/`
- Human diary: `DREAMS.md` (or existing `dreams.md`)

CLI:
```bash
openclaw memory promote              # preview promotion candidates
openclaw memory promote --apply      # apply promotions
openclaw memory promote-explain "q"  # why/why-not a specific candidate
openclaw memory rem-harness          # preview REM + deep output (no write)
openclaw memory rem-backfill --path ./memory --stage-short-term  # historical replay
openclaw memory rem-backfill --rollback
```

---

## Memory Wiki

A **separate layer** from the active memory backend. Compiles durable knowledge into a provenance-rich wiki vault.

Does **not** replace `memory-core`, QMD, or Honcho. Those still own recall, promotion, and search. Memory Wiki adds wiki-native pages, structured claims, dashboards, and `wiki_search`/`wiki_get`/`wiki_apply`/`wiki_lint` tools.

```json5
plugins: {
  entries: {
    "memory-wiki": {
      enabled: true,
      config: {
        vaultMode: "isolated",   // isolated | bridge | unsafe-local
        vault: { path: "~/.openclaw/wiki/main", renderMode: "obsidian" },
        bridge: { enabled: false },  // import from active memory plugin
        search: { backend: "shared", corpus: "wiki" },
        render: { createDashboards: true, createBacklinks: true }
      }
    }
  }
}
```

**Vault modes:**
- `isolated`: own curated vault, no dependencies
- `bridge`: reads public artifacts from the active memory plugin (exports, dream reports, daily notes)
- `unsafe-local`: experimental same-machine escape hatch for private local paths

**Recommended hybrid pattern**: QMD for active recall + `memory-wiki` in `bridge` mode for synthesized knowledge pages.

CLI:
```bash
openclaw wiki status
openclaw wiki doctor
openclaw wiki ingest ./notes/alpha.md
openclaw wiki compile
openclaw wiki lint
openclaw wiki search "alpha"
```

---

## CLI

```bash
openclaw memory status          # check index + provider
openclaw memory status --deep   # detailed diagnostics
openclaw memory search "q"      # CLI search
openclaw memory index --force   # rebuild index
openclaw memory promote         # preview dreaming promotion
openclaw memory promote --apply
openclaw memory promote-explain "query"
openclaw memory rem-harness
openclaw memory rem-backfill --path ./memory
```

---

## References

- `references/memory-overview.md` — file layout, memory files, tools, wiki layer, compaction interaction
- `references/memory-config.md` — all config knobs: provider selection, hybrid search, MMR, decay, QMD, multimodal, dreaming
- `references/memory-builtin.md` — builtin SQLite engine: indexing, sqlite-vec, extraPaths, troubleshooting
- `references/memory-qmd.md` — QMD sidecar: install, collections, extraCollections, sessions, scope, fallback
- `references/memory-honcho.md` — Honcho: setup, tools, user modeling, vs builtin comparison, migration
- `references/memory-search.md` — search pipeline: hybrid flow, provider comparison, MMR, decay, multimodal, session indexing
- `references/active-memory.md` — full active memory reference: gates, query modes, prompt styles, model fallback, transcript persistence, debugging
- `references/dreaming.md` — full dreaming reference: phases, signals, scheduling, CLI, grounded backfill, Dreams UI
