---
summary: "Redirect to /automation"
title: "Cron vs heartbeat"
---

The decision guide for cron vs heartbeat lives under [Automation](/automation).

## Related

- [Scheduled tasks](/automation/cron-jobs)
- [Background tasks](/automation/tasks)

## Example

```yaml
# Schedule a cron job in ~/.openclaw/openclaw.json
automation:
  jobs:
    - id: example-job
      schedule: "0 9 * * 1-5"   # weekdays at 09:00
      task: "Send the daily summary"
```
