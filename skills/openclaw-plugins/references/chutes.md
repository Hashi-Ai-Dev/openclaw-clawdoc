---
summary: "Adds Chutes model provider support to OpenClaw."
read_when:
  - You are installing, configuring, or auditing the chutes plugin
title: "Chutes plugin"
---

# Chutes plugin

Adds Chutes model provider support to OpenClaw.

## Distribution

- Package: `@openclaw/chutes-provider`
- Install route: npm; ClawHub: `clawhub:@openclaw/chutes-provider`

## Surface

providers: chutes

## Related docs

- [chutes](/providers/chutes)

## Example

```yaml
# Enable this provider in ~/.openclaw/openclaw.json
providers:
  chutes: { apiKey: "***", primary: "<see model list>" }
```
