---
summary: "Codex supervisor plugin — supervises Codex app-server sessions from OpenClaw"
read_when:
  - You want OpenClaw to drive the OpenAI Codex app-server (not the standalone Codex CLI)
  - You need to debug Codex session timeouts, hangs, or stuck approvals
  - You want to know how OpenClaw handles Codex session lifecycle
title: "Codex supervisor"
---

The **codex-supervisor** plugin supervises Codex app-server sessions invoked from OpenClaw. It is bundled in the OpenClaw core npm package and runs alongside the standalone `codex` plugin with a distinct role.

| Property         | Value                                    |
| ---------------- | ---------------------------------------- |
| Plugin id        | `codex-supervisor`                       |
| Bundled in       | OpenClaw core npm package                |
| Companion plugin | `codex` (the standalone Codex runtime)   |
| Auth model       | OpenAI Codex OAuth (same as `codex`)      |

## Why two Codex plugins

OpenClaw has two ways to talk to Codex:

- **`codex`** — the standalone Codex runtime. OpenClaw spawns the Codex CLI as an ACP agent and runs individual tasks. Each task is a fresh Codex session.
- **`codex-supervisor`** — supervises a long-running Codex app-server process. OpenClaw manages the app-server lifecycle, holds the connection open, and reuses it across multiple agent turns.

Use `codex-supervisor` when you want OpenClaw to drive a persistent Codex session (e.g., a long-running coding agent that maintains context across many turns). Use `codex` for one-off Codex invocations.

## Install

The plugin is bundled, so no separate install is needed. Verify it's enabled:

```bash
openclaw plugins list | grep codex-supervisor
# Expected: codex-supervisor ... enabled
```

If it's listed but disabled:

```bash
openclaw plugins enable codex-supervisor
openclaw gateway restart
```

## Auth

Codex supervisor uses the same OAuth flow as the `codex` plugin:

```bash
openclaw onboard --auth-choice openai-codex-oauth
```

The supervisor reuses the OAuth token from `~/.openclaw/auth/openai-codex.json`. There is no separate login for `codex-supervisor`.

## Session lifecycle

The supervisor manages Codex app-server sessions like this:

1. **Spawn** — when an agent needs Codex, the supervisor starts an app-server child process.
2. **Connect** — supervisor opens a JSON-RPC channel to the app-server.
3. **Heartbeat** — supervisor sends periodic heartbeats to keep the connection alive.
4. **Reuse** — subsequent agent turns reuse the same app-server process (fast).
5. **Idle timeout** — after `idleTimeoutMs` (default 5 minutes), the app-server is shut down. The next spawn starts a new one.
6. **Hard timeout** — after `hardTimeoutMs` (default 30 minutes), the app-server is force-killed regardless of activity.

The supervisor is responsible for cleanup if the Gateway stops or crashes — app-servers are not left orphaned.

## Configuration

```json5
{
  plugins: {
    entries: {
      "codex-supervisor": {
        enabled: true,
        config: {
          idleTimeoutMs: 300000,
          hardTimeoutMs: 1800000,
          maxConcurrentSessions: 4,
          heartbeatIntervalMs: 30000
        }
      }
    }
  }
}
```

Tunables:

- `idleTimeoutMs` — close the app-server after this many ms of no agent activity. Lower = more process churn, higher = more memory hold.
- `hardTimeoutMs` — force-kill after this many ms total, regardless of activity. Safety net for stuck app-servers.
- `maxConcurrentSessions` — cap on parallel app-servers. Per-Gateway, not per-agent.
- `heartbeatIntervalMs` — supervisor heartbeat to keep the connection alive across proxies/firewalls.

## Troubleshooting

- **"codex-supervisor not enabled"** — `openclaw plugins enable codex-supervisor && openclaw gateway restart`.
- **"app-server stuck on approval"** — check `openclaw plugins logs codex-supervisor`. The supervisor surfaces app-server state via `/acp status`.
- **"OAuth expired"** — re-run `openclaw onboard --auth-choice openai-codex-oauth`. The supervisor picks up the new token on next spawn.
- **High idle timeouts → memory pressure** — lower `idleTimeoutMs` (default 5 min is reasonable; 2 min for memory-constrained setups).

## See also

- [Codex plugin](/plugins/codex) — standalone Codex runtime
- [ACP agents](/concepts/acp-agents) — how Codex fits into the ACP protocol
- [Plugin manifest](/plugins/manifest)