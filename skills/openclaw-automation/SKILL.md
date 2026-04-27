---
name: openclaw-automation
description: Automation in OpenClaw — cron jobs, hooks, tasks, webhooks, poll, standing orders, Task Flow, Clawflow. Use when: scheduling recurring tasks, setting up cron jobs, configuring webhooks, reacting to events with hooks, running background tasks, orchestrating multi-step workflows, using standing orders to inject persistent instructions. Triggers on: "automation", "cron", "schedule", "webhook", "hook", "task", "background", "standing order", "recurring", "every x minutes", "task flow", "clawflow", "poll".
---

# OpenClaw Automation Reference

## Automation mechanisms

| Mechanism | When to use |
|-----------|-------------|
| [Cron jobs](./references/cron-jobs.md) | Exact-time recurring tasks, one-shot reminders, isolated execution |
| [Hooks](./references/hooks.md) | React to events: session start/end, tool calls, message events |
| [Tasks](./references/tasks.md) | Track detached/background work across the system |
| [Webhook](./references/tasks.md) | HTTP callbacks from external services |
| [Standing orders](./references/tasks.md) | Persistent instructions injected into every session |
| [Task Flow](./references/tasks.md) | Durable multi-step orchestration with revision tracking |

## Quick decision guide

**Exact time, recurring?** → Cron jobs  
**Event-driven reaction?** → Hooks  
**Track detached work?** → Background tasks  
**Multi-step orchestration?** → Task Flow  
**HTTP callbacks?** → Webhooks  
**Persistent instructions?** → Standing orders  

## Cron jobs

```bash
# Create a cron job
openclaw cron add --name "daily-report" --every "0 9 * * *" --message "Run daily report"

# List jobs
openclaw cron list

# Remove a job
openclaw cron remove <job-id>
```

## Hooks

Hooks fire on lifecycle events:

| Event | When it fires |
|-------|--------------|
| `session.start` | New session created |
| `session.end` | Session ends |
| `tool.call` | Every tool call |
| `message.in` | Inbound message |
| `message.out` | Outbound message |

```bash
openclaw hooks list
openclaw hooks enable <hook-name>
```

## Heartbeat vs Cron

| | Cron | Heartbeat |
|--|------|-----------|
| Timing | Exact | Approximate (~30 min) |
| Context | Fresh/isolated | Full main session |
| Use when | Precise scheduling | Periodic awareness tasks |

## References

- `references/index.md` — automation overview and decision guide
- `references/cron-jobs.md` — cron job setup and examples
- `references/hooks.md` — hook events and configuration
- `references/tasks.md` — background tasks, webhooks, standing orders
