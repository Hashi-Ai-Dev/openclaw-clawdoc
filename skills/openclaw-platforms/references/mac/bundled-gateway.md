---
summary: "Gateway runtime on macOS (external launchd service)"
read_when:
  - Packaging OpenClaw.app
  - Debugging the macOS gateway launchd service
  - Installing the gateway CLI for macOS
title: "Gateway on macOS"
---

OpenClaw.app no longer bundles Node/Bun or the Gateway runtime. The macOS
app expects an **external** `openclaw` CLI install, does not spawn the
Gateway as a child process, and manages a per-user launchd service to keep
the Gateway running (or attaches to an existing local Gateway if one is
already running).

## Install the CLI (required for local mode)

```bash
npm install -g openclaw
# or pnpm add -g openclaw
# or bun add -g openclaw
```

The app prefers npm, then pnpm, then bun. Node remains the recommended
Gateway runtime.

Verify:

```bash
openclaw --version
openclaw gateway status
```

## Launchd service

The app installs a per-user LaunchAgent labeled `ai.openclaw.gateway`
(or `ai.openclaw.<profile>` when using `--profile`).

```bash
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
launchctl bootout gui/$UID/ai.openclaw.gateway
```

If the LaunchAgent isn't installed, run:

```bash
openclaw gateway install
```

## Why external?

Running the Gateway outside the app sandbox:

- Lets the Gateway survive an app crash or quit
- Lets the CLI work independently of the app (operators want this)
- Avoids the cost and complexity of bundling Node in the .app
- Allows upgrades of the Gateway without touching the .app bundle

The trade-off is that operators must install the CLI separately.

## Local vs remote mode

- **Local** (default): the app attaches to a running local Gateway if
  present; otherwise it enables the launchd service.
- **Remote**: the app connects to a Gateway over SSH/Tailscale. The app
  starts a local node host service so the remote Gateway can reach this
  Mac. The app does NOT spawn the Gateway locally.

## Verifying it works

```bash
openclaw gateway status
# expected: gateway running on 127.0.0.1:18789

openclaw status --json | jq .gateway.uptime
# expected: a positive integer (seconds)
```

If `gateway status` reports no running Gateway:

1. Check `~/.openclaw/logs/gateway.log` for startup errors.
2. Re-run `openclaw gateway install` to (re)install the LaunchAgent.
3. Verify the CLI is on PATH: `which openclaw`.