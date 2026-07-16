---
summary: "Redirect to /cli/message"
title: "Polls"
---

This page moved to [Message tool](/cli/message). See [Message tool](/cli/message) for poll documentation.

## Related

- [Webhook](/automation/webhook)
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
