---
name: openclaw-memory
description: OpenClaw memory systems. Use when configuring memory backends, embedding providers, QMD, Honcho, or memory search. Triggers on: "memory", "memory search", "embedding", "QMD", "Honcho", "sqlite-vec", "vector search", "BM25", "hybrid search", "memory config".
---

# OpenClaw Memory

Memory systems reference. Three backends available.

## Backends

| Backend | Plugin | Best for |
|---------|--------|---------|
| **Builtin** | `memory-core` | Default, auto-detects embeddings |
| **QMD** | — | Reranking, query expansion, external paths |
| **Honcho** | `openclaw-honcho` | Cross-session, user modeling |

## Quick enable

### Honcho (recommended for cross-session)
```json5
plugins: {
  slots: { memory: "openclaw-honcho" },
  entries: {
    "openclaw-honcho": {
      enabled: true,
      config: {
        workspaceId: "openclaw",
        baseUrl: "http://127.0.0.1:8000"  // self-hosted
      }
    }
  }
}
```

### QMD
```json5
memory: { backend: "qmd" }
```

### Builtin (default, no config needed)
Works automatically with OpenAI/Gemini/Voyage/Mistral API keys.

## Embedding providers

| Provider | ID | Auto | Notes |
|----------|-----|------|-------|
| OpenAI | `openai` | ✅ | `text-embedding-3-small` default |
| Gemini | `gemini` | ✅ | Supports multimodal |
| Voyage | `voyage` | ✅ | |
| Mistral | `mistral` | ✅ | |
| Ollama | `ollama` | ❌ | Set explicitly |
| Local | `local` | ✅ (first) | GGUF model, ~0.6GB |
| Bedrock | `bedrock` | ✅ | AWS SDK credential chain |

Auto-detect order: local → openai → gemini → voyage → mistral → bedrock

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

## Citations
```json5
memory.citations: "auto"  // "auto" | "on" | "off"
```
- `auto`: include footer when path available
- `on`: always include
- `off`: omit footer

## QMD extra paths
```json5
memory: {
  backend: "qmd",
  qmd: {
    paths: [{ name: "docs", path: "~/notes", pattern: "**/*.md" }]
  }
}
```

## CLI
```bash
openclaw memory status      # check index + provider
openclaw memory search "q"  # CLI search
openclaw memory index --force  # rebuild
```

## References

- `references/memory-config.md` — full config reference (all knobs)
- `references/memory-backends.md` — detailed backend comparison
- `references/embedding-providers.md` — provider setup details
