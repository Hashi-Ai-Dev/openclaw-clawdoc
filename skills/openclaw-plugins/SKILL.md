---
name: openclaw-plugins
description: OpenClaw plugin system. Use when installing, configuring, debugging, or building plugins; understanding plugin slots, capability model, plugin manifest, SDK entry points, hook system, or plugin allow/deny. Triggers on: "plugin", "plugins install", "plugin slot", "plugin config", "extension", "plugin manifest", "plugin SDK", "channel plugin", "provider plugin", "tool plugin", "hook plugin", "building plugins", "plugin capability", "plugin allow list", "plugin shape", "ClawHub", "npm install", "plugin not loading", "plugin conflict", "disabled plugin", "plugin API", "openclaw plugins".
---

# OpenClaw Plugins

## Plugin basics

Plugins extend OpenClaw: channels, model providers, speech, media, image/video/music generation, web fetch/search, tools, hooks. Install via `openclaw plugins install @scope/plugin-name`.

## Exclusive slots

| Slot | Default | Override key |
|------|---------|--------------|
| `memory` | `memory-core` | `plugins.slots.memory` |
| `contextEngine` | `legacy` | `plugins.slots.contextEngine` |

**Swapping memory to Honcho:**
```json5
plugins: {
  slots: { memory: "openclaw-honcho" },
  entries: { "openclaw-honcho": { enabled: true, config: { baseUrl: "http://127.0.0.1:8000" } } }
}
```
Restart gateway after. Never set a slot to a plugin not in `entries`.

## Allow / deny / entries

```json5
plugins: {
  allow: ["plugin-id"],       // non-bundled plugins — empty = any discovered
  deny: ["some-plugin"],      // block after allow check
  entries: {                  // per-plugin config
    "my-plugin": { enabled: true, config: {} }
  }
}
```
Bundled plugins (`discord`, `minimax`, `browser`, `active-memory`, `brave`, `diffs`, `llm-task`, `lobster`, `memory-core`) ignore `allow`.

## Installing + verifying

```bash
openclaw plugins install @scope/plugin-name
openclaw plugins list            # verify loaded
openclaw plugins inspect <id>    # shape + capabilities
```

## Hook system

```bash
openclaw hooks list              # all hooks
openclaw hooks enable HOOK_NAME  # enable
openclaw hooks disable HOOK_NAME
```

Built-in hooks: `before_agent_start`, `before_model_resolve`, `before_prompt_build`, `session:compact:before`, `gateway:startup`, `message:received`

## Common errors

| Error | Fix |
|-------|-----|
| `plugin disabled (memory slot set to X)` | Only one plugin per slot — check `plugins.slots` |
| Plugin not loading | Add to `plugins.allow`; restart gateway |
| Config validation fail | Check `openclaw.plugin.json` manifest schema |
| Slot set but no entry | Add plugin to `plugins.entries` first |

## References

- `references/plugin-architecture.md` — capability model, shapes, load pipeline
- `references/plugin-manifest.md` — full manifest schema
- `references/building-plugins.md` — first plugin tutorial
- `references/sdk-overview.md` — SDK import map + registration API
- `references/sdk-runtime.md` — runtime registration API
- `references/exec-approvals.md` — exec approval hooks
