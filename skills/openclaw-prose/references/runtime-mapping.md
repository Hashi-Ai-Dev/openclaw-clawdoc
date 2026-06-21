---
title: "OpenProse to OpenClaw runtime mapping"
summary: "How OpenProse constructs (sessions, files, web) map to OpenClaw tools and primitives"
read_when:
  - Debugging a failed /prose run with tool errors
  - Configuring tool allowlists for OpenProse
  - Understanding what sessions_spawn, read, write, and web_fetch do under the hood
---

# Runtime Mapping

OpenProse programs execute inside an OpenClaw agent. Each OpenProse construct is implemented in terms of a small set of OpenClaw tools.

## Concept → tool table

| OpenProse concept | OpenClaw tool | What happens |
|-------------------|---------------|--------------|
| Spawn session / Task tool | `sessions_spawn` | A new sub-agent session is started with the agent's `model` and `prompt` |
| File read | `read` | Reads source files referenced by the program (`.prose` files, templates) |
| File write | `write` | Writes `.prose/runs/...` state, `state.md`, and any program-emitted files |
| Web fetch | `web_fetch` | Fetches remote `.prose` programs (handle/slug resolution, direct URLs) |
| Tool calls inside a sub-agent | Inherited | Sub-agents inherit the same tool allowlist as the parent unless overridden |

## What `sessions_spawn` does

Each `session: <agent>` block in a `.prose` program becomes a `sessions_spawn` call:

```json
{
  "task": "Research agent orchestration",
  "agentId": "researcher",
  "model": "sonnet",
  "systemPrompt": "You research thoroughly and cite sources.",
  "isolatedEnv": "worktree"
}
```

The `agentId` is resolved against the agent's `agents.list[]` config. If the agent isn't defined locally, OpenProse looks it up in `~/.prose/agents/`. Model and prompt come from the `agent` block in the program.

The sub-agent runs to completion, and its final message is bound to the variable name on the left of `=`.

## What `parallel:` actually does

`parallel:` is **not** concurrent OS-level execution. The OpenClaw runtime serializes the fan-out through `sessions_spawn`, but the calls overlap in time — the parent agent yields while sub-agents are running, and resumes when all branches complete.

This is the same pattern as spawning multiple subagents in any other OpenClaw context: useful for parallelism, not parallelism of execution primitives.

## Tool allowlist requirements

OpenProse **requires** these tools to be allowed for any agent that runs `.prose` programs:

- `sessions_spawn` — for sub-agent fan-out
- `read` — for loading program source
- `write` — for persisting state
- `web_fetch` — for handle/slug resolution and direct URL fetches

If any of these is missing from the agent's `tools.allow`, `/prose run` will fail with a "tool not allowed" error.

### Recommended config

```json
{
  "agents": {
    "list": [{
      "id": "prose-runner",
      "tools": {
        "profile": "coding",
        "allow": ["sessions_spawn", "read", "write", "web_fetch", "edit"]
      }
    }]
  }
}
```

The `coding` profile includes the file and runtime groups; `sessions_spawn` and `web_fetch` are added explicitly.

## Sub-agent tool inheritance

Sub-agents spawned by a `.prose` program inherit the parent's tool allowlist unless overridden via the `agent` block:

```prose
agent lock-down-reviewer:
  model: sonnet
  prompt: "Read-only code review."
  tools: ["read"]   # this sub-agent can only read
```

The `tools:` list replaces the inherited allowlist. Use this to enforce least-privilege for sensitive workflow steps (e.g., a reviewer that can only read, an applier that can only write).

## What is *not* in the mapping

- **No direct shell execution.** `.prose` programs cannot call `exec` directly. Sub-agents can, if their tool allowlist permits it.
- **No direct `cron` scheduling.** Programs are triggered by `/prose run` or by an external orchestrator. Use OpenClaw's `cron` tool to schedule program runs.
- **No state engine access.** Programs cannot directly read or write Honcho / QMD. Sub-agents that have memory tools can, but the program itself sees only its own `.prose/runs/...` state.

## Debugging a failed run

When a `/prose run` fails, check the run directory:

```text
.prose/runs/{YYYYMMDD}-{HHMMSS}-{random}/
├── program.prose     # snapshot of the program that ran
├── state.md          # variable bindings, including partial outputs
├── bindings/         # raw sub-agent transcripts
└── agents/           # per-agent metadata
```

`state.md` is the first place to look: it lists each binding and whether the sub-agent succeeded, errored, or was cancelled. `bindings/` contains the full transcript for any sub-agent you need to inspect.

## Related

- [Programming guide](programming.md) — `.prose` file syntax
- [State directory](state.md) — what's in `.prose/runs/...`
- [Tool config](https://docs.openclaw.ai/gateway/config-tools) — full tools config reference
- [Subagents](https://docs.openclaw.ai/tools/subagents) — the underlying multi-agent primitive
