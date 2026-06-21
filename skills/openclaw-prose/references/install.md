---
title: "Install OpenProse"
summary: "Enable the open-prose plugin and verify the /prose slash command is available"
read_when:
  - Setting up OpenProse for the first time
  - Troubleshooting missing /prose command
---

# Install OpenProse

OpenProse ships as the bundled `open-prose` plugin. Plugins are disabled by default; you must explicitly enable it and restart the Gateway.

## Steps

<Steps>
  <Step title="Enable the plugin">

```bash
openclaw plugins enable open-prose
```

  </Step>
  <Step title="Restart the Gateway">

```bash
openclaw gateway restart
```

The plugin list is loaded at startup, so a restart is required for the new plugin to register its slash command and skill pack.

  </Step>
  <Step title="Verify">

```bash
openclaw plugins list | grep prose
```

You should see `open-prose` listed as enabled. The `/prose` slash command is now available in chat:

```bash
/prose help
```

If `/prose help` returns a response, the install is complete.

  </Step>
</Steps>

## Local checkout (development)

If you have a local clone of the open-prose plugin source:

```bash
openclaw plugins install ./path/to/local/open-prose-plugin
```

This registers the plugin from the local directory instead of the bundled version. Useful when contributing upstream changes or testing unreleased builds.

## Uninstall

```bash
openclaw plugins disable open-prose
openclaw gateway restart
```

The `.prose/` state directory and any user-level agents under `~/.prose/agents/` are left in place. Delete them manually if you want a clean removal.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `/prose` not recognized in chat | Plugin enabled but gateway not restarted | `openclaw gateway restart` |
| `plugin 'open-prose' not found` | Plugin bundled copy missing | Reinstall OpenClaw or use `openclaw plugins install <path>` |
| `/prose run` fails with "tool not allowed" | `sessions_spawn` / `read` / `write` / `web_fetch` not in tool allowlist | Update `tools.allow` for the agent running the program |
| Permission denied writing to `.prose/` | Workspace not writable by the gateway user | `chown -R <gateway-user> <workspace>/.prose` |

## Related

- [Slash command reference](slash-command.md) — what `/prose` accepts
- [Programming guide](programming.md) — write your first `.prose` program
- [OpenClaw plugins](https://docs.openclaw.ai/plugins/) — general plugin lifecycle
