---
name: openclaw-channels
description: OpenClaw channel configuration. Use when setting up, auditing, or troubleshooting any messaging channel: Discord, Telegram, WhatsApp, Slack, Signal, Matrix, iMessage, bluebubbles, IRC, Feishu, LINE, GoogleChat, Mattermost, Microsoft Teams, Nextcloud Talk, Nostr, QQ Bot, Synology Chat, Twitch, Tlon, Zalo, Voice Call. Also covers: bluebubbles, feishu, googlechat, group-messages, imessage, irc, line reference docs. Triggers on: "Discord", "Telegram", "WhatsApp", "Signal", "Slack", "channel config", "dmPolicy", "group policy", "allowFrom", "pairing", "broadcast groups", "add discord", "setup telegram", "link whatsapp", "how to add channel", "connect a channel", "channel setup", "channel pairing".
---

# OpenClaw Channels

## Quick config

```json
{
  "channels": {
    "discord":    { "token": "BOT", "dmPolicy": "pairing" },
    "telegram":   { "botToken": "BOT", "dmPolicy": "pairing" },
    "whatsapp":   { "dmPolicy": "pairing" },
    "signal":     { "account": "+1...", "dmPolicy": "pairing" },
    "slack":      { "botToken": "xoxb-", "appToken": "xapp-" },
    "matrix":     { "homeserver": "https://matrix.example.org", "accessToken": "syt_..." },
    "feishu":     { "appId": "...", "appSecret": "..." },
    "line":       { "channelAccessToken": "...", "channelSecret": "..." },
    "googlechat": { "serviceAccountFile": "./sa.json" }
  }
}
```

## DM policy

| Policy | Behavior |
|--------|----------|
| `pairing` (default) | Code → approve via `openclaw pairing approve` |
| `allowlist` | Only `allowFrom` list |
| `open` | Allow all (`allowFrom: ["*"]`) |
| `disabled` | Ignore all |

## Channel matrix (highlights)

| Channel | Multi-account | Notes |
|---------|--------------|-------|
| Discord | ✅ | Threads, exec approvals, role routing |
| Telegram | ✅ | Forum topics, streaming |
| WhatsApp | ✅ | Broadcast groups, QR pairing |
| Signal | ❌ | signal-cli daemon required |
| Slack | ✅ | Socket/ HTTP Mode |
| Matrix | ✅ | E2EE, multi-account |
| iMessage | ❌ | Full Disk Access required |
| Feishu | ✅ | Streaming cards, ACP bindings |

## Pairing

```bash
openclaw pairing list <channel>
openclaw pairing approve <channel> <CODE>
```

## References

- `references/discord.md` — Discord setup, threads, exec approvals
- `references/telegram.md` — Telegram setup, forum topics
- `references/whatsapp.md` — WhatsApp pairing, broadcast groups
- `references/slack.md` — Slack setup, Socket/HTTP mode
- `references/pairing.md` — pairing flow, code approval
- `references/channel-routing.md` — routing rules, match conditions
- `references/broadcast-groups.md` — broadcast group config
- `references/channel-index.md` — all 31 channel overviews
