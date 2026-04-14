---
name: openclaw-plugins
description: OpenClaw plugin system. Use when installing, configuring, debugging, or building plugins; understanding plugin slots, capability model, plugin manifest, SDK entry points, hook system, or plugin allow/deny. Triggers on: "plugin", "plugins install", "plugin slot", "plugin config", "extension", "plugin manifest", "plugin SDK", "channel plugin", "provider plugin", "tool plugin", "hook plugin", "building plugins", "plugin capability", "plugin allow list", "plugin shape", "ClawHub", "npm install", "plugin not loading", "plugin conflict", "disabled plugin", "plugin API", "openclaw plugins".
---

# OpenClaw Plugins

## Plugin system overview

Plugins extend OpenClaw with new capabilities: messaging channels, model providers, speech, media understanding, image/video/music generation, web fetch/search, agent tools, event hooks, or any combination. Published to ClawHub or npm; installed via `openclaw plugins install @scope/plugin-name`.

OpenClaw reads `openclaw.plugin.json` manifest **before loading plugin code** — used for config validation, identity, and capability declarations without booting runtime.

## Capability model

Every native plugin registers against one or more **capability types** via the SDK registration API:

| Capability | Registration method | Example plugins |
|---|---|---|
| Text inference | `api.registerProvider(...)` | `openai`, `anthropic` |
| CLI inference backend | `api.registerCliBackend(...)` | `openai`, `anthropic` |
| Speech | `api.registerSpeechProvider(...)` | `elevenlabs`, `microsoft` |
| Realtime transcription | `api.registerRealtimeTranscriptionProvider(...)` | `openai` |
| Realtime voice | `api.registerRealtimeVoiceProvider(...)` | `openai` |
| Media understanding | `api.registerMediaUnderstandingProvider(...)` | `openai`, `google` |
| Image generation | `api.registerImageGenerationProvider(...)` | `openai`, `google`, `fal`, `minimax` |
| Music generation | `api.registerMusicGenerationProvider(...)` | `google`, `minimax` |
| Video generation | `api.registerVideoGenerationProvider(...)` | `qwen` |
| Web fetch | `api.registerWebFetchProvider(...)` | `firecrawl` |
| Web search | `api.registerWebSearchProvider(...)` | `google` |
| Channel / messaging | `api.registerChannel(...)` | `msteams`, `matrix`, `discord` |

A plugin registering zero capabilities but providing hooks/tools/services is a **legacy hook-only** plugin — fully supported.

### Plugin shapes

OpenClaw classifies every loaded plugin by its actual registration behavior:

- **plain-capability** — exactly one capability type (e.g. `mistral`)
- **hybrid-capability** — multiple capability types (e.g. `openai` = text + speech + media + image)
- **hook-only** — registers only hooks, no capabilities
- **non-capability** — registers tools/commands/services but no capabilities

```bash
openclaw plugins inspect <plugin-id>   # see shape + capability breakdown
```

## Exclusive slots

Some capability kinds map to **exclusive slots** (one plugin owns the slot at a time):

| Slot | Default owner | Override key |
|---|---|---|
| `memory` | `memory-core` | `plugins.slots.memory` |
| `context-engine` | `legacy` | `plugins.slots.contextEngine` |

**Concrete example — swapping memory to Honcho:**

```json5
plugins: {
  slots: { memory: "openclaw-honcho" },  // replaces memory-core
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

After changing a slot you must restart the gateway: `openclaw gateway restart`.

**Never set a slot to a plugin that isn't installed and enabled.** If Honcho isn't in `plugins.entries`, setting `slots.memory: "openclaw-honcho"` will silently disable memory entirely. Always verify with `openclaw plugins list` after a slot change.

## Plugin manifest (`openclaw.plugin.json`)

Every native plugin must ship a manifest in the plugin root. OpenClaw validates config against this schema **before loading code**:

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "description": "Short summary",
  "version": "1.0.0",
  "configSchema": { /* JSON Schema */ },
  "kind": "channel|provider|hook|tool|...",
  "capabilities": ["channel:messaging", "tool:..."],
  "hooks": ["before_agent_start", "before_prompt_build"],
  "setup": { "wizard": "...", "autoEnable": true }
}
```

## SDK entry points

Three helpers for creating plugin entry points:

### `definePluginEntry` — tool/hook/provider plugins
```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
export default definePluginEntry({
  id: "my-plugin",
  name: "My Plugin",
  description: "Short summary",
  register(api) {
    api.registerProvider({ /* ... */ });
    api.registerTool({ /* ... */ });
  },
});
```

### `defineChannelPluginEntry` — messaging channel plugins
```typescript
import { defineChannelPluginEntry } from "openclaw/plugin-sdk/channel-core";
export default defineChannelPluginEntry({
  id: "my-channel",
  name: "My Channel",
  description: "Short summary",
  plugin: myChannelPlugin,
  setRuntime: setMyRuntime,
});
```

### `defineSetupPluginEntry` — setup/onboarding adapters
```typescript
import { defineSetupPluginEntry } from "openclaw/plugin-sdk/setup";
```

## Plugin allow list, deny list, and entries — what's the difference?

```json5
plugins: {
  allow: ["plugin-id", "@scope/plugin-name"],   // only these non-bundled plugins can load
  deny:  ["some-plugin"],                         // block specific plugins even if discovered
  entries: {
    "my-plugin": { enabled: true, config: {} }  // per-plugin config lives here
  }
}
```

**`allow`** — If set to a non-empty array, only plugins whose IDs are listed may auto-load. Unlisted non-bundled plugins are blocked. If set to `[]` (empty), any discovered plugin may try to load. Bundled plugins ignore this list entirely (`discord`, `minimax`, `browser`, `active-memory`, `brave`, `diffs`, `llm-task`, `lobster`, `memory-core`).

**`deny`** — Explicit blocklist applied after `allow`. Use this to quiet a plugin that would otherwise auto-load. Does not require the plugin to be in `allow`.

**`entries`** — Per-plugin runtime configuration (enabled flag, config object, workspace binding). A plugin can be in `entries` without being in `allow` if it's bundled. A non-bundled plugin must be in `allow` to load even if it has an `entries` config.

**Never use `deny` as your primary control mechanism.** The primary gate is `allow`. Use `deny` only as a targeted exception for auto-discovered plugins you'd otherwise permit.

## Installing + verifying plugins

```bash
openclaw plugins install @scope/plugin-name
openclaw plugins list           # verify loaded
openclaw plugins inspect <id>   # shape + capabilities
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

## Hook system

Hooks fire on lifecycle events. Place hook files in `~/.openclaw/hooks/` or register via SDK:

```bash
openclaw hooks list              # list all hooks
openclaw hooks info HOOK_NAME   # check config
openclaw hooks enable HOOK_NAME # enable if disabled
openclaw hooks disable HOOK_NAME
```

Built-in hooks:
- `before_agent_start` — legacy, prefer `before_model_resolve`
- `before_model_resolve` — override model/provider
- `before_prompt_build` — mutate prompt
- `session:compact:before` — pre-compaction memory flush
- `gateway:startup` — post-startup initialization
- `message:received` — inbound message interception

## Legacy hooks guidance

`before_agent_start` is still supported but documented as legacy. For new plugin work:
- Use `before_model_resolve` for model/provider override
- Use `before_prompt_build` for prompt mutation

## Context engine slot

The `contextEngine` slot controls how session context is assembled. Default (`legacy`) uses the classic compaction path. Override via:

```json5
plugins: {
  slots: { contextEngine: "my-engine" }
}
```

## Building your own plugin

See full walkthrough at `references/building-plugins.md`. Quick start:

```bash
mkdir my-plugin && cd my-plugin
pnpm init
pnpm add openclaw/plugin-sdk
```

Key steps:
1. Create `openclaw.plugin.json` manifest
2. Write `src/index.ts` with `definePluginEntry` or `defineChannelPluginEntry`
3. Build with `pnpm build`
4. Publish to ClawHub or npm

## Common plugin errors

| Error | Cause | Fix |
|---|---|---|
| `plugin disabled (memory slot set to X)` | Slot occupied by another plugin | Check `plugins.slots` + `plugins.entries` — only one plugin can own a slot |
| Plugin not loading | Not in `allow` list | Add to `plugins.allow`; verify with `openclaw plugins list` |
| Config validation fail on startup | Missing/invalid `openclaw.plugin.json` | Check manifest schema; see `references/plugin-manifest.md` |
| `openclaw plugins list` empty after install | Gateway not restarted for new plugin | Restart gateway |
| Slot set but plugin not in `entries` | Slot points to plugin that has no config | Add plugin to `plugins.entries` with `enabled: true` first |
| Plugin loads but capability not working | Wrong shape or capability not registered | Run `openclaw plugins inspect <id>` to check registered capabilities |

## References

- `references/plugin-architecture.md` — deep capability model, shapes, load pipeline
- `references/plugin-manifest.md` — full manifest schema
- `references/plugin-slots.md` — slot system details
- `references/plugin-config.md` — plugin config patterns
- `references/sdk-entrypoints.md` — type signatures for all entry helpers
- `references/sdk-channel-plugins.md` — channel plugin building guide
- `references/sdk-provider-plugins.md` — provider plugin building guide
- `references/sdk-overview.md` — SDK import map + registration API
- `references/building-plugins.md` — first plugin tutorial
- `references/sdk-migration.md` — migrating legacy plugins
- `references/sdk-testing.md` — testing strategy
- `references/exec-approvals.md` — exec approval hook integration
- `references/webhooks.md` — inbound webhook configuration
- `references/bundles.md` — compatible bundle formats (Codex, Claude, Cursor)
