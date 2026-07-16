---
summary: "Adds StepFun, StepFun Plan model provider support to OpenClaw."
read_when:
  - You are installing, configuring, or auditing the stepfun plugin
title: "StepFun plugin"
---

# StepFun plugin

Adds StepFun, StepFun Plan model provider support to OpenClaw.

## Distribution

- Package: `@openclaw/stepfun-provider`
- Install route: npm; ClawHub: `clawhub:@openclaw/stepfun-provider`

## Surface

providers: stepfun, stepfun-plan

## Related docs

- [stepfun](/providers/stepfun)

## Example

```yaml
# Enable this provider in ~/.openclaw/openclaw.json
providers:
  stepfun: { apiKey: "***", primary: "<see model list>" }
```
