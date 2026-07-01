---
summary: "Pointer to the canonical logging overview"
read_when:
  - You came here looking for a logging overview from an automation doc
title: "Logging"
---

For the full OpenClaw logging overview (CLI + Control UI + config), see [`openclaw-logging/references/logging.md`](/skills/openclaw-logging/references/logging.md).

For logging config keys and format options, see [`openclaw-config/references/logging.md`](/skills/openclaw-config/references/logging.md).

## Example

```yaml
# Schedule a cron job in ~/.openclaw/openclaw.json
automation:
  jobs:
    - id: example-job
      schedule: "0 9 * * 1-5"   # weekdays at 09:00
      task: "Send the daily summary"
```
