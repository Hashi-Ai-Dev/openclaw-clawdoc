---
name: openclaw-tools
description: OpenClaw built-in tools reference. Use when explaining or configuring tools: exec, memory_search, browser, cron, sessions_*, subagents, gateway, message, image, video, TTS. Triggers on: "tools", "exec", "browser", "cron", "sessions", "subagent", "canvas", "message tool".
---

# OpenClaw Tools

## Core tools

| Tool | What it does |
|------|-------------|
| `read` | Read file contents |
| `write` | Write/overwrite files |
| `edit` | Precise text replacement |
| `exec` | Shell command execution |
| `process` | Manage background exec sessions |

## Session tools

| Tool | What it does |
|------|-------------|
| `sessions_list` | List visible sessions |
| `sessions_history` | Fetch session transcript |
| `sessions_send` | Send message to another session |
| `sessions_spawn` | Spawn isolated sub-agent |
| `sessions_yield` | End turn, receive subagent results |
| `session_status` | Session status card |
| `subagents` | List/kill/steer spawned subagents |

## Memory tools

| Tool | What it does |
|------|-------------|
| `memory_search` | Semantic search over memory |
| `memory_get` | Read specific memory file/lines |
| `honcho_context` | Full user representation |
| `honcho_search_conclusions` | Semantic search over conclusions |
| `honcho_search_messages` | Find messages across sessions |
| `honcho_ask` | Q&A about user (LLM-powered) |
| `honcho_session` | Current session summary |

## Browser tools

| Tool | What it does |
|------|-------------|
| `browser` | Control browser (status/start/stop/snapshot/screenshot/act) |

## Automation tools

| Tool | What it does |
|------|-------------|
| `cron` | Manage cron jobs + wake events |
| `gateway` | Restart/apply config/update gateway |

## Messaging tools

| Tool | What it does |
|------|-------------|
| `message` | Send messages via channel plugins |

## Media tools

| Tool | What it does |
|------|-------------|
| `image` | Analyze image(s) with vision model |
| `image_generate` | Generate images |
| `video_generate` | Generate videos |
| `tts` | Text-to-speech |
| `music_generate` | Generate music |

## Node tools

| Tool | What it does |
|------|-------------|
| `nodes` | Control paired devices (status/describe/notify/camera/screen) |

## Tool groups

| Group | Includes |
|-------|----------|
| `group:fs` | `read`, `write`, `edit`, `apply_patch` |
| `group:runtime` | `exec`, `process`, `code_execution` |
| `group:web` | `web_search`, `x_search`, `web_fetch` |
| `group:sessions` | `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `sessions_yield`, `subagents`, `session_status` |
| `group:memory` | `memory_search`, `memory_get` |
| `group:automation` | `cron`, `gateway` |
| `group:messaging` | `message` |
| `group:ui` | `browser`, `canvas` |
| `group:media` | `image`, `image_generate`, `video_generate`, `tts` |
| `group:nodes` | `nodes` |

## Tool profiles

| Profile | What it allows |
|---------|---------------|
| `minimal` | `session_status` only |
| `coding` | `group:fs` + `group:runtime` + `group:web` + `group:sessions` + `group:memory` + `cron` + `image` + `image_generate` + `video_generate` |
| `messaging` | `group:messaging` + `sessions_list` + `sessions_history` + `sessions_send` + `session_status` |
| `full` | No restriction |

## Elevated exec

```json5
tools: {
  elevated: {
    enabled: true,
    allowFrom: {
      whatsapp: ["+15555550123"],
      discord: ["1234567890", "987654321098765432"]
    }
  }
}
```

## Loop detection

```json5
tools: {
  loopDetection: {
    enabled: true,
    historySize: 30,
    warningThreshold: 10,
    criticalThreshold: 20,
    globalCircuitBreakerThreshold: 30
  }
}
```

## Node tools

| Tool | What it does |
|------|-------------|
| `nodes` | Control paired devices (status/describe/notify/camera/screen) |

## ACP agents (external coding harnesses)

OpenClaw runs external coding harnesses (Codex, Claude Code, Gemini CLI, etc.) via ACP protocol:

```bash
/acp spawn codex --bind here     # spawn + bind to current channel
/acp spawn codex --mode persistent --thread auto  # persistent thread
/acp status                      # check runtime state
/acp cancel                      # stop current turn
/acp close                       # close session + remove bindings
/acp doctor                      # check readiness
```

ACP uses the bundled `acpx` runtime plugin (enabled by default in fresh installs).

## Slash commands

Two systems:
- **Commands** (`/backup`, `/status`): standalone `/...` messages
- **Directives** (`/think`, `/fast`, `/verbose`, `/model`, `/elevated`, `/exec`): inline hints, stripped from model prompt

Config:
```json5
commands: {
  native: "auto",       // register native commands (Discord/Telegram)
  nativeSkills: "auto",  // register native skill commands
  text: true,           // parse /commands in chat
  bash: false,          // allow ! <cmd> (requires elevated)
  restart: true,        // allow /restart
  ownerAllowFrom: ["discord:1234567890"]
}
```

## References

- `references/tool-groups.md` — all tool group memberships
- `references/tool-profiles.md` — profile allowlist details
- `references/acp-agents.md` — ACP agent runtime + spawning
- `references/skills.md` — skills system (locations, allowlists)
- `references/subagents.md` — subagent spawning
- `references/browser.md` — browser tool reference
- `references/loop-detection.md` — loop detection config
