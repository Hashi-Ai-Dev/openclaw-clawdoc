---
name: openclaw-gateway
description: "OpenClaw gateway operations and HTTP/API surface. Use when configuring gateway runtime, working with the OpenAI-compatible HTTP API, the OpenResponses API, the protocol layer, opentelemetry/prometheus observability, secrets handling, sandbox vs tool policy vs elevated, security audit, gateway troubleshooting, gateway exposure (Tailscale/runbook), the doctor command, or the gateway configuration overview. Triggers on: \"gateway\", \"gateway config\", \"HTTP API\", \"OpenAI compatible\", \"OpenResponses\", \"telemetry\", \"OpenTelemetry\", \"prometheus\", \"metrics\", \"secrets\", \"secret resolution\", \"sandbox\", \"tool policy\", \"elevated\", \"security audit\", \"security-audit-checks\", \"exposure\", \"Tailscale\", \"runbook\", \"doctor\", \"diagnostic\", \"CLI backends\", \"config-agents\", \"config-channels\", \"config-tools\"."
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
