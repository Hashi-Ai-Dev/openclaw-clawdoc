---
summary: "Agent-controlled Canvas panel embedded via WKWebView + custom URL scheme"
read_when:
  - Implementing the macOS Canvas panel
  - Adding agent controls for visual workspace
  - Debugging WKWebView canvas loads
title: "Canvas"
---

The macOS app embeds an agent-controlled **Canvas panel** using `WKWebView`.
It is a lightweight visual workspace for HTML/CSS/JS, A2UI, and small
interactive UI surfaces.

## Where Canvas lives

Canvas is rendered in a docked or floating `WKWebView` inside the app. The
panel is registered with the macOS app's window controller and can be
shown/hidden via the menu bar.

## URL scheme

Canvas loads pages from a custom `openclaw-canvas://` URL scheme registered
in the app's Info.plist. The Gateway serves the underlying HTML at
`/__openclaw__/canvas/`. The app rewrites internal links to the custom
scheme so the panel can navigate without exposing the loopback port.

## Canvas commands (foreground only)

The agent drives Canvas via `canvas.*` commands on the paired node:

- `canvas.present` — show the panel
- `canvas.navigate` — load a URL (use `{"url": ""}` to return to default
  scaffold)
- `canvas.eval` — run JS in the current page
- `canvas.snapshot` — capture `{ format, base64 }` (default `jpeg`)
- `canvas.a2ui.push` / `canvas.a2ui.reset` — push A2UI JSONL or clear
- `canvas.a2ui.pushJSONL` — legacy alias for `canvas.a2ui.push`

## A2UI

A2UI is the agent-to-UI protocol. The Gateway also serves
`/__openclaw__/a2ui/`. The macOS app treats remote A2UI pages as
render-only — action-capable A2UI commands use the bundled app-owned A2UI
page before applying messages.

## Live reload

The Canvas server injects a live-reload client into HTML and reloads on
file changes. This is useful for development on the macOS app but disabled
in production builds.

## Tailnet

If both devices are on Tailscale, use a MagicDNS name or tailnet IP
instead of `.local`:

```
http://<gateway-magicdns>:18789/__openclaw__/canvas/
```

## Security

Canvas pages run with the same origin policy as the Gateway. The app
forbids cross-origin loads. Inline scripts are allowed; remote scripts are
gated on the Gateway's CSP.

## Common issues

- Canvas panel won't load → check `openclaw gateway status`. Canvas needs
  a running Gateway.
- A2UI push silently no-ops → verify the Gateway serves
  `/__openclaw__/a2ui/` (200 OK) and that the app-owned page is loaded.
- Canvas snapshot returns empty → the page may not be visible. Bring
  Canvas to the foreground before snapshotting.