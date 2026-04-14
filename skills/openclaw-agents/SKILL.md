---
name: openclaw-agents
description: OpenClaw multi-agent system. Use when setting up multiple agents, bindings, channel routing, per-agent sandbox, tool policies, ACP runtimes, workspace bootstrap, subagent limits, context pruning, or per-agent thinking/reasoning overrides. Triggers on: "multi-agent", "bindings", "routing", "agentId", "workspace", "sandbox", "tool policy", "per-agent", "ACP", "acp", "runtime", "bootstrap", "subagent", "sessions_spawn", "contextPruning", "thinkingDefault", "reasoningDefault", "fastModeDefault", "execApprovals", "sandbox mode", "sandbox scope".
---

# OpenClaw Multi-Agent

## Core concepts

- **agentId**: one brain (workspace + auth + sessions)
- **accountId**: one channel account instance
- **binding**: routes inbound → agentId by (channel, accountId, peer)
- Direct chats collapse to `agent:<agentId>:<mainKey>`

## Agent runtime types

Agents can use either the built-in agent runtime or an external ACP coding harness:

```json5
agents: {
  list: [
    // Built-in agent (default)
    { id: "main", runtime: { type: "agent" } },
    // ACP external coding harness (Codex, Claude Code, etc.)
    { id: "codex", runtime: { type: "acp", acp: {
      agent: "codex",
      backend: "openai",
      mode: "session",    // session | run
      cwd: "/path/to/workdir"
    }}}
  ]
}
```

## Minimal multi-agent setup

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      subagents: { model: null, allowAgents: [], maxConcurrent: 3, runTimeoutSeconds: 300, archiveAfterMinutes: 10080 }
    },
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

## Per-agent defaults

Each agent can override thinking/reasoning/fast-mode independently of global defaults:

```json5
agents: {
  defaults: {
    thinkingDefault: "high",    // off | low | high | maximum
    reasoningDefault: "visible", // hidden | visible
    fastModeDefault: false
  },
  list: [
    { id: "fast-gpt", thinkingDefault: "off", fastModeDefault: true },
    { id: "deep-claude", thinkingDefault: "maximum", reasoningDefault: "visible" }
  ]
}
```

## Per-agent subagent restrictions

```json5
agents: {
  list: [{
    id: "restricted",
    subagents: {
      requireAgentId: true,  // Force explicit agentId in all sessions_spawn calls
      model: "minimax/MiniMax-M2.7",
      allowAgents: ["main", "coding"],
      maxConcurrent: 2,
      runTimeoutSeconds: 600,
      archiveAfterMinutes: 10080
    }
  }]
}
```

## Per-agent memory search override

```json5
agents: {
  defaults: {
    memorySearch: { provider: "openai", model: "text-embedding-3-small", collection: "default" }
  },
  list: [
    // Uses default memory search
    { id: "main" },
    // Custom memory search for this agent
    { id: "coder", memorySearch: { provider: "gemini", model: "gemini-embedding-exp", collection: "code" }},
    // QMD extra collections (cross-agent transcript search)
    { id: "team", memorySearch: { qmd: { extraCollections: ["shared-team", "proj-alpha"] }}}
  ]
}
```

## Workspace bootstrap tuning

```json5
agents: {
  defaults: {
    skipBootstrap: false,                    // Skip AGENTS.md/SOUL.md bootstrap entirely
    contextInjection: "always",              // always | continuation-skip
    bootstrapMaxChars: 20000,                 // Per-file char limit during injection
    bootstrapTotalMaxChars: 50000,           // Total bootstrap budget
    bootstrapPromptTruncationWarning: true,   // Warn when truncating bootstrap content
    imageMaxDimensionPx: 1200                 // Image downscaling
  }
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

## Session scope and policy

```json5
session: {
  scope: "per-sender",    // per-sender | global
  dmScope: "main",         // main | per-peer | per-channel-peer | per-account-channel-peer
  identityLinks: {
    alice: ["telegram:123456789", "discord:987654321"]
  },
  agentToAgent: {
    maxPingPongTurns: 5   // 0 disables agent-to-agent; default 5
  },
  parentForkMaxTokens: null,  // Guard: skip parent transcript if above threshold
  sendPolicy: [              // Deny/allow by channel/chatType/keyPrefix; first-deny wins
    { channel: "discord", chatType: "group", deny: true }
  ],
  maintenance: {
    resetArchiveRetention: null,  // null = same as pruneAfter; false = disable
    maxDiskBytes: null,           // Session store disk budget
    highWaterBytes: null           // Trigger cleanup at threshold
  }
}
```

## Context pruning (in-memory only — does NOT touch .jsonl history)

```json5
agents: {
  defaults: {
    contextPruning: {
      mode: "cache-ttl",     // Only mode currently
      ttl: "1h",             // Cooldown between pruning passes (default unit: minutes)
      softTrimRatio: 0.3,     // Soft trim at 30% of soft cap
      hardClearRatio: 0.5,    // Hard clear at 50% of hard cap
      softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
      hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" },
      tools: { deny: ["browser", "canvas"] },  // Tool-result deny list
      keepLastAssistants: 3  // Keep last N assistant messages
    }
  }
}
```

> **Key distinction:** `contextPruning` only prunes in-memory context sent to the LLM. The `.jsonl` transcript on disk is NOT modified by this setting. Soft trim keeps beginning+end of oversized tool results; hard clear replaces them entirely with a placeholder. Ratios are character-based approximations, not exact token counts. Image blocks are never trimmed or cleared.

## References

- `references/multi-agent.md` — full multi-agent config examples
- `references/agent-loop.md` — agent lifecycle
- `references/agent-workspace.md` — workspace bootstrap
- `references/session.md` — session system
- `references/sandboxing.md` — sandbox config
- `references/context.md` — context window (bootstrap + injection)
- `references/system-prompt.md` — system prompt assembly
- `openclaw-tools/references/acp-agents.md` — ACP agent runtime
