---
summary: "Gateway WebSocket protocol: handshake, frames, versioning"
read_when:
  - Implementing or updating gateway WS clients
  - Debugging protocol mismatches or connect failures
  - Regenerating protocol schema/models
title: "Gateway protocol"
---

The Gateway WS protocol is the **single control plane + node transport** for
OpenClaw. All clients (CLI, web UI, macOS app, iOS/Android nodes, headless
nodes) connect over WebSocket and declare their **role** + **scope** at
handshake time.

## Transport

- WebSocket, text frames with JSON payloads.
- First frame **must** be a `connect` request.
- Pre-connect frames are capped at 64 KiB. After a successful handshake,
  clients should follow the `hello-ok.policy.maxPayload` and
  `hello-ok.policy.maxBufferedBytes` limits.
- With diagnostics enabled, oversized inbound frames and slow outbound
  buffers emit `payload.large` events before the gateway closes or drops
  the affected frame. These events keep sizes, limits, surfaces, and safe
  reason codes. They do **not** keep the message body, attachment
  contents, raw frame body, tokens, cookies, or secret values.

## Handshake (connect)

Gateway → Client (pre-connect challenge):

```json
{
  "type": "connect.challenge",
  "nonce": "...",
  "ts": "2026-06-21T13:00:00Z"
}
```

Client → Gateway (auth):

```json
{
  "type": "connect",
  "role": "operator",
  "auth": { "token": "YOUR_GATEWAY_TOKEN" },
  "nonce": "..."
}
```

Gateway → Client (success):

```json
{
  "type": "hello-ok",
  "protocolVersion": 1,
  "policy": {
    "maxPayload": 262144,
    "maxBufferedBytes": 4194304
  },
  "scopes": ["gateway:read", "agents:invoke"]
}
```

## Frame types

| Type       | Direction       | Purpose |
| ---------- | --------------- | ------- |
| `req`      | client → server | RPC request |
| `res`      | server → client | RPC response |
| `event`    | server → client | Streamed event |
| `ping`     | bidirectional   | Keepalive |
| `pong`     | bidirectional   | Keepalive reply |
| `close`    | bidirectional   | Graceful disconnect |

## Common RPC methods (operator role)

- `agents.invoke` — start an agent run
- `agents.cancel` — cancel a running agent
- `sessions.list` — list sessions
- `sessions.history` — get session messages
- `models.status` — probe provider credentials
- `gateway.status` — gateway health and uptime
- `config.get` / `config.set` — read/write config (scope-required)

For the full method catalog, run `openclaw rpc list`.

## Versioning

`protocolVersion` in `hello-ok` follows semver. Bumping the major version is
a breaking change; clients should refuse to connect when the major version
differs. Minor version changes add new optional fields; clients can
tolerate them.

## Errors

RPC errors return a `res` with `ok: false` and an `error` object:

```json
{
  "type": "res",
  "id": "req-1",
  "ok": false,
  "error": {
    "code": "missing-scope",
    "message": "agents.invoke requires scope agents:invoke",
    "retryable": false
  }
}
```

Common codes:

- `auth` — bad token/password
- `missing-scope` — caller doesn't have required operator scope
- `bad-request` — invalid params
- `not-found` — session/agent doesn't exist
- `conflict` — already-running agent on a session that doesn't allow
  parallel
- `internal` — server-side bug; check logs

## Reconnection

Clients should reconnect with exponential backoff on `close` codes
`1006` (abnormal) and `1011` (server error). Use a fresh `connect` request
on each reconnect — the handshake nonce is required.

For long-lived sessions, send `ping` every 30s. Gateway replies with `pong`
within 5s. Missing pongs trigger a server-initiated `close` with code
`1011`.