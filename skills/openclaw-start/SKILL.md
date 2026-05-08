---
name: openclaw-start
description: First run, bootstrapping, and onboarding OpenClaw. Use when: running OpenClaw for the first time, using the setup wizard, configuring the workspace, bootstrapping an agent, understanding the onboarding flow, using openclaw onboard CLI. Triggers on: "start", "bootstrap", "onboarding", "wizard", "first run", "getting started", "setup", "onboard", "initial", "new install", "fresh install", "how do I start", "where do I begin".
---

# OpenClaw Start Reference

## Onboarding paths

| Path | When to use |
|------|-------------|
| [Wizard CLI](./references/wizard-cli-reference.md) | Full interactive setup via `openclaw onboard` |
| [Wizard automation](./references/wizard-cli-automation.md) | Non-interactive / scripted onboarding |
| [Getting started](https://docs.openclaw.ai/start/getting-started) | Official docs: install → run → chat |

## openclaw onboard

Non-interactive flags for scripted setups:

```bash
# Full non-interactive install
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard

# Reset existing install before re-onboarding
openclaw onboard --reset

# Set up with specific model
openclaw onboard --model "minimax/MiniMax-M2.7"
```

## What the wizard covers

1. **Model + auth** — API key or OAuth for your chosen provider
2. **Workspace** — where agent files, memory, and config live
3. **Gateway** — port, bind address, auth mode, Tailscale
4. **Channels** — Discord, Telegram, WhatsApp, Signal, and others
5. **Daemon** — keep gateway running after logout (LaunchAgent/systemd)

## Workspace bootstrap

OpenClaw seeds these files on first run:

| File | Purpose |
|------|---------|
| `SOUL.md` | Agent personality + behavior |
| `USER.md` | User context |
| `AGENTS.md` | Workspace conventions |
| `TOOLS.md` | Local tool notes |
| `MEMORY.md` | Long-term memory (optional) |
| `HEARTBEAT.md` | Periodic task checklist |

## Key concepts

- [Wizard CLI reference](./references/wizard-cli-reference.md) — full detail on every wizard step
- [Wizard automation](./references/wizard-cli-automation.md) — CI/scripted onboarding flags
- [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace) — workspace file layout

## References

- `references/wizard-cli-reference.md` — complete wizard reference
- `references/wizard-cli-automation.md` — non-interactive flags and CI usage
