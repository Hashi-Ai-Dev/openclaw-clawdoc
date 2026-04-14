---
name: openclaw-cli
description: OpenClaw CLI commands reference. Use when explaining openclaw commands: openclaw status, openclaw gateway, openclaw plugins, openclaw memory, openclaw agents, openclaw channels, openclaw config, openclaw sessions, openclaw cron, openclaw hooks, openclaw pairing, openclaw acp. Triggers on: "openclaw CLI", "openclaw command", "openclaw status", "CLI", "command line", "openclaw hooks", "openclaw pairing".
---

# OpenClaw CLI

## Essential commands

```bash
openclaw status              # Gateway status + health
openclaw gateway start      # Start gateway
openclaw gateway stop        # Stop gateway
openclaw gateway restart     # Restart (requires confirmation!)
openclaw config show         # Show current config
```

## Plugin commands

```bash
openclaw plugins list        # List all plugins
openclaw plugins install @scope/plugin  # Install plugin
openclaw plugins enable PLUGIN_ID       # Enable plugin
openclaw plugins disable PLUGIN_ID       # Disable plugin
```

## Memory commands

```bash
openclaw memory status       # Check index + provider
openclaw memory search "q"   # CLI search
openclaw memory index --force  # Rebuild index
```

## Agent commands

```bash
openclaw agents list         # List agents
openclaw agents add ID       # Create new agent workspace
openclaw agents list --bindings  # Show bindings
```

## Channel commands

```bash
openclaw channels status     # Channel status
openclaw channels login --channel whatsapp --account personal  # Link account
openclaw channels add        # Add channel account
openclaw channels status --probe  # Probe transport health
```

## Config commands

```bash
openclaw config show         # Print config
openclaw config set KEY VALUE  # Set value (requires gateway restart)
openclaw config unset KEY   # Remove value
openclaw config schema      # Print JSON Schema
openclaw doctor             # Diagnose issues (--fix to repair)
```

## Session commands

```bash
openclaw sessions list       # List sessions
openclaw sessions show SESSION_ID  # Show session info
```

## Cron commands

```bash
openclaw cron status        # Cron scheduler status
openclaw cron list          # List jobs
openclaw cron run JOB_ID    # Run job immediately
openclaw cron runs JOB_ID   # Run history for a job
```

**Schedule types:**
- `at`: one-shot ISO 8601 timestamp (or relative like `20m`)
- `every`: fixed interval in ms
- `cron`: 5-field cron expression with optional `--tz`

**Note:** day-of-month + day-of-week use OR logic (standard Vixie cron behavior — to require both, use `+` day-of-week modifier).

## Hooks commands

```bash
openclaw hooks list          # List all hooks (standalone + plugin)
openclaw hooks info HOOK_NAME  # Detailed hook info
openclaw hooks enable HOOK_NAME  # Enable a hook
openclaw hooks check          # Check hook status
```

## Pairing commands

```bash
openclaw pairing list telegram     # List pending pairing requests
openclaw pairing approve telegram <CODE>  # Approve a sender
```

- Codes expire after **1 hour**
- Pending requests capped at **3 per channel**
- Supported channels: `discord`, `telegram`, `whatsapp`, `signal`, `slack`, `matrix`, `imessage`, `line`, and more

## ACP commands

```bash
openclaw acp status         # ACP runtime status
openclaw acp serve          # Expose gateway as ACP server (IDE/client bridge)
```

ACP spawn via chat:
```bash
/acp spawn codex --bind here
/acp spawn codex --mode persistent --thread auto
/acp status
/acp model <provider/model>
/acp cancel
/acp close
/acp doctor
```

## MCP commands

```bash
openclaw mcp serve          # Expose gateway session as MCP server for IDE
openclaw mcp status         # MCP server status
```

## Logs

```bash
openclaw logs              # Stream gateway logs
openclaw logs --lines 100   # Last 100 lines
```

## Update

```bash
openclaw update check       # Check for updates
openclaw update run        # Apply update
```

## Secrets

```bash
openclaw secrets list      # List secrets
openclaw secrets set KEY VALUE  # Set secret
openclaw secrets get KEY   # Get secret value
```

## Doctor (diagnostics)

```bash
openclaw doctor            # Diagnose config + connectivity
openclaw doctor --fix      # Auto-repair common issues
```

## Skills

```bash
openclaw skills list       # List installed skills
openclaw skills install @scope/skill  # Install skill from ClawHub
```

## Hooks reference

Hooks fire on events inside the Gateway:

| Event | When it fires |
|-------|--------------|
| `command:new` | `/new` command issued |
| `command:reset` | `/reset` command issued |
| `command:stop` | `/stop` command issued |
| `session:compact:before` | Before compaction |
| `session:compact:after` | After compaction |
| `agent:bootstrap` | Before bootstrap files injected |
| `gateway:startup` | After channels start |
| `message:received` | Inbound message from any channel |
| `message:preprocessed` | After media/link understanding |
| `message:sent` | Outbound message delivered |

Hook directory: `~/.openclaw/hooks/`

## References

- `references/cli-commands.md` — detailed CLI reference
- `references/cron-jobs.md` — full cron documentation
- `references/slash-commands.md` — slash command reference
- `references/hooks.md` — hook system + writing hooks
