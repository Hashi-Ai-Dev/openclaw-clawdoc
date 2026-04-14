---
name: openclaw-agents
description: OpenClaw multi-agent system. Use when setting up multiple agents, bindings, channel routing, per-agent sandbox, or tool policies. Triggers on: "multi-agent", "bindings", "routing", "agentId", "workspace", "sandbox", "tool policy", "per-agent".
---

# OpenClaw Multi-Agent

## Core concepts

- **agentId**: one brain (workspace + auth + sessions)
- **accountId**: one channel account instance
- **binding**: routes inbound → agentId by (channel, accountId, peer)
- Direct chats collapse to `agent:<agentId>:<mainKey>`

## Minimal multi-agent setup

```json5
{
  agents: {
    defaults: { workspace: "~/.openclaw/workspace" },
    list: [
      { id: "main", default: true, workspace: "~/.openclaw/workspace-main" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" }
    ]
  },
  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } }
  ]
}
```

## Binding match order (most-specific wins)

1. `peer` (exact DM/group/channel id)
2. `parentPeer` (thread inheritance)
3. `guildId + roles` (Discord role routing)
4. `guildId`
5. `teamId` (Slack)
6. `accountId` match
7. channel-level (`accountId: "*"`)
8. default agent

## Per-agent sandbox

```json5
agents: {
  list: [
    {
      id: "family",
      sandbox: {
        mode: "all",     // off | non-main | all
        scope: "agent",  // session | agent | shared
        workspaceAccess: "ro",  // none | ro | rw
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          network: "none",
          memory: "1g"
        }
      },
      tools: {
        allow: ["read", "sessions_list"],
        deny: ["exec", "write", "browser"]
      }
    }
  ]
}
```

## Per-agent tool policy

```json5
agents: {
  list: [{
    id: "locked",
    tools: {
      profile: "minimal",  // minimal | coding | messaging | full
      allow: ["read"],
      deny: ["exec", "write", "browser", "canvas"]
    }
  }]
}
```

Tool profiles: `minimal` (session_status only), `coding` (fs + runtime + web + sessions + memory + cron + media), `messaging` (messaging + sessions), `full` (unrestricted)

## Per-agent skills

```json5
agents: {
  defaults: { skills: ["github", "weather"] },
  list: [
    { id: "writer" },  // inherits github, weather
    { id: "docs", skills: ["docs-search"] },  // replaces defaults
    { id: "locked", skills: [] }  // no skills
  ]
}
```

## Multi-channel binding example

```json5
bindings: [
  // WhatsApp DMs → chat agent
  { agentId: "chat", match: { channel: "whatsapp" } },
  // Telegram → deep work agent
  { agentId: "opus", match: { channel: "telegram" } },
  // Specific WhatsApp DM → Opus
  {
    agentId: "opus",
    match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } }
  }
]
```

## Discord role routing

```json5
bindings: [
  {
    agentId: "mods",
    match: { channel: "discord", guildId: "1234567890", roles: ["moderator", "admin"] }
  }
]
```

## Session scope

```json5
session: {
  scope: "per-sender",    // per-sender | global
  dmScope: "main",         // main | per-peer | per-channel-peer | per-account-channel-peer
  identityLinks: {
    alice: ["telegram:123456789", "discord:987654321"]
  }
}
```

## References

- `references/multi-agent-config.md` — full multi-agent config examples
- `references/binding-reference.md` — all binding match fields
- `references/sandbox-reference.md` — sandbox config all options
