---
summary: "How the macOS app reports gateway/Baileys health states"
read_when:
  - Debugging mac app health indicators
title: "Health checks (macOS)"
---

# Health Checks on macOS

How to see whether the linked channel is healthy from the menu bar app.

## Menu bar

The status dot reflects Baileys (WhatsApp) health:

- **Green** — linked + socket opened recently.
- **Yellow** — linked but no recent socket activity (may be stale).
- **Red** — unlinked, error, or socket closed unexpectedly.
- **Gray** — health unknown (Gateway hasn't reported yet).

The menu bar text shows a short status ("Connected", "Reconnecting", "Error")
next to the icon.

## Where health data comes from

The app subscribes to `node.event` from the Gateway for two event types:

- `node.presence.alive` — node identity confirms it's alive. The Gateway
  records this as `lastSeenAtMs` / `lastSeenReason` on the paired
  node/device metadata after the authenticated node device identity is
  known.
- `node.health` — explicit health report from the node. Includes socket
  state, last error, and reconnect count.

The dot transitions only when the Gateway response includes
`handled: true`. Older gateways may acknowledge `node.event` with
`{ "ok": true }`; that response is compatible but does not count as a
durable last-seen update.

## Forcing a reconnect

If the dot stays red for > 60 seconds:

1. Open the app's Settings → Channels.
2. Click "Reconnect" on the affected channel.
3. Watch the menu bar — the dot should transition yellow → green within
   ~10 seconds.

If reconnect fails:

- Check `~/.openclaw/logs/gateway.log` for the channel's reconnect
  attempts.
- Verify the channel's credentials are still valid (e.g. WhatsApp session
  not logged out from another device).

## Voice wake health

Voice wake has its own health indicator. If the app is unresponsive to
"hey openclaw" but the menu bar dot is green:

1. Check `System Settings → Privacy & Security → Microphone` — the app
   must be granted.
2. Check `System Settings → Privacy & Security → Speech Recognition` —
   same.
3. Toggle Voice Wake off and on in Settings to reset the wake detector.

## Background vs foreground

Health reporting differs based on app focus:

- **Foreground** — full event stream, real-time health updates.
- **Background** — reduced event stream (battery), periodic
  `node.presence.alive` beacon every ~60s.
- **Quit** — no events. The Gateway marks the node as `lastSeen` at the
  time of the last beacon; the app re-announces on next launch.

## Example

```bash
# macOS / iOS / Android: launch + connect to a paired node
openclaw nodes status
openclaw nodes invoke camera_snap --facing front --quality 0.8
```
