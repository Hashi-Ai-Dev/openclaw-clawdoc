---
title: "OpenProse state"
summary: ".prose/ state directory layout, run directories, state backends (filesystem, in-context, sqlite, postgres)"
read_when:
  - Inspecting a previous run's output
  - Choosing a state backend
  - Cleaning up old run directories
---

# State

OpenProse persists program state under a `.prose/` directory in the agent's workspace. Each run gets its own timestamped subdirectory; user-level agents live under `~/.prose/agents/`.

## Directory layout

```text
.prose/
├── .env                    # local env vars (e.g., DATABASE_URL for postgres backend)
├── runs/                   # one subdirectory per run
│   └── {YYYYMMDD}-{HHMMSS}-{random}/
│       ├── program.prose   # snapshot of the program that ran
│       ├── state.md        # variable bindings (the program's "memory")
│       ├── bindings/       # raw sub-agent transcripts
│       └── agents/         # per-agent metadata
└── agents/                 # project-scoped persistent agents
```

User-level agents (shared across projects) live at:

```text
~/.prose/agents/
```

These are read at program compile time when an `agent` block references a name not defined in the program itself.

## Run subdirectory contents

### `program.prose`

A verbatim copy of the program source as it was when `/prose run` started. Useful for post-mortem: "what exactly did we run?"

### `state.md`

The program's variable bindings, in markdown form. After a run, it looks like:

```markdown
# Run state

## inputs
- topic: "agent orchestration"

## bindings
### findings
<text output of the researcher session>

### draft
<text output of the writer session>

## status
- findings: ok
- draft: ok
- final: ok
```

If a binding errored, the section contains the error and any partial output.

### `bindings/`

Raw sub-agent transcripts. One file per `session:` invocation, named by the binding name. These are the full conversation logs of each sub-agent — useful for debugging prompt issues.

### `agents/`

Per-agent metadata: model used, prompt, tool allowlist override, runtime duration, token counts.

## State backends

OpenProse supports four backends for storing run state. The backend is selected at runtime (currently via the open-prose plugin's config; default is `filesystem`).

### filesystem (default)

State is written to `.prose/runs/...` in the workspace. No extra dependencies. Inspect with `ls`, `cat`, `rg`. Backup by copying the directory.

```bash
# inspect the most recent run
ls -t .prose/runs/ | head -1 | xargs -I{} cat .prose/runs/{}/state.md
```

### in-context

State is kept in the parent agent's context window. No files are written. Suitable for small, short-lived programs where persistence across runs is not needed. State is lost when the parent session ends.

### sqlite (experimental)

Requires the `sqlite3` binary on `PATH`. State is stored in a single SQLite database (default `.prose/state.db`). Useful when you want to query run history with SQL.

```bash
sqlite3 .prose/state.db "SELECT id, started_at FROM runs ORDER BY started_at DESC LIMIT 10;"
```

### postgres (experimental)

Requires `psql` and a connection string. State is stored in a dedicated schema. Useful for shared / team workflows where multiple agents need to read each other's run history.

```bash
export PROSE_PG_URL="postgres://prose:***@db.example.com/prose"
```

<Warning>
Postgres credentials flow into sub-agent logs. Use a dedicated, least-privileged database with a read-only role for any agent that only needs to query run history.
</Warning>

## Cleaning up

Run directories accumulate. The plugin does not auto-purge. To clean up:

```bash
# remove runs older than 7 days
find .prose/runs/ -maxdepth 1 -mindepth 1 -mtime +7 -exec rm -rf {} +
```

For shared / postgres-backed workflows, configure a retention policy at the database level.

## Backing up

For `filesystem` backends, the entire `.prose/` directory is the source of truth. Back it up with whatever you use for the rest of the workspace (git, rsync, snapshots).

For `sqlite` / `postgres`, the database is the source of truth. Back up the database file or use the database's native backup tooling.

## Related

- [Runtime mapping](runtime-mapping.md) — how state writes happen via the `write` tool
- [Programming guide](programming.md) — variable bindings and scope
- [Install](install.md) — first-time setup
