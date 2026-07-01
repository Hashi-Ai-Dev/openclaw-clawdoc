---
name: openclaw-tools
description: "OpenClaw tools reference. Use when explaining, configuring, or troubleshooting tools: exec, browser, cron, sessions, subagents, ACP, Lobster, slash commands, /prose, OpenProse, thinking, tool permissions, sandbox, loop detection, LLM task, search providers, media generation. Triggers on: tools, exec, browser, cron, sessions, subagent, canvas, slash commands, /prose, openprose, prose workflow, loop detection, elevated, exec approvals, ACP, thinking, permissions, webhook, clawflow, code execution, auth monitoring, tool profile, search providers, image generation, music generation, video generation, media tools, creating skills, btw, steer, gmail, pubsub, gmail pubsub, poll, polling."
---

## Routing hints

You should route to this skill when the user asks about OpenClaw tools — exec, browser, cron, sessions, subagents, ACP, slash commands, `/prose`, OpenProse, thinking, tool permissions, sandbox, loop detection, LLM task, search providers, media generation, Lobster, Skill Workshop, or any tool-level question. References: `exec.md`, `browser.md`, `cron.md`, `sessions.md`, `subagents.md`, `acp-agents.md`, `acp-agents-setup.md`, `slash-commands.md`, `loop-detection.md`, `thinking.md`, `elevated.md`, `permissions.md`, `lobster.md`, `skill-workshop.md`, `clawhub.md`, `brave-search.md`, `duckduckgo-search.md`, `exa-search.md`, `firecrawl.md`, `gemini-search.md`, `grok-search.md`, `kimi-search.md`, `minimax-search.md`, `ollama-search.md`, `parallel-search.md`, `perplexity-search.md`, `searxng-search.md`, `tavily.md`, `tts.md`, `image-generation.md`, `music-generation.md`, `video-generation.md`, `web-fetch.md`, `webhook.md`, `clawflow.md`, `creating-skills.md`.


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

## Workflow tools

| Tool | Purpose | Skill |
|------|---------|-------|
| `/prose` slash command | Run or compile `.prose` multi-agent workflow files | `openclaw-prose` |
| Lobster | Deterministic, approval-gated pipeline runtime | (see [Lobster](https://docs.openclaw.ai/tools/lobster)) |
| Subagents | Spawn child sessions for fan-out | `sessions_spawn` |

OpenProse (the `open-prose` plugin) requires `sessions_spawn`, `read`, `write`, and `web_fetch` in the agent's `tools.allow`. Programs that fan out via `parallel:` use the same `sessions_spawn` primitive as ad-hoc subagents.

## References

- `references/index.md` — full tool list and reference
- `references/exec.md` — exec tool, timeouts, elevated
- `references/browser.md` — browser automation
- `references/subagents.md` — spawning subagents
- `references/capability-cookbook.md` — tool capability guide
- `references/creating-skills.md` — adding custom skills
- `references/loop-detection.md` — loop detection config
- `references/thinking.md` — thinking configuration

## Related skills

- `openclaw-prose` — OpenProse `.prose` workflow language (plugin + `/prose` slash command + skill pack)
