---
name: openclaw-agents
description: OpenClaw multi-agent system. Use when setting up multiple agents, bindings, channel routing, per-agent sandbox, tool policies, ACP runtimes, workspace bootstrap, subagent limits, context pruning, or per-agent thinking/reasoning overrides. Triggers on: "multi-agent", "bindings", "routing", "agentId", "workspace", "sandbox", "tool policy", "per-agent", "ACP", "acp", "runtime", "bootstrap", "subagent", "sessions_spawn", "contextPruning", "thinkingDefault", "reasoningDefault", "fastModeDefault", "execApprovals", "sandbox mode", "sandbox scope".
---

# OpenClaw Multi-Agent

## Core concepts

- **agentId**: one brain (workspace + auth + sessions)
- **accountId**: one channel account instance
- **binding**: routes inbound → agentId by (channel, accountId, peer)

## Minimal multi-agent

```json5
{
  agents: {
    defaults: { workspace: "~/.openclaw/workspace" },
    list: [
      { id: "main", default: true },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" }
    ]
  },
  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } }
  ]
}
```

## Runtime types

**Built-in agent:**
```json5
{ id: "main", runtime: { type: "agent" } }
```

**ACP external harness (Codex, Claude Code):**
```json5
{ id: "codex", runtime: { type: "acp", acp: {
  agent: "codex", backend: "openai", mode: "session", cwd: "/path"
}}}
```

## Per-agent overrides

```json5
agents: {
  defaults: { thinkingDefault: "high", reasoningDefault: "visible", fastModeDefault: false },
  list: [
    { id: "fast", thinkingDefault: "off", fastModeDefault: true },
    { id: "deep", thinkingDefault: "maximum" }
  ]
}
```

## Per-agent subagent restrictions

```json5
{
  id: "restricted",
  subagents: {
    requireAgentId: true,
    allowAgents: ["main", "coding"],
    maxConcurrent: 2,
    runTimeoutSeconds: 600
  }
}
```

## Per-agent sandbox

```json5
{
  id: "family",
  sandbox: {
    mode: "all",           // off | non-main | all
    scope: "agent",        // session | agent | shared
    workspaceAccess: "ro",  // none | ro | rw
    docker: { image: "openclaw-sandbox:bookworm-slim", network: "none", memory: "1g" }
  },
  tools: { profile: "minimal", deny: ["exec", "write", "browser"] }
}
```

Tool profiles: `minimal` (session_status only), `coding` (fs+runtime+web+sessions+memory+cron+media), `messaging`, `full`.

## Per-agent skills

```json5
{ id: "writer", skills: ["github", "weather"] }  // inherits defaults
{ id: "docs", skills: ["docs-search"] }            // replaces defaults
{ id: "locked", skills: [] }                       // no skills
```

## Binding match order (most-specific wins)

1. `peer` (exact DM/group/channel id)
2. `parentPeer` (thread inheritance)
3. `guildId + roles`
4. `guildId` / `teamId`
5. `accountId`
6. default agent

## Context pruning (in-memory only — does NOT touch .jsonl history)

```json5
{
  mode: "cache-ttl",
  ttl: "1h",
  softTrimRatio: 0.3,
  hardClearRatio: 0.5,
  softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
  hardClear: { enabled: true, placeholder: "[Old tool result cleared]" },
  keepLastAssistants: 3
}
```
> Pruning only affects in-memory context sent to the LLM. The `.jsonl` transcript on disk is NOT modified.

## References

- `references/multi-agent.md` — full examples
- `references/agent-workspace.md` — workspace bootstrap
- `openclaw-tools/references/acp-agents.md` — ACP runtime
- `openclaw-concepts/references/session.md` — session system
