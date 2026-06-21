---
summary: "Delegate gateway authentication to a trusted reverse proxy"
read_when:
  - Running OpenClaw behind an identity-aware proxy
  - Setting up Pomerium, Caddy, or nginx with OAuth in front of OpenClaw
  - Fixing WebSocket 1008 unauthorized errors with reverse proxy setups
  - Deciding where to set HSTS and other HTTP hardening headers
title: "Trusted proxy auth"
---

> **Warning:** Security-sensitive feature. This mode delegates authentication
> entirely to your reverse proxy. Misconfiguration can expose your Gateway to
> unauthorized access. Read this page carefully before enabling.

## When to use

Use `trusted-proxy` auth mode when:

- You run OpenClaw behind an identity-aware proxy (Pomerium, Caddy + OAuth,
  nginx + oauth2-proxy, Traefik + forward auth).
- Your proxy handles all authentication and passes user identity via
  headers.
- You're in a Kubernetes or container environment where the proxy is the
  only path to the Gateway.
- You're hitting WebSocket `1008 unauthorized` errors because browsers
  can't pass tokens in WS payloads.

## When NOT to use

- If your proxy doesn't authenticate users (just a TLS terminator or load
  balancer).
- If there's any path to the Gateway that bypasses the proxy (firewall
  holes, internal network access).
- If you're unsure whether your proxy correctly strips/overwrites forwarded
  headers.
- If you only need personal single-user access (consider Tailscale Serve +
  loopback for simpler setup).

## Configuration

```json5
{
  gateway: {
    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        # Header carrying the authenticated user identity
        userHeader: "x-forwarded-user",
        # Header carrying the user's email (optional, for display)
        emailHeader: "x-forwarded-email",
        # Comma-separated list of trusted proxy IPs/CIDRs
        allowList: ["10.0.0.0/8", "172.16.0.0/12"],
        # Required: reject requests where the userHeader is missing
        requireUserHeader: true,
      },
    },
  },
}
```

## Reverse proxy checklist

Your proxy MUST:

1. Strip any client-supplied `x-forwarded-user` / `x-forwarded-email`
   headers before injecting its own. Otherwise a malicious client can
   impersonate any user.
2. Only accept requests from the IPs in `allowList`. Anything else should
   be refused at the network layer.
3. Set HSTS and other HTTP hardening headers at the proxy (not the
   Gateway, which is loopback-only in this mode).
4. Reject WebSocket upgrades without a valid user identity.

## Common mistakes

- **Trusting `X-Forwarded-For` blindly** — that header is client-controlled
  unless your proxy strips and re-sets it. Use the proxy's own connection
  source IP for `allowList`, not the forwarded header.
- **Forgetting to deny direct access** — if the Gateway's bind address is
  reachable from outside the proxy, you have an auth bypass. Bind to
  `127.0.0.1` (loopback) when using trusted-proxy mode.
- **Mixed-auth in one gateway** — don't combine trusted-proxy with token or
  password auth unless you fully understand the precedence rules.

## Verifying it works

1. From a network path **through** the proxy: open the Gateway UI. It
   should load with no token prompt.
2. From a network path **bypassing** the proxy (e.g. direct curl to the
   gateway bind): the request should be refused at the network layer, OR
   if it somehow reaches the Gateway, return a clear "missing identity"
   error.
3. Use a non-authenticated test user through the proxy: the request should
   be rejected by the proxy, not the Gateway.