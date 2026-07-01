---
summary: "Inworld streaming text-to-speech (MP3, OGG_OPUS, PCM telephony)."
read_when:
  - You are installing, configuring, or auditing the inworld plugin
title: "Inworld plugin"
---

# Inworld plugin

Inworld streaming text-to-speech (MP3, OGG_OPUS, PCM telephony).

## Distribution

- Package: `@openclaw/inworld-speech`
- Install route: npm; ClawHub: `clawhub:@openclaw/inworld-speech`

## Surface

contracts: speechProviders

## Related docs

- [inworld](/providers/inworld)

## Example

```yaml
# Enable this provider in ~/.openclaw/openclaw.json
providers:
  inworld: { apiKey: "***", primary: "<see model list>" }
```
