---
summary: "PeekabooBridge integration for macOS UI automation"
read_when:
  - Hosting PeekabooBridge in OpenClaw.app
  - Integrating Peekaboo via Swift Package Manager
  - Changing PeekabooBridge protocol/paths
  - Deciding between PeekabooBridge, Codex Computer Use, and cua-driver MCP
title: "Peekaboo bridge"
---

OpenClaw can host **PeekabooBridge** as a local, permission-aware UI
automation broker. This lets the `peekaboo` CLI drive UI automation
while reusing the macOS app's TCC permissions.

## What this is (and is not)

- **Is**: a local HTTP+IPC broker that exposes a structured UI
  automation API. It runs **inside** the macOS app so it inherits
  Accessibility, Screen Recording, and Automation permissions the user
  has already granted to the app.
- **Is not**: a screen scraper. It does not OCR the screen. It uses
  macOS Accessibility APIs (AXUIElement) for element discovery.

## When to use

- You want to drive the macOS UI from a CLI or scripted workflow.
- You don't want to grant Accessibility permissions to a separate CLI
  binary.
- You're working on macOS-native tools that need real GUI automation.

## When NOT to use

- You need to drive UI on a **remote** machine — PeekabooBridge is
  local-only.
- You're on Linux or Windows — PeekabooBridge is macOS-specific. Use
  Codex Computer Use or a cua-driver MCP server instead.
- You only need screenshots — use the built-in `screen.snapshot` tool.

## Install

PeekabooBridge is bundled with OpenClaw.app. Enable it in:

**Settings → Advanced → PeekabooBridge**

Once enabled, the bridge listens on `127.0.0.1:4711` (loopback only).

## CLI

```bash
brew install peekaboo
peekaboo click "OK button"
peekaboo type "hello"
peekaboo screenshot --out /tmp/shot.png
peekaboo find "Save menu item"
```

The CLI connects to the running app's PeekabooBridge via the loopback
port.

## Protocol (HTTP)

```http
POST http://127.0.0.1:4711/v1/click
Content-Type: application/json

{
  "query": "OK button",
  "timeout_ms": 5000
}
```

Response:

```json
{
  "ok": true,
  "element": {
    "role": "AXButton",
    "title": "OK",
    "frame": { "x": 412, "y": 311, "w": 80, "h": 24 }
  }
}
```

## Permissions

PeekabooBridge inherits the app's permissions. If the app does not have
Accessibility, every API call returns `403 permission_denied`.

To grant Accessibility to OpenClaw.app:

1. Open System Settings → Privacy & Security → Accessibility.
2. Click the lock to authenticate.
3. Add OpenClaw (or enable the toggle if already listed).
4. Restart the app.

## Security

PeekabooBridge is loopback-only by default. If you need to drive it from
another machine, do so via SSH tunneling — never expose it on a public
interface.

All API calls are rate-limited to 60 requests per minute per CLI session
to prevent runaway automation.

## See also

- `permissions.md` — TCC permissions for the app.
- `xpc.md` — IPC architecture (PeekabooBridge uses the same IPC layer).