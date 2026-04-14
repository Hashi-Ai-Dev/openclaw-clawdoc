---
name: openclaw-plugins
description: OpenClaw plugin system. Use when installing, configuring, debugging plugins, or understanding plugin slots. Triggers on: "plugin", "install plugin", "plugin slot", "plugin config", "extension".
---

# OpenClaw Plugins

## Plugin architecture

- Plugins declare a `kind` field
- Some kinds map to **exclusive slots** (one plugin owns the slot):
  - `memory` → slot owner is `memory-core` by default
  - `contextEngine` → slot owner is `legacy`
- Slot override: `plugins.slots.memory = "plugin-id"`
- Bundled plugins: `discord`, `minimax`, `browser`, `active-memory`, `brave`, `diffs`, `llm-task`, `lobster`, `memory-core`

## Plugin allow list

```json5
plugins: {
  allow: ["plugin-id", "@scope/plugin-name"]
}
```
If empty, discovered non-bundled plugins may auto-load.

## Installing plugins

```bash
openclaw plugins install @scope/plugin-name
openclaw plugins list  # verify
```

## Plugin config location

All plugin config lives under `plugins.entries[<pluginId>].config`:

```json5
plugins: {
  entries: {
    "openclaw-honcho": {
      enabled: true,
      config: {
        workspaceId: "openclaw",
        baseUrl: "http://127.0.0.1:8000"
      }
    }
  }
}
```

## Active memory plugin

The `active-memory` plugin provides `memory_search` and `memory_get` tools.

Config under `plugins.entries["active-memory"].config`:
- `matchAgents`: agent IDs to target
- Other memory settings

## Honcho plugin (memory slot override)

```json5
plugins: {
  slots: { memory: "openclaw-honcho" },
  entries: {
    "openclaw-honcho": {
      enabled: true,
      config: {
        workspaceId: "openclaw",
        baseUrl: "http://127.0.0.1:8000"
      }
    }
  }
}
```

## Building plugins

SDK docs: `/openclaw/docs/plugins/` (sdk-overview, sdk-channel-plugins, sdk-agent-harness, etc.)

## References

- `references/plugin-slots.md` — slot system explained
- `references/plugin-config.md` — plugin config patterns
