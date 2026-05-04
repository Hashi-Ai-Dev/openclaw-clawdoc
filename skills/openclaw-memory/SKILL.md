---
name: openclaw-memory
description: OpenClaw memory systems. Use when configuring memory backends (builtin/QMD/Honcho), embedding providers, QMD, Honcho, active memory, dreaming, memory search, hybrid search, BM25, vector search, citations, or memory not working. Triggers on: "memory", "embedding", "QMD", "Honcho", "vector search", "hybrid search", "BM25", "memory config", "active memory", "dreaming", "citations", "recall", "semantic search", "memory backend", "memory not working".
---

# OpenClaw Memory

## Three backends

| Backend | Config | Best for |
|--------|--------|----------|
| **Builtin** (default) | `memory.backend: "builtin"` | Getting started, no extras |
| **QMD** | `memory.backend: "qmd"` + npm install | Local file indexing, BM25 reranking |
| **Honcho** | `plugins.slots.memory: "openclaw-honcho"` | Cross-session, user modeling, hosted |

## Key configs

**Builtin:**
```json
{ "memory": { "backend": "builtin", "citations": "auto" } }
```

**QMD:**
```json
{ "memory": { "backend": "qmd" } }
```
Requires: `npm install -g @tobilu/qmd`

**Honcho (self-hosted):**
```json
{
  "plugins": {
    "slots": { "memory": "openclaw-honcho" },
    "entries": {
      "openclaw-honcho": {
        "enabled": true,
        "config": {
          "workspaceId": "your-workspace",
          "baseUrl": "http://127.0.0.1:8000"
        }
      }
    }
  }
}
```

## Embedding providers

Set via `agents.defaults.memorySearch`:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "openai",
        "model": "text-embedding-3-small"
      }
    }
  }
}
```

Supported: `openai`, `gemini`, `voyage`, `mistral`, `deepinfra`, `bedrock`, `local`. DeepInfra auto-detects when API key resolves; `local` uses a GGUF model via `node-llama-cpp`.

## Active memory

Plugin that blocks before each reply and injects memory context. Enable:
```json
{ "plugins": { "entries": { "active-memory": { "enabled": true } } } }
```

## References

- `references/memory.md` — memory layers, slot override, backend comparison
- `references/memory-builtin.md` — builtin backend detail
- `references/memory-qmd.md` — QMD setup and extra paths
- `references/memory-honcho.md` — Honcho setup and cross-session memory
- `references/honcho-persistence.md` — **Critical:** postgres data_directory, ephemeral storage, backup, and recovery for self-hosted Honcho
- `references/memory-search.md` — hybrid search, MMR, temporal decay, citations
- `references/active-memory.md` — active memory config, query modes
- `references/dreaming.md` — dreaming background consolidation
