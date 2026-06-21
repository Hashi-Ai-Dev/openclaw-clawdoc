---
summary: "Current integration path for external apps, scripts, dashboards, CI jobs, and IDE extensions"
title: "External apps"
read_when:
  - You are building an external app, script, dashboard, CI job, or IDE extension that talks to OpenClaw
  - You are choosing between Gateway RPC and the Plugin SDK
  - You are integrating with Gateway agent runs, sessions, events, approvals, models, or tools
---

External apps should talk to OpenClaw through the Gateway protocol today. Use
Gateway WebSocket and RPC methods when a script, dashboard, CI job, IDE
extension, or another process wants to start agent runs, stream events,
wait for results, cancel work, or inspect Gateway resources.

> **Warning:** There is no public npm client package yet. Do not add OpenClaw
> client package names as application dependencies until release notes
> announce a published package and this page includes install instructions.

> **Note:** This page is for code outside the OpenClaw process. Plugin code
> that runs inside OpenClaw should use documented `openclaw/plugin-sdk/*`
> subpaths instead.

## What is available today

| Surface                                | Status    | Use it for |
| -------------------------------------- | --------- | ---------- |
| Gateway WebSocket + RPC                | Stable    | Agent runs, sessions, events, approvals, models, tools, channels, nodes |
| HTTP control API (`/v1/...`)           | Stable    | Health, metrics, status endpoints |
| OpenAI-compatible HTTP (`/v1/chat/...`)| Stable    | Any OpenAI-compatible client (chat completions, embeddings) |
| Plugin SDK                             | Stable    | Code that runs inside OpenClaw (slot registration, hook handlers) |

## Minimal example (WebSocket)

```python
import json, websocket

ws = websocket.create_connection("ws://127.0.0.1:18789")

# Handshake
ws.send(json.dumps({
  "type": "connect",
  "role": "operator",
  "auth": {"token": "YOUR_GATEWAY_TOKEN"},
}))

# Wait for hello-ok
hello = json.loads(ws.recv())
assert hello["type"] == "hello-ok"

# Start an agent run
ws.send(json.dumps({
  "type": "req",
  "id": "req-1",
  "method": "agents.invoke",
  "params": {
    "agent": "main",
    "prompt": "Hello from an external app",
  },
}))

# Stream events until result
while True:
    msg = json.loads(ws.recv())
    if msg["type"] == "res" and msg["id"] == "req-1":
        print(msg["payload"]["text"])
        break
```

For the full protocol spec, see `protocol.md`.

## Choosing Gateway RPC vs Plugin SDK

| Use Gateway RPC if... | Use Plugin SDK if... |
| --------------------- | -------------------- |
| Your code runs **outside** OpenClaw | Your code runs **inside** OpenClaw |
| You want to start agent runs, inspect sessions, listen to events | You want to add a new channel, tool, provider, or memory backend |
| You're a script, dashboard, CI job, IDE extension | You're a plugin author |

Don't write a plugin when an RPC call would do.

## Authentication

External apps authenticate as `operator` role using one of:

- Token (`gateway.auth.mode: "token"` + `OPENCLAW_GATEWAY_TOKEN`)
- Password (`gateway.auth.mode: "password"`)
- Trusted-proxy (delegate to your reverse proxy — see
  `trusted-proxy-auth.md`)

The WebSocket handshake is the same for all three. Choose based on your
deployment posture, not on the client library.

## Approvals and operator scopes

Some RPC methods require operator scopes beyond the default. Pairing your
external app records the approved scopes; subsequent reconnects use the
cached approval. See `operator-scopes.md` for the scope matrix.

## Stable event shapes

RPC method names and event payloads follow semver. New fields can be added;
existing fields can be deprecated with a clear migration window. Breaking
changes bump the Gateway's `protocolVersion` and are documented in release
notes.

## What's NOT in scope here

- Plugin development — see `plugins.md` in `openclaw-plugins` skill.
- Channel-specific connection details — see `openclaw-channels` skill.
- Provider configuration — see `openclaw-providers` skill.