---
summary: "Redirect to /automation/cron-jobs"
title: "Webhooks"
---

This page moved to [Scheduled Tasks](/automation/cron-jobs#webhooks). See [Scheduled Tasks](/automation/cron-jobs#webhooks) for webhook documentation.

## Related

- [Poll](/automation/poll)
- [Gmail PubSub](/automation/gmail-pubsub)
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
