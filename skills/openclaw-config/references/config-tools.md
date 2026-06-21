---
summary: "Tools config (policy, profiles, custom provider / base-URL setup)"
read_when:
  - Configuring `tools.*` policy, allowlists, or experimental features
  - Registering custom providers or overriding base URLs
  - Setting up OpenAI-compatible self-hosted endpoints
title: "Tools config"
---

`tools.*` config keys and custom provider / base-URL setup. For agents,
channels, and gateway runtime, see `configuration-reference.md`.

## Tool profiles

`tools.profile` sets a base allowlist before `tools.allow`/`tools.deny`:

> **Note:** Local onboarding defaults new local configs to
> `tools.profile: "coding"` when unset (existing explicit profiles are
> preserved).

| Profile     | Includes |
| ----------- | -------- |
| `minimal`   | `session_status` only |
| `coding`    | `group:fs`, `group:runtime`, `group:web`, `group:sessions`, `group:memory`, `cron`, `image`, `image_generate`, `skill_workshop`, `video_generate` |
| `messaging` | `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status` |
| `full`      | No restriction (same as unset) |

## Tool groups

Tools are grouped by capability. Allow or deny whole groups with
`tools.allow: ["group:fs"]`:

- `group:fs` — `read`, `write`, `edit`, `apply_patch`
- `group:runtime` — `exec`
- `group:web` — `web_fetch`, `web_search`, `browser`
- `group:sessions` — `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`
- `group:memory` — `memory_search`, `memory_get`
- `group:messaging` — `message`
- `group:media` — `image`, `image_generate`, `music_generate`, `video_generate`, `tts`

## Tool allow/deny

```json5
{
  tools: {
    profile: "coding",
    allow: ["group:fs", "group:runtime", "group:web"],
    deny: ["browser_login"], // optional explicit denylist
  },
}
```

`tools.allow` and `tools.deny` are evaluated together. A tool must be in the
profile's include set AND not in the deny list to be available.

## Elevated tools

`tools.elevated.*` controls which tools can run with elevated permissions
(`exec` approval flow):

```json5
{
  tools: {
    elevated: {
      enabled: true,
      approvers: ["YOUR_USER_ID"],
      target: "dm", // or "channel" or "owner"
    },
  },
}
```

## Custom providers and base URLs

`providers.*` lets you register custom OpenAI-compatible endpoints:

```json5
{
  providers: {
    "your-custom-name": {
      baseUrl: "https://your-llm-host.example.com/v1",
      apiKey: "YOUR_PROVIDER_KEY",
      models: [
        { id: "your-model", contextWindow: 200000 },
      ],
    },
  },
}
```

The custom provider's models are then selectable as
`your-custom-name/your-model` in any `model.primary` field.

For the full tool surface, run `openclaw config schema` or use
`config.schema.lookup`.