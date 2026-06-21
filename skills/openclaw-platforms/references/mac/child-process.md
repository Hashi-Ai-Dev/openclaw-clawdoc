---
summary: "Gateway lifecycle on macOS (launchd)"
read_when:
  - Integrating the mac app with the gateway lifecycle
title: "Gateway lifecycle on macOS"
---

The macOS app **manages the Gateway via launchd** by default and does not
spawn the Gateway as a child process. It first tries to attach to an
already-running Gateway on the configured port; if none is reachable, it
enables the launchd service via the external `openclaw` CLI (no embedded
runtime). This gives you reliable auto-start at login and restart on
crashes.

Child-process mode (Gateway spawned directly by the app) is **not in use**
today. If you need tighter coupling to the UI, run the Gateway manually in
a terminal.

## Lifecycle states

1. **Idle** — no Gateway running, app is in menu bar only.
2. **Attaching** — app detected a local Gateway, attempting to connect.
3. **Connected** — WebSocket handshake complete, app is using the
   Gateway.
4. **Launchd-enabling** — app called `openclaw gateway install` to enable
   the LaunchAgent.
5. **Detached** — user manually disabled the LaunchAgent or the Gateway
   is unreachable for > N minutes.

The app surfaces these in the menu bar icon and the first status row.

## launchd label

The LaunchAgent label is `ai.openclaw.gateway` by default. With
`--profile` or `OPENCLAW_PROFILE`, it becomes `ai.openclaw.<profile>`.

Legacy `com.openclaw.*` labels are still recognized for unload, but new
installs use `ai.openclaw.*`.

## Restart on crash

launchd's `KeepAlive` directive restarts the Gateway on exit. The app
expects this and does not attempt to re-spawn.

If the Gateway repeatedly fails to stay up, check
`~/.openclaw/logs/gateway.log`. Common causes:

- Config error (`openclaw config check` to diagnose)
- Port already in use (`lsof -i :18789`)
- Stale `~/.openclaw/state/` (move aside and let the Gateway re-init)

## Manual control

To take the Gateway out of launchd's hands:

```bash
launchctl bootout gui/$UID/ai.openclaw.gateway
openclaw gateway  # run in foreground
```

To put it back:

```bash
# stop the foreground process (Ctrl-C)
openclaw gateway install
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
```

## Profile isolation

For multi-profile setups (work + personal), use `--profile work`. Each
profile gets its own launchd label, state dir, and config path:

```bash
openclaw --profile work gateway install
openclaw --profile personal gateway install
```

The app's profile switcher (in Settings → Gateway) corresponds 1:1 with
launchd labels.