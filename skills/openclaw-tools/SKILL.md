---
name: openclaw-tools
description: OpenClaw tools reference. Use when explaining, configuring, or troubleshooting tools: exec, browser, cron, sessions, subagents, ACP, Lobster, slash commands, thinking, tool permissions, sandbox, loop detection, LLM task. Triggers on: "tools", "exec", "browser", "cron", "sessions", "subagent", "canvas", "message tool", "slash commands", "loop detection", "elevated", "exec approvals", "ACP", "thinking", "permissions", "tool profile".
---

# OpenClaw Tools

## Tool profiles

| Profile | What it allows |
|---------|---------------|
| `minimal` | `session_status` only |
| `coding` | FS, runtime, web, sessions, cron, image/video generation |
| `messaging` | Messaging tools + session tools |
| `full` | No restrictions |

Set via `tools.profile` on an agent, or `tools.allow` / `tools.deny` for fine-grained control.

## Core tools

| Tool | Purpose |
|------|---------|
| `exec` | Run shell commands |
| `read` / `write` / `edit` | File operations |
| `process` | Manage background processes |
| `gateway` | Config inspect/apply/patch, restart |
| `browser` | Browser automation |
| `cron` | Schedule jobs, set reminders |
| `canvas` | Render/control canvas UI |

## Session tools

`sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `sessions_yield`, `session_status`, `subagents`

## Memory tools

| Tool | Purpose |
|------|---------|
| `memory_search` | Semantic search over memory |
| `honcho_context` | Full user representation |
| `honcho_search_conclusions` | Semantic search over conclusions |
| `honcho_ask` | Q&A about the user |

## Tool config

```json
{
  "tools": {
    "profile": "full",
    "allow": ["*"],
    "deny": []
  }
}
```

Per-agent override:
```json
{
  "agents": {
    "list": [{
      "id": "locked-down",
      "tools": {
        "profile": "minimal",
        "allow": ["read", "sessions_list", "sessions_history"],
        "deny": ["exec", "write", "browser"]
      }
    }]
  }
}
```

## Thinking

Enable verbose reasoning: `/thinking` toggle in session. Configure default:
```json
{ "agents": { "defaults": { "thinkingDefault": "high" } } }
```

## Loop detection

Built-in safeguard against infinite tool call loops. Config:
```json
{ "tools": { "loopDetection": { "maxIterations": 100 } } }
```

## References

- `references/index.md` — full tool list and reference
- `references/exec.md` — exec tool, timeouts, elevated
- `references/browser.md` — browser automation
- `references/subagents.md` — spawning subagents
- `references/capability-cookbook.md` — tool capability guide
- `references/creating-skills.md` — adding custom skills
- `references/loop-detection.md` — loop detection config
- `references/thinking.md` — thinking configuration
