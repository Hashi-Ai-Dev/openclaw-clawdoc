# ClawDoc Quickstart

Get ClawDoc running in under 10 minutes. This guide covers the essential path: install OpenClaw, point it at ClawDoc's skills, and verify everything works.

---

## Prerequisites

- OpenClaw installed (`curl -fsSL https://openclaw.ai/install.sh | bash`)
- A model provider account (MiniMax, OpenAI, or any [supported provider](./skills/openclaw-providers/))
- Discord bot token (for Discord setup)

---

## Step 1 — Configure a Model

OpenClaw needs a default model before it can run agents.

```bash
# MiniMax (recommended — free tier available)
openclaw config set agents.defaults.model.primary "minimax/MiniMax-M2.7"
openclaw config set auth.profiles.minimax.provider "minimax"

# Or OpenAI
openclaw config set agents.defaults.model.primary "openai/gpt-4o"
openclaw config set auth.profiles.openai.provider "openai"
openclaw config set auth.profiles.openai.apiKey "your-api-key"
```

Verify:
```bash
openclaw doctor --non-interactive
```

---

## Step 2 — Add ClawDoc Skills

```bash
# Option A: Add the full skill tree
openclaw skills add /path/to/clawdoc/skills

# Option B: Copy skills directly into your OpenClaw workspace
cp -r skills/* ~/.openclaw/skills/
```

Restart the gateway:
```bash
openclaw gateway restart
```

---

## Step 3 — Configure a Channel (Discord example)

```bash
# Set your Discord bot token
openclaw config set channels.discord.token "YOUR_BOT_TOKEN"
openclaw config set channels.discord.enabled true
```

Create a minimal channel config. Save as `~/.openclaw/discord-quick.json`:

```json
{
  "channels": {
    "discord": {
      "dmPolicy": "pairing",
      "guilds": {
        "YOUR_GUILD_ID": {
          "requireMention": false,
          "users": ["YOUR_USER_ID"],
          "channels": {
            "YOUR_CHANNEL_ID": {
              "allow": true
            }
          }
        }
      }
    }
  }
}
```

Apply it:
```bash
openclaw config merge ~/.openclaw/discord-quick.json
openclaw gateway restart
```

---

## Step 4 — Verify

```bash
openclaw doctor --non-interactive
```

You should see:
- ✅ Gateway running
- ✅ Model configured
- ✅ Discord connected
- ✅ Skills loaded

---

## What to Try First

Once running, ask ClawDoc your first question:

```
@your-agent How do I configure memory Search with embeddings?
```

ClawDoc will route to the right skill, read the reference docs, and give you a precise answer.

---

## Common First Tasks

| Task | Command |
|------|---------|
| Configure TTS | See `examples/tts-minimax.json` |
| Set up Honcho memory | See `examples/memory-honcho.json` |
| Add a second channel | See `examples/discord-telegram.json` |
| Lock down an agent | See `examples/per-agent-sandbox.json` |

---

## Next Steps

- Browse [`skills/`](./skills/) to see all 11 available skills
- Check [`examples/`](./examples/) for ready-to-use config snippets
- Read [`CONTRIBUTING.md`](./CONTRIBUTING.md) if you want to extend or fork ClawDoc
