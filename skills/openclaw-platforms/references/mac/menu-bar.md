---
summary: "Menu bar status logic and what is surfaced to users"
read_when:
  - Tweaking mac menu UI or status logic
title: "Menu bar"
---

## What is shown

- We surface the current agent work state in the menu bar icon and in
  the first status row of the menu.
- Health status is hidden while work is active; it returns when all
  sessions are idle.
- A root "Context" submenu contains recent sessions instead of expanding
  them directly in the root menu.
- The "Nodes" block in the root menu lists **devices** only (paired
  nodes via `node.list`), not client/presence entries.
- A root "Usage" section appears below Context when provider usage
  snapshots are available, followed by usage-cost details when
  available.

## Menu structure (top to bottom)

```
[Status row]
- Agent work state (idle / working / error)
- Connected channel summary

[Channels]
- Discord · connected · 2 unread
- Slack · connected
- iMessage · disabled

[Nodes]
- This Mac
- iPhone (paired)

[Context]
  Recent sessions
- code review (5 min ago)
- deploy script (1 h ago)

[Usage]   ← appears only when provider reports snapshots
- Anthropic: $0.42 today
- OpenAI: 12k tokens today
  ↳ cost details

[Settings...]
[Open Control UI]
[Quit OpenClaw]
```

## When rows hide

- **Channels**: hidden if no channels are configured.
- **Nodes**: hidden if no nodes are paired.
- **Context**: hidden if no recent sessions in the last 7 days.
- **Usage**: hidden if no provider usage snapshots received.

The "Open Control UI" and "Settings" rows are always present.

## Status row logic

- **Idle** — no agent work in flight.
- **Working** — at least one session is currently in `running` or
  `streaming` state.
- **Error** — last completed session ended in `error`. Clears when a
  new session starts or after 60 seconds, whichever is first.

The row text matches the icon animation (see `icon.md`).

## Sorting

Within each section:

- Channels: by unread count (descending), then alphabetical.
- Nodes: local first, then by last-seen (most recent first).
- Recent sessions: by last activity (most recent first), capped at 8
  entries.

## Keyboard shortcuts

- `⌘⇧Space` — toggle the menu
- `⌘1` ... `⌘9` — open a recent session from the Context submenu
- `⌘U` — open Control UI in browser

Shortcuts are global; configurable in Settings → Hotkeys.

## Accessibility

- VoiceOver labels every menu row with the same text shown.
- Reduce-motion preference disables animations (icon blink, working
  scurry).
- High-contrast mode uses the system accent color for status dots.