---
summary: "Session goals: durable per-session objectives, /goal controls, model goal tools, token budgets, and TUI status"
read_when:
  - You want OpenClaw to keep one objective visible across a long session
  - You need to pause, resume, block, complete, or clear a session goal
  - You want to understand the get_goal, create_goal, and update_goal tools
  - You want to see how goals appear in the TUI
title: "Goal"
---

A **goal** is one durable objective attached to the current OpenClaw session. It gives the agent and the operator a shared target for long-running work, without turning that target into a background task, reminder, cron job, or standing order.

Goals are session state. They move with the session key, survive process restarts, show up in `/goal`, are available to the model through the goal tools, and appear in the TUI footer when the active session has one.

## Quick start

Set a goal:

```text
/goal start get CI green for PR 87469 and push the fix
```

Check it:

```text
/goal
```

Pause it when work is intentionally waiting:

```text
/goal pause waiting for CI
```

Resume it:

```text
/goal resume
```

Mark it complete:

```text
/goal complete pushed and verified
```

Clear it:

```text
/goal clear
```

## What goals are for

Use a goal when a session has a concrete outcome that should remain visible across many turns:

- A PR closeout: fix, verify, autoreview, push, and open or update the PR.
- A debug run: reproduce the bug, identify the owning surface, patch, and prove the fix.
- A docs pass: read the relevant docs, write the new page, cross-link it, and verify the docs build.
- A maintenance task: inspect current state, make bounded changes, run the validator, push.

A goal is **not** a cron job, not a standing order, not a background task. If you want those, use:

- [Cron jobs](/automation/cron-jobs) for time-based triggers.
- [Standing orders](/cli/standing-orders) for always-on rules.
- [Webhooks](/automation/webhooks) for event-driven automation.

## Goal state machine

Goals have a small explicit state machine:

```
   start        pause       resume       block        complete
draft ──────► active ────────────────► paused ──────► blocked ──────► completed
                ▲                              │           │
                │                              ▼           ▼
                └──────── resume ───────────────┘         clear
                                                           │
                                                           ▼
                                                        (removed)
```

- **draft** — set but not yet acknowledged by the model.
- **active** — the model is working toward it.
- **paused** — work intentionally suspended (`/goal pause`).
- **blocked** — cannot proceed (`/goal block <reason>`); typically followed by a follow-up that resolves the block.
- **completed** — terminal; goal no longer drives the session.
- **cleared** — removed without completion (the operator decided it wasn't needed).

## Model tools

Three tools are exposed to the model:

| Tool | Purpose |
|------|---------|
| `get_goal` | Read the current goal and its state. Returns null if no goal is set. |
| `create_goal` | Set the session goal. The model invokes this when an objective becomes clear. |
| `update_goal` | Change goal state (active/paused/blocked/completed), update the description, or clear it. |

These are session-scoped — every turn has access to the current goal via `get_goal`. The model is expected to consult the goal at the start of every non-trivial turn.

## TUI display

When a session has an active goal, the TUI footer shows it:

```text
[session: discord#12345] ▸ goal: get CI green for PR 87469
```

The footer updates as the goal state changes. Paused/blocked goals show a state prefix:

```text
[session: discord#12345] ▸ goal [paused]: get CI green for PR 87469
```

Completed goals are not shown in the footer.

## Token budget interaction

Goals don't have a hard token budget by themselves, but they interact with session compaction:

- An active goal is preserved across compactions (the goal text is in the compaction-priority set).
- A completed goal is treated as historical context and may be compacted away.
- A paused goal is preserved with its reason.

If a session is hitting compaction frequently, consider completing or clearing goals that are no longer driving the work.

## Storage

Goals are stored under the session's state directory. Per-session:

```text
~/.openclaw/sessions/<session-key>/goal.json
```

The file is human-readable JSON; you can inspect or back it up directly.

## See also

- [Sessions](/concepts/session)
- [Compaction](/concepts/compaction)
- [Cron jobs](/automation/cron-jobs)
- [Standing orders](/cli/standing-orders)