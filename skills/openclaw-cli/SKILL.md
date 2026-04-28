---
name: openclaw-cli
description: OpenClaw CLI commands reference. Use when explaining openclaw commands: openclaw status, openclaw gateway, openclaw plugins, openclaw memory, openclaw agents, openclaw channels, openclaw config, openclaw sessions, openclaw cron, openclaw hooks, openclaw pairing, openclaw acp. Triggers on: "openclaw CLI", "openclaw command", "openclaw status", "CLI", "command line", "openclaw hooks", "openclaw pairing".
---

# OpenClaw CLI

## Essentials

```bash
openclaw status              # Gateway status + health
openclaw gateway restart     # Restart (confirm first!)
openclaw config show         # Show current config
openclaw doctor             # Diagnose issues (--fix to repair)
```

## Plugins

```bash
openclaw plugins list        # List all plugins
openclaw plugins install @scope/plugin  # Install
openclaw plugins enable PLUGIN_ID     # Enable
openclaw plugins disable PLUGIN_ID    # Disable
openclaw plugins inspect ID   # See shape + capabilities
```

## Memory

```bash
openclaw memory status       # Index + provider
openclaw memory search "q"   # CLI search
openclaw memory index --force  # Rebuild index
```

## Agents

```bash
openclaw agents list         # List agents
openclaw agents list --bindings  # Show bindings
openclaw agents add ID        # Create workspace
```

## Channels

```bash
openclaw channels status     # Channel health
openclaw channels login --channel whatsapp --account personal  # Link
openclaw channels status --probe  # Probe transport
```

## Config

```bash
openclaw config show         # Print config
openclaw config set KEY VALUE  # Set (may need restart)
openclaw config unset KEY    # Remove
openclaw config schema      # JSON Schema
openclaw secrets set KEY VALUE  # Store secret
```

## Sessions

```bash
openclaw sessions list       # List sessions
openclaw sessions show ID    # Show session info
```

## Cron

```bash
openclaw cron list          # List jobs
openclaw cron status        # Scheduler status
openclaw cron run JOB_ID    # Run immediately
openclaw cron runs JOB_ID   # Run history
```

Schedule types: `at` (ISO 8601), `every` (ms), `cron` (5-field, `--tz` for timezone). day-of-month + day-of-week use OR logic.

## Hooks

```bash
openclaw hooks list          # List all hooks
openclaw hooks info NAME     # Detailed info
openclaw hooks enable NAME   # Enable
openclaw hooks check         # Check status
```

Hook dir: `~/.openclaw/hooks/`. Events: `command:new|reset|stop`, `session:compact:before|after`, `agent:bootstrap`, `gateway:startup`, `message:received|preprocessed|sent`.

## Pairing

```bash
openclaw pairing list CHANNEL     # Pending requests
openclaw pairing approve CHANNEL CODE  # Approve
```
Codes expire in 1h, max 3 pending per channel.

## ACP

```bash
openclaw acp status         # Runtime status
/acp spawn codex --bind here     # Spawn via chat
/acp status | cancel | close
/acp doctor                 # Check readiness
```

## MCP

```bash
openclaw mcp serve          # Expose gateway as MCP server
openclaw mcp status         # Server status
```

## Update + Logs

```bash
openclaw update check       # Check updates
openclaw update run        # Apply update
openclaw logs --lines 100   # Last 100 log lines
```

## References

- `references/cli-commands.md` — detailed CLI reference
- `references/cron-jobs.md` — full cron docs
- `references/hooks.md` — hook system + writing hooks
