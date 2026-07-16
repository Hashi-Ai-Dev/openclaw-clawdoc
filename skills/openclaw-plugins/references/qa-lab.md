---
summary: "OpenClaw QA lab plugin with private debugger UI and scenario runner."
read_when:
  - You are installing, configuring, or auditing the qa-lab plugin
title: "QA Lab plugin"
---

# QA Lab plugin

OpenClaw QA lab plugin with private debugger UI and scenario runner.

## Distribution

- Package: `@openclaw/qa-lab`
- Install route: source checkout only

## Surface

contracts: webSearchProviders

## Example

```yaml
# Enable this provider in ~/.openclaw/openclaw.json
providers:
  qa-lab: { apiKey: "***", primary: "<see model list>" }
```
