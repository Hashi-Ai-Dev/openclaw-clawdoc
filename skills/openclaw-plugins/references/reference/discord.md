---
summary: "Adds the Discord channel surface for sending and receiving OpenClaw messages."
read_when:
  - You are installing, configuring, or auditing the discord plugin
title: "Discord plugin"
---

# Discord plugin

Adds the Discord channel surface for sending and receiving OpenClaw messages.

## Distribution

- Package: `@openclaw/discord`
- Install route: npm; ClawHub

## Surface

channels: discord; contracts: transcriptSourceProviders

## Related docs

- [discord](/channels/discord)

## Example

```bash
# Codex harness plugin runs as a child process spawned by the Gateway
openclaw acp spawn codex --bind here
```
