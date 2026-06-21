---
summary: "Channel configuration: access control, pairing, multi-account, per-channel keys"
read_when:
  - Configuring a channel plugin (auth, access control, multi-account)
  - Troubleshooting per-channel config keys
  - Auditing DM policy, group policy, or mention gating
title: "Channels config"
---

Per-channel configuration keys under `channels.*`. Covers DM and group access,
multi-account setups, mention gating, and per-channel keys for Slack, Discord,
Telegram, WhatsApp, Matrix, iMessage, and the other bundled channel plugins.

For agents, tools, gateway runtime, and other top-level keys, see
`configuration-reference.md`.

## Channels

Each channel starts automatically when its config section exists (unless
`enabled: false`).

### DM and group access

All channels support DM policies and group policies:

| DM policy       | Behavior |
| --------------- | -------- |
| `pairing`       | Unknown senders get a one-time pairing code; owner must approve |
| `allowlist`     | Only senders in `allowFrom` (or paired allow store) |
| `open`          | Allow all inbound DMs (requires `allowFrom: ["*"]`) |
| `disabled`      | Ignore all inbound DMs |

Group policies:

| Group policy     | Behavior |
| ---------------- | -------- |
| `allowlist`      | Only listed groups can interact |
| `open`           | Any group can interact |
| `disabled`       | Ignore group messages |

### Per-channel keys (common)

Most channels accept these base keys:

```json5
{
  channels: {
    "<plugin>": {
      enabled: true,
      dmPolicy: "pairing",
      groupPolicy: "allowlist",
      allowFrom: ["YOUR_USER_ID"],
      groups: { "YOUR_GROUP_ID": { allow: true } },
      accounts: {
        default: { /* channel-specific auth */ },
        work:    { /* multi-account */ },
      },
    },
  },
}
```

## Channel-specific examples

For the full per-channel config (Discord tokens, Telegram bot tokens, Matrix
homeserver, etc.), see the owning skill:

- `openclaw-channels/references/discord.md`
- `openclaw-channels/references/telegram.md`
- `openclaw-channels/references/whatsapp.md`
- `openclaw-channels/references/imessage.md`
- `openclaw-channels/references/signal.md`
- `openclaw-channels/references/slack.md`
- `openclaw-channels/references/matrix.md`
- `openclaw-channels/references/msteams.md`
- `openclaw-channels/references/sms.md`
- `openclaw-channels/references/wechat.md`
- `openclaw-channels/references/zalo.md`

## Channel model overrides

Override the default model per channel (e.g. a faster model for high-volume
Discord channels):

```json5
{
  channels: {
    discord: {
      model: "anthropic/claude-haiku-4-5",
      accounts: {
        default: {
          guilds: {
            "YOUR_GUILD_ID": {
              channels: {
                "YOUR_CHANNEL_ID": { model: "openai/gpt-4o-mini" },
              },
            },
          },
        },
      },
    },
  },
}
```

## Multi-account

Most channels support multiple accounts under `channels.<plugin>.accounts.<id>`.
Each account can have its own auth, allowlists, and bindings.

Bindings (channel → agent) are configured at the top level under `bindings`
(see `agents-bindings.md`).

## Hot reload

Channel config hot-reloads in most cases. Adding a new channel plugin or
changing the auth flow requires `openclaw gateway restart`.