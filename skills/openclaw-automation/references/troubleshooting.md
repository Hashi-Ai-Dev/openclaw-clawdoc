---
summary: "Redirect to /automation/cron-jobs"
title: "Automation troubleshooting"
---

This page moved to [Scheduled Tasks](/automation/cron-jobs#troubleshooting). See [Scheduled Tasks](/automation/cron-jobs#troubleshooting) for troubleshooting documentation.

## Related

- [Hooks](/automation/hooks)
- [Background tasks](/automation/tasks)
- [Gateway troubleshooting](/gateway/troubleshooting)

## Example

```yaml
# Schedule a cron job in ~/.openclaw/openclaw.json
automation:
  jobs:
    - id: example-job
      schedule: "0 9 * * 1-5"   # weekdays at 09:00
      task: "Send the daily summary"
```
