---
name: openclaw-prose
description: "OpenProse workflow language for OpenClaw. Use when running, writing, or debugging .prose workflow files, the /prose slash command, or the open-prose plugin. Covers multi-agent orchestration with parallel and sequential control flow, .prose/ state directory, and OpenProse-to-OpenClaw runtime mapping (sessions_spawn, read, write, web_fetch). Triggers on: prose, openprose, /prose, .prose files, prose workflow, multi-agent workflow, workflow file, parallel agents, agent orchestration, prose run, prose compile, prose examples."
---

# OpenClaw Prose (OpenProse)

OpenProse is a portable, markdown-first workflow format for orchestrating AI sessions. In OpenClaw it ships as a plugin (`open-prose`) that installs a skill pack and a `/prose` slash command. Programs live in `.prose` files and can spawn multiple sub-agents with explicit control flow.

## Quick start

```bash
# 1. Enable the plugin (bundled, disabled by default)
openclaw plugins enable open-prose

# 2. Restart the gateway
openclaw gateway restart

# 3. Run a program
/prose run ./research.prose
```

## What it can do

- **Multi-agent research and synthesis** with explicit parallelism.
- **Repeatable, approval-safe workflows** (code review, incident triage, content pipelines).
- **Reusable `.prose` programs** that run across supported agent runtimes.
- **Sub-agent fan-out** mapped onto OpenClaw's `sessions_spawn`.

## Minimal example

```prose
# research.prose — parallel research + synthesis
input topic: "What should we research?"

agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

parallel:
  findings = session: researcher
    prompt: "Research {topic}."
  draft = session: writer
    prompt: "Summarize {topic}."

session "Merge the findings + draft into a final answer."
context: { findings, draft }
```

## Runtime mapping

OpenProse concepts map to OpenClaw tools:

| OpenProse concept | OpenClaw tool |
|-------------------|---------------|
| Spawn session / Task tool | `sessions_spawn` |
| File read / write | `read` / `write` |
| Web fetch | `web_fetch` |

If your tool allowlist blocks any of these, OpenProse programs will fail. See the [tools config reference](https://docs.openclaw.ai/gateway/config-tools).

## State location

Programs write state under `.prose/` in the workspace:

```text
.prose/
├── .env
├── runs/
│   └── {YYYYMMDD}-{HHMMSS}-{random}/
│       ├── program.prose
│       ├── state.md
│       ├── bindings/
│       └── agents/
└── agents/
```

User-level persistent agents live at `~/.prose/agents/`.

## State backends

| Backend | Status | Notes |
|---------|--------|-------|
| filesystem | default | Writes to `.prose/runs/...` |
| in-context | stable | Transient, context-window only |
| sqlite | experimental | Requires `sqlite3` on `PATH` |
| postgres | experimental | Requires `psql` + connection string |

## Security

Treat `.prose` files like code. Review them before running. Use OpenClaw tool allowlists and approval gates to control side effects. Postgres credentials flow into sub-agent logs — use a dedicated, least-privileged database.

For deterministic, approval-gated workflows, see [Lobster](https://docs.openclaw.ai/tools/lobster).

## References

- `references/install.md` — enable plugin + verify
- `references/slash-command.md` — `/prose` command reference
- `references/programming.md` — `.prose` file format, syntax, control flow
- `references/runtime-mapping.md` — OpenProse-to-OpenClaw primitive mapping
- `references/state.md` — `.prose/` state directory and backends
- `references/examples.md` — sample `.prose` programs
