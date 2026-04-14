---
name: openclaw-channels
description: OpenClaw channel configuration. Use when setting up, auditing, or troubleshooting any messaging channel: Discord, Telegram, WhatsApp, Slack, Signal, Matrix, iMessage, IRC, Feishu, LINE, GoogleChat, Mattermost, Microsoft Teams, Nextcloud Talk, Nostr, QQ Bot, Synology Chat, Twitch, Tlon, Zalo, Voice Call. Triggers on: "Discord", "Telegram", "WhatsApp", "Signal", "Slack", "channel config", "dmPolicy", "group policy", "allowFrom", "pairing", "broadcast groups".
---

# OpenClaw Channels

## Quick config cheatsheet

```json5
channels: {
  discord:    { token: "BOT", dmPolicy: "pairing", allowFrom: ["ID"] },
  telegram:   { botToken: "BOT", dmPolicy: "pairing", allowFrom: ["tg:ID"] },
  whatsapp:   { dmPolicy: "pairing", allowFrom: ["+1..."] },
  signal:     { account: "+1...", dmPolicy: "pairing", allowFrom: ["+1..."] },
  slack:      { botToken: "xoxb-", appToken: "xapp-", dmPolicy: "pairing" },
  matrix:     { homeserver: "https://matrix.example.org", accessToken: "syt_..." },
  feishu:     { appId: "...", appSecret: "..." },
  line:       { channelAccessToken: "...", channelSecret: "..." },
  googlechat: { serviceAccountFile: "./sa.json" },
  irc:        { servers: [{ server: "irc.libera.chat", ports: { ssl: 6697 } }] },
}
```

## DM policy

| Policy | Behavior |
|--------|----------|
| `pairing` (default) | Code → owner approves via `/openclaw pairing approve` |
| `allowlist` | Only `allowFrom` list |
| `open` | Allow all (`allowFrom: ["*"]`) |
| `disabled` | Ignore all |

## Group policy

| Policy | Behavior |
|--------|----------|
| `allowlist` (default) | Only configured groups |
| `open` | Bypass allowlists |
| `disabled` | Block all |

> **DM pairing ≠ group authorization.** Approving a DM pairing code only unlocks DMs. Group access requires explicit `groupAllowFrom`, per-group `allowFrom`, or channel-specific allowlists.

## All channels reference

| Channel | Key config | Multi-account | Notes |
|---------|-----------|--------------|-------|
| `discord` | `token` | ✅ | Threads, role routing, exec approvals |
| `telegram` | `botToken` | ✅ | Forum topics, custom commands, streaming |
| `whatsapp` | Baileys (auto) | ✅ | Broadcast groups (parallel/sequential), QR pairing |
| `signal` | `account` | ❌ | signal-cli daemon required |
| `slack` | `botToken` + `appToken` | ✅ | Socket Mode or HTTP Mode |
| `matrix` | `accessToken` | ✅ | E2EE, multi-account |
| `imessage` | `cliPath` + `remoteHost` | ❌ | Full Disk Access required |
| `mattermost` | bot token + WebSocket | ✅ | Native slash commands, multi-server |
| `msteams` | Azure Bot app ID + secret/tenant | ✅ | Certificate auth, Graph permissions |
| `irc` | server + port + SSL | ✅ | NickServ identify, `dangerouslyAllowNameMatching` |
| `feishu` | `appId` + `appSecret` | ✅ | Streaming cards, ACP bindings |
| `googlechat` | service account JSON | ✅ | DMs + named spaces, webhook via reverse proxy |
| `line` | `channelAccessToken` + `channelSecret` | ❌ | Quick replies, Flex cards, template messages |
| `nstr` | `nsec` / hex privkey + relay list | ✅ | NIP-04 DMs, profile metadata (NIP-01) |
| `qqbot` | AppID + AppSecret | ✅ | Slash commands, STT/TTS, multi-account |
| `synology-chat` | webhook URL + token | ✅ | Multi-header token acceptance |
| `twitch` | OAuth token + ClientID | ✅ | Role allowlist (mod/owner/vip/sub/all), token refresh |
| `nextcloud-talk` | bot secret + base URL | ✅ | Room type lookup (DM vs room) |
| `tlon` | ship URL + code + ownerShip | ✅ | Bundled `@tloncorp/tlon-skill` (contacts, DMs, groups) |
| `zalo` | bot token + webhook | ❌ | Long-poll, 2000-char limit |
| `zalouser` | QR login | ❌ | `zca-js` in-process browser |
| `bluebubbles` | server + password | ✅ | |
| `nostr` | `nsec` / hex privkey | ✅ | npub/hex pubkey, relay list |
| `voice-call` | Twilio/Plivo/Telnyx config | ❌ | Plugin: `@openclaw/voice-call` |

## Voice Call (plugin)

Separate plugin install:
```bash
openclaw plugins install @openclaw/voice-call
```
Config under `plugins.entries.voice-call.config`. Providers: `twilio`, `telnyx`, `plivo`, `mock`.

## Session key shapes

| Type | Key shape |
|------|----------|
| Direct messages | `agent:<agentId>:main` (collapsed when `session.dmScope: "main"`) |
| Groups | `agent:<agentId>:<channel>:group:<id>` |
| Channels/rooms | `agent:<agentId>:<channel>:channel:<id>` |
| Slack threads | `agent:<agentId>:slack:channel:<C>:thread:<T>` |
| Discord threads | `agent:<agentId>:discord:channel:<C>:thread:<T>` |
| Telegram forum topics | `agent:<agentId>:telegram:group:<G>:topic:<T>` |

## Threading patterns

| Channel | Thread support |
|---------|---------------|
| Discord | `threadBindings` config, `/focus`/`/unfocus` per thread |
| Slack | Threaded replies via `:thread:<T>` key |
| Telegram | Forum topics (each topic = own session with per-topic skills) |
| Tlon | Auto-replies in-thread when inbound is in a thread |

## Channel ID stability

Prefer numeric IDs over usernames (usernames are mutable):

| Channel | ID type | Stable? |
|---------|---------|---------|
| Telegram | `123456789`, `tg:123456789`, `@username` | Numeric stable, @mutable |
| Discord | Numeric user ID | ✅ Stable |
| Slack | `U123...` | ✅ Stable |
| WhatsApp | E.164: `+15551234567` | ✅ Stable |
| Signal | E.164 | ✅ Stable |
| LINE | `U+32hex` (user), `C+32hex` (group) | Case-sensitive |
| IRC | `nick!user@host` | Both mutable |
| Matrix | `@user:example.org` | ✅ Stable |
| Feishu | open_id: `ou_xxx`, chat_id: `oc_xxx` | ✅ Stable |
| GoogleChat | `users/<id>`, `spaces/<id>` | ✅ Stable |
| QQ | OpenID per bot | Per-bot |
| Nostr | `npub...` or hex pubkey | ✅ Stable |
| Tlon | Urbit ship: `~sampel-palnet` | ✅ Stable |
| Zalo | numeric user ID | ✅ Stable |

## Binding match order (most-specific wins)

1. `peer` (exact DM/group/channel id)
2. `parentPeer` (thread inheritance)
3. `guildId + roles` (Discord role routing)
4. `guildId`
5. `teamId` (Slack)
6. `accountId` match
7. channel-level (`accountId: "*"`)
8. default agent

## Rate limits by channel

| Channel | Text limit | Media limit |
|---------|-----------|-------------|
| LINE | 5000 chars (chunked) | |
| Telegram | 4096 chars | |
| WhatsApp | — | `mediaMaxMb: 50` default |
| GoogleChat | — | `mediaMaxMb: 20` |
| Feishu | 2000 chars | `mediaMaxMb: 30` |
| Zalo | 2000 chars, no streaming | `mediaMaxMb: 5` |
| Synology Chat | — | `rateLimitPerMinute: 30` per sender |
| Twitch | 500 chars, auto-chunked | |

## Per-group/channel tool restrictions

Some channels support `tools` + `toolsBySender` inside group configs:

```json5
channels: {
  telegram: {
    groups: {
      "-1001234567890": {
        tools: { allow: ["read", "memory_search"], deny: ["exec", "write"] }
      }
    }
  },
  irc: {
    groups: {
      "#channel": {
        tools: { allow: ["read"] },
        toolsBySender: { "nick!user@host": { deny: ["exec"] } }
      }
    }
  }
}
```

Resolution order: `toolsBySender` (most specific) → group `tools` → default `toolsBySender` → default `tools`.

## Pairing

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

- Codes expire after **1 hour**
- Max **3 pending** per channel
- Channels supporting `pairing`: discord, telegram, whatsapp, signal, slack, matrix, feishu, googlechat, irc, line, mattermost, msteams, nextcloud-talk, nostr, signal, synology-chat, twitch, bluebubbles, imessage, zalo, zalouser

## Broadcast groups (WhatsApp only, experimental)

```json5
broadcast: {
  strategy: "parallel",  // or "sequential"
  peers: {
    "+15551234567": {},
    "+15559876543": {}
  }
}
```
- Precedence: `broadcast` > `bindings`
- Each peer gets isolated session + workspace + tool access
- Does NOT bypass channel allowlists

## Discord-specific

```json5
channels: {
  discord: {
    token: "BOT_TOKEN",
    dmPolicy: "pairing",
    allowFrom: ["1234567890"],
    guilds: {
      "GUILD_ID": {
        channels: {
          "CHANNEL_ID": { allow: true, requireMention: false }
        }
      }
    },
    threadBindings: { enabled: true, idleHours: 24 },
    execApprovals: { enabled: "auto", approvers: ["USER_ID"] }
  }
}
```

## Telegram-specific

```json5
channels: {
  telegram: {
    botToken: "BOT_TOKEN",
    dmPolicy: "pairing",
    allowFrom: ["tg:123456789"],
    groups: {
      "*": { requireMention: true },
      "-1001234567890": { requireMention: false, topics: { "99": { skills: ["docs"] } } }
    },
    streaming: "partial",
    replyToMode: "first"
  }
}
```

## Feishu-specific

```json5
channels: {
  feishu: {
    appId: "APP_ID",
    appSecret: "APP_SECRET",
    dmPolicy: "pairing",
    typingIndicator: true,
    resolveSenderNames: true
  }
}
```

Supports streaming card output for ACP sessions. ACP binding persistent via config + `/acp spawn --thread here`.

## GoogleChat-specific

```json5
channels: {
  googlechat: {
    serviceAccountFile: "./sa.json",  // or serviceAccountRef
    audienceType: "default",
    audience: "spaces/...",
    botUser: "users/..."
  }
}
```

Webhook exposure requires reverse proxy (Tailscale Funnel or similar). DMs use `spaces/` format.

## IRC-specific

```json5
channels: {
  irc: {
    servers: [{
      server: "irc.libera.chat",
      ports: { ssl: 6697 },
      nick: "BotNick",
      nickserv: { identify: "password" }
    }],
    channels: { "#room": { allow: true } },
    dangerouslyAllowNameMatching: false
  }
}
```

## LINE-specific

```json5
channels: {
  line: {
    channelAccessToken: "TOKEN",
    channelSecret: "SECRET"
  }
}
```

Supports quick replies, Flex cards, template messages. Use Flex cards for code/tables (5000-char chunking for text).

## Nostr-specific

```json5
channels: {
  nostr: {
    privateKey: "nsec1...",  // or hex
    relays: ["wss://relay.example.com"]
  }
}
```

Supports NIP-04 DMs. Profile metadata via NIP-01 (`name`/`picture`/`banner`/`nip05`/`lud16`).

## QQ Bot-specific

```json5
channels: {
  qqbot: {
    appId: "APP_ID",
    appSecret: "APP_SECRET",
    slashCommands: true,
    audioFormatPolicy: "convert"
  }
}
```

Supports slash commands (`/bot-ping`, `/bot-help`). STT/TTS config available. Multi-account via separate bot entries.

## Twitch-specific

```json5
channels: {
  twitch: {
    oauthToken: "oauth:...",
    clientId: "CLIENT_ID",
    clientSecret: "CLIENT_SECRET",
    allowedRoles: ["moderator", "owner"],
    requireMention: true
  }
}
```

Token auto-refreshes on expiry. No built-in rate limit — relies on Twitch limits.

## References

- `references/discord.md` — full Discord reference
- `references/telegram.md` — Telegram reference
- `references/whatsapp.md` — WhatsApp reference
- `references/slack.md` — Slack reference
- `references/channel-routing.md` — routing rules + session key shapes
- `references/pairing.md` — pairing + node device pairing
- `references/broadcast-groups.md` — WhatsApp broadcast groups
- `references/channel-troubleshooting.md` — per-channel failure signatures (WhatsApp, Telegram, Discord, Slack, iMessage/BlueBubbles, Signal, QQ Bot, Matrix)
- `references/index.md` — channel overview + directory
- `references/group-messages.md` — group message handling
- `references/groups.md` — group policy + authorization patterns
