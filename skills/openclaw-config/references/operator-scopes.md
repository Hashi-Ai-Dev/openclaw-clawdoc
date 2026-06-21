---
summary: "Operator roles, scopes, and approval-time checks for Gateway clients"
read_when:
  - Debugging missing operator scope errors
  - Reviewing device or node pairing approvals
  - Adding or classifying Gateway RPC methods
title: "Operator scopes"
---

Operator scopes define what a Gateway client may do after it authenticates.
They are a control-plane guardrail inside one trusted Gateway operator
domain, not hostile multi-tenant isolation. If you need strong separation
between people, teams, or machines, run separate Gateways under separate OS
users or hosts.

Related: `gateway.md`, `protocol.md`, `pairing.md`, `devices.md`.

## Roles

Gateway WebSocket clients connect with one role:

- `operator` — control-plane clients (CLI, Control UI, automation, trusted
  helper processes).
- `node` — capability hosts (macOS, iOS, Android, headless nodes) that
  expose commands through `node.invoke`.

Operator RPC methods require the `operator` role. Node-originated methods
require the `node` role.

## Scopes

Scopes are fine-grained permissions attached to an authenticated session.
A client with scope `gateway:read` can read gateway status but not modify
state. A client with `gateway:admin` can do both.

Common scopes:

- `gateway:read` — read-only RPC (status, sessions.list, models.status)
- `gateway:write` — modify config, restart gateway
- `agents:invoke` — start agent runs
- `agents:read` — inspect sessions, history, tool calls
- `channels:read` / `channels:write` — channel inspection / mutation
- `nodes:read` / `nodes:write` — paired node inspection / mutation
- `admin` — all of the above

## Approval at pairing time

When a new client or node pairs, the operator's Gateway prompts the owner
to approve. The approval dialog shows the requested scopes. The owner can:

- Approve all requested scopes
- Approve a subset (deny the rest)
- Reject the pairing

Approved scopes are recorded in the device pairing record and re-validated
on every reconnect. A client cannot escalate its own scopes mid-session.

## Common scope errors

`missing operator scope: agents:invoke` — your device pairing was approved
without `agents:invoke`. Re-pair or have the owner expand the scope.

`role mismatch: connect role 'node' on operator RPC` — you're connecting as
a node but trying to call an operator-only RPC. Connect with role
`operator`.

## Configuring default scopes

Default scopes per role are set in `gateway.operator.scopes` config:

```json5
{
  gateway: {
    operator: {
      scopes: ["gateway:read", "gateway:write", "agents:invoke"],
    },
  },
}
```

Pairing always asks the owner to confirm. The defaults are the *requested*
scopes; the owner can adjust at approval time.

## Hard rule

> Never approve a scope for a device or client you don't fully control.
> Scopes persist across sessions; an attacker with `admin` scope on a
> paired device has full gateway control.