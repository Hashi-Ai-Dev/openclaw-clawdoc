---
title: "/prose slash command"
summary: "Reference for the /prose user-invocable slash command and its subcommands"
read_when:
  - Looking up the exact syntax for /prose run, compile, examples, update
  - Debugging a failed /prose invocation
---

# `/prose` Slash Command

OpenProse registers `/prose` as a user-invocable skill command in any OpenClaw chat surface (Discord, Telegram, webchat, TUI, etc.).

## Command reference

```text
/prose help
/prose run <file.prose>
/prose run <handle/slug>
/prose run <https://example.com/file.prose>
/prose compile <file.prose>
/prose examples
/prose update
```

## `/prose run`

Execute a `.prose` program.

Three input forms are accepted:

| Form | Example | Resolution |
|------|---------|------------|
| Local path | `/prose run ./research.prose` | Read from filesystem |
| Handle + slug | `/prose run myorg/incident-triage` | Fetch `https://p.prose.md/myorg/incident-triage` |
| Direct URL | `/prose run https://example.com/pipeline.prose` | Fetch the URL as-is |

`handle/slug` is resolved through the public [p.prose.md](https://p.prose.md) registry. Direct URLs are fetched with the `web_fetch` tool and parsed as `.prose` source.

### Runtime arguments

Some programs declare `input` variables. Pass them as key=value pairs after the program reference:

```text
/prose run ./research.prose topic="agent orchestration"
/prose run myorg/incident-triage severity=SEV1 region=us-east-1
```

Each `input name: "..."` declaration in the program is matched against a CLI argument. Missing required inputs will prompt before running.

### Exit and output

The run produces:

- A final assistant message with the program's output
- A run directory under `.prose/runs/{YYYYMMDD}-{HHMMSS}-{random}/` containing the program snapshot, state, bindings, and per-agent transcripts
- Exit status: 0 on success, non-zero on sub-agent failure (visible in the run directory's `state.md`)

## `/prose compile`

Validate a `.prose` program without executing it.

```text
/prose compile ./draft.prose
```

Reports syntax errors, undefined agents, missing required inputs, and unbound variables. Use this in CI or before sharing a program with others.

## `/prose examples`

List the bundled example programs shipped with the open-prose plugin. Useful as starting templates:

```text
/prose examples
```

Output is a numbered list with one-line descriptions. Run any of them with `/prose run <id>`.

## `/prose update`

Update the open-prose plugin to the latest bundled version and restart the Gateway.

```text
/prose update
```

Equivalent to `openclaw plugins update open-prose && openclaw gateway restart`.

## `/prose help`

Print the command summary above plus the installed plugin version. Use it to confirm the plugin is loaded.

## Differences from Lobster

`/prose` is markdown-first, agent-routing-oriented, and optimized for spawning sub-agents with explicit control flow. [Lobster](https://docs.openclaw.ai/tools/lobster) is JSON-or-Python-first, deterministic, and approval-gated by default. Use Lobster when you need reproducible, side-effect-free pipelines. Use OpenProse when you need agent fan-out, synthesis, and human-readable workflow files.

## Related

- [Programming guide](programming.md) — `.prose` file syntax
- [Examples](examples.md) — sample programs you can run
- [Slash commands](https://docs.openclaw.ai/tools/slash-commands) — full chat-command catalog
