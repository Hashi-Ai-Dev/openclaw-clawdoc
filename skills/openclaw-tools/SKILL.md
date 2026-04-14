---
name: openclaw-tools
description: OpenClaw built-in tools reference. Use when explaining, configuring, or troubleshooting any OpenClaw tool: exec, browser, cron, sessions, subagents, ACP, Lobster, slash commands, permissions, sandbox, loop detection, thinking, LLM task, plugin tools. Triggers on: "tools", "exec", "browser", "cron", "sessions", "subagent", "canvas", "message tool", "slash commands", "loop detection", "elevated", "exec approvals", "ACP", "thinking", "permissions".
---

# OpenClaw Tools

## Tool Profiles

| Profile | Includes |
|---------|----------|
| `minimal` | `session_status` only |
| `coding` | `group:fs` + `group:runtime` + `group:web` + `group:sessions` + `group:memory` + `cron` + `image` + `image_generate` + `video_generate` |
| `messaging` | `group:messaging` + sessions tools |
| `full` | No restriction |

## Tool Groups

| Group | Tools |
|-------|-------|
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

---

## ⚠️ Critical: exec Approval Tiers

```json5
tools: {
  exec: {
    security: "deny",     // deny | allowlist | full
    ask: "off",          // off | on-miss | always
    askFallback: "deny", // deny | allowlist | full
    strictInlineEval: false
  }
}
```

| Tier | Behavior |
|------|----------|
| `deny` | Block all host exec |
| `allowlist` | Only allowlisted binary paths; shell chaining/re-directions rejected unless every segment allowlisted |
| `full` | Allow everything (equivalent to elevated) |

**`allow-always`** = durable trust but still requires every segment in a pipeline to be individually allowlisted.

**`ask` modes:**
- `off` = never prompt
- `on-miss` = prompt only when binary not in allowlist
- `always` = always prompt for every command

**`askFallback`** = what to do when UI is unreachable: `deny | allowlist | full`

**`strictInlineEval: true`** = forces approval for `python -c`, `node -e`, `ruby -e`, `perl -e`, `php -r`, `lua -e`, `osascript -e` even if interpreter is allowlisted.

### safe bins
- Default safe: `cut`, `uniq`, `head`, `tail`, `tr`, `wc`
- NOT safe: `grep`, `sort`, `jq`, interpreters
- Default trusted dirs: `/bin`, `/usr/bin` only

### elevated vs. exec
- `tools.elevated.enabled` = bypasses exec approval entirely
- Resolution order: inline directive → session override → global default
- Discord fallback: `tools.elevated.allowFrom.discord` falls back to `channels.discord.allowFrom`

---

## ⚠️ Critical: Loop Detection

**Disabled by default.** Must be explicitly enabled:

```json5
tools: {
  loopDetection: {
    enabled: true,
    historySize: 30,
    warningThreshold: 10,           // warn at N consecutive same-tool calls
    criticalThreshold: 20,         // stop + alert at N
    globalCircuitBreakerThreshold: 30  // global kill switch
  }
}
```

**Threshold invariant:** `warning < critical < global`. Misconfiguration causes validation failure.

**Detectors:** `genericRepeat`, `knownPollNoProgress`, `pingPong`

---

## ⚠️ Critical: Sandbox

**Sandbox is OFF by default.** ACP sessions **cannot run sandboxed** (rejected at spawn time).

```json5
agents: {
  defaults: {
    sandbox: {
      mode: "non-main",  // off | non-main | all
      scope: "agent",    // session | agent | shared
      browser: { allowHostControl: false }
    }
  }
}
```

- `host=auto` → gateway when no sandbox; `host=sandbox` fails if sandbox runtime inactive
- `sandbox="require"` on `sessions_spawn` is rejected for ACP runtimes
- Browser in sandbox: `target: "host"` requires `agents.defaults.sandbox.browser.allowHostControl=true`

---

## ⚠️ Critical: ACP Agents (External Coding Harnesses)

ACP runs external agents (Codex, Claude Code, Gemini CLI) on **host**, not sandbox:

```json5
agents: {
  list: [{
    id: "codex",
    runtime: { type: "acp", acp: {
      agent: "codex",
      backend: "openai",
      mode: "session",   // session | run
      cwd: "/path/to/workdir"
    }}
  }]
}
```

**Permission config required for ACP sessions:**
```json5
tools: {
  sessions_spawn: {
    runtime: "acp",
    permissionMode: "approve-reads",  // approve-reads | approve-all
    nonInteractivePermissions: "deny"  // deny | allow — write/exec fails gracefully if deny
  }
}
```

**Key restrictions:**
- ACP sessions are non-interactive → write/exec prompts fail if `nonInteractivePermissions=deny`
- ACP cannot run sandboxed: `sandbox="require"` rejected
- Thread-bound ACP requires `channels.discord.threadBindings.spawnAcpSessions=true`
- Resume: `sessions_spawn({ resumeSessionId })` restores full conversation via `session/load`

**ACP spawn commands:**
```bash
/acp spawn codex --bind here     # spawn + bind to current channel
/acp spawn codex --mode persistent --thread auto  # persistent thread
/acp status; /acp cancel; /acp close; /acp doctor
```

---

## Subagents

```json5
agents: {
  defaults: {
    subagents: {
      model: null,              // null = inherit from agent
      allowAgents: [],           // which agentIds can be spawned
      maxConcurrent: 3,
      runTimeoutSeconds: 300,
      archiveAfterMinutes: 10080  // NOT runTimeoutSeconds
    }
  }
}
```

- `maxSpawnDepth` range 1–5 (default 1); depth 2 = orchestrator pattern
- Max 5 active children per session, 8 global concurrent
- `sessions_spawn` is always non-blocking; push-based completion
- Cascade stop: killing depth-1 kills all depth-2 children
- `runTimeoutSeconds` does NOT auto-archive; `archiveAfterMinutes` (default 10080) handles cleanup

---

## Thinking Levels

Resolution order: inline → session override → per-agent default → global default → fallback:

```json5
agents: {
  defaults: {
    thinkingDefault: "high"      // off | low | high | maximum | adaptive
    reasoningDefault: "visible"  // hidden | visible
    fastModeDefault: false
  }
}
```

- `adaptive` default for Claude 4.6 models; `low` for other reasoning-capable; `off` otherwise
- MiniMax on Anthropic path defaults to thinking disabled unless explicitly set
- `/fast` maps to `MiniMax-M2.7-highspeed` for minimax provider

---

## Slash Commands

Two systems:
- **Commands** (`/status`, `/whoami`): standalone `/...` messages
- **Directives** (`/think`, `/fast`, `/verbose`, `/model`, `/elevated`): inline hints, stripped from model prompt

```json5
commands: {
  allowFrom: ["discord:1234567890"],
  ownerAllowFrom: ["discord:1234567890"],
  useAccessGroups: false,
  text: true,
  native: "auto",
  nativeSkills: "auto",
  restart: true,
  bash: false
}
```

---

## Tool → Skill routing

When asked about specific tools, load these references:

| Tool | Reference |
|------|-----------|
| `exec`, `exec-approvals`, `code-execution` | `references/exec.md`, `references/exec-approvals.md` |
| `browser`, browser login/troubleshooting | `references/browser.md`, `references/browser-login.md` |
| `subagents`, `sessions_spawn` | `references/subagents.md` |
| `ACP` agents | `references/acp-agents.md` |
| `loop-detection` | `references/loop-detection.md` |
| `thinking` | `references/thinking.md` |
| `slash-commands` | `references/slash-commands.md` |
| `llm-task` | `references/llm-task.md` |
| `skills`, `creating-skills` | `references/skills.md`, `references/creating-skills.md` |
| `Lobster` workflow DSL | `references/lobster.md` |
| `Diff viewer` | `references/diffs.md` |
| `plugin` tools | `references/plugin.md` |
| `multi-agent-sandbox-tools` | `references/multi-agent-sandbox-tools.md` |
| All search tools | `references/brave-search.md`, `references/duckduckgo-search.md`, etc. |

## References

Load these for detailed topics:
- `references/exec.md` — exec tool reference
- `references/exec-approvals.md` — exec security tiers, safe bins, approval flow
- `references/loop-detection.md` — loop detection config
- `references/acp-agents.md` — ACP runtime, spawning, permissions
- `references/subagents.md` — subagent spawning, depth, concurrency
- `references/browser.md` — browser tool reference
- `references/slash-commands.md` — command vs directive system
- `references/llm-task.md` — JSON-only LLM task plugin tool
- `references/skills.md` — skills system
- `references/creating-skills.md` — building skills
- `references/index.md` — tools overview, profiles, groups, byProvider
- `references/skills-config.md` — skills install/load config
- `references/plugin.md` — plugin tool registration
- `references/multi-agent-sandbox-tools.md` — per-agent sandbox override
- `references/thinking.md` — thinking tool
- `references/reactions.md` — message reactions tool
- `references/capability-cookbook.md` — tool capability reference
