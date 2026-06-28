---
name: openclaw-gateway
description: "OpenClaw gateway operations and HTTP/API surface. Use when configuring gateway runtime, the OpenAI-compatible HTTP API, OpenResponses API, observability (OpenTelemetry, Prometheus), secrets, sandbox vs tool policy vs elevated, security audit, gateway troubleshooting, gateway exposure (Tailscale/runbook), or gateway-owned node pairing for iOS / remote nodes (Option B). Triggers on: gateway, gateway config, configuration, HTTP API, OpenAI compatible, OpenResponses, telemetry, OpenTelemetry, prometheus, metrics, secrets, secret resolution, sandbox, tool policy, elevated, security audit, security-audit-checks, exposure, Tailscale, runbook, doctor, diagnostic, CLI backends, config-agents, config-channels, config-tools, pairing, gateway-owned, gateway owned, gatewayowned, node pairing, node pairing flow, pairing option, pairing approval."
---

# OpenClaw Gateway

The gateway is the long-running process that owns the HTTP API surface, agent routing, and observability. This skill covers gateway-specific configuration, the protocol/HTTP layer, telemetry, secrets, sandboxing, and operational runbooks.

> **Note:** For schema-level reference of every config key, see `openclaw-config`. This skill focuses on gateway **operational** concerns.

## What this skill covers

- **HTTP / API surface** — OpenAI-compatible API, OpenResponses API, internal protocol
- **Telemetry** — OpenTelemetry, Prometheus metrics
- **Secrets** — secret resolution, SecretRef credential surface
- **Sandboxing** — sandbox vs tool-policy vs elevated distinction
- **Operational runbooks** — exposure (Tailscale), security audit, gateway troubleshooting, doctor
- **Per-area gateway config** — agents, channels, tools (sub-pages of the gateway config tree)

## References

- `references/openai-http-api.md` — OpenAI-compatible HTTP API surface
- `references/openresponses-http-api.md` — OpenResponses HTTP API
- `references/protocol.md` — internal gateway protocol
- `references/opentelemetry.md` — OpenTelemetry instrumentation
- `references/prometheus.md` — Prometheus metrics endpoint
- `references/secrets.md` — secret resolution, SecretRef credential surface
- `references/sandbox-vs-tool-policy-vs-elevated.md` — sandboxing vs tool policy vs elevated
- `references/security-audit-checks.md` — security audit runbook
- `references/security/audit-checks.md` — granular audit-check reference
- `references/security.md` — gateway security overview
- `references/exposure-runbook.md` — gateway exposure (Tailscale) runbook
- `references/health.md` — gateway health endpoints
- `references/troubleshooting.md` — gateway troubleshooting
- `references/doctor.md` — `openclaw doctor` integration
- `references/cli-backends.md` — CLI backends integration
- `references/configuration.md` — gateway configuration overview
- `references/configuration-reference.md` — full configuration key reference
- `references/configuration-examples.md` — example gateway configuration snippets
- `references/authentication.md` — gateway authentication
- `references/config-agents.md` — gateway config: agents subtree
- `references/config-channels.md` — gateway config: channels subtree
- `references/config-tools.md` — gateway config: tools subtree
- `references/pairing.md` — gateway pairing flow
