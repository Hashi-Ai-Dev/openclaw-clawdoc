# First Run Guide — Detailed

## The 15-minute path

```
0:00 - 2:00  Verify OpenClaw installed
2:00 - 5:00  Configure model (MiniMax recommended)
5:00 - 8:00  Connect Discord channel
8:00 - 10:00 Install ClawDoc skills
10:00 - 15:00 Verify end-to-end
```

## Install verification

```bash
openclaw --version
# Expected: OpenClaw version string

openclaw gateway status
# Expected: Runtime: stopped (not running yet)
```

If `openclaw: command not found`:
```bash
# Find where it installed
find ~ -name openclaw -type f 2>/dev/null
# Common locations: ~/.hermes/node/bin/, ~/.local/bin/

# Add to PATH if needed
export PATH="$HOME/.hermes/node/bin:$PATH"
```

## Model setup (MiniMax)

```bash
openclaw config set agents.defaults.model.primary "minimax/MiniMax-M2.7"
openclaw config set auth.profiles.minimax.provider "minimax"
openclaw config set auth.profiles.minimax.apiKey "your-key-here"
```

Verify:
```bash
openclaw models status
```

## Discord setup

1. Go to https://discord.com/developers/applications
2. Create application → Bot
3. Enable Message Content Intent
4. Copy bot token
5. Invite bot to server with `applications.commands` scope

```bash
openclaw config set channels.discord.token "YOUR_TOKEN"
openclaw config set channels.discord.enabled true
openclaw gateway restart
```

## Pairing (DM policy)

Default DM policy is `pairing` — users need to approve themselves:

```bash
openclaw pairing approve discord <PAIRING_CODE>
```

Alternative: set `dmPolicy: "allowlist"` with specific Discord user IDs:
```bash
openclaw config set channels.discord.allowFrom '["YOUR_DISCORD_USER_ID"]'
openclaw gateway restart
```

## Verify everything works

```bash
openclaw status
# Should show: model configured, Discord connected, no errors

openclaw gateway restart  # restart after config changes
```

Send test DM to bot → should respond.
