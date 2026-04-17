---
name: openclaw-setup
description: OpenClaw first-run setup, wizardless install, model configuration, and channel onboarding. Use when installing OpenClaw from scratch, configuring the first model, setting up Discord/Telegram/WhatsApp/other channels, or recovering from a broken wizard run. Triggers on: "install openclaw", "setup openclaw", "first run", "wizardless install", "configure model", "set up discord", "onboarding", "OPENCLAW_NO_ONBOARD", "openclaw config set".
---

# OpenClaw Setup

## Binary not found after install

OpenClaw installs to non-standard npm paths. ALWAYS verify with:
```bash
find ~ -name openclaw -type f 2>/dev/null
```
Common locations: `~/.hermes/node/bin/`, `~/.local/bin/`, `~/.npm/global/bin/`

Add to PATH permanently:
```bash
export PATH="/FULL/PATH/FOUND/bin:$PATH"
echo 'export PATH="/FULL/PATH/FOUND/bin:$PATH"' >> ~/.bashrc
```

## Wizardless install (recommended)

The installer wizard can crash on the channel selection step. Skip it entirely:
```bash
OPENCLAW_NO_ONBOARD=1 curl -fsSL https://openclaw.ai/install.sh | bash
```

After install completes, configure manually.

## Model configuration

```bash
# Set primary model
openclaw config set agents.defaults.model.primary "google/gemini-2.5-flash"

# Set auth profile for the provider
openclaw config set auth.profiles.google.provider "google"
openclaw config set auth.profiles.openai.provider "openai"
openclaw config set auth.profiles.anthropic.provider "anthropic"
```

Free tier options:
- **Google Gemini**: `google/gemini-2.5-flash` — free via Google AI Studio
- **OpenAI**: `openai/gpt-4o-mini` — free key at platform.openai.com

## Channel setup

### Discord
```bash
openclaw config set channels.discord.token "YOUR_BOT_TOKEN"
openclaw config set channels.discord.enabled true
```

### Telegram
```bash
openclaw config set channels.telegram.botToken "YOUR_BOT_TOKEN"
openclaw config set channels.telegram.enabled true
```

### WhatsApp
```bash
openclaw config set channels.whatsapp.botToken "YOUR_BOT_TOKEN"
openclaw config set channels.whatsapp.enabled true
```

## Start the gateway
```bash
openclaw gateway start
```

## Post-install verification
```bash
openclaw status
openclaw doctor
```

## If the wizard was used and crashed

1. Check if install partially completed:
```bash
ls ~/.openclaw/
openclaw --version
```
2. If binary exists but wizard crashed — run `OPENCLAW_NO_ONBOARD=1` install again, it won't re-download
3. If fully broken — clear config and retry:
```bash
rm -rf ~/.openclaw
OPENCLAW_NO_ONBOARD=1 curl -fsSL https://openclaw.ai/install.sh | bash
```
