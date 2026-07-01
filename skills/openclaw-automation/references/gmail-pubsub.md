---
summary: "Redirect to /automation/cron-jobs"
title: "Gmail PubSub"
---

This page moved to [Scheduled Tasks](/automation/cron-jobs#gmail-pubsub-integration). See [Scheduled Tasks](/automation/cron-jobs#gmail-pubsub-integration) for Gmail PubSub documentation.

## Related

- [Webhook](/automation/webhook)
- [Automation troubleshooting](/automation/troubleshooting)

## Example

```yaml
# Schedule a cron job in ~/.openclaw/openclaw.json
automation:
  jobs:
    - id: example-job
      schedule: "0 9 * * 1-5"   # weekdays at 09:00
      task: "Send the daily summary"
```
