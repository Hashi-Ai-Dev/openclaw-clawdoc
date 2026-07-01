---
summary: "Messaging platforms OpenClaw can connect to"
read_when:
  - You want to choose a chat channel for OpenClaw
  - You need a quick overview of supported messaging platforms
title: "Chat Channels"
---

# Chat Channels

OpenClaw can talk to you on any chat app you already use. Each channel connects via the Gateway.
Text is supported everywhere; media and reactions vary by channel.

## Supported channels

- [iMessage](/channels/imessage) — **Recommended for iMessage**; native external CLI integration via `imsg` (JSON-RPC over stdio) with private API actions for replies, tapbacks, effects, attachments, and group management. Requires a signed-in macOS Messages host.
- [Discord](/channels/discord) — Discord Bot API + Gateway; supports servers, channels, and DMs.
- [Feishu](/channels/feishu) — Feishu/Lark bot via WebSocket (bundled plugin).
- [Google Chat](/channels/googlechat) — Google Chat API app via HTTP webhook.
- [IRC](/channels/irc) — Classic IRC servers; channels + DMs with pairing/allowlist controls.
- [ClickClack](/channels/clickclack) — ClickClack bot-token channel setup (bundled plugin).
- [LINE](/channels/line) — LINE Messaging API bot (bundled plugin).
- [Matrix](/channels/matrix) — Matrix protocol (bundled plugin).
- [Mattermost](/channels/mattermost) — Bot API + WebSocket; channels, groups, DMs (bundled plugin).
- [Microsoft Teams](/channels/msteams) — Bot Framework; enterprise support (bundled plugin).
- [Nextcloud Talk](/channels/nextcloud-talk) — Self-hosted chat via Nextcloud Talk (bundled plugin).
- [Nostr](/channels/nostr) — Decentralized DMs via NIP-04 (bundled plugin).
- [QQ Bot](/channels/qqbot) — QQ Bot API; private chat, group chat, and rich media (bundled plugin).
- [QA Channel](/channels/qa-channel) — Utility Q&A channel; lightweight scripted Q→A exchange without a chat UI (bundled plugin).
- [Signal](/channels/signal) — signal-cli; privacy-focused.
- [Slack](/channels/slack) — Bolt SDK; workspace apps.
- [SMS](/channels/sms) — Twilio SMS via webhook (bundled plugin); outbound and inbound.
- [Synology Chat](/channels/synology-chat) — Synology NAS Chat via outgoing+incoming webhooks (bundled plugin).
- [Telegram](/channels/telegram) — Bot API via grammY; supports groups.
- [Tlon](/channels/tlon) — Urbit-based messenger (bundled plugin).
- [Twitch](/channels/twitch) — Twitch chat via IRC connection (bundled plugin).
- [Voice Call](/plugins/voice-call) — Telephony via Plivo or Twilio (plugin, installed separately).
- [WebChat](/web/webchat) — Gateway WebChat UI over WebSocket.
- [WeChat](https://www.npmjs.com/package/@tencent-weixin/openclaw-weixin) — Tencent iLink Bot plugin via QR login; private chats only.
- [WhatsApp](/channels/whatsapp) — Most popular; uses Baileys and requires QR pairing.
- [Yuanbao](/channels/yuanbao) — Tencent Yuanbao channel via Yuanbao API (bundled plugin).
- [Zalo](/channels/zalo) — Zalo Bot API; Vietnam's popular messenger (bundled plugin).
- [Zalo ClawBot](/channels/zaloclawbot) — Zalo ClawBot (bundled plugin).
- [Zalo Personal](/channels/zalouser) — Zalo personal account via QR login (bundled plugin).

## Removed channels (migration-only)

- [BlueBubbles](/channels/bluebubbles) — **Removed in current OpenClaw.** BlueBubbles was the recommended iMessage path on older OpenClaw releases; current OpenClaw supports iMessage exclusively through the native `imsg` CLI. If you have a `channels.bluebubbles` config, migrate to `channels.imessage`. See [Coming from BlueBubbles](/channels/imessage-from-bluebubbles) for the config translation table and step-by-step cutover, or [/channels/imessage](/channels/imessage) for the current setup.

## Notes

- Channels can run simultaneously; configure multiple and OpenClaw will route per chat.
- Fastest setup is usually **Telegram** (simple bot token). WhatsApp requires QR pairing and
  stores more state on disk.
- Group behavior varies by channel; see [Groups](/channels/groups).
- DM pairing and allowlists are enforced for safety; see [Security](/gateway/security).
- Troubleshooting: [Channel troubleshooting](/channels/troubleshooting).
- Model providers are documented separately; see [Model Providers](/providers/models).

## Example

```json5
// Configure one channel in ~/.openclaw/openclaw.json
{
  "channels": {
    "discord": { "token": "***", "dmPolicy": "pairing" }
  }
}
```
