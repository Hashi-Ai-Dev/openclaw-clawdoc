---
summary: "Adds web search provider support."
read_when:
  - You are installing, configuring, or auditing the exa plugin
title: "Exa plugin"
---

# Exa plugin

Adds web search provider support.

## Distribution

- Package: `@openclaw/exa-plugin`
- Install route: npm; ClawHub: `clawhub:@openclaw/exa-plugin`

## Surface

contracts: webSearchProviders

## Related docs

- [exa](/tools/exa-search)

## Example

```yaml
# Enable this provider in ~/.openclaw/openclaw.json
providers:
  exa: { apiKey: "***", primary: "<see model list>" }
```
