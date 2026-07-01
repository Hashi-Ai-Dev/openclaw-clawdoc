---
summary: "Adds text-to-speech provider support."
read_when:
  - You are installing, configuring, or auditing the gradium plugin
title: "Gradium plugin"
---

# Gradium plugin

Adds text-to-speech provider support.

## Distribution

- Package: `@openclaw/gradium-speech`
- Install route: npm; ClawHub: `clawhub:@openclaw/gradium-speech`

## Surface

contracts: speechProviders

## Related docs

- [gradium](/providers/gradium)

## Example

```yaml
# Enable this provider in ~/.openclaw/openclaw.json
providers:
  gradium: { apiKey: "***", primary: "<see model list>" }
```
