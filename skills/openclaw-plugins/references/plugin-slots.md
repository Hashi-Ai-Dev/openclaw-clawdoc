# Plugin Slots

OpenClaw uses an **exclusive slot system** for plugins that can only have one active implementation at a time. Each slot has a single winning plugin — attempting to enable two plugins for the same slot causes a conflict.

## Exclusive Slots

| Slot | Kind | Default | Purpose |
|------|------|---------|---------|
| `plugins.slots.memory` | `"memory"` | `memory-core` | Workspace memory, search, citations, dreaming |
| `plugins.slots.contextEngine` | `"context-engine"` | `legacy` | Context window management, compaction |

### How Slots Work

1. Plugins declare a `kind` in their `openclaw.plugin.json` manifest:
   ```json
   { "kind": "memory" }
   ```
2. The config selects which plugin occupies each slot:
   ```json
   {
     "plugins": {
       "slots": {
         "memory": "openclaw-honcho",
         "contextEngine": "legacy"
       }
     }
   }
   ```

### Memory Slot

Controls which plugin provides the memory system (workspace memory files, semantic search, citations, dreaming).

**Common configurations:**

```json
// Use Honcho (self-hosted)
"plugins": {
  "slots": { "memory": "openclaw-honcho" },
  "entries": {
    "openclaw-honcho": {
      "enabled": true,
      "config": { "baseUrl": "http://127.0.0.1:8000" }
    }
  }
}

// Use QMD (local binary)
"plugins": {
  "slots": { "memory": "qmd" },
  "entries": { "qmd": { "enabled": true } }
}

// Use built-in (workspace Markdown files)
"plugins": {
  "slots": { "memory": "memory-core" }
}

// Disable memory plugins entirely
"plugins": {
  "slots": { "memory": "none" }
}
```

### Context Engine Slot

Controls which plugin manages context window strategy (compaction, pruning, context selection).

Default is `"legacy"` — the built-in context engine. Switching this requires a plugin that registers a context engine capability.

## Slot Override Pattern (Honcho Fix)

The most common OpenClaw misconfiguration: both `memory-core` (default) and a custom memory plugin (e.g., `openclaw-honcho`) fight for the memory slot.

**Wrong:**
```json
"plugins": {
  "entries": { "openclaw-honcho": { "enabled": true } }
  // memory slot still points to memory-core — conflict!
}
```

**Correct:**
```json
"plugins": {
  "slots": { "memory": "openclaw-honcho" },
  "entries": { "openclaw-honcho": { "enabled": true } }
}
```

## Bundled Plugins and Slot Defaults

| Plugin | Kind | Default Slot |
|--------|------|-------------|
| `memory-core` | `memory` | `memory` (default winner) |
| `openclaw-honcho` | `memory` | — (must be explicitly selected) |
| `qmd` | `memory` | — (must be explicitly selected) |
| `memory-lancedb` | `memory` | — (install-on-demand) |
| `legacy` (context engine) | `context-engine` | `contextEngine` (default) |

## Disabling Slots

Set a slot to `"none"` to disable all plugins of that kind:

```json
"plugins": { "slots": { "memory": "none" } }
```

This blocks any plugin with `kind: "memory"` from loading, even if present in `plugins.entries`.
