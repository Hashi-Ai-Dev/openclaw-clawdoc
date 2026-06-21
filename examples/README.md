# ClawDoc Examples

Ready-to-use OpenClaw config examples. Each file is a complete, validated `openclaw config merge` input — paste, merge, restart, and you have a working feature.

| File | Purpose | When to use |
|------|---------|-------------|
| `codex-harness.json` | Codex app-server harness plugin config | Running an ACP Codex sub-agent |
| `discord-full.json` | Full Discord setup with allowFrom, group policy, slash commands | Starting a new Discord agent |
| `discord-single.json` | Single-server Discord config (no DMs) | Bot for one specific server |
| `discord-telegram.json` | Dual Discord + Telegram agent | Multi-channel agent that lives in both |
| `honcho-memory.json` | Honcho memory backend wiring | Switching memory from builtin to Honcho |
| `imessage-native.json` | Native iMessage channel via `imsg` CLI (replaces BlueBubbles) | Setting up the current iMessage channel |
| `install-verify.json` | Post-install sanity check (no-op) | After install, verify the config parses |
| `matrix-channel.json` | Matrix channel setup with homeserver + access token | Connecting to a Matrix homeserver |
| `memory-builtin.json` | Default sqlite-vec builtin memory | Fresh install, no external backend |
| `memory-honcho.json` | Honcho memory + active memory | Production memory with cross-session recall |
| `memory-qmd.json` | QMD memory backend (file-based) | Lightweight memory without external services |
| `msteams-channel.json` | Microsoft Teams channel with bot framework | Connecting a Teams workspace |
| `multi-agent-discord.json` | Multiple agents sharing a Discord guild | Fleet setup (main + claw-doc + others) |
| `per-agent-sandbox.json` | Per-agent sandboxing via Docker | Hard isolation between agents |
| `production-deploy.json` | Production deployment hardening (restart policy, logs, backups) | Going from dev to production |
| `signal-channel.json` | Signal channel via signal-cli | Connecting a Signal number |
| `skill-workshop.json` | Skill Workshop flow (propose → review → approve → publish) | Iterating on new skills |
| `slack-channel.json` | Slack channel with bot token + signing secret | Connecting a Slack workspace |
| `sms-channel.json` | Twilio SMS channel with webhooks + allowlists | Adding SMS as a channel |
| `tts-minimax.json` | TTS provider config (minimax voice) | Adding text-to-speech to a channel |
| `webhook-basic.json` | Inbound webhook for cron-triggered events | Setting up a webhook listener |
| `wechat-channel.json` | Tencent iLink Bot (openclaw-weixin) WeChat channel | Connecting WeChat via iLink |
| `whatsapp-channel.json` | WhatsApp channel via WhatsApp Web multi-device | Connecting a WhatsApp number |
| `zalo-channel.json` | Zalo ClawBot channel (QR-code login, owner-bound) | Connecting a Zalo account |

## Usage

```bash
# Pick an example, copy to your workspace, edit placeholders, merge
cp examples/discord-full.json ~/.openclaw/workspace/
${EDITOR:-vi} ~/.openclaw/workspace/discord-full.json   # replace YOUR_DISCORD_TOKEN
openclaw config merge ~/.openclaw/workspace/discord-full.json
openclaw gateway restart
```

All examples are validated by `scripts/validate_repo.py` and round-trip cleanly through `openclaw config merge` against the tracked OpenClaw version in `CLAWDOC_MANIFEST.json`.
