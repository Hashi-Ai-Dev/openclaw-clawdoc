---
summary: "Agent defaults, multi-agent routing, session, messages, and talk config keys"
read_when:
  - Tuning agent defaults (models, thinking, workspace, heartbeat, media, skills)
  - Configuring multi-agent routing and bindings
  - Adjusting session, message delivery, and talk-mode behavior
title: "Agents config"
---

Agent-scoped configuration keys under `agents.*`, `session.*`, and `messages.*`.
For channels, tools, gateway runtime, and other top-level keys, see
`configuration-reference.md`.

## Agent defaults

The `agents.defaults.*` block sets baseline behavior for every agent that
doesn't override it.

### `agents.defaults.workspace`

Default: `OPENCLAW_WORKSPACE_DIR` when set, otherwise `~/.openclaw/workspace`.

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

An explicit `agents.defaults.workspace` value takes precedence over the
`OPENCLAW_WORKSPACE_DIR` env var.

### `agents.defaults.model.primary`

The default model used when an agent doesn't specify one.

```json5
{
  agents: { defaults: { model: { primary: "YOUR_DEFAULT_MODEL" } } },
}
```

### `agents.defaults.model.fallback`

A fallback model list used when the primary model errors or is rate-limited.

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "YOUR_DEFAULT_MODEL",
        fallback: ["anthropic/claude-sonnet", "openai/gpt-4o"],
      },
    },
  },
}
```

### `agents.defaults.skills`

Restrict which skills an agent loads. Defaults to "all routable skills."

```json5
{
  agents: { defaults: { skills: ["openclaw-master", "openclaw-config"] } },
}
```

### `agents.defaults.thinking`

Per-agent thinking level: `off`, `low`, `medium`, `high`, `adaptive`.

```json5
{ agents: { defaults: { thinking: "medium" } } }
```

## Multi-agent

`agents.list` declares multiple agents. Each entry is a separate identity with
its own workspace, model, and bindings.

```json5
{
  agents: {
    list: [
      { id: "main", default: true, workspace: "~/.openclaw/workspace-main" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" },
    ],
  },
}
```

### Bindings

Bindings route incoming traffic to the right agent by channel, account, peer,
or pattern. See `agents-bindings.md` for details.

## Session

`session.*` keys control session persistence, compaction, and per-session
tool policies. Common keys:

- `session.dmScope` — `"per-peer" | "per-channel-peer" | "global"`
- `session.resetTriggers` — patterns that reset the session (e.g. `/new`, `/reset`)
- `session.historyLimit` — max turns kept in context
- `session.compaction.enabled` — auto-compact long sessions

## Messages

`messages.*` keys configure delivery, TTS, voice, and inbound handling:

- `messages.tts.*` — see `examples/tts-minimax.json`
- `messages.ackReaction` — emoji reaction on inbound message receipt
- `messages.responsePrefix` — text prepended to every response

For the full field map, run `openclaw config schema` or use the
`config.schema.lookup` tool action.