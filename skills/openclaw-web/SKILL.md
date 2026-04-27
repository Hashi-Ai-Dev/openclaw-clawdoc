---
name: openclaw-web
description: OpenClaw web UI. Use when configuring the web dashboard, TUI terminal interface, webchat, or control UI. Triggers on: "web", "dashboard", "TUI", "terminal", "webchat", "control UI", "web UI", "browser", "localhost:18789".
---

# OpenClaw Web UI

## Dashboard

The OpenClaw gateway serves a web dashboard at `http://localhost:18789/`

```bash
openclaw dashboard     # open the dashboard
openclaw status        # check gateway health
```

## TUI (Terminal UI)

```bash
openclaw tui           # launch terminal UI
```

## Webchat

Webchat is served at `http://localhost:18789/chat`

Configure via `web` config section:

```json
{
  "web": {
    "port": 18789,
    "host": "0.0.0.0",
    "webchat": { "enabled": true }
  }
}
```

## References

- `references/index.md` — web UI overview
- `references/dashboard.md` — dashboard configuration
- `references/tui.md` — terminal UI setup
- `references/control-ui.md` — control UI configuration
- `references/webchat.md` — webchat setup