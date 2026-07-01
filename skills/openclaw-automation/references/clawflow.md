---
summary: "Redirect to Task Flow"
title: "ClawFlow"
---

ClawFlow was renamed to [Task flow](/automation/taskflow).

## Related

- [Task flow](/automation/taskflow)
- [Standing orders](/automation/standing-orders)
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
