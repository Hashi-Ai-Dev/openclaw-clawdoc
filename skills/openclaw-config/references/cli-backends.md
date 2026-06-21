---
summary: "CLI backends: how the openclaw CLI talks to a running Gateway vs runs locally"
read_when:
  - Understanding when the CLI uses a local vs remote Gateway
  - Debugging CLI commands that behave unexpectedly
  - Setting CLI defaults for fleet deployment
title: "CLI backends"
---

The `openclaw` CLI is a thin client. Most commands forward to a running
Gateway over the WebSocket protocol and only a few operate locally. This
page explains when each path is used.

## Backend selection

The CLI picks a backend in this order:

1. `--url <gateway>` flag → connect to that Gateway explicitly.
2. `OPENCLAW_GATEWAY_URL` env var → connect to that Gateway.
3. Discovered Gateway on `127.0.0.1:18789` (default).
4. Local fallback → run the operation in-process if supported.

If none of 1-3 are reachable and the command doesn't support local fallback,
the CLI exits with a clear "no Gateway available" error.

## Commands that run locally

These commands don't need a Gateway:

- `openclaw --version`
- `openclaw --help`
- `openclaw doctor` (with `--local`; otherwise may consult a running
  Gateway for state checks)
- `openclaw config schema` (loads the bundled schema)
- `openclaw auth login` (talks to the provider's OAuth endpoint, then
  stores locally)
- `openclaw logs` (reads local log files)
- `openclaw secrets audit --local` (audits local files only)

## Commands that require a Gateway

These commands forward to the Gateway:

- `openclaw agents invoke`
- `openclaw agents list`
- `openclaw sessions list`
- `openclaw models status --probe`
- `openclaw channels status`
- `openclaw nodes list`
- `openclaw rpc ...`

The Gateway must be reachable on the configured URL. If not, the CLI exits
with `gateway-unreachable`.

## Multi-Gateway fleets

For fleet deployments, set `OPENCLAW_GATEWAY_URL` per shell or use
`openclaw --url <host:port>` per command. There is no built-in fleet
registry yet; if you need one, file an issue.

## Common patterns

### Local development with a single Gateway

```bash
openclaw gateway start    # background
openclaw agents invoke --prompt "Hello"
```

### CI / scripts hitting a remote Gateway

```bash
export OPENCLAW_GATEWAY_URL=https://openclaw.tail-<id>.ts.net
export OPENCLAW_GATEWAY_TOKEN=YOUR_TOKEN
openclaw agents invoke --prompt "Run nightly report"
```

### One-off override

```bash
openclaw --url ws://localhost:19000 agents invoke --prompt "..."
```

## Debugging

Add `--debug` to any CLI command to see:

- Backend selection (which Gateway was picked)
- WebSocket handshake details
- RPC method and params sent
- Event stream (if any)
- Final response

For protocol-level debugging, see `protocol.md`.

## What's NOT a backend concern

- Plugin execution — runs in the Gateway, not the CLI.
- Channel lifecycle — managed by the Gateway's plugin host.
- Agent model selection — Gateway-side, not CLI-side.
- State persistence — Gateway's database, not the CLI's local files.