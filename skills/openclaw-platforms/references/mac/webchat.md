---
summary: "How the mac app embeds the gateway WebChat and how to debug it"
read_when:
  - Debugging mac WebChat view or loopback port
title: "WebChat (macOS)"
---

The macOS menu bar app embeds the WebChat UI as a native SwiftUI view.
It connects to the Gateway and defaults to the **main session** for the
selected agent (with a session switcher for other sessions).

- **Local mode**: connects directly to the local Gateway WebSocket.
- **Remote mode**: forwards the Gateway control port over SSH and uses
  that tunnel as the data plane.

## Loopback port

WebChat opens an internal `WKWebView` pointed at
`http://127.0.0.1:<gateway-port>/__openclaw__/webchat/`. The port is the
same as the gateway bind port (default `18789`).

The macOS app does NOT use a separate WebChat port; it's all served by
the Gateway.

## Session selection

The default session is the agent's `main` session (per
`agents.<id>.session.dmScope`). The session switcher (top-right of the
WebChat view) shows all sessions for the current agent, sorted by last
activity.

Clicking a session:

1. Calls `sessions.switch` on the Gateway.
2. Re-renders the WebChat view with the new session's history.
3. The header updates to show the session name and unread count.

## Local mode details

In local mode:

- The app talks to `ws://127.0.0.1:18789` (or wherever the Gateway is
  bound).
- Auth uses the loopback token from `~/.openclaw/state/gateway.token`
  (created on first Gateway start).
- No extra configuration needed.

## Remote mode details

In remote mode:

- The app opens an SSH tunnel:
  `ssh -N -L 18789:127.0.0.1:18789 <gateway-host>`.
- The Gateway on the remote host sees the connection as `127.0.0.1`
  (loopback), which is the expected behavior.
- Auth uses the same token but transmitted over the SSH tunnel.

If SSH tunnel fails:

- Check the host is reachable (`ssh <host> echo ok`).
- Check the gateway port is open on the remote host
  (`ssh <host> ss -tlnp | grep 18789`).
- Check the SSH key is loaded (`ssh-add -l`).

## Voice forwarding

Voice input from the menu bar's voice wake / PTT also goes through the
WebChat session. The session is the one currently selected in WebChat
when the utterance is sent.

If no WebChat session is active, the utterance goes to the agent's
`main` session by default.

## Common issues

- **WebChat loads blank** — the Gateway is not serving
  `/__openclaw__/webchat/`. Check
  `curl http://127.0.0.1:18789/__openclaw__/webchat/`.
- **WebSocket fails to connect** — Gateway may have restarted; the app
  auto-reconnects with backoff (max 30s).
- **Session list is empty** — the agent has no sessions yet. Send a
  message first; the session is created on first send.
- **Token prompt keeps appearing** — the gateway token changed (e.g.
  Gateway reinstall). Re-pair via Settings → Gateway.

## Disabling the embedded WebChat

If you prefer the browser Control UI:

**Settings → WebChat → Use browser Control UI instead**

The WebChat view is replaced by a button that opens
`http://127.0.0.1:18789/__openclaw__/` in your default browser. Useful
for debugging or for users who want a full-window experience.

## Performance

WebChat uses the system WKWebView. Performance is governed by:

- The Gateway's response rate (latency to first token)
- The view's render cost (mostly the message list)
- Local CPU (Safari engine; benefits from Apple Silicon)

If WebChat is sluggish, check:

- `openclaw status --json | jq .gateway.latency` — should be < 500ms.
- Activity Monitor → the app's CPU usage.
- Console.app → filter for `WKWebView` errors.

## Privacy

WebChat is a sandboxed view; it cannot make outbound network requests
except to the configured Gateway URL. The CSP set by the Gateway blocks
inline scripts from non-trusted origins.

## Example

```bash
# macOS / iOS / Android: launch + connect to a paired node
openclaw nodes status
openclaw nodes invoke camera_snap --facing front --quality 0.8
```
