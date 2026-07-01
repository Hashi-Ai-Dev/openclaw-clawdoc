---
summary: "Redirect to /gateway/authentication"
title: "Auth monitoring"
---

Auth monitoring lives under [Authentication](/gateway/authentication).

## Related

- [Automation troubleshooting](/automation/troubleshooting)
- [Hooks](/automation/hooks)

## Example

```yaml
# Schedule a cron job in ~/.openclaw/openclaw.json
automation:
  jobs:
    - id: example-job
      schedule: "0 9 * * 1-5"   # weekdays at 09:00
      task: "Send the daily summary"
```
