---
summary: "Adds policy-backed doctor checks for workspace conformance."
read_when:
  - You are installing, configuring, or auditing the policy plugin
title: "Policy plugin"
---

# Policy plugin

Adds policy-backed doctor checks for workspace conformance.

## Distribution

- Package: `@openclaw/policy`
- Install route: included in OpenClaw

## Surface

plugin

## Related docs

- [policy](/cli/policy)

## Example

```yaml
# Most plugin work involves editing ~/.openclaw/openclaw.json
plugins:
  entries:
    <plugin-id>: { enabled: true }
```
