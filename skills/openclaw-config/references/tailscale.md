---
summary: "Integrated Tailscale Serve/Funnel for the Gateway dashboard"
read_when:
  - Exposing the Gateway Control UI outside localhost
  - Automating tailnet or public dashboard access
title: "Tailscale"
---

OpenClaw can auto-configure Tailscale **Serve** (tailnet) or **Funnel**
(public) for the Gateway dashboard and WebSocket port. This keeps the
Gateway bound to loopback while Tailscale provides HTTPS, routing, and (for
Serve) identity headers.

## Modes

- `serve` — tailnet-only Serve via `tailscale serve`. The gateway stays on
  `127.0.0.1`.
- `funnel` — public HTTPS via `tailscale funnel`. OpenClaw requires a
  shared password.
- `off` — default. No Tailscale automation.

Status and audit output use **Tailscale exposure** for this OpenClaw
Serve/Funnel mode. `off` means OpenClaw is not managing Serve or Funnel; it
does not mean the local Tailscale daemon is stopped or logged out.

## Auth

Set `gateway.auth.mode` to control the handshake:

- `none` — private ingress only (loopback)
- `token` — default when `OPENCLAW_GATEWAY_TOKEN` is set
- `password` — shared secret via `OPENCLAW_GATEWAY_PASSWORD` or config
- `trusted-proxy` — identity-aware reverse proxy (see
  `trusted-proxy-auth.md`)

For `funnel` mode, **always** require `password` or `trusted-proxy`. Never
expose a no-auth gateway to the public internet.

## Configuration

```json5
{
  gateway: {
    bind: "127.0.0.1:18789",
    auth: { mode: "password" },
  },
  tailscale: {
    mode: "serve",  // or "funnel" or "off"
    hostname: "openclaw",  // becomes openclaw.tail-<your-tailnet>.ts.net
  },
}
```

## Commands

```bash
# Apply Tailscale exposure config
openclaw tailscale apply

# Show current status
openclaw tailscale status

# Disable (returns to "off")
openclaw tailscale disable
```

## Identity headers (Serve mode only)

When using `mode: "serve"` and an authenticated Tailscale user connects,
OpenClaw reads the following headers set by Tailscale:

- `Tailscale-User-Login` — the user's tailnet login
- `Tailscale-User-Name` — display name
- `Tailscale-User-Profile-Picture` — avatar URL

These map to operator identity when paired with `mode: "trusted-proxy"`
configured to read the `Tailscale-User-Login` header.

## Funnel caveats

- Public exposure. Use `password` or `trusted-proxy` auth.
- Tailscale Funnel rate limits apply.
- Audit logs show source IPs as Tailscale edge IPs, not the user's home
  IP.
- Some WebSocket clients behave differently over Funnel due to the edge
  proxy. Test with a non-critical session before promoting to production.

## Common issues

- `tailscale: command not found` — install Tailscale first.
- `Funnel requires MagicDNS` — enable MagicDNS in your tailnet admin.
- Gateway unreachable from another tailnet device — check
  `tailscale serve status` and that the hostname is in MagicDNS.
- 401 from Funnel URL — gateway auth mode is `none`; switch to `password`
  or `trusted-proxy`.