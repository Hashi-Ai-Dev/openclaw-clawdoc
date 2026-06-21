---
summary: "macOS IPC architecture for OpenClaw app, gateway node transport, and PeekabooBridge"
read_when:
  - Editing IPC contracts or menu bar app IPC
title: "macOS IPC"
---

# OpenClaw macOS IPC architecture

**Current model:** a local Unix socket connects the **node host
service** to the **macOS app** for exec approvals + `system.run`. A
`openclaw-mac` debug CLI exists for discovery/connect checks; agent
actions still flow through the Gateway WebSocket and `node.invoke`.
UI automation uses PeekabooBridge.

## Goals

- Single GUI app instance that owns all TCC-facing work (notifications,
  screen recording, mic, speech, AppleScript).
- A small surface for automation: Gateway + node commands, plus
  PeekabooBridge for UI automation.

## Components

```
┌─────────────────┐         ┌──────────────────┐
│  Menu bar app   │ ◄─XPC─► │  Node host       │
│  (GUI, TCC)     │         │  service (headless) │
└────────┬────────┘         └────────┬─────────┘
         │                          │
         │  WebSocket (gateway URL) │
         ▼                          ▼
┌──────────────────────────────────────────┐
│              OpenClaw Gateway             │
│         (separate process, port 18789)    │
└──────────────────────────────────────────┘
```

## Local Unix socket (app ↔ node host service)

- Path: `~/Library/Application Support/OpenClaw/ipc.sock`
- Mode: `0600`, owned by the user
- Protocol: newline-delimited JSON
- Used for:
  - Exec approvals (the menu bar shows the approval prompt)
  - `system.run` execution (the app runs the command; the node host
    reports the result)

The socket is created on first launch by the menu bar app. The node
host service is a separate headless process that runs as the same user
and connects to the same socket.

## Approval flow

When the agent invokes a tool that needs approval (e.g. `exec` with an
elevated command):

1. Agent → Gateway: `tools.invoke` with the tool and args.
2. Gateway → Node host service (via the Gateway's node transport):
   approval request.
3. Node host service → Menu bar app (via Unix socket): approval
   prompt.
4. Menu bar app: shows a system notification + modal prompt.
5. User approves or denies.
6. Menu bar app → Node host service: decision.
7. Node host service → Gateway: continues or aborts.
8. Gateway → Agent: tool result.

If the menu bar app is not running, the approval auto-denies with a
clear "node unavailable" error. The agent should not retry indefinitely;
operators who want approvals should keep the menu bar app running.

## `openclaw-mac` debug CLI

A debug CLI for inspecting the IPC state:

```bash
openclaw-mac ipc status
# shows: socket path, connected processes, last activity

openclaw-mac ipc ping
# sends a ping; reports round-trip latency

openclaw-mac approve list
# lists pending approval requests
```

The CLI is for development and operator debugging. Not part of the
public CLI surface.

## PeekabooBridge

UI automation is a separate surface from the IPC socket:

- Bridge listens on `127.0.0.1:4711` (loopback only)
- HTTP API, not Unix socket
- Inherits the app's TCC permissions (Accessibility, Screen Recording)
- See `peekaboo.md` for details

## Failure modes

- **Socket missing** — the menu bar app hasn't launched yet, or
  crashed. Restart it.
- **Permission denied on socket** — the node host service is running
  as a different user. Verify both processes share `UID`.
- **Approval timeout** — the menu bar app's modal timed out (default
  60s). The default is to deny. Adjust in
  Settings → Advanced → Approval timeout.

## What this is NOT

- Not a substitute for the Gateway WebSocket protocol. All agent
  commands still go through the Gateway.
- Not exposed externally. The Unix socket is `0600`, the bridge is
  loopback.
- Not a general IPC framework. It's a minimal surface for the two
  specific needs above.