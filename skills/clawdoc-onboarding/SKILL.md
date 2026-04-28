---
name: clawdoc-onboarding
description: Guided first-run setup for ClawDoc. Checks OpenClaw install state, walks through model setup, first channel connection, and end-to-end verification. Triggers on: "first time setup", "getting started with ClawDoc", "onboard", "new install", "initial setup", "how do I set up ClawDoc", "ClawDoc first run".
---

# ClawDoc Onboarding

Walk a new ClawDoc user through their first successful setup in under 15 minutes.

## What it checks

1. **OpenClaw installed** — binary reachable, gateway can start
2. **Model configured** — primary model set + auth configured
3. **First channel connected** — Discord, Telegram, or other
4. **Verification** — agent responds to first message

## Step-by-step

### Step 1 — Verify OpenClaw install

```bash
openclaw --version
openclaw gateway status
```

If gateway won't start → troubleshoot install first.

### Step 2 — Configure model

Prompt user to pick a provider:

| Provider | Effort | Best for |
|----------|--------|----------|
| MiniMax | Low — free tier | New users, fast setup |
| OpenAI | Medium — needs API key | Advanced users |
| Gemini | Medium — needs API key | Advanced users |
| Ollama | High — local setup | Self-hosted enthusiasts |

For MiniMax (recommended):
```bash
openclaw config set agents.defaults.model.primary "minimax/MiniMax-M2.7"
openclaw config set auth.profiles.minimax.provider "minimax"
```

### Step 3 — Connect first channel

**Discord (most common):**
```bash
openclaw config set channels.discord.token "YOUR_BOT_TOKEN"
openclaw config set channels.discord.enabled true
openclaw gateway restart
```

Verify DM policy and pairing:
```bash
openclaw pairing approve discord <CODE>
```

**Telegram:**
```bash
openclaw config set channels.telegram.token "YOUR_BOT_TOKEN"
openclaw config set channels.telegram.enabled true
```

### Step 4 — Install ClawDoc skills

```bash
# Via clawdhub (recommended)
clawdhub install https://github.com/Hashi-Ai-Dev/openclaw-clawdoc

# Or manual clone
git clone https://github.com/Hashi-Ai-Dev/openclaw-clawdoc.git ~/.openclaw/skills/openclaw
```

### Step 5 — End-to-end verification

Ask user to send a test message:
```
@your-agent "Hello, are you working?"
```

Expected: agent responds within 10 seconds.

## Common first-run failures

| Symptom | Fix |
|---------|-----|
| "command not found" | OpenClaw not in PATH — check install location |
| "invalid config" | `openclaw doctor --fix` to auto-repair |
| Discord bot silent | Verify Message Content Intent enabled in Discord Developer Portal |
| Model auth failing | Check API key format, account credits |
| Gateway won't start | Port 18789 already in use — `openclaw gateway restart` |

## Output

```
## Onboarding Checklist — [date]

### Install
- [ ] openclaw --version succeeds
- [ ] Gateway can start

### Model
- [ ] Primary model set
- [ ] Auth configured

### Channel
- [ ] First channel connected
- [ ] Bot responds to DMs

### ClawDoc
- [ ] Skills installed
- [ ] Agent responds correctly

### Verification
- [ ] First test message succeeded
```

## References

- `references/first-run-guide.md` — detailed first-run steps
