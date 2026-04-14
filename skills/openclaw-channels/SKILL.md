---
name: openclaw-channels
description: OpenClaw channel configuration. Use when setting up Discord, Telegram, WhatsApp, Signal, Slack, Matrix, or any messaging channel. Triggers on: "Discord", "Telegram", "WhatsApp", "Signal", "Slack", "channel config", "dmPolicy", "group policy", "allowFrom".
---

# OpenClaw Channels

## DM and Group policies

| DM Policy | Behavior |
|-----------|----------|
| `pairing` (default) | Pairing code → owner approves |
| `allowlist` | Only `allowFrom` list |
| `open` | Allow all (`allowFrom: ["*"]`) |
| `disabled` | Ignore all |

| Group Policy | Behavior |
|--------------|----------|
| `allowlist` (default) | Only configured groups |
| `open` | Bypass allowlists |
| `disabled` | Block all |

## Discord

```json5
channels: {
  discord: {
    token: "BOT_TOKEN",
    dmPolicy: "pairing",
    allowFrom: ["1234567890"],
    guilds: {
      "GUILD_ID": {
        channels: {
          "CHANNEL_ID": { allow: true, requireMention: false },
          "help": { allow: true, requireMention: true, skills: ["docs"] }
        }
      }
    },
    threadBindings: { enabled: true, idleHours: 24 },
    voice: { enabled: false },
    execApprovals: { enabled: "auto", approvers: ["USER_ID"] }
  }
}
```

**Key fields:**
- `token` or `DISCORD_BOT_TOKEN` env
- `dmPolicy`: `pairing|allowlist|open|disabled`
- `allowFrom`: Discord user IDs
- `guilds.<id>.channels.<id>.requireMention`: gating
- `guilds.<id>.channels.<id>.skills`: per-channel skill allowlist
- `threadBindings.enabled`: Discord thread-bound routing for `/focus`, `/unfocus`, `/agents`
- `execApprovals`: Discord-native exec approval delivery

## Telegram

```json5
channels: {
  telegram: {
    botToken: "BOT_TOKEN",
    dmPolicy: "pairing",
    allowFrom: ["tg:123456789"],
    groups: {
      "*": { requireMention: true },
      "-1001234567890": { requireMention: false, topics: { "99": { skills: ["search"] } } }
    },
    customCommands: [{ command: "backup", description: "Git backup" }],
    streaming: "partial",
    replyToMode: "first"
  }
}
```

## WhatsApp

```json5
channels: {
  whatsapp: {
    dmPolicy: "pairing",
    allowFrom: ["+15555550123"],
    groupPolicy: "allowlist",
    groupAllowFrom: ["+15551234567"],
    mediaMaxMb: 50,
    sendReadReceipts: true
  }
}
```

Multi-account:
```json5
channels: {
  whatsapp: {
    accounts: {
      default: {},
      personal: {},
      biz: {}
    }
  }
}
```

## Slack

```json5
channels: {
  slack: {
    botToken: "xoxb-...",
    appToken: "xapp-...",
    dmPolicy: "pairing",
    allowFrom: ["U123", "*"],
    channels: {
      "C123": { allow: true, requireMention: true }
    },
    execApprovals: { enabled: "auto", approvers: ["U123"] }
  }
}
```

Requires Socket Mode (`botToken` + `appToken`) or HTTP Mode (`botToken` + `signingSecret`).

## Signal

```json5
channels: {
  signal: {
    account: "+15555550123",
    dmPolicy: "pairing",
    allowFrom: ["+15551234567"]
  }
}
```

## Matrix

```json5
channels: {
  matrix: {
    homeserver: "https://matrix.example.org",
    accessToken: "syt_bot_xxx",
    encryption: true,
    accounts: {
      ops: { userId: "@ops:example.org", accessToken: "syt_ops_xxx" },
      alerts: { userId: "@alerts:example.org", password: "secret" }
    }
  }
}
```

## iMessage

```json5
channels: {
  imessage: {
    enabled: true,
    cliPath: "imsg",
    remoteHost: "user@gateway-host",
    dmPolicy: "pairing",
    allowFrom: ["+15555550123"]
  }
}
```
Requires Full Disk Access to Messages DB.

## All channels summary

| Channel | Key Config | Multi-account |
|---------|-----------|---------------|
| `discord` | `token` | ✅ |
| `telegram` | `botToken` | ✅ |
| `whatsapp` | auto (Baileys) | ✅ |
| `signal` | `account` | ❌ |
| `slack` | `botToken` + `appToken` | ✅ |
| `matrix` | `accessToken` | ✅ |
| `imessage` | `cliPath` | ❌ |
| `mattermost` | plugin | ❌ |
| `msteams` | plugin | ❌ |
| `irc` | plugin | ❌ |

## All channels summary

| Channel | Key Config | Multi-account | Notes |
|---------|-----------|---------------|-------|
| `discord` | `token` | ✅ | Voice, threads, exec approvals |
| `telegram` | `botToken` | ✅ | Topics, custom commands, streaming |
| `whatsapp` | auto (Baileys) | ✅ | Broadcast groups (experimental) |
| `signal` | `account` | ❌ | |
| `slack` | `botToken` + `appToken` | ✅ | Socket Mode or HTTP Mode |
| `matrix` | `accessToken` | ✅ | E2EE, multi-account |
| `imessage` | `cliPath` | ❌ | Full Disk Access required |
| `mattermost` | plugin | ❌ | |
| `msteams` | plugin | ❌ | |
| `irc` | plugin | ❌ | |


## Session key shapes

| Type | Key shape |
|------|----------|
| Direct messages | `agent:<agentId>:main` (collapsed) |
| Groups | `agent:<agentId>:<channel>:group:<id>` |
| Channels/rooms | `agent:<agentId>:<channel>:channel:<id>` |
| Slack threads | Appends `:thread:<threadId>` |
| Discord threads | Appends `:thread:<threadId>` |
| Telegram forum topics | Embeds `:topic:<topicId>` in group key |

## Pairing (DM access control)

When `dmPolicy: "pairing"`, unknown senders get an 8-char code and must be approved:
```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```
Codes expire after 1 hour. Max 3 pending per channel.

## Routing binding order (most-specific wins)

1. `peer` (exact DM/group/channel id)
2. `parentPeer` (thread inheritance)
3. `guildId + roles` (Discord role routing)
4. `guildId`
5. `teamId` (Slack)
6. `accountId` match
7. channel-level (`accountId: "*"`)
8. default agent

## References

- `references/discord-config.md` — full Discord reference
- `references/channel-policies.md` — DM/group policy details
- `references/channel-routing.md` — routing rules + session key shapes
- `references/pairing.md` — pairing + node device pairing
- `references/broadcast-groups.md` — WhatsApp broadcast groups
- `references/channel-troubleshooting.md` — per-channel failure signatures
