---
summary: "Adds Groq model provider support to OpenClaw."
read_when:
  - You are installing, configuring, or auditing the groq plugin
title: "Groq plugin"
---

# Groq plugin

Adds Groq model provider support to OpenClaw.

## Distribution

- Package: `@openclaw/groq-provider`
- Install route: npm; ClawHub: `clawhub:@openclaw/groq-provider`

## Surface

providers: groq; contracts: mediaUnderstandingProviders

## Related docs

- [groq](/providers/groq)

## Example

```yaml
# Enable this provider in ~/.openclaw/openclaw.json
providers:
  groq: { apiKey: "***", primary: "<see model list>" }
```
